"""Lip crest heights of the left wing (contract C1) - wings agent tool.  python3 wings_crest.py [h]"""
import sys, os
os.environ['WINGS_ONLY'] = 'left'
import numpy as np
import wings
from sdf import Field
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.35
F = Field((-82, -56, 0), (-20, 12, 70), h)
S, rel = wings.build_left(F)
from wings_core import fill
fill(F, S, rel)
G = F.G
xs = F.lo[0] + np.arange(G.shape[0]) * h; ys = F.lo[1] + np.arange(G.shape[1]) * h; zs = F.lo[2] + np.arange(G.shape[2]) * h
for X, Y0, Y1 in [(-75, -12, 2), (-66, -36, -22), (-45, -50, -36), (-40, -52, -38), (-36, -52, -38), (-32, -52, -38), (-28, -52, -38)]:
    i = int(round((X - F.lo[0]) / h))
    j0 = int((Y0 - F.lo[1]) / h); j1 = int((Y1 - F.lo[1]) / h)
    sub = G[i, j0:j1] < 0
    if not sub.any():
        print(X, 'none'); continue
    zi = np.where(sub.any(1), (np.arange(sub.shape[1])[None] * sub).max(1), -1)
    jm = np.argmax(zi)
    ysol = ys[j0:j1][sub.any(1)]
    print(f'x={X}: crest z={zs[zi[jm]]:.1f} at y={ys[j0 + jm]:.1f}; solid y {ysol.min():.1f}..{ysol.max():.1f}')
