"""Carved feathered wings (v3, round 2).

Each wing is a solid curved sheet (generalised cylinder, ~isometric (u,v) chart: u = arc length along a floor
curve, v = z) whose two faces carry a bas-relief of individually authored, overlapping feathers (see
wings_core.py).  The wing outline is made by the feathers themselves (scalloped secondary tips, free primary
tip), the leading edge is a broad puffy wrist dome covered in tiny marginal coverts, covert tiers follow the
leading edge and grow in size (lesser -> median -> greater), flight feathers are broad separate blades that
fan toward the tip with stepped overlaps, rachis and (fine grids only) barb striations.
Layout curves are traced in reference-photo pixels and mapped onto the sheet (pix2uv) at build time."""
import math, os
import numpy as np
from scipy.spatial import cKDTree
from sdf import Batch, catmull, resample
from wings_core import Sheet, Relief, fill, poly_sdf, unit, smoothstep

DETAIL_H = 0.3          # barbs only when the grid is at least this fine


# ----------------------------------------------------------------------------- helpers
def smooth_poly(pts, n=None, per=10, closed=False):
    c = catmull(np.asarray(pts, float), per=per, closed=closed)
    return resample(c, n) if n else c


def _fair(P, step=0.5, sig=1.0):
    """Resample a polyline uniformly and smooth it (removes pixel-trace kinks); end points kept."""
    from scipy.ndimage import gaussian_filter1d
    S = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
    n = max(int(S[-1] / step), 4)
    Q = resample(P, n)
    Qs = np.stack([gaussian_filter1d(Q[:, 0], sig / step, mode='nearest'), gaussian_filter1d(Q[:, 1], sig / step, mode='nearest')], 1)
    Qs[0] = Q[0]; Qs[-1] = Q[-1]
    return Qs


def arclen(P):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])


def at(P, s):
    """Point(s) at arc length s along polyline P (clamped)."""
    S = arclen(P)
    s = np.clip(s, 0, S[-1])
    return np.stack([np.interp(s, S, P[:, 0]), np.interp(s, S, P[:, 1])], -1)


def rot(d, deg):
    a = math.radians(deg)
    return np.array([d[0] * math.cos(a) - d[1] * math.sin(a), d[0] * math.sin(a) + d[1] * math.cos(a)])


def dist_to(rel, curve):
    uu, vv = rel.grid()
    c = resample(curve, max(int(arclen(curve)[-1] / 0.15), 10))
    d, _ = cKDTree(c).query(np.stack([uu.ravel(), vv.ravel()], 1), workers=-1)
    return d.reshape(uu.shape), uu, vv


def ruled(A, B, a, t):
    """Point at parameter a (0..1, arc-length fraction on each curve) and t (0: A, 1: B)."""
    pa = at(A, a * arclen(A)[-1]); pb = at(B, a * arclen(B)[-1])
    return (1 - t) * pa + t * pb


def tiers(rel, A, B, rows, rng, faces=('f', 'b'), hb=0.8, a_rng=(0.0, 1.0), dirfun=None, barb=0.09, cover=False):
    """Covert tiers between curve A (upper, leading-edge side) and B (lower boundary of the covert zone).
    rows: list of dict(t=, w=, L=, h0=, h1=, sp=) ordered from A toward B.  Feather tips sit on the t-line,
    axes point from A toward B (optionally bent by dirfun), sizes scale with the local zone depth."""
    La = arclen(A)[-1]
    for k, r in enumerate(rows):
        # sample the row line densely to get its length
        aa = np.linspace(a_rng[0], a_rng[1], 300)
        line = np.array([ruled(A, B, x, r['t']) for x in aa])
        S = arclen(line)
        sp = r['sp']
        n = max(int(S[-1] / sp), 1)
        pos = (np.arange(n) + 0.5 + (0.5 if k % 2 else 0.0) * r.get('stagger', 1.0)) * S[-1] / n
        pos = pos + rng.uniform(-0.22, 0.22, n) * sp
        for s in pos:
            if s < 0 or s > S[-1] or rng.random() < r.get('skip', 0.0):
                continue
            a = np.interp(s, S, aa)
            pa = ruled(A, B, a, 0.0); pb = ruled(A, B, a, 1.0)
            tip = at(line, s) + unit(pb - pa) * rng.normal(0, r.get('tj', 0.03)) * np.linalg.norm(pb - pa)
            depth = np.linalg.norm(pb - pa)
            d = unit(pb - pa)
            if dirfun is not None:
                d = dirfun(a, r['t'], d)
            d = rot(d, rng.normal(0, r.get('aj', 5.0) * 0.5))
            scl = np.clip(depth / r.get('D0', 26.0), r.get('smin', 0.5), 1.0)
            if depth * (1.0 - r['t']) < 1.2 and r['t'] < 0.99 or depth < 5.0:
                continue
            offk = r.get('off', 0.0) * float(np.clip((depth - 4.0) / 10.0, 0.15, 1.0))
            j = 1 + float(np.clip(0.12 * rng.standard_normal(), -0.22, 0.22))
            w = r['w'] * (0.75 + 0.25 * scl) * j
            L = r['L'] * scl * (1 + float(np.clip(0.12 * rng.standard_normal(), -0.22, 0.22)))
            L = max(L, 2.2 * w)
            base = tip - d * L
            rel.quill(base, tip, w, h0=r['h0'], h1=r['h1'] * (1 + 0.08 * rng.standard_normal()), faces=faces, hb=hb,
                      off=offk + 0.05 * rng.standard_normal(),
                      R=r.get('R', 0.55), cam=r.get('cam', 0.3), bend=rng.normal(0, 0.06) * L * 0.2,
                      wb=r.get('wb', 0.5), fm=r.get('fm', 0.58), p=r.get('p', 2.2), asym=rng.normal(0, 0.04),
                      tilt=rng.normal(0, 0.08) + r.get('tilt', 0.0), rachis=r.get('rachis', 0.0) * (w > 1.7),
                      barb=barb if w >= 1.7 else 0.0, barb_p=0.7, barb_ang=rng.uniform(24, 34), cover=cover,
                      ramp=r.get('ramp', 1.4), nose=r.get('nose', 0.0), bpow=1.3, bsplit=1.0)


# ----------------------------------------------------------------------------- right wing
# viewer's right = her left wing.  u = arc length along the base curve (u~13 at x=-9), v = z.
R_BASE = [(-22, 33), (-9, 32), (6, 35), (24, 40), (42, 39.5), (60, 29), (73, 15), (80, 1), (84, -12)]
R_UR = (0.0, 132.0); R_VR = (0.0, 118.0)

# outer contour in the reference photo (root behind the hair -> peak -> outer edge -> tip)
R_LE_PX = [(501, 268), (500, 240), (501, 222), (505, 184), (512, 153), (521, 126), (530, 105), (540, 88), (555, 64),
           (572, 53), (592, 48), (617, 46), (640, 48), (660, 53), (690, 66), (720, 86), (745, 110), (770, 140), (795, 175), (812, 202), (830, 240), (847, 278),
           (861, 298), (874, 316), (888, 334), (902, 352), (917, 375), (934, 400), (955, 425), (980, 450), (1008, 475),
           (1040, 500), (1076, 523), (1105, 542), (1127, 555), (1139, 566)]
R_ARCH_END = 22            # index in R_LE_PX: end of the wrist arch (dome ends, primaries form the edge)
# lower boundary of the covert zone (greater-covert tips), photo pixels
R_CB_PX = [(503, 372), (530, 380), (562, 376), (600, 362), (650, 349), (705, 360), (760, 368), (800, 352),
           (836, 334), (866, 312), (884, 296)]
# window-top scallop line (secondary tips over the see-through gap), photo pixels
R_WIN_PX = [(497, 437), (517, 440), (538, 442), (559, 446), (580, 451), (600, 456), (613, 463)]


def r_bow(u, v):
    # top of the wing rolls toward the viewer (concave face); the lower part flares back toward the base;
    # the inner end bends forward onto her left shoulder blade (wing root, C4)
    rootb = 5.5 * smoothstep((13.0 - u) / 8.5) * smoothstep((v - 44) / 8) * smoothstep((88 - v) / 8)
    return (0.0030 * np.maximum(v - 58, 0) ** 2 - 0.0065 * np.maximum(26 - v, 0) ** 2 * smoothstep((u - 30) / 8)
            + rootb)


def drape_rows(rel, A, B, rows, rng, faces=('f', 'b'), tb=0.5, dirfun=None, a_rng=(0.0, 1.0), rev=False, minD=4.0,
               tsign=1.0, barb=0.1):
    """Covert rows between curve A (leading-edge side) and B (greater-covert tip line), painted bottom-up (greater
    first, marginal last) with the drape engine, so every row's rounded tips lie ON the row below with a real step.
    rows: dicts ordered from the edge toward B: t (tip line, fraction A->B), w (half width), T (thickness), D0, ov
    (total length / visible length).  Within a row feathers are painted from the tip end toward the root (rev=False)
    so they overlap like cards.  Sizes, spacing, angle, tip position and shape all jitter; feathers are now and then
    skipped or doubled."""
    tprev = [rows[0]['t'] - 0.06] + [r['t'] for r in rows[:-1]]
    for k in reversed(range(len(rows))):
        r = rows[k]
        aa = np.linspace(a_rng[0], a_rng[1], 300)
        line = np.array([ruled(A, B, x, r['t']) for x in aa])
        S = arclen(line)
        sp = r['sp']
        n = max(int(S[-1] / sp), 1)
        pos = (np.arange(n) + 0.5 + 0.5 * (k % 2)) * S[-1] / n + rng.uniform(-0.15, 0.15, n) * sp
        extra = np.array([q + sp * rng.uniform(0.4, 0.6) for q in pos if rng.random() < r.get('dbl', 0.03)])
        pos = np.sort(np.concatenate([pos, extra])) if len(extra) else np.sort(pos)
        if not rev:
            pos = pos[::-1]
        for s in pos:
            if s < 0 or s > S[-1] or rng.random() < r.get('skip', 0.02):
                continue
            a = np.interp(s, S, aa)
            if a > r.get('amax', 2.0) + rng.uniform(-0.02, 0.02):
                continue
            pa = ruled(A, B, a, 0.0); pb = ruled(A, B, a, 1.0)
            depth = float(np.linalg.norm(pb - pa))
            if depth < minD:
                continue
            d = unit(pb - pa)
            if dirfun is not None:
                d = dirfun(a, r['t'], d)
            d = rot(d, rng.normal(0, r.get('aj', 3.5)))
            tip = at(line, s) + unit(pb - pa) * rng.normal(0, r.get('tj', 0.015)) * depth
            scl = float(np.clip(depth / r['D0'], r.get('smin', 0.5), 1.0))
            w = r['w'] * (0.7 + 0.3 * scl) * (1 + float(np.clip(0.09 * rng.standard_normal(), -0.18, 0.18)))
            vis = max((r['t'] - tprev[k]) * depth, 0.9 * w)
            L = max(vis * r.get('ov', 1.9) + rng.normal(0, 0.12 * vis), 2.3 * w)
            base = tip - d * L
            T = r['T'] * (1 + 0.1 * rng.standard_normal())
            rel.drape(base, tip, w, T=T, faces=faces, Tb=T * tb, bend=rng.normal(0, 0.05) * L,
                      wb=0.55, fm=float(np.clip(1 - r.get('tipk', 1.15) * w / L + rng.normal(0, 0.03), 0.45, 0.8)),
                      p=float(np.clip(rng.normal(r.get('p', 2.3), 0.15), 1.8, 2.8)), asym=rng.normal(0, 0.05),
                      R=r.get('R', 0.6 + 0.1 * w), cross=r.get('cross', 0.3), crown=0.15,
                      tilt=tsign * r.get('tilt', 0.1) * (1 + 0.3 * rng.standard_normal()), ramp=r.get('ramp', 0.5),
                      blur=r.get('blur', 0.9), cav=r.get('cav', 0.1), cav_w=0.5,
                      rachis=r.get('rachis', 0.0) * (w > 1.6), rgroove=r.get('rgroove', 0.0) * (w > 1.6), rw=0.18,
                      barb=barb if w >= 1.6 else 0.0, barb_p=0.7, barb_ang=rng.uniform(22, 32))


def rows_spec(scale=1.0, D0=30.0, ts=None, ws=None, Ts=None, sps=1.45, fuzz=True, tilt=0.12):
    """Covert row table (edge -> greater).  ts: tip lines; ws: half widths; Ts: thickness."""
    R = []
    if fuzz:
        for t, w, T in [(-0.055, 0.85, 0.22), (-0.025, 0.95, 0.28)]:
            R.append(dict(t=t, w=w * scale, T=T, sp=1.35 * w * scale, D0=D0, ov=2.6, aj=12, tilt=0.03, R=0.35,
                          cross=0.35, cav=0.04, smin=0.6, tj=0.012, p=2.2))
    n = len(ts)
    for i, (t, w, T) in enumerate(zip(ts, ws, Ts)):
        gr = i == n - 1
        R.append(dict(t=t, w=w * scale, T=T, sp=sps * w * scale, D0=D0, ov=1.75 if not gr else 1.6,
                      aj=4.0 if w < 1.8 else 3.0, tilt=tilt * w / 2.0, cross=0.38, cav=0.03 + 0.02 * (w > 1.8),
                      rachis=0.07 if w > 1.8 else 0.0, rgroove=0.05 if w > 1.8 else 0.0, smin=0.5,
                      p=2.1 if gr else 2.35, tipk=1.3 if gr else 1.15, tj=0.012 + 0.008 * (i > 1)))
    return R


def build_right(F):
    from wings_dbg import pix2uv
    detail = F.h <= DETAIL_H
    S = Sheet(R_BASE, front_xy=(10, -120), bow=r_bow)
    hr = 0.15 if detail else 0.2
    rel = Relief(R_UR, R_VR, hr=hr, detail=detail, seed=21, drape=True)
    rng = np.random.default_rng(5)
    P2 = lambda px: pix2uv(S, R_UR, R_VR, px)
    LE = _fair(smooth_poly(P2(R_LE_PX), per=12), 0.4, 0.8)
    LEa = _fair(smooth_poly(P2(R_LE_PX[:R_ARCH_END + 1]), per=12), 0.4, 0.8)
    CB = smooth_poly(P2(R_CB_PX), per=8)
    WIN = P2(R_WIN_PX)
    tipP = LE[-1]
    # ---- membrane (guarantees a closed solid inside; feathers make the real edge).  Below the tip the thick
    # rounded tip lobe runs straight down into the dish rim (no notch)
    # rounded capsule end of the free tip (radius ~2.6): the outline wraps a circle instead of a pointed beak
    tng_t = unit(LE[-1] - LE[-8]); nrm_t = np.array([tng_t[1], -tng_t[0]])        # nrm_t points down/out
    rc = 2.4
    Sle = arclen(LE)
    le_in = LE[Sle < Sle[-1] - rc]
    tipC = le_in[-1] + nrm_t * rc
    a0 = math.atan2(-nrm_t[1], -nrm_t[0]); a1 = a0 - math.pi
    arc = tipC[None] + rc * np.stack([np.cos(np.linspace(a0, a1, 12)), np.sin(np.linspace(a0, a1, 12))], 1)
    le_in = np.vstack([le_in, arc[1:]])
    winm = WIN[::-1] + np.array([0.0, 2.6])
    tipb = tipC[None] + np.array([(-1.3, -3.4), (-2.0, -5.6), (-3.4, -8.2), (-6.0, -11.0), (-11.0, -13.0)])
    low = np.vstack([tipb, [(106.0, 22.0), (103.0, 10.0), (101.0, 0.0), (39.5, 0.0), (38, 10),
                            (34.5, 28), (32.0, 37.5)], winm[winm[:, 0] < 30.5],
                     [(9.0, winm[-1][1] + 0.5), (4.0, 53.0), (1.5, 60.0), (1.5, 70.0), (4.5, 76.5)]])
    memb = np.vstack([le_in, low])
    rel.membrane(memb, h=0.3)
    # ---- body: broad rolled leading edge (a smooth thick dome the marginal coverts ride on), thick tip lobe,
    # flared foot
    dLE, uu, vv = dist_to(rel, LE)
    arch_w = np.interp(uu, [0, 20, 40, 60, 72, 85, 132], [8.5, 11.0, 11.5, 10.0, 7.0, 4.5, 4.0])
    fadeu = np.interp(uu, [0, 60, 72, 90, 132], [1, 1, 0.75, 0.3, 0.2])
    rim = np.clip(1 - (dLE / arch_w) ** 2, 0, 1) ** 1.4 * fadeu
    lead = np.exp(-dLE / 12.0)
    foot = np.where(vv < 5.5, 5.5 - np.sqrt(np.clip(5.5 ** 2 - (5.5 - vv) ** 2, 0, None)), 0) * smoothstep((uu - 38) / 6)
    dtip = np.hypot(uu - (tipP[0] - 3.2), vv - (tipP[1] - 3.6))
    lobe = np.exp(-(dtip / 7.5) ** 2) + 0.7 * np.exp(-(dtip / 4.0) ** 2)
    # the lower front of the tip lobe flares down onto the dish rim (fillet, no notch under the tip)
    tfoot = smoothstep((40.0 - vv) / 9.0) * np.exp(-((uu - (tipP[0] - 8.0)) / 10.0) ** 2) * smoothstep((vv - 18.0) / 9.0)
    rel.add_body('f', lambda u, v: 0.95 + 0.6 * lead + 1.5 * rim + 1.5 * lobe + 2.2 * tfoot)
    rel.add_body('b', lambda u, v: 0.9 + 0.5 * lead + 0.9 * rim + foot + 1.7 * lobe)
    # ---- flight feathers first (lowest layer), coverts draped over them
    flight(rel, S, P2, LE, CB, WIN, tipP, rng)
    A = smooth_poly(np.array([at(LEa, s) for s in np.linspace(0, arclen(LEa)[-1], 90)]), per=2)
    tA = unit(np.gradient(A, axis=0)); nA = np.stack([tA[:, 1], -tA[:, 0]], 1)
    wA = np.interp(A[:, 0], [0, 20, 40, 60, 75, 90], [8.5, 11.0, 11.5, 9.5, 6.0, 4.0])
    A0 = A + nA * (wA * 0.3)[:, None]

    def cdir(a, t, d):
        # axes lean toward the wing tip (+u) more for the outer coverts
        return unit(d + np.array([0.12 + 0.4 * a, 0.0]))

    rows = rows_spec(1.0, 30.0, ts=(0.04, 0.13, 0.26, 0.44, 0.68, 1.0), fuzz=False,
                     ws=(1.6, 1.9, 2.15, 2.35, 2.5, 2.65), Ts=(0.7, 0.8, 0.9, 1.0, 1.1, 1.3))
    for r in rows:
        r['smin'] = 0.72
    rows[0]['amax'] = 0.64; rows[1]['amax'] = 0.7
    drape_rows(rel, A0, CB, rows, rng, faces=('f', 'b'), tb=0.55, dirfun=cdir, barb=0.1, minD=8.5)
    # on the outer, descending part of the arch the small coverts give way to long coverts lying parallel to the
    # edge (photo px 800-900, 150-330): two lanes of overlapping long feathers between the roll and the median rows
    SA = arclen(A0); fa = SA / SA[-1]
    for dd_, wq, Lq, sp, T in [(3.4, 1.9, 14.0, 7.0, 0.85), (0.6, 1.7, 12.0, 6.0, 0.75)]:
        lane = A0[fa > 0.6] + nA[fa > 0.6] * dd_
        SL = arclen(lane)
        s0 = rng.uniform(0, sp * 0.5)
        while s0 < SL[-1] - 3:
            s1 = min(s0 + Lq * (1 + 0.1 * rng.standard_normal()), SL[-1] + 1.5)
            spn = np.array([at(lane, x) for x in np.linspace(s0, min(s1, SL[-1]), 24)])
            if np.linalg.norm(spn[-1] - spn[0]) > 5:
                rel.drape(spn[0], spn[-1], wq * (1 + float(np.clip(0.1 * rng.standard_normal(), -0.2, 0.2))), T=T,
                          faces=('f', 'b'), Tb=T * 0.55, spine=spn, R=0.6, cross=0.38, wb=0.55, fm=0.72, p=2.2,
                          ramp=0.45, crown=0.15, tilt=0.12, rachis=0.07, rgroove=0.04, rw=0.16, barb=0.1, cav=0.06)
            s0 += sp * (1 + 0.15 * rng.standard_normal())
    # scapular coverts on the root (back face), where the wing grows out of her left shoulder blade
    for b, t, w in [((4.0, 74.0), (9.0, 65.0), 1.9), ((2.5, 67.0), (7.5, 58.5), 2.0), ((7.0, 71.0), (12.5, 62.0), 2.1),
                    ((5.0, 61.0), (10.0, 53.0), 1.9)]:
        rel.drape(np.array(b) + rng.uniform(-0.4, 0.4, 2), np.array(t) + rng.uniform(-0.4, 0.4, 2), w, T=0.8, faces=('b',),
                  R=0.6, cross=0.38, ramp=0.5, crown=0.15, p=2.3, fm=0.55, tilt=0.1, cav=0.08, rachis=0.06, rgroove=0.04,
                  rw=0.16, barb=0.08)
    tq = tipP - np.array([3.2, 3.6])
    Re = lambda u, v: 1.5 + 1.0 * smoothstep((90 - u) / 15) + 0.9 * np.exp(-(np.hypot(u - tq[0], v - tq[1]) / 5.0) ** 2)
    rel.finish(smooth=0.12, Re=Re, cav=0.0, Re_auto=(0.9, 1.3, 5.0))
    S.build((R_UR[0] - 2, R_UR[1] + 2), (R_VR[0] - 2, R_VR[1] + 2), ds=0.5)
    return S, rel


# flight feathers right of the window, authored in photo pixels: (base, tip); the last one forms the outer edge
R_FAN_PX = [((612, 352), (630, 470)), ((640, 347), (680, 535)), ((672, 342), (740, 560)), ((706, 337), (800, 575)),
            ((742, 330), (865, 585)), ((778, 320), (925, 590)), ((810, 309), (980, 592)), ((836, 299), (1030, 588)),
            ((854, 293), (1070, 578)), ((864, 296), (1100, 570)), ((870, 304), (1125, 566))]
FAN_REV = False


def flight(rel, S, P2, LE, CB, WIN, tipP, rng):
    """Secondaries over the window, flight feathers fanning down-right into the drapery and to the free tip.
    Painted as a stack: each feather lies on its neighbour with a rounded 0.5-0.7 step on its exposed vane."""
    BL = smooth_poly(P2([bp for bp, tp in R_FAN_PX]), n=300)
    TL = smooth_poly(P2([tp for bp, tp in R_FAN_PX]), n=300)
    n = 11
    fs = np.linspace(0, 1, n) + np.concatenate([[0], rng.uniform(-0.02, 0.02, n - 2), [0]])
    Bs = np.array([at(BL, f * arclen(BL)[-1]) for f in fs]); Ts = np.array([at(TL, f * arclen(TL)[-1]) for f in fs])
    mids = 0.5 * (Bs + Ts)
    gap = np.zeros(n)
    for i in range(n):
        dd = []
        for j in (i - 1, i + 1):
            if 0 <= j < n:
                e = unit(Ts[j] - Bs[j]); r = mids[i] - Bs[j]
                dd.append(abs(r[0] * e[1] - r[1] * e[0]))
        gap[i] = max(dd)
    wj = 1 + np.clip(0.12 * rng.standard_normal(n), -0.22, 0.22)
    order = range(n) if FAN_REV else range(n - 1, -1, -1)
    sgn = -1.0 if FAN_REV else 1.0
    for i in order:
        f = i / (n - 1)
        b = Bs[i] + rng.uniform(-0.4, 0.4, 2); t = Ts[i] + rng.uniform(-0.5, 0.5, 2)
        w = float(np.clip(0.62 * gap[i] + 0.9, 2.4, 4.4)) * wj[i]
        d = unit(t - b); pp = np.array([-d[1], d[0]])
        L0 = np.linalg.norm(t - b)
        ff = np.linspace(0, 1, 50)
        # axis bows 1-2 units toward the leading edge as it fans to the tip
        sag = (1.0 + 0.8 * f) * np.sin(math.pi * ff) * (1 - 0.25 * ff)
        if pp[1] < 0:
            sag = -sag
        spine = b[None] + d[None] * (ff * L0)[:, None] + pp[None] * sag[:, None]
        rel.drape(b, t, w, T=0.72 + 0.08 * rng.standard_normal(), faces=('f', 'b'), Tb=0.6, spine=spine, wb=0.7,
                  fm=0.62, p=float(np.clip(rng.normal(2.0, 0.15), 1.7, 2.4)), R=0.55, cross=0.45, crown=0.12, ramp=0.3,
                  tilt=sgn * 0.2, tiltb=-sgn * 0.18, asym=0.1, blur=1.2, keep=0.2, cav=0.06,
                  rachis=0.08, rgroove=0.04, rw=0.16, roff=-0.12, barb=0.1)
    # secondaries over the window: 5 big, irregular, overlapping rounded tips
    win = smooth_poly(WIN, n=200)
    Sw = arclen(win)
    nw = 5
    for i in (range(nw) if FAN_REV else range(nw - 1, -1, -1)):
        s = (i + 0.5) / nw * Sw[-1] + rng.uniform(-0.6, 0.6)
        tip = at(win, s) + np.array([0, rng.uniform(-0.8, 0.8)])
        d = rot(np.array([0.12, -1.0]), rng.normal(0, 6))
        L = 22 + rng.uniform(-2.5, 2.5)
        w = 2.35 * (1 + float(np.clip(0.15 * rng.standard_normal(), -0.25, 0.25)))
        rel.drape(tip - unit(d) * L, tip, w, T=0.7, faces=('f', 'b'), Tb=0.65, wb=0.7, fm=0.72,
                  p=float(np.clip(rng.normal(2.2, 0.2), 1.8, 2.6)), R=0.6, cross=0.32, ramp=0.3, tilt=sgn * 0.2,
                  tiltb=-sgn * 0.2, rachis=0.07, rgroove=0.12, rw=0.17, barb=0.1, bend=rng.normal(0, 0.6),
                  cover=True, blur=1.0)
    # back (outer) face: long flight feathers carried down to the base (C3), fanning over the flared foot
    nb = 13
    for i in range(nb - 1, -1, -1):
        f = i / (nb - 1)
        b = np.array([np.interp(f, [0, 1], [33.0, 80.0]), np.interp(f, [0, 0.5, 1], [52.0, 56.0, 62.0])])
        t = np.array([np.interp(f, [0, 0.15, 1], [36.8, 42.0, 101.0]), np.interp(f, [0, 0.15, 0.85, 1], [4.0, 5.0, 6.5, 9.0])])
        t = t + rng.uniform(-0.8, 0.8, 2) * [1, 0.6]
        d = unit(t - b); pp = np.array([-d[1], d[0]]); L0 = np.linalg.norm(t - b)
        ff = np.linspace(0, 1, 40)
        spine = b[None] + d[None] * (ff * L0)[:, None] + pp[None] * (-(1.0 + 1.0 * f) * np.sin(math.pi * ff))[:, None]
        rel.drape(b, t, 3.1 * (1 + 0.1 * rng.standard_normal()), T=0.7, faces=('b',), spine=spine, wb=0.7, fm=0.62,
                  p=2.0, R=0.55, cross=0.3, ramp=0.3, tilt=-0.2, rachis=0.08, rgroove=0.14, rw=0.18, barb=0.1,
                  asym=-0.1)
    # outermost primary: its leading vane IS the outer contour from the arch end to the free, upturned tip
    oc = LE[(LE[:, 0] > P2([(835, 252)])[0][0])]
    tng = unit(np.gradient(oc, axis=0)); nin = np.stack([tng[:, 1], -tng[:, 0]], 1)
    wo = 3.0
    spine = oc + nin * (wo * 1.0)
    spine = spine[arclen(spine) < arclen(spine)[-1] - 1.2]
    rel.drape(spine[0], spine[-1], wo, T=0.85, faces=('f', 'b'), Tb=0.8, spine=spine, wb=0.45, fm=0.8, p=2.2, R=0.7,
              cross=0.25, ramp=0.15, tilt=0.15, rachis=0.08, rgroove=0.12, rw=0.18, barb=0.1)


# ----------------------------------------------------------------------------- left wing
# viewer's left = her right wing: a tall wall hugging the left of the bowl.  Base curve = rays from the bowl centre
# (2,-6); u = arc length (back -> front-left), v ~ z.  Front face (+n) = inner (bowl) face, back face = outside.
def _ray(th, r, c=(2.0, -6.0)):
    a = math.radians(th)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


L_BASE = [_ray(t, r) for t, r in [(95, 57), (110, 59), (125, 61.5), (140, 64.5), (155, 68), (170, 72), (185, 73),
                                   (200, 69), (215, 59), (228, 51), (240, 46.5)]]
L_UR = (0.0, 166.0); L_VR = (0.0, 116.0)
# photo contour of the top edge (far side of the wall): inner edge by the hair -> peak -> outer silhouette
L_TOP_PX = [(340, 258), (326, 240), (314, 222), (307, 205), (306, 185), (309, 160), (314, 135), (317, 115), (317, 95),
            (312, 78), (300, 62), (280, 53), (260, 52), (230, 60), (200, 75), (175, 90), (150, 115),
            (125, 145), (100, 180), (80, 215), (60, 260), (45, 300), (32, 350), (22, 400), (16, 450), (14, 500)]
# rolled lip crest continuing to the front-left (contract C1), in (u, v)
L_LIP_UV = [(104, 47.5), (110, 40.5), (116, 35.0), (121, 31.0), (128, 27.5), (136, 24.6), (144.5, 22.2), (151, 21.6),
            (157, 21.3), (163, 21.0)]
# tips of the secondaries hanging over the see-through gap beside her arm (photo px 200-330, 460-600)
L_WIN_UV = [(25.5, 45.5), (29.5, 43.6), (33.5, 41.5), (38.6, 39.2), (42.5, 37.8), (46.5, 37.0), (50.5, 36.6),
            (54.5, 36.0), (58.5, 35.0), (62.0, 33.6)]


def l_bow0(u, v):
    wb = smoothstep((48 - u) / 18)
    ws = smoothstep((u - 50) / 18) * smoothstep((150 - u) / 25)
    dz = 0.5 * (v - 20) + 0.5 * np.sqrt((v - 20) ** 2 + 9.0) - 1.5      # smooth max(v-20, 0): no crease
    return wb * 0.13 * dz - ws * 0.10 * dz


def build_left(F):
    from wings_dbg import pix2uv
    detail = F.h <= DETAIL_H
    S0 = Sheet(L_BASE, front_xy=(-30, -6), bow=l_bow0)
    top_px = pix2uv(S0, L_UR, L_VR, L_TOP_PX, pick='far')
    # root: below the hair contact the inner edge runs down behind her shoulder to the scapula (bowed onto her back)
    root = np.array([(24.5, 53.0), (24.8, 58.0), (27.5, 64.0), (32.5, 70.0)])
    TOP = np.vstack([root, top_px, L_LIP_UV])               # whole top edge, root -> front-left end
    TOPs = smooth_poly(TOP, per=20)
    TOPs = _fair(TOPs, 0.5, 1.2)
    # (silhouette measured against the photo: the traced edge already matches within ~2 px, no push needed)
    ut = TOPs[:, 0]; order = np.argsort(ut)

    def vtop(u):
        return np.interp(u, ut[order], TOPs[order, 1])

    def bow(u, v):
        lipz = smoothstep((u - 90) / 16) * smoothstep((170 - u) / 10)
        # wing root: the inner end bends forward onto her right shoulder blade (C4) - no separate root mass
        rootb = 14.5 * smoothstep((42.0 - u) / 18.0) * smoothstep((v - 40) / 9) * smoothstep((83 - v) / 10)
        x = np.maximum(v - (vtop(u) - 10), 0)
        xc = x - 0.5 * (x - 11.0 + np.sqrt((x - 11.0) ** 2 + 4.0)) + 0.5 * (-11.0 + np.sqrt(121.0 + 4.0))  # soft min(x, ~11)
        return l_bow0(u, v) - 0.035 * xc ** 2 * lipz + rootb

    S = Sheet(L_BASE, front_xy=(-30, -6), bow=bow)
    hr = 0.15 if detail else 0.2
    rel = Relief(L_UR, L_VR, hr=hr, detail=detail, seed=31, drape=True)
    rng = np.random.default_rng(11)
    # ---- membrane: wall down to the floor except the gap beside her arm
    lw = np.array(L_WIN_UV)[::-1] + np.array([0.0, 2.6])
    low = np.vstack([[(165.5, 18.0), (163, 12), (158, 5), (152, 0.0), (77.0, 0.0), (72.5, 2.5), (69.0, 6.5),
                      (66.6, 12.0), (65.0, 18.5), (64.2, 25.0), (63.6, 31.0)], lw])
    memb = np.vstack([TOPs[:-2], low])
    rel.membrane(memb, h=0.3)
    # ---- body
    dT, uu, vv = dist_to(rel, TOPs)
    arch = TOPs[TOPs[:, 0] < 86]
    dA, _, _ = dist_to(rel, arch)
    dome_w = np.interp(uu, [20, 40, 50, 70, 84, 95], [7.5, 10.5, 11.5, 9.5, 5.5, 3.0])
    dome = np.clip(1 - (dA / dome_w) ** 2, 0, 1) ** 1.4 * smoothstep((96 - uu) / 14)
    lipz = smoothstep((uu - 76) / 10) * smoothstep((168 - uu) / 8)
    lipb = np.clip(1 - (dT / 9.0) ** 2, 0, 1) ** 1.5 * lipz
    foot_in = (11.5 * smoothstep((118 - uu) / 12) + 2.5) * smoothstep((44 - vv) / 23) * smoothstep((uu - 66) / 6) * smoothstep((156 - uu) / 10)
    fil = np.where(vv < 5.5, 5.5 - np.sqrt(np.clip(5.5 ** 2 - (5.5 - vv) ** 2, 0, None)), 0)
    roll = (2.0 * np.exp(-((dT - 3.6) / 2.3) ** 2) - 0.55 * np.exp(-((dT - 8.2) / 1.8) ** 2)) * lipz
    roll = roll * (0.5 + 0.5 * smoothstep((uu - 118) / 16))
    rel.add_body('f', lambda u, v: 0.95 + 0.6 * np.exp(-dT / 12) + 1.3 * dome + 0.6 * lipb + roll + foot_in)
    rel.add_body('b', lambda u, v: 0.95 + 0.5 * np.exp(-dT / 12) + 1.3 * dome + 2.6 * lipb + fil)
    A = TOPs[TOPs[:, 0] < 92]
    tA = unit(np.gradient(A, axis=0)); nA = np.stack([-tA[:, 1], tA[:, 0]], 1)
    nA = np.where(nA[:, 1:2] > 0, -nA, nA)
    wA = np.interp(A[:, 0], [20, 40, 50, 70, 84, 95], [7.5, 10.0, 11.0, 9.5, 5.5, 3.0])
    CB = smooth_poly([(35.5, 50), (41, 47), (46, 46), (53, 47.5), (58, 50.5), (62, 56), (65, 63), (67, 71),
                      (68.5, 79)], per=8)
    # ================= inner face (f) =================
    # ---- flight-feather fan (bottom layer): secondaries hang straight down over the gap, the outer ones lean
    # forward along the wall; all end in rounded tips at v~28-32 (the dish's rolls begin below them)
    BLf = smooth_poly([(37, 53), (46, 50), (55, 52), (61, 57), (66, 64), (71, 72), (78, 76), (87, 71), (95, 63),
                       (102, 55), (108, 49)], n=300)
    win = smooth_poly(L_WIN_UV, n=200)
    TLf = smooth_poly(np.vstack([np.array(L_WIN_UV)[::2], [(66.5, 29.5), (75, 29.0), (84, 29.5), (93, 30.5), (102, 30.5),
                                                        (111, 29.0), (120, 27.0)]]), n=300)
    nf = 17
    fj = np.sort(np.clip(np.linspace(0, 1, nf) + np.r_[0, rng.uniform(-0.012, 0.012, nf - 2), 0], 0, 1))
    Bs = np.array([at(BLf, f * arclen(BLf)[-1]) for f in fj]); Ts_ = np.array([at(TLf, f * arclen(TLf)[-1]) for f in fj])
    for i in range(nf):                     # painted from the body outward: each outer feather lies on the inner one
        f = fj[i]
        b = Bs[i] + rng.uniform(-0.5, 0.5, 2); t = Ts_[i] + np.array([rng.uniform(-0.6, 0.6), rng.uniform(-1.2, 1.2)])
        onwin = t[0] < 62.5
        w = (2.55 if onwin else 2.85) * (1 + float(np.clip((0.2 if onwin else 0.13) * rng.standard_normal(), -0.3, 0.3)))
        d = unit(t - b); pp = np.array([-d[1], d[0]]); L0 = np.linalg.norm(t - b)
        ff = np.linspace(0, 1, 40)
        sag = (0.6 + 0.8 * f) * np.sin(math.pi * ff)
        spine = b[None] + d[None] * (ff * L0)[:, None] + pp[None] * (sag if pp[0] < 0 else -sag)[:, None]
        rel.drape(b, t, w, T=0.9 + 0.08 * rng.standard_normal(), faces=('f', 'b') if onwin else ('f',), Tb=0.6,
                  spine=spine, wb=0.7, fm=0.66 if onwin else 0.62, p=float(np.clip(rng.normal(2.1, 0.2), 1.7, 2.6)),
                  R=0.55, cross=0.32, crown=0.1, ramp=0.3, tilt=-0.22, tiltb=0.2, asym=-0.08, blur=1.0, keep=0.25,
                  cav=0.12, rachis=0.08, rgroove=0.15, rw=0.17, barb=0.1, cover=bool(onwin))
    # ---- trailing edge beside the gap: layered long feather tips wrap the end of the wall down to the floor
    for tip, dv, L, w in [((63.0, 30.5), (0.06, -1.0), 21.0, 2.3), ((63.5, 23.5), (0.16, -1.0), 23.0, 2.6),
                          ((64.6, 16.5), (0.3, -1.0), 24.0, 2.4), ((66.8, 10.0), (0.45, -1.0), 25.0, 2.8),
                          ((70.2, 5.2), (0.62, -1.0), 25.0, 2.6)]:
        tip = np.array(tip) + rng.uniform(-0.4, 0.4, 2); d = unit(np.array(dv))
        rel.drape(tip - d * L, tip, w, T=0.7, faces=('f', 'b'), Tb=0.7, R=0.8, cross=0.3, wb=0.7, fm=0.5, p=1.9,
                  ramp=0.3, tilt=-0.2, tiltb=0.2, rachis=0.07, rgroove=0.12, rw=0.17, barb=0.1, bend=-0.8, cover=True)
    # ---- the rolled lip: lanes of long striated feathers running along the descending top edge to the front
    lip = TOPs[TOPs[:, 0] > 74]
    tL = unit(np.gradient(lip, axis=0)); nL = np.stack([-tL[:, 1], tL[:, 0]], 1)
    nL = np.where(nL[:, 1:2] > 0, -nL, nL)
    for lane, (dd_, wq, Lq, sp) in reversed(list(enumerate([(2.6, 2.0, 30.0, 14.0), (6.0, 2.2, 34.0, 16.0),
                                                            (9.6, 2.4, 36.0, 18.0), (13.4, 2.6, 38.0, 19.0)]))):
        lane_line = lip + nL * dd_
        SL = arclen(lane_line)
        s = rng.uniform(0, sp) - Lq * 0.3
        while s < SL[-1] - 4:
            s0 = max(s, 0.0); s1 = min(s + Lq * (1 + 0.1 * rng.standard_normal()), SL[-1] + 2)
            ss = np.linspace(s0, s1, 30)
            spine = np.array([at(lane_line, x) for x in ss])
            if s1 > SL[-1]:
                spine[-1] = spine[-2] + unit(spine[-2] - spine[-3]) * (s1 - SL[-1])
            if np.linalg.norm(spine[-1] - spine[0]) > 6:
                wv = wq * (1 + float(np.clip(0.12 * rng.standard_normal(), -0.25, 0.25)))
                rel.drape(spine[0], spine[-1], wv, T=1.0, faces=('f', 'b'), Tb=0.55, spine=spine, R=0.7, cross=0.36,
                          wb=0.6, fm=0.6, p=1.9, ramp=0.35, tilt=0.18, tiltb=0.12, rachis=0.06, rgroove=0.1, rw=0.16,
                          barb=0.08, barb_ang=22, cav=0.08)
            s += sp * (1 + 0.12 * rng.standard_normal())
    # ---- coverts on the inner face under the arch: many rows of small rounded feathers (marginal at the rim ->
    # greater ~4 wide), rows staggered by half a feather, painted bottom-up so each row overhangs the next
    A0 = A + nA * (wA * 0.22)[:, None]
    m = A[:, 0] < 69.5

    def cdir(a, t, d):
        return unit(d + np.array([0.05 + 0.35 * a, 0.0]))

    ts = np.cumsum([0.0, 2.6, 3.0, 3.5, 4.0, 4.6, 5.3, 6.1, 7.0])
    ts = ts / ts[-1]
    ws = np.linspace(1.15, 2.2, len(ts)); Ts = np.linspace(0.55, 1.05, len(ts))
    rows = rows_spec(1.0, 42.0, ts=tuple(ts * 0.97 + 0.03), ws=tuple(ws), Ts=tuple(Ts), sps=1.5, tilt=-0.12)
    for r in rows:
        r['smin'] = 0.65
    drape_rows(rel, A0[m], CB, rows, rng, faces=('f',), dirfun=cdir, barb=0.09, minD=6.0)
    # ================= outer face (b) =================
    # long primaries running down (and forward) the outside of the wall, 6-8 wide, rounded stepped tips
    nb = 11
    fbj = np.sort(np.clip(np.linspace(0, 1, nb) + np.r_[0, rng.uniform(-0.02, 0.02, nb - 2), 0], 0, 1))
    for i in range(nb):
        f = fbj[i]
        b = np.array([np.interp(f, [0, 1], [30, 104]), 0.0]); b[1] = vtop(b[0]) - np.interp(f, [0, 1], [22, 12])
        t = np.array([np.interp(f, [0, 1], [38, 158]), np.interp(f, [0, 0.7, 1], [6.0, 7.0, 10.0])])
        t[1] = min(t[1], vtop(t[0]) - 6)
        d = unit(t - b); pp = np.array([-d[1], d[0]]); L0 = np.linalg.norm(t - b)
        ff = np.linspace(0, 1, 40)
        spine = b[None] + d[None] * (ff * L0)[:, None] + pp[None] * (-(1.0 + 1.0 * f) * np.sin(math.pi * ff))[:, None]
        rel.drape(b, t, 3.4 * (1 + float(np.clip(0.12 * rng.standard_normal(), -0.22, 0.22))), T=0.75, faces=('b',),
                  spine=spine, wb=0.7, fm=0.62, p=2.0, R=0.6, cross=0.3, ramp=0.25, tilt=0.22, asym=0.1, blur=1.2,
                  cav=0.1, rachis=0.07, rgroove=0.14, rw=0.18, barb=0.1)
    # coverts on the outer face near the top, right up to the rim (no flat land)
    DIb = A + nA * (wA * 0.2)[:, None]
    rowsb = rows_spec(1.0, 40.0, ts=(0.03, 0.12, 0.25, 0.42, 0.66, 1.0), ws=(1.3, 1.6, 1.9, 2.15, 2.35, 2.5), fuzz=False,
                      Ts=(0.55, 0.65, 0.75, 0.85, 0.92, 1.0), sps=1.5, tilt=0.12)
    drape_rows(rel, DIb[m], CB, rowsb, rng, faces=('b',), tb=1.0, dirfun=cdir, barb=0.09, minD=3.0)
    # scapular coverts: a few soft feathers on the root where the wing grows out of her shoulder blade
    for b, t, w in [((27.0, 72.0), (31.0, 62.0), 1.9), ((25.0, 66.0), (29.5, 57.0), 2.0), ((29.5, 69.0), (34.5, 59.5), 2.1),
                    ((26.5, 60.5), (31.0, 51.5), 2.0)]:
        rel.drape(np.array(b) + rng.uniform(-0.4, 0.4, 2), np.array(t) + rng.uniform(-0.4, 0.4, 2), w, T=0.8, faces=('b',),
                  R=0.6, cross=0.38, ramp=0.5, crown=0.15, p=2.3, fm=0.55, tilt=0.1, cav=0.08, rachis=0.06, rgroove=0.04,
                  rw=0.16, barb=0.08)
    Re = lambda u, v: (1.4 + (1.2 + 1.4 * smoothstep((u - 122) / 14)) * smoothstep((u - 78) / 10) * smoothstep((166 - u) / 5)
                       + 0.9 * smoothstep((80 - u) / 6) * smoothstep((u - 56) / 4) * smoothstep((36 - v) / 6))
    rel.finish(smooth=0.12, Re=Re, cav=0.0, Re_auto=(0.9, 1.3, 5.0))
    S.build((L_UR[0] - 2, L_UR[1] + 2), (L_VR[0] - 2, L_VR[1] + 2), ds=0.5)
    return S, rel


def roots():
    """Wing roots (C4) are now part of the wing sheets themselves: each sheet's inner end is bowed forward onto her
    shoulder blade (see r_bow / build_left.bow), so no separate root mass shows from any side.  Only the fillet
    between the left wing's inner foot and the dish wall (former dark slot at (-62,-5,26)) remains here."""
    B = Batch()
    B.ellipsoid((-61.5, -5.5, 24.5), (3.2, 9.0, 7.0), k=3.0)
    B.ellipsoid((-26.0, 28.6, 49.5), (2.6, 1.6, 2.4), k=1.5)      # closes a pin-hole void at the left root's lower edge
    B.ellipsoid((-61.8, -22.0, 10.0), (1.7, 2.6, 6.8), k=1.0)     # fills the sealed crevice between inner foot and dish wall
    B.ellipsoid((-27.5, 28.3, 68.3), (1.1, 1.1, 1.1), k=0.5)      # sealed pin-hole between the left root and her back
    B.ellipsoid((-17.9, 30.0, 72.6), (2.0, 1.4, 2.6), k=0.8)      # pocket between the right root and her hair locks
    return B


def cleanup(F, min_vox=None):
    """Remove tiny solid islands and fill tiny enclosed voids (single-voxel fill noise) in the wings grid."""
    from scipy import ndimage
    G = F.G
    if min_vox is None:
        min_vox = int(max(30, 4.0 / F.h ** 3))
    ins = G < 0
    lab, n = ndimage.label(ins)
    if n > 1:
        cnt = np.bincount(lab.ravel())
        small = np.flatnonzero(cnt < min_vox); small = small[small > 0]
        if len(small):
            m = np.isin(lab, small)
            G[m] = np.maximum(G[m], 0.5 * F.h)
    out = G >= 0
    lab, n = ndimage.label(out)
    if n > 1:
        cnt = np.bincount(lab.ravel())
        border = np.unique(np.concatenate([lab[0].ravel(), lab[-1].ravel(), lab[:, 0].ravel(), lab[:, -1].ravel(),
                                           lab[:, :, 0].ravel(), lab[:, :, -1].ravel()]))
        small = np.flatnonzero(cnt < min_vox * 4); small = small[(small > 0) & ~np.isin(small, border)]
        if len(small):
            m = np.isin(lab, small)
            G[m] = np.minimum(G[m], -0.5 * F.h)
    return F


def component(F):
    which = os.environ.get('WINGS_ONLY', 'both')
    if which in ('both', 'right'):
        S, rel = build_right(F)
        fill(F, S, rel)
    if which in ('both', 'left'):
        S, rel = build_left(F)
        fill(F, S, rel)
    if which == 'both':
        F.apply(roots())
    return cleanup(F)
