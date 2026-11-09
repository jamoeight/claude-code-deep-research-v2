"""DEM-based tall-waterfall candidate finder (Copernicus GLO-30).

For each 1x1 degree tile: warp to UTM 30 m, priority-flood (+epsilon) fill, D8 flow
routing and accumulation, then walk every channel pixel (catchment >= MIN_KM2) and
measure the elevation drop over a short downstream path. Abrupt drops on real
rivers are waterfall or cataract candidates.

python3 waterfalls.py <lat0> <lat1> <lon0> <lon1> <out.csv>
"""
import sys, os, math, csv, json
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
import numba as nb
import heapq
import scan_craters as sc

RES = 30.0
MIN_KM2 = float(os.environ.get("WF_MIN_KM2", "5"))
STEPS = 8            # path length ~ 8 pixels (~240-340 m)
MIN_DROP = float(os.environ.get("WF_MIN_DROP", "80"))


@nb.njit(cache=True)
def priority_flood(z):
    H, W = z.shape
    filled = z.copy()
    closed = np.zeros((H, W), np.bool_)
    heap = [(0.0, 0, 0)]
    heap.pop()
    for y in range(H):
        for x in range(W):
            if y == 0 or x == 0 or y == H - 1 or x == W - 1 or np.isnan(z[y, x]):
                if not np.isnan(z[y, x]):
                    heapq.heappush(heap, (z[y, x], y, x))
                closed[y, x] = True
    dy = (-1, -1, -1, 0, 0, 1, 1, 1)
    dx = (-1, 0, 1, -1, 1, -1, 0, 1)
    while len(heap) > 0:
        e, y, x = heapq.heappop(heap)
        for k in range(8):
            yy, xx = y + dy[k], x + dx[k]
            if yy < 0 or xx < 0 or yy >= H or xx >= W or closed[yy, xx]:
                continue
            closed[yy, xx] = True
            v = filled[yy, xx]
            ne = e + 1e-3
            if v <= ne:
                filled[yy, xx] = ne
            heapq.heappush(heap, (filled[yy, xx], yy, xx))
    return filled


@nb.njit(cache=True)
def d8(filled):
    H, W = filled.shape
    rec = np.full((H, W), -1, np.int64)
    dy = (-1, -1, -1, 0, 0, 1, 1, 1)
    dx = (-1, 0, 1, -1, 1, -1, 0, 1)
    for y in range(1, H - 1):
        for x in range(1, W - 1):
            e = filled[y, x]
            if np.isnan(e):
                continue
            best, bk = 0.0, -1
            for k in range(8):
                yy, xx = y + dy[k], x + dx[k]
                v = filled[yy, xx]
                if np.isnan(v):
                    continue
                dist = 1.41421356 if (dy[k] != 0 and dx[k] != 0) else 1.0
                s = (e - v) / dist
                if s > best:
                    best, bk = s, k
            if bk >= 0:
                rec[y, x] = (y + dy[bk]) * W + (x + dx[bk])
    return rec


@nb.njit(cache=True)
def accumulate(filled, rec):
    H, W = filled.shape
    flat = filled.ravel()
    order = np.argsort(-np.where(np.isnan(flat), -1e9, flat))
    acc = np.ones(H * W, np.float64)
    r = rec.ravel()
    for i in order:
        j = r[i]
        if j >= 0:
            acc[j] += acc[i]
    return acc.reshape(H, W)


@nb.njit(cache=True)
def drops(z, rec, acc, min_px, steps):
    H, W = z.shape
    out_drop = np.zeros((H, W), np.float32)
    out_len = np.zeros((H, W), np.float32)
    r = rec.ravel()
    zf = z.ravel()
    for i in range(H * W):
        if acc.ravel()[i] < min_px or np.isnan(zf[i]):
            continue
        j = i
        L = 0.0
        for s in range(steps):
            k = r[j]
            if k < 0:
                break
            y0, x0 = j // W, j % W
            y1, x1 = k // W, k % W
            L += 1.41421356 if (y0 != y1 and x0 != x1) else 1.0
            j = k
        if j == i or np.isnan(zf[j]):
            continue
        out_drop.ravel()[i] = zf[i] - zf[j]
        out_len.ravel()[i] = L
    return out_drop, out_len


def scan_tile(la, lo):
    old = sc.RES
    sc.RES = RES
    t = sc.load_tile(la, lo, pad=0.08)
    sc.RES = old
    if t is None:
        return []
    z, tr, epsg = t
    z = np.where(z > -9000, z, np.nan).astype(np.float64)
    if np.isfinite(z).mean() < 0.2:
        return []
    filled = priority_flood(z)
    rec = d8(filled)
    acc = accumulate(filled, rec)
    min_px = MIN_KM2 * 1e6 / (RES * RES)
    dr, ln = drops(z, rec, acc, min_px, STEPS)
    grad = dr / np.maximum(ln * RES, 1)
    cand = (dr >= MIN_DROP) & (grad >= 0.35)
    from skimage.measure import label, regionprops
    from pyproj import Transformer
    import rasterio
    lab = label(cand, connectivity=2)
    to_ll = Transformer.from_crs(f"EPSG:{epsg}", "EPSG:4326", always_xy=True)
    out = []
    for rp in regionprops(lab):
        cc = rp.coords
        vals = dr[cc[:, 0], cc[:, 1]]
        k = int(np.argmax(vals))
        y, x = cc[k]
        # total drop along the steep reach: highest minus lowest z over cluster + one path
        zs = z[cc[:, 0], cc[:, 1]]
        X, Y = rasterio.transform.xy(tr, int(y), int(x))
        lon, lat = to_ll.transform(X, Y)
        if not (la <= lat < la + 1 and lo <= lon < lo + 1):
            continue
        out.append(dict(lat=round(lat, 5), lon=round(lon, 5), drop_m=round(float(vals[k]), 1),
                        path_m=round(float(ln[y, x] * RES)), grad=round(float(grad[y, x]), 2),
                        reach_relief_m=round(float(np.nanmax(zs) - np.nanmin(zs) + vals[k]), 1),
                        catch_km2=round(float(acc[y, x] * RES * RES / 1e6), 1), npx=int(len(cc)),
                        elev_top=round(float(np.nanmax(zs)), 0)))
    return out


def main():
    a0, a1, o0, o1, outp = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
    tiles = [(la, lo) for la in range(math.floor(a0), math.ceil(a1)) for lo in range(math.floor(o0), math.ceil(o1))]
    rows = []
    for t in tiles:
        r = scan_tile(*t)
        print(t, len(r), flush=True)
        rows += r
    rows.sort(key=lambda r: -(r["drop_m"] * math.log10(1 + r["catch_km2"])))
    if rows:
        with open(outp, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader(); w.writerows(rows)
    print(json.dumps(rows[:12]))


if __name__ == "__main__":
    main()
