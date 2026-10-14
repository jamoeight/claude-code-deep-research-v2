"""python3 head_zoomblend.py TAG [x0,y0,x1,y1] : ref crop | out/TAG/h_refzoom.png | edge overlay -> out/TAG/hb_zoom.png"""
import sys
import numpy as np
from PIL import Image, ImageFilter
tag = sys.argv[1]
box = tuple(int(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '380,110,530,300').split(','))
ref = Image.open('../ref/reference.png').convert('RGB').crop(box)
r = Image.open(f'out/{tag}/h_refzoom.png').convert('RGB')
s = 900 / ref.height; size = (int(ref.width * s), 900)
A = ref.resize(size, Image.BICUBIC); B = r.resize(size, Image.LANCZOS)
def edges(im):
    g = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(2)), float)
    gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1])); gy = np.abs(np.diff(g, axis=0, prepend=g[:1]))
    e = np.hypot(gx, gy); return e / (np.percentile(e, 99) + 1e-6)
ea, eb = edges(A), edges(B); base = np.asarray(A.convert('L'), float) * 0.5
ov = np.stack([base + 255 * np.clip(ea, 0, 1) * 0.8, base + 200 * np.clip(eb, 0, 1), base + 255 * np.clip(eb, 0, 1)], -1)
o = Image.new('RGB', (size[0] * 3, 900)); o.paste(A, (0, 0)); o.paste(B, (size[0], 0))
o.paste(Image.fromarray(np.clip(ov, 0, 255).astype(np.uint8)), (2 * size[0], 0))
o.save(f'out/{tag}/hb_zoom.png')
