#!/usr/bin/env python3
"""T5 sky-island probe: for a bbox, report WorldCover tree fraction, Copernicus
DEM relief, and Meta/WRI 1 m canopy-height (CHM) statistics.

Usage: python3 -I probe.py NAME S N W E [ring_deg]
Prints one JSON line.
Data sources (anonymous S3):
  s3://esa-worldcover/v200/2021/map/...           (10 m land cover, class 10 = tree cover)
  s3://copernicus-dem-30m/...                     (GLO-30 DEM)
  https://dataforgood-fb-data.s3.amazonaws.com/forests/v1/alsgedi_global_v6_float/chm/<quadkey>.tif
"""
import json, math, os, sys
os.environ.setdefault("AWS_NO_SIGN_REQUEST", "YES")
os.environ.setdefault("GDAL_DISABLE_READDIR_ON_OPEN", "EMPTY_DIR")
os.environ.setdefault("CPL_VSIL_CURL_ALLOWED_EXTENSIONS", ".tif")
os.environ.setdefault("CPL_VSIL_CURL_CHUNK_SIZE", "4194304")
os.environ.setdefault("GDAL_HTTP_MULTIRANGE", "YES")
os.environ.setdefault("GDAL_HTTP_MERGE_CONSECUTIVE_RANGES", "YES")
import numpy as np
import rasterio
from rasterio.windows import from_bounds
from rasterio.warp import transform_bounds

HERE = os.path.dirname(os.path.abspath(__file__))


def wc_tiles(s, n, w, e):
    out = []
    for la in range(int(math.floor(s / 3) * 3), int(math.ceil(n / 3) * 3), 3):
        for lo in range(int(math.floor(w / 3) * 3), int(math.ceil(e / 3) * 3), 3):
            ns = ("N%02d" % la) if la >= 0 else ("S%02d" % -la)
            ew = ("E%03d" % lo) if lo >= 0 else ("W%03d" % -lo)
            out.append(f"s3://esa-worldcover/v200/2021/map/ESA_WorldCover_10m_2021_v200_{ns}{ew}_Map.tif")
    return out


def read_merged(paths, s, n, w, e):
    vals = []
    for p in paths:
        try:
            with rasterio.open(p) as ds:
                b = ds.bounds
                ss, nn, ww, ee = max(s, b.bottom), min(n, b.top), max(w, b.left), min(e, b.right)
                if ss >= nn or ww >= ee:
                    continue
                win = from_bounds(ww, ss, ee, nn, ds.transform)
                a = ds.read(1, window=win, boundless=False)
                vals.append(a.ravel())
        except Exception as ex:  # missing tile = ocean
            pass
    return np.concatenate(vals) if vals else np.array([])


def worldcover(s, n, w, e):
    a = read_merged(wc_tiles(s, n, w, e), s, n, w, e)
    a = a[a > 0]
    if a.size == 0:
        return None
    u, c = np.unique(a, return_counts=True)
    frac = {int(k): round(float(v) / a.size, 3) for k, v in zip(u, c)}
    return frac


def dem_tiles(s, n, w, e):
    out = []
    for la in range(int(math.floor(s)), int(math.ceil(n))):
        for lo in range(int(math.floor(w)), int(math.ceil(e))):
            ns = ("N%02d" % la) if la >= 0 else ("S%02d" % -la)
            ew = ("E%03d" % lo) if lo >= 0 else ("W%03d" % -lo)
            name = f"Copernicus_DSM_COG_10_{ns}_00_{ew}_00_DEM"
            out.append(f"s3://copernicus-dem-30m/{name}/{name}.tif")
    return out


def dem(s, n, w, e):
    a = read_merged(dem_tiles(s, n, w, e), s, n, w, e).astype(float)
    a = a[np.isfinite(a) & (a > -100)]
    if a.size == 0:
        return None
    return {"min": int(a.min()), "p10": int(np.percentile(a, 10)), "median": int(np.median(a)),
            "p90": int(np.percentile(a, 90)), "max": int(a.max())}


_TILES = None


def chm_tiles(s, n, w, e):
    global _TILES
    if _TILES is None:
        from shapely.geometry import shape
        with open(os.path.join(HERE, "dl", "tiles.geojson")) as f:
            fc = json.load(f)
        _TILES = [(ft["properties"]["tile"], shape(ft["geometry"]).bounds) for ft in fc["features"]]
    out = []
    for q, (x0, y0, x1, y1) in _TILES:
        if x0 < e and x1 > w and y0 < n and y1 > s:
            out.append(q)
    return out


def chm(s, n, w, e, target_res=4.0):
    base = "/vsicurl/https://dataforgood-fb-data.s3.amazonaws.com/forests/v1/alsgedi_global_v6_float/chm/"
    vals = []
    for q in chm_tiles(s, n, w, e):
        try:
            with rasterio.open(base + q + ".tif") as ds:
                l, b, r, t = transform_bounds("EPSG:4326", ds.crs, w, s, e, n)
                bl, bb, br, bt = ds.bounds
                l, b, r, t = max(l, bl), max(b, bb), min(r, br), min(t, bt)
                if l >= r or b >= t:
                    continue
                res = abs(ds.transform.a)
                win = from_bounds(l, b, r, t, ds.transform)
                f = max(1, int(round(target_res / res)))
                r0, c0 = int(win.row_off), int(win.col_off)
                nr, nc = int(win.height), int(win.width)
                rows = []
                from rasterio.windows import Window
                for rr in range(r0, r0 + nr, f):
                    rows.append(ds.read(1, window=Window(c0, rr, nc, 1))[0, ::f])
                a = np.stack(rows).astype(float)
                vals.append(a.ravel())
        except Exception as ex:
            print("chm err", q, ex, file=sys.stderr)
    if not vals:
        return None
    a = np.concatenate(vals)
    a = a[np.isfinite(a) & (a >= 0) & (a < 120)]
    if a.size == 0:
        return None
    return {"n": int(a.size), "gt5": round(float((a > 5).mean()), 3), "gt15": round(float((a > 15).mean()), 3),
            "gt20": round(float((a > 20).mean()), 3), "gt25": round(float((a > 25).mean()), 3),
            "p50": round(float(np.median(a)), 1), "p90": round(float(np.percentile(a, 90)), 1),
            "p98": round(float(np.percentile(a, 98)), 1)}


def km2(s, n, w, e):
    lat = math.radians((s + n) / 2)
    return round((n - s) * 111.32 * (e - w) * 111.32 * math.cos(lat), 1)


if __name__ == "__main__":
    name = sys.argv[1]
    s, n, w, e = map(float, sys.argv[2:6])
    ring = float(sys.argv[6]) if len(sys.argv) > 6 else 0.0
    res = {"name": name, "bbox": [s, n, w, e], "area_km2": km2(s, n, w, e)}
    res["wc"] = worldcover(s, n, w, e)
    res["dem"] = dem(s, n, w, e)
    res["chm"] = chm(s, n, w, e)
    if res["wc"] and res["chm"]:
        res["tree_km2_wc"] = round(res["area_km2"] * res["wc"].get(10, 0), 1)
        res["tall20_km2"] = round(res["area_km2"] * res["chm"]["gt20"], 1)
    if ring > 0:
        S, N, W, E = s - ring, n + ring, w - ring, e + ring
        # surrounding ring approximated by larger box (includes core)
        res["ring_wc_tree"] = (worldcover(S, N, W, E) or {}).get(10)
        res["ring_dem"] = dem(S, N, W, E)
        pass  # ring CHM skipped (strip-organised COGs, too heavy)
    print(json.dumps(res))
