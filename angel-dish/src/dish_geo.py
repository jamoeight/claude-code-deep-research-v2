"""Plan geometry of the drapery dish (polar description about C = (2, -6)).

phi = plan azimuth in degrees about C (atan2(y - Cy, x - Cx)): front = -90, right = 0, back = 90, left = +-180.
R0(phi)  : nominal outer-wall radius just above the foot chamfer.
FL(phi)  : outward flare of the wall at its top (wall radius = R0 + FL * (z/Zw)^1.6).
ZW(phi)  : height of the core wall top (under the lip where there is a lip).
s(phi)   : arc length along the wall, 0 at the front (phi=-90), increasing toward the viewer's right.
"""
import math
import numpy as np

C = np.array([2.0, -6.0])
NT = 3600                      # table resolution (0.1 deg)
PH = np.linspace(-180, 180, NT, endpoint=False)


def periodic(angles, values, N=NT):
    """Smooth periodic (Catmull-Rom) interpolation on the circle -> table over [-180, 180)."""
    a = np.asarray(angles, float); v = np.asarray(values, float)
    o = np.argsort(a); a = a[o]; v = v[o]
    A = np.concatenate([a[-2:] - 360, a, a[:2] + 360]); V = np.concatenate([v[-2:], v, v[:2]])
    ph = np.linspace(-180, 180, N, endpoint=False)
    i = np.clip(np.searchsorted(A, ph) - 1, 1, len(A) - 3)
    t = (ph - A[i]) / (A[i + 1] - A[i])
    m1 = (V[i + 1] - V[i - 1]) / (A[i + 1] - A[i - 1]) * (A[i + 1] - A[i])
    m2 = (V[i + 2] - V[i]) / (A[i + 2] - A[i]) * (A[i + 1] - A[i])
    t2 = t * t; t3 = t2 * t
    return (2 * t3 - 3 * t2 + 1) * V[i] + (t3 - 2 * t2 + t) * m1 + (-2 * t3 + 3 * t2) * V[i + 1] + (t3 - t2) * m2


def at(T, phi):
    N = len(T)
    u = (np.asarray(phi, float) + 180.0) / 360.0 * N
    i0 = np.floor(u).astype(int); f = u - i0
    return T[i0 % N] * (1 - f) + T[(i0 + 1) % N] * f


def polar(x, y):
    dx = np.asarray(x, float) - C[0]; dy = np.asarray(y, float) - C[1]
    return np.degrees(np.arctan2(dy, dx)), np.hypot(dx, dy)


# ---- nominal outer wall outline (x, y) just above the foot chamfer
OUTLINE = [(2, -55.8), (-10, -54.0), (-22, -51.2), (-32, -46.6), (-42, -40.0), (-50.5, -31.5), (-56, -18), (-60, -4),
           (-59, 10), (-53, 23), (-45, 34), (-33, 41.5), (-17, 44.5), (0, 43.0), (16, 42.5), (30, 42.5),
           (44, 41.0), (59, 32.5), (70, 21.5), (78, 8.5), (82.5, -4), (83, -14), (79, -25.0), (70.0, -35.6),
           (57, -42.6), (44, -49.2), (30, -55.0), (16, -56.8)]
_a, _r = polar(*np.array(OUTLINE).T)
R0T = periodic(_a, _r)
# close the slot against the left wing's inner face (which stands at r~63-65 for az -175..-155):
# the wall reaches into the wing body there (wing outer face is at r>70, so nothing pokes through)
_TGT = [(-180, 0), (-176, 0.3), (-172, 2.4), (-168, 5.6), (-164, 7.6), (-160, 6.6), (-156, 4.0), (-152, 1.6), (-148, 0.3), (-144, 0)]
_ta = np.array(_TGT, float)
R0T = R0T + np.interp(PH, _ta[:, 0], _ta[:, 1], left=0.0, right=0.0) * 1.0
R0T = np.convolve(np.concatenate([R0T[-20:], R0T, R0T[:20]]), np.ones(21) / 21.0, mode='same')[20:-20]

# outward flare at the top of the wall
FLT = periodic([-155, -140, -120, -90, -65, -45, -30, -15, 0, 12, 25, 40, 70, 110, 150, 180],
               [-0.5, -2.6, -3.0, -3.3, -2.7, -0.2, -1.4, -3.0, -3.0, -2.0, -0.8, 0.0, 0.0, 0.0, 0.0, 0.0])

# core wall top
ZWT = periodic([-160, -150, -135, -120, -105, -90, -75, -62, -50, -38, -25, -12, 0, 10, 20, 30, 42, 55, 70, 90, 110, 125, 140, 155, 170, 185],
               [21.0, 18.0, 17.2, 17.8, 18.8, 19.6, 19.6, 19.2, 19.6, 20.8, 22.6, 24.2, 24.6, 24.0, 22.0, 18.0, 15.0, 13.0, 12.0, 11.5, 12.0, 13.5, 16.5, 20.5, 23.0, 23.0])

# arc length (front = 0)
_dphi = math.radians(360.0 / NT)
_ds = R0T * _dphi
ST = np.cumsum(_ds) - _ds
ST = ST - np.interp(-90.0, PH, ST)


def R0(phi):
    return at(R0T, phi)


def FL(phi):
    return at(FLT, phi)


def ZW(phi):
    return at(ZWT, phi)


def s_of(phi):
    """arc length; continuous on (-180, 180)."""
    return np.interp(np.asarray(phi, float), PH, ST)


def phi_of(s):
    return np.interp(np.asarray(s, float), ST, PH)


def wall_r(phi, z):
    """nominal outer wall radius (no folds, no foot chamfer)."""
    zw = ZW(phi)
    t = np.clip(np.asarray(z, float) / np.maximum(zw, 1.0), 0, 1.3)
    return R0(phi) + FL(phi) * t ** 1.6


def xy(phi, r):
    a = np.radians(phi)
    return C[0] + r * np.cos(a), C[1] + r * np.sin(a)
