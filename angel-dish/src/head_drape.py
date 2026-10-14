"""Body proxy for hair draping: builds the figure's torso + arms (if available) into a coarse field,
then provides SDF sampling, surface projection and reference-pixel ray casting."""
import math
import numpy as np
from scipy.ndimage import map_coordinates
from sdf import Field, Batch
import cam

LO = np.array([-44.0, 2.0, 44.0]); HI = np.array([4.0, 44.0, 92.0])


class Body:
    def __init__(self, h=0.5):
        self.F = Field(LO, HI, h)
        self.ok = False
        import os
        if os.environ.get('HEAD_DRAPE_FULL', '1') == '1':
            # the figure's finished surface (gown relief included), so hair lies ON the visible surface
            try:
                import figure
                G = figure.component(self.F.blank())
                if G is not None and np.isfinite(G.G).all() and (G.G < 0).sum() > 1000:
                    self.F = G
                    self.ok = True
            except Exception as e:
                print('head_drape: full figure proxy failed:', e)
        if not self.ok:
            try:
                import figure
                self.F.apply(figure.torso())
                self.F.apply(figure.arms())
                self.ok = True
            except Exception as e:  # fall back to a simple proxy
                print('head_drape: figure proxy unavailable:', e)
                B = Batch()
                B.ellipsoid((-21.0, 23.0, 62.0), (8.5, 6.4, 9.6), k=0)
                B.ellipsoid((-21.3, 23.6, 68.2), (10.0, 5.6, 4.4), xaxis=(0.88, 0.47, 0), k=3.0)
                B.rcone((-19.6, 22.0, 69.5), (-17.0, 20.2, 82.0), 3.9, 3.45, k=2.5)
                B.sphere((-29.7, 19.5, 70.0), 3.25, k=2.0)
                B.rcone((-30.0, 20.0, 68.0), (-33.8, 25.0, 50.3), 2.8, 2.05, k=1.8)
                self.F.apply(B)
        G = self.F.G
        G[G > 20] = 20.0

    def d(self, P):
        P = np.atleast_2d(np.asarray(P, float))
        idx = ((P - self.F.lo) / self.F.h).T
        return map_coordinates(self.F.G, idx, order=1, mode='nearest')

    def grad(self, P):
        P = np.atleast_2d(np.asarray(P, float)); e = self.F.h
        g = np.zeros_like(P)
        for i in range(3):
            o = np.zeros(3); o[i] = e
            g[:, i] = (self.d(P + o) - self.d(P - o)) / (2 * e)
        n = np.linalg.norm(g, axis=1, keepdims=True) + 1e-9
        return g / n

    def project(self, P, off, iters=6, maxmove=6.0):
        """Move points onto the iso-surface d = off along the gradient (only if within maxmove)."""
        P = np.array(np.atleast_2d(P), float)
        for _ in range(iters):
            d = self.d(P) - off
            g = self.grad(P)
            m = np.abs(d) < maxmove
            P[m] -= (d[m] * 0.9)[:, None] * g[m]
        return P

    def raycast(self, uv, off, y_fallback, mode='cast'):
        loc, fwd, right, up = cam.frame()
        c = cam.load(); W = c['w']; Hh = c['h']; f = c['lens'] / 36.0 * W
        u, v = uv
        dx = (u - W / 2) / f; dy = -(v - Hh / 2) / f
        r = fwd + dx * right + dy * up; r /= np.linalg.norm(r)
        # plane hit (fallback)
        tp = (y_fallback - loc[1]) / r[1]
        pp = loc + tp * r
        if mode == 'plane':
            return pp, False
        ts = np.arange(tp - 25.0, tp + 25.0, 0.15)
        P = loc[None] + ts[:, None] * r[None]
        inb = np.all((P > LO + 1) & (P < HI - 1), axis=1)
        dd = self.d(P) - off
        dd[~inb] = 1.0
        hit = np.where((dd[:-1] > 0) & (dd[1:] <= 0))[0]
        if len(hit) == 0:
            return pp, False
        i = hit[0]
        t = ts[i] + (ts[i + 1] - ts[i]) * dd[i] / (dd[i] - dd[i + 1])
        return loc + t * r, True
