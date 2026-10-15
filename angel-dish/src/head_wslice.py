"""python3 head_wslice.py out.png z1,z2,... [h]: world z-slices (x horizontal, y vertical: front = down) of
head+hair (red) over the figure body proxy (blue); camera-ray direction drawn (head agent tool)."""
import sys, numpy as np
from PIL import Image, ImageDraw
from scipy.ndimage import map_coordinates
from sdf import Field
import head, head_hair as hh, cam
out = sys.argv[1]; zs = [float(v) for v in sys.argv[2].split(',')]; h = float(sys.argv[3]) if len(sys.argv) > 3 else 0.25
F = Field((-45, -5, 50), (15, 50, 108), h)
S = head.component(F)
body = hh.LAST_BODY
x = np.arange(-36, -2, 0.05); y = np.arange(8, 36, 0.05)
X, Y = np.meshgrid(x, y)
tiles = []
loc = cam.frame()[0]
for z in zs:
    W = np.stack([X, Y, np.full_like(X, z)], -1).reshape(-1, 3)
    dS = map_coordinates(S.G, ((W - S.lo) / S.h).T, order=1, mode='nearest').reshape(X.shape)
    dB = body.d(W).reshape(X.shape)
    img = np.full(X.shape + (3,), 255, np.uint8)
    img[dB < 0] = (150, 150, 230)
    img[(dS < 0) & (dB >= 0)] = (230, 120, 120)
    img[(dS < 0) & (dB < 0)] = (190, 110, 190)
    for i, xv in enumerate(x):
        if abs(xv - round(xv)) < 0.026:
            img[:, i] = img[:, i] * 0.75
    for j, yv in enumerate(y):
        if abs(yv - round(yv)) < 0.026:
            img[j, :] = img[j, :] * 0.75
    im = Image.fromarray(img)
    d = ImageDraw.Draw(im)
    d.text((5, 5), 'z=%.1f  x[-36,-2] y[8,36] (y down = back)' % z, fill=(0, 0, 0))
    # camera ray direction (projected to the xy plane) from the slice centre
    c = np.array([-18, 20, z]); r = c - loc; r /= np.linalg.norm(r)
    p0 = ((c[0] - x[0]) / 0.05, (c[1] - y[0]) / 0.05); p1 = (p0[0] - r[0] * 60, p0[1] - r[1] * 60)
    d.line([p0, p1], fill=(0, 140, 0), width=2)
    tiles.append(im)
o = Image.new('RGB', (sum(t.width for t in tiles), tiles[0].height), 'white')
xo = 0
for t in tiles:
    o.paste(t, (xo, 0)); xo += t.width
o.save(out)
