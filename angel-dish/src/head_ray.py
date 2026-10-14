"""python3 head_ray.py mesh.ply u,v [u,v ...]  : ray-cast reference pixels onto a mesh; print world, head-local
coordinates and cap angles (phi, theta) of the hit (head agent tool)."""
import sys, math
import numpy as np
import trimesh
import cam, head
from head_hair import CAP_C, CAP_R

m = trimesh.load(sys.argv[1], process=False)
V = np.asarray(m.vertices); Fc = np.asarray(m.faces)
A0 = V[Fc[:, 0]]; E1 = V[Fc[:, 1]] - A0; E2 = V[Fc[:, 2]] - A0


def mt(o, d):
    pv = np.cross(d, E2); det = np.einsum('ij,ij->i', E1, pv)
    ok = np.abs(det) > 1e-12
    inv = np.where(ok, 1.0 / np.where(ok, det, 1), 0)
    tv = o - A0; uu = np.einsum('ij,ij->i', tv, pv) * inv
    qv = np.cross(tv, E1); vv = (qv @ d) * inv
    t = np.einsum('ij,ij->i', E2, qv) * inv
    hit = ok & (uu >= 0) & (vv >= 0) & (uu + vv <= 1) & (t > 0)
    return t[hit].min() if hit.any() else None
loc, fwd, right, up = cam.frame()
c = cam.load(); W = c['w']; H = c['h']; f = c['lens'] / 36.0 * W
for a in sys.argv[2:]:
    u, v = (float(t) for t in a.split(','))
    dx = (u - W / 2 - c.get('shift_x', 0) * W) / f; dy = -(v - H / 2 + c.get('shift_y', 0) * W) / f
    d = fwd + dx * right + dy * up; d /= np.linalg.norm(d)
    t = mt(loc, d)
    if t is None:
        print(a, 'miss'); continue
    p = loc + t * d
    l = head.POSE.to_local(p)
    q = (l - CAP_C) / CAP_R
    rn = np.linalg.norm(q)
    phi = math.degrees(math.atan2(q[0], q[1])); th = math.degrees(math.asin(np.clip(q[2] / rn, -1, 1)))
    print(a, 'world', p.round(2), 'local', l.round(2), 'cap phi %.0f th %.0f rn %.2f' % (phi, th, rn))
