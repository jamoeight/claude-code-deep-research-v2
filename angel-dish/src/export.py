"""Final export: python3 export.py OUT.stl [--h 0.22] [--target_faces 2500000]
High-res SDF build -> marching cubes -> keep largest component -> quadric decimation ->
scale to real mm (layout.EXPORT_SCALE) -> binary STL, plus a validation report."""
import sys, time, json
import numpy as np
import model
from layout import EXPORT_SCALE
from sdf import save_stl, save_ply


def largest_component(v, f):
    import scipy.sparse as sp
    from scipy.sparse.csgraph import connected_components
    n = len(v)
    e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
    A = sp.coo_matrix((np.ones(len(e), np.int8), (e[:, 0], e[:, 1])), shape=(n, n))
    nc, lab = connected_components(A, directed=False)
    counts = np.bincount(lab)
    keep = np.argmax(counts)
    info = sorted(counts.tolist(), reverse=True)[:10]
    vm = lab == keep
    fm = vm[f[:, 0]]
    remap = -np.ones(n, np.int64); remap[np.where(vm)[0]] = np.arange(vm.sum())
    return v[vm], remap[f[fm]], nc, info


def main():
    a = sys.argv[1:]
    out = a[0]
    h = float(a[a.index('--h') + 1]) if '--h' in a else 0.22
    tf = int(a[a.index('--target_faces') + 1]) if '--target_faces' in a else 2_500_000
    t0 = time.time()
    F = model.build(h)
    v, f = F.mesh()
    del F
    print(f'[{time.time() - t0:.0f}s] marching cubes: {len(v)} verts {len(f)} faces', flush=True)
    v, f, nc, info = largest_component(v, f)
    print(f'components: {nc}, largest sizes: {info}', flush=True)
    if len(f) > tf:
        import fast_simplification
        v, f = fast_simplification.simplify(v.astype(np.float32), f.astype(np.int64), target_reduction=1 - tf / len(f), agg=5)
        v, f, nc2, _ = largest_component(v, f)
        print(f'[{time.time() - t0:.0f}s] decimated: {len(v)} verts {len(f)} faces', flush=True)
    v = (v * EXPORT_SCALE).astype(np.float32)
    v[:, 2] -= v[:, 2].min()           # sit exactly on the bed
    save_stl(out, v, f)
    save_ply(out.replace('.stl', '.ply'), v, f)
    # validation
    import trimesh
    m = trimesh.Trimesh(v, f, process=False)
    rep = dict(faces=int(len(f)), verts=int(len(v)), watertight=bool(m.is_watertight), winding_consistent=bool(m.is_winding_consistent),
               volume_cm3=float(m.volume / 1000), bbox_mm=[[round(float(x), 1) for x in m.bounds[0]], [round(float(x), 1) for x in m.bounds[1]]],
               extents_mm=[round(float(x), 1) for x in m.extents], euler=int(m.euler_number), seconds=round(time.time() - t0))
    print(json.dumps(rep, indent=1))
    json.dump(rep, open(out.replace('.stl', '_report.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
