"""leftmost solid x per (y,z) for dish and cached wings (h 0.45 full grid)."""
import sys, glob, numpy as np
import model, dish
from sdf import Field
h = 0.45
F = Field(model.LO, model.HI, h)
D = dish.component(F.blank()).G
W = np.load(sorted(glob.glob('out/cache/wings_*.npy'), key=lambda f: -__import__('os').path.getmtime(f))[0])
xs, ys, zs = F.coords()
def leftmost(G, y, z):
    j = int(round((y - F.lo[1]) / h)); k = int(round((z - F.lo[2]) / h))
    col = np.where(G[:, j, k] < 0)[0]
    return xs[col[0]] if len(col) else None
for y in (-10, -15, -20, -25, -30, -35, -40, -45):
    print('y=%4d' % y, '  '.join('z%2d d%6s w%6s' % (z, ('%.1f' % leftmost(D, y, z)) if leftmost(D, y, z) is not None else '-', ('%.1f' % leftmost(W, y, z)) if leftmost(W, y, z) is not None else '-') for z in (1, 6, 12, 18, 24, 30, 36, 44)))
