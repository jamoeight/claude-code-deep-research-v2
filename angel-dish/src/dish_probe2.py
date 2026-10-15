import sys, glob, os, numpy as np
import model, dish
from sdf import Field
h = 0.45
F = Field(model.LO, model.HI, h)
D = dish.component(F.blank()).G
W = np.load(sorted(glob.glob('out/cache/wings_*.npy'), key=lambda f: -os.path.getmtime(f))[0])
xs, ys, zs = F.coords()
def I(v, ax): return int(round((v - F.lo[ax]) / h))
print('back: per x, wing solid y-range & min z (y 20..50), dish max z per y')
for x in range(-10, 90, 6):
    i = I(x, 0)
    sl = W[i] < 0          # (y,z)
    # wing lowest z for each y in 15..50
    out = []
    for y in (20, 25, 30, 33, 36, 39, 42, 45):
        j = I(y, 1)
        kw = np.where(sl[j])[0]; kd = np.where(D[i, j] < 0)[0]
        out.append('y%d w%s d%s' % (y, ('%.0f' % zs[kw[0]]) if len(kw) else '-', ('%.0f' % zs[kd[-1]]) if len(kd) else '-'))
    print('x=%3d ' % x, ' | '.join(out))
print('right end: wing min z / dish max z at x, y')
for x in (66, 70, 74, 78, 82, 86):
    i = I(x, 0)
    print('x=%d' % x, ' | '.join('y%d w%s d%s' % (y, ('%.0f' % zs[np.where(W[i, I(y,1)] < 0)[0][0]]) if (W[i, I(y,1)] < 0).any() else '-', ('%.0f' % zs[np.where(D[i, I(y,1)] < 0)[0][-1]]) if (D[i, I(y,1)] < 0).any() else '-') for y in (-15, -10, -5, 0, 5, 10, 15, 20)))
