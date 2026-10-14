"""Numba kernels for the drapery dish (helper for dish.py).

body(F, ...): the whole dish in one pass:
  - polar outer wall  rho < R0(phi) + FL(phi)*(z/ZW)^1.6 + D(phi, z) - foot chamfer, capped at ZW(phi)
    (D = satin-fold displacement table over (phi, z), with a matching normalisation table)
  - minus the interior cavity  z > H(x, y)  (H = interior height field incl. folds/whirlpool)
  - plus a rolled lip swept along phi: a tilted ellipse in the (rho, z) half-plane with varying size,
    centre and tilt, combed striations and shallow longitudinal grooves, buried where it fades out.
"""
import math
import numpy as np
from numba import njit, prange


@njit(fastmath=True, inline='always')
def _smin(a, b, k):
    if k <= 0.0:
        return a if a < b else b
    h = k - abs(a - b)
    if h <= 0.0:
        return a if a < b else b
    h = h / k
    return (a if a < b else b) - h * h * k * 0.25


@njit(fastmath=True, inline='always')
def _smax(a, b, k):
    return -_smin(-a, -b, k)


@njit(fastmath=True, inline='always')
def _lerp_tab(T, u, N):
    i0 = int(math.floor(u)); f = u - i0
    i0 = i0 % N; i1 = (i0 + 1) % N
    return T[i0] * (1.0 - f) + T[i1] * f


@njit(fastmath=True, inline='always')
def _ell(u, v, a, b):
    """approximate signed distance to an axis-aligned ellipse (semi-axes a, b)."""
    k0 = math.sqrt((u / a) ** 2 + (v / b) ** 2)
    k1 = math.sqrt((u / (a * a)) ** 2 + (v / (b * b)) ** 2)
    if k1 < 1e-9:
        return -min(a, b)
    return k0 * (k0 - 1.0) / k1


@njit(parallel=True, fastmath=True)
def _body(G, ox, oy, oz, h, cx, cy, R0, FL, ZW, ZWF, LIPS, DT, DLT, NT, dz0, dzs, hf, hn, RIN, kt, cham, fine, nstri, astri, kl, zmax, wedge):
    nx, ny, nz = G.shape
    N = R0.shape[0]
    NL = LIPS.shape[0]
    NZ = DT.shape[1]
    for i in prange(nx):
        x = ox + i * h
        for j in range(ny):
            y = oy + j * h
            dx = x - cx; dy = y - cy
            rho = math.sqrt(dx * dx + dy * dy)
            ph = math.atan2(dy, dx)
            phd = ph * 57.29577951308232
            u = (phd + 180.0) / 360.0 * N
            r0 = _lerp_tab(R0, u, N)
            fl = _lerp_tab(FL, u, N)
            zw = _lerp_tab(ZW, u, N)
            zwf = _lerp_tab(ZWF, u, N)
            rin = _lerp_tab(RIN, u, N)
            H = hf[i, j]; nn = hn[i, j]
            ui = int(math.floor(u)); fu = u - ui
            i0 = ui % N; i1 = (ui + 1) % N
            kmax = min(nz, int((zmax - oz) / h) + 2)
            for k in range(kmax):
                z = oz + k * h
                t = z / max(zwf, 1.0)
                if t < 0.0:
                    t = 0.0
                if t > 1.3:
                    t = 1.3
                # fold displacement (bilinear in the table)
                w = (z - dz0) / dzs
                if w < 0.0:
                    w = 0.0
                if w > NZ - 1.001:
                    w = NZ - 1.001
                k0 = int(w); fz = w - k0
                D = (DT[i0, k0] * (1 - fu) + DT[i1, k0] * fu) * (1 - fz) + (DT[i0, k0 + 1] * (1 - fu) + DT[i1, k0 + 1] * fu) * fz
                nr = (NT[i0, k0] * (1 - fu) + NT[i1, k0] * fu) * (1 - fz) + (NT[i0, k0 + 1] * (1 - fu) + NT[i1, k0 + 1] * fu) * fz
                rw = r0 + fl * t ** 1.6 + D
                if z < cham:
                    rw -= (cham - z)
                d = (rho - rw) * nr
                # domed top: the wall's outer half rolls over instead of being cut flat
                hw = 0.5 * (rw - rin)
                if hw < 1.5:
                    hw = 1.5
                e = (rho - 0.5 * (rw + rin)) / hw
                if e > 1.0:
                    e = 1.0
                if e < -1.0:
                    e = -1.0
                dr = 3.2 if hw > 3.2 else hw
                d = _smax(d, z - zw + dr * (1.0 - math.sqrt(1.0 - 0.96 * e * e)), kt)
                d = _smax(d, (z - H) * nn, 1.8)
                for li in range(NL):
                    lon = _lerp_tab(LIPS[li, 0], u, N)
                    if lon <= 0.02:
                        continue
                    lrc = _lerp_tab(LIPS[li, 1], u, N)
                    lzc = _lerp_tab(LIPS[li, 2], u, N)
                    la = _lerp_tab(LIPS[li, 3], u, N)
                    lb = _lerp_tab(LIPS[li, 4], u, N)
                    lt = _lerp_tab(LIPS[li, 5], u, N)
                    g1 = _lerp_tab(LIPS[li, 6], u, N)
                    g2 = _lerp_tab(LIPS[li, 7], u, N)
                    sw = _lerp_tab(LIPS[li, 8], u, N)
                    lf = _lerp_tab(LIPS[li, 9], u, N)
                    ct = math.cos(lt); st = math.sin(lt)
                    # rolled lip: tilted ellipse in the (rho, z) half plane
                    pu = rho - (r0 + fl + lrc)
                    pv = z - lzc
                    qu = pu * ct + pv * st
                    qv = -pu * st + pv * ct
                    dl = _ell(qu, qv, la, lb) + (1.0 - lon) * 6.0     # a fading hem stays buried in the folds
                    if lf > 0.01:
                        DL = (DLT[i0, k0] * (1 - fu) + DLT[i1, k0] * fu) * (1 - fz) + (DLT[i0, k0 + 1] * (1 - fu) + DLT[i1, k0 + 1] * fu) * fz
                        wq = (qu / la + 0.7) / 1.4
                        if wq < 0.0:
                            wq = 0.0
                        if wq > 1.0:
                            wq = 1.0
                        dl -= lf * DL * wq * wq * (3.0 - 2.0 * wq)
                    ang = math.atan2(qv / lb, qu / la)
                    # shallow longitudinal grooves (fold creases running along the hem)
                    e1 = ang - g1
                    e2 = ang - g2
                    dl += 1.0 * sw * (math.exp(-(e1 / 0.24) ** 2) + 0.8 * math.exp(-(e2 / 0.2) ** 2))
                    if fine > 0:
                        am = -0.15 + 1.1 * math.sin(0.17 * phd + 1.3 * math.sin(0.06 * phd)) + 0.35 * math.sin(0.43 * phd + 2.0)
                        if am < 0.0:
                            am = 0.0
                        # no combing where the hem tucks into the wall (underside / inner foot): avoids beading
                        fa = (ang + 1.0) / 0.8
                        if fa < 0.0:
                            fa = 0.0
                        if fa > 1.0:
                            fa = 1.0
                        fb = (2.9 - ang) / 0.6
                        if fb < 0.0:
                            fb = 0.0
                        if fb > 1.0:
                            fb = 1.0
                        am = am * fa * fa * (3.0 - 2.0 * fa) * fb
                        dl += astri * am * (math.sin(nstri * ang + 0.35 * math.sin(0.11 * phd))
                                            + 0.5 * math.sin((nstri + 23.0) * ang + 0.8 * math.sin(0.08 * phd + 1.0)))
                    d = _smin(d, dl, kl)
                    # printable underside: a 50-deg wedge from the hem's outer-lower point down into the wall
                    # support face tangent to the hem: the ellipse point whose outward normal points 50 deg
                    # below horizontal (in the ellipse's own tilted frame), so no edge stands proud
                    nu = 0.643 * ct - 0.766 * st
                    nv = -0.643 * st - 0.766 * ct
                    t0 = math.atan2(nv * lb, nu * la)
                    eu = la * math.cos(t0); ev = lb * math.sin(t0)
                    p0r = (r0 + fl + lrc) + eu * ct - ev * st
                    p0z = lzc + eu * st + ev * ct
                    d1 = (rho - p0r + (p0z - z) * 1.19) * 0.643
                    d2 = z - p0z
                    d3 = (r0 + fl + lrc - 0.6 * la) - rho
                    ds_ = _smax(d1, _smax(d2, d3, 1.2), 1.2)
                    # fade the support out with the hem so its edges never stand proud of the wall
                    fw = (lon - 0.55) / 0.4
                    if fw < 0.0:
                        fw = 0.0
                    if fw > 1.0:
                        fw = 1.0
                    ds_ += (1.0 - fw * fw * (3.0 - 2.0 * fw)) * 30.0
                    if wedge > 0:
                        d = _smin(d, ds_, 1.4)
                a = G[i, j, k]
                G[i, j, k] = a if a < d else d


def body(F, cx, cy, R0, FL, ZW, LIP, DT, DLT, NTab, dz0, dzs, hf, RIN, kt=2.5, cham=2.5, fine=False, nstri=38, astri=0.16, kl=1.6, zmax=48.0, wedge=1, ZWF=None):
    if ZWF is None:
        ZWF = ZW
    gx, gy = np.gradient(hf, F.h)
    hn = (1.0 / np.sqrt(1.0 + gx * gx + gy * gy)).astype(np.float64)
    _body(F.G, F.lo[0], F.lo[1], F.lo[2], F.h, float(cx), float(cy), R0.astype(np.float64), FL.astype(np.float64),
          ZW.astype(np.float64), ZWF.astype(np.float64), np.ascontiguousarray(LIP if LIP.ndim == 3 else LIP[None], np.float64), np.ascontiguousarray(DT, np.float64), np.ascontiguousarray(DLT, np.float64),
          np.ascontiguousarray(NTab, np.float64), float(dz0), float(dzs), hf.astype(np.float64), hn, RIN.astype(np.float64), float(kt), float(cham),
          1 if fine else 0, float(nstri), float(astri), float(kl), float(zmax), int(wedge))
    return F
