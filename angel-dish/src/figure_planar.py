"""Find planar patches (clusters of coplanar faces) in the figure-only mesh."""
import sys
import numpy as np
import model, figure
from sdf import Field
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.4
F = figure.component(Field(model.LO, model.HI, h).blank())
v, f = F.mesh()
t = v[f]; n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0]); a = np.linalg.norm(n, axis=1) / 2
n /= (2 * a[:, None] + 1e-12)
c = t.mean(1)
off = np.einsum('ij,ij->i', n, c)
key = np.round(np.concatenate([n * 40, off[:, None] / 0.15], 1)).astype(int)
_, inv, cnt = np.unique(key, axis=0, return_inverse=True, return_counts=True)
area = np.bincount(inv.ravel(), weights=a)
order = np.argsort(-area)[:8]
for o in order:
    m = inv.ravel() == o
    print('area %.1f  faces %d  normal %s  bbox %s..%s' % (area[o], m.sum(), n[m][0].round(2), c[m].min(0).round(1), c[m].max(0).round(1)))
