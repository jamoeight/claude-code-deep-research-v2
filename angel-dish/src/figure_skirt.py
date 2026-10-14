"""Skirt base for the figure: a smooth height field H(x, y) -- fabric hanging from the support outline (where the
gown leaves her thighs / hips / seat) and flaring out onto the bowl floor (tangent to it at the hem), so the gown
pools and flows into the dish with no step, no plinth and no planar cuts.  Folds are added later (figure_tex)."""
import math
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
from figure_tex import inpoly
from sdf import catmull

ZF = 7.3          # hem height: just under the dish floor (~7.6-8) so the pool meets it tangentially

# support outline (counter-clockwise seen from above), per point: x, y, zt (top height), W (horizontal fall
# width to the hem), q (profile exponent: larger = steeper top / longer flat pool)
SUP = [
    # front: under the front of her right thigh, hip -> knee
    (-32.0, 13.0, 31.0, 16.0, 1.05),
    (-25.0, 11.0, 30.5, 8.5, 2.1),
    (-17.0, 8.0, 30.0, 7.5, 2.2),
    (-9.0, 4.5, 30.0, 7.0, 2.2),
    (-3.0, 1.8, 31.5, 7.5, 2.1),
    # knee and the fabric falling down-right off the knees (legs tucked to the right, behind): a broad tent
    (2.0, 1.5, 34.5, 11.0, 1.7),
    (6.0, 5.5, 31.0, 13.0, 1.6),
    (8.0, 12.0, 27.0, 13.0, 1.7),
    (7.5, 20.0, 23.0, 12.0, 1.8),
    (5.0, 28.0, 22.0, 10.0, 1.8),
    # back of the seat
    (0.0, 32.0, 23.0, 6.5, 1.8),
    (-8.0, 34.5, 25.0, 5.5, 1.8),
    (-17.0, 35.0, 26.0, 5.5, 1.8),
    (-25.0, 33.5, 27.0, 6.0, 1.9),
    # her right hip side: fabric falls outward and pools toward the left wall
    (-31.5, 30.0, 29.0, 8.5, 2.0),
    (-35.0, 25.0, 31.5, 15.5, 0.95),
    (-35.0, 18.0, 32.0, 18.5, 0.85),
]


# plan region the skirt solid must stay inside (the dish footprint at the table, shrunk ~3 units): nothing of the
# gown may poke out through the bowl's outer wall / foot
SAFE = [(-47, 22), (-43, 29.5), (-37, 33.5), (-28, 38), (-15, 39.5), (0, 38.5), (15, 38), (25, 36.5), (40, 0), (25, -40),
        (-20, -45), (-50, -25), (-54.5, 0), (-51.5, 15)]


def outline(n_per=10):
    P = np.array([(p[0], p[1]) for p in SUP], float)
    return catmull(P, per=n_per, closed=True)


def params(X, Y, sigma=7.0):
    """Gaussian-weighted interpolation of the per-point parameters (smooth everywhere)."""
    S = np.array(SUP, float)
    num = np.zeros(X.shape + (3,)); den = np.zeros(X.shape)
    for p in S:
        w = np.exp(-((X - p[0]) ** 2 + (Y - p[1]) ** 2) / (2 * sigma * sigma)) + 1e-12
        num += w[..., None] * p[2:5]; den += w
    return num[..., 0] / den, num[..., 1] / den, num[..., 2] / den


def height(xs, ys, h):
    X, Y = np.meshgrid(xs, ys, indexing='ij')
    O = outline()
    ins = inpoly(np.stack([X.ravel(), Y.ravel()], 1), O).reshape(X.shape)
    dense = np.vstack([np.linspace(O[i], O[i + 1], 6, endpoint=False) for i in range(len(O) - 1)])
    d, _ = cKDTree(dense).query(np.stack([X.ravel(), Y.ravel()], 1))
    d = d.reshape(X.shape)
    dS = np.where(ins, -d, d)
    zt, W, q = params(X, Y)
    s = dS / W
    Hout = ZF + (zt - ZF) * np.clip(1 - s, 0, 1) ** q
    Hin = zt + 0.9 * np.minimum(-dS, 9.0)
    H = np.where(dS < 0, Hin, Hout)
    e = np.maximum(dS - W, 0.0)
    H = np.where(s > 1, ZF - 0.3 * e * e, H)
    # keep inside the bowl footprint
    S = np.array(SAFE, float)
    insafe = inpoly(np.stack([X.ravel(), Y.ravel()], 1), S).reshape(X.shape)
    dense_s = np.vstack([np.linspace(S[i], S[(i + 1) % len(S)], 40, endpoint=False) for i in range(len(S))])
    ds, _ = cKDTree(dense_s).query(np.stack([X.ravel(), Y.ravel()], 1))
    dsf = np.where(insafe, -ds.reshape(X.shape), ds.reshape(X.shape))
    H = np.minimum(H, ZF + 30.0 - 12.0 * (dsf + 2.5))
    H = np.maximum(H, -4.0)
    H = ndimage.gaussian_filter(H, 1.1 / h, mode='nearest')
    return H


def sdf_block(xs, ys, zs, h, H=None):
    """Height field -> SDF block: min-magnitude of the slope-normalised vertical estimate and the per-slice
    horizontal distance (exact in plan), so the field is a usable distance in front of steep curtains too."""
    if H is None:
        H = height(xs, ys, h)
    gx, gy = np.gradient(H, h)
    nrm = 1.0 / np.sqrt(1 + gx * gx + gy * gy)
    out = np.empty((len(xs), len(ys), len(zs)), np.float32)
    for k_, z in enumerate(zs):
        v = (z - H) * nrm
        m = H > z
        if m.any() and (~m).any():
            din = ndimage.distance_transform_edt(m) * h - 0.5 * h
            dout = ndimage.distance_transform_edt(~m) * h - 0.5 * h
            near = 4.5     # near the surface keep the smooth slope-normalised estimate (EDT is voxel-quantised)
            v = np.where(m, np.maximum(v, -np.maximum(din, near)), np.minimum(v, np.maximum(dout, near)))
        out[:, :, k_] = v
    return out, H
