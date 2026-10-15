"""python3 head_bodyray.py u,v ... : first body-proxy hit (off 0) for ref pixels (and plane y=22 point if none)."""
import sys, numpy as np
from head_drape import Body
import cam
b = Body()
for a in sys.argv[1:]:
    u, v = (float(x) for x in a.split(','))
    p, hit = b.raycast((u, v), 0.0, 22.0)
    print(a, 'HIT' if hit else 'miss', np.round(p, 1), 'n=', np.round(b.grad(p)[0], 2))
