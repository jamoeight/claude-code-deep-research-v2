import csv, json, math, sys, re
eid_csv, astro_geo, afr_geo, outdir = sys.argv[1:5]
def hav(a,b,c,d):
    a,b,c,d=map(math.radians,(a,b,c,d))
    return 2*6371*math.asin(math.sqrt(math.sin((c-a)/2)**2+math.cos(a)*math.cos(c)*math.sin((d-b)/2)**2))
rows=[]; prov=[]
def add(name,lat,lon,dkm,status,source,note=''):
    rows.append(dict(name=name,lat=round(float(lat),5),lon=round(float(lon),5),diameter_km=('' if dkm in (None,'') else round(float(dkm),3)),status=status))
    prov.append(dict(name=name,status=status,source=source,note=note))
# 1. EID (PASSC) scrape via cjwinchester/earth-impact-data
EIDURL='https://raw.githubusercontent.com/cjwinchester/earth-impact-data/main/earth-impact-craters.csv'
for r in csv.DictReader(open(eid_csv)):
    add(r['crater_name'],r['latitude'],r['longitude'],r['diameter_km'],'confirmed',EIDURL,'Earth Impact Database (PASSC, UNB) scrape; page '+r['url'])
conf=[(r['name'],r['lat'],r['lon']) for r in rows]
def near_confirmed(lat,lon,km=15):
    return any(hav(lat,lon,a,b)<km for _,a,b in conf)
ASTRO='https://github.com/nobulart/astrobleme (catalog_repair/astroblemes_repaired.geojson, repair v2026-06-21)'
fixes={'Tsenkher':(43.645,98.369)}  # wiki-confirmed record carries a coordinate ~500 km off; use the possible-list coordinate
astro=json.load(open(astro_geo))['features']
skip_names={'Shoemaker','New Quebec/Pingualuit','Nördlinger Ries','Meteor/Barringer','Tunnunik','Rochechouart impact structure'}
for f in astro:
    p=f['properties']
    if not p['analytical_include'] and p['name'] not in ('Pantasma',): continue
    if p['duplicate_of_record_id']: continue
    lat,lon=p['center_lat'],p['center_lon']
    if p['name'] in fixes: lat,lon=fixes[p['name']]
    if p['source'].startswith('Wikipedia confirmed'):
        if p['earth_impact_database_match'] or p['name'] in skip_names or near_confirmed(lat,lon): continue
        add(p['name'],lat,lon,p['diameter_km'],'confirmed_post_eid',ASTRO+' <- '+p['source_url'],'Wikipedia confirmed list; not in 2018-era EID scrape')
        conf.append((p['name'],lat,lon)); continue
    if p['source'].startswith('Wikipedia possible'):
        if near_confirmed(lat,lon,10): continue
        st='proposed'
        if p['earth_impact_database_match'] and p['name'] in ('Pantasma','Decorah','Ramgarh','Cerro do Jarau','Yallalie'):
            st='confirmed_post_eid'
        nm=p['name'] if p['name']!='38th Parallel structures' else f"38th Parallel structure ({lat:.1f},{lon:.1f})"
        add(nm,lat,lon,p['diameter_km'],st,ASTRO+' <- '+p['source_url'],('coord '+p['coordinate_audit_status'])+('; listed on Wikipedia possible list but flagged EID-match in astrobleme' if st!='proposed' else ''))
        if st!='proposed': conf.append((nm,lat,lon))
        continue
# 2. Reimold & Koeberl 2014 Africa (proposed + discarded), from astrobleme african_impact_structures.geojson
afr=json.load(open(afr_geo))['features']
RK='Reimold & Koeberl 2014, J. Afr. Earth Sci. 93, Tables 2a-2c, via https://github.com/nobulart/astrobleme (african_impact_structures.geojson)'
for f in afr:
    p=f['properties']
    if p['geometry_role']!='center': continue
    lon,lat=f['geometry']['coordinates']
    d=p.get('diameter_max_km') or p.get('diameter_min_km')
    if p['status']=='confirmed':
        if near_confirmed(lat,lon,15) or p['name']=='Ouarkziz': continue  # Ouarkziz: sign error in source file, already in EID
        if p['name']=='Agoudal' and not d: d=1.0
        add(p['name'],lat,lon,d,'confirmed_post_eid',RK,'R&K 2014 Table 2a confirmed; missing from EID scrape'); conf.append((p['name'],lat,lon)); continue
    if any(hav(lat,lon,r['lat'],r['lon'])<5 and r['status']!='confirmed' for r in rows): continue
    st={'proposed_unconfirmed':'proposed','discarded':'discarded'}[p['status']]
    if p['name']=='Kebira':
        lat,lon=24.667,24.967  # R&K record reuses Oasis coordinates; use the El-Baz & Ghoneim centre as listed on Wikipedia possible list
        if any(r['name']=='Kebira' for r in rows): 
            for i,r in enumerate(rows):
                if r['name']=='Kebira': rows[i]['status']='discarded'; prov[i]['note']+='; R&K 2014 Table 2c lists as discarded'
            continue
    add(p['name'],lat,lon,d,st,RK,'R&K 2014 Table '+p['table'])
# 3. Additions from T4 literature review
add('Bolaven (buried, proposed Australasian tektite source)',15.2033,106.2708,15,'proposed',
    'Sieh et al. 2020 PNAS doi:10.1073/pnas.1904368116; centre from inversion of Dataset S1 distances in github.com/yicolas/2024_Laos_Australasian_Impactor Fig1 gpkg',
    'buried under lava; 17x13 km gravity outline; NOT visible in DEM')
add('Badain Jaran megadune-lake area (buried, proposed AAT source)',39.75,102.4,'','proposed',
    'Karimi et al. 2023 Sci. Rep. doi:10.1038/s41598-023-40177-7 (verbal location only: SE Badain Jaran megadune-lake area)',
    'coordinates APPROXIMATE (+-50 km), derived by T4 from verbal description; diameter not retrieved')
for i,r in enumerate(rows):
    if r['name']=='Tsenkher':
        rows[i]['status']='confirmed_post_eid'; prov[i]['note']+='; also on Wikipedia confirmed list (record there carries a wrong coordinate 47.44N 101.77E)'
seen=set(); out=[]; pv=[]
for r,p in zip(rows,prov):
    k=(r['name'],r['lat'],r['lon'])
    if k in seen: continue
    seen.add(k); out.append(r); pv.append(p)
with open(outdir+'/known_impact_structures.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['name','lat','lon','diameter_km','status']); w.writeheader(); w.writerows(out)
with open(outdir+'/known_impact_structures_provenance.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['name','status','source','note']); w.writeheader(); w.writerows(pv)
from collections import Counter
print(Counter(r['status'] for r in out), len(out))
