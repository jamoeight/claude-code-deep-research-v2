"""Integrator dev loop (owned by the integrator).
   python3 seams_dev.py build RAWTAG h            -> out/RAWTAG/raw.npy (assembled field, NO seams/post)
   python3 seams_dev.py apply RAWTAG OUTTAG [--views ..] [--regions ..] [--res N] [--samples N] [--norender]
        loads raw field, runs seams.apply, saves post.npy + model.ply, renders + compare (same outputs as preview.py)."""
import sys, os, json, time, subprocess
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def load_field(path):
    from sdf import Field
    meta = json.load(open(os.path.join(os.path.dirname(path), 'raw.json')))
    F = Field.__new__(Field)
    F.lo = np.asarray(meta['lo'], float); F.h = float(meta['h'])
    F.G = np.load(path)
    F.shape = F.G.shape
    return F


def opt(a, name, default):
    return a[a.index(name) + 1] if name in a else default


def main():
    a = sys.argv[1:]
    cmd = a[0]
    if cmd == 'build':
        tag, h = a[1], float(a[2])
        os.environ['NOPOST'] = '1'
        import model
        od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
        F = model.build(h)
        np.save(os.path.join(od, 'raw.npy'), F.G)
        json.dump({'lo': list(F.lo), 'h': F.h}, open(os.path.join(od, 'raw.json'), 'w'))
        print('saved', od)
    elif cmd == 'apply':
        src, tag = a[1], a[2]
        import seams
        from sdf import save_ply
        t = time.time()
        F = load_field(os.path.join(HERE, 'out', src, 'raw.npy'))
        od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
        seams.apply(F)
        print('seams.apply %.0fs' % (time.time() - t), flush=True)
        np.save(os.path.join(od, 'post.npy'), F.G)
        json.dump({'lo': list(F.lo), 'h': F.h}, open(os.path.join(od, 'raw.json'), 'w'))
        v, f = F.mesh()
        print('mesh', len(v), len(f), flush=True)
        save_ply(os.path.join(od, 'model.ply'), v, f)
        if '--norender' in a:
            return
        views = opt(a, '--views', 'ref'); regions = opt(a, '--regions', 'full')
        res = opt(a, '--res', '900'); samples = opt(a, '--samples', '24')
        r = subprocess.run([sys.executable, os.path.join(HERE, 'render.py'), os.path.join(od, 'model.ply'), os.path.join(od, 'r'), views,
                            '--res', res, '--samples', samples], cwd=HERE, capture_output=True, text=True)
        if r.returncode:
            print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
        if 'ref' in views.split(','):
            for reg in regions.split(','):
                subprocess.run([sys.executable, os.path.join(HERE, 'compare.py'), os.path.join(od, 'r_ref.png'), os.path.join(od, f'cmp_{reg}.png'),
                                '--region', reg], check=True, cwd=HERE)
        print('done %.0fs' % (time.time() - t), od)


if __name__ == '__main__':
    main()
