"""Solid drapery folds for the figure's gown (helper for figure.py) -- round 3.

Large satin folds are real volume, not a displacement texture: each fold is a soft band with a flattened
elliptical section lying on the base surface (crest `hgt` above it, half-width `w`, tapered in height AND width at
both ends), hard-unioned along its length (no beading) and then smooth-unioned into the gown with a wide blend
(k ~2), so its flanks fillet into the cloth.  `lean` tilts the section toward one side (steep / undercut flank on
that side, gentle ramp on the other).  Recesses (pockets / valleys between heavy folds) are the same band
subtracted.  Paths are traced on the reference photo (pixel polylines ray-cast onto the base surface) or given in
3D for the sides the photo does not show.
"""
import math
import numpy as np
from sdf import Batch, Field, catmull, resample, FAR
import figure_tex as TXM


def FB(pix=None, p3=None, w=3.0, hgt=2.0, t=None, ta=0.3, tb=0.3, lean=0.0, k=2.0, wend=0.45, off=0.0, sub=False, floor=False):
    return dict(pix=pix, p3=p3, w=w, hgt=hgt, t=t, ta=ta, tb=tb, lean=lean, k=k, wend=wend, off=off, sub=sub, floor=floor)


def CH(pix=None, p3=None, w=1.8, depth=1.5, t=None, ta=0.3, tb=0.3, lean=0.0, k=1.4, wend=0.5):
    return dict(pix=pix, p3=p3, w=w, hgt=depth, t=t, ta=ta, tb=tb, lean=lean, k=k, wend=wend, off=0.0, sub=True, floor=False)


# ------------------------------------------------------------------ folds traced on the photo (ref camera px)
# her right hip: heavy vertical folds hanging below the hand, the outer one turning into the swag at the bottom
HIP = [
    FB([(355, 514), (353, 540), (354, 566), (359, 590), (370, 609), (390, 622), (414, 630)], w=[2.4, 2.8, 3.0, 3.0, 2.8, 2.6, 2.4],
       hgt=[1.6, 2.0, 2.2, 2.1, 1.8, 1.5, 1.0], ta=0.3, tb=0.35, lean=0.25, k=2.0, wend=0.8),
    FB([(385, 504), (387, 532), (390, 560), (395, 586), (403, 606)], w=[1.8, 2.2, 2.4, 2.2, 2.0], hgt=[1.2, 1.6, 1.7, 1.4, 1.0],
       ta=0.35, tb=0.4, lean=0.2, k=1.8, wend=0.8),
]

# the U swag between her right hip and the knee: a soft shadowed hollow under the lap, the heavy U roll below it
# (lowest in the middle, broad, leaning up so its upper flank overhangs the hollow)
SWAG = [
    CH([(404, 612), (424, 628), (450, 640), (476, 645), (498, 639), (514, 627)], w=[1.8, 2.3, 2.6, 2.6, 2.3, 1.8],
       depth=[0.6, 1.3, 1.7, 1.7, 1.3, 0.6], ta=0.3, tb=0.35, k=2.2, wend=0.8),
    FB([(396, 600), (420, 615), (450, 626), (480, 628), (506, 620)], w=[1.6, 2.2, 2.4, 2.2, 1.8], hgt=[0.6, 1.2, 1.4, 1.2, 0.7],
       ta=0.3, tb=0.35, lean=0.4, k=1.8, wend=0.8),
    FB([(378, 616), (406, 640), (442, 660), (484, 668), (522, 660), (554, 642), (580, 620)], w=[2.4, 3.0, 3.6, 3.8, 3.6, 3.0, 2.6],
       hgt=[1.2, 2.0, 2.6, 2.8, 2.6, 2.2, 1.6], ta=0.3, tb=0.3, lean=0.35, k=2.2, wend=0.8),
]

# the fall off the knee: a heavy vertical fold, a thinner companion, and the broad fold sweeping down-right that
# curls toward the floor
KNEE = [
    FB([(522, 532), (527, 566), (534, 600), (540, 634), (544, 664)], w=[2.4, 3.0, 3.2, 3.0, 2.8], hgt=[1.2, 2.0, 2.2, 2.0, 1.4],
       ta=0.25, tb=0.35, lean=-0.15, k=2.0, wend=0.8),
    FB([(549, 576), (557, 604), (565, 632), (571, 660)], w=[1.6, 2.0, 2.2, 2.0], hgt=[0.8, 1.3, 1.4, 1.0], ta=0.35, tb=0.4, k=1.6,
       wend=0.85),
    FB([(556, 548), (576, 574), (596, 600), (612, 624), (622, 648), (626, 672)], w=[2.4, 3.0, 3.4, 3.4, 3.2, 2.8],
       hgt=[0.5, 1.3, 2.0, 2.3, 2.0, 1.2], ta=0.4, tb=0.4, lean=[0.0, -0.15, -0.3, -0.35, -0.25, -0.1], k=2.0, wend=0.85),
]

# thinner flowing folds sweeping down / right off the knee and the lap
SEC = [
    FB([(530, 518), (547, 545), (565, 572), (583, 596), (598, 614)], w=[1.2, 1.6, 1.8, 1.6, 1.2], hgt=[0.4, 0.9, 1.1, 0.9, 0.4],
       ta=0.35, tb=0.4, lean=0.2, k=1.5, wend=0.8),
    FB([(504, 560), (512, 588), (519, 616), (525, 644)], w=[1.1, 1.5, 1.6, 1.3], hgt=[0.4, 0.9, 1.0, 0.5], ta=0.35, tb=0.4,
       lean=-0.2, k=1.5, wend=0.8),
    FB([(370, 640), (395, 656), (425, 668)], w=[1.2, 1.6, 1.3], hgt=[0.5, 0.9, 0.5], ta=0.4, tb=0.45, lean=0.2, k=1.5, wend=0.8),
]

# lower skirt: long rolls sweeping from the knee side toward the front-left onto the floor (S-curved, uneven)
HEM = [
    FB([(584, 650), (558, 660), (522, 670), (474, 676), (424, 670), (372, 660), (318, 652), (290, 650)],
       w=[2.0, 2.8, 3.4, 3.2, 3.0, 3.2, 2.8, 2.4], hgt=[0.8, 1.8, 2.5, 2.3, 2.1, 2.3, 1.9, 1.3], ta=0.4, tb=0.3,
       lean=[0.0, 0.2, 0.35, 0.35, 0.35, 0.35, 0.3, 0.25],
       k=2.2, wend=0.8),
    FB([(596, 702), (548, 712), (488, 716), (428, 708), (372, 696), (318, 688), (284, 686)],
       w=[2.4, 3.0, 3.4, 3.4, 3.0, 2.8, 2.4], hgt=[1.2, 2.0, 2.4, 2.4, 2.2, 1.8, 1.2], ta=0.3, tb=0.35, lean=0.3, k=2.0, wend=0.8),
]

# the lap: soft tension folds from her right hip over the thigh toward the knee (diverging), low and broad
LAP = [
    FB([(404, 478), (440, 491), (478, 506), (514, 521), (544, 531)], w=[1.8, 2.4, 2.6, 2.4, 1.8], hgt=[0.6, 1.1, 1.3, 1.1, 0.6],
       ta=0.35, tb=0.4, lean=0.3, k=1.8, wend=0.8),
    FB([(400, 518), (432, 535), (466, 554), (500, 569), (528, 578)], w=[1.8, 2.4, 2.6, 2.4, 1.8], hgt=[0.6, 1.1, 1.3, 1.0, 0.5],
       ta=0.35, tb=0.4, lean=0.3, k=1.8, wend=0.8),
    FB([(446, 474), (474, 486), (500, 500), (522, 512)], w=[1.4, 1.9, 1.9, 1.4], hgt=[0.4, 0.8, 0.8, 0.4], ta=0.4, tb=0.4,
       lean=0.2, k=1.6, wend=0.8),
]

PX = LAP + HIP + SWAG + KNEE + SEC + HEM

# ------------------------------------------------------------------ 3D folds (sides / back / floor the photo hides)
# back of the gown: five broad falls fanning from the small of the back / hips down to the floor (uneven widths,
# heights and spacing), rounded cushions blended into the cloth
BACK = [
    FB(p3=[(-24.5, 30.5, 45), (-28, 33, 36), (-31, 35.5, 27), (-33, 35.5, 18)], w=[1.6, 2.2, 2.4, 2.2], hgt=[0.8, 1.4, 1.7, 1.3],
       ta=0.35, tb=0.4, lean=0.15, k=2.0, wend=0.8),
    FB(p3=[(-20, 31, 46), (-21, 35, 35), (-22.5, 38.5, 26), (-23.5, 37.5, 16)], w=[1.8, 2.4, 2.6, 2.4], hgt=[0.9, 1.6, 1.9, 1.4],
       ta=0.35, tb=0.4, lean=-0.1, k=2.0, wend=0.8),
    FB(p3=[(-16, 31, 44), (-15.5, 35.5, 35), (-15, 39, 26), (-14.5, 37.5, 16)], w=[1.4, 1.9, 2.1, 1.9], hgt=[0.7, 1.2, 1.4, 1.1],
       ta=0.4, tb=0.4, lean=0.1, k=1.8, wend=0.8),
    FB(p3=[(-12, 31, 42), (-9.5, 34.5, 34), (-7, 37.5, 26), (-5, 36.5, 17)], w=[1.7, 2.3, 2.5, 2.2], hgt=[0.8, 1.5, 1.8, 1.3],
       ta=0.35, tb=0.4, lean=-0.15, k=2.0, wend=0.8),
    FB(p3=[(-7, 30, 39), (-3, 31, 32), (0.5, 33, 25), (3, 33.5, 17)], w=[1.4, 2.0, 2.2, 1.9], hgt=[0.6, 1.2, 1.4, 1.0],
       ta=0.4, tb=0.4, lean=-0.1, k=1.8, wend=0.8),
]

# the hem flaring out on the floor toward the front-left (her right side): broad rolls sweeping out from the skirt
# foot and dying into the bowl floor (dish floor z ~7.6-8)
FLOOR = [
    FB(p3=[(-14, 0.5, 7.7), (-23, -2.5, 7.7), (-32, -6, 7.8), (-39, -10.5, 8.0), (-44, -15.5, 8.6)], w=[2.6, 2.8, 2.6, 2.3, 1.9],
       hgt=[1.6, 2.0, 1.8, 1.4, 0.8], ta=0.25, tb=0.45, lean=0.2, k=2.0, wend=0.8, floor=True),
    FB(p3=[(-22, 6, 7.8), (-30, 3.5, 7.8), (-37, 0.5, 7.9), (-43, -3, 8.4)], w=[2.4, 2.6, 2.3, 1.8], hgt=[1.6, 1.8, 1.4, 0.7],
       ta=0.3, tb=0.45, lean=0.2, k=2.0, wend=0.8, floor=True),
    FB(p3=[(-3, -3.5, 7.6), (-12, -7.5, 7.6), (-22, -11, 7.6), (-31, -14.5, 7.7), (-37, -19, 8.2)], w=[2.2, 2.4, 2.3, 2.0, 1.6],
       hgt=[1.2, 1.5, 1.4, 1.1, 0.6], ta=0.3, tb=0.45, lean=0.15, k=2.0, wend=0.8, floor=True),
]

# her right side: the long hem roll continues past the hip foot, sweeping left and up onto the bowl's left wall
# (photo px 220-330, 590-650), with a lower roll under it near the floor
SIDE = [
    FB(p3=[(-37.0, 11.5, 22.0), (-41.5, 13.0, 23.0), (-46, 14.0, 23.5), (-50, 13.5, 22.5), (-53, 11.0, 20.0)],
       w=[2.6, 3.0, 3.2, 3.0, 2.4], hgt=[1.6, 2.2, 2.4, 2.1, 1.2], t=[3.6, 4.8, 6.0, 6.4, 6.0], ta=0.25, tb=0.35, lean=0.3,
       k=2.6, wend=0.85, floor=True),
    FB(p3=[(-39, 5.0, 14.0), (-43.5, 6.0, 14.5), (-47.5, 6.0, 14.5), (-50.5, 4.5, 14.0)], w=[2.4, 2.8, 2.6, 2.0],
       hgt=[1.4, 1.9, 1.7, 0.9], t=[3.2, 4.0, 4.4, 4.2], ta=0.3, tb=0.45, lean=0.25, k=2.6, wend=0.85, floor=True),
]

D3 = BACK + FLOOR + SIDE


def _env(m, ta, tb):
    s = np.linspace(0, 1, m)
    e = np.minimum(np.clip(s / max(ta, 1e-6), 0, 1), np.clip((1 - s) / max(tb, 1e-6), 0, 1))
    return np.sin(e * math.pi / 2)


def _prof(v, m):
    """scalar or per-control-point list -> per-sample profile (smooth interpolation along the path)."""
    if np.ndim(v) == 0:
        return np.full(m, float(v))
    v = np.asarray(v, float)
    x = np.linspace(0, 1, len(v)); xi = np.linspace(0, 1, m)
    from scipy.interpolate import PchipInterpolator
    return PchipInterpolator(x, v)(xi)


def band_batch(P, N, sp):
    """eseg chain (k=0 inside the band) for one fold along surface polyline P with normals N.
    Section: a flattened ellipse (cushion) sitting on the surface -- crest `hgt` above it, half-width `w`;
    the ends fade by flattening (height -> 0) while staying broad (the fold dies into the cloth, no sausage tip)."""
    B = Batch()
    m = len(P)
    if m < 3:
        return B
    env = _env(m, sp['ta'], sp['tb'])
    T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
    side = np.cross(N, T); side /= np.linalg.norm(side, axis=1, keepdims=True) + 1e-12
    w = _prof(sp['w'], m) * (sp['wend'] + (1 - sp['wend']) * env)
    hh = _prof(sp['hgt'], m) * env ** 1.3
    if sp['t'] is not None:
        t = _prof(sp['t'], m) * (0.5 + 0.5 * env)
        t = np.maximum(t, hh * 0.75 + 0.3)
    else:
        t = hh * 0.92 + 0.3                   # centre just under the surface: full width where the fold meets it
    lean = _prof(sp['lean'], m)
    up = N + lean[:, None] * side
    up /= np.linalg.norm(up, axis=1, keepdims=True)
    if sp['sub']:
        C = P + N * (t - hh)[:, None]            # digs hh into the surface
    else:
        C = P + N * (hh - t + sp['off'])[:, None]
    C = C + side * (0.3 * lean * w)[:, None]
    for i in range(m - 1):
        B.eseg(C[i], C[i + 1], up[i] + up[i + 1], max(w[i], 0.35), max(w[i + 1], 0.35), max(t[i], 0.3), max(t[i + 1], 0.3), 0.0)
    return B


def blend_into(F, B, k, sub=False):
    """Evaluate batch B (hard union) in a sub-block and smooth-union / smooth-subtract it into F.G with radius k."""
    if len(B) == 0 or not np.isfinite(np.array([b[0] for b in B.bounds] + [b[1] for b in B.bounds])).all():
        return
    lo = np.min([b[0] for b in B.bounds], axis=0) - (k + 2.0 + 3 * F.h)
    hi = np.max([b[1] for b in B.bounds], axis=0) + (k + 2.0 + 3 * F.h)
    a = np.clip(np.floor((lo - F.lo) / F.h).astype(int), 0, F.shape)
    b = np.clip(np.ceil((hi - F.lo) / F.h).astype(int) + 1, 0, F.shape)
    if np.any(b <= a):
        return
    S = Field.__new__(Field); S.lo = F.lo + a * F.h; S.h = F.h; S.shape = tuple(int(v) for v in (b - a))
    S.G = np.full(S.shape, FAR, np.float32)
    S.apply(B, 'union', pad=k + 1.5)
    V = F.G[a[0]:b[0], a[1]:b[1], a[2]:b[2]]
    d = S.G
    if sub:
        d = -d
        hk = np.clip(k - np.abs(V - d), 0, None) / k
        V[...] = np.maximum(V, d) + hk * hk * k * 0.25
    else:
        hk = np.clip(k - np.abs(V - d), 0, None) / k
        V[...] = np.minimum(V, d) - hk * hk * k * 0.25


def smooth_path(P, N, step=0.5):
    L = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
    n = max(4, int(L / step) + 1)
    idx = np.linspace(0, len(P) - 1, n)
    Pi = np.stack([np.interp(idx, np.arange(len(P)), P[:, j]) for j in range(3)], 1)
    Ni = np.stack([np.interp(idx, np.arange(len(P)), N[:, j]) for j in range(3)], 1)
    # smooth normals along the path (no wobble from the surface relief)
    from scipy.ndimage import gaussian_filter1d
    Ni = gaussian_filter1d(Ni, 2.0, axis=0, mode='nearest')
    Ni /= np.linalg.norm(Ni, axis=1, keepdims=True)
    return Pi, Ni


HGAIN, DGAIN = 1.45, 1.3


def apply(F, G0, lo, h, only=None):
    """Add all folds to F (full field).  G0: base block (copy) at lo used for tracing / normals."""
    T = TXM.CamTex(TXM.ref_camera(), (0, 0, 1179, 1078), 1.0, G0, lo, h, full=False)
    adds, subs = [], []
    for sp in (PX + D3) if only is None else only:
        if sp['pix'] is not None:
            P = T.trace(sp['pix'], step=0.25)
            N = T.normals(P) if len(P) >= 4 else None
        elif sp.get('floor'):
            P = resample(catmull(np.asarray(sp['p3'], float), per=10), 120)
            N = np.tile([0.0, 0.0, 1.0], (len(P), 1))
        else:
            P = T.surf(sp['p3'], step=0.25)
            N = T.normals(P) if len(P) >= 4 else None
        if len(P) < 4 or N is None:
            continue
        ok = np.isfinite(P).all(1) & np.isfinite(N).all(1) & (np.linalg.norm(N, axis=1) > 0.5)
        P, N = P[ok], N[ok]
        if len(P) < 4:
            continue
        P, N = smooth_path(P, N)
        if not (np.isfinite(P).all() and np.isfinite(N).all()):
            continue
        sp = dict(sp)
        g = DGAIN if sp['sub'] else HGAIN
        sp['hgt'] = (np.asarray(sp['hgt'], float) * g).tolist() if np.ndim(sp['hgt']) else sp['hgt'] * g
        (subs if sp['sub'] else adds).append((band_batch(P, N, sp), sp['k']))
    for B, k in adds:
        blend_into(F, B, k)
    for B, k in subs:
        blend_into(F, B, k, sub=True)
