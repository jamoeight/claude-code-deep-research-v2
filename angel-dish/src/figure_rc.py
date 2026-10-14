"""Figure helpers: evaluate Batch SDFs at points, ray-cast reference-camera pixels onto them,
and turn traced pixel polylines into surface curves (for ridges / grooves of drapery)."""
import math
import numpy as np
from numba import njit, prange
from sdf import prim_dist, _smin, Batch, catmull, resample
import cam

_loc, _fwd, _right, _up = cam.frame()
_C = cam.load()
_W, _H = _C['w'], _C['h']
_F = _C['lens'] / 36.0 * _W


def merge(*batches):
    """Concatenate batches (keeps per-primitive k, order preserved)."""
    out = Batch()
    for b in batches:
        out.kinds += b.kinds; out.params += b.params; out.bounds += b.bounds; out.ks += b.ks
    return out


def _arr(B):
    return (np.array(B.kinds, np.int64), np.array(B.params, np.float64), np.array(B.ks, np.float64))


@njit(parallel=True, fastmath=True)
def _eval(kinds, params, ks, P, out):
    for i in prange(P.shape[0]):
        x = P[i, 0]; y = P[i, 1]; z = P[i, 2]
        a = 50.0
        for n in range(kinds.shape[0]):
            d = prim_dist(kinds[n], params[n], x, y, z)
            a = _smin(a, d, ks[n])
        out[i] = a


def sdf_eval(B, P):
    P = np.ascontiguousarray(np.atleast_2d(P), np.float64)
    out = np.empty(len(P)); k, p, kk = _arr(B)
    _eval(k, p, kk, P, out)
    return out


def normals(B, P, e=0.05):
    P = np.atleast_2d(np.asarray(P, float))
    n = np.zeros_like(P)
    for i in range(3):
        d = np.zeros(3); d[i] = e
        n[:, i] = sdf_eval(B, P + d) - sdf_eval(B, P - d)
    return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)


def project_to_surface(B, P, iters=6):
    P = np.array(np.atleast_2d(P), float)
    for _ in range(iters):
        d = sdf_eval(B, P); n = normals(B, P)
        P = P - n * d[:, None]
    return P


def rays(uv):
    uv = np.atleast_2d(np.asarray(uv, float))
    dx = (uv[:, 0] - _W / 2) / _F; dy = -(uv[:, 1] - _H / 2) / _F
    d = _fwd[None] + dx[:, None] * _right[None] + dy[:, None] * _up[None]
    return d / np.linalg.norm(d, axis=1, keepdims=True)


def cast(B, uv, t0=120.0, t1=400.0):
    """Sphere-trace reference-camera rays through pixels uv onto the batch surface.
    Returns points (nan where missed)."""
    D = rays(uv); n = len(D)
    t = np.full(n, t0); hit = np.zeros(n, bool); alive = np.ones(n, bool)
    for _ in range(400):
        idx = np.where(alive)[0]
        if len(idx) == 0:
            break
        P = _loc[None] + D[idx] * t[idx, None]
        d = sdf_eval(B, P)
        h = d < 0.01
        hit[idx[h]] = True; alive[idx[h]] = False
        t[idx[~h]] += np.maximum(d[~h] * 0.9, 0.03)
        far = t > t1; alive &= ~far
    P = _loc[None] + D * t[:, None]
    P[~hit] = np.nan
    return P


def trace(B, pix, n=None, per=10, step=1.2):
    """Pixel polyline -> 3D surface polyline (smoothed, resampled ~step units)."""
    pix = np.asarray(pix, float)
    dense = catmull(pix, per=per)
    P = cast(B, dense)
    ok = ~np.isnan(P[:, 0])
    P = P[ok]
    if len(P) < 2:
        return P
    L = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
    m = n if n else max(3, int(L / step) + 1)
    return resample(P, m)


def ridge(Bout, base, P, r, depth=0.35, k=1.0, taper=(0.35, 0.35), rmin=0.5):
    """Tube of radius r along surface polyline P, sunk `depth*r` into the surface of `base`."""
    if len(P) < 2:
        return
    N = normals(base, P)
    m = len(P); s = np.linspace(0, 1, m)
    a, b = taper
    env = np.minimum(np.clip(s / max(a, 1e-6), 0, 1), np.clip((1 - s) / max(b, 1e-6), 0, 1)) if (a or b) else np.ones(m)
    env = np.sin(env * math.pi / 2) ** 0.8
    rr = np.maximum(r * (0.25 + 0.75 * env) if np.ndim(r) == 0 else np.asarray(r) * (0.25 + 0.75 * env), rmin)
    C = P - N * (rr * depth)[:, None] if np.ndim(depth) == 0 else P - N * (rr * np.asarray(depth))[:, None]
    for i in range(m - 1):
        Bout.rcone(C[i], C[i + 1], rr[i], rr[i + 1], k)


def groove(Bout, base, P, r, lift=0.45, k=0.8, taper=(0.3, 0.3)):
    """Subtractive tube centred `lift*r` outside the surface (use with op='sub')."""
    if len(P) < 2:
        return
    N = normals(base, P)
    m = len(P); s = np.linspace(0, 1, m)
    a, b = taper
    env = np.minimum(np.clip(s / max(a, 1e-6), 0, 1), np.clip((1 - s) / max(b, 1e-6), 0, 1))
    env = np.sin(env * math.pi / 2)
    rr = np.maximum(r * (0.2 + 0.8 * env), 0.3)
    lf = lift + (1.0 - env) * 0.6        # ends rise out of the surface -> groove fades
    C = P + N * (rr * lf)[:, None]
    for i in range(m - 1):
        Bout.rcone(C[i], C[i + 1], rr[i], rr[i + 1], k)


def _env(m, taper):
    s = np.linspace(0, 1, m); a, b = taper
    e = np.minimum(np.clip(s / max(a, 1e-6), 0, 1), np.clip((1 - s) / max(b, 1e-6), 0, 1))
    return np.sin(e * math.pi / 2)


def band(Bout, base, P, w, height, t=None, k=1.2, taper=(0.3, 0.3), N=None, skew=0.0):
    """Flat soft ridge lying on the surface: elliptic section (half-width w in the surface,
    half-thickness t along the normal), top `height` above the base surface.
    skew shifts the band sideways (in units of w) to make one flank steeper."""
    if len(P) < 2:
        return
    if N is None:
        N = normals(base, P)
    m = len(P); env = _env(m, taper)
    t = (w * 0.45) if t is None else t
    T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
    side = np.cross(N, T)
    ww = np.maximum(w * (0.35 + 0.65 * env), 0.5)
    tt = np.maximum(t * (0.35 + 0.65 * env), 0.45)
    hh = height * env
    C = P + N * (hh - tt)[:, None] + side * (skew * ww)[:, None]
    for i in range(m - 1):
        up = N[i] + N[i + 1]
        Bout.eseg(C[i], C[i + 1], up, ww[i], ww[i + 1], tt[i], tt[i + 1], k)


def channel(Bout, base, P, w, depth, t=None, k=0.8, taper=(0.3, 0.3), N=None):
    """Subtractive soft valley (use op='sub'): elliptic section centred above the surface so that
    it digs `depth` into it."""
    if len(P) < 2:
        return
    if N is None:
        N = normals(base, P)
    m = len(P); env = _env(m, taper)
    t = (w * 0.6) if t is None else t
    T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
    ww = np.maximum(w * (0.3 + 0.7 * env), 0.4)
    tt = np.maximum(t * (0.5 + 0.5 * env), 0.4)
    dd = depth * env
    C = P + N * (tt - dd)[:, None]
    for i in range(m - 1):
        up = N[i] + N[i + 1]
        Bout.eseg(C[i], C[i + 1], up, ww[i], ww[i + 1], tt[i], tt[i + 1], k)


def ridge2(Bout, base, P, r, height, k=1.0, taper=(0.3, 0.3), rmin=0.6, N=None, rfloor=0.55, hpow=0.8):
    """Tube ridge whose crest height fades to zero at both ends (no sausage tips)."""
    if len(P) < 2:
        return
    if N is None:
        N = normals(base, P)
    m = len(P); env = _env(m, taper)
    rr = np.maximum(r * (rfloor + (1 - rfloor) * env), rmin)
    hh = height * env ** hpow
    C = P - N * (rr - hh)[:, None]
    for i in range(m - 1):
        Bout.rcone(C[i], C[i + 1], rr[i], rr[i + 1], k)


def groove2(Bout, base, P, r, depth, k=0.8, taper=(0.3, 0.3), N=None, rfloor=0.6):
    """Subtractive tube (op='sub') digging `depth` into the base, fading to zero depth at the ends."""
    if len(P) < 2:
        return
    if N is None:
        N = normals(base, P)
    m = len(P); env = _env(m, taper)
    rr = r * (rfloor + (1 - rfloor) * env)
    dd = depth * env
    C = P + N * (rr - dd)[:, None]
    for i in range(m - 1):
        Bout.rcone(C[i], C[i + 1], rr[i], rr[i + 1], k)
