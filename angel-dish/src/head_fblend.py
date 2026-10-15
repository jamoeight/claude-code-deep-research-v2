"""python3 head_fblend.py render_refzoom.png out.png [x0,y0,x1,y1] [zbox 320,100,540,380] [zscale 4] : ref | render | blend (face)"""
import sys
from PIL import Image, ImageDraw
r = Image.open(sys.argv[1]).convert('RGB'); out = sys.argv[2]
x0, y0, x1, y1 = (int(v) for v in (sys.argv[3] if len(sys.argv) > 3 else '420,170,510,270').split(','))
zb = [int(v) for v in (sys.argv[4] if len(sys.argv) > 4 else '320,100,540,380').split(',')]
zs = float(sys.argv[5]) if len(sys.argv) > 5 else 4
z = 6
fc = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/crop_face.png').convert('RGB')
A = fc.crop((int((x0 - 330) * 5), int((y0 - 110) * 5), int((x1 - 330) * 5), int((y1 - 110) * 5))).resize(((x1 - x0) * z, (y1 - y0) * z), Image.BICUBIC)
B = r.crop((int((x0 - zb[0]) * zs), int((y0 - zb[1]) * zs), int((x1 - zb[0]) * zs), int((y1 - zb[1]) * zs))).resize(A.size, Image.LANCZOS)
C = Image.blend(A, B, 0.5)
o = Image.new('RGB', (A.width * 3, A.height))
for i, im in enumerate((A, B, C)):
    d = ImageDraw.Draw(im)
    for x in range((x0 // 10 + 1) * 10, x1, 10):
        X = (x - x0) * z; d.line((X, 0, X, 8), fill=(0, 255, 255), width=2); d.text((X + 2, 10), str(x), fill=(255, 255, 0))
    for y in range((y0 // 10 + 1) * 10, y1, 10):
        Y = (y - y0) * z; d.line((0, Y, 8, Y), fill=(0, 255, 255), width=2); d.text((10, Y + 2), str(y), fill=(255, 255, 0))
    o.paste(im, (i * A.width, 0))
o.save(out)
