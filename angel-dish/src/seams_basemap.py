"""Bottom heightmap: lowest solid z per column (integrator tool).  python3 seams_basemap.py field.npy out.png"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
p = sys.argv[1]
meta = json.load(open(os.path.join(os.path.dirname(p), 'raw.json')))
lo = np.array(meta['lo']); h = meta['h']
G = np.load(p, mmap_mode='r')
k0 = int(np.ceil((1e-6 - lo[2]) / h)); k1 = k0 + int(10 / h)
S = np.asarray(G[:, :, k0:k1]) < 0
has = S.any(2)
low = np.where(has, np.argmax(S, 2) * h, np.nan)
kf = int(np.floor((1.2 - lo[2]) / h)) - k0
foot = ndi.binary_fill_holes(S[:, :, :kf + 1].any(2))
img = np.zeros(has.shape + (3,), np.uint8)
v = np.clip(np.nan_to_num(low, nan=10) / 6.0, 0, 1)
img[..., 0] = (255 * (1 - v)).astype(np.uint8); img[..., 1] = (255 * (1 - v) * 0.6).astype(np.uint8); img[..., 2] = (80 * v).astype(np.uint8)
img[~has] = (255, 255, 255)
img[has & (low > 0.05) & foot] = (0, 160, 255)   # recess inside footprint (blue)
img[has & (low > 2.5) & foot] = (0, 0, 200)
edge = foot ^ ndi.binary_erosion(foot)
img[edge] = (0, 200, 0)
im = Image.fromarray(np.transpose(img, (1, 0, 2))[::-1])  # x right, y up
s = 3
im = im.resize((im.width * s, im.height * s), Image.NEAREST)
d = ImageDraw.Draw(im)
for x in range(-80, 100, 10):
    px = (x - lo[0]) / h * s
    d.line((px, 0, px, 8), fill=(0, 0, 0)); d.text((px + 2, 0), str(x), fill=(0, 0, 0))
for y in range(-60, 60, 10):
    py = (has.shape[1] - 1 - (y - lo[1]) / h) * s
    d.line((0, py, 8, py), fill=(0, 0, 0)); d.text((10, py - 5), str(y), fill=(0, 0, 0))
im.save(sys.argv[2]); print('saved', sys.argv[2], 'foot', foot.sum() * h * h, 'recess cols', (has & (low > 0.05) & foot).sum() * h * h)
