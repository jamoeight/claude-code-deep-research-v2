"""Connected components of a PLY mesh (wings agent tool).  python3 wings_cc.py mesh.ply"""
import sys
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
d = open(sys.argv[1], 'rb').read()
hdr = d[:d.index(b'end_header\n') + 11].decode()
nv = int(hdr.split('element vertex ')[1].split()[0]); nf = int(hdr.split('element face ')[1].split()[0])
off = len(hdr)
v = np.frombuffer(d, np.float32, nv * 3, off).reshape(-1, 3)
rec = np.frombuffer(d, dtype=[('n', 'u1'), ('i', '<i4', (3,))], count=nf, offset=off + nv * 12)
f = rec['i']
e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]]])
A = coo_matrix((np.ones(len(e)), (e[:, 0], e[:, 1])), shape=(nv, nv))
n, lab = connected_components(A, directed=False)
cnt = np.bincount(lab)
order = np.argsort(-cnt)
print('components', n)
for k in order[:12]:
    P = v[lab == k]
    print(cnt[k], np.round(P.mean(0), 1), np.round(P.min(0), 1), np.round(P.max(0), 1))
