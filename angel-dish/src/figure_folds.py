"""Drapery fold specification for the figure's gown (helper for figure.py).

PX folds are traced on the reference photo (pixel polylines) and laid onto the base surface through the
reference camera; O3 folds are designed in 3D for the sides / back the photo does not show and are laid through
orbit cameras.  Units: A crest height (+) / valley depth (-), wu gentle half-width, wd steep half-width (design
units).  steep: which side of the crest is the steep flank ('below'/'above'/'left'/'right' in the image).
"""
import math
import numpy as np
import figure_tex as TXM


def F(pix, A, wu, wd=None, steep="below", ta=0.3, tb=0.3, cr=0.0, step=0.0, sband=3.0, wt=0.55, hp=1.0, shape='cos'):
    return dict(pix=pix, A=A, wu=wu, wd=wd, steep=steep, ta=ta, tb=tb, cr=cr, step=step, sband=sband, wt=wt, hp=hp, shape=shape)


# ------------------------------------------------------------------ traced on the photo
# round 2: fewer, broader, smoother folds (clinging satin); cosine sections with a gentle upper flank and a
# steeper lower flank, light shadow creases, every end tapered; nothing stacked on top of another fold.
BODICE = [
    # top lapel (her left side of the V): a soft rolled fabric edge from her left shoulder to the V bottom, fading out
    # just past it (no long knife line across the stomach)
    F([(484, 296), (480, 318), (474, 340), (467, 358), (459, 372), (450, 384)],
      0.55, 1.3, 0.7, 'above', ta=0.06, tb=0.35, cr=0.0, step=0.4, sband=2.4),
    # under lapel edge (her right side of the V)
    F([(416, 298), (426, 316), (438, 332), (450, 346), (463, 360)], 0.4, 1.2, 0.7, 'above', ta=0.12, tb=0.1, cr=0.0),
    # armhole edge on her right shoulder (a rolled edge, arm side a little lower)
    F([(393, 292), (386, 314), (381, 338), (380, 362), (383, 382), (389, 398)], 0.5, 1.2, 0.8, 'left', ta=0.1, tb=0.35,
      cr=0.0, step=0.38, sband=2.0),
    # curved wrap folds from her left side (below the bust) toward her right hip: rounded crests with soft valleys,
    # starting below the under-bust line (no ledge under the breasts)
    F([(505, 412), (484, 420), (460, 432), (436, 448), (414, 466), (398, 482)], 1.75, 2.3, 1.5, ta=0.35, tb=0.45, cr=0.0),
    F([(499, 446), (478, 455), (455, 469), (432, 487), (412, 506)], 1.6, 2.4, 1.6, ta=0.35, tb=0.45, cr=0.0),
    F([(500, 428), (480, 436), (457, 449), (433, 466), (410, 486)], -1.0, 1.5, 1.3, ta=0.35, tb=0.4),
    F([(470, 476), (452, 490), (432, 508), (416, 526)], 1.1, 2.0, 1.4, ta=0.4, tb=0.45, cr=0.0),
]

LAP = [
    # two soft tension folds from her right hip over the thigh toward the knee (diverging, not parallel), a soft
    # valley between them
    F([(404, 478), (440, 492), (478, 508), (516, 524), (546, 534)], 1.3, 3.4, 2.4, ta=0.35, tb=0.4, cr=0.0),
    F([(400, 516), (432, 534), (466, 554), (500, 570), (528, 580)], 1.2, 3.4, 2.4, ta=0.35, tb=0.4, cr=0.0),
    F([(402, 497), (440, 514), (478, 532), (514, 550)], -0.6, 2.0, 1.8, ta=0.35, tb=0.4),
]

HIP = [
    # her right hip: broad soft falls from below the hand down to the pooled hem (start well below the fingers,
    # wide and low so they never read as extra fingers)
    F([(350, 548), (348, 566), (349, 584), (352, 600)], 1.05, 3.2, 2.2, 'left', ta=0.45, tb=0.4),
    F([(384, 520), (387, 542), (390, 562), (393, 582), (396, 598)], 1.35, 3.4, 2.3, 'left', ta=0.4, tb=0.35),
    F([(366, 540), (368, 558), (370, 574), (373, 588)], -0.8, 2.2, 1.6, ta=0.4, tb=0.4),
]

SWAG = [
    # the U swag hanging between her right hip and the knee: broad crest, the pocket above it
    F([(372, 585), (388, 612), (412, 635), (445, 648), (478, 644), (505, 628), (528, 606)], 3.0, 4.6, 2.0, 'above',
      ta=0.3, tb=0.3, cr=0.0),
    F([(392, 592), (404, 614), (422, 628), (448, 634), (474, 627), (494, 610)], -1.6, 2.8, 2.2, ta=0.3, tb=0.35),
]

ROLLS = [
    # folds from the hip converging down-right into the hem sweep
    F([(318, 560), (340, 590), (366, 612), (396, 640), (428, 664), (458, 684)], 2.4, 3.8, 1.8, ta=0.3, tb=0.45, cr=0.0),
    F([(482, 560), (498, 600), (515, 640), (532, 672), (548, 690)], 2.1, 3.6, 1.8, 'left', ta=0.3, tb=0.4, cr=0.0),
    # the hem sweeping out to the right along the floor (varies in height / width, tapers at both ends)
    F([(300, 642), (350, 657), (400, 673), (450, 688), (500, 697), (548, 698), (595, 690)], 2.6, 4.8, 2.1, 'below',
      ta=0.22, tb=0.38, cr=0.0, wt=0.65),
]

KNEE = [
    # the fall from the knee: broad, strongly lit right flank, steeper left flank
    F([(549, 528), (548, 560), (546, 595), (543, 628), (538, 652)], 1.9, 5.0, 2.3, 'left', ta=0.22, tb=0.4, cr=0.0),
    # the gown sweeping off the knee down and to the right onto the floor: one long S-sweep plus a broad
    # companion fold beside it (no closed curl, no pocket)
    F([(556, 546), (572, 574), (592, 600), (612, 623), (628, 649), (642, 676), (656, 700)], 2.1, 4.4, 2.1, 'R',
      ta=0.25, tb=0.4, cr=0.0),
    F([(568, 586), (596, 622), (626, 656), (660, 690), (690, 714)], 1.5, 4.0, 2.1, 'R', ta=0.3, tb=0.4, cr=0.0),
]

# solid bands (rolled swags) laid on the base before the relief: pix, half-width w, crest height, half-thickness t
def BD(pix, w, hgt, t=None, ta=0.15, tb=0.2, k=1.6, skew=0.0):
    return dict(pix=pix, w=w, hgt=hgt, t=t if t is not None else 0.7 * w, ta=ta, tb=tb, k=k, skew=skew)


BANDS = []     # round 2: no solid rolled tubes (they read as a plinth ring)


def _gain(lst, g, gw=1.0):
    out = []
    for sp in lst:
        sp = dict(sp); sp['A'] *= g; sp['wu'] *= gw
        if sp['wd'] is not None:
            sp['wd'] *= gw
        out.append(sp)
    return out


def _soften(lst, wr=0.62, tmin=0.35):
    """skirt folds: no cliff flanks (steep half-width >= wr * gentle) and long, fading ends"""
    out = []
    for sp in lst:
        sp = dict(sp)
        sp['wd'] = max(sp['wd'] if sp['wd'] is not None else 0.55 * sp['wu'], wr * sp['wu'])
        sp['ta'] = max(sp['ta'], tmin); sp['tb'] = max(sp['tb'], tmin)
        out.append(sp)
    return out


PX_FOLDS = BODICE    # round 3: lap / hip / swag / knee / hem folds are solid: hip / swag / knee / hem folds are solid (figure_drape)

# skin inside the V neckline (lowered ~0.7 under the fabric edge; fades out toward the sternal notch)
VNECK = [(463, 362), (450, 346), (438, 332), (426, 316), (418, 300), (414, 288), (487, 288), (483, 300), (478, 320), (472, 342)]
VFADE = (298.0, 314.0)


def steep_side(pix, steep):
    if steep in ('L', 'R'):
        return steep
    p = np.asarray(pix, float); du, dv = p[-1] - p[0]
    # left of travel (image, v down) = (dv, -du)
    if steep == 'below':
        return 'L' if du < 0 else 'R'
    if steep == 'above':
        return 'R' if du < 0 else 'L'
    if steep == 'right':
        return 'L' if dv > 0 else 'R'
    if steep == 'left':
        return 'R' if dv > 0 else 'L'
    raise ValueError(steep)


def lay(T, spec, P):
    T.fold(P, spec['A'], spec['wu'], spec['wd'], steep_side(spec['pix'], spec['steep']) if spec['pix'] is not None else spec['steep'],
           (spec['ta'], spec['tb']), spec['cr'], spec['wt'], True, spec['hp'], spec['step'], spec['sband'], spec.get('shape', 'cos'))


def ref_texture(G0, lo, h, ts):
    c = TXM.ref_camera()
    T = TXM.CamTex(c, (270, 240, 730, 760), ts, G0, lo, h)
    for sp in PX_FOLDS:
        P = T.trace(sp['pix'])
        lay(T, sp, P)
    # combing guides along the solid satin folds (no relief; only steer the fine striations)
    import figure_drape as DR
    for sp in (DR.PX if STRI_GUIDES else []):
        if sp['sub']:
            continue
        P = T.trace(sp['pix'])
        if len(P) >= 3:
            w = float(np.max(sp['w']))
            T.fold(P, 0.0, w, 0.8 * w, 'L', (sp['ta'], sp['tb']), 0.0, 0.55, True, 1.0, 0.0, 3.0, 'cos')
    # V neckline skin step
    m = T.region_step(VNECK, 0.35, soft_px=2.0)
    vv = T.v0 + np.arange(T.nv) / T.ts
    fade = TXM.sstep(vv, *VFADE)[:, None]
    T.D += 0.35 * m * (1 - fade)            # undo the step above the fade line (smooth into the neck)
    T.smask *= 1 - 0.0 * m
    return T


def bands(G0, lo, h):
    """Solid rolled bands traced on the photo -> Batch (smooth-unioned into the base before the relief)."""
    import figure_rc as rc
    from sdf import Batch, resample
    T = TXM.CamTex(TXM.ref_camera(), (0, 0, 1179, 1078), 1.0, G0, lo, h, full=False)
    B = Batch()
    for sp in BANDS:
        P = T.trace(sp['pix'])
        if len(P) < 4:
            continue
        L = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
        P = resample(P, max(4, int(L / 0.9) + 1))
        N = T.normals(P)
        rc.band(B, None, P, sp['w'], sp['hgt'], sp['t'], k=sp['k'], taper=(sp['ta'], sp['tb']), N=N, skew=sp['skew'])
    return B


# ------------------------------------------------------------------ folds the photo does not show (3D, orbit cameras)
def F3(p3, A, wu, wd=None, steep='R', ta=0.25, tb=0.3, cr=0.3, shape='roll', step=0.0, sband=3.0):
    return dict(p3=p3, pix=None, A=A, wu=wu, wd=wd, steep=steep, ta=ta, tb=tb, cr=cr, step=step, sband=sband, wt=0.55, hp=1.0, shape=shape)


# back of the gown: long falls from the waist / hips fanning out to the floor, a few diagonal pulls toward the
# hidden left arm, and soft swags where the train bunches at the back of the seat
BACK = [
    # three broad shallow falls fanning from the small of the back to the floor (open U sections, no tubes)
    F3([(-19, 31.5, 45), (-24, 34, 34), (-29, 36.5, 24), (-33, 37.5, 14)], 1.0, 4.4, 3.2, 'R', ta=0.3, tb=0.45, cr=0.0, shape='cos'),
    F3([(-17, 32, 44), (-18.5, 35.5, 33), (-19.5, 38, 22), (-20, 38.5, 13)], 0.9, 4.0, 3.0, 'R', ta=0.3, tb=0.45, cr=0.0, shape='cos'),
    F3([(-15, 32, 43), (-11, 35, 33), (-8, 37.5, 22), (-6, 38, 13)], 1.0, 4.4, 3.2, 'L', ta=0.3, tb=0.45, cr=0.0, shape='cos'),
    # soft diagonal pull over the hidden left forearm
    F3([(-14, 33, 45), (-20, 34, 39.5), (-27, 33, 34)], 0.55, 2.8, 1.8, 'L', ta=0.35, tb=0.35, cr=0.0, shape='cos'),
]


# her left side (viewer right): the gown over the knees and the tucked-back shins, falling down-back to the floor
SIDE = [
    F3([(0, 7, 38), (4.5, 6.5, 31), (8.5, 5, 23), (11.5, 3, 15)], 1.3, 4.4, 2.2, 'L', ta=0.3, tb=0.45, cr=0.0, shape='cos'),
    F3([(4, 3, 31), (8, 9, 24), (12, 15, 16), (15, 21, 10)], 1.1, 4.5, 2.2, 'L', ta=0.25, tb=0.45, cr=0.15, shape='cos'),
    F3([(4, 12, 29), (7.5, 18, 21), (10, 24, 13)], 1.0, 4.2, 2.0, 'L', ta=0.3, tb=0.45, cr=0.15, shape='cos'),
    F3([(1, 24, 31), (4, 29, 23), (6.5, 33, 14)], 0.9, 4.0, 2.0, 'L', ta=0.3, tb=0.45, cr=0.15, shape='cos'),
]


def orbit_texture(G0, lo, h, ts, target, az, el, folds):
    c = TXM.orbit_camera(target, az, el, 200.0, lens=60.0, W=1000, H=1000)
    import itertools
    L = np.array(lo); Hh = L + np.array(G0.shape) * h
    corners = np.array(list(itertools.product(*zip(L, Hh))))
    uv = TXM.project(c, corners)
    box = (max(0, uv[:, 0].min() - 5), max(0, uv[:, 1].min() - 5), min(1000, uv[:, 0].max() + 5), min(1000, uv[:, 1].max() + 5))
    T = TXM.CamTex(c, box, ts, G0, lo, h)
    for sp in folds:
        P = T.surf(sp['p3'])
        lay(T, sp, P)
    return T


def back_texture(G0, lo, h, ts):
    c = TXM.orbit_camera((-14.0, 30.0, 28.0), 180.0, 20.0, 200.0, lens=60.0, W=1000, H=1000)
    # pixel box of the block
    import itertools
    L = np.array(lo); Hh = L + np.array(G0.shape) * h
    corners = np.array(list(itertools.product(*zip(L, Hh))))
    uv = TXM.project(c, corners)
    box = (max(0, uv[:, 0].min() - 5), max(0, uv[:, 1].min() - 5), min(1000, uv[:, 0].max() + 5), min(1000, uv[:, 1].max() + 5))
    T = TXM.CamTex(c, box, ts, G0, lo, h)
    for sp in BACK:
        P = T.surf(sp['p3'])
        lay(T, sp, P)
    return T


STRI_PITCH, STRI_AMP = 1.25, 0.04
STRI_GUIDES = False     # combing along the solid folds read as crumpled wrinkles at h 0.22 -> off (smooth satin)
RBLUR = 0.5


def apply_all(G0, G, lo, h, fine):
    ts = 2.0 if h <= 0.3 else 1.0
    import os
    T = ref_texture(G0, lo, h, ts)
    if not os.environ.get('FIG_NOREF'):
      T.apply(G0, G, band=6.0, fine=fine, pitch=STRI_PITCH, amp=STRI_AMP, fc=(0.12, 0.38), blur=RBLUR)
    Ts = orbit_texture(G0, lo, h, ts, (5.0, 15.0, 20.0), 75.0, 15.0, SIDE)
    if not os.environ.get('FIG_NOSIDE'):
      Ts.apply(G0, G, band=6.0, fine=fine, pitch=STRI_PITCH, amp=STRI_AMP, fc=(0.3, 0.55), blur=RBLUR)
    Tb = back_texture(G0, lo, h, ts)
    if os.environ.get('FIG_BACKTEX'):      # round 3: the back folds are solid (figure_drape.BACK)
      Tb.apply(G0, G, band=6.0, fine=fine, pitch=STRI_PITCH, amp=STRI_AMP, fc=(0.3, 0.55), blur=RBLUR)
    return T
