"""Compare water between two S2 L2A scenes in a window: SCL==6 OR (NDWI>0.3 and B08<1500 and B03<2500, not snow).
Reports connected components of NEW water (present in post, absent in pre) with area and centroid lat/lon.
Usage: python3 -I newwater.py <lat> <lon> <half_m> <pre_sid> <post_sid> [min_px]
"""
import sys
import numpy as np
from scipy import ndimage
from pyproj import Transformer
sys.path.insert(0, __file__.rsplit("/", 1)[0])
from s2chip import scene_base, read_win  # noqa


def water_mask(sid, lat, lon, half_m):
    b = scene_base(sid)
    g, wt, crs = read_win(f"/vsicurl/{b}/B03.tif", lat, lon, half_m)
    n, _, _ = read_win(f"/vsicurl/{b}/B08.tif", lat, lon, half_m)
    scl, _, _ = read_win(f"/vsicurl/{b}/SCL.tif", lat, lon, half_m)
    g = g[0].astype(float); n = n[0].astype(float)
    scl = np.kron(scl[0], np.ones((2, 2), dtype=scl.dtype))[: g.shape[0], : g.shape[1]]
    ndwi = (g - n) / np.maximum(g + n, 1)
    w = ((ndwi > 0.3) & (n < 1500) & (g < 2500)) | (scl == 6)
    w &= scl != 11  # not snow
    valid = (g > 0) & (scl != 8) & (scl != 9) & (scl != 3)  # not cloud/shadow
    return w, valid, wt, crs


def main():
    lat, lon, half = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
    pre, post = sys.argv[4], sys.argv[5]
    min_px = int(sys.argv[6]) if len(sys.argv) > 6 else 50
    wa, va, wt, crs = water_mask(pre, lat, lon, half)
    wb, vb, _, _ = water_mask(post, lat, lon, half)
    new = wb & ~ndimage.binary_dilation(wa, iterations=2) & va & vb
    new = ndimage.binary_opening(new, iterations=1)
    lab, k = ndimage.label(new)
    inv = Transformer.from_crs(crs, "EPSG:4326", always_xy=True)
    print(f"pre water px={int(wa.sum())}  post water px={int(wb.sum())}  new components={k}")
    rows = []
    for i, sl in enumerate(ndimage.find_objects(lab), 1):
        m = lab[sl] == i
        npx = int(m.sum())
        if npx < min_px:
            continue
        cy, cx = ndimage.center_of_mass(m)
        cy += sl[0].start; cx += sl[1].start
        x = wt.c + (cx + 0.5) * wt.a; y = wt.f + (cy + 0.5) * wt.e
        lo, la = inv.transform(x, y)
        L = max(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) * 10
        rows.append((npx, la, lo, L))
    for npx, la, lo, L in sorted(rows, reverse=True)[:15]:
        print(f"  new water: {npx*100/1e6:.3f} km2 ({npx} px), centroid {la:.5f}, {lo:.5f}, bbox max dim ~{L} m")


if __name__ == "__main__":
    main()
