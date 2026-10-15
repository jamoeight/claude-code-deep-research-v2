"""Fast head iteration (head agent tool; not used by model.py).
python3 head_fast.py TAG [--h 0.3] [--views refzoom,wL,wB,zS] [--pbox 320,100,540,380] [--res 500] [--samples 14] [--refig]
Figure field is cached (box -46,2,0..12,46,104, z0 = 0 so the figure matches the full build); the head is rebuilt and
union-ed with the model.py blend, meshed above z 44 and rendered with head_render.py."""
import sys, os, subprocess, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
a = sys.argv[1:]
tag = a[0]


def opt(n, d):
    return a[a.index(n) + 1] if n in a else d


h = float(opt('--h', '0.3'))
views = opt('--views', 'refzoom,wL,wB,zS'); pbox = opt('--pbox', '320,100,540,380')
res = opt('--res', '500'); samples = opt('--samples', '14'); scale = opt('--scale', '4')
od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
t = time.time()
from sdf import Field, Batch, save_ply
LO, HI = (-46, 2, 0), (12, 46, 104)
cache = os.path.join(HERE, 'out', 'figcache_%.2f.npy' % h)
F = Field(LO, HI, h)
if '--nofig' in a:
    pass
elif os.path.exists(cache) and '--refig' not in a:
    F.G = np.load(cache)
else:
    import figure
    F = figure.component(F.blank())
    np.save(cache, F.G)
print('figure %.0fs' % (time.time() - t), flush=True)
if '--nohead' not in a:
    import head
    G = head.component(F.blank())
    F.combine(G, 'union', 1.2)
    del G
print('head %.0fs' % (time.time() - t), flush=True)
k0 = int((44 - LO[2]) / h)
S = Field.__new__(Field); S.h = h; S.lo = F.lo + np.array([0, 0, k0 * h]); S.G = np.ascontiguousarray(F.G[:, :, k0:]); S.shape = S.G.shape
v, f = S.mesh()
save_ply(os.path.join(od, 'model.ply'), v, f)
print('mesh %.0fs' % (time.time() - t), flush=True)
if views:
    r = subprocess.run([sys.executable, 'head_prev.py', tag, '--norebuild', '--views', views, '--pbox', pbox, '--res', res,
                        '--samples', samples, '--scale', scale], cwd=HERE, capture_output=True, text=True)
    print(r.stdout[-500:], r.stderr[-800:] if r.returncode else '')
print('done %.0fs' % (time.time() - t), od)
