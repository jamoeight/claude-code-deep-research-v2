"""python3 head_blend.py r_ref.png out.png [box] : ref | render | edges overlay (ref edges red, render edges cyan)"""
import sys, os
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
box = [int(v) for v in (a[2] if len(a) > 2 else '380,110,530,300').split(',')]
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
r = Image.open(a[0]).convert('RGB').resize(ref.size, Image.LANCZOS)
s = 900 / (box[3] - box[1])
A = ref.crop(box); B = r.crop(box)
size = (int(A.width * s), int(A.height * s))
A = A.resize(size, Image.BICUBIC); B = B.resize(size, Image.BICUBIC)
def edges(im):
    g = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(2)), float)
    gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1])); gy = np.abs(np.diff(g, axis=0, prepend=g[:1]))
    e = np.hypot(gx, gy); return e / (np.percentile(e, 99) + 1e-6)
ea, eb = edges(A), edges(B)
base = np.asarray(A.convert('L'), float) * 0.5
ov = np.stack([base + 255 * np.clip(ea, 0, 1) * 0.8, base + 200 * np.clip(eb, 0, 1), base + 255 * np.clip(eb, 0, 1)], -1)
o = Image.new('RGB', (size[0] * 3, size[1]))
o.paste(A, (0, 0)); o.paste(B, (size[0], 0)); o.paste(Image.fromarray(np.clip(ov, 0, 255).astype(np.uint8)), (2 * size[0], 0))
o.save(a[1])
