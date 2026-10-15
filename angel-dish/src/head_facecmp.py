"""side-by-side photo | render (refzoom) of a ref-pixel box with a pixel grid. python3 head_facecmp.py TAG [box] [out]"""
import sys
from PIL import Image, ImageDraw
REF = '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
tag = sys.argv[1]
b = tuple(int(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '410,150,510,280').split(','))
out = sys.argv[3] if len(sys.argv) > 3 else 'out/%s/face_cmp.png' % tag
s = 7
A = Image.open(REF).convert('RGB').crop(b).resize(((b[2] - b[0]) * s, (b[3] - b[1]) * s), Image.BICUBIC)
R = Image.open('out/%s/h_refzoom.png' % tag).convert('RGB')
pb = (320, 100); sc = R.width / 220.0
B = R.crop((int((b[0] - pb[0]) * sc), int((b[1] - pb[1]) * sc), int((b[2] - pb[0]) * sc), int((b[3] - pb[1]) * sc))).resize(A.size, Image.LANCZOS)
o = Image.new('RGB', (A.width * 2, A.height)); o.paste(A, (0, 0)); o.paste(B, (A.width, 0))
d = ImageDraw.Draw(o)
for y in range(b[1], b[3], 10):
    Y = (y - b[1]) * s; d.line([(0, Y), (o.width, Y)], fill=(0, 255, 0)); d.text((2, Y + 2), str(y), fill=(0, 255, 0))
for x in range(b[0], b[2], 10):
    X = (x - b[0]) * s
    for off in (0, A.width):
        d.line([(X + off, 0), (X + off, 10)], fill=(0, 255, 0)); d.text((X + off + 2, 12), str(x), fill=(0, 255, 0))
o.save(out)
