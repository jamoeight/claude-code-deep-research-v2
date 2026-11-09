import sys, numpy as np
sys.path.insert(0,'.')
import geo
from scipy import ndimage as ndi
KS=(15.765684,-7.968710)
b=geo.box(*KS,17.0); z=geo.dem(b)
W,S,E,N=b; ny,nx=z.shape
zs=ndi.uniform_filter(z,9)  # ~270 m smoothing
def at(la,lo):
    r=int((N-la)/(N-S)*ny); c=int((lo-W)/(E-W)*nx); return zs[r,c]
for azm in [300,320,340,0,20,40,90,180,250]:
    row=[]
    for km in range(0,15,1):
        la,lo=geo.fwd(*KS,azm,km); row.append('%3.0f'%at(la,lo))
    print('az%3d'%azm,' '.join(row))
