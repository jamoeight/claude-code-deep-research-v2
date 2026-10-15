"""Slice images of a field (integrator tool).
   python3 seams_slice.py field.npy out.png AXIS=VAL:u0,u1,v0,v1 [AXIS=VAL:...]   (AXIS x|y|z; u,v = the other two axes in order)"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw
p = sys.argv[1]
meta = json.load(open(os.path.join(os.path.dirname(p), 'raw.json')))
lo = np.array(meta['lo']); h = meta['h']
G = np.load(p, mmap_mode='r')
ims = []
S = 4
for spec in sys.argv[3:]:
    ax, rest = spec.split('=')
    val, box = rest.split(':')
    ai = 'xyz'.index(ax); val = float(val)
    u0, u1, v0, v1 = [float(t) for t in box.split(',')]
    oth = [i for i in range(3) if i != ai]
    k = int(round((val - lo[ai]) / h))
    sl = [slice(None)] * 3; sl[ai] = k
    A = np.asarray(G[tuple(sl)])
    a0 = int((u0 - lo[oth[0]]) / h); a1 = int((u1 - lo[oth[0]]) / h)
    b0 = int((v0 - lo[oth[1]]) / h); b1 = int((v1 - lo[oth[1]]) / h)
    A = A[a0:a1, b0:b1]
    img = np.zeros(A.shape + (3,), np.uint8)
    ins = A < 0
    img[ins] = (200, 120, 130)
    img[~ins] = (250, 250, 245)
    img[(A >= 0) & (A < 0.3)] = (170, 200, 255)
    im = Image.fromarray(np.transpose(img, (1, 0, 2))[::-1]).resize((A.shape[0] * S, A.shape[1] * S), Image.NEAREST)
    d = ImageDraw.Draw(im)
    for t in range(int(np.ceil(u0 / 5) * 5), int(u1) + 1, 5):
        px = (t - u0) / h * S; d.line((px, im.height - 6, px, im.height), fill=(0, 0, 0)); d.text((px + 1, im.height - 16), str(t), fill=(0, 0, 0))
    for t in range(int(np.ceil(v0 / 5) * 5), int(v1) + 1, 5):
        py = im.height - (t - v0) / h * S; d.line((0, py, 6, py), fill=(0, 0, 0)); d.text((8, py - 6), str(t), fill=(0, 0, 0))
    d.text((4, 4), f'{ax}={val}  ({"xyz"[oth[0]]} right, {"xyz"[oth[1]]} up)', fill=(0, 0, 0))
    ims.append(im)
W = sum(i.width for i in ims) + 6 * (len(ims) - 1); H = max(i.height for i in ims)
o = Image.new('RGB', (W, H), (90, 90, 90)); x = 0
for i in ims:
    o.paste(i, (x, 0)); x += i.width + 6
o.save(sys.argv[2]); print('saved', sys.argv[2], o.size)
