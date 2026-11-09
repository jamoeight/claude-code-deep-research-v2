import csv, numpy as np, sys
f=sys.argv[1]
R=6371.0
rows=[r for r in csv.DictReader(open(f)) if r['mt_per_cm2_gt125um'] not in ('',None)]
lat=np.radians([float(r['lat']) for r in rows]); lon=np.radians([float(r['lon']) for r in rows])
C=np.array([float(r['mt_per_cm2_gt125um']) for r in rows]); y=np.log10(C)
print('n cores',len(C))
def dist_az(la0,lo0):
    la0,lo0=np.radians(la0),np.radians(lo0)
    d=2*R*np.arcsin(np.sqrt(np.sin((lat-la0)/2)**2+np.cos(la0)*np.cos(lat)*np.sin((lon-lo0)/2)**2))
    az=np.arctan2(np.sin(lon-lo0)*np.cos(lat), np.cos(la0)*np.sin(lat)-np.sin(la0)*np.cos(lat)*np.cos(lon-lo0))
    return d,az
def r2(X,y):
    X=np.column_stack([np.ones(len(y))]+X); b,res,rk,sv=np.linalg.lstsq(X,y,rcond=None)
    yh=X@b; return 1-np.sum((y-yh)**2)/np.sum((y-y.mean())**2), b
lats=np.arange(-5,35.01,0.25); lons=np.arange(90,130.01,0.25)
def grid(idx=None):
    best={}
    res={k:np.zeros((len(lats),len(lons))) for k in ['lin','log','lin_az','log_az']}
    yy=y if idx is None else y[idx]
    for i,a in enumerate(lats):
        for j,o in enumerate(lons):
            d,az=dist_az(a,o)
            if idx is not None: d,az=d[idx],az[idx]
            ld=np.log10(np.maximum(d,50))
            res['lin'][i,j]=r2([d],yy)[0]
            res['log'][i,j]=r2([ld],yy)[0]
            res['lin_az'][i,j]=r2([d,np.cos(az),np.sin(az)],yy)[0]
            res['log_az'][i,j]=r2([ld,np.cos(az),np.sin(az)],yy)[0]
    return res
res=grid()
for k,v in res.items():
    i,j=np.unravel_index(np.argmax(v),v.shape)
    good=v>=v.max()-0.02
    gl=[lats[a] for a,b in zip(*np.where(good))]; go=[lons[b] for a,b in zip(*np.where(good))]
    print(f"{k}: best r2={v.max():.3f} at {lats[i]:.2f}N {lons[j]:.2f}E ; within 0.02 r2: lat {min(gl):.1f}-{max(gl):.1f}, lon {min(go):.1f}-{max(go):.1f}")
# r2 at named candidates
cands={'Bolaven':(15.20,106.27),'TonleSap':(12.9,104.1),'GulfTonkin/RedRiver':(19.5,107.0),'BadainJaran':(39.6,102.5),'GlassPizzuto94':(12,106),'MuongNong_village':(16.6,106.5),'Hainan':(19.2,109.7)}
for n,(a,o) in cands.items():
    d,az=dist_az(a,o); ld=np.log10(np.maximum(d,50))
    print(n, 'lin',round(r2([d],y)[0],3),'log',round(r2([ld],y)[0],3),'lin_az',round(r2([d,np.cos(az),np.sin(az)],y)[0],3), 'slope_lin',r2([d],y)[1][1]*1000,'per 1000 km')
# bootstrap
rng=np.random.default_rng(1)
bl=[]
for b in range(int(sys.argv[2]) if len(sys.argv)>2 else 0):
    idx=rng.integers(0,len(y),len(y))
    v=grid(idx)['lin']
    i,j=np.unravel_index(np.argmax(v),v.shape); bl.append((lats[i],lons[j]))
if bl:
    bl=np.array(bl); print('bootstrap lin best: median',np.median(bl,0),'5-95%',np.percentile(bl,5,0),np.percentile(bl,95,0))
