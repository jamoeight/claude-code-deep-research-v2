"""Satin-fold displacement fields for the drapery dish.

Folds are level sets of a scalar phase field P (fold units: P increases by 1 from one fold valley to the
next).  A vortex term n*theta/(2*pi) (single-valued mod 1 because n is an integer) plus a log-radius term
makes the wall folds flow continuously into a whirlpool (clockwise-inward as seen from the front);
smooth single-valued perturbations make the pitch and course of every fold irregular.  Fine combed
striations are a higher harmonic of the same phase, so they always run along the fold flow.
"""
import math
import numpy as np


def smoothstep(x, a, b):
    t = np.clip((np.asarray(x, float) - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def noise2(u, v, seed, f=1.0):
    """cheap smooth 2D pseudo-noise in [-1, 1] (sum of rotated sines)."""
    rs = np.random.default_rng(seed)
    out = 0.0
    wsum = 0.0
    for k in range(4):
        a = rs.random() * math.pi
        fr = f * (0.6 + 0.9 * k + 0.3 * rs.random())
        ph = rs.random() * 6.283
        w = 1.0 / (1.0 + k)
        out = out + w * np.sin(fr * (u * math.cos(a) + v * math.sin(a)) + ph)
        wsum += w
    return out / wsum


def profile(t, crest=0.42, sharp=0.62):
    """Asymmetric fold profile over one period t in [0,1): 0 at the valleys (tight crease), broad rounded
    crest at `crest` (crest < 0.5: steep underside, long gentle upper face)."""
    t = np.mod(t, 1.0)
    # warp so the crest lands at `crest`
    a = (0.5 - crest) / 0.13 * 0.9 / 0.9
    a = np.clip(a, -0.95, 0.95)
    w = t + a * np.sin(2 * math.pi * t) / (2 * math.pi)
    base = 0.5 - 0.5 * np.cos(2 * math.pi * w)
    return base ** sharp


def roll(t, c=0.6, top=0.55, crease=0.07):
    """'rolled band' fold profile over one period (t increasing upward): from the crease at t=0 the band's
    underside rises with bounded slope (printable) to a round crest at t=c, then its top rolls over and drops
    steeply back into the next crease at t=1 (an upward-facing face, also printable)."""
    t = np.mod(t, 1.0)
    rise = np.sin(0.5 * math.pi * np.clip(t / c, 0, 1))
    u = np.clip((t - c) / (1 - c), 0, 1)
    fall = np.clip(1 - u ** 2, 0, 1) ** top
    # soft crease: a narrow rounded notch instead of a zero-width slit (no aliasing, printable)
    cr = smoothstep(t, 0.0, crease) * smoothstep(1.0 - t, 0.0, crease)
    return np.where(t < c, rise, fall) * (0.25 + 0.75 * cr) if crease > 0 else np.where(t < c, rise, fall)


def striae(P, U, V, seed, amp, m=7):
    """fine combed striations running along the folds (level sets of P): two harmonics of the fold phase
    (integer multiples keep them continuous) with soft, patchy strength -- brushed velvet, not lathe rings."""
    am = np.clip(0.05 + 0.95 * noise2(U, V, seed, 0.05) + 0.3 * noise2(U, V, seed + 1, 0.16), 0.0, 1.0)
    ph = 0.8 * noise2(U, V, seed + 2, 0.12)
    return amp * am * (np.sin(2 * math.pi * m * P + ph) + 0.5 * np.sin(2 * math.pi * (m + 3) * P - 0.7 * ph))


def _sp(x, w):
    """softplus of width w (smooth max(x, 0))."""
    return w * np.logaddexp(0.0, np.asarray(x, float) / w)


# ------------------------------------------------------------------ front + right outer wall
# eye of the whirlpool scroll at arc length sv, height zv (~ (32,-56,7.5));  the twirl rotates the far field about
# the eye by B*exp(-(r/Rt)^2) + B1*exp(-(r/Rt1)^2) (r measured with the s axis squeezed by sq).
VORTEX = dict(sv=29.0, zv=10.5, B=2.4, Rt=8.5, B1=2.3, Rt1=21.0, sq=1.28, Rd=23.0, dome=4.6, eye=7.5, re=3.0,
              slL=0.10, H=46.0, L=48.0, lamL=10.8, p0=1.10, lamR=10.2, A=4.2, Ar=3.9)


def far_phase(S, Z):
    """phase of the un-twisted far field: broad bands, nearly level along the front with a gentle fall toward the
    scroll; on the right they climb in long curves to the right rim (fold units)."""
    V = VORTEX
    ds = S - V['sv']
    zc = V['slL'] * _sp(-ds, 9.0) + V['H'] * (1 - np.exp(-_sp(ds, 10.0) / V['L']))
    zc = zc + 1.6 * noise2(S, 0.3 * Z, 81, 0.045) + 0.6 * noise2(S, Z, 82, 0.11)      # wavy irregular course
    # S-sweep of the right-wall bands (they bow as they come down from the rim toward the scroll)
    zc = zc + 3.2 * smoothstep(ds, 12.0, 30.0) * np.sin((S - 40.0) / 13.0 + 0.04 * Z)
    lam = V['lamL'] + (V['lamR'] - V['lamL']) * smoothstep(S, 28.0, 62.0)
    lam = lam * (1 + 0.15 * noise2(S, Z, 83, 0.04))                                   # irregular pitch
    lam = lam * (1 + 0.42 * np.exp(-((S - V['sv'] - 2.0) / 18.0) ** 2 - ((Z - V['zv'] - 9.0) / 11.0) ** 2))   # fat scroll arch
    W = Z - zc
    return W / lam + 0.05 * np.sin(0.45 * W + 0.03 * S)


def twirl(S, Z):
    """coordinate warp of the vortex: points are rotated about the eye by beta(r) (bounded, so the field stays
    continuous everywhere -- no branch cut).  Returns the pre-image coordinates (S', Z') and the radius r."""
    V = VORTEX
    u = (S - V['sv']) / V['sq']; v = Z - V['zv']
    r = np.hypot(u, v)
    be = V['B'] * np.exp(-(r / V['Rt']) ** 2) + V['B1'] * np.exp(-(r / V['Rt1']) ** 2)
    cb = np.cos(be); sb = np.sin(be)
    u2 = u * cb - v * sb; v2 = u * sb + v * cb
    return V['sv'] + V['sq'] * u2, V['zv'] + v2, r


def front_phase(S, Z):
    V = VORTEX
    S2, Z2, r = twirl(S, Z)
    Pc = far_phase(np.array([V['sv']]), np.array([V['zv']]))[0]
    return far_phase(S2, Z2) - Pc + VORTEX['p0'], S2, Z2, r


def front_disp(S, Z, fine=False, parts=False):
    """outward displacement (design units) of the front/right outer wall at arc length S, height Z.
    parts=True also returns the vortex body, the folds and the local fold amplitude (crest value)."""
    V = VORTEX
    P, S2, Z2, r = front_phase(S, Z)
    # all modulations live in the pre-image coordinates, so they twist along with the folds
    right = smoothstep(S2, V['sv'] + 8.0, V['sv'] + 30.0)
    A = V['A'] * np.clip(1 + 0.22 * noise2(S2, Z2, 21, 0.05) + 0.10 * noise2(S2, Z2, 22, 0.15), 0.6, 1.4)
    Ar = V['Ar'] * np.clip(1 + 0.30 * noise2(S2, Z2, 23, 0.06) + 0.1 * noise2(S2, Z2, 24, 0.17), 0.55, 1.45)
    Aloc = (1 - right) * A + right * Ar
    Aloc = Aloc * (1 - 0.5 * (1 - smoothstep(r, 8.0, 18.0)) * smoothstep(r, 2.0, 5.0))   # smooth convex scroll body, few creases
    # broad satin band: tight crease, steep (<=45 deg) underside, round crest low in the band, long convex upper face
    band = profile(P, crest=0.40, sharp=0.55)
    # a shallower secondary fold inside some bands (patchy): 2-3 big bands become 4-5 of varying width
    sec = np.clip(0.5 + 0.9 * noise2(S2, Z2, 25, 0.035), 0.0, 1.0) * 0.32
    band = band * (1 - sec * (1 - profile(2.0 * P + 0.15, crest=0.45, sharp=0.7)))
    # inside the whirl the arms become fat round rolls
    wv = 1 - smoothstep(r, 14.0, 24.0)
    band = (1 - wv) * band + wv * profile(P, crest=0.5, sharp=0.85)
    # right wall: rounder, softer satin bands (no pleat look)
    band = (1 - right) * band + right * (0.85 * profile(P, crest=0.45, sharp=0.8) + 0.15 * band)
    folds = Aloc * band
    # a narrow dark crease along every main fold valley (deep shadow line between satin rolls)
    tq = np.mod(P, 1.0); tq = np.minimum(tq, 1.0 - tq)
    lamloc = V['lamL'] * (1 - right) + V['lamR'] * right
    nw, nd = (0.75, 1.0) if fine else (1.1, 0.85)          # notch must stay wider than ~2 voxels
    folds = folds - nd * np.exp(-(tq * lamloc / (nw * (1 + 0.6 * right))) ** 2) * smoothstep(r, 3.0, 8.0) * (1 - 0.25 * right)
    # vortex body: convex dome with a deep eye
    q = r / V['Rd']
    dome = np.where(q < 1, (1 - q * q) ** 2, 0.0)
    body = V['dome'] * dome - V['eye'] * np.exp(-(r / V['re']) ** 2)
    folds = folds * (0.45 + 0.55 * smoothstep(r, 1.0, 5.0))
    D = folds + body
    if fine:
        D = D + striae(P, S2, Z2, 31, 0.05, m=9) * smoothstep(r, 5.0, 10.0)
    if parts:
        return D, body, folds, Aloc * (0.45 + 0.55 * smoothstep(r, 1.0, 5.0))
    return D


# ------------------------------------------------------------------ back base wall (behind / under the wings)
def back_disp(S, Z, fine=False):
    P = (Z + 0.45 * (S - 130.0)) / 9.0 + 0.5 * noise2(S, Z, 41, 0.045) + 0.15 * noise2(S, Z, 42, 0.15)
    A = 2.8 * np.clip(1 + 0.45 * noise2(S, Z, 43, 0.04), 0.3, 1.5)
    D = A * profile(P, crest=0.5, sharp=0.7)
    if fine:
        D = D + striae(P, S, Z, 44, 0.09)
    return D


# ------------------------------------------------------------------ interior folds (height-field bumps, normal units)
# front-left: 5 irregular nested cloth rolls (C-arcs open toward the bowl centre) round the pendant spot
WHIRL = dict(cx=-35.0, cy=-8.0)
_ARCS = [  # r0, half-width, height, start angle, end angle (deg from +x, ccw), spiral (units/turn), skew, centre offset
    (8.0, 2.7, 2.8, 75.0, 295.0, 2.5, 0.3, (0.8, -0.6)),
    (13.2, 3.2, 4.2, 52.0, 322.0, 3.5, 0.4, (-0.5, 0.9)),
    (18.8, 2.9, 3.6, 84.0, 290.0, 2.0, 0.35, (1.2, 0.4)),
    (24.4, 3.4, 4.6, 46.0, 333.0, 4.0, 0.45, (-1.0, -1.2)),
    (30.2, 3.0, 3.2, 64.0, 302.0, 2.5, 0.35, (0.6, 1.5)),
]


def _arc_rolls(X, Y, u):
    cx, cy = WHIRL['cx'], WHIRL['cy']
    rw = np.hypot(X - cx, Y - cy)
    out = np.zeros_like(X)
    for i, (r0, w, hgt, a0, a1, spi, sk, (ox, oy)) in enumerate(_ARCS):
        dx = X - cx - ox; dy = Y - cy - oy
        ri_ = np.hypot(dx, dy)
        th = np.degrees(np.mod(np.arctan2(dy, dx), 2 * math.pi))      # 0..360 from +x
        # each roll wanders: radius drifts along the arc (slight spiral + noise), width and height swell
        ri = r0 + spi * (th - 180.0) / 360.0 + 2.0 * noise2(X, Y, 90 + i, 0.05) + 0.9 * np.sin(np.radians(th) * 2.0 + 1.7 * i)
        wi = w * np.clip(1 + 0.3 * noise2(X, Y, 100 + i, 0.06), 0.6, 1.4)
        d = (ri_ - ri) / wi
        # skewed rounded roll: steeper on the inside (toward the centre), longer slope outside
        d = np.where(d < 0, d * (1 + sk), d * (1 - 0.5 * sk))
        prof = np.clip(1 - d * d, 0, 1) ** 0.7
        # tapered ends (each roll starts / stops at its own angle; ends overlap the neighbours)
        e = smoothstep(th, a0 - 16.0, a0 + 26.0) * (1 - smoothstep(th, a1 - 26.0, a1 + 16.0))
        hh = hgt * np.clip(1 + 0.3 * noise2(X, Y, 110 + i, 0.05), 0.5, 1.4)
        v = hh * prof * e
        out = np.maximum(out, v) + 0.25 * np.minimum(out, v)
    # smooth floor in the centre, strongest on the inner-wall slope, fade on the open floor and before the wing face
    env = smoothstep(rw, 5.0, 9.0) * (0.62 + 0.38 * (1 - smoothstep(u, 0.35, 0.9)))
    env = env * smoothstep(X, -47.0, -42.5) * (1 - smoothstep(rw, 33.0, 39.0))
    return out * env, smoothstep(rw, 30.0, 38.0)


def interior_folds(X, Y, ph, rho, u, fine=False):
    out = np.zeros_like(X)
    # --- skirt train: 4-5 broad, irregular satin folds leaving the skirt's right hem and sweeping across the floor
    #     in long S-curves toward the front-right and the right rim, climbing the right inner wall diagonally
    fx, fy = 0.0, 10.0
    dxs = X - fx; dys = Y - fy
    dist = np.hypot(dxs, dys)
    ang = np.degrees(np.arctan2(dys, dxs))
    ang = ang + 9.0 * np.sin(dist / 16.0 + 0.8) - 0.18 * dist            # S-sweep, curving toward the front
    dA = 23.0 * (1 + 0.35 * noise2(X * 0.5, Y * 0.5, 57, 0.03))       # irregular spacing (+-35..40 %)
    Pt = ang / dA + 0.30 * noise2(X, Y, 51, 0.035) + 0.08 * noise2(X, Y, 52, 0.12)
    wt = DF_s(dist, 16.0, 26.0) * DF_s(ang, -95.0, -75.0) * (1 - DF_s(ang, 28.0, 48.0))
    At = 2.3 * np.clip(1 + 0.45 * noise2(X, Y, 53, 0.035) + 0.2 * noise2(X, Y, 56, 0.11), 0.35, 1.5)
    near = np.exp(-((dist - 24.0) / 14.0) ** 2)
    wall = 1 - smoothstep(u, 0.35, 0.95)
    env = np.clip(0.25 + 0.75 * near + 0.75 * wall, 0, 1.15)
    along = np.clip(0.75 + 0.6 * noise2(dist * 0.8, Pt * 5.0, 58, 0.18), 0.2, 1.2)   # folds swell and fade
    ft = At * env * along * profile(Pt, crest=0.5, sharp=0.9)
    if fine:
        ft = ft + striae(Pt, X, Y, 55, 0.035, 9) * wall
    out += ft * wt
    # --- right inner wall under the wing tip: 3-4 long crisp satin folds running from the rim down to the floor
    #     (from about (78,-5,28) toward (30,-10,9))
    zr = (1 - u)
    Pr = (np.radians(ph) * 78.0 - 9.0 * zr) / 11.0 + 0.35 * noise2(X, Y, 71, 0.04) + 0.1 * noise2(X, Y, 73, 0.13)
    wr = DF_s(ph, -40.0, -26.0) * (1 - DF_s(ph, 14.0, 30.0)) * DF_s(zr, 0.08, 0.35)
    fr = 1.8 * profile(Pr, crest=0.5, sharp=0.7) * np.clip(0.8 + 0.45 * noise2(X, Y, 72, 0.05), 0.3, 1.3)
    if fine:
        fr = fr + striae(Pr, X, Y, 75, 0.035, 7)
    wr = wr * (1 - 0.7 * wt)
    out += fr * wr
    # --- back inner wall (behind the figure / under the right wing): 2-3 broad soft swags, no fluting
    arc = np.radians(ph) * 50.0
    Pb = (zr * 14.0 - 0.55 * arc) / 19.0 + 0.30 * noise2(X, Y, 81, 0.03) + 0.08 * noise2(X, Y, 82, 0.1)
    wb = DF_s(ph, 30.0, 52.0) * (1 - DF_s(ph, 168.0, 182.0)) * DF_s(zr, 0.1, 0.35) * (1 - DF_s(zr, 0.75, 0.97)) * (1 - 0.8 * wt)
    fb = 1.5 * profile(Pb, crest=0.5, sharp=1.0) * np.clip(0.75 + 0.45 * noise2(X, Y, 83, 0.04), 0.25, 1.3)
    out += fb * wb
    # --- front-left whirlpool rolls (replace whatever else is there)
    fw, wsw = _arc_rolls(X, Y, u)
    cx, cy = WHIRL['cx'], WHIRL['cy']
    inwhirl = 1 - smoothstep(np.hypot(X - cx, Y - cy), 30.0, 40.0)
    out = out * (1 - inwhirl) + fw
    return out


def DF_s(x, a, b):
    return smoothstep(x, a, b)
