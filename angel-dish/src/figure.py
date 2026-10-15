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
import figure_cloth as CL

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
JR = np.array([-30.2, 20.1, 70.6])      # her right shoulder joint (viewer left; r3c3 raised ~1.7: rounder, higher cap)
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
    B.ellipsoid(P((-19.5, 23.4), -0.5, 0.3, 43.0, 28.0), (8.8, 6.9, 7.0), xaxis=l4, yaxis=f4, k=5.0)
    # pelvis
    l5, f5 = frame(TH_PE)
    B.ellipsoid(P(C_PE, -0.6, 0, 36.5, TH_PE), (11.0, 8.6, 7.4), xaxis=l5, yaxis=f5, k=5.0)   # (r3c3: her-left hip pulled in)
    # bust (under clinging satin), placed on the photo: her right breast (viewer left, px ~440,382) and her left
    # breast (viewer right, px ~497,362, rounder, forming the chest contour against the wing); distinct rounded
    # forms (low blend k) standing ~1.5 proud of the under-bust line
    # (round 3c1: further forward -- apex ~3 proud of the under-bust; her left one higher, forming the contour
    #  against the wing at px ~508)
    # (round 3c2: soft clothed bust -- wide blend, flattened upper pole on her right one so the chest slopes into it)
    # (round 3c3: broad flattened domes under the stretched satin -- wide blend, no apex point)
    for c, r, d, kb in (((-20.4, 16.1, 62.0), (4.4, 3.1, 3.5), (0.3, -0.93, -0.3), 3.2),
                        ((-11.7, 18.5, 63.2), (3.8, 3.3, 3.6), (0.75, -0.62, -0.2), 3.0)):
        dv = U(d); xv = U(np.cross(dv, (0, 0, 1)))
        B.ellipsoid(c, r, xaxis=xv, yaxis=dv, k=kb)
    # (round 3c3: no sternum filler under the V -- the cleavage notch is cut in subtract_details)
    # waist front under the bust: fabric clinging over the stomach (no rib-cage hollow) and the lap junction
    B.ellipsoid((-18.6, 17.4, 54.5), (4.6, 0.9, 3.6), k=2.5)     # (3c2: ends inside the waist side -- no lip at px 485,425)
    B.ellipsoid((-16.5, 17.6, 50.5), (3.0, 1.0, 2.2), k=2.5)
    # side of the chest under her left breast (fills the bust into the rib cage, no hollow toward the wing)
    B.ellipsoid((-13.9, 22.8, 60.2), (3.0, 3.5, 4.6), k=3.5)
    # upper chest above the bust: forward so the sternum / collarbones stand in the light in front of the hair
    B.ellipsoid(P(C_SH, 0.2, 5.1, 68.9, TH_SH), (4.5, 1.8, 2.6), xaxis=l2, yaxis=f2, k=2.0)
    # her left upper chest / pectoral (round 3c2: fills the pocket between the neck, her left shoulder and the bust
    # so the sternum and upper chest stand lit between the hair locks)
    B.ellipsoid((-12.8, 20.0, 68.3), (4.0, 2.8, 3.4), xaxis=l2, yaxis=f2, k=2.5)
    # trapezius slopes neck -> shoulders (shoulder line slopes down outward)
    for s, J in ((-1, JR), (1, JL)):
        nside = P(C_SH, 2.3 * s, -0.9, 72.0, TH_SH)
        B.rcone(nside, J + np.array([0, 0, 1.1]) - 1.2 * s * l2, 2.4, 2.2, k=2.5)
    # shoulder balls (deltoid caps)
    B.sphere(JR + np.array([0.6, 0.2, 0.0]), 2.7, k=2.2)
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
        B.tube(resample(catmull([a, m, b], per=6), 7), np.linspace(0.78, 0.9, 7), k=1.0)
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
    # her right side (round 3c1): the torso side stays at x ~-28.5 down to the waist (a real slot between the
    # hanging arm and the body); the gown bunches on the hip below the hand and hangs as a column of drapery
    # (outer edge px ~323) that turns into the top roll of the train sweeping left to the wing base (px 283,577 ->
    # 250,587)
    B.ellipsoid((-31.0, 22.5, 33.5), (3.4, 5.0, 5.5), k=4.0)
    B.ellipsoid((-33.6, 22.4, 34.8), (2.8, 4.2, 4.2), k=3.0)
    B.eseg(np.array([-36.0, 21.0, 35.0]), np.array([-37.0, 20.8, 28.5]), (0, 1, 0), 2.0, 2.4, 3.2, 3.6, k=2.5)
    # (round 3c2: top edge level at photo px y ~592-598 from x 215 to 320 -- the window above it is rectangular)
    # (round 3c2b: the drape flares diagonally out from below the hand toward the wing base -- photo contour px
    #  (323,530) -> (273,587) -> (247,597) -- then runs on level at px y ~597 into the wall)
    # (round 3c3: the drape drops as a column at x ~-38.5 (photo outline px ~320, open window beside it) and only then
    #  runs level along the floor into the wing base; round end buried in the wall -- no horn)
    B.tube(resample(catmull([(-36.8, 21.3, 34.5), (-37.2, 21.0, 28.0), (-37.6, 20.8, 23.6), (-40.8, 20.6, 20.9),
                             (-48.0, 20.8, 20.3), (-54.5, 21.4, 19.6), (-56.5, 21.6, 19.2)], per=8), 18),
           np.concatenate([np.linspace(2.4, 2.6, 5), np.linspace(2.7, 2.6, 7), np.linspace(2.6, 2.5, 6)]), k=2.2)
    B.ellipsoid((-38.4, 19.6, 23.6), (2.2, 3.5, 2.8), k=3.0)
    # mass under the top roll (no hollow between it and the front side rolls)
    B.ellipsoid((-44.5, 17.5, 15.0), (6.5, 5.0, 3.5), k=3.0)
    # (r3c3b) fill a small crease at the foot of the lower train roll (no slit)
    B.ellipsoid((-43.3, 4.9, 14.6), (1.7, 1.3, 1.3), k=1.2)
    # seat: the hips spread on the gown-covered mound
    B.ellipsoid((-19.0, 27.0, 26.0), (15.5, 11.5, 9.0), xaxis=(math.cos(0.4), math.sin(0.4), 0), k=6.0)
    return B


# ------------------------------------------------------------------ the S-cowl off the knee (round 3c2)
COWL = [  # crest point seen from the ref camera (front surface), half-width, half-thickness
    # (round 3c3: a thin rolled lip of cloth, not a lobe -- half-width <= 3.4, half-thickness <= 1.9)
    ((2.49, -0.5, 35.79), 1.6, 1.2), ((5.11, -1.0, 32.79), 2.4, 1.5), ((7.17, -1.0, 29.16), 3.2, 1.8),
    ((8.08, -1.0, 25.48), 3.4, 1.9), ((7.06, -1.5, 22.89), 2.9, 1.7), ((4.55, -2.5, 21.94), 2.2, 1.5),
    ((1.9, -3.0, 21.89), 1.5, 1.3)]


def cowl():
    """The cloth spilling off the knee: a broad flattened lobe facing the viewer, bulging right and curling back left
    under its lip (photo px 566-633, 560-680).  Hard-unioned eseg chain (no beading), blended into the gown."""
    vd = U((0.01, 0.886, -0.463))                     # ref-camera view direction here
    C, W, T = [], [], []
    for i, (c, w, t) in enumerate(COWL):
        s = w - 1.5
        sh = (-s, 0, 0) if i < 4 else ((-0.6 * s, 0, 0.6 * s) if i == 4 else (0, 0, s))
        C.append(np.asarray(c) + vd * t + np.asarray(sh)); W.append(w); T.append(t)
    C = np.array(C)
    P = resample(catmull(C, per=8), 28)
    s0 = np.linspace(0, 1, len(C)); s1 = np.linspace(0, 1, len(P))
    Wi = np.interp(s1, s0, W); Ti = np.interp(s1, s0, T)
    env = np.minimum(np.clip(s1 / 0.15, 0, 1), np.clip((1 - s1) / 0.2, 0, 1))
    Wi *= 0.6 + 0.4 * np.sin(env * np.pi / 2); Ti *= 0.45 + 0.55 * np.sin(env * np.pi / 2)
    B = Batch()
    for i in range(len(P) - 1):
        B.eseg(P[i], P[i + 1], -vd, Wi[i], Wi[i + 1], Ti[i], Ti[i + 1], 0.0)
    return B


# ------------------------------------------------------------------ arms
def arms():
    B = Batch()
    # her right arm: a full rounded column hanging at her side (deltoid cap, upper arm ~6.4 wide at the shoulder),
    # slightly behind the torso line; the hand rests on and blends into the hip drapery
    sh = JR + np.array([-1.3, -0.2, -1.2])
    el = np.array([-34.3, 23.6, 54.3])          # (r3c3: closer to the flank -- crease, no see-through slot)
    wr = np.array([-36.5, 21.9, 42.5])          # (r3c3b: forearm / hand outer edge in line with the gown's edge, px ~322)
    B.ellipsoid(JR + np.array([-1.3, 0.0, -1.5]), (3.1, 2.7, 3.6), xaxis=(1, 0, 0), yaxis=(0, 1, 0), k=2.0)
    B.eseg(sh + np.array([0.3, 0, 0]), el + np.array([0.4, 0, 0]), (0.25, 1, 0), 3.65, 3.4, 3.0, 2.75, k=1.8)
    B.eseg(el + np.array([0.4, 0, 0]), wr + np.array([0.35, 0, 0]), (0.25, 1, 0), 3.1, 2.2, 2.45, 1.65, k=1.3)
    # biceps swell (front of the upper arm) and the elbow's bony point (back)
    ax = U(el - sh)
    B.ellipsoid(sh + 0.42 * (el - sh) + np.array([0.15, -0.55, 0.0]), (2.3, 2.1, 4.2), xaxis=(1, 0, 0), yaxis=(0, 1, 0), k=1.6)
    B.sphere(el + np.array([-0.5, 1.2, 0.3]), 1.35, k=1.2)
    # (r3c3) web of cloth / flesh at the BACK of the arm-torso slot: from the front only a dark crease, no see-through
    B.eseg(np.array([-30.6, 24.6, 59.5]), np.array([-32.4, 24.4, 45.0]), (0.3, 1, 0), 1.3, 1.5, 1.6, 1.8, k=1.4)
    B.eseg(np.array([-31.4, 24.0, 51.0]), np.array([-33.6, 23.2, 40.5]), (0.3, 1, 0), 1.9, 2.1, 1.9, 2.1, k=1.6)
    B.ellipsoid(el + 0.25 * (wr - el), (2.4, 2.1, 3.2), xaxis=(1, 0, 0), yaxis=(0, 1, 0), k=1.6)
    # hand: slender, back of the hand outward, fingers together lying down over the bunched gown on her hip
    pd = U(np.array([-0.2, -0.4, -0.9]))            # wrist -> knuckles
    bk = np.array([-0.55, -0.83, 0.0])                                                    # back of the hand: out-front
    upv = U(bk - pd * np.dot(bk, pd))
    side = U(np.cross(upv, pd))
    kn = wr + pd * 3.0
    B.eseg(wr - pd * 0.6, kn, upv, 1.6, 1.7, 0.8, 0.7, k=1.0)
    # (round 3c2: slimmer fingers, tips sunk ~0.6 into the drape)
    for o, L, cu, r0 in ((-1.15, 2.5, 0.18, 0.51), (-0.38, 3.1, 0.2, 0.54), (0.4, 2.9, 0.2, 0.54), (1.15, 2.3, 0.16, 0.48)):
        a_ = kn + side * o - upv * 0.1
        m_ = a_ + pd * L * 0.5 - upv * (cu * L * 0.15 + 0.3)
        b_ = a_ + pd * L * 0.92 - upv * (cu * L * 0.5 + 0.65)
        B.tube([a_, m_, b_], [r0, r0 * 0.93, r0 * 0.8], k=0.35)
    # (r3c3b) the fingertips sink into the drape: fill the little pocket between them and the cloth (no dark pit)
    B.ellipsoid((-35.7, 20.5, 38.4), (1.25, 1.0, 1.5), k=0.9)
    # thumb along the inner side, lying against the gown
    th0 = wr + pd * 0.8 + side * 1.6 + upv * -0.5
    B.tube([th0, th0 + pd * 1.5 + side * 0.2 - upv * 0.3, th0 + pd * 2.6 + side * 0.05 - upv * 0.5], [0.62, 0.56, 0.48], k=0.4)
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
    S.ellipsoid(NOTCH + np.array([0.0, -0.45, 0.7]), (1.3, 0.55, 0.9), k=1.0)
    # (round 3: no carved under-bust line -- the breasts' own rounded undersides make the shadow)
    # (round 3c3) cleavage notch just above the V bottom (photo px 462-472, 336-358): a narrow wedge ~1.2 deep
    if not os.environ.get('FIG_NOCLEAV'):
        import figure_tex as TX
        T = TX.CamTex(TX.ref_camera(), (0, 0, 1179, 1078), 1.0, F.G, F.lo, F.h, full=False)
        Q = T.cast([(466.5, 355.0), (468.5, 341.0)])
        if np.isfinite(Q).all():
            n = T.normals(Q).mean(0); n /= np.linalg.norm(n)
            ax = Q[1] - Q[0]; L = np.linalg.norm(ax); ax /= L
            sd = U(np.cross(n, ax))
            S.ellipsoid(0.5 * (Q[0] + Q[1]) + n * 0.25, (0.75, 0.5 * L + 1.2, 1.45), xaxis=sd, yaxis=ax, k=0.9)
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
    # (round 3c3) her right side: the skirt sheet stays at x >= -39.5 above the floor roll (no tent into the window)
    X3 = xs[:, None, None]; Z3 = zs[None, None, :kz]
    ramp = np.clip((Z3 - 20.5) / 2.5, 0.0, 1.0)
    Gs = (Gs + ramp * (np.maximum(Gs, -39.0 - X3) - Gs)).astype(Gs.dtype)
    del X3, Z3, ramp
    Gb[:, :, :kz] = _smin_np(Gb[:, :, :kz], Gs, 3.0)
    del Gs
    if not os.environ.get('FIG_NOCLOTH'):
        import figure_cloth as CL          # (round 3c3) the bodice as a real cloth layer with crisp fabric edges
        CL.apply(Gb, lo, F.h)
    if os.environ.get('FIG_COWL'):        # (r3c3: the lobe is replaced by a curled hem fold, figure_drape.STREAM)
        DR.blend_into(F, cowl(), 2.0)
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
