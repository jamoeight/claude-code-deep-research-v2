"""python3 head_dbg.py out.png [x0,y0,x1,y1] : draw hair guide paths (projected with the ref camera) on the reference."""
import sys
import numpy as np
from PIL import Image, ImageDraw
import cam, head_hair
REF = '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
out = sys.argv[1]
box = tuple(int(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '320,100,540,380').split(','))
s = 4
im = Image.open(REF).convert('RGB').crop(box)
im = im.resize((im.width * s, im.height * s), Image.BICUBIC)
d = ImageDraw.Draw(im)
cols = {'RF': (0, 255, 255), 'RS': (255, 255, 0), 'RB': (128, 128, 255), 'CB': (90, 90, 90), 'LF': (0, 255, 0), 'LS': (255, 0, 255), 'LB': (255, 255, 255), 'RM': (0, 120, 255), 'RU': (160, 0, 255)}
paths = head_hair.debug_paths()
for name, gs in paths.items():
    for g in gs:
        uv = cam.project(g)
        pts = [((u - box[0]) * s, (v - box[1]) * s) for u, v in uv]
        d.line(pts, fill=cols.get(name, (255, 0, 0)), width=2)
        d.ellipse((pts[109][0] - 4, pts[109][1] - 4, pts[109][0] + 4, pts[109][1] + 4), outline=(255, 0, 0))
        d.ellipse((pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3), fill=(255, 0, 0))
    d.text(((cam.project(gs[0][-1:])[0][0] - box[0]) * s, (cam.project(gs[0][-1:])[0][1] - box[1]) * s), name, fill=(255, 255, 255))
im.save(out)
for name, gs in paths.items():
    for g in gs:
        print(name, 'exit', g[109].round(1), 'end', g[-1].round(1), 'minz', g[:, 2].min().round(1))
