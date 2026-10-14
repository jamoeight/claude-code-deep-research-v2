"""Probe helpers on cached grids (wings agent tool)."""
import sys, glob, os
import numpy as np
import model
HERE = os.path.dirname(os.path.abspath(__file__))


def load(h=0.5):
    p = sorted(glob.glob(os.path.join(HERE, 'out', '_cache', 'others_*.npy')), key=os.path.getmtime)[-1]
    G = np.load(p)
    return G, np.array(model.LO, float), h


def idx(P, lo, h):
    return np.round((np.asarray(P) - lo) / h).astype(int)


if __name__ == '__main__':
    G, lo, h = load()
    xs = lo[0] + np.arange(G.shape[0]) * h; ys = lo[1] + np.arange(G.shape[1]) * h; zs = lo[2] + np.arange(G.shape[2]) * h
    print('figure back: max y inside for x,z')
    for z in (55, 60, 65, 70, 75):
        row = []
        for x in (-30, -26, -22, -18, -14, -10, -7, -4):
            i, k = idx([x, 0, z], lo, h)[[0, 2]]
            col = G[i, :, k]
            ins = np.flatnonzero(col < 0)
            ins = ins[ys[ins] > 5]
            row.append(f'{ys[ins].max():5.1f}' if len(ins) else '  -  ')
        print(z, ' '.join(row))
    print('top surface z (max z inside) along back, at x (cols) for y rows')
    for y in (20, 25, 30, 35, 40, 45, 50):
        row = []
        for x in (-45, -35, -25, -15, -5, 0, 5, 10, 15, 25, 35, 45, 55, 65, 75):
            i, j = idx([x, y, 0], lo, h)[[0, 1]]
            col = G[i, j, :]
            ins = np.flatnonzero(col < 0)
            ins = ins[zs[ins] < 45]
            row.append(f'{zs[ins].max():4.0f}' if len(ins) else '   -')
        print(y, ' '.join(row))
    print('right side top z, x cols, y rows')
    for y in (15, 10, 5, 0, -5, -10, -15):
        row = []
        for x in (60, 65, 70, 75, 80, 85, 88, 92):
            i, j = idx([x, y, 0], lo, h)[[0, 1]]
            ins = np.flatnonzero(G[i, j, :] < 0)
            row.append(f'{zs[ins].max():4.0f}' if len(ins) else '   -')
        print(y, ' '.join(row))
