"""python3 head_ov2.py out.png render_refzoom.png box scale names  : centre lines + projected rope edges over photo | render"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
import cam
out, rend = sys.argv[1], sys.argv[2]
box = tuple(int(v) for v in sys.argv[3].split(',')); s = float(sys.argv[4]); only = sys.argv[5].split(',')
os.environ['HEAD_NOCLOSE'] = '1'
from sdf import Field
import head, head_hair
F = Field((-45, -5, 50), (15, 50, 108), 0.45)
head.component(F)
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
A = ref.crop(box).resize((int((box[2] - box[0]) * s), int((box[3] - box[1]) * s)), Image.BICUBIC)
B = Image.open(rend).convert('RGB').resize(A.size, Image.LANCZOS)
loc = cam.frame()[0]
cols = [(255, 60, 60), (60, 255, 60), (80, 160, 255), (255, 220, 0), (255, 0, 255), (0, 255, 255)]
k = 0
for im in (A, B):
    d = ImageDraw.Draw(im); k = 0
    for name, C, W in head_hair.CENTRES:
        if name not in only:
            continue
        T = np.gradient(C, axis=0); T /= np.linalg.norm(T, axis=1)[:, None] + 1e-9
        v = loc[None] - C; v /= np.linalg.norm(v, axis=1)[:, None]
        Sd = np.cross(v, T); Sd /= np.linalg.norm(Sd, axis=1)[:, None] + 1e-9
        col = cols[k % len(cols)]; k += 1
        for P_ in (C, C + Sd * W[:, None], C - Sd * W[:, None]):
            uv = cam.project(P_)
            pts = [((u - box[0]) * s, (vv - box[1]) * s) for u, vv in uv]
            d.line(pts, fill=col, width=1 if P_ is not C else 2)
o = Image.new('RGB', (A.width * 2 + 6, A.height)); o.paste(A, (0, 0)); o.paste(B, (A.width + 6, 0)); o.save(out)
