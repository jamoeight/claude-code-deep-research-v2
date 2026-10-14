"""python3 head_cmp.py render_refzoom.png out.png --box x0,y0,x1,y1 : ref crop (upscaled) | render | blend"""
import sys, os
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
box = [int(v) for v in (a[a.index('--box') + 1] if '--box' in a else '360,110,540,300').split(',')]
r = Image.open(a[0]).convert('RGB')
ref = Image.open(os.path.join(HERE, '..', 'ref', 'reference.png')).convert('RGB').crop(box).resize(r.size, Image.BICUBIC)
H = 900; s = H / r.height
ref = ref.resize((int(r.width * s), H), Image.LANCZOS); r = r.resize(ref.size, Image.LANCZOS)
o = Image.new('RGB', (ref.width * 3, H))
o.paste(ref, (0, 0)); o.paste(r, (ref.width, 0)); o.paste(Image.blend(ref, r, 0.5), (2 * ref.width, 0))
o.save(a[1])
