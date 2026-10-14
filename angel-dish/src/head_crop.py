"""python3 head_crop.py TAG x0,y0,x1,y1 out.png : ref | render | blend crops (ref px box) from out/TAG/hz.png (pbox 320,100,540,380)."""
import sys
from PIL import Image
tag, box, out = sys.argv[1], [int(v) for v in sys.argv[2].split(',')], sys.argv[3]
pb = [int(v) for v in (sys.argv[4] if len(sys.argv) > 4 else '320,100,540,380').split(',')]
im = Image.open(f'out/{tag}/hz.png'); w = im.width // 3; s = 900 / (pb[3] - pb[1])
a = im.crop((0, 0, w, 900)); b = im.crop((w, 0, 2 * w, 900))
bx = tuple(int(v) for v in ((box[0] - pb[0]) * s, (box[1] - pb[1]) * s, (box[2] - pb[0]) * s, (box[3] - pb[1]) * s))
pw = bx[2] - bx[0]
o = Image.new('RGB', (pw * 3, bx[3] - bx[1]))
for i, x in enumerate([a, b, Image.blend(a, b, 0.5)]):
    o.paste(x.crop(bx), (i * pw, 0))
k = min(2.0, 2400 / o.width)
o.resize((int(o.width * k), int(o.height * k))).save(out)
