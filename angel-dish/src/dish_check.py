"""Printability check of a build: solid components, enclosed voids, downward-facing overhang area.
   python3 dish_check.py [h] [--parts dish,...]"""
import sys
import numpy as np
from scipy import ndimage
import model
h = float(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else 0.5
parts = sys.argv[sys.argv.index('--parts') + 1].split(',') if '--parts' in sys.argv else ['dish']
F = model.build(h, parts, verbose=False)
G = F.G
solid = G < 0
lab, n = ndimage.label(solid)
sizes = ndimage.sum(solid, lab, range(1, n + 1))
print('solid components:', n, 'sizes(voxels):', sorted(sizes.astype(int))[::-1][:6])
empty = ~solid
le, ne = ndimage.label(empty)
# background = components touching the grid border
border = set(np.unique(np.concatenate([le[0].ravel(), le[-1].ravel(), le[:, 0].ravel(), le[:, -1].ravel(), le[:, :, 0].ravel(), le[:, :, -1].ravel()])))
voids = [i for i in range(1, ne + 1) if i not in border]
if voids:
    vs = ndimage.sum(empty, le, voids)
    cs = ndimage.center_of_mass(empty, le, voids)
    lo = np.array(F.lo)
    print('enclosed voids:', len(voids), [(int(s), tuple(np.round(lo + h * np.array(c), 1))) for s, c in zip(vs, cs)][:8])
else:
    print('enclosed voids: 0')
# overhang: surface normals from the SDF gradient, area of faces pointing down steeper than 45/55 deg (z > 0.6)
gx, gy, gz = np.gradient(G, h)
near = (np.abs(G) < 0.5 * h) & (np.arange(G.shape[2])[None, None, :] * h + F.lo[2] > 0.8)
nz = gz[near] / (np.sqrt(gx[near] ** 2 + gy[near] ** 2 + gz[near] ** 2) + 1e-9)
# downward facing: nz < -cos(90-angle) ; overhang angle from vertical a: nz < -sin(a)
for a in (45, 55, 65):
    print('overhang >%d deg: %.0f units^2' % (a, (nz < -np.sin(np.radians(a))).sum() * h * h / 0.5 * 0.5 / 1.0))
