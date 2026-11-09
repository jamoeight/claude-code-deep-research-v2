"""Small Sentinel-2 L2A COG chip reader (sentinel-cogs public bucket, no STAC API).

Usage:
  python3 -I s2chip.py list  <lat> <lon> <year> <month>          # list scenes + cloud cover
  python3 -I s2chip.py chip  <lat> <lon> <scene_id> <half_m> <out_prefix>
     -> writes <out_prefix>_rgb.png (TCI) and prints NDWI stats for the window
"""
import sys, json, re, urllib.request
import numpy as np
import mgrs
import rasterio
from rasterio.windows import from_bounds
from pyproj import Transformer

BUCKET = "https://sentinel-cogs.s3.us-west-2.amazonaws.com"


def tile_of(lat, lon):
    t = mgrs.MGRS().toMGRS(lat, lon, MGRSPrecision=0)
    return t[:2].lstrip("0"), t[2], t[3:5]


def list_scenes(lat, lon, year, month):
    z, b, sq = tile_of(lat, lon)
    prefix = f"sentinel-s2-l2a-cogs/{z}/{b}/{sq}/{year}/{int(month)}/"
    url = f"{BUCKET}/?list-type=2&prefix={prefix}&delimiter=/"
    xml = urllib.request.urlopen(url, timeout=30).read().decode()
    ids = re.findall(r"<Prefix>" + re.escape(prefix) + r"([^/]+)/</Prefix>", xml)
    out = []
    for sid in ids:
        try:
            j = json.loads(urllib.request.urlopen(f"{BUCKET}/{prefix}{sid}/{sid}.json", timeout=30).read())
            cc = j["properties"].get("eo:cloud_cover")
            dt = j["properties"].get("datetime")
        except Exception as e:  # noqa
            cc, dt = None, None
        out.append((sid, cc, dt, f"{BUCKET}/{prefix}{sid}"))
    return out


def scene_base(sid):
    m = re.match(r"S2[ABC]_(\d{2})([A-Z])([A-Z]{2})_(\d{4})(\d{2})\d{2}_", sid)
    z, b, sq, y, mo = m.groups()
    return f"{BUCKET}/sentinel-s2-l2a-cogs/{int(z)}/{b}/{sq}/{y}/{int(mo)}/{sid}"


def read_win(url, lat, lon, half_m):
    with rasterio.open(url) as ds:
        tr = Transformer.from_crs("EPSG:4326", ds.crs, always_xy=True)
        x, y = tr.transform(lon, lat)
        w = from_bounds(x - half_m, y - half_m, x + half_m, y + half_m, ds.transform)
        arr = ds.read(window=w, boundless=True, fill_value=0)
        return arr, ds.window_transform(w), ds.crs


def chip(lat, lon, sid, half_m, outp):
    base = scene_base(sid)
    tci, wt, crs = read_win(f"/vsicurl/{base}/TCI.tif", lat, lon, half_m)
    g, _, _ = read_win(f"/vsicurl/{base}/B03.tif", lat, lon, half_m)
    n, _, _ = read_win(f"/vsicurl/{base}/B08.tif", lat, lon, half_m)
    g = g[0].astype(float); n = n[0].astype(float)
    ndwi = (g - n) / np.maximum(g + n, 1)
    water = ndwi > 0.2
    print(f"{sid}: window {g.shape}, water px (NDWI>0.2) = {int(water.sum())} "
          f"= {water.sum()*100/1e6:.3f} km2, NDWI mean {ndwi.mean():.3f}")
    from PIL import Image
    img = np.moveaxis(tci[:3], 0, -1)
    Image.fromarray(img.astype(np.uint8)).resize((img.shape[1]*2, img.shape[0]*2), Image.NEAREST).save(outp + "_rgb.png")
    np.save(outp + "_water.npy", water)
    with open(outp + "_meta.json", "w") as f:
        json.dump({"sid": sid, "transform": list(wt)[:6], "crs": str(crs), "center": [lat, lon], "half_m": half_m}, f)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "list":
        lat, lon, y, mo = float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
        for s in list_scenes(lat, lon, y, mo):
            print(s[0], s[1], s[2])
    elif cmd == "chip":
        chip(float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], float(sys.argv[5]), sys.argv[6])
