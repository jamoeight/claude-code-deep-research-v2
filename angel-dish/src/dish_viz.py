"""Quick 2D look at the outer-wall relief of the dish (unrolled: S right, Z up), no meshing/rendering.
   python3 dish_viz.py out.png [--fine] [--s0 -80 --s1 150]
Top panel: shaded relief (light from upper right / front).  Bottom panel: overhang map
(green <45, yellow 45-52, red >52 deg) of the outer wall, with the wall top line."""
import sys, math
import numpy as np
from PIL import Image
import dish as Dm
import dish_geo as G

a = sys.argv[1:]
out = a[0]
fine = '--fine' in a
s0 = float(a[a.index('--s0') + 1]) if '--s0' in a else -80.0
s1 = float(a[a.index('--s1') + 1]) if '--s1' in a else 150.0
LIP, ZW = Dm.lip_tables()
D, DL, NTab = Dm.wall_table(ZW, fine)
Z = Dm.DZ0 + Dm.DZS * np.arange(Dm.NZ)
S = G.ST
o = np.argsort(S)
# resample to a regular (s, z) grid, px = 0.1
px = 0.1 if not fine else 0.05
sg = np.arange(s0, s1, px)
zg = np.arange(0.0, 36.0, px)
ii = np.interp(sg, S[o], np.arange(len(S))[o])
i0 = np.floor(ii).astype(int) % len(S); f = ii - np.floor(ii)
i1 = (i0 + 1) % len(S)
kz = (zg - Dm.DZ0) / Dm.DZS
k0 = np.floor(kz).astype(int); fz = kz - k0
Dg = (D[i0][:, k0] * (1 - f)[:, None] + D[i1][:, k0] * f[:, None]) * (1 - fz)[None] + \
     (D[i0][:, k0 + 1] * (1 - f)[:, None] + D[i1][:, k0 + 1] * f[:, None]) * fz[None]
phi = np.interp(sg, S[o], G.PH[o])
base = G.R0(phi)[:, None] + G.FL(phi)[:, None] * np.clip(zg[None] / np.maximum(G.at(ZW, phi)[:, None], 1), 0, 1.3) ** 1.6
R = base + Dg
zw = G.at(ZW, phi)
gs = np.gradient(R, px, axis=0) * (base.mean() / R.clip(1)) * 0 + np.gradient(R, px, axis=0)
gz = np.gradient(R, px, axis=1)
# outward normal ~ (-gs, 1, -gz) in (s, r, z)
n = np.stack([-gs, np.ones_like(gs), -gz], -1)
n /= np.linalg.norm(n, axis=-1, keepdims=True)
L = np.array([0.45, 0.55, 0.70]); L /= np.linalg.norm(L)
sh = np.clip(0.55 + 0.6 * (n * L).sum(-1) - 0.3, 0.05, 1)
mask = zg[None] <= zw[:, None]
img = (sh * 255).astype(np.uint8)
img = np.where(mask, img, 40)
ov = np.degrees(np.arctan(np.maximum(gz, 0)))
col = np.zeros(gz.shape + (3,), np.uint8)
col[...] = (90, 180, 90)
col[ov > 45] = (230, 210, 60)
col[ov > 52] = (220, 50, 40)
col[~mask] = (30, 30, 30)
A = np.flipud(img.T)
B = np.flipud(np.transpose(col, (1, 0, 2)))
top = np.stack([A] * 3, -1)
o_ = np.concatenate([top, np.full((6, top.shape[1], 3), 255, np.uint8), B], 0)
im = Image.fromarray(o_)
# grid ticks every 10 units of s
from PIL import ImageDraw
d = ImageDraw.Draw(im)
for sv in range(int(math.ceil(s0 / 10) * 10), int(s1), 10):
    x = int((sv - s0) / px)
    d.line((x, 0, x, 8), fill=(255, 0, 0) if sv == 0 else (0, 120, 255))
    d.text((x + 2, 0), str(sv), fill=(0, 120, 255))
im.save(out)
print('saved', out, im.size, 'overhang>52 area %.1f, >45 %.1f (unit^2)' % ((ov[mask] > 52).sum() * px * px, (ov[mask] > 45).sum() * px * px))
