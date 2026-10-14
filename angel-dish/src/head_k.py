"""Custom kernels for the head component (hair locks with strand grooves, sub-field helpers)."""
import math
import numpy as np
from numba import njit, prange
from sdf import Field, FAR


@njit(fastmath=True, inline='always')
def _smin(a, b, k):
    if k <= 0.0:
        return a if a < b else b
    h = k - abs(a - b)
    if h <= 0.0:
        return a if a < b else b
    h = h / k
    return (a if a < b else b) - h * h * k * 0.25


@njit(parallel=True, fastmath=True)
def _lock_segments(tmp, ox, oy, oz, h, P, U, W, T, nstr, amp, pad):
    """min-union of grooved elliptic tapered segments into tmp (a sub-block grid with origin ox,oy,oz)."""
    nx, ny, nz = tmp.shape
    for s in range(P.shape[0] - 1):
        ax = P[s, 0]; ay = P[s, 1]; az = P[s, 2]
        bx = P[s + 1, 0]; by = P[s + 1, 1]; bz = P[s + 1, 2]
        tx = bx - ax; ty = by - ay; tz = bz - az
        L = math.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
        tx /= L; ty /= L; tz /= L
        ux = 0.5 * (U[s, 0] + U[s + 1, 0]); uy = 0.5 * (U[s, 1] + U[s + 1, 1]); uz = 0.5 * (U[s, 2] + U[s + 1, 2])
        du = ux * tx + uy * ty + uz * tz
        ux -= du * tx; uy -= du * ty; uz -= du * tz
        un = math.sqrt(ux * ux + uy * uy + uz * uz) + 1e-9
        ux /= un; uy /= un; uz /= un
        sx = ty * uz - tz * uy; sy = tz * ux - tx * uz; sz = tx * uy - ty * ux
        w1 = W[s]; w2 = W[s + 1]; t1 = T[s]; t2 = T[s + 1]
        r = max(max(w1, w2), max(t1, t2)) + pad
        i0 = max(int(math.floor((min(ax, bx) - r - ox) / h)), 0); i1 = min(int(math.ceil((max(ax, bx) + r - ox) / h)) + 1, nx)
        j0 = max(int(math.floor((min(ay, by) - r - oy) / h)), 0); j1 = min(int(math.ceil((max(ay, by) + r - oy) / h)) + 1, ny)
        k0 = max(int(math.floor((min(az, bz) - r - oz) / h)), 0); k1 = min(int(math.ceil((max(az, bz) + r - oz) / h)) + 1, nz)
        for i in prange(i0, i1):
            x = ox + i * h
            for j in range(j0, j1):
                y = oy + j * h
                for kk in range(k0, k1):
                    z = oz + kk * h
                    px = x - ax; py = y - ay; pz = z - az
                    sp = px * tx + py * ty + pz * tz
                    sc = min(max(sp, 0.0), L)
                    f = sc / L
                    w = w1 + (w2 - w1) * f
                    t = t1 + (t2 - t1) * f
                    vx = px - tx * sc; vy = py - ty * sc; vz = pz - tz * sc
                    vu = vx * ux + vy * uy + vz * uz
                    vs = vx * sx + vy * sy + vz * sz
                    va = sp - sc
                    e = math.sqrt((vu / t) ** 2 + (vs / w) ** 2 + (va / w) ** 2)
                    d = (e - 1.0) * min(w, t)
                    if amp > 0.0:
                        a = min(max(vs / w, -1.0), 1.0)  # -1..1 across the lock
                        # nstr strand bundles across the width: g = 1 at bundle centres, 0 in the grooves between
                        g = 0.5 - 0.5 * math.cos(math.pi * nstr * (a + 1.0))
                        d += amp * min(1.0, w / 1.1) * (1.0 - g)
                    if d < tmp[i, j, kk]:
                        tmp[i, j, kk] = d


@njit(parallel=True, fastmath=True)
def _smin_block(G, i0, j0, k0, tmp, k):
    nx, ny, nz = tmp.shape
    for i in prange(nx):
        for j in range(ny):
            for l in range(nz):
                a = G[i0 + i, j0 + j, k0 + l]
                b = tmp[i, j, l]
                G[i0 + i, j0 + j, k0 + l] = _smin(a, b, k)


@njit(parallel=True, fastmath=True)
def _smax_block(G, i0, j0, k0, tmp, k):
    """subtract tmp-solid from G (smooth)."""
    nx, ny, nz = tmp.shape
    for i in prange(nx):
        for j in range(ny):
            for l in range(nz):
                a = G[i0 + i, j0 + j, k0 + l]
                b = -tmp[i, j, l]
                if k <= 0.0:
                    G[i0 + i, j0 + j, k0 + l] = a if a > b else b
                else:
                    hh = k - abs(a - b)
                    if hh <= 0.0:
                        G[i0 + i, j0 + j, k0 + l] = a if a > b else b
                    else:
                        hh = hh / k
                        G[i0 + i, j0 + j, k0 + l] = (a if a > b else b) + hh * hh * k * 0.25


def add_lock(F, pts, ups, widths, thicks, nstr=3, amp=0.0, k=0.3, op='union'):
    """Grooved tapered lock along polyline pts (world). ups = thickness direction per point.
    widths/thicks = half sizes. nstr = strand bundles across the width, amp = groove depth."""
    P = np.ascontiguousarray(pts, np.float64); n = len(P)
    U = np.ascontiguousarray(np.broadcast_to(np.asarray(ups, float), (n, 3)) if np.ndim(ups) == 1 else ups, np.float64)
    W = np.ascontiguousarray(np.broadcast_to(np.asarray(widths, float), (n,)), np.float64)
    T = np.ascontiguousarray(np.broadcast_to(np.asarray(thicks, float), (n,)), np.float64)
    r = max(W.max(), T.max()) + k + 3 * F.h + amp
    lo = P.min(0) - r; hi = P.max(0) + r
    a = np.clip(np.floor((lo - F.lo) / F.h).astype(int), 0, F.shape)
    b = np.clip(np.ceil((hi - F.lo) / F.h).astype(int) + 1, 0, F.shape)
    if np.any(b <= a):
        return
    tmp = np.full(tuple(b - a), FAR, np.float32)
    org = F.lo + a * F.h
    _lock_segments(tmp, org[0], org[1], org[2], F.h, P, U, W, T, float(nstr), float(amp), float(k + 2 * F.h + amp))
    if op == 'union':
        _smin_block(F.G, a[0], a[1], a[2], tmp, float(k))
    else:
        _smax_block(F.G, a[0], a[1], a[2], tmp, float(k))


@njit(parallel=True, fastmath=True)
def _ribbon_segments(tmp, tg, ox, oy, oz, h, P, U, W, T, A, nstr, pexp, pad, sig, PI, gph):
    """min-union of ribbon segments: super-elliptic section (half width W, half thickness T, exponent pexp).
    The strand-groove term (per-point amplitude A: nstr rounded strands separated by narrow V grooves) is taken
    from the segment that is nearest to the smooth surface, so grooves run continuously across segment joints."""
    nx, ny, nz = tmp.shape
    ip = 1.0 / pexp
    for s in range(P.shape[0] - 1):
        ax = P[s, 0]; ay = P[s, 1]; az = P[s, 2]
        bx = P[s + 1, 0]; by = P[s + 1, 1]; bz = P[s + 1, 2]
        tx = bx - ax; ty = by - ay; tz = bz - az
        L = math.sqrt(tx * tx + ty * ty + tz * tz) + 1e-9
        tx /= L; ty /= L; tz /= L
        ux = 0.5 * (U[s, 0] + U[s + 1, 0]); uy = 0.5 * (U[s, 1] + U[s + 1, 1]); uz = 0.5 * (U[s, 2] + U[s + 1, 2])
        du = ux * tx + uy * ty + uz * tz
        ux -= du * tx; uy -= du * ty; uz -= du * tz
        un = math.sqrt(ux * ux + uy * uy + uz * uz) + 1e-9
        ux /= un; uy /= un; uz /= un
        sx = ty * uz - tz * uy; sy = tz * ux - tx * uz; sz = tx * uy - ty * ux
        w1 = W[s]; w2 = W[s + 1]; t1 = T[s]; t2 = T[s + 1]; a1 = A[s]; a2 = A[s + 1]; pi1 = PI[s]; pi2 = PI[s + 1]
        r = max(max(w1, w2), max(t1, t2)) + pad
        i0 = max(int(math.floor((min(ax, bx) - r - ox) / h)), 0); i1 = min(int(math.ceil((max(ax, bx) + r - ox) / h)) + 1, nx)
        j0 = max(int(math.floor((min(ay, by) - r - oy) / h)), 0); j1 = min(int(math.ceil((max(ay, by) + r - oy) / h)) + 1, ny)
        k0 = max(int(math.floor((min(az, bz) - r - oz) / h)), 0); k1 = min(int(math.ceil((max(az, bz) + r - oz) / h)) + 1, nz)
        for i in prange(i0, i1):
            x = ox + i * h
            for j in range(j0, j1):
                y = oy + j * h
                for kk in range(k0, k1):
                    z = oz + kk * h
                    px = x - ax; py = y - ay; pz = z - az
                    sp = px * tx + py * ty + pz * tz
                    sc = min(max(sp, 0.0), L)
                    f = sc / L
                    w = w1 + (w2 - w1) * f
                    t = t1 + (t2 - t1) * f
                    vx = px - tx * sc; vy = py - ty * sc; vz = pz - tz * sc
                    vu = vx * ux + vy * uy + vz * uz
                    vs = vx * sx + vy * sy + vz * sz
                    va = sp - sc
                    qa = abs(vs / w); qu = abs(vu / t)
                    e = (qa ** pexp + qu ** pexp) ** ip
                    e = math.sqrt(e * e + (va / t) ** 2)   # short end caps: no scallops where the lock bends over the body
                    d = (e - 1.0) * min(w, t)
                    if d < tmp[i, j, kk]:
                        tmp[i, j, kk] = d
                        am = a1 + (a2 - a1) * f
                        g = 0.0
                        pitch = pi1 + (pi2 - pi1) * f
                        if am > 0.0 and vu > -0.2 * t and pitch > 0.0:
                            # pitch combing: grooves parallel to the centre line at vs = (k + 1/2) pitch
                            xs = vs / pitch
                            kc = math.floor(xs - gph + 0.5) + gph
                            if abs(kc) * pitch < w - 0.15 * pitch:
                                dl = abs(xs - kc) * pitch
                                g = am * math.exp(-(dl / sig) ** 2)
                        elif am > 0.0 and vu > -0.2 * t:
                            # soft groove valleys (gaussian, >= ~1 voxel wide) at the strand boundaries
                            a = min(max(vs / w, -1.0), 1.0)
                            xs = 0.5 * (a + 1.0) * nstr
                            kc = math.floor(xs + 0.5)          # nearest strand boundary, interior ones only
                            kc = min(max(kc, 1.0), nstr - 1.0)
                            if nstr >= 2.0:
                                dl = abs(xs - kc) * (2.0 * w / nstr)
                                g = am * math.exp(-(dl / sig) ** 2)
                        tg[i, j, kk] = g


def add_ribbon(F, pts, ups, widths, thicks, amps, nstr=2, pexp=2.4, k=0.2, op='union', pitch=0.0, sig=None, gph=0.5):
    P = np.ascontiguousarray(pts, np.float64); n = len(P)
    U = np.ascontiguousarray(ups, np.float64)
    W = np.ascontiguousarray(np.broadcast_to(np.asarray(widths, float), (n,)), np.float64)
    T = np.ascontiguousarray(np.broadcast_to(np.asarray(thicks, float), (n,)), np.float64)
    A = np.ascontiguousarray(np.broadcast_to(np.asarray(amps, float), (n,)), np.float64)
    PI = np.ascontiguousarray(np.broadcast_to(np.asarray(pitch, float), (n,)), np.float64)
    r = max(W.max(), T.max()) + k + 3 * F.h + A.max()
    lo = P.min(0) - r; hi = P.max(0) + r
    a = np.clip(np.floor((lo - F.lo) / F.h).astype(int), 0, F.shape)
    b = np.clip(np.ceil((hi - F.lo) / F.h).astype(int) + 1, 0, F.shape)
    if np.any(b <= a):
        return
    tmp = np.full(tuple(b - a), FAR, np.float32)
    tg = np.zeros(tuple(b - a), np.float32)
    org = F.lo + a * F.h
    _ribbon_segments(tmp, tg, org[0], org[1], org[2], F.h, P, U, W, T, A, float(nstr), float(pexp), float(k + 2 * F.h + A.max()), float(max(sig or 0.22, 1.3 * F.h)), PI, float(gph))
    tmp += tg
    if op == 'union':
        _smin_block(F.G, a[0], a[1], a[2], tmp, float(k))
    else:
        _smax_block(F.G, a[0], a[1], a[2], tmp, float(k))


def subfield(F, lo, hi):
    """A Field on the same lattice as F covering [lo, hi] (clipped). Returns (S, (i0,j0,k0))."""
    a = np.clip(np.floor((np.asarray(lo) - F.lo) / F.h).astype(int), 0, np.array(F.shape) - 1)
    b = np.clip(np.ceil((np.asarray(hi) - F.lo) / F.h).astype(int) + 1, 1, F.shape)
    S = Field.__new__(Field)
    S.lo = F.lo + a * F.h; S.h = F.h; S.shape = tuple(int(v) for v in (b - a))
    S.G = np.full(S.shape, FAR, np.float32)
    return S, a


def paste(F, S, a, k=0.0):
    i0, j0, k0 = (int(v) for v in a)
    _smin_block(F.G, i0, j0, k0, S.G, float(k))


@njit(parallel=True, fastmath=True)
def scalp_grooves(G, ox, oy, oz, h, i0, i1, j0, j1, k0, k1, O, R, capC, capR, psi, fade, phi0, dphi, th0, dth,
                  amp_fine, amp_bundle, swell, nb, th_lo, th_fade, rn_lo, rn_hi, mean_disp):
    """Displace field G with flow-aligned combing grooves on the hair cap.
    psi(phi, theta) grid: groove index along the flow (integer = groove centre). R: local->world columns."""
    nphi, nth = psi.shape
    for i in prange(i0, i1):
        x = ox + i * h
        for j in range(j0, j1):
            y = oy + j * h
            for k in range(k0, k1):
                z = oz + k * h
                dx = x - O[0]; dy = y - O[1]; dz = z - O[2]
                lx = R[0, 0] * dx + R[1, 0] * dy + R[2, 0] * dz
                ly = R[0, 1] * dx + R[1, 1] * dy + R[2, 1] * dz
                lz = R[0, 2] * dx + R[1, 2] * dy + R[2, 2] * dz
                qx = (lx - capC[0]) / capR[0]; qy = (ly - capC[1]) / capR[1]; qz = (lz - capC[2]) / capR[2]
                rn = math.sqrt(qx * qx + qy * qy + qz * qz)
                if rn < rn_lo or rn > rn_hi:
                    continue
                ph = math.degrees(math.atan2(qx, qy))
                th = math.degrees(math.asin(max(-1.0, min(1.0, qz / rn))))
                m = (th - th_lo) / th_fade
                if m <= 0.0:
                    continue
                if m > 1.0:
                    m = 1.0
                pm = (88.0 - th) / 9.0
                fpole = 1.0
                if pm < 1.0:
                    fpole = max(pm, 0.0)
                fu = (ph - phi0) / dphi; fv = (th - th0) / dth
                iu = int(math.floor(fu)); iv = int(math.floor(fv))
                if iv < 0 or iv >= nth - 1:
                    continue
                au = fu - iu; av = fv - iv
                iu0 = iu % nphi; iu1 = (iu + 1) % nphi
                p00 = psi[iu0, iv]; p10 = psi[iu1, iv]; p01 = psi[iu0, iv + 1]; p11 = psi[iu1, iv + 1]
                mx = max(max(p00, p10), max(p01, p11)); mn = min(min(p00, p10), min(p01, p11))
                if mx - mn > 1.5:
                    ps = p00 if au < 0.5 and av < 0.5 else (p10 if av < 0.5 else (p01 if au < 0.5 else p11))
                else:
                    ps = (p00 * (1 - au) + p10 * au) * (1 - av) + (p01 * (1 - au) + p11 * au) * av
                fd = (fade[iu0, iv] * (1 - au) + fade[iu1, iv] * au) * (1 - av) + (fade[iu0, iv + 1] * (1 - au) + fade[iu1, iv + 1] * au) * av
                fd *= fpole
                c = 0.5 + 0.5 * math.cos(2.0 * math.pi * ps)
                g = c * c
                cb = 0.5 + 0.5 * math.cos(2.0 * math.pi * ps / nb)
                b = cb * cb * cb * cb
                disp = amp_fine * g + amp_bundle * g * b - swell * (1.0 - cb)
                G[i, j, k] += m * (fd * (disp - mean_disp) + mean_disp)
