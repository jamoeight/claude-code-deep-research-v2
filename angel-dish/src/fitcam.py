import json, numpy as np
from scipy.optimize import least_squares
import cam
# (pixel in reference, design 3D point)
LM = [
 ((442,125), (-13,20,96)),   # head crown
 ((468,254), (-9,15,80)),    # chin
 ((270,58), (-45,29,108)),   # left wing peak
 ((620,52), (6,30,111)),     # right wing peak
 ((1110,560), (82,4,32)),    # right wing tip
 ((560,1065), (0,-56,0)),    # front wall bottom centre
 ((15,520), (-80,-5,55)),    # left wall outer
 ((880,960), (35,-55,13)),   # scroll centre
 ((1172,700), (82,-12,25)),  # right rim outer
 ((365,300), (-31,23,68)),   # her right shoulder
]
px = np.array([a for a,b in LM],float); P = np.array([b for a,b in LM],float)
base = cam.load()
def mk(x):
    c = dict(base); c.update(az=x[0], el=x[1], dist=x[2], lens=x[3], target=[x[4],x[5],x[6]]); return c
def res(x):
    return (cam.project(P, mk(x)) - px).ravel()
x0 = [0,30,300,50,0,0,45]
r = least_squares(res, x0, bounds=([-30,10,150,25,-40,-40,0],[30,60,800,120,40,40,90]))
c = mk(r.x); print({k:(round(v,2) if isinstance(v,float) else v) for k,v in c.items()})
err = cam.project(P,c)-px
for (a,b),e in zip(LM,err): print(a, b, np.round(e,1))
print('rms', np.sqrt((err**2).mean()))
c['target']=[round(t,2) for t in c['target']]
for k in ('az','el','dist','lens'): c[k]=round(float(c[k]),2)
json.dump(c, open('camera.json','w'))
