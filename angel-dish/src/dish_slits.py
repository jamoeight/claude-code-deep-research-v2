"""Knife-slit / thin-skin scan of the dish alone: morphological closing (r) adds material in slits narrower than
~2r; report the biggest added clusters.   python3 dish_slits.py [h] [r]"""
import sys, numpy as np
from scipy import ndimage as ndi
import model
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.3
r = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
F = model.build(h, ['dish'], verbose=False)
m = F.G < 0
rv = r / h
dil = ndi.distance_transform_edt(~m) <= rv
clo = ndi.distance_transform_edt(dil) > rv
add = clo & ~m
lab, n = ndi.label(add)
sizes = ndi.sum(add, lab, range(1, n + 1))
o = np.argsort(sizes)[::-1]
print('closing r=%.2f added %.1f mm^3 in %d clusters' % (r, add.sum() * h ** 3, n))
for i in o[:15]:
    c = np.array(ndi.center_of_mass(add, lab, i + 1)) * h + F.lo
    print('  %.2f mm^3 at (%.1f, %.1f, %.1f)' % (sizes[i] * h ** 3, *c))
# thin skins near the floor: solid voxels at z<0.6 with empty directly above at z~1
k0 = int(round((0.3 - F.lo[2]) / h)); k1 = int(round((1.2 - F.lo[2]) / h))
skin = m[:, :, k0] & ~m[:, :, k1]
print('floor skin area %.1f mm^2' % (skin.sum() * h * h))
