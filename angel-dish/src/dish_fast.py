"""Fast preview for the dish sculptor: the other components' fields are cached per (h, box, source mtimes).
   python3 dish_fast.py TAG [--h 0.45] [--parts dish,figure,head,wings] [--views ref,...] [--regions full,...]
                       [--res 900] [--samples 24] [--box x0,y0,z0,x1,y1,z1] [--post]
Same outputs as preview.py (out/TAG/model.ply, r_<view>.png, cmp_<region>.png)."""
import sys, os, glob, hashlib, subprocess, time, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)
import model
from sdf import Field, Batch, save_ply

a = sys.argv[1:]
tag = a[0]


def opt(name, default):
    return a[a.index(name) + 1] if name in a else default


h = float(opt('--h', '0.45')); parts = opt('--parts', 'dish,figure,head,wings').split(',')
views = opt('--views', 'ref'); regions = opt('--regions', 'full'); res = opt('--res', '900'); samples = opt('--samples', '24')
lo, hi = model.LO, model.HI
if '--box' in a:
    b = [float(x) for x in opt('--box', '').split(',')]
    lo, hi = tuple(b[:3]), tuple(b[3:])
od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
cd = os.path.join(HERE, 'out', 'cache'); os.makedirs(cd, exist_ok=True)
t0 = time.time()


def key(p):
    fs = sorted(glob.glob(os.path.join(HERE, f'{p}.py')) + glob.glob(os.path.join(HERE, f'{p}_*.py')))
    s = '|'.join(f'{os.path.basename(f)}:{os.path.getmtime(f)}' for f in fs) + f'|{h}|{lo}|{hi}'
    return hashlib.md5(s.encode()).hexdigest()[:12]


F = Field(lo, hi, h)
first = True
for p in model.PARTS:
    if p not in parts:
        continue
    if p == 'dish':
        mod = importlib.import_module('dish')
        G = mod.component(F.blank())
    else:
        fn = os.path.join(cd, f'{p}_{key(p)}.npy')
        if os.path.exists(fn):
            G = F.blank(); G.G = np.load(fn)
        else:
            for old in glob.glob(os.path.join(cd, f'{p}_*.npy')):
                if len(glob.glob(os.path.join(cd, '*.npy'))) > 8:
                    os.remove(old)
            mod = importlib.import_module(p)
            G = mod.component(F.blank())
            np.save(fn, G.G)
    if first:
        F = G; first = False
    else:
        F.combine(G, 'union', model.BLEND[p])
    del G
    print(f'[{time.time() - t0:5.1f}s] {p}', flush=True)
floor = Batch(); floor.rbox((0, 0, -400), (400, 400, 400))
F.apply(floor, 'sub')
if '--post' in a and len(parts) == 4:
    import seams
    seams.apply(F)
v, f = F.mesh()
save_ply(os.path.join(od, 'model.ply'), v, f)
print(f'[{time.time() - t0:5.1f}s] mesh {len(v)}', flush=True)
r = subprocess.run([sys.executable, os.path.join(HERE, 'render.py'), os.path.join(od, 'model.ply'), os.path.join(od, 'r'), views, '--res', res, '--samples', samples],
                   cwd=HERE, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
if 'ref' in views.split(','):
    for reg in regions.split(','):
        if reg:
            subprocess.run([sys.executable, os.path.join(HERE, 'compare.py'), os.path.join(od, 'r_ref.png'), os.path.join(od, f'cmp_{reg}.png'), '--region', reg], check=True, cwd=HERE)
print('done in %.0fs ->' % (time.time() - t0), od)
