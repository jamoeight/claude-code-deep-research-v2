"""Contact sheets: S2 true colour + DEM hillshade per candidate, in a grid.

python3 sheet.py <cands.json> <out.jpg> [--cols 4] [--px 300]
cands.json: list of {"id","lat","lon","half_km", optional "label"}
Also saves per-candidate full-size chips in imagery/chips/<id>_s2.jpg / _dem.jpg
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.dirname(__file__))
import geo
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.join(os.path.dirname(__file__), "..")
CHIPS = os.path.join(ROOT, "imagery", "chips")
os.makedirs(CHIPS, exist_ok=True)
try:
    F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)
except Exception:
    F = ImageFont.load_default()


def chips_for(c, want_dem=True):
    lat, lon, hk = c["lat"], c["lon"], c.get("half_km", 2.0)
    lab = c.get("label", c["id"])
    out = {"id": c["id"]}
    s2p = os.path.join(CHIPS, f"{c['id']}_s2.jpg")
    dmp = os.path.join(CHIPS, f"{c['id']}_dem.jpg")
    try:
        if not os.path.exists(s2p):
            img, meta = geo.s2_chip(lat, lon, hk, c.get("months") or geo.default_months(lat))
            if img is not None:
                geo.annotate(img, hk, lab, footer=f"S2 {meta['scene']} | {lat:.4f}, {lon:.4f}").save(s2p, quality=88)
                out["s2_meta"] = meta
        out["s2"] = s2p if os.path.exists(s2p) else None
    except Exception as e:
        out["s2"] = None; out["s2_err"] = repr(e)[:200]
    if want_dem:
        try:
            if not os.path.exists(dmp):
                z, res = geo.dem_window(lat, lon, hk, 30.0 if hk > 1.5 else 15.0)
                if z is not None:
                    geo.annotate(geo.dem_render(z, res), hk, lab, footer=f"DEM {lat:.4f}, {lon:.4f}").save(dmp, quality=88)
            out["dem"] = dmp if os.path.exists(dmp) else None
        except Exception as e:
            out["dem"] = None; out["dem_err"] = repr(e)[:200]
    return out


def tile(path, px, text):
    if path and os.path.exists(path):
        im = Image.open(path).convert("RGB").resize((px, px), Image.LANCZOS)
    else:
        im = Image.new("RGB", (px, px), (40, 40, 40))
    d = ImageDraw.Draw(im)
    tw = d.textlength(text, font=F)
    d.rectangle([0, px - 20, tw + 8, px], fill=(0, 0, 0))
    d.text((4, px - 18), text, fill=(255, 255, 0), font=F)
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cands"); ap.add_argument("out")
    ap.add_argument("--cols", type=int, default=4); ap.add_argument("--px", type=int, default=300)
    ap.add_argument("--nodem", action="store_true")
    a = ap.parse_args()
    cands = json.load(open(a.cands))
    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(lambda c: chips_for(c, not a.nodem), cands))
    per = 1 if a.nodem else 2
    cols = a.cols
    rows = (len(cands) + cols - 1) // cols
    W = cols * per * a.px + (cols - 1) * 6
    sheet = Image.new("RGB", (W, rows * a.px + (rows - 1) * 6), (255, 255, 255))
    for i, (c, r) in enumerate(zip(cands, res)):
        x = (i % cols) * (per * a.px + 6); y = (i // cols) * (a.px + 6)
        sheet.paste(tile(r.get("s2"), a.px, c["id"]), (x, y))
        if per == 2:
            sheet.paste(tile(r.get("dem"), a.px, c["id"] + " DEM"), (x + a.px, y))
    sheet.save(a.out, quality=85)
    json.dump(res, open(a.out + ".json", "w"), indent=1)
    print(a.out, sum(1 for r in res if r.get("s2")), "s2 ok /", len(res))


if __name__ == "__main__":
    main()
