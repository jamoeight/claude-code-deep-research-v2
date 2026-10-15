"""Contact sheet: python3 seams_sheet.py out.png cols cell_px img1[:label] img2 ...  (integrator tool)"""
import sys
from PIL import Image, ImageDraw
out, cols, cell = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
items = sys.argv[4:]
rows = (len(items) + cols - 1) // cols
o = Image.new('RGB', (cols * cell, rows * cell), (40, 40, 40))
d = ImageDraw.Draw(o)
for i, it in enumerate(items):
    p, _, lab = it.partition('::')
    im = Image.open(p).convert('RGB'); im.thumbnail((cell, cell))
    x, y = (i % cols) * cell, (i // cols) * cell
    o.paste(im, (x, y)); d.text((x + 4, y + 4), lab or p.rsplit('/', 1)[-1], fill=(255, 255, 0))
o.save(out); print('saved', out, o.size)
