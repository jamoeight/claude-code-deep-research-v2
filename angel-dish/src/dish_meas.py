"""Front rim crest numbers (dish only).  python3 dish_meas.py [x1 x2 ...]
For each x: crest z (max solid z over y < -28), its y, and the innermost y of the rim at crest-2."""
import sys
import numpy as np
from sdf import Field
import dish

xs = [float(v) for v in sys.argv[1:]] or [-40, -30, -20, -10, 0, 10, 20, 28, 34, 40, 46, 52]
h = 0.25
for x in xs:
    F = Field((x - h, -66, 0), (x + h, -20, 40), h)
    F = dish.component(F)
    sl = F.G[F.G.shape[0] // 2]          # (y, z)
    ys = F.lo[1] + h * np.arange(sl.shape[0]); zs = F.lo[2] + h * np.arange(sl.shape[1])
    m = sl < 0
    mm = m & (ys[:, None] < -28)
    kz = np.where(mm.any(0))[0]
    if not len(kz):
        print(x, 'none'); continue
    ktop = kz.max(); zc = zs[ktop]
    yc = ys[np.where(mm[:, ktop])[0]].mean()
    k2 = np.searchsorted(zs, zc - 2.0)
    yin = ys[np.where(mm[:, k2])[0]].max()
    yout = ys[np.where(m[:, 4])[0]].min() if m[:, 4].any() else np.nan
    print(f'x {x:6.1f}: crest z {zc:5.1f} at y {yc:6.1f}; inner y at crest-2 {yin:6.1f}; foot y(z1) {yout:6.1f}')
