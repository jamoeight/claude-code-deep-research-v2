"""Ref-camera pixel -> 3D point on the (cached) figure field.
python3 figure_refpick.py [--rebuild] [--h 0.45] [--base] u,v [u,v ...]
--base: field without relief/folds (FIG_NOFOLDS)."""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
a = sys.argv[1:]
h = float(a[a.index('--h') + 1]) if '--h' in a else 0.45
base = '--base' in a
fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', '_figcache', 'figself_%s_%.3f.npy' % ('base' if base else 'full', h))
import model, figure_tex as T
from sdf import Field
F = Field(model.LO, model.HI, h)
if '--rebuild' in a or not os.path.exists(fn):
    if base:
        os.environ['FIG_NOFOLDS'] = '1'
    import figure
    G = figure.component(F.blank()).G
    np.save(fn, G)
else:
    G = np.load(fn)
rc = T.ref_camera()
CT = T.CamTex(rc, (0, 0, 1179, 1078), 1.0, G, np.array(F.lo, float), h, full=False)
pts = [x for x in a if ',' in x]
for s in pts:
    u, v = map(float, s.split(','))
    p = CT.cast([(u, v)])[0]
    n = CT.normals(np.atleast_2d(p))[0] if not np.isnan(p[0]) else None
    print(s, np.round(p, 1), 'n', None if n is None else np.round(n, 2))
