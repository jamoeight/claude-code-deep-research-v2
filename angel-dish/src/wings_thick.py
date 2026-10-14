"""Thin-region check for the wings grid (wings agent tool).  python3 wings_thick.py [h]"""
import sys
import numpy as np
from scipy import ndimage
import model, wings
from sdf import Field
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
F = Field(model.LO, model.HI, h)
W = wings.component(F.blank())
ins = W.G < 0
edt = ndimage.distance_transform_edt(ins) * h
mx = ndimage.maximum_filter(edt, size=3)
ridge = ins & (edt >= mx - 1e-6) & (edt > 0)
thin = ridge & (edt < 0.65)
idx = np.argwhere(thin)
P = W.lo + idx * h
print('ridge voxels', ridge.sum(), 'thin (<1.3 thick)', len(idx))
if len(idx):
    lab, n = ndimage.label(ndimage.binary_dilation(thin, iterations=2))
    cnt = np.bincount(lab[thin])
    for k in np.argsort(-cnt)[:12]:
        if k == 0 or cnt[k] == 0:
            continue
        m = lab[tuple(idx.T)] == k
        print(cnt[k], np.round(P[m].mean(0), 1), 'min thick %.2f' % (2 * edt[tuple(idx[m].T)].min()))
# thickness distribution of the sheet ridge
r = edt[ridge] * 2
print('thickness percentiles 1/5/25/50:', np.round(np.percentile(r, [1, 5, 25, 50]), 2))
