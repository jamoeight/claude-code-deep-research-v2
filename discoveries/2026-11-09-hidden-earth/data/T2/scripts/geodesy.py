# Itinerary geodesy for Xuanzang's southern-route chain (Da Tang Xiyu Ji, book 12)
from pyproj import Geod
g=Geod(ellps="WGS84")
P={ # lat, lon, source tag
 "Hotan(Khotan capital area)":(37.0997,79.9269,"NaturalEarth"),
 "Uzun-tati":(37.28,80.95,"WP list"),
 "Domoko":(37.1019,81.0781,"WP list"),
 "Dandan Oilik":(37.7744,81.0731,"WP"),
 "Keriya town":(36.85,81.667,"WP"),
 "Karadong":(38.533,81.867,"WP list"),
 "Yuansha":(38.867,81.583,"Springer/RG"),
 "Keriya mouth (modern)":(38.603,82.097,"WP Keriya River"),
 "Niya county seat (Minfeng)":(37.067,82.767,"WP Niya County"),
 "Niya ruins":(38.0,82.68,"aroundus"),
 "Endere":(37.783,83.817,"Wikidata"),
 "Qiemo":(38.1338,85.5333,"NaturalEarth"),
}
def inv(a,b):
    la1,lo1,_=P[a]; la2,lo2,_=P[b]
    az,baz,d=g.inv(lo1,la1,lo2,la2); return az%360,d/1000
print("Pairwise distances/bearings:")
for a,b in [("Hotan(Khotan capital area)","Uzun-tati"),("Uzun-tati","Niya county seat (Minfeng)"),("Uzun-tati","Keriya town"),
            ("Niya county seat (Minfeng)","Endere"),("Endere","Qiemo"),("Niya county seat (Minfeng)","Qiemo"),
            ("Yuansha","Karadong"),("Hotan(Khotan capital area)","Dandan Oilik"),("Uzun-tati","Dandan Oilik"),
            ("Hotan(Khotan capital area)","Niya county seat (Minfeng)"),("Keriya town","Karadong"),("Niya ruins","Endere"),("Niya county seat (Minfeng)","Niya ruins")]:
    az,d=inv(a,b); print(f"  {a:30s} -> {b:28s} az {az:6.1f}  {d:7.1f} km")
# Xuanzang segments (li) and hypotheses
segs=[("Hotan(Khotan capital area)","Uzun-tati",330),("Uzun-tati","Niya county seat (Minfeng)",200),
      ("Niya county seat (Minfeng)","Endere",400),("Endere","Qiemo",600)]
print("\nH1 (Stein): Pi-mo=Uzun-tati, Ni-jang=Niya oasis, Tukhara=Endere, Che-mo-t'o-na=Qiemo")
tot_d=tot_li=0
for a,b,li in segs:
    az,d=inv(a,b); tot_d+=d; tot_li+=li
    print(f"  {li:4d} li  {d:6.1f} km  => {1000*d/li:5.0f} m/li")
print(f"  overall {1000*tot_d/tot_li:.0f} m/li; excluding Pi-mo->Ni-jang: ", end="")
dd=sum(inv(a,b)[1] for a,b,li in segs if li!=200); ll=sum(li for a,b,li in segs if li!=200)
print(f"{1000*dd/ll:.0f} m/li")
