"""Head: serene classical female face (downcast eyes), long wavy combed hair.
Built in a head-local frame (x = her left, y = face forward, z = up, origin = skull centre at eye level),
see head_pose.py.  Hair locks use the grooved-lock kernel in head_k.py."""
import math, os
import numpy as np
from sdf import Batch, catmull, resample
from head_pose import Pose
from head_k import add_lock, subfield, paste

POSE = Pose(O=(-16.4, 19.0, 88.3), turn=34.0, pitch=8.0, roll=5.0)
P, D = POSE.P, POSE.D
NECK_BOTTOM = np.array([-19.0, 21.2, 75.5])


# ------------------------------------------------------------------ local helpers
class LB:
    """Batch wrapper taking head-local coordinates."""

    def __init__(self):
        self.b = Batch()

    def E(self, c, r, xa=(1, 0, 0), ya=(0, 1, 0), k=0.0):
        self.b.ellipsoid(P(c), r, xaxis=D(xa), yaxis=D(ya), k=k)

    def S(self, c, r, k=0.0):
        self.b.sphere(P(c), r, k=k)

    def C(self, a, b, ra, rb=None, k=0.0):
        self.b.rcone(P(a), P(b), ra, ra if rb is None else rb, k=k)

    def T(self, pts, radii, k=0.0, n=None):
        pts = np.asarray(pts, float)
        if n:
            pts = resample(catmull(pts, per=8), n)
        self.b.tube(np.array([P(p) for p in pts]), radii, k=k)

    def mirror(self, fn):
        for s in (-1, 1):
            fn(s)


def face_parts():
    base, sub1, feat, sub2 = LB(), LB(), LB(), LB()
    # ---------------- skull & face masses (soft, youthful oval; classical proportions)
    base.E((0, -1.4, 1.6), (5.0, 6.6, 6.4))                          # cranium
    base.E((0, 1.9, 2.7), (4.05, 3.6, 3.25), k=1.5)                   # forehead
    base.E((0, 1.5, 0.2), (4.5, 4.1, 4.3), k=1.5)                    # upper face
    base.E((0, 2.0, -3.85), (4.0, 3.6, 3.2), xa=(1, 0, 0), ya=(0, 1, 0.25), k=2.6)   # lower face / jaw (rounded)
    base.E((0, 4.6, -6.4), (1.8, 1.6, 1.3), k=1.4)                  # chin (small, round)
    base.E((0, 0.6, -5.4), (3.1, 3.4, 2.2), k=1.6)                   # jaw floor
    for s in (-1, 1):
        base.E((3.0 * s, 3.3, -1.3), (1.55, 1.3, 1.15), xa=(1, 0.3 * s, 0), k=1.4)    # cheekbones
        base.E((2.5 * s, 3.45, -2.85), (1.9, 1.5, 1.85), k=1.6)       # cheek fullness
        base.E((2.0 * s, 4.6, 1.15), (1.95, 0.95, 0.65), xa=(1, -0.25 * s, 0), ya=(0, 1, 0), k=0.9)  # brow arcs (overhang: socket shadow)
    base.E((0, 4.5, 0.85), (0.9, 0.9, 0.75), k=0.7)                  # glabella
    base.E((0, 4.3, -4.6), (1.9, 1.9, 1.4), k=1.3)                   # muzzle (round, under lips)
    # ---------------- carve (shallow sockets)
    for s in (-1, 1):
        sub1.E((2.15 * s, 5.3, 0.05), (1.38, 0.95, 0.8), k=0.7)
    sub1.E((0, 6.15, -5.8), (1.05, 0.45, 0.28), k=0.5)                # mentolabial sulcus
    # ---------------- features
    for s in (-1, 1):
        feat.S((2.15 * s, 3.45, -0.1), 1.15, k=0.3)                  # eyeball
        feat.E((2.15 * s, 3.62, 0.0), (1.35, 1.2, 1.0), k=0.45)       # upper lid (closed, downcast)
        feat.E((2.15 * s, 3.95, -0.85), (1.15, 0.7, 0.32), k=0.4)    # lower lid
    feat.C((0, 5.4, 0.35), (0, 6.6, -2.3), 0.5, 0.55, k=0.6)         # nose bridge (straight Greek line)
    feat.E((0, 5.55, -1.6), (0.85, 0.95, 1.35), k=0.6)               # nose sides
    feat.S((0, 6.38, -2.5), 0.54, k=0.45)                            # tip (short, soft)
    for s in (-1, 1):
        feat.S((0.6 * s, 5.6, -2.92), 0.41, k=0.45)                  # alae
    feat.E((0, 5.95, -3.15), (0.4, 0.55, 0.3), k=0.3)                # columella
    feat.E((0, 5.6, -3.9), (1.0, 0.65, 0.6), k=0.6)                  # philtrum region
    for s in (-1, 1):
        feat.E((0.55 * s, 5.92, -4.42), (0.76, 0.52, 0.33), xa=(1, -0.3 * s, -0.1 * s), k=0.3)  # upper lip halves
    feat.E((0, 5.82, -5.05), (0.92, 0.6, 0.4), k=0.35)               # lower lip
    # ---------------- fine carve: closed mouth line with slightly raised corners
    sub2.T([(-1.05, 5.55, -4.62), (-0.55, 6.36, -4.78), (0, 6.6, -4.76), (0.55, 6.36, -4.78), (1.05, 5.55, -4.62)], 0.085, k=0.06, n=14)
    for s in (-1, 1):
        sub2.S((1.1 * s, 5.35, -4.62), 0.16, k=0.3)                  # mouth corners
    return base.b, sub1.b, feat.b, sub2.b


def neck():
    B = Batch()
    B.rcone(P((0, -0.6, -5.2)), NECK_BOTTOM, 2.25, 2.5, k=1.0)
    return B


def build_face(S):
    base, sub1, feat, sub2 = face_parts()
    S.apply(base)
    S.apply(neck())
    S.apply(sub1, 'sub')
    S.apply(feat)
    S.apply(sub2, 'sub')
    return S


def component(F):
    S, a = subfield(F, (-45, -5, 50), (15, 50, 108))
    build_face(S)
    if os.environ.get('HEAD_NOHAIR') != '1':
        import head_hair
        head_hair.build_hair(S)
    _fill_voids(S)
    paste(F, S, a)
    return F


def _fill_voids(S):
    """Fill air pockets fully enclosed by the head/hair solid, or by hair lying on the figure (body proxy),
    so the final union has no internal voids (printability)."""
    from scipy import ndimage
    air = S.G >= 0
    try:
        import head_hair
        body = head_hair.LAST_BODY
    except Exception:
        body = None
    if body is not None:
        from scipy.ndimage import map_coordinates
        xs = S.lo[0] + np.arange(S.shape[0]) * S.h; ys = S.lo[1] + np.arange(S.shape[1]) * S.h
        X, Y = np.meshgrid(xs, ys, indexing='ij')
        for k in range(S.shape[2]):
            z = S.lo[2] + k * S.h
            idx = np.stack([(X - body.F.lo[0]) / body.F.h, (Y - body.F.lo[1]) / body.F.h, np.full_like(X, (z - body.F.lo[2]) / body.F.h)])
            bd = map_coordinates(body.F.G, idx.reshape(3, -1), order=1, mode='nearest').reshape(X.shape)
            air[:, :, k] &= bd >= 0.35      # coarse proxy: a small margin closes pockets under locks lying on the gown
    lab, n = ndimage.label(air)
    if n <= 1:
        return
    edge = np.unique(np.concatenate([lab[0].ravel(), lab[-1].ravel(), lab[:, 0].ravel(), lab[:, -1].ravel(),
                                     lab[:, :, 0].ravel(), lab[:, :, -1].ravel()]))
    inner = ~np.isin(lab, edge) & air & (S.G >= 0)
    S.G[inner] = -0.5 * S.h
