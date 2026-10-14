"""ASCII slices of the combined field (others cached + wings) - wings agent tool.
   python3 wings_slice.py z=26 x0,x1,y0,y1 [h]"""
import sys, os, glob
import numpy as np
import model, wings
from sdf import Field
ax, val = sys.argv[1].split('='); val = float(val)
x0, x1, y0, y1 = [float(t) for t in sys.argv[2].split(',')]
h = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
p = sorted(glob.glob('out/_cache/others_*.npy'), key=os.path.getmtime)
F = Field(model.LO, model.HI, h)
O = None
for q in p[::-1]:
    G = np.load(q, mmap_mode='r')
    if G.shape == F.shape:
        O = np.array(G); break
W = wings.component(F.blank()).G
def sample(G, P):
    i = np.round((P - F.lo) / h).astype(int)
    return G[i[..., 0], i[..., 1], i[..., 2]]
A = np.arange(x0, x1, 1.0); B = np.arange(y1, y0, -1.0)
for b in B:
    row = ''
    for a in A:
        P = {'z': (a, b, val), 'y': (a, val, b), 'x': (val, a, b)}[ax]
        P = np.array(P)
        w = sample(W, P); o = sample(O, P) if O is not None else 9
        row += '#' if (w < 0 and o < 0) else ('W' if w < 0 else ('o' if o < 0 else '.'))
    print(f'{b:6.0f} ' + row)
print('       ' + ''.join(str(int(abs(a)) % 10) for a in A))
