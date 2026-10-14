"""Side-by-side (stacked) reference | render crops in reference pixel coords, with pixel rulers.
   python3 dish_cmp.py r_ref.png out.png x0,y0,x1,y1 [--scale S] [--stack]"""
import sys
from PIL import Image, ImageDraw
a = sys.argv[1:]
src, out = a[0], a[1]
box = tuple(int(v) for v in a[2].split(','))
sc = float(a[a.index('--scale') + 1]) if '--scale' in a else None
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
r = Image.open(src).convert('RGB').resize(ref.size, Image.LANCZOS)
A = ref.crop(box); B = r.crop(box)
if '--gray' in a:
    from PIL import ImageOps, ImageEnhance
    A = ImageEnhance.Contrast(ImageOps.autocontrast(A.convert('L'), cutoff=1)).enhance(1.4).convert('RGB')
    B = ImageEnhance.Contrast(ImageOps.autocontrast(B.convert('L'), cutoff=1)).enhance(1.4).convert('RGB')
w, h = A.size
if sc is None:
    sc = min(2.5, 1800.0 / w, 1000.0 / h)
A = A.resize((int(w * sc), int(h * sc)), Image.LANCZOS); B = B.resize(A.size, Image.LANCZOS)
st = 20 if (box[2] - box[0]) < 500 else 50
for im in (A, B):
    d = ImageDraw.Draw(im)
    for x in range((box[0] // st + 1) * st, box[2], st):
        xx = (x - box[0]) * sc; d.line((xx, 0, xx, 8), fill=(0, 0, 255)); d.text((xx + 2, 8), str(x), fill=(0, 0, 255))
    for y in range((box[1] // st + 1) * st, box[3], st):
        yy = (y - box[1]) * sc; d.line((0, yy, 8, yy), fill=(0, 0, 255)); d.text((10, yy - 5), str(y), fill=(0, 0, 255))
        d.line((im.width - 8, yy, im.width, yy), fill=(0, 0, 255))
if '--stack' in a:
    o = Image.new('RGB', (A.width, A.height * 2 + 4), 'white'); o.paste(A, (0, 0)); o.paste(B, (0, A.height + 4))
else:
    o = Image.new('RGB', (A.width * 2 + 4, A.height), 'white'); o.paste(A, (0, 0)); o.paste(B, (A.width + 4, 0))
o.save(out)
print(out, o.size)
