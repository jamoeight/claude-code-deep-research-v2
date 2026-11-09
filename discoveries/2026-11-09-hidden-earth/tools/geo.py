"""Imagery helpers for Operation Hidden Earth.

Pulls Sentinel-2 L2A true-colour chips (10 m) from the public `sentinel-cogs`
bucket and Copernicus GLO-30 DEM hillshades from `copernicus-dem-30m`, both via
HTTP range requests (no API keys, no STAC). Also builds Google Earth links.

Usage (CLI):
  python3 geo.py chip  <lat> <lon> <half_km> <out_prefix> [--months 2023-01,2023-02] [--label TEXT]
  python3 geo.py dem   <lat> <lon> <half_km> <out_prefix> [--label TEXT]
"""
from __future__ import annotations

import io
import json
import math
import os
import re
import sys
import urllib.request
from functools import lru_cache

os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif,.TIF")
os.environ.setdefault("GDAL_HTTP_MULTIRANGE", "YES")
os.environ.setdefault("GDAL_HTTP_MERGE_CONSECUTIVE_RANGES", "YES")
os.environ.setdefault("VSI_CACHE", "TRUE")
os.environ.setdefault("GDAL_CACHEMAX", "512")
if os.path.exists("/root/.ccr/ca-bundle.crt"):
    os.environ.setdefault("CURL_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")
    os.environ.setdefault("GDAL_CURL_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")

import numpy as np
import mgrs as mgrs_lib
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer
from PIL import Image, ImageDraw, ImageFont

S2_BASE = "https://sentinel-cogs.s3.us-west-2.amazonaws.com"
S2_PREFIX = "sentinel-s2-l2a-cogs"
DEM_BASE = "https://copernicus-dem-30m.s3.amazonaws.com"
_M = mgrs_lib.MGRS()


def _get(url: str, timeout: int = 60) -> bytes:
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return r.read()


def earth_link(lat: float, lon: float, alt_m: float = 3000, dist_m: float = 4000) -> str:
    return f"https://earth.google.com/web/@{lat:.5f},{lon:.5f},{alt_m:.0f}a,{dist_m:.0f}d,35y,0h,0t,0r"


def gmaps_link(lat: float, lon: float, zoom: int = 16) -> str:
    return f"https://www.google.com/maps/@{lat:.5f},{lon:.5f},{zoom}z/data=!3m1!1e3"


# ---------------------------------------------------------------- Sentinel-2
def mgrs_tile(lat: float, lon: float) -> str:
    return _M.toMGRS(lat, lon, MGRSPrecision=0)


def _tile_path(tile: str) -> str:
    m = re.match(r"(\d+)([A-Z])([A-Z]{2})", tile)
    zone, band, sq = m.groups()
    return f"{S2_PREFIX}/{int(zone)}/{band}/{sq}"


@lru_cache(maxsize=512)
def list_scenes(tile: str, year: int, month: int) -> tuple:
    url = f"{S2_BASE}/?list-type=2&delimiter=/&prefix={_tile_path(tile)}/{year}/{month}/"
    try:
        txt = _get(url).decode()
    except Exception:
        return tuple()
    return tuple(p for p in re.findall(r"<Prefix>([^<]+)</Prefix>", txt) if p.endswith("_L2A/"))


@lru_cache(maxsize=2048)
def scene_meta(prefix: str) -> dict:
    sid = prefix.rstrip("/").split("/")[-1]
    try:
        return json.loads(_get(f"{S2_BASE}/{prefix}{sid}.json"))
    except Exception:
        return {}


def _window_read(url: str, lat: float, lon: float, half_km: float, out_shape=None, resampling=None):
    with rasterio.open(url) as ds:
        tr = Transformer.from_crs("EPSG:4326", ds.crs, always_xy=True)
        x, y = tr.transform(lon, lat)
        h = half_km * 1000
        win = from_bounds(x - h, y - h, x + h, y + h, ds.transform)
        kw = dict(window=win, boundless=True, fill_value=0)
        if out_shape is not None:
            kw["out_shape"] = out_shape
            if resampling is not None:
                kw["resampling"] = resampling
        return ds.read(**kw)


def candidate_tiles(lat: float, lon: float, half_km: float) -> list[str]:
    d = half_km / 111.0
    dl = d / max(0.2, math.cos(math.radians(lat)))
    tiles = [mgrs_tile(lat, lon)]
    for a, b in [(lat + d, lon + dl), (lat - d, lon - dl), (lat + d, lon - dl), (lat - d, lon + dl)]:
        try:
            t = mgrs_tile(max(-79.9, min(83.9, a)), b)
        except Exception:
            continue
        if t not in tiles:
            tiles.append(t)
    return tiles


def find_clear_scene(lat, lon, half_km, months, max_scene_cloud=40, max_tries=14):
    """Return (prefix, local_cloud_frac, nodata_frac) of the clearest scene in the window."""
    from concurrent.futures import ThreadPoolExecutor
    jobs = [(t, *map(int, ym.split("-"))) for t in candidate_tiles(lat, lon, half_km) for ym in months]
    with ThreadPoolExecutor(16) as ex:
        lists = list(ex.map(lambda j: list_scenes(*j), jobs))
    cands = [p for L in lists for p in L]
    with ThreadPoolExecutor(24) as ex:
        metas = list(ex.map(scene_meta, cands))
    scored = []
    for p, md in zip(cands, metas):
        pr = md.get("properties", {})
        cc = pr.get("eo:cloud_cover", 100)
        nd = pr.get("s2:nodata_pixel_percentage", 100)
        if cc <= max_scene_cloud:
            scored.append((cc + 0.5 * nd, p))
    scored.sort()
    # keep the best few per MGRS tile so a tile-edge point still gets its proper tile checked
    per_tile, picked = {}, []
    for sc, p in scored:
        t = p.split("/")[-2].split("_")[1]
        if per_tile.get(t, 0) < max(3, max_tries // 3):
            per_tile[t] = per_tile.get(t, 0) + 1
            picked.append((sc, p))
    scored = picked

    def check(p):
        try:
            scl = _window_read(f"{S2_BASE}/{p}SCL.tif", lat, lon, half_km)[0]
        except Exception:
            return None
        nodata = float(np.mean(scl == 0))
        cloud = float(np.mean(np.isin(scl, [3, 8, 9, 10])))
        return (cloud + 1.5 * nodata, p, cloud, nodata)

    with ThreadPoolExecutor(8) as ex:
        res = [r for r in ex.map(check, [p for _, p in scored[:max_tries]]) if r]
    if not res:
        return None
    best = min(res)
    return best[1], best[2], best[3]


def _stretch(arr: np.ndarray, lo=2, hi=98) -> np.ndarray:
    out = np.zeros_like(arr, dtype=np.uint8)
    valid = arr > 0
    if valid.sum() < 10:
        return out
    a, b = np.percentile(arr[valid], [lo, hi])
    if b <= a:
        b = a + 1
    out = np.clip((arr.astype(float) - a) / (b - a) * 255, 0, 255).astype(np.uint8)
    return out


def s2_chip(lat, lon, half_km, months, enhance=True):
    found = find_clear_scene(lat, lon, half_km, months)
    if not found:
        return None, None
    p, cloud, nodata = found
    rgb = _window_read(f"{S2_BASE}/{p}TCI.tif", lat, lon, half_km)  # 3 x H x W uint8
    img = np.transpose(rgb, (1, 2, 0))
    if enhance:  # joint stretch keeps the colour balance natural
        valid = img.sum(axis=2) > 0
        if valid.sum() > 10:
            a, b = np.percentile(img[valid], [0.5, 99.7])
            img = np.clip((img.astype(float) - a) / max(1, b - a) * 255, 0, 255).astype(np.uint8)
    sid = p.rstrip("/").split("/")[-1]
    return img, {"scene": sid, "local_cloud": round(float(cloud), 3), "nodata": round(float(nodata), 3)}


def s2_band_chip(lat, lon, half_km, prefix, bands=("B12", "B08", "B04")):
    """False-colour composite from arbitrary bands (all resampled to 10 m grid)."""
    from rasterio.enums import Resampling
    ref = _window_read(f"{S2_BASE}/{prefix}B04.tif", lat, lon, half_km)
    shape = ref.shape[1:]
    chans = []
    for b in bands:
        arr = _window_read(f"{S2_BASE}/{prefix}{b}.tif", lat, lon, half_km,
                           out_shape=(1, *shape), resampling=Resampling.bilinear)[0]
        chans.append(_stretch(arr, 1, 99.5))
    return np.dstack(chans)


# ---------------------------------------------------------------- DEM
def _dem_name(lat_i: int, lon_i: int) -> str:
    ns = "N" if lat_i >= 0 else "S"
    ew = "E" if lon_i >= 0 else "W"
    return f"Copernicus_DSM_COG_10_{ns}{abs(lat_i):02d}_00_{ew}{abs(lon_i):03d}_00_DEM"


def dem_window(lat, lon, half_km, res_m=30.0):
    """Return (elev array in metres, pixel size m) on a local metric grid centred on lat/lon."""
    from rasterio.vrt import WarpedVRT
    from rasterio.enums import Resampling
    from rasterio.io import MemoryFile
    from rasterio.merge import merge

    d = half_km / 111.0 * 1.05
    dl = d / max(0.05, math.cos(math.radians(lat)))
    tiles = set()
    for a in (lat - d, lat + d):
        for b in (lon - dl, lon + dl):
            tiles.add((math.floor(a), math.floor(b)))
    srcs = []
    for la, lo in sorted(tiles):
        n = _dem_name(la, lo)
        url = f"{DEM_BASE}/{n}/{n}.tif"
        try:
            srcs.append(rasterio.open(url))
        except Exception:
            pass  # ocean tile or missing
    if not srcs:
        return None, None
    bounds = (lon - dl, lat - d, lon + dl, lat + d)
    mosaic, tr = merge(srcs, bounds=bounds, nodata=-9999)
    crs = srcs[0].crs
    for s in srcs:
        s.close()
    # reproject to local azimuthal equidistant grid
    from rasterio.warp import reproject
    aeqd = f"+proj=aeqd +lat_0={lat} +lon_0={lon} +datum=WGS84 +units=m"
    n = int(round(2 * half_km * 1000 / res_m))
    from rasterio.transform import from_origin
    dst_tr = from_origin(-half_km * 1000, half_km * 1000, res_m, res_m)
    dst = np.full((n, n), -9999, dtype=np.float32)
    reproject(mosaic[0].astype(np.float32), dst, src_transform=tr, src_crs=crs, src_nodata=-9999,
              dst_transform=dst_tr, dst_crs=aeqd, dst_nodata=-9999, resampling=Resampling.bilinear)
    dst[dst == -9999] = np.nan
    return dst, res_m


def hillshade(z, res, az=315, alt=35, zfactor=1.0):
    gy, gx = np.gradient(np.nan_to_num(z, nan=np.nanmean(z)) * zfactor, res)
    slope = np.pi / 2 - np.arctan(np.hypot(gx, gy))
    aspect = np.arctan2(-gx, gy)
    azr, altr = math.radians(360 - az + 90), math.radians(alt)
    hs = np.sin(altr) * np.sin(slope) + np.cos(altr) * np.cos(slope) * np.cos(azr - aspect)
    return np.clip(hs * 255, 0, 255).astype(np.uint8)


def dem_render(z, res, mode="hs+color"):
    hs = hillshade(z, res).astype(float) / 255
    zz = np.nan_to_num(z, nan=np.nanmin(z))
    a, b = np.nanpercentile(z, [2, 98])
    t = np.clip((zz - a) / max(1e-6, b - a), 0, 1)
    # simple terrain colormap: blue-green-yellow-brown-white
    stops = np.array([[40, 70, 140], [60, 140, 90], [200, 200, 110], [150, 100, 60], [245, 245, 245]], float)
    idx = t * (len(stops) - 1)
    i0 = np.floor(idx).astype(int).clip(0, len(stops) - 2)
    f = (idx - i0)[..., None]
    col = stops[i0] * (1 - f) + stops[i0 + 1] * f
    out = col * (0.35 + 0.65 * hs[..., None])
    return out.clip(0, 255).astype(np.uint8)


# ---------------------------------------------------------------- annotation
def annotate(img: np.ndarray, half_km: float, label: str = "", marker=True, footer: str = "") -> Image.Image:
    im = Image.fromarray(img).convert("RGB")
    W, H = im.size
    if W < 600:
        s = 600 / W
        im = im.resize((int(W * s), int(H * s)), Image.LANCZOS)
        W, H = im.size
    dr = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", max(12, W // 50))
        fsmall = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", max(10, W // 65))
    except Exception:
        font = fsmall = ImageFont.load_default()
    if marker:
        cx, cy, r = W // 2, H // 2, max(6, W // 60)
        dr.line([(cx - 3 * r, cy), (cx - r, cy)], fill=(255, 40, 40), width=2)
        dr.line([(cx + r, cy), (cx + 3 * r, cy)], fill=(255, 40, 40), width=2)
        dr.line([(cx, cy - 3 * r), (cx, cy - r)], fill=(255, 40, 40), width=2)
        dr.line([(cx, cy + r), (cx, cy + 3 * r)], fill=(255, 40, 40), width=2)
    # scale bar: choose nice length
    km_per_px = 2 * half_km / W
    nice = [0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
    L = min(nice, key=lambda v: abs(v / km_per_px - W * 0.2))
    px = int(L / km_per_px)
    x0, y0 = 15, H - 25
    dr.rectangle([x0 - 4, y0 - 22, x0 + px + 60, y0 + 10], fill=(0, 0, 0))
    dr.line([(x0, y0), (x0 + px, y0)], fill=(255, 255, 255), width=4)
    dr.text((x0 + px + 6, y0 - 14), f"{L:g} km", fill=(255, 255, 255), font=fsmall)
    if label:
        tw = dr.textlength(label, font=font)
        dr.rectangle([0, 0, tw + 16, font.size + 12], fill=(0, 0, 0))
        dr.text((8, 5), label, fill=(255, 255, 255), font=font)
    if footer:
        tw = dr.textlength(footer, font=fsmall)
        dr.rectangle([W - tw - 14, H - fsmall.size - 12, W, H], fill=(0, 0, 0))
        dr.text((W - tw - 7, H - fsmall.size - 7), footer, fill=(220, 220, 220), font=fsmall)
    return im


def default_months(lat: float, years=(2023, 2024, 2025)) -> list[str]:
    """Dry/clear-ish season months by hemisphere and latitude band."""
    if abs(lat) < 12:          # tropics: try a broad set, dry season varies
        ms = [1, 2, 3, 7, 8, 9, 12]
    elif lat >= 12:
        ms = [10, 11, 12, 1, 2, 3] if lat < 40 else [6, 7, 8, 9]
    else:
        ms = [5, 6, 7, 8, 9] if lat > -40 else [12, 1, 2, 3]
    return [f"{y}-{m}" for y in reversed(years) for m in ms]


def main(argv):
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["chip", "dem", "false"])
    ap.add_argument("lat", type=float)
    ap.add_argument("lon", type=float)
    ap.add_argument("half_km", type=float)
    ap.add_argument("out")
    ap.add_argument("--months", default="")
    ap.add_argument("--label", default="")
    ap.add_argument("--res", type=float, default=30.0)
    a = ap.parse_args(argv)
    months = a.months.split(",") if a.months else default_months(a.lat)
    foot = f"{a.lat:.4f}, {a.lon:.4f}"
    if a.kind == "chip":
        img, meta = s2_chip(a.lat, a.lon, a.half_km, months)
        if img is None:
            print(json.dumps({"ok": False, "why": "no scene"}))
            return
        annotate(img, a.half_km, a.label, footer=f"S2 {meta['scene']} | {foot}").save(a.out + "_s2.jpg", quality=88)
        print(json.dumps({"ok": True, "file": a.out + "_s2.jpg", **meta, "earth": earth_link(a.lat, a.lon)}))
    elif a.kind == "false":
        found = find_clear_scene(a.lat, a.lon, a.half_km, months)
        if not found:
            print(json.dumps({"ok": False}))
            return
        img = s2_band_chip(a.lat, a.lon, a.half_km, found[0])
        sid = found[0].rstrip('/').split('/')[-1]
        annotate(img, a.half_km, a.label, footer=f"S2 B12/B8/B4 {sid} | {foot}").save(a.out + "_s2fc.jpg", quality=88)
        print(json.dumps({"ok": True, "file": a.out + "_s2fc.jpg", "scene": sid}))
    else:
        z, res = dem_window(a.lat, a.lon, a.half_km, a.res)
        if z is None:
            print(json.dumps({"ok": False, "why": "no dem"}))
            return
        c = z.shape[0] // 2
        stats = {"min": float(np.nanmin(z)), "max": float(np.nanmax(z)), "centre": float(z[c, c])}
        annotate(dem_render(z, res), a.half_km, a.label, footer=f"COP-DEM30 hillshade | {foot}").save(a.out + "_dem.jpg", quality=88)
        np.save(a.out + "_dem.npy", z)
        print(json.dumps({"ok": True, "file": a.out + "_dem.jpg", **{k: round(v, 1) for k, v in stats.items()}}))


if __name__ == "__main__":
    main(sys.argv[1:])
