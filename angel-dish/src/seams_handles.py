"""Locate tunnels (b1) of a field by recursive bisection (integrator tool).  python3 seams_handles.py field.npy [minbox_mm]"""
import sys, os, json
import numpy as np
from scipy import ndimage as ndi
from skimage.measure import euler_number
S26 = np.ones((3, 3, 3), bool)
p = sys.argv[1]
meta = json.load(open(os.path.join(os.path.dirname(p), 'raw.json')))
lo = np.array(meta['lo']); h = meta['h']
ins = np.load(p, mmap_mode='r')
ins = np.asarray(ins) < 0
def betti1(a):
    q = np.pad(a, 1)
    chi = euler_number(q, connectivity=3)
    b0 = ndi.label(q, S26)[1]; b2 = ndi.label(~q)[1] - 1
    return b0 + b2 - chi
MIN = int(round(float(sys.argv[2]) / h)) if len(sys.argv) > 2 else int(round(6 / h))
out = []
def rec(b, val):
    sz = [b[1] - b[0], b[3] - b[2], b[5] - b[4]]
    ax = int(np.argmax(sz))
    if sz[ax] <= MIN:
        out.append((b, val)); return
    m = (b[2 * ax] + b[2 * ax + 1]) // 2
    c1 = list(b); c1[2 * ax + 1] = m + 3
    c2 = list(b); c2[2 * ax] = m - 3
    v1 = betti1(ins[c1[0]:c1[1], c1[2]:c1[3], c1[4]:c1[5]]); v2 = betti1(ins[c2[0]:c2[1], c2[2]:c2[3], c2[4]:c2[5]])
    if v1 + v2 < val:
        out.append((b, val - v1 - v2))
    if v1 > 0: rec(c1, v1)
    if v2 > 0: rec(c2, v2)
full = (0, ins.shape[0], 0, ins.shape[1], 0, ins.shape[2])
t = betti1(ins); print('b1', t, flush=True)
rec(full, t)
for b, val in out:
    p0 = lo + np.array([b[0], b[2], b[4]]) * h; p1 = lo + np.array([b[1], b[3], b[5]]) * h
    print('b1=%d  box %s .. %s' % (val, np.round(p0, 1).tolist(), np.round(p1, 1).tolist()), flush=True)
