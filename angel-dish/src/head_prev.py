"""Fast head close-up preview (head agent tool; not used by model.py).
python3 head_prev.py TAG [--h 0.2] [--parts figure,head,wings] [--box x0,y0,z0,x1,y1,z1]
                         [--pbox 320,100,540,380] [--scale 4] [--views refzoom,front,q3,profile,wL,wB] [--samples 20] [--res 640]
Outputs out/TAG/: model.ply, h_<view>.png, hz.png (ref crop | render | edges), hv.png (other views strip)."""
import sys, os, subprocess, time
import numpy as np
from PIL import Image, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
REF = '/tmp/claude-0/-home-user-claude-code-deep-research-v2/7b47191c-d71c-5999-a319-d37f870318ab/scratchpad/ref/reference.png'
a = sys.argv[1:]
tag = a[0]


def opt(n, d):
    return a[a.index(n) + 1] if n in a else d


h = opt('--h', '0.2'); parts = opt('--parts', 'figure,head,wings')
box = opt('--box', '-46,2,52,12,46,104'); pbox = opt('--pbox', '320,100,540,380')
views = opt('--views', 'refzoom,front,q3,profile,wL,wB'); scale = opt('--scale', '4')
samples = opt('--samples', '20'); res = opt('--res', '640')
od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
t = time.time()
if '--norebuild' not in a:
    subprocess.run([sys.executable, 'model.py', os.path.join(od, 'model.ply'), h, '--parts', parts, '--box', box], check=True, cwd=HERE)
r = subprocess.run([sys.executable, 'head_render.py', os.path.join(od, 'model.ply'), os.path.join(od, 'h'), '--box', pbox,
                    '--scale', scale, '--samples', samples, '--views', views, '--res', res], cwd=HERE, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-1500:], r.stderr[-1500:]); sys.exit(1)
vs = views.split(',')
if 'refzoom' in vs:
    b = tuple(int(v) for v in pbox.split(','))
    ref = Image.open(REF).convert('RGB').crop(b)
    rr = Image.open(os.path.join(od, 'h_refzoom.png')).convert('RGB')
    H = 900; s = H / ref.height; size = (int(ref.width * s), H)
    A = ref.resize(size, Image.BICUBIC); B = rr.resize(size, Image.LANCZOS)

    def edges(im):
        g = np.asarray(im.convert('L').filter(ImageFilter.GaussianBlur(2)), float)
        gx = np.abs(np.diff(g, axis=1, prepend=g[:, :1])); gy = np.abs(np.diff(g, axis=0, prepend=g[:1]))
        e = np.hypot(gx, gy); return e / (np.percentile(e, 99) + 1e-6)
    ea, eb = edges(A), edges(B); base = np.asarray(A.convert('L'), float) * 0.5
    ov = np.stack([base + 255 * np.clip(ea, 0, 1) * 0.8, base + 200 * np.clip(eb, 0, 1), base + 255 * np.clip(eb, 0, 1)], -1)
    o = Image.new('RGB', (size[0] * 3, H)); o.paste(A, (0, 0)); o.paste(B, (size[0], 0))
    o.paste(Image.fromarray(np.clip(ov, 0, 255).astype(np.uint8)), (2 * size[0], 0))
    o.save(os.path.join(od, 'hz.png'))
    o2 = Image.new('RGB', (size[0] * 2, H)); o2.paste(A, (0, 0)); o2.paste(B, (size[0], 0)); o2.save(os.path.join(od, 'hz2.png'))
ims = [Image.open(os.path.join(od, f'h_{v}.png')) for v in vs if v != 'refzoom']
if ims:
    o = Image.new('RGB', (sum(i.width for i in ims), ims[0].height)); x = 0
    for i in ims:
        o.paste(i, (x, 0)); x += i.width
    o.save(os.path.join(od, 'hv.png'))
print('done %.0fs' % (time.time() - t), od)
