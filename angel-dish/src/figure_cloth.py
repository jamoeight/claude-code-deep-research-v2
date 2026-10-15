"""The gown's bodice as a real cloth layer (helper for figure.py) -- round 3c3.

The torso base is skin.  Everything below the neckline is covered by a satin layer `T_CLOTH` thick: the field is
offset outward where the point is cloth, with a crisp step (~0.3 wide) at the fabric edge.  Skin = the region above
the V neckline and the armhole (a polygon traced on the photo, applied to the front half of the torso through the
reference camera), plus the back above z ~64.5 (hidden behind the hair / wings), minus the two shoulder straps
(vertical slabs in plan crossing each shoulder top).  The two lapels of the wrap get a rolled hem (a soft roll just
inside the edge, on the cloth side), the top lapel (her left) a little proud of the under one.
"""
import math
import numpy as np
from scipy.spatial import cKDTree

import figure_tex as TXM

T_CLOTH = 0.68
EDGE = 0.16            # half-width of the fabric step (design units)
C_SH = (-21.3, 23.6); TH_SH = 28.0

# skin region in the reference photo (px): above the her-right armhole and both lapels; V bottom at (466, 358)
ARMHOLE_R = [(384, 357), (387, 342), (391, 326), (397, 311), (404, 300), (410, 294)]
LAPEL_R = [(410, 294), (416, 306), (426, 321), (438, 335), (451, 347), (466, 358)]    # under lapel (her right)
LAPEL_L = [(466, 358), (470, 346), (475, 331), (480, 315), (485, 300), (490, 287)]    # top lapel (her left)
POLY = [(290, 140), (290, 384), (352, 380), (370, 373), (379, 365)] + ARMHOLE_R + LAPEL_R[1:] + LAPEL_L[1:] + [(530, 282), (560, 140)]

# shoulder straps: plan polylines (x, y) crossing each shoulder top, half-width, from z
STRAPS = [([(-23.0, 16.6), (-23.9, 19.6), (-25.0, 23.0), (-26.0, 26.6), (-26.4, 29.0)], 1.05, 60.0),
          ([(-12.4, 22.4), (-12.6, 25.4), (-13.4, 28.4), (-14.6, 31.0)], 1.0, 60.0)]

# rolled hems (px polylines on the cloth side measured from the edge): (line, crest height, crest offset, width)
ROLLS = [(LAPEL_L[:-1] + [(493, 280)], 0.42, 0.95, 0.85, 'L'),
         ([(406, 287)] + LAPEL_R, 0.24, 0.85, 0.75, 'R'),
         (ARMHOLE_R, 0.16, 0.7, 0.6, 'A')]

ZRAMP = (40.0, 47.0)     # cloth thickness fades in over the waist (the skirt base already includes it)
SUB = ((-40.0, 4.0, 40.0), (4.0, 42.0, 86.5))


def _dense(poly, step=0.25):
    P = np.asarray(poly, float)
    out = [P[0]]
    for a, b in zip(P[:-1], P[1:]):
        n = max(1, int(np.linalg.norm(b - a) / step))
        out.append(a + (b - a) * (np.arange(1, n + 1) / n)[:, None])
    return np.vstack([np.atleast_2d(o) for o in out])


def _seg_dist(Q, poly):
    """distance from 2D points Q to the polyline, and the normalised arclength parameter of the nearest point."""
    D = _dense(poly)
    L = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(D, axis=0), axis=1))])
    d, i = cKDTree(D).query(Q)
    return d, L[i] / L[-1]


def offset_field(X, Y, Z, px_per_mm=6.7):
    """cloth offset (design units, >= 0) at the points (flat arrays)."""
    P = np.stack([X, Y, Z], 1)
    rc = TXM.ref_camera()
    uv = TXM.project(rc, P)
    # signed px distance to the skin polygon (+ inside = skin)
    poly = np.asarray(POLY, float)
    ins = TXM.inpoly(uv, poly)
    d, _ = _seg_dist(uv, list(poly) + [poly[0]])
    sd = np.where(ins, d, -d) / px_per_mm
    skin_f = TXM.sstep(sd, -EDGE, EDGE)
    t = math.radians(TH_SH)
    b = (X - C_SH[0]) * math.sin(t) - (Y - C_SH[1]) * math.cos(t)       # forward coordinate in the shoulder frame
    front = TXM.sstep(b, -2.6, -0.6)
    skin_b = TXM.sstep(Z, 64.0, 64.7)
    skin = front * skin_f + (1 - front) * skin_b
    for pl, w, z0 in STRAPS:
        dp, s = _seg_dist(np.stack([X, Y], 1), pl)
        strap = (1 - TXM.sstep(dp, w - EDGE, w + EDGE)) * TXM.sstep(Z, z0, z0 + 1.0)
        skin = skin * (1 - strap)
    cloth = 1 - skin
    off = T_CLOTH * cloth * TXM.sstep(Z, *ZRAMP)
    # rolled lapel hems: a soft crest just inside the fabric edge (on the cloth side), fading at the ends
    for line, hh, c0, wd, tag in ROLLS:
        dl, s = _seg_dist(uv, line)
        dl = dl / px_per_mm
        env = np.minimum(TXM.sstep(s, 0.0, 0.18), 1 - TXM.sstep(s, 0.85, 1.0)) if tag != 'L' else 1 - TXM.sstep(s, 0.9, 1.0)
        bell = np.exp(-((dl - c0) / wd) ** 2) * TXM.sstep(dl, 0.05, 0.4)
        off += hh * bell * env * cloth * front
    return off


def apply(Gb, lo, h):
    """offset the base block in place (Gb: figure block at lo, spacing h)."""
    a = [max(0, int(math.floor((SUB[0][i] - lo[i]) / h))) for i in range(3)]
    bb = [min(Gb.shape[i], int(math.ceil((SUB[1][i] - lo[i]) / h)) + 1) for i in range(3)]
    V = Gb[a[0]:bb[0], a[1]:bb[1], a[2]:bb[2]]
    near = np.abs(V) < 2.5
    idx = np.nonzero(near)
    X = lo[0] + (a[0] + idx[0]) * h; Y = lo[1] + (a[1] + idx[1]) * h; Z = lo[2] + (a[2] + idx[2]) * h
    off = offset_field(X, Y, Z)
    V[idx] -= off.astype(V.dtype)
    # outside the processed shell / sub-block: the plain cloth offset (keeps the field continuous)
    far = ~near
    if far.any():
        iz = np.nonzero(far)
        Zf = lo[2] + (a[2] + iz[2]) * h
        V[iz] -= (T_CLOTH * TXM.sstep(Zf, *ZRAMP) * (Zf < 63.0)).astype(V.dtype)
    # the rest of the block below / beside the sub-block
    zs = lo[2] + np.arange(Gb.shape[2]) * h
    ramp = (T_CLOTH * TXM.sstep(zs, *ZRAMP)).astype(Gb.dtype)
    M = np.ones(Gb.shape[:2], bool); M[a[0]:bb[0], a[1]:bb[1]] = False
    Gb[M] -= ramp[None, :]
    if a[2] > 0:
        Gb[a[0]:bb[0], a[1]:bb[1], :a[2]] -= ramp[None, None, :a[2]]
    if bb[2] < Gb.shape[2]:
        Gb[a[0]:bb[0], a[1]:bb[1], bb[2]:] -= ramp[None, None, bb[2]:]
