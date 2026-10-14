"""python3 head_rayv.py mesh.ply view u,v ... : raycast pixels of a head_render orbit view (front,q3,profile,back,q3back,...)."""
import sys, math, numpy as np, trimesh
import head
from head import POSE
from head_hair import CAP_C, CAP_R
m = trimesh.load(sys.argv[1], process=False); view = sys.argv[2]
V = np.asarray(m.vertices); Fc = np.asarray(m.faces)
A0 = V[Fc[:, 0]]; E1 = V[Fc[:, 1]] - A0; E2 = V[Fc[:, 2]] - A0
def mt(o, d):
    pv = np.cross(d, E2); det = np.einsum('ij,ij->i', E1, pv); ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0); tv = o - A0; uu = np.einsum('ij,ij->i', tv, pv) * inv
    qv = np.cross(tv, E1); vv = (qv @ d) * inv; t = np.einsum('ij,ij->i', E2, qv) * inv
    hit = ok & (uu >= 0) & (vv >= 0) & (uu + vv <= 1) & (t > 0)
    return t[hit].min() if hit.any() else None
ang = {'front': (0, 0), 'q3': (35, 5), 'profile': (85, 0), 'q3R': (-40, 5), 'back': (180, 10), 'q3back': (140, 10), 'top': (0, 70)}[view]
yaw, elv = (math.radians(x) for x in ang)
dl = np.array([math.sin(yaw) * math.cos(elv), math.cos(yaw) * math.cos(elv), math.sin(elv)])
tgt = POSE.P((0, 2.0, -2.5)) if view not in ('back', 'q3back') else POSE.P((0, -2.0, -6.0))
dist = 52 if view not in ('back', 'q3back') else 140; lens = 105 if view not in ('back', 'q3back') else 80
loc = tgt + dist * POSE.D(dl)
fwd = tgt - loc; fwd /= np.linalg.norm(fwd)
# blender track_quat('-Z','Y'): camera up is world-Z-ish projected
right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
res = int(sys.argv[3]) if sys.argv[3].isdigit() else 700
f = lens / 36.0 * res
for a in sys.argv[4 if sys.argv[3].isdigit() else 3:]:
    u, v = (float(t) for t in a.split(','))
    d = fwd + (u - res / 2) / f * right - (v - res / 2) / f * up; d /= np.linalg.norm(d)
    t = mt(loc, d)
    if t is None:
        print(a, 'miss'); continue
    p = loc + t * d; l = POSE.to_local(p)
    print(a, 'world', p.round(2), 'local', l.round(2))
