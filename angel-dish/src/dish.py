"""Drapery bowl (the angel's gown spread into an oval dish) -- round 2.

Built as ONE continuous sculpted surface instead of stacked tubes:
  * outer wall: polar wall about C=(2,-6) carrying a satin-fold displacement field D(phi, z).  The folds
    are level sets of a phase field: broad irregular S-bands that flow from the front-left, wrap into a
    clockwise whirlpool vortex at the front-right (eye ~ (32,-57,9.5)) and sweep up-right in arcs to the
    right rim; low diagonal folds on the back base.  Foot chamfered in 2.5 (45 deg) under everything.
  * rolled hem: a tilted ellipse swept along the rim with varying size / height / tilt (breaking outward
    at the front, curling inward as a wave crest at the right where it meets the right wing), with
    shallow longitudinal fold grooves; absent on the left (the left wing owns that wall + lip, contract
    C1) and at the back behind the wings (contract C3: low base wall the wing feathers blend into).
  * interior: height field (floor + concave inner wall) carrying the skirt-train folds (continuing the
    figure's hem toward the right), the front-left whirlpool of concentric rolling ridges, soft diagonal
    folds on the right inner wall.  Fine combed striations (harmonics of the fold phases) when F.h <= 0.3.
Coordinates: X right, Y away from viewer, Z up (design mm)."""
import math
import os
import numpy as np
import dish_geo as G
import dish_fold as DF
import dish_k as K

FLOOR = 8.0
FINE_H = 0.3


# ------------------------------------------------------------------ rolled lip tables
# Three overlapping hem rolls (each a tilted ellipse swept along phi):
#   B  the front rim: the top of the big front band, emerging low under the tongue at the front-left, rising to
#      the rim crest across the front and arching down at the right of the scroll into its outer arm;
#   A  the "tongue": continuation of the left wing's rolled lip (contract C1 handoff, crest ~21.5 at x -40..-32),
#      lying over band B and ending in a rounded tip at x ~ -20;
#   R  the right rim wave crest: rises from behind B's arch (notch between them), curls inward over the bowl
#      where it meets the right wing's lower feathers, fades out at the back-right.
# rows: az, on, lrc (centre offset beyond the wall-top radius), crest z, la (radial semi), lb (vertical semi), tilt deg
#   tilt < 0: the roll's outer side droops (rolls over outward);  tilt > 0 would lift the outer side.
_LIP_B = [
    (-156, 0.0, -1.5, 10.0, 3.0, 2.8, -14),
    (-146, 0.35, -1.2, 12.5, 4.0, 3.4, -20),
    (-138, 0.75, -1.0, 14.8, 4.8, 3.8, -26),
    (-130, 1.0, -0.9, 16.8, 5.4, 4.1, -30),
    (-122, 1.0, -0.6, 19.4, 5.9, 4.3, -34),
    (-114, 1.0, 0.0, 21.8, 6.2, 4.3, -38),
    (-102, 1.0, 1.0, 23.4, 6.3, 4.4, -40),
    (-90, 1.0, 1.2, 24.5, 6.4, 4.4, -40),
    (-80, 1.0, 0.6, 25.6, 6.3, 4.4, -38),
    (-70, 1.0, -0.2, 26.9, 6.2, 4.4, -34),
    (-62, 1.0, -0.8, 27.4, 6.0, 4.3, -30),
    (-56, 0.9, -1.4, 26.8, 5.6, 4.2, -26),
    (-51, 0.62, -2.0, 25.5, 5.0, 4.0, -20),
    (-46, 0.28, -2.6, 23.0, 4.4, 3.7, -14),
    (-41, 0.0, -3.2, 20.0, 3.6, 3.4, -8),
]
_LIP_R = [
    (-48, 0.0, -5.6, 15.0, 3.0, 3.0, 0),
    (-42, 0.4, -4.8, 18.5, 3.6, 3.2, -4),
    (-36, 0.85, -4.3, 23.0, 4.3, 3.5, -8),
    (-30, 1.0, -4.1, 26.6, 4.8, 3.7, -12),
    (-23, 1.0, -4.3, 29.2, 5.1, 3.9, -18),
    (-14, 1.0, -4.8, 31.0, 5.4, 4.1, -24),
    (-3, 1.0, -5.0, 31.6, 5.4, 4.2, -28),
    (8, 1.0, -4.7, 30.4, 5.0, 4.0, -24),
    (19, 0.7, -4.0, 27.4, 4.2, 3.6, -12),
    (30, 0.0, -3.5, 21.0, 3.0, 3.0, 0),
    (40, 0.0, -3.5, 18.0, 3.0, 3.0, 0),
]
_A_END, _A_CAP = -128.0, 12.0          # tongue tip: azimuth where the round cap starts, cap radius (design units)
_LIP_A = [
    (-176, 0.0, -5.0, 18.0, 2.5, 2.5, -10),
    (-163, 0.0, -3.5, 21.0, 3.0, 3.0, -12),
    (-152, 0.5, -1.0, 22.6, 4.0, 3.8, -14),
    (-144, 0.95, 0.4, 22.2, 4.5, 4.3, -16),
    (-138, 1.0, 1.0, 21.9, 4.9, 4.5, -18),
    (-131, 1.0, 1.5, 21.6, 5.3, 4.6, -21),
    (-125, 1.0, 1.4, 21.0, 5.3, 4.5, -24),
    (-119, 1.0, 0.9, 20.2, 5.0, 4.3, -27),
    (-112, 1.0, 0.2, 19.2, 4.6, 4.0, -30),
]
# wall top where no hem roll covers it: front low (the rolls make the rim), back = low base wall the wing
# feathers blend into, left inside the wing, notch between the front band's arch and the right crest
_ZWN = [(-178, 26.0), (-168, 26.5), (-160, 25.0), (-152, 22.0), (-144, 18.0), (-120, 16.0), (-90, 16.0), (-68, 16.5), (-60, 25.5),
        (-54, 25.8), (-48, 24.5), (-43, 21.0), (-39.5, 18.0), (-35, 18.5), (-27, 24.0),
        (-10, 28.0), (5, 28.0), (20, 25.5), (32, 24.5), (45, 24.0), (60, 24.5), (75, 25.0), (90, 25.0), (105, 23.5),
        (120, 20.0), (135, 18.5), (150, 20.0), (170, 21.5)]
# how much the drapery folds are tucked in at the very top of the wall
_TUCK = [(-170, 0.4), (-140, 0.6), (-110, 0.7), (-75, 0.7), (-60, 0.55), (-45, 0.4), (-30, 0.3), (20, 0.3), (40, 0.9), (120, 0.9),
         (160, 0.6)]


def _lip(rows, ph0, ph1, ph2, wob=1.0):
    L = np.array(rows, float)
    az = L[:, 0]
    # zero rows far away so the periodic spline stays 0 outside the segment
    ext = [r for r in rows]
    lo, hi = az.min(), az.max()
    for q in np.arange(-180.0, 180.0, 10.0):
        if q < lo - 8 or q > hi + 8:
            ext.append((q, 0.0, L[0, 2] if q < lo else L[-1, 2], L[0, 3] if q < lo else L[-1, 3], 3.0, 3.0, 0.0))
    L = np.array(ext, float)
    a_ = L[:, 0]
    on = np.clip(G.periodic(a_, L[:, 1]), 0, 1)
    lrc = G.periodic(a_, L[:, 2]); crest = G.periodic(a_, L[:, 3])
    la = G.periodic(a_, L[:, 4]); lb = G.periodic(a_, L[:, 5]); tilt = np.radians(G.periodic(a_, L[:, 6]))
    ph = G.PH
    a = np.radians(ph)
    crest = crest + wob * on * (0.6 * np.sin(a * 7.0 + ph0) + 0.35 * np.sin(a * 13.0 + ph1) + 0.18 * np.sin(a * 23.0 + ph2))
    sw_ = 1.0 + wob * (0.12 * np.sin(a * 5.0 + ph1) + 0.07 * np.sin(a * 11.0 + ph2) + 0.05 * np.sin(a * 19.0 + ph0))
    la = la * sw_; lb = lb * (1.0 + 0.08 * np.sin(a * 6.0 + ph2) + 0.05 * np.sin(a * 15.0 + ph0))
    tilt = tilt + np.radians(5.0) * np.sin(a * 9.0 + ph1) * on
    lzc = crest - np.sqrt((la * np.sin(tilt)) ** 2 + (lb * np.cos(tilt)) ** 2) - (1 - on) * 2.5
    g1 = 0.75 + 0.25 * np.sin(a * 4.0 + ph0) + 0.10 * np.sin(a * 10.0)
    g2 = 1.45 + 0.22 * np.sin(a * 6.0 + ph1)
    sw = np.clip(0.3 + 0.6 * np.sin(a * 3.0 + ph2) + 0.25 * np.sin(a * 8.0 + ph0), 0.0, 1.0) * on * 0.6
    lf = np.zeros_like(on)
    return np.stack([on, lrc, lzc, la, lb, tilt, g1, g2, sw, lf])


def lip_tables():
    ph = G.PH
    B = _lip(_LIP_B, 0.6, 2.0, 1.0)
    B[9] = G.periodic([-150, -100, -78, -66, -52, -40, -30, 0, 60, 120], [0.0, 0.0, 0.15, 0.4, 0.5, 0.45, 0.0, 0.0, 0.0, 0.0]) * B[0]
    A = _lip(_LIP_A, 2.4, 0.3, 1.7, wob=0.5)
    # rounded tongue tip: past _A_END the roll is cut by a quarter circle in (arc length, section)
    x = np.clip((ph - _A_END) * math.radians(1.0) * 50.0, 0.0, None)
    off = np.where(x < _A_CAP, _A_CAP - np.sqrt(np.clip(_A_CAP ** 2 - x ** 2, 0, None)), _A_CAP + (x - _A_CAP) * 3.0)
    capon = np.clip(1.0 - 0.7 * off / 6.0, 0.0, 1.0) ** 0.8
    A[0] = np.where(ph > _A_END, np.minimum(A[0], capon), A[0])
    A[0] = np.where(ph > -100, 0.0, A[0])
    R = _lip(_LIP_R, 1.3, 2.6, 0.2)
    a_ = np.radians(ph)
    R[6] = 0.55 + 0.12 * np.sin(a_ * 5.0 + 0.4)          # groove angles on the top / outer face of the crest
    R[7] = 1.35 + 0.15 * np.sin(a_ * 7.0 + 1.9)
    R[8] = np.clip(0.75 + 0.3 * np.sin(a_ * 4.0 + 2.6), 0.3, 1.0) * R[0]
    # the tongue and the right crest never overlap: share one table
    AR = np.where(ph[None] < -80, A, R)
    zwn = G.periodic(*np.array(_ZWN, float).T)
    # back wall (under / behind the wings): no dead-flat shelf -- the crest undulates with the drapery and
    # rises a little where the right wing's lower feathers come down onto it, so the wing lands in folds
    wbk = DF.smoothstep(ph, 32.0, 50.0) * (1 - DF.smoothstep(ph, 160.0, 176.0))
    und = 1.3 * np.sin(np.radians(ph) * 5.0 + 0.8) + 0.7 * np.sin(np.radians(ph) * 9.0 + 2.1) + 0.3 * np.sin(np.radians(ph) * 14.0)
    lift = 2.6 * DF.smoothstep(ph, 30.0, 45.0) * (1 - DF.smoothstep(ph, 52.0, 66.0))
    zwn = zwn + wbk * und + lift
    ZW = zwn.copy()
    from scipy.ndimage import gaussian_filter1d as _g1
    for T in (B, AR):
        on = np.clip(_g1(T[0], 45.0, mode='wrap'), 0, 1)     # gentle: a roll ending must not step the wall top
        ZW = np.maximum(ZW, on * (_g1(T[2], 45.0, mode='wrap') + 0.45 * T[4]) + (1 - on) * zwn)
    # soften the joins between rolls (no kinks in the wall top)
    from scipy.ndimage import gaussian_filter1d
    ZW = gaussian_filter1d(ZW, 18.0, mode='wrap')
    LIPS = np.stack([B, AR])
    if os.environ.get('DISH_NOLIP'):
        LIPS[:, 0] = 0.0
    return LIPS, ZW


def zw_flare(ZW):
    """heavily smoothed wall top used for the wall's flare / fold hold (so a hem roll ending never steps the wall)."""
    from scipy.ndimage import gaussian_filter1d
    return gaussian_filter1d(ZW, 70.0, mode='wrap')


def lip_on(LIPS):
    return LIPS[:, 0].max(0)


# ------------------------------------------------------------------ outer wall displacement table
DZ0, DZS, NZ = -1.0, 0.1, 471          # z from -1 to 46


def wall_table(ZW, fine, ONZ=None):
    if ONZ is None:
        ONZ = lip_on(lip_tables()[0])
    Z = DZ0 + DZS * np.arange(NZ)
    S = G.ST
    SS, ZZ = np.meshgrid(S, Z, indexing='ij')                 # (NT, NZ)
    PHI = np.repeat(G.PH[:, None], NZ, 1)
    zw = zw_flare(ZW)[:, None]
    # front + right drapery (s ~ -58 .. 130)
    wf = DF.smoothstep(SS, -96, -72) * (1 - DF.smoothstep(SS, 118, 136))
    Df, Dbody, Dfold, Aloc = DF.front_disp(SS, ZZ, fine=fine, parts=True)
    onz = ONZ[:, None]
    # under the hem rolls the top band holds its crest, so band + roll read as one fat rolled towel edge
    wtop = DF.smoothstep(ZZ, zw - 7.5, zw - 3.5) * onz
    Df = Df + np.maximum(Aloc - Dfold, 0.0) * wtop
    # back base wall: low diagonal folds continuing the front drapery
    wb = DF.smoothstep(SS, 120, 138) * (1 - DF.smoothstep(SS, 262, 280))
    Db = DF.back_disp(SS, ZZ, fine=fine)
    D = Df * wf + Db * wb
    # front-left base under the end of the wing lip: a few bunched drapery lobes hanging over the foot
    for (sc, zc, ws, wz, amp) in ((-63.0, 7.0, 2.4, 7.0, 2.6), (-58.0, 5.5, 2.7, 6.5, 3.2), (-52.5, 8.0, 2.3, 7.0, 2.4), (-47.0, 6.0, 2.0, 6.0, 1.6)):
        D = D + amp * np.exp(-((SS - sc) / ws) ** 2 - ((ZZ - zc) / wz) ** 2)
    # the hem rides on the vortex body, while the fold bands mostly pass beneath it
    DL = (np.clip(Dbody, -1.0, 5.0) + 0.3 * Dfold) * wf + 0.3 * Db * wb
    # folds tuck under the hem / round over the low top (but keep most of their depth right up to it)
    fo = G.periodic([-150, -130, -90, -66, -50, -30, -10, 10, 40, 120], [3.5, 7.5, 9.0, 8.5, 7.5, 8.5, 7.5, 5.0, 3.5, 3.5])[:, None]
    tk = G.periodic(*np.array(_TUCK, float).T)[:, None]
    D = D * (1 - tk * DF.smoothstep(ZZ, zw - 3.0 - (fo - 3.0) * (1 - onz) * 0.0, zw + 1.5))
    # printability: slightly recessed foot and no outer-wall undercut much steeper than 45 deg near the base /
    # ~50 deg above.  Soft envelope marched up each column, then the correction is smoothed in (s, z) so the
    # limiter cannot leave planar facets or column streaks.
    base = G.R0T[:, None] + G.FLT[:, None] * np.clip(ZZ / np.maximum(zw, 1.0), 0, 1.3) ** 1.6
    cd = G.periodic([-150, -110, -60, -30, 30, 120], [1.0, 1.1, 1.3, 1.1, 1.0, 1.0])[:, None]
    RW0 = base + D - np.maximum(0.0, cd - 0.8 * ZZ)
    RW = RW0.copy()
    k0 = int(round((0.0 - DZ0) / DZS))
    ks = 0.35
    # the whirlpool scroll keeps its sculpted undercuts (small, local): limit relaxed to ~62 deg there
    _, _, _, rv = DF.front_phase(SS, ZZ)
    relax = (1 - DF.smoothstep(rv, 9.0, 16.0)) * wf
    for k in range(k0 + 1, NZ):
        slope = (1.0 if Z[k] < 4.0 else 1.28) + 0.3 * relax[:, k]
        lim = RW[:, k - 1] + slope * DZS
        RW[:, k] = -ks * np.logaddexp(-RW[:, k] / ks, -lim / ks)
    corr = RW0 - RW
    from scipy.ndimage import gaussian_filter, maximum_filter
    corr = gaussian_filter(corr, sigma=(3.0, 2.0), mode=('wrap', 'nearest'))
    RW = RW0 - corr
    D = RW - base
    # normalisation (slope of the displacement along the wall)
    ds = (G.R0T * math.radians(360.0 / G.NT))[:, None]
    gs = np.gradient(D, axis=0) / ds
    gz = np.gradient(D, DZS, axis=1)
    NTab = 1.0 / np.sqrt(1.0 + gs * gs + gz * gz)
    return D, DL, NTab


# ------------------------------------------------------------------ interior height field
WTT = G.periodic([-150, -120, -90, -60, -20, 10, 40, 90, 140, 170], [3.5, 4.2, 4.5, 4.6, 5.0, 5.0, 5.5, 5.5, 4.0, 3.0])
RINT = G.R0T + G.FLT - WTT           # radius of the inner edge of the wall top


def heightfield(F, ZW, fine):
    xs, ys, _ = F.coords()
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    ph, rho = G.polar(X, Y)
    Rtop = G.R0(ph) + G.FL(ph)
    WT = G.at(WTT, ph)
    DW = G.at(G.periodic([-150, -110, -80, -50, -20, 10, 40, 70, 110, 140, 170], [17, 15, 14, 15, 17, 16, 14, 13, 12, 14, 18]), ph)
    Rin = Rtop - WT
    zwin = G.at(ZW, ph) + 0.6
    u = np.clip((Rin - rho) / DW, 0, 1)
    v = 1 - u
    g = 0.65 * (1 - np.sqrt(np.clip(1 - v * v, 0, 1))) + 0.35 * v ** 2.2
    H0 = FLOOR + (zwin - FLOOR) * g
    H0 = np.where(rho > Rin, zwin + (rho - Rin) * 2.0, H0)
    gx, gy = np.gradient(H0, F.h)
    slope = np.sqrt(1 + gx * gx + gy * gy)
    Fv = DF.interior_folds(X, Y, ph, rho, u, fine)
    inside = DF.smoothstep(Rin - rho, -1.0, 1.5)
    return H0 + Fv * np.minimum(slope, 3.5) * inside


def component(F):
    fine = F.h <= FINE_H
    LIP, ZW = lip_tables()
    D, DL, NTab = wall_table(ZW, fine, lip_on(LIP))
    hf = heightfield(F, ZW, fine)
    K.body(F, G.C[0], G.C[1], G.R0T, G.FLT, ZW, LIP, D, DL, NTab, DZ0, DZS, hf, RINT, kt=1.0, cham=0.0, fine=fine,
           nstri=52.0, astri=0.016, kl=2.6, wedge=0 if os.environ.get('DISH_NOWEDGE') else 1, ZWF=zw_flare(ZW))
    _fill_slits(F)
    return F


def _fill_slits(F, box=((10.0, -66.0, 0.0), (92.0, 12.0, 34.0))):
    """close the odd hair-thin crease pocket that a hem support face or two touching fold crests seal off
    (an enclosed void would be an internal shell in the print): any empty voxel cluster inside the wall
    region that does not reach the box border is set solid."""
    from scipy import ndimage
    lo = np.array(F.lo, float); h = F.h
    sh = np.array(F.G.shape)
    i0 = np.clip(np.floor((np.array(box[0]) - lo) / h).astype(int), 0, sh - 1)
    i1 = np.clip(np.ceil((np.array(box[1]) - lo) / h).astype(int) + 1, 1, sh)
    if np.any(i1 - i0 < 3):
        return
    sub = F.G[i0[0]:i1[0], i0[1]:i1[1], i0[2]:i1[2]]
    empty = sub >= 0
    lab, n = ndimage.label(empty)
    if n <= 1:
        return
    border = np.unique(np.concatenate([lab[0].ravel(), lab[-1].ravel(), lab[:, 0].ravel(), lab[:, -1].ravel(),
                                       lab[:, :, 0].ravel(), lab[:, :, -1].ravel()]))
    sizes = ndimage.sum(empty, lab, np.arange(1, n + 1))
    inner = np.setdiff1d(np.arange(1, n + 1)[sizes < 4000], border)
    if len(inner):
        m = np.isin(lab, inner)
        sub[m] = -0.5 * h
