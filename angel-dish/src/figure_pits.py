"""Find sharp concave spots (pits, slots, engraved creases) on the figure surface: SDF Laplacian at mesh vertices.
python3 figure_pits.py [h] [thr]   -> clusters of vertices with laplacian < -thr (thr in 1/units)"""
import sys, os
import numpy as np
from scipy import ndimage
from scipy.spatial import cKDTree
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model, figure, figure_tex as T
from sdf import Field
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 3.0
F = figure.component(Field(model.LO, model.HI, h).blank())
G = F.G
L = ndimage.laplace(G.astype(np.float64)) / (h * h)
v, f = F.mesh()
idx = (v - np.array(F.lo)) / h
lap = ndimage.map_coordinates(L, idx.T, order=1)
bad = lap < -thr
P = v[bad]; Lb = lap[bad]
print('vertices', len(v), 'concave', bad.sum())
if len(P):
    tree = cKDTree(P)
    pairs = tree.query_pairs(0.9)
    import collections
    parent = list(range(len(P)))
    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb: parent[ra] = rb
    groups = collections.defaultdict(list)
    for i in range(len(P)): groups[find(i)].append(i)
    c = T.ref_camera()
    out = []
    for g in groups.values():
        g = np.array(g); q = P[g]
        ext = np.ptp(q, axis=0).max()
        out.append((Lb[g].min(), len(g), ext, q.mean(0)))
    out.sort(key=lambda t: t[0])
    for m, n, ext, cen in out[:40]:
        print('lap %7.1f  n %5d  extent %5.1f  at (%6.1f %6.1f %6.1f)  px %s' % (m, n, ext, *cen, T.project(c, cen)[0].round(0)))
