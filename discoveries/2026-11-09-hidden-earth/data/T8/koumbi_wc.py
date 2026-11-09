import sys, json, numpy as np
from scipy import ndimage as ndi
sys.path.insert(0, '.')
import geo
KS=(15.765684,-7.968710)
b=geo.box(*KS,17.0)
w=geo.worldcover(b)
lat,lon=geo.grid_latlon(b,w.shape)
kx=111.32*np.cos(np.radians(KS[0])); ky=110.57
D=np.hypot((lon-KS[1])*kx,(lat-KS[0])*ky)
az=(np.degrees(np.arctan2((lon-KS[1])*kx,(lat-KS[0])*ky))+360)%360
u,c=np.unique(w[D<=17],return_counts=True); print('classes within 17km',dict(zip(u.astype(int),np.round(c/c.sum()*100,2))))
for name,cls in [('tree',[10]),('water/wetland',[80,90]),('built',[50]),('crop',[40])]:
    m=np.isin(w,cls)
    # block fraction in 500 m cells (50x50 px)
    k=50
    ny,nx=(m.shape[0]//k)*k,(m.shape[1]//k)*k
    f=m[:ny,:nx].reshape(ny//k,k,nx//k,k).mean((1,3))
    Dk=D[:ny,:nx].reshape(ny//k,k,nx//k,k).mean((1,3))
    lk=lat[:ny,:nx].reshape(ny//k,k,nx//k,k).mean((1,3)); ok=lon[:ny,:nx].reshape(ny//k,k,nx//k,k).mean((1,3))
    azk=az[:ny,:nx].reshape(ny//k,k,nx//k,k).mean((1,3))
    print(name,'mean frac within 14km %.4f'%f[Dk<=14].mean(),' ring 8.5-12.5 %.4f'%f[(Dk>=8.5)&(Dk<=12.5)].mean())
    idx=np.argsort(f.ravel())[::-1][:8]
    for i in idx:
        r,cc=divmod(i,f.shape[1])
        if f[r,cc]>0: print('   %.3f at %.4f,%.4f d=%.1f az=%d'%(f[r,cc],lk[r,cc],ok[r,cc],Dk[r,cc],azk[r,cc]))
    if name=='tree':
        for s in range(0,360,45):
            mm=(Dk>=8.5)&(Dk<=12.5)&(azk>=s)&(azk<s+45)
            print('   ring sector',s,'tree frac %.4f'%f[mm].mean())
