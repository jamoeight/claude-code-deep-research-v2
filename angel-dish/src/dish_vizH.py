"""Top-down shaded relief of the dish interior height field (plan view, +y up in the image).
   python3 dish_vizH.py out.png"""
import sys
import numpy as np
from PIL import Image, ImageDraw
import dish as Dm


class _F:
    def __init__(self, h):
        self.h = h
        self.xs = np.arange(-70, 90, h); self.ys = np.arange(-66, 50, h)

    def coords(self):
        return self.xs, self.ys, None


h = 0.25
F = _F(h)
LIP, ZW = Dm.lip_tables()
H = Dm.heightfield(F, ZW, False)
gx, gy = np.gradient(H, h)
n = np.stack([-gx, -gy, np.ones_like(H)], -1); n /= np.linalg.norm(n, axis=-1, keepdims=True)
L = np.array([0.5, 0.6, 0.62]); L /= np.linalg.norm(L)
sh = np.clip(0.25 + 0.85 * (n * L).sum(-1), 0, 1)
img = (sh * 255).astype(np.uint8).T[::-1]
rgb = np.stack([img] * 3, -1)
H2 = np.clip(H, 0, 40).T[::-1]
rgb[(H2 > 30)] = (rgb[(H2 > 30)] * 0.5).astype(np.uint8)
im = Image.fromarray(rgb).resize((rgb.shape[1] * 2, rgb.shape[0] * 2))
d = ImageDraw.Draw(im)
for x in range(-70, 90, 10):
    X = (x + 70) / h * 2
    d.line((X, 0, X, 12), fill=(255, 0, 0)); d.text((X + 2, 0), str(x), fill=(255, 0, 0))
for y in range(-60, 50, 10):
    Y = (50 - y) / h * 2
    d.line((0, Y, 12, Y), fill=(255, 0, 0)); d.text((14, Y - 6), str(y), fill=(255, 0, 0))
im.save(sys.argv[1])
print('saved', sys.argv[1], im.size)
