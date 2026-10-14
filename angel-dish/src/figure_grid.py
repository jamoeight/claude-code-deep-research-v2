"""Reference crops with a labelled pixel grid (helper for tracing folds).
python3 figure_grid.py out.png x0,y0,x1,y1 [--s 4] [--hp] [--step 10]"""
import sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
a = sys.argv[1:]
out = a[0]; box = tuple(int(v) for v in a[1].split(','))
s = int(a[a.index('--s') + 1]) if '--s' in a else 4
step = int(a[a.index('--step') + 1]) if '--step' in a else 10
src = a[a.index('--img') + 1] if '--img' in a else '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
ref = Image.open(src).convert('RGB')
if ref.size != (1179, 1078):
    ref = ref.resize((1179, 1078), Image.LANCZOS)
im = ref.crop(box)
if '--hp' in a:
    g = im.convert('L'); A = np.asarray(g).astype(float); B = np.asarray(g.filter(ImageFilter.GaussianBlur(10))).astype(float)
    im = Image.fromarray(np.clip((A - B) * 3 + 128, 0, 255).astype(np.uint8)).convert('RGB')
im = im.resize(((box[2] - box[0]) * s, (box[3] - box[1]) * s), Image.LANCZOS)
d = ImageDraw.Draw(im)
for x in range((box[0] // step + 1) * step, box[2], step):
    X = (x - box[0]) * s
    col = (0, 200, 255) if x % (step * 5) else (255, 60, 60)
    for y0 in range(0, im.height, 6):
        d.point((X, y0), fill=col)
    if x % (step * 2) == 0:
        d.text((X + 2, 2), str(x), fill=(255, 255, 0))
for y in range((box[1] // step + 1) * step, box[3], step):
    Y = (y - box[1]) * s
    col = (0, 200, 255) if y % (step * 5) else (255, 60, 60)
    for x0 in range(0, im.width, 6):
        d.point((x0, Y), fill=col)
    if y % (step * 2) == 0:
        d.text((2, Y + 2), str(y), fill=(255, 255, 0))
im.save(out)
