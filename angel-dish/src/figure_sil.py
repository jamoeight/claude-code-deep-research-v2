"""Quick silhouette + numpy shading of the figure alone from the reference camera, overlaid on the photo.
python3 figure_sil.py out.png [--h 0.6] [--box x0,y0,x1,y1] [--scale 2]"""
import sys, os
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model, cam, figure
from sdf import Field

a = sys.argv[1:]
out = a[0]
h = float(a[a.index('--h') + 1]) if '--h' in a else 0.6
box = tuple(int(v) for v in a[a.index('--box') + 1].split(',')) if '--box' in a else (280, 220, 700, 740)
sc = float(a[a.index('--scale') + 1]) if '--scale' in a else 2.0
F = figure.component(Field(model.LO, model.HI, h).blank())
v, f = F.mesh()
W, H = 1179, 1078
uv = cam.project(v)
loc, fwd, right, up = cam.frame()
dep = (v - loc) @ fwd
# vertex normals
fn = np.cross(v[f[:, 1]] - v[f[:, 0]], v[f[:, 2]] - v[f[:, 0]])
vn = np.zeros_like(v)
for i in range(3):
    np.add.at(vn, f[:, i], fn)
vn /= np.linalg.norm(vn, axis=1, keepdims=True) + 1e-9
L = np.array([-0.5, -0.6, 0.62]); L /= np.linalg.norm(L)
shade = 0.25 + 0.75 * np.clip(vn @ L, 0, 1)
# z-buffer splat of barycentric samples of every triangle
S = 1
bary = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1], [.5, .5, 0], [0, .5, .5], [.5, 0, .5], [1/3, 1/3, 1/3], [.66, .17, .17], [.17, .66, .17], [.17, .17, .66]])
uvf = uv[f]; df = dep[f]; sf = shade[f]
SU = np.einsum('bk,fkc->fbc', bary, uvf).reshape(-1, 2); SD = (df @ bary.T).reshape(-1); SS = (sf @ bary.T).reshape(-1)
ui = np.round(SU[:, 0]).astype(int); vi = np.round(SU[:, 1]).astype(int)
img = np.zeros((H, W)); zb = np.full((H, W), np.inf)
PX = []; PY = []; PD = []; PS = []
for dx in (0, 1):
    for dy in (0, 1):
        PX.append(np.clip(ui + dx, 0, W - 1)); PY.append(np.clip(vi + dy, 0, H - 1)); PD.append(SD); PS.append(SS)
PX = np.concatenate(PX); PY = np.concatenate(PY); PD = np.concatenate(PD); PS = np.concatenate(PS)
order = np.argsort(-PD)
img[PY[order], PX[order]] = PS[order]; zb[PY[order], PX[order]] = PD[order]
mask = np.isfinite(zb)
mask = ndimage.binary_closing(mask, iterations=1)
img = Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8))
mask = Image.fromarray(mask.astype(np.uint8) * 255)
mk = np.asarray(mask) > 0
edge = mk ^ ndimage.binary_erosion(mk, iterations=1)
ref = np.asarray(Image.open(os.path.join(HERE, '..', 'ref', 'reference.png')).convert('RGB')).copy()
ov = ref.copy(); ov[edge] = (0, 255, 0)
sh = np.asarray(img.convert('RGB')).copy(); sh[~mk] = (60, 60, 60)
x0, y0, x1, y1 = box
A = Image.fromarray(ov).crop(box); Bm = Image.fromarray(sh).crop(box)
A = A.resize((int(A.width * sc), int(A.height * sc)), Image.LANCZOS); Bm = Bm.resize(A.size, Image.LANCZOS)
o = Image.new('RGB', (A.width * 2, A.height)); o.paste(A, (0, 0)); o.paste(Bm, (A.width, 0))
d = ImageDraw.Draw(o)
for x in range((x0 // 50 + 1) * 50, x1, 50):
    X = (x - x0) * sc
    for off in (0, A.width):
        d.line((X + off, 0, X + off, 8), fill=(255, 255, 0)); d.text((X + off + 2, 8), str(x), fill=(255, 255, 0))
for y in range((y0 // 50 + 1) * 50, y1, 50):
    Y = (y - y0) * sc
    for off in (0, A.width):
        d.line((off, Y, off + 8, Y), fill=(255, 255, 0)); d.text((off + 10, Y - 5), str(y), fill=(255, 255, 0))
o.save(out)
print('saved', out, 'faces', len(f))
