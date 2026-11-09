"""Knickpoint test for waterfall candidates: is the drop a discrete step (fall) or a steady gorge?"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np, numba as nb
import waterfalls as wf, scan_craters as sc
from pyproj import Transformer
import rasterio
from concurrent.futures import ProcessPoolExecutor

@nb.njit(cache=True)
def upstream(rec, acc):
    n = rec.size; r = rec.ravel(); a = acc.ravel()
    up = np.full(n, -1, np.int64); best = np.zeros(n)
    for i in range(n):
        j = r[i]
        if j >= 0 and a[i] > best[j]:
            best[j] = a[i]; up[j] = i
    return up

def profile(i0, rec, up, z, W, n_up=40, n_dn=40):
    path = [i0]; j = i0
    for _ in range(n_up):
        j = up[j]
        if j < 0: break
        path.insert(0, j)
    k0 = len(path) - 1; j = i0
    for _ in range(n_dn):
        j = rec.ravel()[j]
        if j < 0: break
        path.append(j)
    ys = np.array([p // W for p in path]); xs = np.array([p % W for p in path])
    zs = z[ys, xs]
    d = np.zeros(len(path))
    for q in range(1, len(path)):
        d[q] = d[q-1] + (1.41421356 if (ys[q] != ys[q-1] and xs[q] != xs[q-1]) else 1.0) * wf.RES
    return d, zs, k0

def analyze_tile(args):
    (la, lo), cands = args
    sc.RES = wf.RES
    t = sc.load_tile(la, lo, pad=0.08)
    if t is None: return []
    z, tr, epsg = t
    z = np.where(z > -9000, z, np.nan).astype(np.float64)
    filled = wf.priority_flood(z); rec = wf.d8(filled); acc = wf.accumulate(filled, rec)
    up = upstream(rec, acc)
    H, W = z.shape
    to_xy = Transformer.from_crs("EPSG:4326", f"EPSG:{epsg}", always_xy=True)
    out = []
    for c in cands:
        X, Y = to_xy.transform(c["lon"], c["lat"])
        row, col = rasterio.transform.rowcol(tr, X, Y)
        # snap to highest-acc pixel within 2 px
        best = None
        for dy in range(-2, 3):
            for dx in range(-2, 3):
                yy, xx = row + dy, col + dx
                if 0 <= yy < H and 0 <= xx < W and (best is None or acc[yy, xx] > acc[best]):
                    best = (yy, xx)
        i0 = best[0] * W + best[1]
        d, zs, k0 = profile(i0, rec, up, z, W)
        if len(zs) < 30 or np.isnan(zs).any(): continue
        # smallest window (in m) holding a 70% share of the max local drop -> step
        g = np.diff(zs) / np.maximum(np.diff(d), 1)
        # steepest 3-step window near k0
        best_s = None
        for a in range(max(0, k0 - 8), min(len(zs) - 4, k0 + 8)):
            dr = zs[a] - zs[a + 3]; L = d[a + 3] - d[a]
            if best_s is None or dr > best_s[0]: best_s = (dr, L, a)
        dr, L, a = best_s
        above = zs[max(0, a - 12)] - zs[a]; La = d[a] - d[max(0, a - 12)]
        below = zs[a + 3] - zs[min(len(zs) - 1, a + 15)]; Lb = d[min(len(zs) - 1, a + 15)] - d[a + 3]
        ga, gb, gs = above / max(La, 1), below / max(Lb, 1), dr / max(L, 1)
        ratio = gs / max(ga, gb, 0.02)
        c2 = dict(c); c2.update(step_drop=round(float(dr), 1), step_len=round(float(L)), step_grad=round(float(gs), 2),
                                above_grad=round(float(ga), 3), below_grad=round(float(gb), 3), knick_ratio=round(float(ratio), 2),
                                lip_elev=round(float(zs[a])), prof=[round(float(v)) for v in zs[::2]])
        out.append(c2)
    return out

if __name__ == "__main__":
    cands = json.load(open(sys.argv[1]))
    groups = {}
    for c in cands: groups.setdefault((math.floor(c["lat"]), math.floor(c["lon"])), []).append(c)
    res = []
    with ProcessPoolExecutor(int(os.environ.get("NP", "3"))) as ex:
        for r in ex.map(analyze_tile, list(groups.items())):
            res += r
            print(len(res), flush=True)
    json.dump(res, open(sys.argv[2], "w"))
