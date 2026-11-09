import sys, numpy as np
sys.path.insert(0,'/home/user/claude-code-deep-research-v2/discoveries/2026-11-09-hidden-earth/data/T8')
import geo
W,S,E,N,k=[float(x) for x in sys.argv[1:6]]; k=int(k)
w=geo.worldcover((W,S,E,N))
ny,nx=w.shape[0]//k,w.shape[1]//k
def frac(cls):
    return np.isin(w,cls)[:ny*k,:nx*k].reshape(ny,k,nx,k).mean((1,3))
water=frac([80,0]); mang=frac([95]); built=frac([50]); wet=frac([90]); tree=frac([10])
step=k/12000
print('rows from lat %.4f step %.4f ; cols from lon %.4f step %.4f'%(N-step/2,step,W+step/2,step))
for i in range(ny):
    s=''
    for j in range(nx):
        s+= '~' if water[i,j]>0.5 else 'm' if mang[i,j]>0.3 else 'B' if built[i,j]>0.3 else 'w' if wet[i,j]>0.3 else 'T' if tree[i,j]>0.5 else '.'
    print('%8.4f '%(N-(i+0.5)*step)+s)
for j in range(0,nx,10): print('col',j,'lon %.4f'%(W+(j+0.5)*step))
