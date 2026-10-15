"""ref px -> 3D hit point on a mesh (nearest triangle under the pixel): python3 figure_hit.py mesh.ply u,v [u,v ...]"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trimesh
import figure_tex as T
m = trimesh.load(sys.argv[1], process=False)
rc = T.ref_camera()
V = np.asarray(m.vertices); Fc = np.asarray(m.faces)
uvV = T.project(rc, V); dep = (V - rc['loc']) @ rc['fwd']
A, B, C = uvV[Fc[:, 0]], uvV[Fc[:, 1]], uvV[Fc[:, 2]]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
for a in sys.argv[2:]:
    p = np.array(list(map(float, a.split(','))))
    c = np.nonzero((lo[:, 0] <= p[0]) & (hi[:, 0] >= p[0]) & (lo[:, 1] <= p[1]) & (hi[:, 1] >= p[1]))[0]
    a_, b_, c_ = A[c], B[c], C[c]
    v0 = b_ - a_; v1 = c_ - a_; v2 = p - a_
    den = v0[:, 0] * v1[:, 1] - v1[:, 0] * v0[:, 1]
    s = (v2[:, 0] * v1[:, 1] - v1[:, 0] * v2[:, 1]) / den; t = (v0[:, 0] * v2[:, 1] - v2[:, 0] * v0[:, 1]) / den
    ok = (s >= 0) & (t >= 0) & (s + t <= 1)
    if not ok.any():
        print(a, '-> None'); continue
    c = c[ok]; s = s[ok]; t = t[ok]
    P = V[Fc[c, 0]] * (1 - s - t)[:, None] + V[Fc[c, 1]] * s[:, None] + V[Fc[c, 2]] * t[:, None]
    d = (P - rc['loc']) @ rc['fwd']
    print(a, '->', np.round(P[np.argmin(d)], 2))
