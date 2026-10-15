"""python3 head_sc.py TAG [x0,y0,x1,y1] [z]: photo | refzoom render for a refzoom rendered with --pbox = that box"""
import sys
from PIL import Image
REF = '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
tag = sys.argv[1]; b = tuple(int(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '325,185,465,345').split(','))
z = float(sys.argv[3]) if len(sys.argv) > 3 else 5
A = Image.open(REF).convert('RGB').crop(b).resize((int((b[2] - b[0]) * z), int((b[3] - b[1]) * z)), Image.BICUBIC)
B = Image.open('out/%s/h_refzoom.png' % tag).convert('RGB').resize(A.size, Image.LANCZOS)
o = Image.new('RGB', (A.width * 2 + 6, A.height)); o.paste(A, (0, 0)); o.paste(B, (A.width + 6, 0)); o.save('out/%s/sc.png' % tag)
