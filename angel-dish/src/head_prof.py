"""radial hair-surface profile across the parting (head agent debug tool)."""
import sys, math, numpy as np
from sdf import Field
import head, head_hair as hh
from head_hair import CAP_C, CAP_R, cap_local
from scipy.ndimage import map_coordinates
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.25
F = Field((-45, -5, 50), (15, 50, 108), h)
S = F.blank(); head.build_face(S)
stages = {}
orig_combine = None
Hc = S.blank(); hh.cap_volume(Hc)
stages['cap'] = Hc.G.copy()
S2 = F.blank(); head.build_face(S2); hh.build_hair(S2)
stages['final'] = S2.G
def surf(G, phi, th):
    d = np.array([math.cos(math.radians(th)) * math.sin(math.radians(phi)), math.cos(math.radians(th)) * math.cos(math.radians(phi)), math.sin(math.radians(th))])
    rs = np.arange(4, 12, 0.05)
    L = CAP_C[None] + rs[:, None] * (d * CAP_R / np.linalg.norm(d * CAP_R))[None]
    W = head.P(L)
    v = map_coordinates(G, ((W - F.lo) / F.h).T, order=1, mode='nearest')
    i = np.where(v < 0)[0]
    return rs[i[-1]] if len(i) else float('nan')
for th in [35, 50, 65]:
    print('theta', th)
    for name, G in stages.items():
        print('  %-6s' % name, ' '.join('%5.2f' % surf(G, p, th) for p in range(-40, 31, 4)))
print('phi    ', ' '.join('%5d' % p for p in range(-40, 31, 4)))
