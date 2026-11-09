# Two-circle intersection: Xuanzang's "old Tukhara" = 400 li from Ni-jang and 600 li from Che-mo-t'o-na
import numpy as np
from pyproj import Geod
g=Geod(ellps="WGS84")
Nij=(37.067,82.767)   # Niya county seat (Minfeng) as Ni-jang
Qie=(38.1338,85.5333) # Qiemo as Che-mo-t'o-na
End=(37.783,83.817)   # Endere (Wikidata)
def best(mli):
    r1=400*mli/1000; r2=600*mli/1000
    lats=np.arange(36.8,38.8,0.005); lons=np.arange(82.6,85.6,0.005)
    LA,LO=np.meshgrid(lats,lons,indexing='ij')
    _,_,d1=g.inv(np.full(LA.shape,Nij[1]),np.full(LA.shape,Nij[0]),LO,LA)
    _,_,d2=g.inv(np.full(LA.shape,Qie[1]),np.full(LA.shape,Qie[0]),LO,LA)
    mis=np.abs(d1/1000-r1)+np.abs(d2/1000-r2)
    # report the two local minima (north and south of the Nij-Qie line)
    out=[]
    for sel in [LA>=37.6, LA<37.6]:
        m=np.where(sel,mis,np.inf); i=np.unravel_index(np.argmin(m),m.shape)
        out.append((round(LA[i],3),round(LO[i],3),round(float(mis[i]),1)))
    return r1,r2,out
for mli in [260,279,300,320,350]:
    r1,r2,out=best(mli)
    print(f"{mli} m/li: r(Ni-jang)={r1:.0f} km r(Che-mo)={r2:.0f} km -> intersections {out}")
    for la,lo,_ in out:
        az,_,d=g.inv(End[1],End[0],lo,la); print(f"      offset from Endere fort: {d/1000:.1f} km az {az%360:.0f}")
