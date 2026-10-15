"""python3 head_depth.py u,v ... : along the ref-camera ray of each pixel, body(+face) distance vs world y."""
import sys, os, numpy as np
os.environ['HEAD_NOHAIR'] = '1'
from sdf import Field
import head, cam
from head_drape import Body
from head_hair import _with_face
F = Field((-45, -5, 50), (15, 50, 108), 0.3)
S, a = head.subfield(F, (-45, -5, 50), (15, 50, 108))
head.build_face(S)
b = _with_face(Body(), S)
for arg in sys.argv[1:]:
    u, v = (float(x) for x in arg.split(','))
    out = []
    for y in np.arange(14, 32, 1.0):
        p = cam.unproject((u, v), plane_y=y)
        out.append('%d:%.1f' % (y, b.d(p)[0]))
    print(arg, ' '.join(out))
