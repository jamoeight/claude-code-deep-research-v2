"""Measure silhouette top / contour columns in a refzoom render vs the photo (head agent tool).
python3 head_meas.py h_refzoom.png [pbox] [scale]"""
import sys
import numpy as np
from PIL import Image
REF = '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
im = np.asarray(Image.open(sys.argv[1]).convert('RGB'), float)
pb = [int(v) for v in (sys.argv[2] if len(sys.argv) > 2 else '320,100,540,380').split(',')]
sc = float(sys.argv[3]) if len(sys.argv) > 3 else 4
bg = im[2, 2]
def top(x):
    col = im[:, int((x - pb[0]) * sc)]
    d = np.abs(col - col[5]).sum(1)
    i = np.argmax(d > 60)
    return pb[1] + i / sc
for x in (425, 430, 442, 455, 470, 485):
    print('render top at px x %d: %.1f' % (x, top(x)))
