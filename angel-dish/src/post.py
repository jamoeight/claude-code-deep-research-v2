"""Post-processing on the assembled Field (owned by the integrator; called from model.py).

fill_voids(F)              : enclosed empty pockets (not connected to the outside) become solid.
flat_base(F, zmax)         : below zmax the footprint is filled solid (no recesses/channels under the base).
close_box(F, box, r, ...)  : local morphological closing (fills pits, slots and cracks narrower than ~2r) inside box.
"""
import numpy as np
from scipy import ndimage as ndi


def _idx(F, box):
    lo = np.floor((np.asarray(box[:3], float) - F.lo) / F.h).astype(int)
    hi = np.ceil((np.asarray(box[3:], float) - F.lo) / F.h).astype(int) + 1
    lo = np.clip(lo, 0, F.shape); hi = np.clip(hi, 0, F.shape)
    return tuple(slice(a, b) for a, b in zip(lo, hi))


def _sdf_from_mask(m, h):
    """Approximate signed distance (negative inside) of a boolean mask, lightly smoothed."""
    d_out = ndi.distance_transform_edt(~m)
    d_in = ndi.distance_transform_edt(m)
    sd = (np.where(m, -(d_in - 0.5), d_out - 0.5) * h).astype(np.float32)
    return ndi.gaussian_filter(sd, 0.8)


def fill_voids(F, verbose=True):
    out = F.G > 0
    lab, n = ndi.label(out)
    if n <= 1:
        return 0
    border = np.unique(np.concatenate([lab[0].ravel(), lab[-1].ravel(), lab[:, 0].ravel(), lab[:, -1].ravel(), lab[:, :, 0].ravel(), lab[:, :, -1].ravel()]))
    enclosed = np.setdiff1d(np.arange(1, n + 1), border)
    if len(enclosed) == 0:
        return 0
    m = np.isin(lab, enclosed)
    nvox = int(m.sum())
    # push enclosed voxels (and a 1-voxel shell around them) inside
    F.G[m] = -F.h
    if verbose:
        print(f'post.fill_voids: filled {len(enclosed)} pockets, {nvox} voxels', flush=True)
    return len(enclosed)


def flat_base(F, zmax=1.2, close_r=2.5, verbose=True):
    """For layers z < zmax: close (2D, radius close_r) and fill holes of the footprint so the bottom is one solid face."""
    k1 = int(np.ceil((zmax - F.lo[2]) / F.h)) + 1
    k0 = max(int(np.floor((0.0 - F.lo[2]) / F.h)), 0)
    added = 0
    # footprint = union of solid over the lowest few mm, holes filled
    foot = (F.G[:, :, k0:k1 + 2] < 0).any(axis=2)
    if close_r > 0:
        rv = close_r / F.h
        dil = ndi.distance_transform_edt(~foot) <= rv
        foot = foot | (ndi.distance_transform_edt(dil) > rv)
    foot = ndi.binary_fill_holes(foot)
    for k in range(k0, k1):
        layer = F.G[:, :, k]
        need = foot & (layer >= 0)
        added += int(need.sum())
        layer[need] = np.minimum(layer[need], -0.5 * F.h)
    if verbose:
        print(f'post.flat_base: filled {added} voxels below z={zmax}', flush=True)


def close_box(F, box, r, smooth=True, verbose=True):
    """Morphological closing with ball radius r (design units) inside box; only ADDS material."""
    sl = _idx(F, box)
    G = F.G[sl]
    if G.size == 0:
        return
    m = G < 0
    rv = r / F.h
    dil = ndi.distance_transform_edt(~m) <= rv
    clo = ndi.distance_transform_edt(dil) > rv
    clo |= m
    add = clo & ~m
    if not add.any():
        return
    sd = _sdf_from_mask(clo, F.h) if smooth else np.where(clo, -F.h, F.h).astype(np.float32)
    # keep the box border untouched (avoid seams): fade the effect out over 3 voxels
    w = np.ones(G.shape, np.float32)
    for ax in range(3):
        n = G.shape[ax]
        ramp = np.clip(np.minimum(np.arange(n), np.arange(n)[::-1]) / 3.0, 0, 1).astype(np.float32)
        shp = [1, 1, 1]; shp[ax] = n
        w = w * ramp.reshape(shp)
    newG = np.minimum(G, sd + 0.25 * F.h)
    F.G[sl] = G * (1 - w) + newG * w
    if verbose:
        print(f'post.close_box {tuple(round(b, 1) for b in box)} r={r}: +{int(add.sum())} voxels', flush=True)
