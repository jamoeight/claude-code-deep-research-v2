import sys, numpy as np
sys.path.insert(0,'.')
import geo
b=(-72.32,19.62,-71.95,19.86)
w=geo.worldcover(b)
np.save('haiti_wc.npy',w)
W,S,E,N=b
k=40 # 400 m cells (approx 0.0033 deg)
ny,nx=w.shape[0]//k,w.shape[1]//k
water=(w==80)|(w==0)
f=water[:ny*k,:nx*k].reshape(ny,k,nx,k).mean((1,3))
built=(w==50)[:ny*k,:nx*k].reshape(ny,k,nx,k).mean((1,3))
mang=(w==95)[:ny*k,:nx*k].reshape(ny,k,nx,k).mean((1,3))
step=k/12000
print('rows lat from %.3f step %.4f; cols lon from %.3f step %.4f'%(N,step,W,step))
for i in range(ny):
    s=''
    for j in range(nx):
        if f[i,j]>0.5: s+='~'
        elif mang[i,j]>0.3: s+='m'
        elif built[i,j]>0.3: s+='B'
        else: s+='.'
    print('%7.4f '%(N-(i+0.5)*step)+s)
print('        '+''.join('|' if abs(((W+(j+0.5)*step)*100)%5)<step*100 else ' ' for j in range(nx)))
for j in range(0,nx,15): print('col',j,'lon %.4f'%(W+(j+0.5)*step))
