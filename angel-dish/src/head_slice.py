"""python3 head_slice.py out.png axis val [h]: head-local slice (axis x|y|z = val) of face-only vs face+hair contours."""
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
from sdf import Field
import head, head_hair as hh
out, ax, val = sys.argv[1], sys.argv[2], float(sys.argv[3]); h = float(sys.argv[4]) if len(sys.argv) > 4 else 0.25
F = Field((-45, -5, 50), (15, 50, 108), h)
A = F.blank(); head.build_face(A)
B = F.blank(); head.build_face(B); hh.build_hair(B)
u = np.arange(-11, 11, 0.05); v = np.arange(-11, 13, 0.05)
U, V = np.meshgrid(u, v)
if ax == 'x':
    L = np.stack([np.full_like(U, val), U, V], -1); lab = ('y (fwd)', 'z')
elif ax == 'y':
    L = np.stack([U, np.full_like(U, val), V], -1); lab = ('x (her left)', 'z')
else:
    L = np.stack([U, V, np.full_like(U, val)], -1); lab = ('x', 'y')
W = head.P(L.reshape(-1, 3))
img = np.zeros(U.shape + (3,), np.uint8) + 255
dA = map_coordinates(A.G, ((W - F.lo) / F.h).T, order=1, mode='nearest').reshape(U.shape)
dB = map_coordinates(B.G, ((W - F.lo) / F.h).T, order=1, mode='nearest').reshape(U.shape)
img[dB < 0] = (230, 150, 150)
img[dA < 0] = (150, 150, 230)
# grid every 1 unit
for i, x in enumerate(u):
    if abs(x - round(x)) < 0.026:
        img[:, i] = img[:, i] // 2 + (60 if round(x) % 5 else 0)
for j, y in enumerate(v):
    if abs(y - round(y)) < 0.026:
        img[j, :] = img[j, :] // 2 + (60 if round(y) % 5 else 0)
im = Image.fromarray(img[::-1]); im = im.resize((im.width * 2, im.height * 2), Image.NEAREST)
ImageDraw.Draw(im).text((10, 10), f'{ax}={val}  horiz {lab[0]} [-11,11]  vert {lab[1]} [-11,13]', fill=(0, 0, 0))
im.save(out)
