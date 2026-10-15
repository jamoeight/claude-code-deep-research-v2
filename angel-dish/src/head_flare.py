"""Her right (viewer-left) shoulder flare, round 3c3: an upper convex S-lobe of combed hair leaving the side/back of the
head and curling under, and three long thick rope locks running out nearly horizontally over the top of the shoulder,
turning down onto the back of the upper arm.  All of them lie on a smooth hair core (no cave, no crumpled ruffle);
the gaps between neighbouring ropes are recessed fillers (dark grooves, never slots).  Paths traced on the photo
(ref_flare / g2 grid) at chosen depth planes."""
import math
import numpy as np
from sdf import Batch, catmull, resample
from head_k import add_ribbon
import cam

CAMLOC = cam.frame()[0]


def _u(px_, ys):
    return [np.array(cam.unproject(p, plane_y=y), float) for p, y in zip(px_, ys)]


def unit_rows(V):
    return V / (np.linalg.norm(V, axis=1, keepdims=True) + 1e-12)


def arclen(C):
    return np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))])


def smooth_rows(V, it=3):
    V = np.array(V, float)
    for _ in range(it):
        V[1:-1] = 0.25 * V[:-2] + 0.5 * V[1:-1] + 0.25 * V[2:]
    return V


def groove_gate(h):
    return float(np.clip((0.42 - h) / 0.12, 0.0, 1.0))


# --------------------------------------------------------------------------- paths (world)
# upper lobe: outer (silhouette) and inner combed bands of one convex wave, curling under at the bottom
# (centre lines traced ~1 lock half-width inside the photo silhouette)
LOBE = [
    dict(pts=[(-23.6, 21.0, 86.8)] + _u([(399, 200), (388, 204), (378, 212), (370, 224), (366, 237), (367, 248), (373, 255), (383, 258)],
                                        [22.6, 23.0, 23.4, 23.7, 23.9, 24.0, 23.9, 23.7]),
         w=1.15, t=0.95, nstr=4),
    dict(pts=[(-23.4, 20.4, 85.6)] + _u([(403, 212), (394, 216), (386, 226), (380, 238), (380, 248), (387, 254)],
                                        [21.9, 22.2, 22.5, 22.8, 22.8, 22.6]),
         w=1.05, t=0.9, nstr=3),
]
# three long ropes below the lobe: from behind the front column out over the top of the shoulder, turning down at the
# outer shoulder and lying on the back of the upper arm (centre lines ~ the middle of the photo's lit bands)
ROPES = [
    dict(pts=_u([(405, 258), (394, 265), (380, 265), (366, 266), (352, 269), (342, 275), (335, 284)], [23.4, 23.6, 23.9, 24.0, 24.2, 24.3, 24.4]) +
         [np.array(p) for p in [(-35.8, 24.3, 72.4), (-36.0, 24.1, 69.8), (-35.9, 23.8, 67.4)]], w=0.84, t=0.84, nstr=3, rest=0.45),
    dict(pts=_u([(403, 272), (391, 279), (374, 280), (359, 283), (347, 289), (340, 297)], [22.3, 22.5, 22.7, 22.8, 22.9, 23.1]) +
         [np.array(p) for p in [(-35.0, 23.0, 70.8), (-35.1, 22.6, 68.6), (-35.0, 22.2, 66.4)]], w=0.8, t=0.8, nstr=3, rest=0.6),
    dict(pts=_u([(401, 286), (387, 292), (371, 294), (358, 298), (350, 305)], [21.1, 21.3, 21.5, 21.7, 21.8]) +
         [np.array(p) for p in [(-33.8, 21.6, 70.2), (-34.1, 21.2, 68.2), (-34.1, 20.8, 66.4)]], w=0.76, t=0.76, nstr=2, rest=0.9),
]
LOBE_CORE = [(-23.4, 21.2, 86.0), (-25.4, 22.8, 85.0), (-27.4, 24.0, 83.0), (-28.6, 24.6, 80.8), (-28.6, 24.6, 79.0),
             (-27.6, 24.2, 78.0), (-26.2, 23.6, 77.8)]
LOBE_R = [1.2, 1.5, 1.7, 1.7, 1.5, 1.2, 0.9]


def _frames(C, core, body=None, nref=None):
    T = unit_rows(np.gradient(C, axis=0))
    # outward: from the nearest core point toward the rope, blended with the direction to the camera
    from scipy.spatial import cKDTree
    tc = unit_rows(CAMLOC[None] - C)
    if nref is not None:
        # explicit reference normals (the slab's front normal): the ropes lie flat on the slab face
        _, j = cKDTree(nref[0]).query(C)
        U = unit_rows(nref[1][j] + 0.15 * tc)
    else:
        kd = cKDTree(core)
        _, j = kd.query(C)
        out = unit_rows(C - core[j])
        U = unit_rows(0.55 * out + 0.45 * tc)
    U = unit_rows(smooth_rows(U, 20))
    U = unit_rows(U - T * np.sum(U * T, axis=1)[:, None])
    return T, U


def _rope(H, pts, w, t, nstr, core, body, gate, h, tip_rest=0.6, start_w=0.75, ltip=4.0, name='FL', centres=None, wave=None, nref=None):
    C = resample(catmull(np.array(pts, float), per=12), 160)
    s = arclen(C); L = s[-1]
    T, U = _frames(C, core, nref=nref)
    if wave is not None:
        a, lam, ph = wave
        S = unit_rows(np.cross(U, T))
        env = np.clip(s / 4.0, 0, 1) * np.clip((L - s) / 4.0, 0, 1)
        C = C + S * (a * env * np.sin(2 * math.pi * s / lam + ph))[:, None]
    tip = np.clip((L - s) / ltip, 0, 1)
    W = w * (start_w + (1 - start_w) * np.clip(s / 3.0, 0, 1)) * (0.5 + 0.5 * tip ** 0.8)
    Tt = t * (0.85 + 0.15 * np.clip(s / 3.0, 0, 1)) * (0.45 + 0.55 * tip ** 0.9)
    if body is not None and tip_rest > 0:
        # where the rope lies on the body along its run, sink it a little (fused, no near-tangent surfaces)
        dd0 = body.d(C)
        near = np.clip((1.2 - dd0) / 1.0, 0, 1)
        C = C - body.grad(C) * (0.35 * near)[:, None]
        # the end lies on the body: sink the centre so the flattened end rests on the arm (no free hook)
        dd = body.d(C)
        onb = np.clip((2.5 - dd) / 2.0, 0, 1) * (1 - tip)
        g = body.grad(C)
        C = C - g * (tip_rest * onb)[:, None]
    amp = 0.24 * gate * np.clip(s / 2.0, 0, 1) * np.clip((L - s) / 3.0, 0, 1)
    pitch = np.maximum(2.0 * W / nstr, 0.55)
    if h <= 0.34:
        add_ribbon(H, C, U, W, Tt, amp, nstr=nstr, pexp=2.0, k=0.25, pitch=pitch, gph=0.5 if nstr % 2 == 0 else 0.0, sig=0.2)
    else:
        add_ribbon(H, C, U, W, Tt, 0.0, nstr=1, pexp=2.2, k=0.3)
    if centres is not None:
        centres.append((name, C.copy(), W.copy()))
    return C, U, W, Tt


def _filler(H, A, B, depth=0.6, wx=0.3, t=0.6):
    """recessed band along the gap between two neighbouring ropes (same sample count)."""
    (C0, U0, W0, T0), (C1, U1, W1, T1) = A, B
    n = min(len(C0), len(C1))
    M = 0.5 * (C0[:n] + C1[:n]); Um = unit_rows(U0[:n] + U1[:n])
    s = arclen(M); L = s[-1]
    lat = np.linalg.norm(C0[:n] - C1[:n], axis=1)
    fr = np.clip(s / 2.0, 0, 1) * np.clip((L - s - 1.0) / 2.5, 0, 1)
    m = fr > 0.02
    if m.sum() < 4:
        return
    Tm = 0.5 * (T0[:n] + T1[:n])
    Wg = np.clip(0.5 * lat + wx, 0.4, 1.8)
    Tg = np.full(n, t)
    off = Tm + depth - Tg
    add_ribbon(H, (M - Um * off[:, None])[m], Um[m], Wg[m], Tg[m], 0.0, nstr=1, pexp=2.0, k=0.3)


def _slab(H, lines, back=1.0, ht=1.25, margin=0.9, n=160):
    """smooth slab behind a stack of ropes (the hair mass they lie on): spans the stack, sits `back` behind the ropes'
    mean line (away from the camera).  Returns (centre line, front normal, width axis, half width, half thickness)."""
    L = [resample(catmull(np.array(p, float), per=12), n) for p in lines]
    A, Cc = L[0], L[-1]
    M = np.mean(L, axis=0)
    tc = unit_rows(CAMLOC[None] - M)
    M = M - tc * back
    T = unit_rows(np.gradient(M, axis=0))
    Wd = A - Cc
    hw = 0.5 * np.linalg.norm(Wd, axis=1) + margin
    U = unit_rows(np.cross(T, unit_rows(Wd)))
    U = np.where(np.sum(U * tc, axis=1)[:, None] > 0, U, -U)
    Wa = unit_rows(np.cross(U, T))
    s = arclen(M); Ls = s[-1]
    f = np.clip(s / 2.5, 0, 1) * np.clip((Ls - s) / 3.0, 0.25, 1)
    hw = hw * (0.6 + 0.4 * f); ht_ = ht * (0.5 + 0.5 * f)
    add_ribbon(H, M, U, hw, ht_, 0.0, nstr=1, pexp=2.0, k=0.6)
    return M, U, Wa, hw, ht_


def _back_ropes(H, M, U, Wa, hw, ht, fracs, w, t, gate, h, sink=0.35, centres=None):
    """ropes on the back face of a slab / core (seen from behind: the same locks draped over the shoulder)."""
    out = []
    for fi, f in enumerate(fracs):
        C = M - U * (ht - sink)[:, None] + Wa * (hw * f)[:, None]
        C = resample(catmull(C[::8], per=8), len(C))
        s = arclen(C); L = s[-1]
        Ub = -U
        T = unit_rows(np.gradient(C, axis=0))
        Ub = unit_rows(Ub - T * np.sum(Ub * T, axis=1)[:, None])
        tip = np.clip((L - s) / 4.0, 0, 1); st = np.clip(s / 3.0, 0, 1)
        W = w * (0.6 + 0.4 * st) * (0.5 + 0.5 * tip ** 0.8)
        Tt = t * (0.6 + 0.4 * st) * (0.45 + 0.55 * tip)
        amp = 0.16 * gate * st * np.clip((L - s) / 3.0, 0, 1)
        if h <= 0.34:
            add_ribbon(H, C, Ub, W, Tt, amp, nstr=3, pexp=2.2, k=0.3, pitch=np.maximum(2 * W / 3, 0.55), gph=0.0, sig=0.2)
        else:
            add_ribbon(H, C, Ub, W, Tt, 0.0, nstr=1, pexp=2.2, k=0.3)
        out.append((C, Ub, W, Tt))
        if centres is not None:
            centres.append(('FLB', C.copy(), W.copy()))
    for a, b in zip(out[:-1], out[1:]):
        _filler(H, a, b, depth=0.65, t=0.45)
    return out


def _skirt(H, core, body, step=6, r0=1.5, r1=1.2):
    """smooth support from the core down onto the shoulder (the pile rests on the body: no cave under the ropes)."""
    B = Batch()
    for i in range(0, len(core), step):
        p0 = core[i]
        dirn = np.array([0.0, -0.1, -1.0]); dirn /= np.linalg.norm(dirn)
        for tt in np.arange(0.5, 10.0, 0.25):
            q = p0 + dirn * tt
            if body.d(q)[0] < -0.7:           # well into the body (no near-coincident surfaces -> no speckles)
                B.rcone(tuple(p0), tuple(q), r0, r1, k=1.0)
                break
    H.apply(B, 'union')


def _bundle(H, axis, rad, angles, w, t, gate, h, sink=0.3, twist=0.35, centres=None):
    """ropes wrapped around a core axis at the given angles (0 = toward the camera), slowly twisting along it."""
    T = unit_rows(np.gradient(axis, axis=0))
    tc = unit_rows(CAMLOC[None] - axis)
    N1 = unit_rows(tc - T * np.sum(tc * T, axis=1)[:, None])
    N2 = unit_rows(np.cross(T, N1))
    s = arclen(axis); L = s[-1]
    for k, a0 in enumerate(angles):
        th = a0 + twist * (s / L - 0.5)
        Ud = N1 * np.cos(th)[:, None] + N2 * np.sin(th)[:, None]
        C = axis + Ud * (rad - sink)[:, None]
        st = np.clip(s / 2.5, 0, 1); tip = np.clip((L - s) / 3.0, 0, 1)
        W = w * (0.55 + 0.45 * st) * (0.5 + 0.5 * tip)
        Tt = t * (0.55 + 0.45 * st) * (0.5 + 0.5 * tip)
        amp = 0.15 * gate * st * tip
        if h <= 0.34:
            add_ribbon(H, C, Ud, W, Tt, amp, nstr=3, pexp=2.0, k=0.3, pitch=np.maximum(2 * W / 3, 0.5), gph=0.0, sig=0.2)
        else:
            add_ribbon(H, C, Ud, W, Tt, 0.0, nstr=1, pexp=2.0, k=0.3)
        if centres is not None:
            centres.append(('FLW', C.copy(), W.copy()))


def _ride(pts, body, clear):
    """keep each control point on its camera ray, but pull it toward the camera until it clears the body by `clear`
    (the ropes ride over the shoulder whatever its exact height)."""
    out = []
    for p in pts:
        p = np.array(p, float)
        r = CAMLOC - p; r /= np.linalg.norm(r)
        for _ in range(60):
            if body.d(p)[0] >= clear:
                break
            p = p + r * 0.15
        out.append(p)
    # smooth the depth change along the rope (no kinks where the pull starts)
    P = np.array(out)
    for _ in range(2):
        P[1:-1] = 0.25 * P[:-2] + 0.5 * P[1:-1] + 0.25 * P[2:]
    P[0] = out[0]; P[-1] = out[-1]
    return [q for q in P]


def build_flare(H, body, h, centres=None):
    gate = groove_gate(h)
    ROPES_ = [dict(R, pts=_ride(R['pts'][:-3], body, R['t'] * 0.95) + R['pts'][-3:]) for R in ROPES]
    M, U, Wa, hw, ht = _slab(H, [R['pts'] for R in ROPES_], back=1.95, ht=1.3, margin=0.35)
    _skirt(H, M - U * 0.7, body, r0=1.0, r1=1.1)
    _back_ropes(H, M, U, Wa, hw, ht, (-0.62, 0.0, 0.62), 0.9, 0.85, gate, h, sink=0.2, centres=centres)
    lc = resample(catmull(np.array(LOBE_CORE, float), per=12), 100)
    sl = arclen(lc)
    B = Batch()
    rr = np.interp(sl, np.linspace(0, sl[-1], len(LOBE_R)), LOBE_R)
    B.tube(lc[::4], rr[::4], k=0.8)
    # web joining the lobe to the side of the head / nape (no see-through loop between the lobe and the head)
    B.rcone((-23.2, 21.6, 84.8), (-26.6, 23.8, 79.2), 1.7, 1.4, k=1.0)
    B.rcone((-22.6, 22.6, 83.0), (-25.6, 24.6, 78.2), 1.6, 1.4, k=1.0)
    H.apply(B, 'union')
    # lobe core seen from the side / behind: combed bands wrapped around it (sides and back)
    _bundle(H, lc, rr, np.radians([70, 120, 170, 220, 270]), 0.85, 0.75, gate, h, centres=centres)
    allcore = np.vstack([M, lc])
    lobes = [_rope(H, L['pts'], L['w'], L['t'], L['nstr'], allcore, body, gate, h, tip_rest=0.0, start_w=0.8, ltip=3.0,
                   name='FLL', centres=centres) for L in LOBE]
    ropes = [_rope(H, R['pts'], R['w'], R['t'], R['nstr'], allcore, body, gate, h, tip_rest=R['rest'], name='FLR', centres=centres,
                   nref=(M, U)) for R in ROPES_]
    for a, b in zip(lobes[:-1], lobes[1:]):
        _filler(H, a, b, depth=0.5, t=0.45)
    for a, b in zip(ropes[:-1], ropes[1:]):
        _filler(H, a, b, depth=1.05, t=0.35, wx=0.12)
