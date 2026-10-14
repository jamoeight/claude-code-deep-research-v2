"""python3 head_dbgback.py out.png : back orthographic view (from +y) of hair guide paths over the body silhouette."""
import sys, numpy as np
from PIL import Image, ImageDraw
import head_hair
from head_drape import Body
out = sys.argv[1]
b = Body()
x0, x1, z0, z1, s = -40, 2, 52, 102, 16
W, H = (x1 - x0) * s, (z1 - z0) * s
img = Image.new('RGB', (W, H), (40, 40, 40)); d = ImageDraw.Draw(img)
# body silhouette (min over y)
xs = np.arange(x0, x1, 0.25); zs = np.arange(z0, z1, 0.25)
for z in zs:
    for x in xs:
        ys = np.arange(5, 44, 0.5)
        P = np.stack([np.full_like(ys, x), ys, np.full_like(ys, z)], 1)
        if (b.d(P) < 0).any():
            d.rectangle(((x - x0) * s, (z1 - z) * s, (x - x0 + 0.25) * s, (z1 - z + 0.25) * s), fill=(90, 70, 70))
cols = {'RF': (0, 255, 255), 'RS1': (255, 255, 0), 'RS2': (255, 128, 0), 'RS3': (255, 60, 0), 'RB': (128, 128, 255), 'CB': (200, 200, 200),
        'LF': (0, 255, 0), 'LS': (255, 0, 255), 'LB': (255, 255, 255), 'RM': (0, 120, 255), 'RU': (160, 0, 255)}
paths = head_hair.debug_paths()
for name, gs in paths.items():
    for g in gs:
        pts = [((p[0] - x0) * s, (z1 - p[2]) * s) for p in g]
        d.line(pts, fill=cols.get(name, (255, 0, 0)), width=2)
        d.text(pts[-1], name, fill=cols.get(name, (255, 0, 0)))
img = img.transpose(Image.FLIP_LEFT_RIGHT)   # seen from behind: world -x on the right
img.save(out)
