"""ref px + target y -> 3D point on the camera ray: python3 figure_pxy.py u,v,y [u,v,y ...]"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import figure_tex as T
rc = T.ref_camera()
def ray(u, v):
    # numerically: find two points projecting to (u,v) via least squares on a generic ray
    from scipy.optimize import least_squares
    def f(p, y):
        q = np.array([[p[0], y, p[1]]]); return T.project(rc, q)[0] - np.array([u, v])
    return f
for a in sys.argv[1:]:
    u, v, y = map(float, a.split(','))
    from scipy.optimize import least_squares
    f = ray(u, v)
    r = least_squares(lambda p: f(p, y), [0.0, 20.0])
    print(a, '->', np.round([r.x[0], y, r.x[1]], 2))
