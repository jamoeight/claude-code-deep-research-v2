"""Crown combing (round 3c3): dense fine strand grooves sweeping from the parting over the convex dome, branching in
as the flow fans out (constant ~0.6-0.75 mm pitch, irregular), a narrow part seam, and the forehead roll that forms the
hairline on her right."""
import math
import numpy as np
from sdf import Batch, catmull, resample
import head
import head_hair as hh

P, D = head.P, head.D

# flow guides on the cap (phi, theta), ordered front -> back; all start on the part line
RIGHT = [
    [(hh.PART_PHI, 25), (-30, 13), (-40, 2), (-48, -8), (-54, -16)],
    [(hh.PART_PHI, 36), (-30, 22), (-44, 9), (-54, -3), (-62, -12)],
    [(hh.PART_PHI, 48), (-38, 33), (-60, 18), (-76, 4), (-88, -8)],
    [(hh.PART_PHI, 62), (-50, 48), (-84, 30), (-106, 12), (-118, -4)],
    [(hh.PART_PHI, 76), (-80, 64), (-130, 42), (-150, 20), (-158, 0)],
    [(hh.PART_PHI, 87), (-150, 78), (-170, 54), (-174, 30), (-176, 8)],
]
LEFT = [
    [(hh.PART_PHI, 34), (0, 29), (18, 23), (34, 14), (48, 4), (58, -6)],
    [(hh.PART_PHI, 48), (14, 44), (44, 36), (66, 24), (80, 10), (88, -4)],
    [(hh.PART_PHI, 62), (30, 58), (68, 46), (92, 28), (104, 10), (110, -6)],
    [(hh.PART_PHI, 76), (60, 68), (106, 48), (124, 24), (130, 4)],
    [(hh.PART_PHI, 87), (150, 80), (170, 58), (174, 32), (176, 8)],
]


def _guide_xyz(g, N):
    A = catmull(np.array(g, float), per=10)
    sa = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(A, axis=0), axis=1))])
    A = np.stack([np.interp(np.linspace(0, sa[-1], N), sa, A[:, k]) for k in range(2)], 1)
    return np.array([hh.cap_local(*a) for a in A])


def flow_lines(guides, nper, rng, N=90):
    G = [_guide_xyz(g, N) for g in guides]
    lines = []
    for i in range(len(G) - 1):
        us = (np.arange(nper) + 0.5 + rng.uniform(-0.3, 0.3, nper)) / nper
        for u in np.sort(us):
            lines.append(G[i] * (1 - u) + G[i + 1] * u)
    return lines


def _bitrev_order(n):
    order, seen = [], set()
    k = 1
    while len(order) < n:
        for j in range(k):
            i = int((2 * j + 1) * n / (2 * k))
            if i < n and i not in seen:
                seen.add(i); order.append(i)
        k *= 2
        if k > 4 * n:
            break
    order += [i for i in range(n) if i not in seen]
    return order


LAST = {}


def comb(H, side='right', seed=41, pitch=0.62, depth=0.2, sig=None):
    """fine combing grooves on the outer hair surface of the crown."""
    from scipy.spatial import cKDTree
    rng = np.random.default_rng(seed)
    hs = hh.Sampler(H)
    guides = RIGHT if side == 'right' else LEFT
    L = flow_lines(guides, 26 if side == 'right' else 18, rng)
    n = len(L); N = len(L[0])
    W = [P(l) for l in L]                       # world, on the nominal cap
    # activity: a line becomes active along t once it keeps >= pitch from every higher-priority active line
    order = _bitrev_order(n)
    act = np.zeros((n, N), bool)
    jit = rng.uniform(0.9, 1.3, n)
    for t in range(N):
        pts = np.zeros((0, 3))
        for i in order:
            p = W[i][t]
            if len(pts) == 0 or np.min(np.linalg.norm(pts - p, axis=1)) >= pitch * jit[i]:
                act[i, t] = True; pts = np.vstack([pts, p])
    pts_all, dep_all = [], []
    for i in range(n):
        a = act[i]
        # once active stay active (no flicker)
        idx = np.where(a)[0]
        if len(idx) == 0:
            continue
        t0 = idx[0]
        t1 = N - 1 - int(rng.integers(0, 12))
        if t1 - t0 < 8:
            continue
        Pw = W[i][t0:t1 + 1]
        Pw = catmull(Pw[::3], per=6) if len(Pw) > 6 else Pw
        Ls = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(Pw, axis=0), axis=1))])
        Pw = resample(Pw, max(int(Ls[-1] / 0.08), 10))
        Pw = hs.project(Pw, 0.0, it=8)
        tt = np.linspace(0, 1, len(Pw)); Lr = Ls[-1]
        taper = np.clip(tt * Lr / 1.2, 0, 1) * np.clip((1 - tt) * Lr / 1.8, 0, 1)
        pts_all.append(Pw); dep_all.append(depth * rng.uniform(0.8, 1.15) * taper ** 0.8)
    if not pts_all:
        return
    Pa = np.vstack(pts_all); Da = np.concatenate(dep_all)
    LAST[side] = (Pa, Da)
    _displace(H, Pa, Da, max(sig or 0.19, 0.8 * H.h))


def part_seam(H, depth=0.32, sig=0.22):
    hs = hh.Sampler(H)
    th = np.linspace(29, 86, 40)
    Pw = P(np.array([hh.cap_local(hh.PART_PHI, t) for t in th]))
    Pw = resample(catmull(Pw, per=6), 140)
    Pw = hs.project(Pw, 0.0, it=8)
    t = np.linspace(0, 1, len(Pw))
    dep = depth * (np.clip(t / 0.12, 0, 1) * np.clip((1 - t) / 0.25, 0, 1)) ** 0.8
    _displace(H, Pw, dep, max(sig, 0.8 * H.h))


def _displace(H, Pa, Da, sig):
    from scipy.spatial import cKDTree
    lo = np.floor((Pa.min(0) - 1.5 - H.lo) / H.h).astype(int); hi = np.ceil((Pa.max(0) + 1.5 - H.lo) / H.h).astype(int) + 1
    lo = np.clip(lo, 0, np.array(H.shape) - 1); hi = np.clip(hi, 1, H.shape)
    sub = H.G[lo[0]:hi[0], lo[1]:hi[1], lo[2]:hi[2]]
    near = np.argwhere(np.abs(sub) < 1.0)
    if len(near) == 0:
        return
    X = H.lo + (near + lo) * H.h
    d, j = cKDTree(Pa).query(X, distance_upper_bound=3.5 * sig)
    ok = np.isfinite(d)
    disp = np.zeros(len(X), np.float32)
    disp[ok] = Da[j[ok]] * np.exp(-(d[ok] / sig) ** 2)
    sub[near[:, 0], near[:, 1], near[:, 2]] += disp


def forehead_roll(Hc):
    """rounded combed roll along the hairline on her right: from the front end of the part down over the upper right
    forehead and the temple, back over the ear (its lower edge is the hairline; stands ~1 mm proud of the skin)."""
    B = Batch()
    pts = [(-1.3, 3.55, 7.3), (-2.2, 3.7, 6.5), (-3.25, 3.4, 5.6), (-4.25, 2.7, 4.6), (-5.0, 1.6, 3.6), (-5.55, 0.15, 2.6),
           (-5.85, -1.6, 1.7)]
    rad = [0.6, 0.82, 0.92, 0.98, 1.0, 1.0, 0.95]
    C = catmull(np.array(pts, float), per=6)
    s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(C, axis=0), axis=1))])
    sp = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(np.array(pts), axis=0), axis=1))])
    r = np.interp(s, sp, rad)
    B.tube(np.array([P(p) for p in C]), r, k=2.0)
    # fullness between the dome and the roll (one convex sweep, no crease above the roll)
    B.ellipsoid(P((-2.8, 2.4, 6.4)), (2.1, 2.2, 1.6), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=2.2)
    B.ellipsoid(P((-4.5, 1.0, 4.6)), (1.5, 2.0, 1.7), xaxis=D((1, 0, 0)), yaxis=D((0, 1, 0)), k=2.2)
    Hc.apply(B)
