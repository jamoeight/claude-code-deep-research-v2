"""Head: serene classical female face (downcast eyes), long wavy combed hair.
Built in a head-local frame (x = her left, y = face forward, z = up, origin = skull centre at eye level),
see head_pose.py.  Hair locks use the grooved-lock kernel in head_k.py."""
import math, os
import numpy as np
from sdf import Batch, catmull, resample
from head_pose import Pose
from head_k import add_lock, subfield, paste

POSE = Pose(O=(-16.76, 18.27, 88.57), turn=39.0, pitch=16.0, roll=1.0)   # bowed toward her left, downcast
P, D = POSE.P, POSE.D
NECK_BOTTOM = np.array([-18.6, 21.5, 77.5])


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
    base.E((0, 2.0, -3.85), (3.6, 3.55, 3.2), xa=(1, 0, 0), ya=(0, 1, 0.25), k=2.6)   # lower face / jaw (narrow, tapering)
    base.E((0, 4.3, -6.0), (1.85, 1.55, 1.25), k=1.6)                 # chin (small, round)
    base.E((0, 0.6, -5.3), (2.7, 3.4, 2.2), k=1.8)                   # jaw floor
    for s in (-1, 1):
        base.E((3.0 * s, 3.3, -1.3), (1.55, 1.3, 1.15), xa=(1, 0.3 * s, 0), k=1.4)    # cheekbones
        base.E((2.5 * s, 3.45, -2.85), (1.9, 1.5, 1.85), k=1.6)       # cheek fullness
        base.E((2.0 * s, 4.5, 1.15), (1.95, 0.95, 0.68), xa=(1, -0.25 * s, 0), ya=(0, 1, 0), k=1.0)  # brow arcs (overhang: socket shadow)
    base.E((0, 4.5, 0.85), (0.9, 0.9, 0.75), k=0.7)                  # glabella
    base.E((0, 3.8, -4.6), (1.7, 1.6, 1.2), k=1.3)                   # muzzle (soft, set back)
    # ---------------- carve (shallow sockets)
    for s in (-1, 1):
        sub1.E((2.15 * s, 5.52, 0.08), (1.34, 0.82, 0.74), k=0.75)
    sub1.E((0, 5.7, -5.6), (0.85, 0.3, 0.18), k=0.6)                  # mentolabial sulcus (shallow)
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
    feat.E((0, 5.3, -3.85), (0.9, 0.6, 0.55), k=0.6)                 # philtrum region
    for s in (-1, 1):
        feat.E((0.42 * s, 5.6, -4.22), (0.6, 0.36, 0.25), xa=(1, -0.3 * s, -0.1 * s), k=0.3)  # upper lip halves (small, relaxed)
    feat.E((0, 5.38, -4.74), (0.74, 0.37, 0.27), k=0.5)                # lower lip (relaxed)
    # ---------------- fine carve: closed mouth line with slightly raised corners
    sub2.T([(-0.8, 5.5, -4.38), (-0.45, 5.83, -4.46), (0, 5.93, -4.46), (0.45, 5.83, -4.46), (0.8, 5.5, -4.38)], 0.045, k=0.05, n=14)
    return base.b, sub1.b, feat.b, sub2.b


def neck():
    B = Batch()
    B.rcone(P((0, -0.6, -5.2)), NECK_BOTTOM, 2.25, 2.15, k=1.6)
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
        if os.environ.get('HEAD_NOCLOSE') != '1':
            _close_pockets(S, head_hair.LAST_BODY)
            # behind the neck / right shoulder: channels between the back curtains and the flare (seen from behind)
            _close_pockets(S, head_hair.LAST_BODY, r=2.3, keep=0.7, box=((-37.0, 21.0, 66.0), (-12.0, 34.0, 86.0)), front_keep=None)
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


CLOSE_BOX = ((-37.5, 11.0, 63.0), (-6.0, 32.0, 89.0))


def _close_pockets(S, body, r=1.6, keep=0.6, box=None, front_keep=1.15):
    """Morphological close of (head + body proxy) around the neck / shoulders: slots and pockets between the hair
    locks and the neck/shoulders narrower than ~2r become solid up to `keep` below the bridged surface, so they read
    as shallow creases instead of dark holes (and trap no resin).  Shallow strand grooves are left untouched."""
    from scipy import ndimage
    from scipy.ndimage import map_coordinates
    if body is None:
        return
    box = box or CLOSE_BOX
    lo = np.asarray(box[0]); hi = np.asarray(box[1])
    a = np.clip(np.floor((lo - S.lo) / S.h).astype(int), 0, np.array(S.shape) - 1)
    b = np.clip(np.ceil((hi - S.lo) / S.h).astype(int) + 1, 1, S.shape)
    if np.any(b - a < 4):
        return
    G = S.G[a[0]:b[0], a[1]:b[1], a[2]:b[2]]
    h = S.h
    idx = [S.lo[i] + (a[i] + np.arange(b[i] - a[i])) * h for i in range(3)]
    X, Y, Z = np.meshgrid(*idx, indexing='ij')
    q = np.stack([(X - body.F.lo[0]) / body.F.h, (Y - body.F.lo[1]) / body.F.h, (Z - body.F.lo[2]) / body.F.h])
    bd = map_coordinates(body.F.G, q.reshape(3, -1), order=1, mode='nearest').reshape(X.shape)
    solid = (G < 0) | (bd < 0.1)
    pw = int(np.ceil(r / h)) + 2
    sp = np.pad(solid, pw, mode='edge')
    dil = ndimage.distance_transform_edt(~sp) * h <= r
    dil = np.pad(dil[1:-1, 1:-1, 1:-1], 1, constant_values=False)      # the box faces erode (no slabs at the faces)
    clo = (ndimage.distance_transform_edt(dil) * h > r)[pw:-pw, pw:-pw, pw:-pw]
    clo |= solid
    depth = ndimage.distance_transform_edt(np.pad(clo, 1, constant_values=False))[1:-1, 1:-1, 1:-1] * h
    if front_keep is not None:
        # in front (visible from the ref camera) the fill stays deeper: a shadowed crease beside the neck, not a lit web
        keep = keep + (front_keep - keep) * np.clip((22.5 - Y) / 2.0, 0.0, 1.0)
    acc = clo & ~solid & (depth > keep)
    if not acc.any():
        return
    # smooth signed distance of the closed shape, offset inward by `keep`
    sd = ndimage.distance_transform_edt(~clo) * h - depth
    sd = ndimage.gaussian_filter(sd, max(0.8, 0.32 / h)) + keep          # smooth (no voxel staircase / torn bits)
    # restrict the fill to the neighbourhood of the accepted pockets with a continuous field (no hard cut at a mask edge)
    dacc = ndimage.distance_transform_edt(~acc) * h
    fill = np.maximum(sd, ndimage.gaussian_filter(dacc, max(0.8, 0.32 / h)) - 3.0 * h)
    m = fill < 0.6
    a_ = G[m]; b_ = fill[m].astype(np.float32); kk = 0.3
    hh = np.clip(kk - np.abs(a_ - b_), 0, None) / kk
    G[m] = np.minimum(a_, b_) - hh * hh * kk * 0.25
    print('head: closed %d pocket voxels' % int(acc.sum()))
    if os.environ.get('HEAD_DBGCLOSE') == '1':
        lab, n = ndimage.label(acc)
        cnt = np.bincount(lab.ravel()); cnt[0] = 0
        for i in np.argsort(-cnt)[:25]:
            if cnt[i] == 0:
                break
            c = np.argwhere(lab == i).mean(0)
            print('   pocket %5d vox at' % cnt[i], np.round(S.lo + (a + c) * h, 1))
