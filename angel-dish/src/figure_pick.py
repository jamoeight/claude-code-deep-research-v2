"""Map pixels of a figure_render CLOSE/ORB view to 3D surface points (figure alone) and to ref-camera pixels.
python3 figure_pick.py view res h u,v [u,v ...]"""
import sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import model, figure, figure_tex as T
from sdf import Field
ORB = {'fFront': (0, 12), 'fBack': (180, 18), 'fLeft': (-90, 12), 'fRight': (90, 14), 'fTQL': (-40, 20), 'fTQR': (40, 20),
       'fBackL': (-140, 20), 'fBackR': (140, 20), 'fTop': (0, 70), 'fLow': (10, 3)}
CLOSE = {'cHand': ((-35.0, 21.0, 36.0), -30, 15, 80, 60), 'cBust': ((-17.0, 18.0, 62.0), 15, 10, 90, 60),
         'cBack': ((-20.0, 30.0, 52.0), 180, 15, 110, 60), 'cKnee': ((0.0, 8.0, 28.0), 35, 15, 110, 60),
         'cSide': ((-18.0, 22.0, 45.0), 90, 10, 150, 60), 'cHem': ((-18.0, 4.0, 16.0), -15, 22, 120, 60), 'cBackSk': ((-14.0, 36.0, 22.0), 180, 18, 110, 60), 'cRightSk': ((0.0, 20.0, 30.0), 75, 12, 110, 60), 'cScroll': ((6.0, 4.0, 16.0), 5, 25, 75, 60), 'cPocket': ((-18.0, 6.0, 22.0), 5, 22, 70, 60),
         'cHemR': ((5.0, 8.0, 16.0), 40, 22, 120, 60), 'cHemL': ((-35.0, 12.0, 18.0), -70, 22, 120, 60)}
view, res, h = sys.argv[1], int(sys.argv[2]), float(sys.argv[3])
if view in CLOSE:
    tgt, az, el, d, lens = CLOSE[view]; W = H = res
else:
    az, el = ORB[view]; tgt = (-14.0, 18.0, 50.0); d = 175.0; lens = 75; W = int(res * 0.8); H = res
c = T.orbit_camera(tgt, az, el, d, lens=lens, W=W, H=H)
F = figure.component(Field(model.LO, model.HI, h).blank())
CT = T.CamTex(c, (0, 0, W, H), 1.0, F.G, np.array(F.lo, float), h, full=False)
rc = T.ref_camera()
for a in sys.argv[4:]:
    u, v = map(float, a.split(','))
    p = CT.cast([(u, v)])[0]
    print(a, np.round(p, 1), 'ref px', None if np.isnan(p[0]) else T.project(rc, p)[0].round(0))
