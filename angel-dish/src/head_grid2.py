"""python3 head_grid2.py TAG x0,y0,x1,y1 out.png [z]  photo | render(refzoom) with 10px grid lines and lm ticks"""
import sys
from PIL import Image, ImageDraw
REF = '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
tag = sys.argv[1]; b = tuple(int(v) for v in sys.argv[2].split(',')); out = sys.argv[3]; z = float(sys.argv[4]) if len(sys.argv) > 4 else 4
A = Image.open(REF).convert('RGB').crop(b).resize((int((b[2] - b[0]) * z), int((b[3] - b[1]) * z)), Image.BICUBIC)
R = Image.open('out/%s/h_refzoom.png' % tag).convert('RGB'); sc = R.width / 220.0
B = R.crop((int((b[0] - 320) * sc), int((b[1] - 100) * sc), int((b[2] - 320) * sc), int((b[3] - 100) * sc))).resize(A.size, Image.LANCZOS)
o = Image.new('RGB', (A.width * 2 + 6, A.height), (0, 0, 0)); o.paste(A, (0, 0)); o.paste(B, (A.width + 6, 0))
d = ImageDraw.Draw(o)
for off in (0, A.width + 6):
    for y in range(b[1] - b[1] % 10 + 10, b[3], 10):
        yy = (y - b[1]) * z
        d.line([(off, yy), (off + 12, yy)], fill=(0, 255, 0)); d.text((off + 14, yy - 6), str(y), fill=(0, 255, 0))
    for x in range(b[0] - b[0] % 10 + 10, b[2], 10):
        xx = off + (x - b[0]) * z
        d.line([(xx, 0), (xx, 10)], fill=(0, 255, 0)); d.text((xx - 8, 12), str(x), fill=(0, 255, 0))
o.save(out)
