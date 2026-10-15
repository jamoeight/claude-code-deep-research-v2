"""Fold check (wings agent tool): where does the offset map P + t*n of a wing sheet degenerate within the relief
thickness?  python3 wings_fold.py right|left  -> prints (u,v) cells where det(J(t)) < 0.35 for some t in [-Hb, Hf]."""
import sys
import numpy as np
import wings


class _F:
    h = 0.45


side = sys.argv[1]
S, rel = (wings.build_right if side == 'right' else wings.build_left)(_F())
Hf = rel.final['f'][0]; Hb = rel.final['b'][0]
U = np.arange(rel.u0 + 1, rel.u0 + rel.nu * rel.hr - 1, 1.0)
V = np.arange(rel.v0 + 1, rel.v0 + rel.nv * rel.hr - 1, 1.0)
uu, vv = np.meshgrid(U, V, indexing='ij')
e = 0.25
def nrm(u, v):
    return S.normal(u, v)
P = S.P(uu, vv)
Pu = (S.P(uu + e, vv) - S.P(uu - e, vv)) / (2 * e); Pv = (S.P(uu, vv + e) - S.P(uu, vv - e)) / (2 * e)
n = nrm(uu, vv)
nu = (nrm(uu + e, vv) - nrm(uu - e, vv)) / (2 * e); nv = (nrm(uu, vv + e) - nrm(uu, vv - e)) / (2 * e)
i = ((uu - rel.u0) / rel.hr).astype(int); j = ((vv - rel.v0) / rel.hr).astype(int)
hf = Hf[i, j]; hb = Hb[i, j]
cov = rel.C[i, j] < 0
d0 = np.linalg.det(np.stack([Pu, Pv, n], -1))
worst = np.full(uu.shape, 9.0)
for t in np.linspace(-1, 1, 21):
    tt = np.where(t > 0, t * hf, -t * hb) * (np.sign(t) if t != 0 else 0)
    tt = np.where(t >= 0, t * np.maximum(hf, 0), t * np.maximum(hb, 0))
    J = np.stack([Pu + tt[..., None] * nu, Pv + tt[..., None] * nv, n], -1)
    worst = np.minimum(worst, np.linalg.det(J) / d0)
bad = cov & (worst < 0.35)
print('bad cells', int(bad.sum()))
for a, b in np.argwhere(bad)[::max(1, int(bad.sum() // 60))] if len(sys.argv) < 3 else []:
    print('  u %.0f v %.0f  det %.2f  hf %.1f hb %.1f' % (uu[a, b], vv[a, b], worst[a, b], hf[a, b], hb[a, b]), np.round(P[a, b], 1))
# coarse map of bad regions (u bins of 6, v bins of 6)
from collections import Counter
cnt = Counter()
for a, b in np.argwhere(bad):
    cnt[(int(uu[a, b] // 6) * 6, int(vv[a, b] // 6) * 6)] += 1
for k in sorted(cnt):
    print('  region u %3d-%3d v %3d-%3d : %d  min det %.2f' % (k[0], k[0] + 6, k[1], k[1] + 6, cnt[k],
          worst[(uu >= k[0]) & (uu < k[0] + 6) & (vv >= k[1]) & (vv < k[1] + 6) & cov].min()))
if len(sys.argv) > 3:
    u0, u1, v0, v1 = [float(x) for x in sys.argv[3].split(',')]
    print('det map (rows v desc, cols u)')
    for b in range(len(V) - 1, -1, -1):
        if not (v0 <= V[b] <= v1):
            continue
        row = ''
        for a in range(len(U)):
            if not (u0 <= U[a] <= u1):
                continue
            row += ('%d' % min(int(worst[a, b] * 10), 9)) if cov[a, b] else '.'
        print('%5.0f %s' % (V[b], row))
