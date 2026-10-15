"""orbit-view px -> 3D hit on a mesh: python3 figure_hito.py mesh.ply VIEW W H u,v [u,v ...]  (figure_render ORB views)"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import trimesh
import figure_tex as T
ORB = {'fFront': (0, 12), 'fBack': (180, 18), 'fLeft': (-90, 12), 'fRight': (90, 14), 'fTQL': (-40, 20), 'fTQR': (40, 20),
       'fBackL': (-140, 20), 'fBackR': (140, 20), 'fTop': (0, 70), 'fLow': (10, 3)}
m = trimesh.load(sys.argv[1], process=False)
az, el = ORB[sys.argv[2]]; W, H = int(sys.argv[3]), int(sys.argv[4])
c = T.orbit_camera((-14.0, 18.0, 50.0), az, el, 175.0, lens=75.0, W=W, H=H)
V = np.asarray(m.vertices); Fc = np.asarray(m.faces)
uvV = T.project(c, V)
A, B, C = uvV[Fc[:, 0]], uvV[Fc[:, 1]], uvV[Fc[:, 2]]
lo = np.minimum(np.minimum(A, B), C); hi = np.maximum(np.maximum(A, B), C)
for a in sys.argv[5:]:
    p = np.array(list(map(float, a.split(','))))
    cc = np.nonzero((lo[:, 0] <= p[0]) & (hi[:, 0] >= p[0]) & (lo[:, 1] <= p[1]) & (hi[:, 1] >= p[1]))[0]
    a_, b_, c_ = A[cc], B[cc], C[cc]
    v0 = b_ - a_; v1 = c_ - a_; v2 = p - a_
    den = v0[:, 0] * v1[:, 1] - v1[:, 0] * v0[:, 1]
    s = (v2[:, 0] * v1[:, 1] - v1[:, 0] * v2[:, 1]) / den; t = (v0[:, 0] * v2[:, 1] - v2[:, 0] * v0[:, 1]) / den
    ok = (s >= 0) & (t >= 0) & (s + t <= 1)
    if not ok.any():
        print(a, '-> None'); continue
    cc = cc[ok]; s = s[ok]; t = t[ok]
    P = V[Fc[cc, 0]] * (1 - s - t)[:, None] + V[Fc[cc, 1]] * s[:, None] + V[Fc[cc, 2]] * t[:, None]
    d = (P - c['loc']) @ c['fwd']
    print(a, '->', np.round(P[np.argmin(d)], 2))
