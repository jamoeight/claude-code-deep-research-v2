"""Connected components of the figure-only mesh (bbox of each small one)."""
import sys, numpy as np, model, figure
from sdf import Field
import scipy.sparse as sp
from scipy.sparse.csgraph import connected_components
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
F = figure.component(Field(model.LO, model.HI, h).blank())
v, f = F.mesh()
n = len(v); e = np.concatenate([f[:, [0, 1]], f[:, [1, 2]], f[:, [2, 0]]])
A = sp.coo_matrix((np.ones(len(e), np.int8), (e[:, 0], e[:, 1])), shape=(n, n))
nc, lab = connected_components(A, directed=False)
c = np.bincount(lab); big = np.argmax(c)
print('components', nc)
for i in range(nc):
    if i != big:
        P = v[lab == i]; print(c[i], P.min(0).round(1), P.max(0).round(1))
