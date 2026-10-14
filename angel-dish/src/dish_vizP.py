"""Phase-line plot of the front-wall folds (valleys = integer P black, crests red) in unrolled (S, Z) coords,
plus the raw displacement in gray below.   python3 dish_vizP.py out.png [s0 s1]"""
import sys
import numpy as np
from PIL import Image, ImageDraw
import dish_fold as DF
import dish as Dm
import dish_geo as G

out = sys.argv[1]
s0 = float(sys.argv[2]) if len(sys.argv) > 2 else -80
s1 = float(sys.argv[3]) if len(sys.argv) > 3 else 140
px = 0.1
S, Z = np.meshgrid(np.arange(s0, s1, px), np.arange(0, 34, px), indexing='ij')
P, S2, Z2, r = DF.front_phase(S, Z)
D = DF.front_disp(S, Z)
LIP, ZW = Dm.lip_tables()
gP = np.hypot(*np.gradient(P, px))
fr = np.abs((P + 0.5) % 1.0 - 0.5) / np.maximum(gP, 1e-6)       # distance to nearest valley line
fc = np.abs(P % 1.0 - 0.5) / np.maximum(gP, 1e-6)
img = np.full(S.shape + (3,), 255, np.uint8)
img[fc < 0.12] = (220, 40, 40)
img[fr < 0.15] = (0, 0, 0)
phi = np.interp(S[:, 0], np.sort(G.ST), G.PH[np.argsort(G.ST)])
zw = G.at(ZW, phi)
for i in range(S.shape[0]):
    k = int(zw[i] / px)
    if 0 <= k < S.shape[1]:
        img[i, max(k - 2, 0):k + 2] = (0, 0, 255)
d = (np.clip((D - D.min()) / (np.ptp(D) + 1e-9), 0, 1) * 255).astype(np.uint8)
A = np.flipud(np.transpose(img, (1, 0, 2)))
B = np.flipud(np.stack([d.T] * 3, -1))
o = np.concatenate([A, np.full((5, A.shape[1], 3), 128, np.uint8), B], 0)
im = Image.fromarray(o)
dr = ImageDraw.Draw(im)
for sv in range(int(np.ceil(s0 / 10) * 10), int(s1), 10):
    x = int((sv - s0) / px)
    dr.line((x, 0, x, 10), fill=(0, 120, 255)); dr.text((x + 2, 0), str(sv), fill=(0, 120, 255))
for zv in range(0, 34, 5):
    y = A.shape[0] - int(zv / px)
    dr.line((0, y, 10, y), fill=(0, 120, 255)); dr.text((12, y - 10), str(zv), fill=(0, 120, 255))
im.save(out)
print('saved', out, im.size)
