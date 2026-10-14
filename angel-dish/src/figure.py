"""Seated angel figure (body + gown, no head/hair) -- round 2.
Side-saddle on her gown at the back-left of the bowl, torso turned ~28 deg to her left (+X), right arm hanging
with the hand on the drapery, left arm hidden behind her back.

Build:
  1. smooth base: torso / pelvis / legs primitives (SDF batch) + a height-field skirt that hangs from the
     thighs / hips / seat and flares onto the bowl floor (figure_skirt) -- no plinth, no planar cuts;
  2. drapery relief: camera-space displacement textures (figure_tex): folds traced on the reference photo are
     ray-cast onto the base and rasterised with true surface widths -- asymmetric crests (gentle upper flank,
     steep lower flank ending in a thin crease), tapered ends, V-neck / armhole as fabric step edges, plus
     fine combed striations along the flow (only when F.h <= FINE_H); orbit-camera textures carry the folds on
     the sides / back the photo does not show;
  3. arms and small subtractive details.
"""
import math
import os
import numpy as np
from sdf import Batch, catmull, resample
import figure_rc as rc
import figure_skirt as SK
import figure_tex as TXM
import figure_folds as FD
import figure_drape as DR

FINE_H = 0.3
BLOCK = ((-56.0, -24.0, -1.0), (36.0, 56.0, 86.0))     # region the figure's own field processing touches


def U(v):
    v = np.asarray(v, float); return v / np.linalg.norm(v)


def frame(th):
    t = math.radians(th)
    return np.array([math.cos(t), math.sin(t), 0.0]), np.array([math.sin(t), -math.cos(t), 0.0])


def P(c, a, b, z, th):
    """point = c(x,y) + a*lat + b*fwd at height z, frame angle th."""
    lat, fwd = frame(th)
    return np.array([c[0], c[1], 0.0]) + a * lat + b * fwd + np.array([0, 0, z])


# ------------------------------------------------------------------ skeleton
TH_SH, TH_CH, TH_WA, TH_PE = 28.0, 26.0, 22.0, 32.0
C_SH = (-21.3, 23.6)          # shoulder-girdle centre (x, y)
C_CH = (-21.0, 23.0)          # chest
C_WA = (-20.0, 22.8)          # waist
C_PE = (-19.0, 24.2)          # pelvis
JR = np.array([-29.6, 19.6, 69.0])      # her right shoulder joint (viewer left)
JL = np.array([-14.2, 30.3, 68.4])      # her left shoulder joint (retracted, hidden)
NOTCH = P(C_SH, 0.0, 5.6, 71.4, TH_SH)  # sternal notch (front of neck base)
NB = np.array([-19.4, 22.2, 69.8])      # neck base centre
NT = np.array([-17.0, 20.4, 82.0])      # neck top (under the skull)


def torso():
    B = Batch()
    lat, fwd = frame(TH_CH)
    # rib cage / chest (deeper front-to-back: no plank profile)
    B.ellipsoid(P(C_CH, 0, 0.35, 62.0, TH_CH), (8.4, 6.95, 9.6), xaxis=lat, yaxis=fwd, k=0)
    # upper chest + shoulder girdle (narrow, sloping)
    l2, f2 = frame(TH_SH)
    B.ellipsoid(P(C_SH, 0, -0.4, 67.6, TH_SH), (9.6, 5.4, 4.2), xaxis=l2, yaxis=f2, k=3.0)
    # waist
    l3, f3 = frame(TH_WA)
    B.ellipsoid(P((-20.5, 22.8), 0, 0, 50.0, TH_WA), (8.4, 5.7, 7.0), xaxis=l3, yaxis=f3, k=5.0)
    # belly / hip top
    l4, f4 = frame(28.0)
    B.ellipsoid(P((-19.5, 23.4), 0, 0.3, 43.0, 28.0), (9.6, 6.9, 7.0), xaxis=l4, yaxis=f4, k=5.0)
    # pelvis
    l5, f5 = frame(TH_PE)
    B.ellipsoid(P(C_PE, 0, 0, 36.5, TH_PE), (12.6, 8.6, 7.4), xaxis=l5, yaxis=f5, k=5.0)
    # bust (under clinging satin), placed on the photo: her right breast (viewer left, px ~440,382) and her left
    # breast (viewer right, px ~497,362, rounder, forming the chest contour against the wing); distinct rounded
    # forms (low blend k) standing ~1.5 proud of the under-bust line
    for c, r, d in (((-18.9, 17.4, 61.3), (3.5, 2.9, 3.2), (0.42, -0.88, -0.22)),
                    ((-12.1, 19.4, 62.3), (3.3, 2.9, 3.1), (0.82, -0.54, -0.20))):
        dv = U(d); xv = U(np.cross(dv, (0, 0, 1)))
        B.ellipsoid(c, r, xaxis=xv, yaxis=dv, k=2.2)
    # sternum between the breasts (soft cleavage, no chasm under the V)
    B.ellipsoid((-15.6, 18.0, 62.8), (2.0, 1.6, 3.0), k=2.2)
    # side of the chest under her left breast (fills the bust into the rib cage, no hollow toward the wing)
    B.ellipsoid((-13.6, 22.8, 60.2), (3.4, 3.6, 4.6), k=3.5)
    # upper chest above the bust: forward so the sternum / collarbones stand in the light in front of the hair
    B.ellipsoid(P(C_SH, 0.2, 4.1, 68.9, TH_SH), (3.7, 1.8, 2.6), xaxis=l2, yaxis=f2, k=2.0)
    # trapezius slopes neck -> shoulders (shoulder line slopes down outward)
    for s, J in ((-1, JR), (1, JL)):
        nside = P(C_SH, 2.3 * s, -0.9, 72.0, TH_SH)
        B.rcone(nside, J + np.array([0, 0, 1.1]) - 1.2 * s * l2, 2.4, 2.2, k=2.5)
    # shoulder balls (deltoid caps)
    B.sphere(JR + np.array([0.6, 0.2, 0.1]), 2.1, k=2.2)
    B.sphere(JL, 3.0, k=2.0)
    # slender neck (contract C5: r 3.1 base -> 2.8 top)
    B.rcone(NB, NT, 3.1, 2.8, k=2.2)
    # her left trapezius rises under the hair (no pocket between neck, shoulder and the hair lock)
    B.ellipsoid((-14.5, 24.0, 72.0), (2.2, 2.0, 2.5), k=1.5)
    # sternocleidomastoid hints (behind the ear -> sternal notch)
    B.rcone(np.array([-20.9, 22.4, 80.2]), NOTCH + np.array([-0.9, 0.7, 0.5]), 0.85, 0.7, k=1.3)
    B.rcone(np.array([-14.2, 22.0, 79.8]), NOTCH + np.array([0.9, 0.9, 0.5]), 0.75, 0.65, k=1.3)
    # clavicles (subtle, ~0.2 proud)
    for s, J in ((-1, JR), (1, JL)):
        a = NOTCH + 1.1 * s * l2 + np.array([0, 0.4, -0.25])
        b = J + np.array([0, 0, 2.0]) - 0.8 * s * l2
        m = 0.5 * (a + b) - 0.85 * f2 * (1 if s < 0 else -0.2) + np.array([0, 0, 0.25])
        B.tube(resample(catmull([a, m, b], per=6), 7), np.linspace(0.62, 0.75, 7), k=1.0)
    # lower back fill (no shelf under the rib cage)
    B.ellipsoid(P(C_WA, 0, -0.8, 55.5, TH_WA), (8.0, 5.6, 6.0), xaxis=l3, yaxis=f3, k=4.0)
    # back: shoulder blades + upper back surface the wing roots attach to (y ~26-28, contract C4)
    for s in (-1, 1):
        c = P(C_CH, 4.6 * s, -5.9, 63.5, TH_CH)
        B.ellipsoid(c, (3.4, 1.2, 4.6), xaxis=lat, yaxis=fwd, k=2.8)
    return B


def legs():
    """Pelvis-to-feet body under the gown (fabric thickness included); the skirt height field hangs from it."""
    B = Batch()
    RHIP = np.array([-24.5, 21.5, 38.0]); RKNEE = np.array([-1.5, 5.0, 34.6])
    LHIP = np.array([-14.5, 28.0, 35.0]); LKNEE = np.array([1.5, 14.0, 28.5])
    RANK = np.array([1.0, 22.0, 14.0]); LANK = np.array([4.0, 29.0, 12.0])
    B.rcone(RHIP, RKNEE, 7.0, 4.1, k=4.0)
    B.rcone(LHIP, LKNEE, 6.6, 3.9, k=4.0)
    B.rcone(RKNEE, RANK, 3.7, 3.0, k=3.0)
    B.rcone(LKNEE, LANK, 3.6, 2.9, k=3.0)

    # lap bridge between the thighs (soft dip, fabric stretched knee to knee)
    B.eseg(np.array([-18.0, 22.0, 39.0]), np.array([-3.5, 11.5, 35.0]), (0, 0, 1), 8.0, 4.6, 5.0, 4.5, k=4.0)
    # her right side under the hanging arm: the gown over waist and hip fills out to the arm (no see-through gap
    # between forearm and hip; the hand rests on it)
    B.rcone(np.array([-29.0, 23.6, 50.5]), np.array([-31.0, 22.8, 37.5]), 2.4, 3.4, k=3.5)
    B.ellipsoid((-31.0, 22.5, 33.5), (3.4, 5.0, 5.5), k=4.0)
    # gown hanging off her right hip below the hand (the drapery mass the hand rests on, out to px ~318)
    B.ellipsoid((-33.6, 21.0, 31.5), (3.0, 5.2, 5.0), k=4.0)
    # seat: the hips spread on the gown-covered mound
    B.ellipsoid((-19.0, 27.0, 26.0), (15.5, 11.5, 9.0), xaxis=(math.cos(0.4), math.sin(0.4), 0), k=6.0)
    return B


# ------------------------------------------------------------------ arms
def arms():
    B = Batch()
    # her right arm: a full rounded column hanging at her side (deltoid cap, upper arm ~6.4 wide at the shoulder),
    # slightly behind the torso line; the hand rests on and blends into the hip drapery
    sh = JR + np.array([-1.3, -0.2, -1.2])
    el = np.array([-33.4, 24.2, 50.6])
    wr = np.array([-35.0, 22.0, 38.0])
    B.ellipsoid(JR + np.array([-1.2, 0.0, -1.5]), (2.8, 2.6, 3.6), xaxis=(1, 0, 0), yaxis=(0, 1, 0), k=2.2)
    B.eseg(sh, el, (0.25, 1, 0), 3.2, 2.6, 3.0, 2.4, k=2.0)
    B.eseg(el, wr, (0.25, 1, 0), 2.5, 1.9, 2.25, 1.75, k=1.4)
    B.ellipsoid(el + 0.22 * (wr - el), (2.2, 2.25, 3.5), xaxis=(1, 0, 0), yaxis=(0, 1, 0), k=1.8)
    # hand: back of the hand outward, fingers together (a soft mitten with shallow finger grooves) lying down
    # over the bunched drapery of her hip
    pd = U(np.array([0.05, -0.22, -0.97]))          # wrist -> knuckles
    upv = U(np.array([-1.0, 0.2, 0.0]) - pd * np.dot(np.array([-1.0, 0.2, 0.0]), pd))   # back of the hand (outward)
    side = U(np.cross(upv, pd))
    kn = wr + pd * 3.5
    B.eseg(wr - pd * 0.4, kn, upv, 1.6, 2.0, 0.95, 0.8, k=0.9)
    for o, L, cu in ((-1.6, 3.0, 0.32), (-0.55, 3.7, 0.36), (0.55, 3.5, 0.36), (1.6, 2.8, 0.3)):
        a_ = kn + side * o * 0.95 - upv * 0.1
        m_ = a_ + pd * L * 0.5 - upv * cu * L * 0.18
        b_ = a_ + pd * L * 0.86 - upv * cu * L * 0.6
        B.tube([a_, m_, b_], [0.8, 0.76, 0.68], k=0.45)
    th0 = wr + pd * 1.2 + side * 1.8 - upv * 0.5
    B.tube([th0, th0 + pd * 1.8 + side * 0.5 - upv * 0.6, th0 + pd * 3.0 + side * 0.3 - upv * 1.0], [0.8, 0.72, 0.64], k=0.6)
    # her left arm: hidden from the front -- the upper arm drops behind her left side, the forearm lies in the
    # small of her back under the gown's back drape, hand resting on her right hip from behind
    sh = JL + np.array([0.0, 0.6, -1.0])
    el = np.array([-15.2, 30.4, 52.5]); wr = np.array([-23.0, 30.0, 45.5])
    B.rcone(sh, el, 2.8, 2.2, k=2.4)
    B.rcone(el, wr, 1.9, 1.45, k=2.4)
    hd = U(np.array([-1.0, -0.2, -0.45]))
    kn = wr + hd * 4.2
    B.eseg(wr, kn, (0, 1, 0), 1.6, 1.8, 0.9, 0.8, k=1.0)
    return B


def surf_pts(F, P, off=0.0, iters=8):
    """move points onto the zero level of F (along the field gradient), then offset `off` along the normal."""
    import figure_k as K
    P = np.ascontiguousarray(np.atleast_2d(np.asarray(P, float)))
    G = F.G; lo = F.lo; h = F.h
    def smp(Q):
        Q = np.ascontiguousarray(Q, np.float64); o = np.empty(len(Q))
        K.sample(G, lo[0], lo[1], lo[2], h, Q, o); return o
    for _ in range(iters):
        d = smp(P)
        n = np.stack([smp(P + e) - smp(P - e) for e in np.eye(3) * 0.5 * h], 1)
        n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
        P = P - n * np.clip(d, -1.5, 1.5)[:, None]
    return P + n * off, n


def crease(S, F, ctrl, r, k, off=0.0, per=6, n=16, rmin=0.12):
    """soft subtractive crease lying in the surface (tube centred on the surface, tapering at both ends)."""
    P = resample(catmull(np.asarray(ctrl, float), per=per), n)
    P, _ = surf_pts(F, P, off)
    rr = r * np.sin(np.linspace(0.1, 0.9, n) * np.pi) + rmin
    S.tube(P, rr, k=k)


def subtract_details(F):
    S = Batch()
    # sternal notch: shallow dip just above the clavicle heads
    S.sphere(NOTCH + np.array([0.0, -0.3, 0.9]), 0.8, k=1.2)
    # (round 3: no carved under-bust line -- the breasts' own rounded undersides make the shadow)
    # separation between her hanging right arm and the torso (shadow crease from the armpit down along the junction)
    crease(S, F, [(-28.4, 19.6, 62.0), (-28.9, 20.6, 58.0), (-29.3, 21.1, 54.5), (-29.9, 21.8, 50.0), (-30.6, 22.4, 46.0)],
           0.7, 1.3, off=0.25)
    # lumbar hollow
    S.ellipsoid((-20.0, 30.2, 52.0), (4.5, 1.6, 3.5), k=2.0)
    return S


def block_slices(F):
    lo, hi = BLOCK
    a = [int(max(0, math.floor((lo[i] - F.lo[i]) / F.h))) for i in range(3)]
    b = [int(min(F.shape[i], math.ceil((hi[i] - F.lo[i]) / F.h) + 1)) for i in range(3)]
    return tuple(slice(a[i], b[i]) for i in range(3)), np.array([F.lo[i] + a[i] * F.h for i in range(3)])


def drop_specks(Gb, h, keep_vox=None):
    """Remove small solid islands the relief may leave floating in front of the surface (printability)."""
    from scipy import ndimage
    solid = Gb < 0
    lab, n = ndimage.label(solid)
    if n <= 1:
        return
    cnt = np.bincount(lab.ravel())
    cnt[0] = 0
    keep_vox = keep_vox or int(60.0 / h ** 3)          # anything under ~60 cubic units goes
    small = cnt < keep_vox
    small[0] = False
    m = small[lab]
    Gb[m] = np.maximum(Gb[m], 0.6 * h)
    del lab, m, solid
    # and small enclosed voids (bubbles) the creases may open inside the material
    empty = Gb >= 0
    lab, n = ndimage.label(empty)
    if n > 1:
        cnt = np.bincount(lab.ravel()); cnt[0] = 0
        small = cnt < keep_vox; small[0] = False
        m = small[lab]
        Gb[m] = np.minimum(Gb[m], -0.6 * h)


def _smin_np(a, b, k):
    h = np.clip(k - np.abs(a - b), 0, None) / k
    return np.minimum(a, b) - h * h * k * 0.25


def component(F):
    fine = F.h <= FINE_H
    sl, lo = block_slices(F)
    # 1. base: body primitives + skirt height field
    F.apply(rc.merge(torso(), legs()), pad=3.0)
    Gb = F.G[sl]
    xs, ys, zs = [lo[i] + np.arange(Gb.shape[i]) * F.h for i in range(3)]
    kz = int(np.searchsorted(zs, 46.0))
    Gs, _ = SK.sdf_block(xs, ys, zs[:kz], F.h)
    Gb[:, :, :kz] = _smin_np(Gb[:, :, :kz], Gs, 3.0)
    del Gs
    if not os.environ.get('FIG_NOFOLDS'):
        # 2a. heavy solid satin folds (hip tubes, swag pocket + roll, knee fall and curl, hem rolls)
        if not os.environ.get('FIG_NODRAPE'):
            DR.apply(F, np.ascontiguousarray(Gb).copy(), lo, F.h)
        # 2b. drapery relief (bodice + lap tension folds, orbit folds on the sides / back)
        F.apply(FD.bands(np.ascontiguousarray(Gb), lo, F.h), pad=3.0)
        G0 = Gb.copy()
        FD.apply_all(G0, Gb, lo, F.h, fine)
        del G0
        if fine:
            # light smoothing of the relief at export resolution: no sub-0.3 teeth survive along fold edges
            from scipy import ndimage
            Gb[...] = ndimage.gaussian_filter(Gb, 0.6, mode='nearest')
        drop_specks(Gb, F.h)
    # 3. details + arms
    F.apply(subtract_details(F), 'sub')
    F.apply(arms(), pad=2.0)
    return F
