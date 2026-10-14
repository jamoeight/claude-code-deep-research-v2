"""Numba kernels for the figure (helper for figure.py).

 * cast(G, ...)       sphere-trace camera rays against a grid SDF (trilinear) -> surface points
 * displace(G0, G, ...) apply a camera-space displacement texture to the surface of a grid SDF:
       every grid point near the surface is moved to its foot point on the base surface, the foot point is
       projected into the texture camera, and the texel's displacement D (+ fine striations along the
       texel's fold-distance field) is subtracted from the SDF -- but only where the texel's surface point
       IS that foot point (visible from the texture camera) and the surface faces the camera.
"""
import math
import numpy as np
from numba import njit, prange


@njit(fastmath=True, inline='always')
def _tri(G, ox, oy, oz, ih, x, y, z):
    nx, ny, nz = G.shape
    fx = (x - ox) * ih; fy = (y - oy) * ih; fz = (z - oz) * ih
    if fx < 0.0 or fy < 0.0 or fz < 0.0 or fx >= nx - 1 or fy >= ny - 1 or fz >= nz - 1:
        return 50.0
    i = int(fx); j = int(fy); k = int(fz)
    ax = fx - i; ay = fy - j; az = fz - k
    c00 = G[i, j, k] * (1 - ax) + G[i + 1, j, k] * ax
    c10 = G[i, j + 1, k] * (1 - ax) + G[i + 1, j + 1, k] * ax
    c01 = G[i, j, k + 1] * (1 - ax) + G[i + 1, j, k + 1] * ax
    c11 = G[i, j + 1, k + 1] * (1 - ax) + G[i + 1, j + 1, k + 1] * ax
    c0 = c00 * (1 - ay) + c10 * ay
    c1 = c01 * (1 - ay) + c11 * ay
    return c0 * (1 - az) + c1 * az


@njit(parallel=True, fastmath=True)
def cast(G, ox, oy, oz, h, O, D, t0, t1, out):
    """O (3,), D (n,3) unit rays. out (n,3) hit points (nan if missed).  Conservative steps (the grid field is
    not an exact distance everywhere) + bisection of the first sign change."""
    ih = 1.0 / h
    nx, ny, nz = G.shape
    smax = 1.6 * h
    lo0 = ox; lo1 = oy; lo2 = oz
    hi0 = ox + (nx - 1) * h; hi1 = oy + (ny - 1) * h; hi2 = oz + (nz - 1) * h
    for r in prange(D.shape[0]):
        # clip the ray to the block
        ta = t0; tb = t1
        for ax in range(3):
            o = O[ax]; d = D[r, ax]
            lo = lo0 if ax == 0 else (lo1 if ax == 1 else lo2)
            hi = hi0 if ax == 0 else (hi1 if ax == 1 else hi2)
            if abs(d) < 1e-12:
                if o < lo or o > hi:
                    ta = 1e9
            else:
                q0 = (lo - o) / d; q1 = (hi - o) / d
                if q0 > q1:
                    q0, q1 = q1, q0
                ta = max(ta, q0); tb = min(tb, q1)
        out[r, 0] = np.nan; out[r, 1] = np.nan; out[r, 2] = np.nan
        if ta >= tb:
            continue
        t = ta + 1e-3; tp = t; dp = 50.0
        while t < tb:
            x = O[0] + D[r, 0] * t; y = O[1] + D[r, 1] * t; z = O[2] + D[r, 2] * t
            d = _tri(G, ox, oy, oz, ih, x, y, z)
            if d < 0.0 and dp >= 0.0 and dp < 49.0:
                a = tp; b = t
                for _ in range(10):
                    m = 0.5 * (a + b)
                    dm = _tri(G, ox, oy, oz, ih, O[0] + D[r, 0] * m, O[1] + D[r, 1] * m, O[2] + D[r, 2] * m)
                    if dm < 0.0:
                        b = m
                    else:
                        a = m
                t = 0.5 * (a + b)
                out[r, 0] = O[0] + D[r, 0] * t; out[r, 1] = O[1] + D[r, 1] * t; out[r, 2] = O[2] + D[r, 2] * t
                break
            tp = t; dp = d
            t += min(max(d * 0.8, 0.3 * h), smax)


@njit(parallel=True, fastmath=True)
def sample(G, ox, oy, oz, h, P, out):
    ih = 1.0 / h
    for r in prange(P.shape[0]):
        out[r] = _tri(G, ox, oy, oz, ih, P[r, 0], P[r, 1], P[r, 2])


@njit(fastmath=True, inline='always')
def _sstep(x, a, b):
    t = (x - a) / (b - a)
    if t < 0.0:
        return 0.0
    if t > 1.0:
        return 1.0
    return t * t * (3.0 - 2.0 * t)


@njit(parallel=True, fastmath=True)
def displace(G0, G, ox, oy, oz, h, band, cam, TX, u0, v0, ts, fine, pitch, amp, rv0, rv1, fc0, fc1, nfoot):
    """G0: base SDF block (read), G: output block (written: G = G0 - disp*w where applicable).
    cam = [locx,locy,locz, fwd(3), right(3), up(3), f, W, H]
    TX: texture (nv, nu, 7): Xs(3), D, dn, sw, valid."""
    nx, ny, nz = G0.shape
    lx = cam[0]; ly = cam[1]; lz = cam[2]
    fx_ = cam[3]; fy_ = cam[4]; fz_ = cam[5]
    rx = cam[6]; ry = cam[7]; rz = cam[8]
    ux = cam[9]; uy = cam[10]; uz = cam[11]
    f = cam[12]; W = cam[13]; H = cam[14]
    nv = TX.shape[0]; nu = TX.shape[1]
    tw = 6.283185307179586 / pitch
    for i in prange(1, nx - 1):
        x = ox + i * h
        for j in range(1, ny - 1):
            y = oy + j * h
            for k in range(1, nz - 1):
                g = G0[i, j, k]
                if g > band or g < -band:
                    continue
                z = oz + k * h
                gx = (G0[i + 1, j, k] - G0[i - 1, j, k])
                gy = (G0[i, j + 1, k] - G0[i, j - 1, k])
                gz = (G0[i, j, k + 1] - G0[i, j, k - 1])
                gl = math.sqrt(gx * gx + gy * gy + gz * gz)
                if gl < 1e-9:
                    continue
                nx_ = gx / gl; ny_ = gy / gl; nz_ = gz / gl
                # foot point on the base surface (Newton-refined on the trilinear field)
                px = x - nx_ * g; py = y - ny_ * g; pz = z - nz_ * g
                ih = 1.0 / h
                for _it in range(nfoot):
                    gp = _tri(G0, ox, oy, oz, ih, px, py, pz)
                    if abs(gp) < 0.02 * h:
                        break
                    e = 0.75 * h
                    qx = _tri(G0, ox, oy, oz, ih, px + e, py, pz) - _tri(G0, ox, oy, oz, ih, px - e, py, pz)
                    qy = _tri(G0, ox, oy, oz, ih, px, py + e, pz) - _tri(G0, ox, oy, oz, ih, px, py - e, pz)
                    qz = _tri(G0, ox, oy, oz, ih, px, py, pz + e) - _tri(G0, ox, oy, oz, ih, px, py, pz - e)
                    ql = math.sqrt(qx * qx + qy * qy + qz * qz)
                    if ql < 1e-9:
                        break
                    gsc = ql / (2 * e)
                    px -= qx / ql * gp / max(gsc, 0.5); py -= qy / ql * gp / max(gsc, 0.5); pz -= qz / ql * gp / max(gsc, 0.5)
                dx = px - lx; dy = py - ly; dz = pz - lz
                zc = dx * fx_ + dy * fy_ + dz * fz_
                if zc < 1.0:
                    continue
                dl = math.sqrt(dx * dx + dy * dy + dz * dz)
                facing = -(nx_ * dx + ny_ * dy + nz_ * dz) / dl
                wf = _sstep(facing, fc0, fc1)
                if wf <= 0.0:
                    continue
                u = W * 0.5 + f * (dx * rx + dy * ry + dz * rz) / zc
                v = H * 0.5 - f * (dx * ux + dy * uy + dz * uz) / zc
                tu = (u - u0) * ts; tv = (v - v0) * ts
                if tu < 0.0 or tv < 0.0 or tu >= nu - 1 or tv >= nv - 1:
                    continue
                a = int(tu); b = int(tv); au = tu - a; av = tv - b
                acc = 0.0; wsum = 0.0
                Dv = 0.0; dnv = 0.0; swv = 0.0; ex = 0.0; ey = 0.0; ez = 0.0
                for q in range(4):
                    aa = a + (q & 1); bb = b + (q >> 1)
                    wq = (au if (q & 1) else 1.0 - au) * (av if (q >> 1) else 1.0 - av)
                    if TX[bb, aa, 6] > 0.5:
                        wsum += wq
                        ex += TX[bb, aa, 0] * wq; ey += TX[bb, aa, 1] * wq; ez += TX[bb, aa, 2] * wq
                        Dv += TX[bb, aa, 3] * wq; dnv += TX[bb, aa, 4] * wq; swv += TX[bb, aa, 5] * wq
                if wsum < 0.5:
                    continue
                ex /= wsum; ey /= wsum; ez /= wsum; Dv /= wsum; dnv /= wsum; swv /= wsum
                dd = math.sqrt((ex - px) ** 2 + (ey - py) ** 2 + (ez - pz) ** 2)
                ag = abs(g)
                slack = 0.3 * ag
                wv = 1.0 - _sstep(dd, rv0 + slack, rv1 + slack)
                if wv <= 0.0:
                    continue
                disp = Dv
                if fine:
                    disp += amp * swv * math.sin(dnv * tw)
                ad = abs(disp)
                wb = 1.0 - _sstep(abs(g), ad + 1.0, ad + 2.5)
                G[i, j, k] = G[i, j, k] - disp * wv * wf * wb
