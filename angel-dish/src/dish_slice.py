"""Vertical sections of the dish SDF (dish only).  python3 dish_slice.py out.png x=2 x=34 y=-20 ...
Each spec 'x=V' cuts the plane x=V (horizontal axis y), 'y=V' cuts y=V (horizontal axis x).
Draws solid in pink, 45/55 deg guide lines, grid every 5 units."""
import sys
import numpy as np
from PIL import Image, ImageDraw
from sdf import Field
import dish

out = sys.argv[1]
specs = sys.argv[2:] or ['x=2']
h = 0.2
panels = []
for sp in specs:
    ax, v = sp.split('='); v = float(v)
    if ax == 'x':
        lo, hi = (v - h, -68, -1), (v + h, -25, 34)
    else:
        lo, hi = (-90, v - h, -1), (96, v + h, 40)
    F = Field(lo, hi, h)
    F = dish.component(F)
    G = F.G
    sl = G[G.shape[0] // 2] if ax == 'x' else G[:, G.shape[1] // 2]
    img = np.where(sl.T[::-1] < 0, 0, 1)
    rgb = np.zeros(img.shape + (3,), np.uint8)
    rgb[img == 0] = (230, 140, 150); rgb[img == 1] = (250, 250, 250)
    im = Image.fromarray(rgb).resize((rgb.shape[1] * 3, rgb.shape[0] * 3), Image.NEAREST)
    d = ImageDraw.Draw(im)
    o = lo[1] if ax == 'x' else lo[0]
    W, H = im.size
    for g in range(int(np.ceil(o / 5) * 5), int(o + rgb.shape[1] * h), 5):
        x = (g - o) / h * 3
        d.line((x, 0, x, H), fill=(200, 200, 255) if g % 10 else (120, 120, 255))
    for z in range(0, 40, 5):
        y = H - (z - lo[2]) / h * 3
        d.line((0, y, W, y), fill=(200, 200, 255) if z % 10 else (120, 120, 255))
    d.text((5, 5), sp, fill=(0, 0, 0))
    panels.append(im)
W = max(p.size[0] for p in panels)
o = Image.new('RGB', (W, sum(p.size[1] + 4 for p in panels)), 'white')
y = 0
for p in panels:
    o.paste(p, (0, y)); y += p.size[1] + 4
o.save(out)
print('saved', out, o.size)
