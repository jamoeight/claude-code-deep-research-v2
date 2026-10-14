"""Probe top-surface heights of a cached part field: python3 figure_probe.py part h x,y [x,y ...]"""
import sys, glob, json, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model
from sdf import Field
part = sys.argv[1]; h = float(sys.argv[2])
F = Field(model.LO, model.HI, h)
G = np.load(f'out/_figcache/{part}_{h:.3f}.npy')
xs, ys, zs = F.coords()
def top(x, y):
    i = int(round((x - xs[0]) / h)); j = int(round((y - ys[0]) / h))
    col = G[i, j, :]
    ins = np.where(col < 0)[0]
    if len(ins) == 0: return None
    # list of solid intervals
    runs = []; s = ins[0]; p = ins[0]
    for k in ins[1:]:
        if k != p + 1: runs.append((zs[s], zs[p])); s = k
        p = k
    runs.append((zs[s], zs[p]))
    return [(round(a, 1), round(b, 1)) for a, b in runs]
for a in sys.argv[3:]:
    x, y = map(float, a.split(','))
    print(a, top(x, y))
