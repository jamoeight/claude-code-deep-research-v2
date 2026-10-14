"""Fast wings iteration preview (wings agent tool).
Caches the union of the other parts (dish, figure, head) per (h, box, file mtimes) and only rebuilds the wings.
Reproduces model.build exactly (wings are the last union, blend 1.5, then floor cut).
   python3 wings_prev.py TAG [--h 0.5] [--views ref,threeqR] [--regions full,wingR] [--res 800] [--samples 16]
                             [--box x0,y0,z0,x1,y1,z1] [--parts dish,figure,head,wings] [--nocache]
"""
import sys, os, time, hashlib, subprocess, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model
from sdf import Field, Batch, save_ply

a = sys.argv[1:]
tag = a[0]


def opt(name, default):
    return a[a.index(name) + 1] if name in a else default


h = float(opt('--h', '0.5')); views = opt('--views', 'ref'); regions = opt('--regions', 'full')
res = opt('--res', '800'); samples = opt('--samples', '16'); parts = opt('--parts', 'dish,figure,head,wings').split(',')
lo, hi = model.LO, model.HI
if '--box' in a:
    b = [float(x) for x in opt('--box', '').split(',')]
    lo, hi = tuple(b[:3]), tuple(b[3:])
od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
t0 = time.time()
others = [p for p in model.PARTS if p in parts and p != 'wings']
key = hashlib.md5(repr((h, lo, hi, others, [os.path.getmtime(os.path.join(HERE, f)) for f in sorted(os.listdir(HERE))
                                              if f.endswith('.py') and not f.startswith('wings') and f.split('_')[0].split('.')[0] in others])).encode()).hexdigest()[:12]
cdir = os.path.join(HERE, 'out', '_cache'); os.makedirs(cdir, exist_ok=True)
cpath = os.path.join(cdir, f'others_{key}.npy')
F = Field(lo, hi, h)
if others:
    if os.path.exists(cpath) and '--nocache' not in a:
        F.G = np.load(cpath)
        print('cached others', cpath)
    else:
        first = True
        for p in model.PARTS:
            if p not in others:
                continue
            G = importlib.import_module(p).component(F.blank())
            if first:
                F = G; first = False
            else:
                F.combine(G, 'union', model.BLEND[p])
            del G
            print(f'[{time.time() - t0:5.1f}s] {p}', flush=True)
        np.save(cpath, F.G)
if 'wings' in parts:
    import wings
    t1 = time.time()
    W = wings.component(F.blank())
    print(f'wings built in {time.time() - t1:.1f}s', flush=True)
    if others:
        F.combine(W, 'union', model.BLEND['wings'])
    else:
        F = W
    if '--savewings' in a:
        np.save(os.path.join(od, 'wings_G.npy'), W.G)
    del W
floor = Batch(); floor.rbox((0, 0, -400), (400, 400, 400))
F.apply(floor, 'sub')
v, f = F.mesh()
print('mesh', len(v), len(f), f'{time.time() - t0:.0f}s', flush=True)
save_ply(os.path.join(od, 'model.ply'), v, f)
if '--norender' in a:
    sys.exit(0)
r = subprocess.run([sys.executable, os.path.join(HERE, 'render.py'), os.path.join(od, 'model.ply'), os.path.join(od, 'r'), views,
                    '--res', res, '--samples', samples], cwd=HERE, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
if 'ref' in views.split(','):
    for reg in regions.split(','):
        subprocess.run([sys.executable, os.path.join(HERE, 'compare.py'), os.path.join(od, 'r_ref.png'), os.path.join(od, f'cmp_{reg}.png'),
                        '--region', reg], check=True, cwd=HERE)
print('done in %.0fs ->' % (time.time() - t0), od)
