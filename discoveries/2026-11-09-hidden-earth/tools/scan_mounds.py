"""Tell / large-mound finder on Copernicus GLO-30 (h-dome transform on flat plains).

Settlement mounds (tells, togue, Sao mounds, depe) rise 3-40 m above flat alluvial
plains and are 1-150 ha. h-dome isolates local bumps of up to H metres; we then keep
compact bumps whose surroundings are flat.

python3 scan_mounds.py <lat0> <lat1> <lon0> <lon1> <out.json>
"""
import sys, os, math, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import scan_craters as sc
from skimage.morphology import reconstruction
from skimage.measure import label, regionprops
from pyproj import Transformer
import rasterio
from concurrent.futures import ThreadPoolExecutor

H = 30.0          # max dome height considered (m)
MIN_H = 2.5       # minimum mound prominence (m)
RES = 30.0


def scan_tile(la, lo):
    sc.RES = RES
    t = sc.load_tile(la, lo, pad=0.03)
    if t is None:
        return []
    z, tr, epsg = t
    valid = z > -9000
    if valid.mean() < 0.2:
        return []
    zz = np.where(valid, z, np.nanmin(np.where(valid, z, np.nan))).astype(np.float64)
    dome = zz - reconstruction(zz - H, zz, method="dilation")
    lab = label(dome > MIN_H, connectivity=2)
    to_ll = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    out = []
    Hh, Ww = zz.shape
    for rp in regionprops(lab, intensity_image=dome):
        A_ha = rp.area * RES * RES / 1e4
        if A_ha < 1.0 or A_ha > 200:
            continue
        hmax = float(rp.intensity_max)
        if hmax < 3.0:
            continue
        if rp.eccentricity > 0.93 or rp.solidity < 0.75:
            continue
        cy, cx = map(int, rp.centroid)
        R = math.sqrt(rp.area / math.pi)
        r0, r1 = int(1.6 * R) + 2, int(3.2 * R) + 8
        y0, y1, x0, x1 = max(0, cy - r1), min(Hh, cy + r1 + 1), max(0, cx - r1), min(Ww, cx + r1 + 1)
        sub = zz[y0:y1, x0:x1]
        yy, xx = np.mgrid[y0:y1, x0:x1]
        d = np.hypot(yy - cy, xx - cx)
        ring = sub[(d >= r0) & (d < r1)]
        if ring.size < 20:
            continue
        ring_sd = float(np.std(ring))
        ring_rng = float(np.percentile(ring, 95) - np.percentile(ring, 5))
        base = float(np.median(ring))
        top = float(zz[rp.coords[:, 0], rp.coords[:, 1]].max())
        rel = top - base
        if ring_rng > max(4.0, 0.6 * rel):      # surroundings not flat -> natural hill/dune country
            continue
        # count other bumps nearby (dune fields / hummocky ground produce many)
        x, y = rasterio.transform.xy(tr, cy, cx)
        lon, lat = to_ll.transform(x, y)
        if not (la <= lat < la + 1 and lo <= lon < lo + 1):
            continue
        score = min(rel, 25) * (rp.solidity) * (1.0 - min(rp.eccentricity, 0.95) * 0.5) / (1.0 + ring_rng / 3.0)
        out.append(dict(lat=round(lat, 5), lon=round(lon, 5), area_ha=round(A_ha, 1), rel_m=round(rel, 1),
                        dome_m=round(hmax, 1), ring_range_m=round(ring_rng, 1), ecc=round(float(rp.eccentricity), 2),
                        solidity=round(float(rp.solidity), 2), score=round(score, 2)))
    # isolation: drop bumps with many neighbours within 3 km (hummocky/dune ground)
    if out:
        P = np.array([[r["lat"], r["lon"]] for r in out])
        for r in out:
            dd = np.hypot(P[:, 0] - r["lat"], (P[:, 1] - r["lon"]) * math.cos(math.radians(r["lat"]))) * 111
            r["nbr3km"] = int((dd < 3).sum() - 1)
    return out


def main():
    a0, a1, o0, o1, outp = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    tiles = [(la, lo) for la in range(math.floor(a0), math.ceil(a1)) for lo in range(math.floor(o0), math.ceil(o1))]
    rows = []
    with ThreadPoolExecutor(int(os.environ.get("NTH", "3"))) as ex:
        for t, r in zip(tiles, ex.map(lambda t: scan_tile(*t), tiles)):
            rows += r
            print(t, len(r), flush=True)
    rows.sort(key=lambda r: -r["score"])
    json.dump(rows, open(outp, "w"))
    print(json.dumps(rows[:10]))


if __name__ == "__main__":
    main()
