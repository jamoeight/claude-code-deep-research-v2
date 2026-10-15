"""fine radial profile across the parting from a cached head field (head agent debug tool)."""
import math, sys, numpy as np, os
from sdf import Field
import head
from head_hair import CAP_C, CAP_R
from scipy.ndimage import map_coordinates
F = Field((-45, -5, 50), (15, 50, 108), float(sys.argv[1]) if len(sys.argv) > 1 else 0.2)
S2 = head.component(F.blank())
np.save('out/headG.npy', S2.G)
def surf(G, phi, th):
    d = np.array([math.cos(math.radians(th)) * math.sin(math.radians(phi)), math.cos(math.radians(th)) * math.cos(math.radians(phi)), math.sin(math.radians(th))])
    rs = np.arange(5, 11, 0.01)
    L = CAP_C[None] + rs[:, None] * (d * CAP_R / np.linalg.norm(d * CAP_R))[None]
    W = head.P(L)
    v = map_coordinates(G, ((W - F.lo) / F.h).T, order=1, mode='nearest')
    i = np.where(v < 0)[0]
    return rs[i[-1]] if len(i) else float('nan')
ph = np.arange(-20, 4.1, 1.0)
for th in [42, 50, 58, 66, 74]:
    print('%2d' % th, ' '.join('%5.2f' % surf(S2.G, p, th) for p in ph))
print('ph', ' '.join('%5d' % p for p in ph))
