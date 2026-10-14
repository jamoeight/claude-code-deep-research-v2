"""Vertical slices of the figure field (and the cached dish) -> png.  python3 figure_slice.py out.png h x=-15 y=10 ..."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
import model, figure
from sdf import Field
out = sys.argv[1]; h = float(sys.argv[2]); cuts = sys.argv[3:]
F = Field(model.LO, model.HI, h)
G = figure.component(F.blank()).G
dn = f'out/_figcache/dish_{h:.3f}.npy'
D = np.load(dn) if os.path.exists(dn) else None
xs, ys, zs = F.coords()
ims = []
for c in cuts:
    ax, v = c.split('='); v = float(v)
    if ax == 'x':
        i = int(round((v - xs[0]) / h)); S = G[i, :, :]; SD = D[i] if D is not None else None; hor = ys
    else:
        j = int(round((v - ys[0]) / h)); S = G[:, j, :]; SD = D[:, j] if D is not None else None; hor = xs
    zmax = 60; kz = int((zmax - zs[0]) / h)
    S = S[:, :kz]; img = np.full(S.shape + (3,), 255, np.uint8)
    img[S < 0] = (200, 120, 130)
    if SD is not None:
        SD = SD[:, :kz]; img[(SD < 0) & (S >= 0)] = (150, 150, 200)
    img = np.transpose(img, (1, 0, 2))[::-1]
    im = Image.fromarray(img).resize((img.shape[1] * 2, img.shape[0] * 2), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for zz in range(0, zmax, 10):
        Y = (kz - (zz - zs[0]) / h) * 2; d.line((0, Y, 10, Y), fill=(0, 0, 0)); d.text((12, Y - 6), str(zz), fill=(0, 0, 0))
    for hh in range(-60, 100, 10):
        X = (hh - hor[0]) / h * 2
        if 0 < X < im.width:
            d.line((X, im.height - 10, X, im.height), fill=(0, 0, 0)); d.text((X + 2, im.height - 22), str(hh), fill=(0, 0, 0))
    d.text((5, 5), c, fill=(0, 0, 0))
    ims.append(im)
W = max(i.width for i in ims); H = sum(i.height for i in ims)
o = Image.new('RGB', (W, H), 'white'); y = 0
for i in ims:
    o.paste(i, (0, y)); y += i.height
o.save(out)
