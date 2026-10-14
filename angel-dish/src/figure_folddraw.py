"""Draw figure_folds.PX_FOLDS pixel paths on the reference (green crest, red valley, yellow tick = steep side)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
import figure_folds as FD
box = tuple(int(v) for v in sys.argv[2].split(',')) if len(sys.argv) > 2 else (280, 270, 720, 730)
s = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
src = sys.argv[4] if len(sys.argv) > 4 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'ref', 'reference.png')
ref = Image.open(src).convert('RGB').resize((1179, 1078), Image.LANCZOS)
c = ref.crop(box).resize((int((box[2] - box[0]) * s), int((box[3] - box[1]) * s)), Image.LANCZOS)
d = ImageDraw.Draw(c)
for i, sp in enumerate(FD.PX_FOLDS):
    pix = sp['pix']
    pts = [((x - box[0]) * s, (y - box[1]) * s) for x, y in pix]
    d.line(pts, fill=(0, 255, 0) if sp['A'] > 0 else (255, 0, 0), width=2)
    side = FD.steep_side(pix, sp['steep'])
    p = np.asarray(pts); m = len(p) // 2; t = p[min(m + 1, len(p) - 1)] - p[max(m - 1, 0)]; t /= np.linalg.norm(t) + 1e-9
    left = np.array([t[1], -t[0]])
    nv = left if side == 'L' else -left
    d.line([tuple(p[m]), tuple(p[m] + nv * 10)], fill=(255, 255, 0), width=2)
    d.text((pts[0][0] + 3, pts[0][1] - 10), str(i), fill=(255, 255, 0))
poly = [((x - box[0]) * s, (y - box[1]) * s) for x, y in FD.VNECK]
d.line(poly + [poly[0]], fill=(0, 255, 255), width=1)
c.save(sys.argv[1])
