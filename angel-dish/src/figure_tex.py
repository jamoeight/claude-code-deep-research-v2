"""Camera-space drapery displacement for the figure (helper for figure.py).

A CamTex is a texture laid over the image plane of a camera (the reference-photo camera for everything the
photo shows, plus orbit cameras for the hidden sides).  Each texel stores the base-surface point its ray hits.
Folds are 3D polylines on the base surface (pixel polylines traced on the photo are ray-cast onto it); they are
rasterised with *surface* distances (design units), so widths / heights / striation pitch are true sizes:

  crest  A>0 : rounded crest, gentle flank (half-width wu) on one side, steep flank (wd) on the other, ending
               in a thin dark crease at the foot of the steep flank; tapered (height AND width) at both ends.
  crease A<0 : narrow valley (same profile, negative).
  guide  A=0 : no relief, only steers the fine combed striations.
Fine striations: sin(2 pi d / pitch) of the distance d to the nearest fold / guide (combed lines that run
parallel to the flow), phase-jittered, faded at the seams between two folds' zones.
"""
import math
import numpy as np
from scipy.spatial import cKDTree
from scipy import ndimage
from sdf import catmull, resample
import figure_k as K
import cam as CAM


def inpoly(Q, poly):
    """even-odd point-in-polygon for points Q (n,2)."""
    Q = np.asarray(Q, float); poly = np.asarray(poly, float)
    x = Q[:, 0]; y = Q[:, 1]; ins = np.zeros(len(Q), bool)
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        c = (y1 > y) != (y2 > y)
        xi = x1 + (y - y1) * (x2 - x1) / ((y2 - y1) if y2 != y1 else 1e-12)
        ins ^= c & (x < xi)
    return ins


def sstep(x, a, b):
    t = np.clip((x - a) / (b - a), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def ref_camera():
    c = CAM.load(); loc, fwd, right, up = CAM.frame(c)
    f = c['lens'] / 36.0 * c['w']
    return dict(loc=loc, fwd=fwd, right=right, up=up, f=f, W=c['w'], H=c['h'])


def orbit_camera(target, az, el, dist, lens=60.0, W=1000, H=1000):
    az, el = math.radians(az), math.radians(el)
    t = np.asarray(target, float)
    loc = t + dist * np.array([math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)])
    fwd = t - loc; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return dict(loc=loc, fwd=fwd, right=right, up=up, f=lens / 36.0 * W, W=W, H=H)


def project(c, P):
    P = np.atleast_2d(P) - c['loc']
    zc = P @ c['fwd']
    u = c['W'] / 2 + c['f'] * (P @ c['right']) / zc
    v = c['H'] / 2 - c['f'] * (P @ c['up']) / zc
    return np.stack([u, v], 1)


class CamTex:
    def __init__(self, c, box, ts, G, lo, h, full=True):
        """c camera dict, box (u0,v0,u1,v1) in camera pixels, ts texels per pixel, G base SDF block at lo, h.
        full=False: tracing only (no texel grid)."""
        self.c = c; self.u0, self.v0, u1, v1 = box; self.ts = ts
        self.G = G; self.lo = np.asarray(lo, float); self.h = h
        if not full:
            return
        self.nu = int((u1 - self.u0) * ts); self.nv = int((v1 - self.v0) * ts)
        uu = self.u0 + (np.arange(self.nu) + 0.0) / ts; vv = self.v0 + (np.arange(self.nv) + 0.0) / ts
        U, V = np.meshgrid(uu, vv)
        D = self.rays(np.stack([U.ravel(), V.ravel()], 1))
        out = np.empty_like(D)
        K.cast(G, self.lo[0], self.lo[1], self.lo[2], h, np.asarray(c['loc'], float), D, 10.0, 600.0, out)
        self.X = out.reshape(self.nv, self.nu, 3)
        self.valid = ~np.isnan(self.X[..., 0])
        Xf = np.where(self.valid[..., None], self.X, 0.0).reshape(-1, 3)
        self.N = self.normals(Xf).reshape(self.nv, self.nu, 3)
        self.D = np.zeros((self.nv, self.nu)); self.d1 = np.full((self.nv, self.nu), 99.0)
        self.d2 = np.full((self.nv, self.nu), 99.0); self.id1 = np.full((self.nv, self.nu), -1)
        self.dn = np.full((self.nv, self.nu), 99.0)
        self.smask = np.ones((self.nv, self.nu))
        self.nf = 0

    # ---------------------------------------------------------------- geometry
    def rays(self, uv):
        c = self.c
        dx = (uv[:, 0] - c['W'] / 2) / c['f']; dy = -(uv[:, 1] - c['H'] / 2) / c['f']
        d = c['fwd'][None] + dx[:, None] * c['right'][None] + dy[:, None] * c['up'][None]
        return np.ascontiguousarray(d / np.linalg.norm(d, axis=1, keepdims=True))

    def sdf(self, P):
        P = np.ascontiguousarray(np.atleast_2d(P), np.float64); out = np.empty(len(P))
        K.sample(self.G, self.lo[0], self.lo[1], self.lo[2], self.h, P, out)
        return out

    def normals(self, P, e=None):
        e = e or self.h * 0.75
        n = np.zeros_like(P)
        for i in range(3):
            d = np.zeros(3); d[i] = e
            n[:, i] = self.sdf(P + d) - self.sdf(P - d)
        return n / (np.linalg.norm(n, axis=1, keepdims=True) + 1e-12)

    def cast(self, uv):
        D = self.rays(np.atleast_2d(np.asarray(uv, float))); out = np.empty_like(D)
        K.cast(self.G, self.lo[0], self.lo[1], self.lo[2], self.h, np.asarray(self.c['loc'], float), D, 10.0, 600.0, out)
        return out

    def trace(self, pix, step=0.12):
        """pixel polyline (camera pixels) -> dense 3D surface polyline."""
        pix = np.asarray(pix, float)
        dense = catmull(pix, per=12) if len(pix) > 2 else resample(pix, 24)
        P = self.cast(dense)
        P = P[~np.isnan(P[:, 0])]
        if len(P) < 2:
            return P
        # drop jumps (ray slipped onto another surface)
        seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
        med = np.median(seg) + 1e-6
        keep = np.concatenate([[True], seg < 8 * med + 1.0])
        P = P[np.cumsum(~keep) == 0] if not keep.all() else P
        L = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
        return resample(P, max(4, int(L / step) + 1))

    def surf(self, pts3, step=0.12, iters=5):
        """3D polyline (approximate) -> dense polyline projected onto the base surface."""
        P = resample(catmull(np.asarray(pts3, float), per=10), 200)
        for _ in range(iters):
            d = self.sdf(P); n = self.normals(P)
            P = P - n * d[:, None]
        L = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
        return resample(P, max(4, int(L / step) + 1))

    # ---------------------------------------------------------------- rasterisation
    def _region(self, P, margin):
        uv = project(self.c, P)
        lo = uv.min(0) - margin; hi = uv.max(0) + margin
        a0 = int(max(0, (lo[0] - self.u0) * self.ts)); a1 = int(min(self.nu, (hi[0] - self.u0) * self.ts + 1))
        b0 = int(max(0, (lo[1] - self.v0) * self.ts)); b1 = int(min(self.nv, (hi[1] - self.v0) * self.ts + 1))
        return a0, a1, b0, b1

    def fold(self, P, A, wu, wd=None, steep='R', taper=(0.3, 0.3), crease=0.35, wtaper=0.55, guide=True, hpow=1.0,
             step=0.0, sband=3.0, shape='cos'):
        """Rasterise one fold along dense 3D surface polyline P.  step>0: additionally lower the steep side by
        `step` (an overlapping fabric edge / garment edge), fading out `sband` units away from the edge."""
        if len(P) < 3:
            return
        wd = wu * 0.55 if wd is None else wd
        hm = self.h
        wd = max(wd, 1.9 * hm); wu = max(wu, 2.2 * hm)       # never narrower than the grid can carry (no aliasing)
        wmax = max(wu, wd * 2.2, sband * 1.6 if step else 0) * 1.15 + 0.5
        pxs = self.c['f'] / np.linalg.norm(P.mean(0) - self.c['loc'])     # px per unit
        a0, a1, b0, b1 = self._region(P, wmax * pxs + 3)
        if a1 <= a0 or b1 <= b0:
            return
        X = self.X[b0:b1, a0:a1]; ok = self.valid[b0:b1, a0:a1]
        Q = X[ok]
        if len(Q) == 0:
            return
        tree = cKDTree(P)
        d, idx = tree.query(Q, distance_upper_bound=max(wmax, 6.0) + 6.0)
        far = ~np.isfinite(d); idx = np.where(far, 0, idx); d = np.where(far, 99.0, d)
        s = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]); t = s / s[-1]
        T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
        Nn = self.normals(P)
        side = np.einsum('ij,ij->i', Q - P[idx], np.cross(Nn[idx], T[idx]))   # >0: left of travel (seen from outside)
        sgn = np.where(side >= 0, 1.0, -1.0)
        ta, tb = taper
        e = np.minimum(np.clip(t / max(ta, 1e-6), 0, 1), np.clip((1 - t) / max(tb, 1e-6), 0, 1))
        env = np.sin(e * math.pi / 2)
        en = env[idx]
        endcap = (idx == 0) | (idx == len(P) - 1)
        en = np.where(endcap, en * np.exp(-(d / max(wd, 0.5)) ** 2), en)
        wsc = (1 - wtaper) + wtaper * en
        is_steep = (sgn > 0) if steep == 'L' else (sgn < 0)
        sd = sgn * d
        w = np.where(is_steep, wd, wu) * wsc
        x = d / w
        if shape == 'roll':
            prof = np.where(x < 1, np.clip(1 - x * x, 0, 1) ** 0.75, 0.0)
        else:
            prof = np.where(x < 1, 0.5 * (1 + np.cos(np.pi * np.clip(x, 0, 1))), 0.0)
        if crease and A > 0:
            xc = (d - wd * wsc * 1.05) / np.maximum(0.42 * wd * wsc + 0.05, 1.5 * hm)
            cr = np.where(np.abs(xc) < 1, 0.5 * (1 + np.cos(np.pi * np.clip(xc, -1, 1))), 0.0)
            prof = prof - crease * cr * is_steep
        val = A * (en ** hpow) * prof
        if step:
            low = np.where(is_steep, d, -d)
            sw_ = max(0.35 * wd, 1.3 * hm)
            val = val - step * en * sstep(low, -sw_, sw_) * (1 - sstep(d, sband, sband * 1.6))
        Dsub = self.D[b0:b1, a0:a1]
        Dsub[ok] += val
        if guide:
            dd = d + (1 - en) * 2.5           # fold ends release the striations
            d1 = self.d1[b0:b1, a0:a1]; d2 = self.d2[b0:b1, a0:a1]; dn = self.dn[b0:b1, a0:a1]
            o1 = d1[ok]; o2 = d2[ok]; on = dn[ok]
            better = dd < o1
            n2 = np.where(better, o1, np.minimum(o2, dd))
            n1 = np.where(better, dd, o1)
            # phase distance: signed so that lines continue across the fold
            nn = np.where(better, sd + (1 - en) * 2.5 * sgn, on)
            d1[ok] = n1; d2[ok] = n2; dn[ok] = nn
        self.nf += 1

    def region_step(self, poly_px, depth, soft_px=2.0, mask_stri=True):
        """Lower the surface by `depth` inside a pixel polygon (soft edge) -- e.g. skin inside a neckline."""
        uu = self.u0 + np.arange(self.nu) / self.ts; vv = self.v0 + np.arange(self.nv) / self.ts
        U, V = np.meshgrid(uu, vv)
        ins = inpoly(np.stack([U.ravel(), V.ravel()], 1), poly_px).reshape(U.shape)
        di = ndimage.distance_transform_edt(ins) / self.ts; do = ndimage.distance_transform_edt(~ins) / self.ts
        sd = np.where(ins, di, -do)
        m = sstep(sd, -soft_px * 0.5, soft_px * 0.5)
        self.D -= depth * m
        if mask_stri:
            self.smask *= 1 - sstep(sd, -soft_px * 2, soft_px)
        return m

    def stri_mask_poly(self, poly_px, soft_px=4.0):
        uu = self.u0 + np.arange(self.nu) / self.ts; vv = self.v0 + np.arange(self.nv) / self.ts
        U, V = np.meshgrid(uu, vv)
        ins = inpoly(np.stack([U.ravel(), V.ravel()], 1), poly_px).reshape(U.shape)
        di = ndimage.distance_transform_edt(ins) / self.ts
        self.smask *= 1 - sstep(di, 0, soft_px)

    def texture(self, seed=3, jitter=0.12, dclip=(-4.0, 5.0), blur=0.0):
        rng = np.random.default_rng(seed)
        if blur > 0:
            # soften the relief map (rounded crests / filleted valleys): sigma `blur` design units
            Xm = self.X[self.valid]
            pxs = self.c['f'] / np.linalg.norm(Xm.mean(0) - self.c['loc']) if len(Xm) else 6.0
            sg = blur * pxs * self.ts
            w = ndimage.gaussian_filter(self.valid.astype(float), sg)
            self.D = np.where(self.valid, ndimage.gaussian_filter(np.where(self.valid, self.D, 0.0), sg) / np.maximum(w, 1e-3), 0.0)
        nz = ndimage.gaussian_filter(rng.standard_normal((self.nv, self.nu)), 6 * self.ts)
        nz /= nz.std() + 1e-9
        nz2 = ndimage.gaussian_filter(rng.standard_normal((self.nv, self.nu)), 10 * self.ts)
        nz2 /= nz2.std() + 1e-9
        seam = sstep(self.d2 - self.d1, 0.3, 2.2)
        far = 1 - sstep(self.d1, 3.5, 6.5)
        nearc = sstep(self.d1, 1.2, 2.2)                        # none on / right beside a crest or step edge
        zm = 1 - sstep(np.where(self.valid, self.X[..., 2], 99.0), 38.0, 45.0)   # lower skirt only
        sw = seam * far * nearc * zm * self.smask * np.clip(0.75 + 0.3 * nz2, 0.3, 1.2)
        dn = self.dn + jitter * nz
        D = np.clip(self.D, *dclip)
        # soft clip
        TX = np.zeros((self.nv, self.nu, 7), np.float64)
        TX[..., :3] = np.where(self.valid[..., None], self.X, 0.0)
        TX[..., 3] = np.where(self.valid, D, 0.0)
        TX[..., 4] = np.where(self.valid, dn, 0.0)
        TX[..., 5] = np.where(self.valid, sw, 0.0)
        TX[..., 6] = self.valid
        return np.ascontiguousarray(TX)

    def camvec(self):
        c = self.c
        return np.array([*c['loc'], *c['fwd'], *c['right'], *c['up'], c['f'], c['W'], c['H']], np.float64)

    def apply(self, G0, Gout, band=6.0, fine=False, pitch=0.8, amp=0.22, rv=(1.2, 2.4), fc=(0.04, 0.22), TX=None, nfoot=1, blur=0.0):
        TX = self.texture(blur=blur) if TX is None else TX
        K.displace(G0, Gout, self.lo[0], self.lo[1], self.lo[2], self.h, band, self.camvec(), TX, float(self.u0), float(self.v0),
                   float(self.ts), fine, pitch, amp, rv[0], rv[1], fc[0], fc[1], nfoot)
