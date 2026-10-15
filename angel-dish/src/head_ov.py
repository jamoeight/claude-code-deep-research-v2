"""python3 head_ov.py out.png [render.png] [--box x0,y0,x1,y1] [--scale 4] [--h 0.5] [--only RS,RF]
Builds the head hair (h coarse) and draws every ribbon centre line (projected with the ref camera) over the reference
crop (left) and an optional render (right)."""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
import cam
a = sys.argv[1:]
def opt(n, d):
    return a[a.index(n) + 1] if n in a else d
out = a[0]
rend = a[1] if len(a) > 1 and not a[1].startswith('--') else None
box = tuple(int(v) for v in opt('--box', '320,100,540,380').split(','))
s = float(opt('--scale', '4')); h = float(opt('--h', '0.5'))
only = opt('--only', '')
os.environ['HEAD_NOCLOSE'] = '1'
from sdf import Field
import head, head_hair
F = Field((-45, -5, 50), (15, 50, 108), h)
head.component(F)
COL = {'RF': (255, 60, 60), 'RS': (255, 200, 0), 'RM': (255, 120, 255), 'RU': (160, 80, 255), 'RB': (0, 160, 255), 'CB': (0, 255, 255),
       'LF': (60, 255, 60), 'LS': (0, 140, 60), 'LB': (0, 90, 200), 'RR': (255, 255, 255)}
ims = []
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
srcs = [ref] + ([Image.open(rend).convert('RGB')] if rend else [])
for im in srcs:
    if im.size != ref.size:
        # a refzoom render of the same box
        im = im.resize((int((box[2] - box[0]) * s), int((box[3] - box[1]) * s)), Image.LANCZOS)
    else:
        im = im.crop(box).resize((int((box[2] - box[0]) * s), int((box[3] - box[1]) * s)), Image.LANCZOS)
    d = ImageDraw.Draw(im)
    for name, C, W in head_hair.CENTRES:
        if only and name not in only.split(','):
            continue
        uv = cam.project(C)
        pts = [((u - box[0]) * s, (v - box[1]) * s) for u, v in uv]
        d.line(pts, fill=COL.get(name, (255, 255, 255)), width=2)
        d.text(pts[-1], name, fill=COL.get(name, (255, 255, 255)))
    ims.append(im)
o = Image.new('RGB', (sum(i.width for i in ims), ims[0].height))
x = 0
for i in ims:
    o.paste(i, (x, 0)); x += i.width
o.save(out)
