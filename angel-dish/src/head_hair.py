"""Hair for the head component (round 2).

The hair is a smooth cap plus SHEETS of ribbon locks.  A sheet is bounded by guide paths; each guide is a list of
cap angles (phi, theta) sweeping from the parting over the scalp, followed by fall control points that are either
reference-pixel points (ray-cast onto the figure's body, or a depth plane when nothing is near) or world points.
Ribbons are interpolated between neighbouring guides, so they flow continuously from the parting to their tips,
wave in phase within a sheet (long combed S-waves), taper to flat points and carry 1-2 fine strand grooves
(grooves only at fine resolution, h <= ~0.3)."""
import math
import numpy as np
from sdf import Batch, catmull, resample
from head_k import add_ribbon
from head_drape import Body
import head
import cam

P, D = head.P, head.D
CAMLOC = cam.frame()[0]
CAP_C = np.array([-0.3, -1.8, 1.6])          # outer hair surface (ribbon top) of the scalp, head-local
CAP_R = np.array([6.7, 7.6, 8.2])


TC, SINK, CAP_SHRINK, WOVER_CAP = 1.0, 0.4, 0.85, 1.15     # scalp ribbon half-thickness, how deep its centre sits in the cap volume


import os
DBG = os.environ.get('HEAD_DBG') == '1'
GAMP_CAP = 0.32
PITCH = 0.8          # strand-groove pitch (centre groove on every ribbon; side grooves on wide ribbons)


def detail_gate(h):
    """1 at h <= 0.22, 0 at h >= 0.36 (fine grooves alias at coarse preview resolution)."""
    return float(np.clip((0.36 - h) / 0.14, 0.0, 1.0))


def cap_local(phi, theta):
    f, t = math.radians(phi), math.radians(theta)
    return CAP_C + CAP_R * np.array([math.cos(t) * math.sin(f), math.cos(t) * math.cos(f), math.sin(t)])


def unit_rows(V):
    return V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)


def smooth_rows(V, it=3, norm=True):
    V = np.array(V, float)
    for _ in range(it):
        V[1:-1] = 0.25 * V[:-2] + 0.5 * V[1:-1] + 0.25 * V[2:]
    return unit_rows(V) if norm else V


def arclen(C):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))])


def px(u, v, y):
    return ('px', u, v, y)


def w(x, y, z):
    return ('w', x, y, z)


def ws(x, y, z):
    """world point snapped onto the body surface (lying on it) when the body is within 6 mm."""
    return ('ws', x, y, z)


def hl(x, y, z):
    """head-local point (x = her left, y = face forward, z = up)."""
    return ('w', *P((x, y, z)))


def pf(u, v, y):
    """reference pixel ray-cast onto the FIRST body surface it meets (the visible surface); plane y if no hit."""
    return ('pf', u, v, y)


def pp(u, v, y):
    """reference pixel on the depth plane y (no ray-cast; pushed out of the body only)."""
    return ('pp', u, v, y)


# ----------------------------------------------------------------------------- sheets
# guide = (cap angle list, fall item list).  n = ribbons between consecutive guides.
# wave = (amplitude, wavelength, phase) lateral S-wave on the fall (and optionally from 'wcap' on the scalp).
def band(cpts, hw):
    """Two guide fall lists offset +-hw laterally (perpendicular to the path, in the camera-facing plane)."""
    C = np.array(cpts, float)
    Cd = catmull(C, per=8)
    out0, out1 = [], []
    for p in C:
        i = int(np.argmin(np.linalg.norm(Cd - p, axis=1)))
        t = Cd[min(i + 1, len(Cd) - 1)] - Cd[max(i - 1, 0)]; t /= np.linalg.norm(t)
        tc = CAMLOC - p; tc /= np.linalg.norm(tc)
        lat = np.cross(tc, t); lat /= np.linalg.norm(lat)
        out0.append(w(*(p + lat * hw))); out1.append(w(*(p - lat * hw)))
    return out0, out1


# flare locks over her right shoulder (centre lines, world): they spring from the side of the head, pass over
# the back of the shoulder in front of the wing and curl down behind the shoulder
def P2W(trace, ys):
    return [tuple(cam.unproject(p, plane_y=y)) for p, y in zip(trace, ys)]


# three stacked S-locks traced on the photo (px) at chosen depths: they leave the side of the head behind the
# front column, run out over the shoulder (in front of the wing) and curl down at the outer end
# flare over her right shoulder (traced on the photo, ref_flare5): an upper wave lobe that curls under, and two
# heavy locks that pass over the top of the shoulder, turn down at px x~337 and hang along the back of the upper arm
# flare over her right shoulder: ONE cascade of ~7 packed S-wave locks (traced on ref_flare6): the top edge follows the
# outer contour of the upper lobe, the bottom edge rests on the top of the shoulder; all of them pass over the shoulder
# and end flattened on the back of the upper arm / shoulder (no free hooks)
_FT = P2W([(393, 192), (375, 207), (363, 222), (357, 238), (354, 251), (343, 261), (337, 271)], [23.6, 24.2, 24.8, 25.4, 25.8, 26.1, 26.2]) + \
    [ws(-35.2, 25.6, 71.8), ws(-35.0, 24.4, 69.2), ws(-34.6, 23.6, 67.0)]
_FM = P2W([(403, 236), (388, 249), (372, 258), (357, 264), (346, 271)], [23.0, 23.9, 24.9, 25.5, 25.8]) + \
    [ws(-34.4, 24.6, 70.2), ws(-34.0, 23.6, 67.8), ws(-33.6, 23.0, 66.0)]
_FB = [(-24.2, 22.4, 76.0), ws(-27.2, 22.5, 74.4), ws(-29.8, 22.7, 73.0), ws(-31.8, 23.0, 71.6), ws(-33.0, 23.2, 69.8),
       ws(-33.4, 23.0, 68.0), ws(-33.2, 22.6, 66.4)]
_FT = [w(*p) if not isinstance(p[0], str) else p for p in _FT]
_FM = [w(*p) if not isinstance(p[0], str) else p for p in _FM]
_FB = [w(*p) if not isinstance(p[0], str) else p for p in _FB]
_RU = [(-25.6, 23.8, 81.2), (-27.2, 26.4, 77.6), (-29.0, 28.8, 74.6), (-30.8, 30.6, 72.0), (-31.6, 31.6, 68.5),
       (-31.6, 32.0, 64.5)]
_RUa, _RUb = band(_RU, 2.4)
_RUa = _RUa[:2] + [ws(*x[1:]) for x in _RUa[2:]]
_RUb = _RUb[:2] + [ws(*x[1:]) for x in _RUb[2:]]
_RM = [(-24.8, 21.0, 83.6), (-26.0, 22.6, 80.4), (-26.6, 23.8, 77.6), (-26.8, 25.0, 75.8)]
_RMa, _RMb = band(_RM, 2.0)


SHEETS = [
    # her right, front: covers the upper right forehead and temple (the lobe edge forms the hairline), then a column of
    # heavy fused locks beside the cheek and the neck, over the front of the right shoulder, ending flat by the V-neck
    dict(name='RF', var=(0.08, 0.18, 0.25), under_end=1.8, offk=1.0, tipfade=True, bulge=(0.22, 5.0, 7.5), n=[4], wave=(1.2, 9.6, 0.6), nstr=2, tf=1.3, amp=0.32, wover=1.4, seed=1,
         guides=[([(-9, 37), (-19, 30), (-29, 23), (-39, 15), (-48, 7), (-57, -3), (-61, -14)],
                  [hl(-6.5, 1.6, -3.0), hl(-6.3, 1.2, -4.6), hl(-5.6, 0.5, -6.0), hl(-4.9, -0.3, -7.3), pp(421, 255, 20.2), pp(418, 273, 20.6), pf(420, 289, 20.6), pf(424, 305, 20.0),
                   pf(429, 320, 19.0), pf(434, 335, 18.0), pf(438, 348, 17.5), pf(440, 358, 17.0)]),
                 ([(-10, 40), (-34, 36), (-52, 27), (-64, 14), (-70, -2), (-73, -17), (-74, -30)],
                  [pp(398, 241, 21.4), pp(393, 257, 21.8), pp(394, 273, 22.0), pf(396, 289, 22.0), pf(400, 305, 21.2),
                   pf(405, 320, 20.4), pf(410, 335, 19.6), pf(415, 348, 19.0), pf(420, 359, 18.5)])]),
    # her right: hair mass hanging from the side of the head onto the trapezius, behind the front column
    dict(name='RM', tipw=0.6, n=[3], wave=(0.9, 10.5, 1.4), nstr=3, tf=1.15, amp=0.3, wover=1.25, seed=8, under_t=1.25,
         guides=[([(-10, 41), (-35, 37), (-57, 28), (-73, 14), (-81, -2), (-85, -18), (-87, -32)], _RMa),
                 ([(-10, 42), (-38, 38), (-62, 29), (-80, 15), (-90, -3), (-95, -19), (-98, -31)], _RMb)]),
    dict(name='RU', tipfade=True, tipw=0.6, stagger=3.0, nmode='radial', wdelay=4.0, n=[3], wave=(0.8, 10.0, 0.9), nstr=3, tf=1.1, amp=0.3, wover=1.25, seed=9, under_t=1.0,
         guides=[([(-10, 50), (-55, 44), (-92, 29), (-112, 9), (-121, -11), (-125, -26)], _RUa),
                 ([(-10, 58), (-66, 50), (-108, 32), (-130, 10), (-139, -10), (-143, -25)], _RUb)]),
    # her right: the flare over the shoulder (upper curling lobe + two heavy locks turning down behind the arm)
    dict(name='RS', tipfade=True, tipw=0.75, n=[3, 3], groups=(2, 3), var=(0.08, 0.2, 0.3), under_t=0.95, under_end=2.0, wave=(0.5, 9.0, 2.4), nstr=3, tf=1.2, amp=0.3, wover=1.6, seed=2,
         guides=[([(-10, 46), (-46, 41), (-78, 30), (-98, 13), (-108, -5), (-113, -19), (-116, -29)], _FT),
                 ([(-10, 52), (-56, 46), (-92, 31), (-112, 12), (-121, -6), (-126, -19), (-129, -28)], _FM),
                 ([(-10, 60), (-68, 53), (-108, 34), (-130, 11), (-139, -8), (-144, -20), (-147, -27)], _FB)]),
    # her right, back of the head -> down the back of the head, then a wavy curtain on the upper back
    dict(name='RB', tipfade=True, tipw=0.5, stagger=3.0, nmode='radial', wdelay=4.0, n=[3, 3], wave=(0.8, 10.5, 1.0), nstr=3, tf=1.1, amp=0.3, wover=1.25, seed=4, under_t=0.8,
         guides=[([(-10, 66), (-84, 57), (-126, 36), (-142, 12), (-146, -12)],
                  [ws(-24.5, 28.5, 78.5), ws(-27.5, 30.5, 72.5), ws(-28.5, 31.2, 67.0), ws(-28.0, 31.6, 61.5)]),
                 ([(-10, 76), (-110, 63), (-150, 40), (-160, 14), (-163, -12)],
                  [ws(-21.5, 29.0, 78.0), ws(-23.5, 31.0, 72.0), ws(-24.0, 31.6, 66.2), ws(-23.6, 32.0, 60.5)]),
                 ([(-40, 80), (-160, 70), (-170, 42), (-172, 14), (-173, -12)],
                  [ws(-20.4, 30.0, 78.0), ws(-20.8, 31.6, 71.5), ws(-21.0, 32.3, 66.0), ws(-21.0, 32.6, 60.5)])]),
    # centre back: from the crown straight down the nape (closes the seam between RB and LB)
    dict(name='CB', tipfade=True, tipw=0.5, stagger=3.0, nmode='radial', wdelay=4.0, n=[6], wave=(0.8, 10.5, 1.6), nstr=3, tf=1.1, amp=0.3, wover=1.25, seed=11, under_t=0.9,
         guides=[([(-150, 80), (-168, 62), (-172, 40), (-173, 14), (-174, -12)],
                  [w(-21.6, 29.0, 79.0), w(-22.0, 30.6, 73.0), w(-22.2, 32.2, 67.0), w(-22.2, 32.4, 62.0)]),
                 ([(150, 80), (168, 62), (172, 40), (173, 14), (174, -12)],
                  [w(-15.4, 29.0, 79.0), w(-15.6, 32.2, 73.0), w(-15.8, 34.6, 67.0), w(-15.8, 34.2, 62.0)])]),
    # her left, front: sweeps over the left temple, behind the cheek, column beside the neck onto the chest
    dict(name='LF', var=(0.08, 0.18, 0.25), under_end=1.8, offk=1.0, tipfade=True, bulge=(0.14, 4.8, 7.0), n=[3, 2], wave=(1.15, 9.6, 0.2), nstr=2, tf=1.3, amp=0.32, wover=1.4, seed=5,
         guides=[([(-12, 36), (6, 30), (22, 23), (35, 15), (45, 4), (51, -10), (55, -25), (56, -32)],
                  [pp(467, 252, 21.8), pp(467, 266, 22.0), pp(469, 281, 22.2), pp(473, 296, 22.2), pf(477, 311, 22.0),
                   pf(482, 325, 21.5), pf(484, 338, 21.0), pf(486, 349, 20.5), pf(487, 356, 20.0)]),
                 ([(-12, 44), (22, 40), (48, 31), (66, 17), (76, 0), (82, -17), (85, -31)],
                  [pp(483, 247, 22.6), pp(489, 264, 22.8), pp(493, 282, 23.0), pp(496, 300, 23.0), pp(498, 317, 22.6),
                   pp(497, 331, 22.0), pf(495, 344, 22.0), pf(493, 353, 21.5), pf(491, 360, 21.0)]),
                 ([(-12, 54), (34, 50), (64, 40), (84, 23), (94, 4), (100, -14), (102, -28)],
                  [pp(494, 240, 23.6), pp(500, 255, 24.0), pp(503, 272, 24.0), pp(505, 290, 23.8), pp(505, 306, 23.5),
                   pp(505, 322, 23.0), pp(503, 336, 21.5), pf(501, 346, 22.0)])]),
    # her left, side: behind the ear, down behind the left shoulder
    dict(name='LS', tipfade=True, tipw=0.6, stagger=3.0, nmode='radial', wdelay=4.0, n=[3], wave=(0.9, 10.5, 1.8), nstr=3, tf=1.15, amp=0.3, wover=1.25, seed=6, under_t=0.7,
         guides=[([(-12, 58), (36, 54), (66, 44), (86, 26), (96, 6), (102, -14)],
                  [w(-11.6, 25.5, 79.0), w(-10.6, 27.6, 73.5), w(-10.4, 29.2, 67.5), w(-10.8, 30.2, 61.5)]),
                 ([(-12, 70), (50, 60), (90, 42), (112, 18), (122, -4), (126, -16)],
                  [w(-13.0, 27.6, 79.0), w(-12.2, 29.6, 73.5), w(-12.0, 30.8, 67.2), w(-12.4, 31.4, 61.0)])]),
    # her left, back
    dict(name='LB', tipfade=True, tipw=0.5, stagger=3.0, nmode='radial', wdelay=4.0, n=[4], wave=(0.8, 10.5, 0.4), nstr=3, tf=1.1, amp=0.3, wover=1.25, seed=7, under_t=0.8,
         guides=[([(-12, 72), (60, 64), (106, 44), (124, 18), (130, -12)],
                  [ws(-13.6, 28.6, 78.4), ws(-12.4, 30.4, 72.6), ws(-12.0, 31.4, 66.6), ws(-12.2, 31.8, 60.6)]),
                 ([(40, 80), (160, 70), (170, 42), (172, 14), (173, -12)],
                  [ws(-16.8, 30.0, 78.0), ws(-17.0, 31.6, 71.5), ws(-17.2, 32.3, 66.0), ws(-17.2, 32.6, 60.5)])]),
]


# ----------------------------------------------------------------------------- geometry helpers
class Sampler:
    def __init__(self, F):
        from scipy.ndimage import map_coordinates
        self.F = F; self.mc = map_coordinates

    def d(self, Pp):
        Pp = np.atleast_2d(Pp)
        return self.mc(self.F.G, ((Pp - self.F.lo) / self.F.h).T, order=1, mode='nearest')

    def g(self, Pp):
        Pp = np.atleast_2d(Pp); e = max(self.F.h, 0.3); out = np.zeros_like(Pp)
        for i in range(3):
            o = np.zeros(3); o[i] = e
            out[:, i] = (self.d(Pp + o) - self.d(Pp - o)) / (2 * e)
        return unit_rows(out)

    def project(self, Pp, iso, it=6, wgt=None):
        Pp = np.array(Pp, float)
        wgt = np.ones(len(Pp)) if wgt is None else wgt
        for _ in range(it):
            dd = self.d(Pp) - iso
            Pp -= (0.9 * dd * wgt)[:, None] * self.g(Pp)
        return Pp


def resolve(body, item, off):
    if item[0] == 'pp':
        p, _ = body.raycast((item[1], item[2]), off, item[3], mode='plane')
        if body.d(p)[0] < off:
            p = body.project(p, off, maxmove=4.0)[0]
        return p
    if item[0] == 'pf':
        p, hit = body.raycast((item[1], item[2]), off, item[3])
        if not hit:
            p, _ = body.raycast((item[1], item[2]), off, item[3], mode='plane')
            if body.d(p)[0] < off:
                p = body.project(p, off, maxmove=4.0)[0]
        return p
    if item[0] == 'px':
        p, hit = body.raycast((item[1], item[2]), off, item[3])
        if not hit or abs(p[1] - item[3]) > 2.5:
            p, _ = body.raycast((item[1], item[2]), off, item[3], mode='plane')
        if body.d(p)[0] < off:
            p = body.project(p, off, maxmove=4.0)[0]
        return p
    p = np.array(item[1:], float)
    if item[0] == 'ws':
        if body.d(p)[0] < 6.0:
            p = body.project(p, off, iters=10, maxmove=7.0)[0]
        return p
    if body.d(p)[0] < off:
        p = body.project(p, off, maxmove=5.0)[0]
    return p


def smooth_fall(body, fl, off, it=4):
    """Remove depth zigzags of the ray-cast fall points (pixel casts land alternately on the plane and on the body
    relief): Laplacian smoothing (end points fixed), then pushed back out of the body."""
    fl = np.array(fl, float)
    if len(fl) < 4:
        return fl
    for _ in range(it):
        fl[1:-1] = 0.5 * fl[1:-1] + 0.25 * (fl[:-2] + fl[2:])
        dd = body.d(fl)
        m = dd < off
        if m.any():
            fl[m] = body.project(fl[m], off, maxmove=5.0)
    return fl


def guide_path(body, cs, cap_ang, fall, off, sink, Nc, Nf):
    ang = catmull(np.array(cap_ang, float), per=10)
    loc = np.array([cap_local(*a) for a in ang])
    wp = cs.project(P(loc), -sink)
    ws = arclen(wp)
    keep = [0]
    for i in range(1, len(wp) - 1):
        if ws[i] - ws[keep[-1]] >= 1.4:
            keep.append(i)
    keep.append(len(wp) - 1)
    cap_ctrl = wp[keep]
    fl = np.array([resolve(body, it, off) for it in fall])
    fl = smooth_fall(body, fl, off)
    ctrl = np.vstack([cap_ctrl, fl])
    C = catmull(ctrl, per=14)
    s = arclen(C)
    # arc position of the exit (last cap control point)
    i_ex = int(np.argmin(np.linalg.norm(C - cap_ctrl[-1], axis=1)))
    s_ex = s[i_ex]
    cpart = np.stack([np.interp(np.linspace(0, s_ex, Nc), s, C[:, k]) for k in range(3)], 1)
    fpart = np.stack([np.interp(np.linspace(s_ex, s[-1], Nf + 1)[1:], s, C[:, k]) for k in range(3)], 1)
    return np.vstack([cpart, fpart])


SPINE = np.array([-18.6, 23.4])


def frames(C, sf, body, cs, mode='cam'):
    """Robust ribbon frame: U = outward normal (cap normal on the scalp, body normal near the body; when hanging
    free: toward the camera (mode 'cam', front locks) or radially away from the body axis (mode 'radial')),
    S = lateral (in the ribbon plane)."""
    T = unit_rows(np.gradient(C, axis=0))
    cn = cs.g(C)
    bd = body.d(C); bg = body.grad(C)
    if mode == 'cam':
        free = unit_rows(CAMLOC[None] - C)
    else:
        rr = np.zeros_like(C); rr[:, :2] = C[:, :2] - SPINE[None]
        free = unit_rows(rr)
    kb = (0.6 if mode == 'cam' else 1.6) * np.clip((4.0 - bd) / 2.5, 0, 1)[:, None]
    fn = smooth_rows(unit_rows(free + kb * smooth_rows(bg, 30)), 30)     # smooth: the body relief must not twist the locks
    a = np.clip((sf + 1.0) / 5.0, 0, 1)[:, None]
    ref = unit_rows((1 - a) * cn + a * fn)
    U = ref - T * np.sum(ref * T, axis=1)[:, None]
    U = smooth_rows(unit_rows(U), 30)
    U = unit_rows(U - T * np.sum(U * T, axis=1)[:, None])
    S = unit_rows(np.cross(U, T))
    return T, U, S


def build_sheet(H, body, cs, sh, gate, h):
    rng = np.random.default_rng(sh['seed'])
    tf = sh['tf']; tc = TC
    off = tf * sh.get('offk', 0.55)
    sink = SINK
    Nc = 110; Nf = 130
    G = [guide_path(body, cs, cap_ang, fall, off, sink, Nc, Nf) for cap_ang, fall in sh['guides']]
    A0, Lam, Ph = sh['wave']
    gamp = sh.get('amp', 0.22)
    ribbons = []
    for gi in range(len(G) - 1):
        nl = sh['n'][gi]
        for j in range(nl):
            u = (j + 0.5) / nl + rng.uniform(-0.1, 0.1) / nl
            ribbons.append((G[gi], G[gi + 1], u, nl))
    # locks are grouped into broader masses of 2-3 ribbons: each mass has its own wavelength / amplitude / phase /
    # end position (hand-sculpted variation), the ribbons inside a mass stay nearly in phase (fused, combed)
    gmin, gmax = sh.get('groups', (2, 3))
    gid = []
    g = 0
    while len(gid) < len(ribbons):
        gid += [g] * int(rng.integers(gmin, gmax + 1)); g += 1
    vl, va, vp = sh.get('var', (0.15, 0.32, 0.5))
    gpar = [(rng.uniform(1 - vl, 1 + 0.7 * vl), rng.uniform(1 - va, 1 + va), rng.uniform(-vp, vp), rng.uniform(0.0, sh.get('stagger', 1.4)))
            for _ in range(g)]
    for ri, (Ga, Gb, u, nl) in enumerate(ribbons):
        gl, ga_, gp, gst = gpar[gid[ri]]
        C = Ga + (Gb - Ga) * u
        N = len(C)
        wsc = np.clip((Nc + 6 - np.arange(N)) / 12.0, 0, 1)
        C = cs.project(C, -sink, wgt=wsc)
        s = arclen(C)
        s_ex = s[Nc - 1]
        sf = s - s_ex
        T, Uv, S = frames(C, sf, body, cs, sh.get('nmode', 'cam'))
        dG = Gb - Ga
        dist = np.linalg.norm(dG - T * np.sum(dG * T, axis=1)[:, None], axis=1)
        # ---- coherent S-wave (same phase across the sheet, tiny per-ribbon offset)
        dph = gp + rng.uniform(-0.12, 0.12)
        Lr = s[-1]
        w0 = sh.get('wdelay', 0.0)
        ramp = np.clip((sf + 1.0 - w0) / 5.0, 0, 1) * np.clip((Lr - s - 0.5) / 4.5, 0, 1) ** 0.7
        disp = A0 * ga_ * ramp * np.sin(2 * math.pi * np.maximum(sf - w0, 0) / (Lam * gl) + Ph + dph)
        if sh.get('wcap'):
            sc0 = s_ex - 9.0
            rc = np.clip((s - sc0) / 3.0, 0, 1) * (sf < 0)
            disp = disp + sh['wcap'] * rc * np.sin(2 * math.pi * (s - sc0) / (Lam * 0.8) + Ph + dph)
        C = C + S * disp[:, None]
        if sh.get('bulge'):
            # marcel-wave crests across the flow on the scalp/temple part (same phase across the sheet)
            ba, bl, bs = sh['bulge']
            br = np.clip((s - bs) / 2.0, 0, 1) * np.clip((4.0 - sf) / 4.0, 0, 1)
            C = C + Uv * (ba * br * np.sin(2 * math.pi * (s - bs) / bl + Ph))[:, None]
        # roots emerge from the parting: sink the first ~2.4 mm into the scalp (soft V valley along the part line)
        C = C - Uv * (sh.get('rootsink', 0.2) * np.clip(1 - s / 2.5, 0, 1) ** 1.3)[:, None]
        # ---- end stagger, profiles
        cut = Lr - gst - rng.uniform(0.0, 0.4)
        m = s <= cut
        C, Uv, S, s, sf, dist = C[m], Uv[m], S[m], s[m], sf[m], dist[m]
        Lr = s[-1]
        wv = rng.uniform(0.75, 1.3)
        fallw = np.clip((sf + 2.0) / 5.0, 0, 1)
        wo = WOVER_CAP + (sh['wover'] - WOVER_CAP) * fallw
        wb = np.clip(0.5 * dist / nl * wo, 0.45, 2.3) * wv
        wb = np.convolve(np.pad(wb, 6, mode='edge'), np.ones(13) / 13, mode='valid')
        ltip = 4.5
        tipf = np.clip((Lr - s) / ltip, 0, 1)
        root = np.clip(0.8 + 0.2 * s / 1.0, 0, 1)
        tw = sh.get('tipw', 0.08)
        fall = np.clip((sf + 2.0) / 4.0, 0, 1)
        tv = rng.uniform(0.85, 1.15)
        TWR = 1.1 + (sh.get('twr', 0.9) - 1.1) * fall     # thickness/width cap: ridge-like combed strands on the scalp
        gfade = 1.0
        if sh.get('tipfade'):
            # lock ends flatten onto the body: width to ~45%, thickness to ~15%, centre sinks into the surface
            lf = 5.0
            tf_ = np.clip((Lr - s) / lf, 0, 1)
            W = wb * root * (0.45 + 0.55 * tf_ ** 0.8)
            onb = np.clip((2.5 - body.d(C)) / 1.5, 0, 1)            # 1 where the lock lies on the body
            floor = 0.15 * onb + 0.55 * (1 - onb)
            Tt = (tc + (tf - tc) * fall) * tv * np.clip(0.58 + 0.42 * s / 1.3, 0, 1) * (floor + (1 - floor) * tf_ ** 0.9)
            Tt = np.minimum(Tt, np.maximum(W * TWR, 0.5))
            C = C - Uv * (0.85 * off * onb * (1 - tf_) ** 1.3)[:, None]
            gfade = np.clip(tf_ * 1.6, 0, 1) ** 1.2          # no strand grooves on the thin flattened ends (no torn teeth)
        else:
            W = wb * root * (tw + (1 - tw) * tipf ** 0.7)
            Tt = (tc + (tf - tc) * fall) * tv * np.clip(0.58 + 0.42 * s / 1.3, 0, 1) * (max(0.35, tw) + (1 - max(0.35, tw)) * tipf)
            Tt = np.minimum(Tt, W * TWR)
            # printable free-hanging ends: >= ~0.9 mm thick unless lying on the body
            onb = np.clip((2.5 - body.d(C)) / 1.5, 0, 1)
            hang = (1 - onb) * (sf > 0)
            Tt = np.maximum(Tt, 0.7 * hang)
            W = np.maximum(W, Tt * 1.05)
            C = C - Uv * (sh.get('tipsink', 0.25) * tf * np.clip(1 - (Lr - s) / 2.5, 0, 1) ** 1.5)[:, None]
        ga = np.where(sf < 0, sh.get('amp_cap', GAMP_CAP), gamp)
        ga = ga + (gamp - ga) * np.clip((sf + 1.5) / 3.0, 0, 1)
        amp = ga * gate * np.clip(0.3 + 0.7 * s / 0.6, 0, 1) * np.clip((Lr - s) / 3.0, 0, 1) * gfade
        if DBG:
            mc = sf < 0
            print('%s r%d  cap W med %.2f min %.2f max %.2f | fall W med %.2f T med %.2f | L %.1f sf_end %.1f' % (
                sh['name'], ri, np.median(W[mc]) if mc.any() else 0, W[mc].min() if mc.any() else 0, W[mc].max() if mc.any() else 0,
                np.median(W[~mc]), np.median(Tt[~mc]), Lr, sf[-1]))
        # combed strands: a groove on the ribbon centre line and one at each boundary with the neighbours (~0.5-0.8 pitch)
        add_ribbon(H, C, Uv, W, Tt, amp, nstr=sh['nstr'], pexp=sh.get('pexp', 2.0), k=0.32, pitch=PITCH, gph=0.0, sig=0.24)
    # under-layer on the fall so the sheet never shows gaps between ribbons
    M = 0.5 * (G[0] + G[-1])
    s = arclen(M); s_ex = s[Nc - 1]
    T, Uv, S = frames(M, s - s_ex, body, cs, sh.get('nmode', 'cam'))
    dG = G[-1] - G[0]
    lat = np.linalg.norm(dG - T * np.sum(dG * T, axis=1)[:, None], axis=1)
    m = (s > s_ex + 1.0) & (s < s[-1] - sh.get('under_end', 4.0))
    if m.sum() > 3:
        Wm = np.clip(0.5 * lat * 0.85, 0.5, 3.5)
        add_ribbon(H, (M - Uv * 0.3)[m], Uv[m], Wm[m], np.full(m.sum(), sh.get('under_t', 0.45)), 0.0, nstr=1, pexp=2.0, k=0.3)


def back_mass(H, body, cs):
    """Smooth hair volume from the nape down the upper back (under the back sheets): a finished curtain."""
    ctrl = np.array([P((0.0, -5.0, -3.0)), (-18.8, 28.0, 78.5), (-19.2, 30.0, 72.0), (-19.4, 30.8, 66.0), (-19.4, 31.0, 61.5)])
    C = resample(catmull(ctrl, per=12), 90)
    s = arclen(C)
    T, U, S = frames(C, s, body, cs)
    U = unit_rows(np.where((U[:, 1:2] > 0), U, -U))
    L = s[-1]
    Wd = np.interp(s, [0, 5, 12, L - 6, L], [3.5, 5.5, 6.8, 6.0, 3.5])
    Tt = np.interp(s, [0, 5, L - 4, L], [1.4, 1.2, 1.0, 0.6])
    add_ribbon(H, C - U * 0.4, U, Wd, Tt, 0.0, nstr=1, pexp=2.0, k=0.6)


def cap_volume(Hc):
    B = Batch()
    r = CAP_R - CAP_SHRINK
    B.ellipsoid(P(CAP_C), tuple(r), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=0)
    B.ellipsoid(P((-3.6, -2.4, 0.4)), (3.9, 5.0, 5.4), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=2.0)    # her right, swept volume
    B.ellipsoid(P((2.4, -3.2, -1.2)), (2.6, 4.2, 4.4), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=2.0)    # her left
    B.ellipsoid(P((0.0, -4.6, -4.2)), (4.4, 2.8, 3.4), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=2.0)    # nape
    B.ellipsoid(P((-4.6, 0.3, 4.4)), (3.1, 4.0, 2.6), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=3.0)      # her right front lobe (rounded roll beside the part)
    B.ellipsoid(P((3.7, 0.0, 4.1)), (2.2, 3.6, 2.2), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=2.0)       # her left front lobe
    Hc.apply(B)


def _drop_islands(H):
    from scipy import ndimage
    lab, n = ndimage.label(H.G < 0)
    if n <= 1:
        return
    cnt = np.bincount(lab.ravel()); cnt[0] = 0
    keep = np.argmax(cnt)
    m = (lab > 0) & (lab != keep)
    H.G[m] = np.abs(H.G[m]) + H.h


LAST_BODY = None


def build_hair(S):
    global LAST_BODY
    import os
    body = Body()
    LAST_BODY = body
    gate = detail_gate(S.h)
    Hc = S.blank()
    cap_volume(Hc)
    if os.environ.get('HEAD_VALLEY') == '1':
        # (off: any valley in the cap volume exposes a smooth strip of cap between the thin ribbon roots; the part is
        # the seam where the combed strands of both sides diverge)
        # parting: only a gentle depression (~0.22 deep, ~2 mm wide, wide-radius cut so it has no flat floor) under the
        # ribbon roots; the part itself is the seam where the combed strands of both sides diverge
        th = np.linspace(32, 88, 29)
        pl = np.array([cap_local(-10.0, t) for t in th])
        nrm = (pl - CAP_C) / CAP_R ** 2; nrm /= np.linalg.norm(nrm, axis=1)[:, None]
        fade = np.interp(th, [32, 42, 76, 88], [0.0, 1.0, 1.0, 0.2])
        RV, dv = 2.5, 0.22 * fade
        pv = pl - nrm * (CAP_SHRINK - (RV - dv))[:, None]
        Bv = Batch()
        Bv.tube(np.array([P(p) for p in pv]), np.full(len(th), RV), k=0.8)
        Hc.apply(Bv, 'sub')
    # projection surface = hair cap volume U skull/face, so locks over the forehead lie ON the skin (hairline stands proud)
    Hs = S.blank(); Hs.G = np.minimum(Hc.G, S.G)
    cs = Sampler(Hs)
    H = S.blank()
    import os
    skip = set(os.environ.get('HEAD_SKIP', '').split(','))
    for sh in SHEETS:
        if sh['name'] in skip:
            continue
        build_sheet(H, body, cs, sh, gate, S.h)
    # hidden hair mass behind the front columns, closing see-through slits between the hair and the neck
    Bf = Batch()
    Bf.rcone((-18.0, 25.0, 82.5), (-19.0, 27.6, 72.0), 2.2, 2.0, k=1.0)          # nape mass under the back curtain
    Bf.rcone((-14.6, 25.4, 82.0), (-13.6, 26.8, 73.0), 1.9, 1.7, k=1.0)          # her left nape mass (no channel behind the neck)
    # pad under the flare over her right shoulder (no see-through holes between the locks; one heavy mass)
    # (set back behind the locks and hard-unioned, so the valleys between the locks stay dark grooves)
    Bf.tube(np.array([(-24.5, 24.6, 78.6), (-27.5, 25.4, 77.0), (-30.5, 25.9, 75.4), (-32.8, 25.8, 73.8), (-33.8, 25.0, 71.8),
                      (-34.0, 24.0, 69.8)]), [1.2, 1.2, 1.1, 0.95, 0.8, 0.7], k=0.4)
    H.apply(Bf, 'union')
    H.combine(Hc, 'union', 0.3)
    del Hc
    # parting: a fine V crease where the hair of both sides rolls down into it (the ribbon roots sink toward the part);
    # only a thin tube is cut, so no flat lit floor (which read as a raised rib), fading at both ends
    th = np.linspace(37, 86, 26)
    pl = np.array([cap_local(-9.0, t) for t in th])
    nrm = (pl - CAP_C) / CAP_R; nrm /= np.linalg.norm(nrm, axis=1)[:, None]
    RP = 0.32
    dep = np.interp(th, [37, 44, 74, 86], [0.05, 0.14, 0.12, 0.0]) + 0.5
    pl = pl + nrm * (RP - dep - 0.6)[:, None]          # crease bottom ~0.3 below the cap-volume top (CAP - 0.6)
    Pt = Batch()
    Pt.tube(np.array([P(p) for p in pl]), np.interp(th, [37, 44, 74, 86], [0.15, 0.22, 0.22, 0.12]), k=0.2)
    if os.environ.get('HEAD_SLOT') == '1':
        H.apply(Pt, 'sub')
    # face window: the hair thins to nothing over ~1.4 mm toward the face (feathered hairline, no overhanging lip)
    Wn = Batch()
    Wn.ellipsoid(P((0.3, 7.6, -2.3)), (3.75, 7.0, 6.3), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=0.0)
    Wf = S.blank(); Wf.apply(Wn)
    tw = np.clip((0.9 - Wf.G) / 1.5, 0.0, 1.0)
    H.G += (2.2 * tw * tw * (3 - 2 * tw)).astype(np.float32)
    del Wf
    _drop_islands(H)
    S.combine(H, 'union', 0.35)
    return S


def debug_paths():
    """Return {sheet: [guide world polylines]} for overlay checks (no SDF)."""
    from sdf import Field
    body = Body()
    F = Field((-45, -5, 50), (15, 50, 108), 0.4)
    Hc = F.blank(); cap_volume(Hc)
    cs = Sampler(Hc)
    out = {}
    for sh in SHEETS:
        off = sh['tf'] * sh.get('offk', 0.55)
        out[sh['name']] = [guide_path(body, cs, ca, fl, off, SINK, 110, 130) for ca, fl in sh['guides']]
    return out
