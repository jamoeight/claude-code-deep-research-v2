"""Slices of the figure field (cached) with a coordinate grid -> png.
python3 figure_cut.py out.png [--rebuild] [--h 0.3] [--win x0,x1,y0,y1] x=-15 y=10 z=56 ...
(x cut: horizontal axis y, vertical z; y cut: x/z; z cut: x/y).  Dish (cached) drawn blue-grey."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model
from sdf import Field
a = sys.argv[1:]
out = a[0]
h = float(a[a.index('--h') + 1]) if '--h' in a else 0.3
fn = os.path.join('out', '_figcache', 'figself_full_%.3f.npy' % h)
F = Field(model.LO, model.HI, h)
if '--rebuild' in a or not os.path.exists(fn):
    import figure
    G = figure.component(F.blank()).G
    np.save(fn, G)
else:
    G = np.load(fn)
dn = f'out/_figcache/dish_{h:.3f}.npy'
D = np.load(dn) if os.path.exists(dn) else None
xs, ys, zs = F.coords()
S_ = 4 if h <= 0.3 else 3
ims = []
for c in [x for x in a[1:] if '=' in x and x[0] in 'xyz']:
    ax, v = c.split('='); v = float(v)
    if ax == 'x':
        i = int(round((v - xs[0]) / h)); S = G[i, :, :]; SD = D[i] if D is not None else None; hor, ver = ys, zs
        win = (-10, 45, 0, 90)
    elif ax == 'y':
        j = int(round((v - ys[0]) / h)); S = G[:, j, :]; SD = D[:, j] if D is not None else None; hor, ver = xs, zs
        win = (-60, 25, 0, 90)
    else:
        k = int(round((v - zs[0]) / h)); S = G[:, :, k]; SD = D[:, :, k] if D is not None else None; hor, ver = xs, ys
        win = (-55, 20, -15, 45)
    if '--win' in a:
        win = tuple(float(t) for t in a[a.index('--win') + 1].split(','))
    i0, i1 = np.searchsorted(hor, win[0]), np.searchsorted(hor, win[1])
    j0, j1 = np.searchsorted(ver, win[2]), np.searchsorted(ver, win[3])
    S = S[i0:i1, j0:j1]
    img = np.full(S.shape + (3,), 255, np.uint8)
    img[S < 0] = (200, 120, 130)
    if SD is not None:
        SD = SD[i0:i1, j0:j1]; img[(SD < 0) & (S >= 0)] = (160, 160, 200)
    img = np.transpose(img, (1, 0, 2))[::-1]
    im = Image.fromarray(img).resize((img.shape[1] * S_, img.shape[0] * S_), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for t in range(int(np.ceil(win[0])), int(win[1]) + 1):
        X = (t - hor[i0]) / h * S_
        col = (0, 0, 0) if t % 5 == 0 else (215, 215, 215)
        d.line((X, 0, X, im.height), fill=col if t % 5 == 0 else (230, 230, 230), width=1)
        if t % 5 == 0:
            d.text((X + 2, im.height - 12), str(t), fill=(0, 0, 0))
    for t in range(int(np.ceil(win[2])), int(win[3]) + 1):
        Y = im.height - (t - ver[j0]) / h * S_
        if t % 5 == 0:
            d.line((0, Y, im.width, Y), fill=(0, 0, 0)); d.text((2, Y - 12), str(t), fill=(0, 0, 0))
        else:
            d.line((0, Y, im.width, Y), fill=(230, 230, 230))
    d.text((40, 5), c, fill=(0, 0, 255))
    ims.append(im)
W = max(i.width for i in ims); H = sum(i.height for i in ims)
o = Image.new('RGB', (W, H), 'white'); y = 0
for i in ims:
    o.paste(i, (0, y)); y += i.height
o.save(out)
print(out, o.size)
