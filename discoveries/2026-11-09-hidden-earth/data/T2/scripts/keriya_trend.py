# Keriya delta settlement-migration extrapolation and misc geodesy
from pyproj import Geod
g=Geod(ellps="WGS84")
Y=(38.867,81.583); K=(38.533,81.867); M=(38.603,82.097)  # Yuansha, Karadong, modern Keriya terminus
az,baz,d=g.inv(Y[1],Y[0],K[1],K[0]); print(f"Yuansha->Karadong az {az%360:.1f} dist {d/1000:.1f} km")
for f in [0.5,1.0]:
    lo,la,_=g.fwd(K[1],K[0],az,d*f); print(f"  forward x{f}: {la:.3f},{lo:.3f}")
    lo,la,_=g.fwd(Y[1],Y[0],baz,d*f); print(f"  backward x{f} (NW of Yuansha): {la:.3f},{lo:.3f}")
# Ho-lao-lo-kia corridor centre vs Pi-mo and Dandan Oilik
U=(37.28,80.95); D=(37.7744,81.0731); H=(37.0997,79.9269)
for name,p in [("HLLK centre",(37.55,80.72))]:
    a,_,dd=g.inv(p[1],p[0],U[1],U[0]); print(f"{name} -> Uzun-tati az {a%360:.0f} {dd/1000:.0f} km")
    a,_,dd=g.inv(p[1],p[0],D[1],D[0]); print(f"{name} -> Dandan Oilik az {a%360:.0f} {dd/1000:.0f} km")
    a,_,dd=g.inv(H[1],H[0],p[1],p[0]); print(f"Hotan -> {name} az {a%360:.0f} {dd/1000:.0f} km")
# Song Yun proportional check (figures quoted from memory: Zuomo->Mo 1275 li, Mo->Hanmo 22 li, Hanmo->Khotan 878 li)
Q=(38.1338,85.5333)
a,_,dqh=g.inv(Q[1],Q[0],H[1],H[0]); tot=1275+22+878
print(f"Qiemo->Hotan {dqh/1000:.0f} km over {tot} li = {dqh/tot:.0f} m/li; Hanmo at {878/tot:.3f} of the way from Khotan = {dqh*878/tot/1000:.0f} km")
_,_,dhu=g.inv(H[1],H[0],U[1],U[0]); print(f"Hotan->Uzun-tati {dhu/1000:.0f} km = {dhu/878:.0f} m/li if Hanmo=Uzun-tati")
