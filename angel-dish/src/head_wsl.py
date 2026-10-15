"""python3 head_wsl.py out.png x0 [x1 ...] : world x-slices (y horizontal 14..32, z vertical 60..92) of head (red) + figure cache (grey), h 0.3"""
import sys, os, numpy as np
from PIL import Image, ImageDraw
from sdf import Field
os.environ['HEAD_NOCLOSE'] = os.environ.get('HEAD_NOCLOSE', '0')
import head, cam
h = 0.3
LO, HI = (-46, 2, 0), (12, 46, 104)
F = Field(LO, HI, h)
fig = np.load('out/figcache_0.30.npy')
G = head.component(F.blank()).G
outs = []
loc = cam.frame()[0]
for xv in [float(v) for v in sys.argv[2:]]:
    i = int(round((xv - LO[0]) / h))
    j0, j1 = int((14 - LO[1]) / h), int((32 - LO[1]) / h); k0, k1 = int((60 - LO[2]) / h), int((92 - LO[2]) / h)
    g = G[i, j0:j1, k0:k1].T[::-1]; f = fig[i, j0:j1, k0:k1].T[::-1]
    img = np.full(g.shape + (3,), 255, np.uint8)
    img[f < 0] = (170, 170, 170); img[g < 0] = (220, 120, 120); img[(g < 0) & (f < 0)] = (150, 90, 90)
    im = Image.fromarray(img).resize((g.shape[1] * 4, g.shape[0] * 4), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for y in range(14, 33, 2):
        X = (y - 14) / h * 4; d.line([(X, 0), (X, 8)], fill=(0, 0, 255)); d.text((X + 1, 9), str(y), fill=(0, 0, 255))
    for z in range(60, 93, 2):
        Y = (92 - z) / h * 4; d.line([(0, Y), (8, Y)], fill=(0, 0, 255)); d.text((10, Y - 5), str(z), fill=(0, 0, 255))
    # camera direction arrow
    c = np.array([xv, 20.0, 66.0]); dv = loc - c; dv /= np.linalg.norm(dv)
    p0 = ((c[1] - 14) / h * 4, (92 - c[2]) / h * 4); p1 = (p0[0] + dv[1] * 60, p0[1] - dv[2] * 60)
    d.line([p0, p1], fill=(0, 160, 0), width=2); d.text((5, im.height - 14), 'x=%.1f (cam: green)' % xv, fill=(0, 0, 0))
    outs.append(im)
W = sum(o.width for o in outs) + 4 * len(outs)
o = Image.new('RGB', (W, outs[0].height), (0, 0, 0)); x = 0
for im in outs:
    o.paste(im, (x, 0)); x += im.width + 4
o.save(sys.argv[1])
