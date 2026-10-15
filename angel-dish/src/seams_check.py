"""Print-readiness / junction analysis of an assembled field (owned by the integrator).
   python3 seams_check.py out/TAG/post.npy [--slit 0.6] [--thin 1.0] [--handles] [--box x0,y0,z0,x1,y1,z1]
Reports: solid components (floating bits), enclosed voids, Betti numbers (tunnels), knife slits (closing test),
thin slivers (medial thickness), base recesses / footprint holes."""
import sys, os, json, time
import numpy as np
from scipy import ndimage as ndi
from skimage.measure import euler_number

S26 = np.ones((3, 3, 3), bool)


def load(path):
    meta = json.load(open(os.path.join(os.path.dirname(path), 'raw.json')))
    return np.load(path, mmap_mode='r'), np.asarray(meta['lo'], float), float(meta['h'])


def betti(a):
    p = np.pad(a, 1)
    chi = euler_number(p, connectivity=3)
    b0 = ndi.label(p, S26)[1]
    b2 = ndi.label(~p)[1] - 1
    return b0, b0 + b2 - chi, b2


def clusters(mask, P0, h, val=None, top=15, minvox=1, dil=1, label=''):
    if dil:
        lab, n = ndi.label(ndi.binary_dilation(mask, iterations=dil), S26)
        lab = np.where(mask, lab, 0)
    else:
        lab, n = ndi.label(mask, S26)
    if n == 0:
        return []
    idx = np.nonzero(mask)
    li = lab[idx]
    cnt = np.bincount(li, minlength=n + 1)
    res = []
    for k in np.argsort(-cnt):
        if k == 0 or cnt[k] < minvox:
            continue
        m = li == k
        Q = np.stack([idx[0][m], idx[1][m], idx[2][m]], 1) * h + P0
        e = {'n': int(cnt[k]), 'vol': round(float(cnt[k] * h ** 3), 2), 'c': np.round(Q.mean(0), 1).tolist(),
             'lo': np.round(Q.min(0), 1).tolist(), 'hi': np.round(Q.max(0), 1).tolist()}
        if val is not None:
            e['max'] = round(float(val[idx[0][m], idx[1][m], idx[2][m]].max()), 2)
        res.append(e)
        if len(res) >= top:
            break
    return res


def main():
    a = sys.argv[1:]
    path = a[0]
    opt = lambda n, d: a[a.index(n) + 1] if n in a else d
    G, lo, h = load(path)
    t0 = time.time()
    ins_full = np.asarray(G) < 0
    if '--box' in a:
        b = [float(v) for v in opt('--box', '').split(',')]
        i0 = np.clip(np.floor((np.array(b[:3]) - lo) / h).astype(int), 0, ins_full.shape)
        i1 = np.clip(np.ceil((np.array(b[3:]) - lo) / h).astype(int) + 1, 0, ins_full.shape)
    else:
        nz = [np.nonzero(ins_full.any(axis=tuple(j for j in range(3) if j != i)))[0] for i in range(3)]
        i0 = np.array([max(n[0] - 4, 0) for n in nz]); i1 = np.array([min(n[-1] + 5, s) for n, s in zip(nz, ins_full.shape)])
    sl = tuple(slice(x, y) for x, y in zip(i0, i1))
    ins = np.ascontiguousarray(ins_full[sl]); del ins_full
    P0 = lo + i0 * h
    out = {'h': h, 'box_lo': np.round(P0, 2).tolist(), 'shape': list(ins.shape)}
    # ---- components
    lab, n = ndi.label(ins, S26)
    cnt = np.bincount(lab.ravel())
    cnt[0] = 0
    order = np.argsort(-cnt)
    comps = []
    for k in order[:min(n, 12)]:
        if cnt[k] == 0:
            continue
        w = np.argwhere(lab == k) if cnt[k] < 2e6 else None
        e = {'n': int(cnt[k]), 'vol': round(float(cnt[k] * h ** 3), 2)}
        if w is not None:
            e['lo'] = np.round(w.min(0) * h + P0, 1).tolist(); e['hi'] = np.round(w.max(0) * h + P0, 1).tolist()
        comps.append(e)
    out['components'] = n; out['comp_list'] = comps
    del lab
    # ---- voids
    labo, no = ndi.label(~ins)
    border = np.unique(np.concatenate([labo[0].ravel(), labo[-1].ravel(), labo[:, 0].ravel(), labo[:, -1].ravel(), labo[:, :, 0].ravel(), labo[:, :, -1].ravel()]))
    enc = np.setdiff1d(np.arange(1, no + 1), border)
    vm = np.isin(labo, enc)
    out['voids'] = int(len(enc)); out['void_list'] = clusters(vm, P0, h, dil=0)
    del labo, vm
    # ---- betti
    b = betti(ins)
    out['betti'] = list(map(int, b)); out['genus'] = int(b[1])
    print(json.dumps({k: out[k] for k in ('components', 'voids', 'betti')}), '%.0fs' % (time.time() - t0), flush=True)
    # ---- slits: closing with ball r
    r = float(opt('--slit', '0.6')); rv = r / h
    d_out = ndi.distance_transform_edt(~ins).astype(np.float32)
    dil = d_out <= rv
    d_dil = ndi.distance_transform_edt(dil).astype(np.float32)
    clo = d_dil > rv
    add = clo & ~ins
    # depth of each added voxel inside the closed body (how far below the closed surface the crack goes)
    dep = ndi.distance_transform_edt(clo).astype(np.float32) * h
    deep = add & (dep >= float(opt('--deep', '0.6')))
    out['slit_r'] = r
    out['slit_vol_all'] = round(float(add.sum() * h ** 3), 1)
    out['slit_vol_deep'] = round(float(deep.sum() * h ** 3), 1)
    # cluster: deep voxels seed, report cluster extent over the 'add' set
    out['slits'] = clusters(deep, P0, h, val=dep, top=int(opt('--top', '25')), dil=1)
    del dil, d_dil, clo, add, deep, dep
    # ---- thin (medial thickness)
    thr = float(opt('--thin', '1.0'))
    edt = ndi.distance_transform_edt(ins).astype(np.float32) * h
    mx = ndi.maximum_filter(edt, size=3)
    ridge = ins & (edt >= mx - 1e-6)
    del mx
    zc = P0[2] + np.arange(ins.shape[2]) * h
    thin = ridge & (edt < thr / 2) & (zc[None, None, :] > 0.5)
    out['thin_thr'] = thr
    out['thin'] = clusters(thin, P0, h, val=-2 * edt, top=20, dil=2, minvox=2)
    rr = edt[ridge] * 2
    out['thick_pct'] = np.round(np.percentile(rr, [0.1, 1, 5, 50]), 2).tolist()
    del edt, ridge, thin
    # ---- base
    k0 = int(np.ceil((0.0 - P0[2]) / h))
    lay = ins[:, :, k0]
    out['base_z'] = round(float(P0[2] + k0 * h), 2)
    out['foot_area'] = round(float(lay.sum() * h * h), 1)
    holes = ndi.binary_fill_holes(lay) & ~lay
    out['foot_holes'] = clusters(holes[:, :, None], P0 + [0, 0, k0 * h], h, dil=0, top=10)
    # recesses: inside the hole-filled footprint (z<=1.2), empty voxels at z in [0, 3] with solid above within 6 mm
    kf = int(np.floor((1.2 - P0[2]) / h))
    foot = ndi.binary_fill_holes(ins[:, :, k0:kf + 1].any(axis=2))
    kk = int(round(3.0 / h)); ku = int(round(6 / h))
    rec = np.zeros(ins.shape[:2] + (kk,), bool)
    for j in range(kk):
        k = k0 + j
        top = ins[:, :, k + 1:k + 1 + ku].any(axis=2)
        rec[:, :, j] = ~ins[:, :, k] & top & foot
    # single-layer skins: solid base voxel with empty directly above while solid exists higher up
    skin = ins[:, :, k0] & ~ins[:, :, k0 + 1] & ~ins[:, :, k0 + 2] & ins[:, :, k0 + 3:k0 + 3 + ku].any(axis=2)
    out['skins_mm2'] = round(float(skin.sum() * h * h), 1)
    out['recess_vol'] = round(float(rec.sum() * h ** 3), 1)
    out['recesses'] = clusters(rec, P0 + [0, 0, k0 * h], h, dil=1, top=12, minvox=3)
    for k, v in out.items():
        if isinstance(v, list) and v and isinstance(v[0], dict):
            print(f'{k}: ({len(v)})')
            for e in v:
                print('   ', ' '.join(f'{a}={b}' for a, b in e.items()))
        else:
            print(f'{k}: {v}')
    json.dump(out, open(path.rsplit('.', 1)[0] + '_check.json', 'w'))
    print('done %.0fs' % (time.time() - t0))
    if '--handles' in a:
        handles(ins, P0, h)


def handles(ins, lo, h):
    MIN = int(round(8 / h))
    out = []

    def sub(b):
        return ins[b[0]:b[1], b[2]:b[3], b[4]:b[5]]

    def rec(b, val):
        sz = [b[1] - b[0], b[3] - b[2], b[5] - b[4]]
        ax = int(np.argmax(sz))
        if sz[ax] <= MIN:
            out.append((b, val)); return
        m = (b[2 * ax] + b[2 * ax + 1]) // 2
        c1 = list(b); c1[2 * ax + 1] = m + 3
        c2 = list(b); c2[2 * ax] = m - 3
        v1 = betti(sub(c1))[1]; v2 = betti(sub(c2))[1]
        if v1 + v2 < val:
            out.append((b, val - v1 - v2))
        if v1 > 0: rec(c1, v1)
        if v2 > 0: rec(c2, v2)
    full = (0, ins.shape[0], 0, ins.shape[1], 0, ins.shape[2])
    rec(full, betti(ins)[1])
    for b, val in out:
        p0 = lo + np.array([b[0], b[2], b[4]]) * h; p1 = lo + np.array([b[1], b[3], b[5]]) * h
        print('handle b1=%d  box %s .. %s' % (val, np.round(p0, 1).tolist(), np.round(p1, 1).tolist()), flush=True)


if __name__ == '__main__':
    main()
