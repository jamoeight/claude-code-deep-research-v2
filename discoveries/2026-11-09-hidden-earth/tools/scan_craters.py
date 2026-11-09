"""DEM circular-depression scanner (simple bowl craters, ~0.3-6 km) on Copernicus GLO-30.

python3 scan_craters.py <lat_min> <lat_max> <lon_min> <lon_max> <out.csv>
Processes 1x1 degree tiles, each warped to a local UTM 30 m grid.
"""
import sys, os, math, csv, json
sys.path.insert(0, os.path.dirname(__file__))
import geo  # sets GDAL env
import numpy as np
import rasterio
from rasterio.warp import reproject, calculate_default_transform
from rasterio.enums import Resampling
from skimage.morphology import reconstruction
from skimage.measure import label, regionprops
from pyproj import Transformer
from concurrent.futures import ThreadPoolExecutor

RES = float(os.environ.get("SCAN_RES", "60"))


def load_tile(la, lo, pad=0.03):
    """Read tile plus small padding from neighbours, warp to UTM grid."""
    from rasterio.merge import merge
    srcs = []
    for a in (la - 1, la, la + 1):
        for b in (lo - 1, lo, lo + 1):
            n = geo._dem_name(a, b)
            try:
                srcs.append(rasterio.open(f"{geo.DEM_BASE}/{n}/{n}.tif"))
            except Exception:
                pass
    if not srcs:
        return None
    bounds = (lo - pad, la - pad, lo + 1 + pad, la + 1 + pad)
    try:
        src_res = (RES / 30.0) / 3600.0  # read via COG overviews when coarser than native
        mos, tr = merge(srcs, bounds=bounds, nodata=-9999, res=(src_res, src_res) if RES > 30 else None)
    except Exception:
        return None
    crs = srcs[0].crs
    for s in srcs:
        s.close()
    zone = int((lo + 0.5 + 180) // 6) + 1
    epsg = (32600 if la >= 0 else 32700) + zone
    dt, w, h = calculate_default_transform(crs, f"EPSG:{epsg}", mos.shape[2], mos.shape[1], *bounds, resolution=RES)
    dst = np.full((h, w), -9999, np.float32)
    reproject(mos[0].astype(np.float32), dst, src_transform=tr, src_crs=crs, src_nodata=-9999,
              dst_transform=dt, dst_crs=f"EPSG:{epsg}", dst_nodata=-9999, resampling=Resampling.bilinear)
    return dst, dt, epsg


def ring_stats(z, cy, cx, r_in, r_out, nsec=12):
    H, W = z.shape
    R = int(math.ceil(r_out)) + 1
    y0, y1, x0, x1 = max(0, cy - R), min(H, cy + R + 1), max(0, cx - R), min(W, cx + R + 1)
    sub = z[y0:y1, x0:x1]
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.hypot(yy - cy, xx - cx)
    ang = (np.arctan2(yy - cy, xx - cx) + np.pi) / (2 * np.pi) * nsec
    m = (d >= r_in) & (d < r_out) & np.isfinite(sub)
    sec = []
    for k in range(nsec):
        mk = m & (ang.astype(int) % nsec == k)
        sec.append(np.nanmedian(sub[mk]) if mk.sum() > 2 else np.nan)
    return np.array(sec)


def scan_tile(la, lo):
    t = load_tile(la, lo)
    if t is None:
        return []
    z, tr, epsg = t
    valid = z > -9000
    if valid.mean() < 0.2:
        return []
    zf = np.where(valid, z, np.nan)
    # sea/nodata -> very low so depressions don't leak
    zz = np.where(valid, z, np.nanmin(zf) - 100).astype(np.float64)
    seed = zz.copy()
    seed[1:-1, 1:-1] = zz.max()
    filled = reconstruction(seed, zz, method="erosion")
    depth = filled - zz
    lab = label(depth > 2.0, connectivity=2)
    out = []
    to_ll = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    for rp in regionprops(lab, intensity_image=depth):
        A = rp.area * RES * RES
        D = 2 * math.sqrt(A / math.pi)
        if D < max(250, 6 * RES) or D > 8000:
            continue
        per = rp.perimeter * RES
        circ = 4 * math.pi * A / max(per, 1) ** 2
        if circ < 0.55 or rp.eccentricity > 0.8:
            continue
        dmax = rp.intensity_max
        if dmax / D < 0.015:
            continue
        cy, cx = map(int, rp.centroid)
        Rpx = D / 2 / RES
        rim = ring_stats(zf, cy, cx, 0.95 * Rpx, 1.35 * Rpx)
        outer = ring_stats(zf, cy, cx, 2.0 * Rpx, 2.6 * Rpx)
        if np.isnan(rim).sum() > 3 or np.isnan(outer).sum() > 3:
            continue
        raised = rim - outer
        frac_raised = float(np.nanmean(raised > 1.0))
        rim_relief = float(np.nanmedian(raised))
        floor = float(np.nanmin(zf[lab == rp.label])) if False else float(zf[cy, cx])
        rim_sd = float(np.nanstd(rim))
        score = circ * (0.3 + frac_raised) * min(1.0, (dmax / D) / 0.06)
        x, y = rasterio.transform.xy(tr, cy, cx)
        lon, lat = to_ll.transform(x, y)
        if not (la <= lat < la + 1 and lo <= lon < lo + 1):
            continue
        out.append(dict(lat=round(lat, 5), lon=round(lon, 5), diam_m=round(D), depth_m=round(float(dmax), 1),
                        d_over_D=round(float(dmax / D), 3), circ=round(circ, 2), ecc=round(float(rp.eccentricity), 2),
                        frac_rim_raised=round(frac_raised, 2), rim_relief_m=round(rim_relief, 1),
                        rim_sd_m=round(rim_sd, 1), score=round(score, 3)))
    return out


def main():
    a0, a1, o0, o1, outp = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    tiles = [(la, lo) for la in range(math.floor(a0), math.ceil(a1)) for lo in range(math.floor(o0), math.ceil(o1))]
    rows = []
    with ThreadPoolExecutor(3) as ex:
        for i, res in enumerate(ex.map(lambda t: scan_tile(*t), tiles)):
            rows.extend(res)
            print(f"tile {tiles[i]}: {len(res)} cands", flush=True)
    rows.sort(key=lambda r: -r["score"])
    if rows:
        with open(outp, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    print(json.dumps(rows[:15], indent=0))


if __name__ == "__main__":
    main()
