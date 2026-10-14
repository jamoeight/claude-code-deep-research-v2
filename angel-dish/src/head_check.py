"""Printability check of the head region: python3 head_check.py [h] [parts]
Reports enclosed voids, disconnected solid islands and sub-0.8 mm thin regions inside the head/hair box."""
import sys, numpy as np
from scipy import ndimage
import model
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.2
parts = sys.argv[2].split(',') if len(sys.argv) > 2 else ['figure', 'head']
lo, hi = (-46, 2, 52), (12, 46, 104)
F = model.build(h, parts, verbose=False, lo=lo, hi=hi)
S = F.G < 0
# voids: air components not connected to the box boundary
air = ~S
lab, n = ndimage.label(air)
border = set(np.unique(np.concatenate([lab[0].ravel(), lab[-1].ravel(), lab[:, 0].ravel(), lab[:, -1].ravel(), lab[:, :, 0].ravel(), lab[:, :, -1].ravel()])))
cnt = np.bincount(lab.ravel())
voids = [(i, cnt[i]) for i in range(1, n + 1) if i not in border]
print('enclosed voids:', len(voids))
for i, c in sorted(voids, key=lambda t: -t[1])[:10]:
    idx = np.argwhere(lab == i).mean(0)
    print('  void voxels %d at' % c, (F.lo + idx * h).round(1))
# islands
lab2, n2 = ndimage.label(S)
cnt2 = np.bincount(lab2.ravel()); cnt2[0] = 0
main = np.argmax(cnt2)
isl = [(i, cnt2[i]) for i in range(1, n2 + 1) if i != main]
print('solid islands:', len(isl))
for i, c in sorted(isl, key=lambda t: -t[1])[:10]:
    idx = np.argwhere(lab2 == i).mean(0)
    print('  island voxels %d at' % c, (F.lo + idx * h).round(1))
# thin: solid voxels removed by an opening with a ball of radius 0.4 mm (features thinner than ~0.8 mm)
r = max(1, int(round(0.4 / h)))
zz, yy, xx = np.mgrid[-r:r + 1, -r:r + 1, -r:r + 1]
ball = (xx ** 2 + yy ** 2 + zz ** 2) <= r * r
op = ndimage.binary_opening(S, structure=ball)
thin = S & ~op
labt, nt = ndimage.label(thin)
cntt = np.bincount(labt.ravel()); cntt[0] = 0
big = [(i, cntt[i]) for i in range(1, nt + 1) if cntt[i] >= 8]
print('thin (<~0.8mm) clusters >= 8 voxels:', len(big), 'total thin voxels', int(thin.sum()))
for i, c in sorted(big, key=lambda t: -t[1])[:15]:
    idx = np.argwhere(labt == i).mean(0)
    print('  thin voxels %d at' % c, (F.lo + idx * h).round(1))
