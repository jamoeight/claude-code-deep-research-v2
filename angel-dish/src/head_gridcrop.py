"""python3 head_gridcrop.py img out x0 y0 x1 y1 scale [step] [--ticks] - crop (ref px) with labelled grid (or border ticks)"""
import sys
from PIL import Image, ImageDraw
src, out = sys.argv[1], sys.argv[2]
x0, y0, x1, y1 = (int(v) for v in sys.argv[3:7]); s = float(sys.argv[7]); st = int(sys.argv[8]) if len(sys.argv) > 8 else 10
ticks = '--ticks' in sys.argv
im = Image.open(src).convert('RGB')
if im.size != (1179, 1078):
    im = im.resize((1179, 1078), Image.LANCZOS)
c = im.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * s), int((y1 - y0) * s)), Image.LANCZOS)
d = ImageDraw.Draw(c)
for x in range((x0 // st + 1) * st, x1, st):
    X = (x - x0) * s
    if ticks:
        d.line((X, 0, X, 12), fill=(0, 255, 255), width=2); d.line((X, c.height - 12, X, c.height), fill=(0, 255, 255), width=2)
        d.text((X + 2, 14), str(x), fill=(255, 255, 0))
    else:
        d.line((X, 0, X, c.height), fill=(0, 255, 255), width=1); d.text((X + 2, 2), str(x), fill=(255, 255, 0))
for y in range((y0 // st + 1) * st, y1, st):
    Y = (y - y0) * s
    if ticks:
        d.line((0, Y, 12, Y), fill=(0, 255, 255), width=2); d.line((c.width - 12, Y, c.width, Y), fill=(0, 255, 255), width=2)
        d.text((14, Y + 2), str(y), fill=(255, 255, 0))
    else:
        d.line((0, Y, c.width, Y), fill=(0, 255, 255), width=1); d.text((2, Y + 2), str(y), fill=(255, 255, 0))
c.save(out)
