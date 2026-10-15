"""python3 head_pair.py render_refzoom.png out.png x0,y0,x1,y1 [z]  (refzoom box 320,100,540,380 scale 4)"""
import sys
from PIL import Image
ref = Image.open('/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png').convert('RGB')
r = Image.open(sys.argv[1]).convert('RGB')
x0, y0, x1, y1 = (int(v) for v in sys.argv[3].split(',')); z = float(sys.argv[4]) if len(sys.argv) > 4 else 4
A = ref.crop((x0, y0, x1, y1)).resize((int((x1 - x0) * z), int((y1 - y0) * z)), Image.BICUBIC)
B = r.crop(((x0 - 320) * 4, (y0 - 100) * 4, (x1 - 320) * 4, (y1 - 100) * 4)).resize(A.size, Image.LANCZOS)
o = Image.new('RGB', (A.width * 2, A.height)); o.paste(A, (0, 0)); o.paste(B, (A.width, 0)); o.save(sys.argv[2])
