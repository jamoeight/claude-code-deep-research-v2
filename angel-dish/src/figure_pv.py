"""Figure-agent fast preview (helper; does not change shared files).
   python3 figure_pv.py TAG [--h 0.5] [--parts dish,figure,head,wings] [--views v1,v2] [--res 900] [--samples 16]
Views: ref | c_<region> (ref camera cropped to a compare.py region, rendered at --scale) |
       fFront fBack fLeft fRight fTQL fTQR fBackL fBackR fTop (orbit close-ups around the figure)
Other parts' fields are cached per h in out/_figcache (rebuilt when their module files change)."""
import sys, os, glob, time, subprocess, json, importlib
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from sdf import Field, Batch, save_ply
import model

a = sys.argv[1:]
tag = a[0]
def opt(n, d):
    return a[a.index(n) + 1] if n in a else d
h = float(opt('--h', '0.5')); parts = opt('--parts', 'dish,figure,head,wings').split(',')
views = opt('--views', 'ref'); res = opt('--res', '900'); samples = opt('--samples', '16'); scale = opt('--scale', '2.0')
od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
cd = os.path.join(HERE, 'out', '_figcache'); os.makedirs(cd, exist_ok=True)
t0 = time.time()
log = lambda *x: print(f'[{time.time() - t0:6.1f}s]', *x, flush=True)


def part_field(p, F0):
    if p == 'figure':
        import figure
        return figure.component(F0.blank())
    srcs = glob.glob(os.path.join(HERE, p + '*.py'))
    mt = max(os.path.getmtime(s) for s in srcs)
    fn = os.path.join(cd, f'{p}_{h:.3f}' + ('_' + '_'.join('%g' % v for v in BOX) if BOX else '') + '.npy'); meta = fn + '.json'
    if os.path.exists(fn) and os.path.exists(meta) and json.load(open(meta))['mt'] >= mt:
        G = F0.blank(); G.G = np.load(fn); return G
    mod = importlib.import_module(p)
    G = mod.component(F0.blank())
    np.save(fn, G.G); json.dump({'mt': mt}, open(meta, 'w'))
    return G


BOX = [float(v) for v in opt('--box', '').split(',')] if '--box' in a else None
F0 = Field(tuple(BOX[:3]) if BOX else model.LO, tuple(BOX[3:]) if BOX else model.HI, h)
if BOX:
    cd = os.path.join(HERE, 'out', '_figcache_box'); os.makedirs(cd, exist_ok=True)
F = None
for p in model.PARTS:
    if p not in parts:
        continue
    G = part_field(p, F0)
    if F is None:
        F = G
    else:
        F.combine(G, 'union', model.BLEND[p])
    del G
    log(p)
floor = Batch(); floor.rbox((0, 0, -400), (400, 400, 400))
F.apply(floor, 'sub')
v, f = F.mesh()
save_ply(os.path.join(od, 'model.ply'), v, f)
log('mesh', len(f))
del F
r = subprocess.run([sys.executable, os.path.join(HERE, 'figure_render.py'), os.path.join(od, 'model.ply'), os.path.join(od, 'r'), views,
                    '--res', res, '--samples', samples, '--scale', scale], cwd=HERE, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-3000:], r.stderr[-3000:]); sys.exit(1)
log('rendered')
# side-by-side for crop views
from PIL import Image
sys.argv = ['x']
REG = {'full': (0, 0, 1179, 1078), 'figure': (250, 90, 620, 640), 'face': (360, 110, 540, 300),
       'wingR': (480, 30, 1179, 620), 'wingL': (0, 30, 430, 900), 'front': (0, 580, 1179, 1078),
       'torso': (300, 250, 600, 560), 'skirt': (280, 430, 820, 760), 'body': (300, 240, 680, 720),
       'arm': (300, 280, 420, 560), 'neck': (400, 230, 560, 400)}
ref = Image.open(os.path.join(HERE, '..', 'ref', 'reference.png')).convert('RGB')
for v in views.split(','):
    if v.startswith('c_'):
        box = REG[v[2:]]
        rr = Image.open(os.path.join(od, f'r_{v}.png')).convert('RGB')
        aa = ref.crop(box).resize(rr.size, Image.LANCZOS)
        o = Image.new('RGB', (rr.width * 2, rr.height)); o.paste(aa, (0, 0)); o.paste(rr, (rr.width, 0))
        o.save(os.path.join(od, f'cmp_{v[2:]}.png'))
    if v == 'ref':
        rr = Image.open(os.path.join(od, 'r_ref.png')).convert('RGB').resize(ref.size, Image.LANCZOS)
        o = Image.new('RGB', (ref.width * 2, ref.height)); o.paste(ref, (0, 0)); o.paste(rr, (ref.width, 0))
        o.resize((ref.width, ref.height // 2)).save(os.path.join(od, 'cmp_full.png'))
log('done', od)
