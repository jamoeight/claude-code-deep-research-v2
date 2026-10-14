"""Engine for carved wings (v3): a curved 3D sheet (generalised cylinder, ~isometric (u,v) chart)
carrying a bas-relief on each face (front = +n, back = -n).

Solid = { P(u,v) + t n(u,v) :  -Hb(u,v) <= t <= Hf(u,v) }.

Relief model (per face):
  H = (body + max_k feather_k) * E(C) + detail_winner
  * feather_k : 'quill' pillows authored in the (u,v) plane (true outline polygon: narrow base, widest
                ~60%, rounded/ogive tip, bent shaft), height ramping up toward the tip so each feather's tip
                steps down onto the one beneath it (shingles).  max() over all feathers.
  * C         : coverage signed distance = min over feather outlines and membrane polygons.  The wing's
                outline is therefore formed by the outermost feathers themselves (scalloped trailing edge,
                feathered tips) - no frame / bead.  E(C) rounds the edge.
  * body      : smooth thickness field (wrist dome, thicker leading edge, flared foot ...).
  * detail    : rachis + barb striations of the feather that wins each texel (tracked like a z-buffer),
                added after smoothing so it stays crisp.  Barbs only when detail=True (fine grids).
  * cavity    : the foot of every step is deepened a little -> dark shadow line under feather tips.
The SDF is evaluated on the shared grid by projecting voxels onto the sheet (KD-tree + Newton steps)."""
import math
import numpy as np
from scipy.spatial import cKDTree
from scipy.ndimage import map_coordinates, gaussian_filter, maximum_filter
from sdf import catmull

NEG = -30.0


def unit(v):
    v = np.asarray(v, float)
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


# ----------------------------------------------------------------------------- sheet
class Sheet:
    """P(u,v) = (B(u) + v*lean + bow(u,v)*N(u), v + rise(u,v))   B: XY base curve (arc-length u), v ~ z."""

    def __init__(self, base_xy, front_xy, lean=(0.0, 0.0), bow=None, rise=None):
        C = catmull(np.asarray(base_xy, float), per=40)
        seg = np.linalg.norm(np.diff(C, axis=0), axis=1)
        s = np.concatenate([[0], np.cumsum(seg)])
        self.s, self.C = s, C
        self.t0 = unit(C[1] - C[0]); self.t1 = unit(C[-1] - C[-2])
        self.lean = np.asarray(lean, float)
        self.bow = bow
        self.rise = rise
        self.front_xy = np.asarray(front_xy, float)

    def base(self, u):
        u = np.asarray(u, float)
        x = np.interp(u, self.s, self.C[:, 0]); y = np.interp(u, self.s, self.C[:, 1])
        lo = u < self.s[0]; hi = u > self.s[-1]
        x = np.where(lo, self.C[0, 0] + (u - self.s[0]) * self.t0[0], x)
        y = np.where(lo, self.C[0, 1] + (u - self.s[0]) * self.t0[1], y)
        x = np.where(hi, self.C[-1, 0] + (u - self.s[-1]) * self.t1[0], x)
        y = np.where(hi, self.C[-1, 1] + (u - self.s[-1]) * self.t1[1], y)
        return x, y

    def nrm_xy(self, u):
        e = 0.25
        x0, y0 = self.base(u - e); x1, y1 = self.base(u + e)
        tx, ty = x1 - x0, y1 - y0
        L = np.sqrt(tx * tx + ty * ty) + 1e-12
        nx, ny = ty / L, -tx / L
        x, y = self.base(u)
        sg = np.sign(nx * (self.front_xy[0] - x) + ny * (self.front_xy[1] - y))
        sg = np.where(sg == 0, 1, sg)
        return nx * sg, ny * sg

    def P(self, u, v):
        u = np.asarray(u, float); v = np.asarray(v, float)
        x, y = self.base(u); nx, ny = self.nrm_xy(u)
        w = self.bow(u, v) if self.bow is not None else 0.0
        z = v + (self.rise(u, v) if self.rise is not None else 0.0) + 0 * u
        return np.stack([x + v * self.lean[0] + w * nx, y + v * self.lean[1] + w * ny, z], -1)

    def build(self, ur, vr, ds=0.5):
        U = np.arange(ur[0], ur[1] + 1e-9, ds); V = np.arange(vr[0], vr[1] + 1e-9, ds)
        uu, vv = np.meshgrid(U, V, indexing='ij')
        uu = uu.ravel(); vv = vv.ravel()
        P = self.P(uu, vv)
        e = 0.05
        Pu = (self.P(uu + e, vv) - self.P(uu - e, vv)) / (2 * e)
        Pv = (self.P(uu, vv + e) - self.P(uu, vv - e)) / (2 * e)
        n = unit(np.cross(Pu, Pv))
        nx, ny = self.nrm_xy(uu)
        sg = np.sign(n[:, 0] * nx + n[:, 1] * ny); sg[sg == 0] = 1
        n *= sg[:, None]
        J = np.stack([Pu, Pv, n], -1)
        self.Jinv = np.linalg.inv(J)
        self.SP, self.SU, self.SV, self.SN = P, uu, vv, n
        self.tree = cKDTree(P)
        self.ur, self.vr = ur, vr
        self.gU, self.gV, self.gds = U, V, ds
        self.gshape = (len(U), len(V))
        return self

    def normal(self, u, v):
        e = 0.05
        Pu = (self.P(u + e, v) - self.P(u - e, v)); Pv = (self.P(u, v + e) - self.P(u, v - e))
        n = unit(np.cross(Pu, Pv))
        nx, ny = self.nrm_xy(u)
        sg = np.sign(n[..., 0] * nx + n[..., 1] * ny); sg = np.where(sg == 0, 1, sg)
        return n * sg[..., None]


# ----------------------------------------------------------------------------- outline helpers
def poly_sdf(poly, uu, vv):
    """Signed distance to a closed polygon (negative inside)."""
    P = np.asarray(poly, float)
    n = len(P)
    d2 = np.full(uu.shape, 1e18); sgn = np.ones(uu.shape)
    for i in range(n):
        a = P[i]; b = P[(i + 1) % n]
        e = b - a; L2 = e @ e + 1e-12
        wx = uu - a[0]; wy = vv - a[1]
        t = np.clip((wx * e[0] + wy * e[1]) / L2, 0, 1)
        dx = wx - e[0] * t; dy = wy - e[1] * t
        d2 = np.minimum(d2, dx * dx + dy * dy)
        c1 = vv >= a[1]; c2 = vv < b[1]; c3 = e[0] * wy > e[1] * wx
        flip = (c1 & c2 & c3) | (~c1 & ~c2 & ~c3)
        sgn = np.where(flip, -sgn, sgn)
    return sgn * np.sqrt(d2)


def quill_hw(f, w, wb=0.5, fm=0.58, p=2.0):
    """Half-width profile of a feather along f in [0,1]."""
    f = np.asarray(f, float)
    return w * np.where(f < fm, wb + (1 - wb) * smoothstep(f / fm) ** 0.8,
                        np.clip(1 - np.clip((f - fm) / (1 - fm), 0, 1) ** p, 0, 1) ** (1 / p))


def quill_outline(L, w, wb=0.5, fm=0.58, p=2.0, asym=0.0, n=16):
    """Feather outline polygon in local (s, l) coords: base at s=0 (width 2*wb*w), widest at fm*L, tip at s=L.
    p: tip exponent (2 = round, <2 more pointed).  asym>0 makes the +l vane narrower."""
    f = np.concatenate([np.linspace(0, fm, 5, endpoint=False), fm + (1 - fm) * np.sin(np.linspace(0, math.pi / 2, n))])
    hw = quill_hw(f, w, wb, fm, p)
    up = np.stack([f * L, hw * (1 - asym)], 1)
    dn = np.stack([f * L, -hw * (1 + asym)], 1)
    return np.vstack([up, dn[-2::-1]])


# ----------------------------------------------------------------------------- relief
class Relief:
    def __init__(self, ur, vr, hr=0.2, detail=False, seed=0, drape=False):
        self.u0, self.v0, self.hr = ur[0], vr[0], hr
        self.nu = int(math.ceil((ur[1] - ur[0]) / hr)) + 1
        self.nv = int(math.ceil((vr[1] - vr[0]) / hr)) + 1
        sh = (self.nu, self.nv)
        h0 = 0.0 if drape else NEG
        self.H = {'f': np.full(sh, h0, np.float32), 'b': np.full(sh, h0, np.float32)}
        self.D = {'f': np.zeros(sh, np.float32), 'b': np.zeros(sh, np.float32)}
        self.body = {'f': np.zeros(sh, np.float32), 'b': np.zeros(sh, np.float32)}
        self.C = np.full(sh, 50.0, np.float32)
        self.ID = np.full(sh, -1, np.int32)
        self.nid = 0
        self.detail = detail
        self.rng = np.random.default_rng(seed)

    def grid(self):
        U = self.u0 + np.arange(self.nu) * self.hr; V = self.v0 + np.arange(self.nv) * self.hr
        return np.meshgrid(U, V, indexing='ij')

    def window(self, lo, hi):
        i0 = max(int((lo[0] - self.u0) / self.hr), 0); i1 = min(int((hi[0] - self.u0) / self.hr) + 2, self.nu)
        j0 = max(int((lo[1] - self.v0) / self.hr), 0); j1 = min(int((hi[1] - self.v0) / self.hr) + 2, self.nv)
        if i1 <= i0 or j1 <= j0:
            return None
        U = self.u0 + np.arange(i0, i1) * self.hr; V = self.v0 + np.arange(j0, j1) * self.hr
        uu, vv = np.meshgrid(U, V, indexing='ij')
        return (slice(i0, i1), slice(j0, j1)), uu, vv

    # ------------------------------------------------------------------ feather
    def quill(self, base, tip, w, h0=0.3, h1=1.6, faces=('f',), R=0.55, cam=0.35, bend=0.0, wb=0.5, fm=0.58,
              p=2.0, asym=0.0, tilt=0.0, lift=0.0, ramp=1.4, rachis=0.0, roff=-0.12, rw=0.28,
              barb=0.0, barb_p=0.75, barb_ang=26.0, splits=2, cover=True, hb=None, tiltb=None, track=True, off=0.0, spine=None,
              nose=0.0, bpow=1.3, bsplit=1.0):
        """One feather from base to tip (u,v).  w: half-width.  bend: lateral sag of the shaft (u,v units)
        at the tip.  tilt: height difference between the two vane edges (stepped overlap with neighbours).
        lift: extra height at the tip (curl).  rachis: shaft ridge height.  barb: striation depth."""
        base = np.asarray(base, float); tip = np.asarray(tip, float)
        if spine is None:
            d = tip - base; L0 = float(np.linalg.norm(d)); d /= L0
            pp = np.array([-d[1], d[0]])
            ff = np.linspace(0, 1, max(int(L0 / 0.25), 8))
            spine = base[None] + d[None] * (ff * L0)[:, None] + pp[None] * (bend * ff * ff)[:, None]
        spine = np.asarray(spine, float)
        seg = np.linalg.norm(np.diff(spine, axis=0), axis=1)
        Sa = np.concatenate([[0], np.cumsum(seg)])
        L = float(Sa[-1])
        dense = max(int(L / 0.12), 8)
        St = np.linspace(0, L, dense)
        sp = np.stack([np.interp(St, Sa, spine[:, 0]), np.interp(St, Sa, spine[:, 1])], 1)
        T = np.gradient(sp, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
        N = np.stack([-T[:, 1], T[:, 0]], 1)
        m = w * 1.4 + R + 1.0
        lo = sp.min(0) - m; hi = sp.max(0) + m
        W = self.window(lo, hi)
        if W is None:
            return
        sl, uu, vv = W
        Q = np.stack([uu.ravel(), vv.ravel()], 1)
        _, kk = cKDTree(sp).query(Q, workers=-1)
        dq = Q - sp[kk]
        s = (St[kk] + np.einsum('ij,ij->i', dq, T[kk])).reshape(uu.shape)
        l = np.einsum('ij,ij->i', dq, N[kk]).reshape(uu.shape)
        f = np.clip(s / L, 0, 1)
        poly = quill_outline(L, w, wb=wb, fm=fm, p=p, asym=asym)
        sd = poly_sdf(poly, s, l)
        hwl = np.maximum(quill_hw(f, w, wb, fm, p), 0.05 * w)
        y = np.clip(l / np.maximum(hwl, 0.3), -1, 1)
        along = h0 + (h1 - h0) * (1 - (1 - f) ** ramp)
        if lift:
            along = along + lift * smoothstep((f - 0.55) / 0.45) ** 1.5
        if nose:
            # rounded 'nose': the feather crowns at ~70 % of its length and rolls over toward the tip
            along = along - nose * (h1 - h0) * smoothstep((f - 0.62) / 0.38) ** 2
        E = np.where(sd <= -R, 1.0, np.sqrt(np.clip(1 - ((sd + R) / R) ** 2, 0, 1)))
        inside = sd <= 0
        # detail: rachis + barbs
        lr = roff * hwl
        dl = l - lr
        det = np.zeros_like(s)
        if rachis:
            fade = smoothstep((0.97 - f) / 0.2) * smoothstep((f - 0.02) / 0.1)
            det = det + rachis * (np.exp(-(dl / rw) ** 2) - 0.45 * np.exp(-(dl / (2.6 * rw)) ** 2)) * fade
        if barb and self.detail:
            ta = math.tan(math.radians(barb_ang))
            ps = barb_p / math.sin(math.radians(barb_ang))
            ad = np.abs(dl)
            ph0 = self.rng.uniform(0, 1)
            ph = (s - (ad ** 0.92) / ta) / ps + ph0 + 0.35 * np.sin(s * 0.9 + ph0 * 6)
            g = (0.5 + 0.5 * np.cos(2 * math.pi * ph)) ** bpow
            fadeb = smoothstep((ad - 0.25) / 0.35) * smoothstep((-sd - 0.15) / 0.45) * smoothstep((f - 0.08) / 0.2)
            bt = -barb * g * fadeb
            for _ in range(splits):
                side = self.rng.choice([-1, 1]); phk = self.rng.uniform(0.25, 0.85) * L / ps
                cut = np.exp(-((ph - ph0 - phk) / 0.22) ** 2) * (np.sign(dl) == side) * smoothstep((ad - 0.4) / 0.4)
                bt = bt - bsplit * barb * cut * fadeb
            det = det + bt
        for fc in faces:
            tl = tilt if (fc == 'f' or tiltb is None) else tiltb
            sc = 1.0 if (fc == 'f' or hb is None) else hb
            core = (off + along * (1 - cam * y * y) + tl * y) * sc
            h = np.where(inside, core * E, -2.0 * sd - 1.0)
            A = self.H[fc][sl]
            mwin = h > A
            if track and fc == 'f':
                self.ID[sl][mwin] = self.nid
            self.D[fc][sl][mwin] = (det * (inside & (sd < -0.05)))[mwin]
            np.maximum(A, h.astype(np.float32), out=A)
        if cover:
            np.minimum(self.C[sl], sd.astype(np.float32), out=self.C[sl])
        self.nid += 1


    # ------------------------------------------------------------------ draped feather (painter's stacking)
    def _frame(self, base, tip, w, R, spine=None, bend=0.0):
        base = np.asarray(base, float); tip = np.asarray(tip, float)
        if spine is None:
            d = tip - base; L0 = float(np.linalg.norm(d)); d /= L0
            pp = np.array([-d[1], d[0]])
            ff = np.linspace(0, 1, max(int(L0 / 0.25), 8))
            spine = base[None] + d[None] * (ff * L0)[:, None] + pp[None] * (bend * ff * ff)[:, None]
        spine = np.asarray(spine, float)
        seg = np.linalg.norm(np.diff(spine, axis=0), axis=1)
        Sa = np.concatenate([[0], np.cumsum(seg)])
        L = float(Sa[-1])
        dense = max(int(L / 0.12), 8)
        St = np.linspace(0, L, dense)
        sp = np.stack([np.interp(St, Sa, spine[:, 0]), np.interp(St, Sa, spine[:, 1])], 1)
        T = np.gradient(sp, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
        N = np.stack([-T[:, 1], T[:, 0]], 1)
        m = w * 1.4 + R + 2.5
        W = self.window(sp.min(0) - m, sp.max(0) + m)
        if W is None:
            return None
        sl, uu, vv = W
        Q = np.stack([uu.ravel(), vv.ravel()], 1)
        _, kk = cKDTree(sp).query(Q, workers=-1)
        dq = Q - sp[kk]
        s = (St[kk] + np.einsum('ij,ij->i', dq, T[kk])).reshape(uu.shape)
        l = np.einsum('ij,ij->i', dq, N[kk]).reshape(uu.shape)
        return sl, uu, vv, s, l, L

    def drape(self, base, tip, w, T=0.8, faces=('f',), Tb=None, spine=None, bend=0.0, wb=0.5, fm=0.58, p=2.0,
              asym=0.0, R=0.5, ramp=0.45, crown=0.12, cross=0.3, tilt=0.0, tiltb=None, blur=1.0, keep=0.3,
              cav=0.12, cav_w=0.55, rachis=0.0, rgroove=0.0, rw=0.2, roff=-0.1, barb=0.0, barb_p=0.75,
              barb_ang=26.0, splits=2, bpow=1.3, bsplit=1.0, cover=False, track=True, lift=0.0):
        """A feather LAID ON TOP of what is already there (painter's algorithm, bottom layer first).
        Its top surface = (smoothed surface below) + its own thickness profile, so it can never dip under a
        neighbour: every free edge is a rounded STEP down onto the feather beneath (no V grooves, no outlines).
        T: thickness at the crown; thickness ramps up from ~0 at the hidden base (over ramp*L), crowns slightly at
        ~70 %, is domed across (cross), and rounds over its free edge with radius R.  tilt: extra thickness on the
        +l vane (absolute units) -> sideways card-like overlap.  cav: small shadow dent at the foot of the tip.
        rachis: shaft ridge; rgroove: groove flanking it; barb: striations (fine grids only)."""
        fr = self._frame(base, tip, w, R, spine, bend)
        if fr is None:
            return
        sl, uu, vv, s, l, L = fr
        f = np.clip(s / L, 0, 1)
        poly = quill_outline(L, w, wb=wb, fm=fm, p=p, asym=asym)
        sd = poly_sdf(poly, s, l)
        hwl = np.maximum(quill_hw(f, w, wb, fm, p), 0.05 * w)
        y = np.clip(l / np.maximum(hwl, 0.3), -1, 1)
        a = smoothstep(f / ramp) ** 0.8 * (1 + crown * np.exp(-((f - 0.68) / 0.22) ** 2))
        if lift:
            a = a + lift * smoothstep((f - 0.55) / 0.45) ** 1.5
        E = np.where(sd <= -R, 1.0, np.sqrt(np.clip(1 - ((sd + R) / R) ** 2, 0, 1)))
        inside = sd < 0
        al = np.where(inside, smoothstep(-sd / (0.7 * R)), 0.0)
        # detail
        lr = roff * hwl
        dl = l - lr
        det = np.zeros_like(s)
        if rachis or rgroove:
            fade = smoothstep((0.96 - f) / 0.18) * smoothstep((f - 0.03) / 0.12)
            det = det + (rachis * np.exp(-(dl / rw) ** 2) - rgroove * np.exp(-(dl / (2.4 * rw)) ** 2)) * fade
        if barb and self.detail:
            ta = math.tan(math.radians(barb_ang))
            ps = barb_p / math.sin(math.radians(barb_ang))
            ad = np.abs(dl)
            ph0 = self.rng.uniform(0, 1)
            ph = (s - (ad ** 0.92) / ta) / ps + ph0 + 0.35 * np.sin(s * 0.9 + ph0 * 6)
            g = (0.5 + 0.5 * np.cos(2 * math.pi * ph)) ** bpow
            fadeb = smoothstep((ad - 0.25) / 0.35) * smoothstep((-sd - 0.15) / 0.45) * smoothstep((f - 0.08) / 0.2)
            bt = -barb * g * fadeb
            for _ in range(splits):
                side = self.rng.choice([-1, 1]); phk = self.rng.uniform(0.25, 0.85) * L / ps
                cut = np.exp(-((ph - ph0 - phk) / 0.22) ** 2) * (np.sign(dl) == side) * smoothstep((ad - 0.4) / 0.4)
                bt = bt - bsplit * barb * cut * fadeb
            det = det + bt
        k_b = int(max(round(blur / self.hr), 1))
        for fc in faces:
            Tf = T if (fc == 'f' or Tb is None) else Tb
            tl = tilt if (fc == 'f' or tiltb is None) else tiltb
            if Tf <= 0:
                continue
            thick = np.maximum(Tf * a * (1 - cross * y * y) + tl * y * a, 0.0) * E
            Hb = self.H[fc][sl]
            below = Hb.astype(np.float64)
            bs = gaussian_filter(below, k_b, mode='nearest')
            rest = (1 - keep) * bs + keep * below
            top = np.maximum(rest + thick, below + 0.2 * thick)
            new = below + al * (top - below)
            if cav > 0:
                ring = (~inside) & (sd < cav_w)
                dent = cav * (1 - np.clip(sd / cav_w, 0, 1)) ** 2 * smoothstep((f - 0.6) / 0.25)
                new = np.where(ring, below - dent, new)
            if track and fc == 'f':
                self.ID[sl][al > 0.5] = self.nid
            self.D[fc][sl][al > 0.5] = (det * (sd < -0.05))[al > 0.5]
            self.H[fc][sl] = new.astype(np.float32)
        if cover:
            np.minimum(self.C[sl], sd.astype(np.float32), out=self.C[sl])
        self.nid += 1

    # ------------------------------------------------------------------ areas
    def membrane(self, poly, h=0.0, faces=('f', 'b'), cover=True):
        """Mark the inside of a polygon as covered (solid); optional flat relief h."""
        poly = np.asarray(poly, float)
        W = self.window(poly.min(0) - 2, poly.max(0) + 2)
        if W is None:
            return
        sl, uu, vv = W
        sd = poly_sdf(poly, uu, vv)
        if cover:
            np.minimum(self.C[sl], sd.astype(np.float32), out=self.C[sl])
        if h is not None:
            for fc in faces:
                hh = np.where(sd <= 0, h, -2.0 * sd - 1.0).astype(np.float32)
                np.maximum(self.H[fc][sl], hh, out=self.H[fc][sl])

    def add_body(self, face, fn):
        uu, vv = self.grid()
        self.body[face] += fn(uu, vv).astype(np.float32)

    def cut(self, poly, R=1.0):
        """Remove coverage inside a polygon (e.g. a window)."""
        uu, vv = self.grid()
        sd = poly_sdf(np.asarray(poly, float), uu, vv)
        np.maximum(self.C, (-sd).astype(np.float32), out=self.C)

    # ------------------------------------------------------------------ finish
    def finish(self, smooth=0.18, Re=1.3, cav=0.35, cav_r=0.7, hmin=0.0, Re_auto=None):
        """Re_auto=(k, rmin, rmax): edge rounding radius = k * local half thickness (semicircular rim section),
        at least Re."""
        uu, vv = self.grid()
        C = self.C
        if callable(Re):
            Re = Re(uu, vv)
        if Re_auto is not None:
            k, rmin, rmax = Re_auto
            Tt = (self.body['f'] + np.maximum(self.H['f'], 0) + self.body['b'] + np.maximum(self.H['b'], 0)) * (C < 0)
            Tt = gaussian_filter(Tt.astype(np.float64), 2.0 / self.hr)
            Wt = gaussian_filter((C < 0).astype(np.float64), 2.0 / self.hr)
            Tt = Tt / np.maximum(Wt, 0.2)
            Re = np.maximum(Re, np.clip(0.5 * k * Tt, rmin, rmax))
        E = np.where(C <= -Re, 1.0, np.sqrt(np.clip(1 - ((C + Re) / Re) ** 2, 0, 1))).astype(np.float32)
        self.Re_map = Re
        out = {}
        for fc in ('f', 'b'):
            H = np.maximum(self.H[fc], hmin)
            if cav > 0:
                k = max(int(round(cav_r / self.hr)), 1) * 2 + 1
                Hm = maximum_filter(H, size=k)
                H = H - cav * np.clip(Hm - H - 0.15, 0, 1.2)
            if smooth > 0:
                H = gaussian_filter(H, smooth / self.hr)
            Ht = (self.body[fc] + H) * E
            Ht = Ht + self.D[fc] * (C < -0.4)
            Ht = np.where(C > 0, -2.0 * C, Ht)
            gu, gv = np.gradient(Ht, self.hr)
            g = np.sqrt(1.0 + np.clip(gu * gu + gv * gv, 0, 9.0))
            out[fc] = (Ht.astype(np.float32), g.astype(np.float32))
        self.final = out
        return out

    def sample(self, fc, u, v):
        H, g = self.final[fc]
        cu = (u - self.u0) / self.hr; cv = (v - self.v0) / self.hr
        h = map_coordinates(H, [cu, cv], order=1, mode='nearest')
        gg = map_coordinates(g, [cu, cv], order=1, mode='nearest')
        return h, gg


# ----------------------------------------------------------------------------- SDF fill
def fill(F, sheet, relief, margin=None, k=0.0):
    """Union the sheet solid into Field F (in place)."""
    if margin is None:
        margin = max(float(relief.final['f'][0].max()), float(relief.final['b'][0].max())) + 3.0
    SP = sheet.SP
    lo = SP.min(0) - margin; hi = SP.max(0) + margin
    a = np.clip(np.floor((lo - F.lo) / F.h).astype(int), 0, F.shape)
    b = np.clip(np.ceil((hi - F.lo) / F.h).astype(int) + 1, 0, F.shape)
    cs = 4
    ii = np.arange(a[0], b[0], cs); jj = np.arange(a[1], b[1], cs); kk = np.arange(a[2], b[2], cs)
    if len(ii) == 0 or len(jj) == 0 or len(kk) == 0:
        return F
    gi, gj, gk = np.meshgrid(ii, jj, kk, indexing='ij')
    X = np.stack([F.lo[0] + gi.ravel() * F.h, F.lo[1] + gj.ravel() * F.h, F.lo[2] + gk.ravel() * F.h], 1)
    # local band half-width per sheet sample: dilated local relief height + slack (the global max is set by a few
    # thick spots such as the inner foot; using it everywhere made the band ~3x thicker than needed)
    Hm = np.maximum(np.maximum(relief.final['f'][0], relief.final['b'][0]), 0.0)
    Hm = maximum_filter(Hm, size=max(int(6.0 / relief.hr), 3))
    cu = (sheet.SU - relief.u0) / relief.hr; cv = (sheet.SV - relief.v0) / relief.hr
    msamp = map_coordinates(Hm, [cu, cv], order=1, mode='nearest') + 2.5
    dist, nb = sheet.tree.query(X, distance_upper_bound=margin + cs * F.h * 1.8, workers=-1)
    okb = np.isfinite(dist)
    nb = np.minimum(nb, len(msamp) - 1)
    okb &= dist < msamp[nb] + cs * F.h * 1.8 + 1.0
    near = okb.reshape(gi.shape)
    blocks = np.argwhere(near)
    if len(blocks) == 0:
        return F
    off = np.stack(np.meshgrid(np.arange(cs), np.arange(cs), np.arange(cs), indexing='ij'), -1).reshape(-1, 3)
    bi = np.stack([ii[blocks[:, 0]], jj[blocks[:, 1]], kk[blocks[:, 2]]], 1)
    G = F.G
    bnd = np.array(F.shape, np.int32)
    _, bn = sheet.tree.query(F.lo + bi * F.h + 0.5 * (cs - 1) * F.h, workers=-1)
    nU, nV = sheet.gshape
    U0, V0, ds = sheet.gU[0], sheet.gV[0], sheet.gds
    CH = max(int(4000 * (0.45 / F.h) ** 0), 500)
    for c0 in range(0, len(bi), CH):
        idx = (bi[c0:c0 + CH, None, :] + off[None, :, :]).reshape(-1, 3).astype(np.int32)
        nn0 = np.repeat(bn[c0:c0 + CH], len(off))
        ok = (idx < bnd).all(1)
        idx = idx[ok]; nn0 = nn0[ok]
        X = (F.lo + idx * F.h)
        _, nn0 = sheet.tree.query(X, workers=-1)          # per-voxel seed (robust on strongly curved parts)
        u = sheet.SU[nn0].copy(); v = sheet.SV[nn0].copy()
        for it in range(3):
            i = np.clip(np.rint((u - U0) / ds).astype(np.int64), 0, nU - 1)
            j = np.clip(np.rint((v - V0) / ds).astype(np.int64), 0, nV - 1)
            nn = i * nV + j
            dl = X - sheet.SP[nn]
            duvt = np.einsum('nij,nj->ni', sheet.Jinv[nn], dl)
            u = sheet.SU[nn] + duvt[:, 0]; v = sheet.SV[nn] + duvt[:, 1]; t = duvt[:, 2]
        # refine with a smoothly interpolated sheet (bilinear P and n): removes the grid-snapping noise
        # ("orange peel") on strongly curved, thick parts
        for it in range(3):
            fi = np.clip((u - U0) / ds, 0, nU - 1.001); fj = np.clip((v - V0) / ds, 0, nV - 1.001)
            i0 = np.floor(fi).astype(np.int64); j0 = np.floor(fj).astype(np.int64)
            a = (fi - i0)[:, None]; b = (fj - j0)[:, None]
            n00 = i0 * nV + j0; n10 = n00 + nV; n01 = n00 + 1; n11 = n10 + 1
            Pq = (1 - a) * (1 - b) * sheet.SP[n00] + a * (1 - b) * sheet.SP[n10] + (1 - a) * b * sheet.SP[n01] + a * b * sheet.SP[n11]
            nq = (1 - a) * (1 - b) * sheet.SN[n00] + a * (1 - b) * sheet.SN[n10] + (1 - a) * b * sheet.SN[n01] + a * b * sheet.SN[n11]
            nq /= np.linalg.norm(nq, axis=1, keepdims=True) + 1e-12
            nn = np.where(a[:, 0] < 0.5, np.where(b[:, 0] < 0.5, n00, n01), np.where(b[:, 0] < 0.5, n10, n11))
            dl = X - Pq
            duv = np.einsum('nij,nj->ni', sheet.Jinv[nn], dl)
            if it < 2:
                u = u + duv[:, 0]; v = v + duv[:, 1]
            t = np.einsum('ij,ij->i', dl, nq)
        keep = np.abs(t) < msamp[nn0] + 1.0
        idx = idx[keep]; u = u[keep]; v = v[keep]; t = t[keep]
        hf, gf = relief.sample('f', u, v)
        hb, gb = relief.sample('b', u, v)
        d = np.maximum((t - hf) / gf, (-t - hb) / gb)
        du_out = np.maximum(sheet.ur[0] - u, 0) + np.maximum(u - sheet.ur[1], 0)
        dv_out = np.maximum(sheet.vr[0] - v, 0) + np.maximum(v - sheet.vr[1], 0)
        o = np.maximum(du_out, dv_out)
        d = np.where(o > 0, np.maximum(d, o), d)
        d = np.minimum(d, 50.0).astype(np.float32)
        cur = G[idx[:, 0], idx[:, 1], idx[:, 2]]
        if k > 0:
            hh = np.clip(k - np.abs(cur - d), 0, None) / k
            new = np.minimum(cur, d) - hh * hh * k * 0.25
        else:
            new = np.minimum(cur, d)
        G[idx[:, 0], idx[:, 1], idx[:, 2]] = new
    return F
