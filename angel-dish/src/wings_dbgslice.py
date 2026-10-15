"""Fine ASCII slice of the right/left wing alone in a small box (wings agent debug tool).
   python3 wings_dbgslice.py right|left z=70 x0,x1,y0,y1 [h=0.2]"""
import sys, os
import numpy as np
os.environ['WINGS_ONLY'] = sys.argv[1]
import wings
from sdf import Field
ax, val = sys.argv[2].split('='); val = float(val)
a0, a1, b0, b1 = [float(t) for t in sys.argv[3].split(',')]
h = float(sys.argv[4]) if len(sys.argv) > 4 else 0.2
if ax == 'z':
    lo, hi = (a0, b0, val - 1), (a1, b1, val + 1)
elif ax == 'y':
    lo, hi = (a0, val - 1, b0), (a1, val + 1, b1)
else:
    lo, hi = (val - 1, a0, b0), (val + 1, a1, b1)
F = Field(lo, hi, h)
S, rel = (wings.build_right if sys.argv[1] == 'right' else wings.build_left)(F)
from wings_core import fill
fill(F, S, rel)
G = F.G
k = {'x': 0, 'y': 1, 'z': 2}[ax]
i = int(round((val - F.lo[k]) / h))
sl = np.take(G, i, axis=k)
step = max(int(round(0.4 / h)), 1)
sl = sl[::step, ::step]
for r in range(sl.shape[1] - 1, -1, -1):
    print('%6.1f ' % (F.lo[1 if k != 1 else 2] + r * step * h) + ''.join('#' if g < 0 else '.' for g in sl[:, r]))
