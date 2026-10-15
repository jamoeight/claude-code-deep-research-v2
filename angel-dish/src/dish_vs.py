"""Unrolled relief crop of the outer wall (shaded), fast.  python3 dish_vs.py out.png [s0 s1] [--fine]"""
import sys, subprocess
from PIL import Image
a = sys.argv[1:]
s0, s1 = (float(a[1]), float(a[2])) if len(a) > 2 and not a[1].startswith('--') else (-40.0, 90.0)
subprocess.run([sys.executable, 'dish_viz.py', a[0] + '.tmp.png', '--s0', str(s0), '--s1', str(s1)] + (['--fine'] if '--fine' in a else []), check=True, capture_output=True)
im = Image.open(a[0] + '.tmp.png'); w, h = im.size
im = im.crop((0, int(h * 0.12), w, h // 2))
sc = 1200.0 / w
im.resize((1200, int(im.size[1] * sc * 1.0))).save(a[0])
print(a[0])
