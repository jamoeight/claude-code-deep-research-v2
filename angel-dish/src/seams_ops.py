"""Field operations used by seams.py (owned by the integrator).

base_fill(F, ...)    : flat, print-ready base: inside the (hole-filled) footprint every column is solid from the table up to its
                       highest solid voxel below zmax (no bridged recesses, channels or one-layer skins); smooth SDF, no layer below z=0.
soft_close(F, box, r): morphological closing (fills slits/pits narrower than ~2r) that only fills where the gap is DEEP
                       (depth >= dmin below the closed surface); shallow carved grooves are left untouched. Smooth SDF output.
drop_specks(F, vmin) : delete solid islands smaller than vmin mm^3 (floating bits).
"""
import numpy as np
from scipy import ndimage as ndi

S26 = np.ones((3, 3, 3), bool)


def _idx(F, box, pad=0):
    lo = np.floor((np.asarray(box[:3], float) - F.lo) / F.h).astype(int) - pad
    hi = np.ceil((np.asarray(box[3:], float) - F.lo) / F.h).astype(int) + 1 + pad
    lo = np.clip(lo, 0, F.shape); hi = np.clip(hi, 0, F.shape)
    return tuple(slice(a, b) for a, b in zip(lo, hi))


def _sd(m, h, sigma=0.8):
    d_out = ndi.distance_transform_edt(~m)
    d_in = ndi.distance_transform_edt(m)
    sd = (np.where(m, -(d_in - 0.5), d_out - 0.5) * h).astype(np.float32)
    return ndi.gaussian_filter(sd, sigma) if sigma > 0 else sd


def _fade(shape, n=3):
    w = np.ones(shape, np.float32)
    for ax in range(3):
        k = shape[ax]
        ramp = np.clip(np.minimum(np.arange(k), np.arange(k)[::-1]) / float(n), 0, 1).astype(np.float32)
        s = [1, 1, 1]; s[ax] = k
        w = w * ramp.reshape(s)
    return w


def _blend_add(G, sd, add, h, grow=3, bias=0.25):
    """G <- min(G, sd + bias*h) but only near the voxels in `add` (smooth weight), so untouched surfaces keep their exact SDF."""
    if not add.any():
        return 0
    near = ndi.distance_transform_edt(~add) <= grow
    w = ndi.gaussian_filter(near.astype(np.float32), 1.0)
    w = np.clip(w * 1.5, 0, 1)
    newG = np.minimum(G, sd + bias * h)
    G[...] = G * (1 - w) + newG * w
    return int(add.sum())


def soft_close(F, box, r, dmin=0.0, bias=0.25, verbose=True, tag=''):
    """Closing with ball radius r inside box (only adds material). Gap voxels shallower than dmin (distance below the
    closed surface) are not filled, so shallow grooves keep their profile; only their deep part is filled.
    The new surface is a smoothed SDF of (solid | fill), blended in only around the filled voxels (cluster by cluster)."""
    h = F.h
    pad = int(np.ceil(r / h)) + 3
    sl = _idx(F, box, pad)
    G = F.G[sl]
    if G.size == 0:
        return 0
    m = G < 0
    rv = r / h
    dil = ndi.distance_transform_edt(~m) <= rv
    clo = ndi.distance_transform_edt(dil) > rv
    del dil
    clo |= m
    add = clo & ~m
    if dmin > 0:
        add &= ndi.distance_transform_edt(clo) * h >= dmin
    del clo
    # restrict to the box proper (pad only provides context)
    lo_i = [max(0, int(np.floor((box[i] - F.lo[i]) / h)) - sl[i].start) for i in range(3)]
    hi_i = [min(G.shape[i], int(np.ceil((box[3 + i] - F.lo[i]) / h)) + 1 - sl[i].start) for i in range(3)]
    inner = np.zeros(G.shape, bool)
    inner[lo_i[0]:hi_i[0], lo_i[1]:hi_i[1], lo_i[2]:hi_i[2]] = True
    add &= inner
    del inner
    n = int(add.sum())
    if n == 0:
        return 0
    lab, nc = ndi.label(ndi.binary_dilation(add, S26, iterations=2), S26)
    objs = ndi.find_objects(lab)
    M = 6
    for k, o in enumerate(objs):
        if o is None:
            continue
        b = tuple(slice(max(q.start - M, 0), min(q.stop + M, G.shape[d])) for d, q in enumerate(o))
        g = G[b]; a = add[b] & (lab[b] == k + 1)
        if not a.any():
            continue
        sd = _sd(m[b] | a, h)
        # fade toward the box faces (3 voxels) so nothing changes at the box border
        wb = np.ones(g.shape, np.float32)
        for d in range(3):
            idx = np.arange(b[d].start, b[d].stop)
            dist = np.minimum(idx - lo_i[d], hi_i[d] - 1 - idx).astype(np.float32)
            sh = [1, 1, 1]; sh[d] = -1
            wb = wb * np.clip(dist / 3.0, 0, 1).reshape(sh)
        near = ndi.distance_transform_edt(~a) <= 3
        wn = np.clip(ndi.gaussian_filter(near.astype(np.float32), 1.0) * 1.5, 0, 1) * wb
        G[b] = g * (1 - wn) + np.minimum(g, sd + bias * h) * wn
    F.G[sl] = G
    if verbose:
        print(f'seams.soft_close {tag} {tuple(round(b, 1) for b in box)} r={r} dmin={dmin}: +{n} voxels ({n * h ** 3:.2f} mm3) in {nc} clusters', flush=True)
    return n


def _seg_dist(P, a, b):
    a = np.asarray(a, float); b = np.asarray(b, float); ab = b - a
    t = np.clip(((P - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(P - (a + t[..., None] * ab), axis=-1)


def smooth_zone(F, segs, r_in, r_out, sigma, verbose=True, tag=''):
    """Low-pass the field near a set of segments/points (fine relief < ~3*sigma pitch fades out, broad folds stay).
    segs: list of (a, b) 3D segments (a == b for a ball); weight 1 within r_in of a segment, 0 beyond r_out."""
    h = F.h
    pts = np.array([p for sg in segs for p in sg], float)
    box = (*(pts.min(0) - r_out), *(pts.max(0) + r_out))
    pad = int(np.ceil(3 * sigma / h)) + 2
    sl = _idx(F, box, pad)
    G = F.G[sl]
    if min(G.shape) < 2:
        return
    xs = [F.lo[d] + np.arange(sl[d].start, sl[d].stop) * h for d in range(3)]
    P = np.stack(np.meshgrid(*xs, indexing='ij'), -1)
    dmin = np.full(G.shape, 1e9, np.float32)
    for a, b in segs:
        dmin = np.minimum(dmin, _seg_dist(P, a, b))
    t = np.clip((r_out - dmin) / (r_out - r_in), 0, 1)
    w = (t * t * (3 - 2 * t)).astype(np.float32)
    Gs = ndi.gaussian_filter(G, sigma / h, mode='nearest')
    F.G[sl] = G * (1 - w) + Gs * w
    if verbose:
        print(f'seams.smooth_zone {tag}: sigma={sigma} r={r_in}..{r_out}, {int((w > 0).sum())} voxels', flush=True)


def base_fill(F, zfoot=1.2, zmax=6.0, verbose=True, boxes_zmax=(), close_boxes=()):
    """Flat print base. footprint = solid at 0<z<=zfoot (holes filled). Every footprint column is filled from the table up to
    its highest solid voxel below zmax (per-box override of zmax via boxes_zmax=[(x0,y0,x1,y1,zmax)])."""
    h = F.h
    if F.lo[2] > 0 or F.lo[2] + (F.shape[2] - 1) * h < zmax + 1:   # sub-box build (e.g. head close-up): no base here
        return 0
    k0 = int(np.ceil((1e-6 - F.lo[2]) / h))          # first layer above the table
    kf = int(np.floor((zfoot - F.lo[2]) / h))
    kz = int(np.floor((max([zmax] + [b[4] for b in boxes_zmax]) - F.lo[2]) / h))
    S = F.G[:, :, k0:kz + 1] < 0
    foot = S[:, :, :kf - k0 + 1].any(axis=2)
    xs = F.lo[0] + np.arange(F.shape[0]) * h; ys = F.lo[1] + np.arange(F.shape[1]) * h
    for x0, y0, x1, y1, r in close_boxes:     # seal narrow mouths of base pockets (2D closing, local)
        ii = np.nonzero((xs >= x0) & (xs <= x1))[0]; jj = np.nonzero((ys >= y0) & (ys <= y1))[0]
        sub = foot[ii[0]:ii[-1] + 1, jj[0]:jj[-1] + 1]
        rv = r / h
        dil = ndi.distance_transform_edt(~np.pad(sub, 1)) <= rv
        clo = (ndi.distance_transform_edt(dil) > rv)[1:-1, 1:-1]
        foot[ii[0]:ii[-1] + 1, jj[0]:jj[-1] + 1] = sub | clo
    foot = ndi.binary_fill_holes(foot)
    # per-column zmax
    zm = np.full(foot.shape, zmax, np.float32)
    for x0, y0, x1, y1, z in boxes_zmax:
        zm[np.ix_((xs >= x0) & (xs <= x1), (ys >= y0) & (ys <= y1))] = z
    zc = F.lo[2] + np.arange(k0, kz + 1) * h
    S2 = S & (zc[None, None, :] <= zm[:, :, None])
    # highest solid voxel per column (within zmax)
    has = S2.any(axis=2)
    ktop = S2.shape[2] - 1 - np.argmax(S2[:, :, ::-1], axis=2)
    # footprint columns with nothing below their zmax (deep pockets): fill up to the first solid above
    deep = foot & ~has & S.any(axis=2)
    ktop = np.where(deep, np.argmax(S, axis=2), ktop)
    col = foot & (has | deep)
    fill = (np.arange(S.shape[2])[None, None, :] <= ktop[:, :, None]) & col[:, :, None]
    add = fill & ~S
    n = int(add.sum())
    if n:
        # smooth SDF of (solid | fill) in the slab, blended in only near the added voxels
        ka = kz + 1 + 4
        sub = F.G[:, :, k0:ka]
        msk = sub < 0
        msk[:, :, :S.shape[2]] |= fill
        # restrict the work to the xy bbox of the added voxels
        ax = np.nonzero(add.any(axis=(1, 2)))[0]; ay = np.nonzero(add.any(axis=(0, 2)))[0]
        i0, i1 = max(ax[0] - 6, 0), min(ax[-1] + 7, F.shape[0]); j0, j1 = max(ay[0] - 6, 0), min(ay[-1] + 7, F.shape[1])
        Gs = sub[i0:i1, j0:j1]
        ms = msk[i0:i1, j0:j1]
        ad = np.zeros(ms.shape, bool); ad[:, :, :S.shape[2]] = add[i0:i1, j0:j1]
        # sd of the union; mirror the table plane so the base stays flat (pad 3 layers below)
        mp = np.concatenate([ms[:, :, :1].repeat(3, axis=2), ms], axis=2)
        sd = _sd(mp, h)[:, :, 3:]
        _blend_add(Gs, sd, ad, h)
        sub[i0:i1, j0:j1] = Gs
        F.G[:, :, k0:ka] = sub
    # re-impose the table plane (nothing below z=0, flat bottom)
    zz = (F.lo[2] + np.arange(F.shape[2]) * h).astype(np.float32)
    kk = int(np.ceil((3.0 - F.lo[2]) / h))
    F.G[:, :, :kk] = np.maximum(F.G[:, :, :kk], -zz[None, None, :kk])
    if verbose:
        print(f'seams.base_fill: footprint {foot.sum() * h * h:.0f} mm2, filled {n} voxels ({n * h ** 3:.1f} mm3) below z<={zmax}', flush=True)
    return n


def drop_specks(F, vmin=2.0, verbose=True):
    m = F.G < 0
    lab, n = ndi.label(m, S26)
    if n <= 1:
        return 0
    cnt = np.bincount(lab.ravel()); cnt[0] = 0
    big = np.argmax(cnt)
    small = [k for k in range(1, n + 1) if k != big and cnt[k] * F.h ** 3 < vmin]
    if small:
        kill = np.isin(lab, small)
        F.G[kill] = F.h
    if verbose:
        print(f'seams.drop_specks: {n} solid components, removed {len(small)} specks', flush=True)
    return len(small)
