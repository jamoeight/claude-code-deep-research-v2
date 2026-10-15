"""Overlay the model's hem-roll crest lines (B red, A/R green) projected into the ref camera on the reference
photo and on a render.   python3 dish_crest.py render.png out.png [x0,y0,x1,y1]"""
import sys, math, numpy as np
from PIL import Image, ImageDraw
import cam, dish, dish_geo as G
LIPS, ZW = dish.lip_tables()
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
ren = Image.open(sys.argv[1]).convert('RGB').resize(ref.size)
box = tuple(int(v) for v in sys.argv[3].split(',')) if len(sys.argv) > 3 else (0, 0) + ref.size
th = np.linspace(0, 2 * math.pi, 181)
out = []
for im in (ref.copy(), ren):
    d = ImageDraw.Draw(im)
    for li, col in ((0, (255, 0, 0)), (1, (0, 200, 0))):
        T = LIPS[li]
        pts = []
        for n in range(0, G.NT, 5):
            if T[0, n] < 0.3:
                if len(pts) > 1:
                    d.line(pts, fill=col, width=2)
                pts = []
                continue
            ph = G.PH[n]; on, lrc, lzc, la, lb, tl = T[:6, n]
            u = la * np.cos(th) * math.cos(tl) - lb * np.sin(th) * math.sin(tl)
            v = la * np.cos(th) * math.sin(tl) + lb * np.sin(th) * math.cos(tl)
            k = np.argmax(v)
            rc = G.R0T[n] + G.FLT[n] + lrc
            x, y = G.xy(ph, rc + u[k]); z = lzc + v[k]
            pts.append(tuple(cam.project((float(x), float(y), float(z)))[0]))
        if len(pts) > 1:
            d.line(pts, fill=col, width=2)
    out.append(im.crop(box))
W, H = out[0].size
o = Image.new('RGB', (W, 2 * H + 4), 'white'); o.paste(out[0], (0, 0)); o.paste(out[1], (0, H + 4))
o.save(sys.argv[2]); print(sys.argv[2])
