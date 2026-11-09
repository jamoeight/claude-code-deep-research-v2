import csv, numpy as np, sys
R=6371.0
rows=[r for r in csv.DictReader(open(sys.argv[1])) if r['mt_per_cm2_gt125um']]
lat=np.radians([float(r['lat']) for r in rows]); lon=np.radians([float(r['lon']) for r in rows])
y=np.log10([float(r['mt_per_cm2_gt125um']) for r in rows])
lats=np.arange(-5,40.01,0.5); lons=np.arange(90,130.01,0.5)
LA,LO=np.meshgrid(np.radians(lats),np.radians(lons),indexing='ij')
# distances: grid x cores
D=2*R*np.arcsin(np.sqrt(np.sin((lat[None,None,:]-LA[...,None])/2)**2+np.cos(LA[...,None])*np.cos(lat[None,None,:])*np.sin((lon[None,None,:]-LO[...,None])/2)**2))
for mode in ['log','lin']:
    X=np.log10(np.maximum(D,50)) if mode=='log' else D
    def r2map(idx):
        x=X[...,idx]; yy=y[idx]
        xm=x.mean(-1,keepdims=True); ym=yy.mean()
        cov=((x-xm)*(yy-ym)).sum(-1); vx=((x-xm)**2).sum(-1); vy=((yy-ym)**2).sum()
        return cov**2/(vx*vy)
    rng=np.random.default_rng(42); best=[]
    for b in range(500):
        idx=rng.integers(0,len(y),len(y)); m=r2map(idx)
        i,j=np.unravel_index(np.argmax(m),m.shape); best.append((lats[i],lons[j]))
    best=np.array(best)
    print(mode,'bootstrap best-fit median',np.median(best,0),'2.5%',np.percentile(best,2.5,0),'97.5%',np.percentile(best,97.5,0))
    # fraction of bootstrap best fits within 150 km of candidates
    for n,(a,o) in {'Bolaven':(15.2,106.27),'TonleSap':(12.9,104.1),'GulfTonkin':(19.5,107.0),'BadainJaran':(39.6,102.5)}.items():
        dd=2*R*np.arcsin(np.sqrt(np.sin(np.radians(best[:,0]-a)/2)**2+np.cos(np.radians(a))*np.cos(np.radians(best[:,0]))*np.sin(np.radians(best[:,1]-o)/2)**2))
        print('  frac within 300 km of',n,round((dd<300).mean(),3))
