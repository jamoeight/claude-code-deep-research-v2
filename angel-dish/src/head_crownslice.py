"""local horizontal slices through the crown: face+cap (blue), final head (red). python3 head_crownslice.py out.png"""
import sys, os, numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
from sdf import Field
import head, head_hair as hh
F = Field((-45, -5, 50), (15, 50, 108), 0.15)
S = head.component(F)
C = F.blank(); hh.cap_volume(C)
tiles = []
for zl in (6.0, 7.0, 8.0):
    u = np.arange(-4, 4, 0.01); v = np.arange(-2, 7, 0.01)
    U, V = np.meshgrid(u, v)
    W = head.P(np.stack([U, V, np.full_like(U, zl)], -1).reshape(-1, 3))
    d = map_coordinates(S.G, ((W - F.lo) / F.h).T, order=1).reshape(U.shape)
    dc = map_coordinates(C.G, ((W - F.lo) / F.h).T, order=1).reshape(U.shape)
    img = np.full(U.shape + (3,), 255, np.uint8); img[d < 0] = (225, 150, 150); img[(dc < 0)] = (150, 150, 225)
    img[(dc < 0) & (d < 0)] = (190, 140, 200)
    for i, x in enumerate(u):
        if abs(x - round(x)) < 0.006: img[:, i] = img[:, i] * 0.6
    for j, y in enumerate(v):
        if abs(y - round(y)) < 0.006: img[j, :] = img[j, :] * 0.6
    im = Image.fromarray(img[::-1]); ImageDraw.Draw(im).text((4, 4), 'z=%.1f x[-4,4] y[-2,7]' % zl, fill=(0, 0, 0))
    tiles.append(im)
o = Image.new('RGB', (sum(t.width for t in tiles), tiles[0].height)); x = 0
for t in tiles: o.paste(t, (x, 0)); x += t.width
o.save(sys.argv[1])
