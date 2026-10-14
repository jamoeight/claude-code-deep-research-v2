"""Fast 2D check of a wing relief (wings agent tool): shaded height maps of both faces in the (u,v) chart.
   python3 wings_hmap.py right|left OUT.png [h=0.45] [--box u0,v0,u1,v1] [--scale 4]
Image: front face (as seen from the front; left wing mirrored so it reads like the photo) | back face."""
import sys, time
import numpy as np
from PIL import Image
import wings

side = sys.argv[1]; out = sys.argv[2]
h = float(sys.argv[3]) if len(sys.argv) > 3 and not sys.argv[3].startswith('--') else 0.45
a = sys.argv
box = [float(t) for t in a[a.index('--box') + 1].split(',')] if '--box' in a else None
scale = float(a[a.index('--scale') + 1]) if '--scale' in a else 4.0


class _F:
    pass


F = _F(); F.h = h
t0 = time.time()
S, rel = (wings.build_right if side == 'right' else wings.build_left)(F)
print('built %.1fs' % (time.time() - t0))
hr = rel.hr


def shade(H, light):
    gu, gv = np.gradient(H, hr)
    n = np.stack([-gu, -gv, np.ones_like(H)], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    L = np.asarray(light, float); L /= np.linalg.norm(L)
    d = np.clip(n @ L, 0, 1)
    # cheap ambient occlusion: darker where lower than the local mean
    from scipy.ndimage import gaussian_filter
    ao = np.clip(1 + 0.35 * (H - gaussian_filter(H, 1.5 / hr)), 0.55, 1.15)
    return np.clip((0.18 + 0.82 * d) * ao, 0, 1)


imgs = []
for fc in ('f', 'b'):
    H = rel.final[fc][0].astype(np.float64)
    cov = H > -0.05
    if box:
        i0 = int((box[0] - rel.u0) / hr); i1 = int((box[2] - rel.u0) / hr)
        j0 = int((box[1] - rel.v0) / hr); j1 = int((box[3] - rel.v0) / hr)
        H = H[i0:i1, j0:j1]; cov = cov[i0:i1, j0:j1]
    # light from upper right (as the photo key) in image space
    flip = (side == 'left') == (fc == 'f')
    lu = -0.5 if flip else 0.5
    I = shade(H, (lu, 0.75, 0.6))
    I = np.where(cov, I, 0.15)
    I = I.T[::-1]                 # rows = -v, cols = u
    if flip:
        I = I[:, ::-1]
    im = Image.fromarray((I * 255).astype(np.uint8))
    s = scale * hr
    im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    imgs.append(im)
W = sum(i.width for i in imgs) + 10; Hh = max(i.height for i in imgs)
o = Image.new('L', (W, Hh), 40)
x = 0
for i in imgs:
    o.paste(i, (x, 0)); x += i.width + 10
o.save(out)
print('saved', out, o.size)
