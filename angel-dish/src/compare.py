"""python3 compare.py render_ref.png out.png [--region NAME|x0,y0,x1,y1] [--lm]
Side-by-side: reference | render | 50% blend, cropped to the region (reference pixel coords)."""
import sys, json, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
REGIONS = {'full': (0, 0, 1179, 1078), 'figure': (250, 90, 620, 640), 'face': (360, 110, 540, 300),
           'wingR': (480, 30, 1179, 620), 'wingL': (0, 30, 430, 900), 'front': (0, 580, 1179, 1078),
           'torso': (300, 250, 600, 560), 'skirt': (300, 450, 800, 750)}
args = sys.argv[1:]
src, out = args[0], args[1]
region = 'full'; lm = '--lm' in args
if '--region' in args:
    region = args[args.index('--region') + 1]
box = REGIONS[region] if region in REGIONS else tuple(int(v) for v in region.split(','))
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
r = Image.open(src).convert('RGB').resize(ref.size, Image.LANCZOS)
if lm and os.path.exists(os.path.join(HERE, 'landmarks.json')):
    L = json.load(open(os.path.join(HERE, 'landmarks.json')))
    import cam
    import numpy as np
    for im in (ref, r):
        d = ImageDraw.Draw(im)
        for e in L:
            x, y = e['px']; d.ellipse((x - 5, y - 5, x + 5, y + 5), outline=(0, 255, 255), width=2)
    # where the design's 3D points actually project (on the render)
    d = ImageDraw.Draw(r)
    for e in L:
        if 'p3' in e:
            (x, y), = cam.project([e['p3']])
            d.line((x - 6, y, x + 6, y), fill=(255, 255, 0), width=2); d.line((x, y - 6, x, y + 6), fill=(255, 255, 0), width=2)
a = ref.crop(box); b = r.crop(box)
s = min(1.0, 2400 / (3 * a.width)) if region == 'full' else min(2.5, 2400 / (2 * a.width), 1300 / a.height)
a = a.resize((int(a.width * s), int(a.height * s)), Image.LANCZOS); b = b.resize(a.size, Image.LANCZOS)
panels = [a, b] if region != 'full' else [a, b, Image.blend(a, b, 0.5)]
o = Image.new('RGB', (a.width * len(panels), a.height), 'white')
for i, p in enumerate(panels):
    o.paste(p, (i * a.width, 0))
o.save(out)
