"""Grid-based SDF sculpting engine (numba).

Coordinates are millimetres. X = viewer's right, Y = away from viewer (back), Z = up.
Primitives are evaluated only inside their (padded) AABB and combined into a dense
float32 grid with union / smooth-union / subtract / intersect operators.
"""
import math
import numpy as np
from numba import njit, prange

FAR = np.float32(50.0)

# ---------------------------------------------------------------- primitive kinds
SPHERE, ELLIPSOID, RCONE, RBOX, ESEG, FEATHER, TORUS = 0, 1, 2, 3, 4, 5, 6
NPARAM = 24


@njit(fastmath=True, inline='always')
def _smin(a, b, k):
    if k <= 0.0:
        return a if a < b else b
    h = k - abs(a - b)
    if h <= 0.0:
        return a if a < b else b
    h = h / k
    return (a if a < b else b) - h * h * k * 0.25


@njit(fastmath=True, inline='always')
def _smax(a, b, k):
    return -_smin(-a, -b, k)


@njit(fastmath=True)
def prim_dist(kind, q, x, y, z):
    if kind == 0:  # sphere c r
        dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
        return math.sqrt(dx * dx + dy * dy + dz * dz) - q[3]
    elif kind == 1:  # ellipsoid c(0:3) R rows(3:12) radii(12:15)
        dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
        lx = (q[3] * dx + q[4] * dy + q[5] * dz) / q[12]
        ly = (q[6] * dx + q[7] * dy + q[8] * dz) / q[13]
        lz = (q[9] * dx + q[10] * dy + q[11] * dz) / q[14]
        k0 = math.sqrt(lx * lx + ly * ly + lz * lz)
        k1 = math.sqrt((lx / q[12]) ** 2 + (ly / q[13]) ** 2 + (lz / q[14]) ** 2)
        if k1 < 1e-9:
            return -min(q[12], min(q[13], q[14]))
        return k0 * (k0 - 1.0) / k1
    elif kind == 2:  # round cone a(0:3) b(3:6) ra rb   (iq sdRoundCone, exact)
        bax = q[3] - q[0]; bay = q[4] - q[1]; baz = q[5] - q[2]
        r1 = q[6]; r2 = q[7]
        l2 = bax * bax + bay * bay + baz * baz
        if l2 < 1e-12:
            dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
            return math.sqrt(dx * dx + dy * dy + dz * dz) - max(r1, r2)
        rr = r1 - r2
        a2 = l2 - rr * rr
        il2 = 1.0 / l2
        pax = x - q[0]; pay = y - q[1]; paz = z - q[2]
        yy = pax * bax + pay * bay + paz * baz
        zz = yy - l2
        cx = pax * l2 - bax * yy; cy = pay * l2 - bay * yy; cz = paz * l2 - baz * yy
        x2 = cx * cx + cy * cy + cz * cz
        y2 = yy * yy * l2
        z2 = zz * zz * l2
        k = (1.0 if rr >= 0 else -1.0) * rr * rr * x2
        if a2 <= 0.0:  # one sphere contains the other
            dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
            d1 = math.sqrt(dx * dx + dy * dy + dz * dz) - r1
            dx = x - q[3]; dy = y - q[4]; dz = z - q[5]
            d2 = math.sqrt(dx * dx + dy * dy + dz * dz) - r2
            return min(d1, d2)
        sz = 1.0 if zz >= 0 else -1.0
        if sz * a2 * z2 > k:
            return math.sqrt(x2 + z2) * il2 - r2
        sy = 1.0 if yy >= 0 else -1.0
        if sy * a2 * y2 < k:
            return math.sqrt(x2 + y2) * il2 - r1
        return (math.sqrt(x2 * a2 * il2) + yy * rr) * il2 - r1
    elif kind == 3:  # rounded box c(0:3) R rows(3:12) half(12:15) round(15)
        dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
        lx = abs(q[3] * dx + q[4] * dy + q[5] * dz) - q[12]
        ly = abs(q[6] * dx + q[7] * dy + q[8] * dz) - q[13]
        lz = abs(q[9] * dx + q[10] * dy + q[11] * dz) - q[14]
        ox = max(lx, 0.0); oy = max(ly, 0.0); oz = max(lz, 0.0)
        return math.sqrt(ox * ox + oy * oy + oz * oz) + min(max(lx, max(ly, lz)), 0.0) - q[15]
    elif kind == 4:  # elliptic tapered segment a(0:3) b(3:6) up(6:9) w1 w2 t1 t2 (9:13)
        bax = q[3] - q[0]; bay = q[4] - q[1]; baz = q[5] - q[2]
        L2 = bax * bax + bay * bay + baz * baz
        L = math.sqrt(L2) + 1e-12
        tx = bax / L; ty = bay / L; tz = baz / L
        ux = q[6]; uy = q[7]; uz = q[8]
        pax = x - q[0]; pay = y - q[1]; paz = z - q[2]
        s = (pax * tx + pay * ty + paz * tz)
        sc = min(max(s, 0.0), L)
        f = sc / L
        w = q[9] + (q[10] - q[9]) * f
        t = q[11] + (q[12] - q[11]) * f
        vx = pax - tx * sc; vy = pay - ty * sc; vz = paz - tz * sc
        vu = vx * ux + vy * uy + vz * uz
        wx = vx - ux * vu; wy = vy - uy * vu; wz = vz - uz * vu
        vw = math.sqrt(wx * wx + wy * wy + wz * wz)
        va = s - sc
        rmin = min(w, t)
        e = math.sqrt((vu / t) ** 2 + (vw / w) ** 2 + (va / w) ** 2)
        return (e - 1.0) * rmin
    elif kind == 5:  # feather: base c(0:3) axis t(3:6) normal n(6:9) L W1(base r) W2(tip r) T bend ridge lift (9:16)
        dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
        lx = dx * q[3] + dy * q[4] + dz * q[5]
        lz = dx * q[6] + dy * q[7] + dz * q[8]
        bx = q[4] * q[8] - q[5] * q[7]
        by = q[5] * q[6] - q[3] * q[8]
        bz = q[3] * q[7] - q[4] * q[6]
        ly = abs(dx * bx + dy * by + dz * bz)
        L = q[9]; r1 = q[10]; r2 = q[11]; T = q[12]; bend = q[13]; ridge = q[14]; lift = q[15]
        u = lx / L
        lz = lz - bend * L * u * u - lift * u  # curved / lifted toward tip
        # 2D uneven capsule (iq): circle r1 at (0,0), circle r2 at (L,0); here axis along x
        b = (r1 - r2) / L
        a = math.sqrt(max(1.0 - b * b, 1e-9))
        px = ly; py = lx  # iq formulation uses y as axis
        k = px * (-b) + py * a  # dot(p, vec2(-b,a))
        if k < 0.0:
            d2 = math.sqrt(px * px + py * py) - r1
        elif k > a * L:
            d2 = math.sqrt(px * px + (py - L) * (py - L)) - r2
        else:
            d2 = px * a + py * b - r1
        # thickness: thicker near rachis, thin at the edge; ridge along centre on top
        ru = max(min(u, 1.0), 0.0)
        wloc = r1 + (r2 - r1) * ru
        yy = min(ly / max(wloc, 1e-6), 1.0)
        top = T * (0.55 + 0.45 * (1.0 - yy * yy)) + ridge * math.exp(-(ly / (0.09 * wloc + 0.05)) ** 2)
        bot = T * 0.6
        if lz > 0:
            dzv = lz - top
        else:
            dzv = -lz - bot
        # smooth intersection (rounded edges)
        return _smax(d2, dzv, 0.35 * T)
    elif kind == 6:  # torus c(0:3) R rows(3:12) major r minor r (12,13) ; ring in local xy
        dx = x - q[0]; dy = y - q[1]; dz = z - q[2]
        lx = q[3] * dx + q[4] * dy + q[5] * dz
        ly = q[6] * dx + q[7] * dy + q[8] * dz
        lz = q[9] * dx + q[10] * dy + q[11] * dz
        qq = math.sqrt(lx * lx + ly * ly) - q[12]
        return math.sqrt(qq * qq + lz * lz) - q[13]
    return 1e9


@njit(parallel=True, fastmath=True)
def _apply(G, ox, oy, oz, h, kinds, params, boxes, op, ks):
    for n in range(kinds.shape[0]):
        i0 = boxes[n, 0]; i1 = boxes[n, 1]; j0 = boxes[n, 2]; j1 = boxes[n, 3]; k0 = boxes[n, 4]; k1 = boxes[n, 5]
        if i1 <= i0 or j1 <= j0 or k1 <= k0:
            continue
        kind = kinds[n]
        q = params[n]
        kk = ks[n]
        for i in prange(i0, i1):
            x = ox + i * h
            for j in range(j0, j1):
                y = oy + j * h
                for k in range(k0, k1):
                    z = oz + k * h
                    d = prim_dist(kind, q, x, y, z)
                    a = G[i, j, k]
                    if op == 0:
                        G[i, j, k] = _smin(a, d, kk)
                    elif op == 1:
                        G[i, j, k] = _smax(a, -d, kk)
                    elif op == 2:
                        G[i, j, k] = _smax(a, d, kk)
                    else:
                        G[i, j, k] = d


@njit(parallel=True, fastmath=True)
def _combine(A, B, op, k):
    nx, ny, nz = A.shape
    for i in prange(nx):
        for j in range(ny):
            for l in range(nz):
                a = A[i, j, l]; b = B[i, j, l]
                if op == 0:
                    A[i, j, l] = _smin(a, b, k)
                elif op == 1:
                    A[i, j, l] = _smax(a, -b, k)
                else:
                    A[i, j, l] = _smax(a, b, k)


def rot_rows(xaxis, yaxis=None, zaxis=None):
    """Return 9 numbers: rows = local x,y,z axes (orthonormalised)."""
    x = np.asarray(xaxis, float); x = x / np.linalg.norm(x)
    if yaxis is not None:
        y = np.asarray(yaxis, float); y = y - x * np.dot(x, y); y /= np.linalg.norm(y)
        z = np.cross(x, y)
    else:
        z = np.asarray(zaxis, float); z = z - x * np.dot(x, z); z /= np.linalg.norm(z)
        y = np.cross(z, x)
    return np.concatenate([x, y, z])


class Batch:
    """Collects primitives, then applies them to a Field."""

    def __init__(self):
        self.kinds = []; self.params = []; self.bounds = []; self.ks = []

    def _add(self, kind, prm, lo, hi, k):
        p = np.zeros(NPARAM); p[:len(prm)] = prm
        self.kinds.append(kind); self.params.append(p)
        self.bounds.append((np.asarray(lo, float), np.asarray(hi, float))); self.ks.append(k)

    def sphere(self, c, r, k=0.0):
        c = np.asarray(c, float)
        self._add(SPHERE, [*c, r], c - r, c + r, k)

    def ellipsoid(self, c, radii, xaxis=(1, 0, 0), yaxis=(0, 1, 0), k=0.0):
        c = np.asarray(c, float); R = rot_rows(xaxis, yaxis)
        m = max(radii)
        self._add(ELLIPSOID, [*c, *R, *radii], c - m, c + m, k)

    def rcone(self, a, b, ra, rb, k=0.0):
        a = np.asarray(a, float); b = np.asarray(b, float)
        lo = np.minimum(a - ra, b - rb); hi = np.maximum(a + ra, b + rb)
        self._add(RCONE, [*a, *b, ra, rb], lo, hi, k)

    def capsule(self, a, b, r, k=0.0):
        self.rcone(a, b, r, r, k)

    def tube(self, pts, radii, k=0.0, kseg=None):
        """Polyline of round cones (tapered tube)."""
        pts = np.asarray(pts, float); radii = np.broadcast_to(np.asarray(radii, float), (len(pts),))
        for i in range(len(pts) - 1):
            self.rcone(pts[i], pts[i + 1], radii[i], radii[i + 1], k if kseg is None else kseg)

    def rbox(self, c, half, xaxis=(1, 0, 0), yaxis=(0, 1, 0), rnd=0.0, k=0.0):
        c = np.asarray(c, float); R = rot_rows(xaxis, yaxis)
        m = np.linalg.norm(np.asarray(half) + rnd)
        self._add(RBOX, [*c, *R, *half, rnd], c - m, c + m, k)

    def eseg(self, a, b, up, w1, w2, t1, t2, k=0.0):
        a = np.asarray(a, float); b = np.asarray(b, float)
        up = np.asarray(up, float); t = b - a; t /= (np.linalg.norm(t) + 1e-12)
        up = up - t * np.dot(up, t); up /= np.linalg.norm(up)
        m1 = max(w1, t1); m2 = max(w2, t2)
        lo = np.minimum(a - m1, b - m2); hi = np.maximum(a + m1, b + m2)
        self._add(ESEG, [*a, *b, *up, w1, w2, t1, t2], lo, hi, k)

    def ribbon(self, pts, ups, widths, thicks, k=0.0, kseg=0.0):
        pts = np.asarray(pts, float); n = len(pts)
        ups = np.broadcast_to(np.asarray(ups, float), (n, 3)) if np.ndim(ups) == 1 else np.asarray(ups, float)
        widths = np.broadcast_to(np.asarray(widths, float), (n,)); thicks = np.broadcast_to(np.asarray(thicks, float), (n,))
        for i in range(n - 1):
            self.eseg(pts[i], pts[i + 1], (ups[i] + ups[i + 1]) / 2, widths[i], widths[i + 1], thicks[i], thicks[i + 1], k if i == 0 else max(kseg, 0.0))

    def feather(self, base, axis, normal, L, r1, r2, T, bend=0.0, ridge=0.0, lift=0.0, k=0.0):
        base = np.asarray(base, float); t = np.asarray(axis, float); t /= np.linalg.norm(t)
        n = np.asarray(normal, float); n = n - t * np.dot(n, t); n /= np.linalg.norm(n)
        tip = base + t * L
        m = max(r1, r2) + T + abs(bend) * L + abs(lift) + ridge
        lo = np.minimum(base, tip) - m; hi = np.maximum(base, tip) + m
        self._add(FEATHER, [*base, *t, *n, L, r1, r2, T, bend, ridge, lift], lo, hi, k)

    def torus(self, c, R, r, normal=(0, 0, 1), xaxis=None, k=0.0):
        c = np.asarray(c, float); n = np.asarray(normal, float); n /= np.linalg.norm(n)
        if xaxis is None:
            xaxis = np.cross(n, [0, 0, 1]) if abs(n[2]) < 0.9 else np.cross(n, [1, 0, 0])
        rows = rot_rows(xaxis, None, n)
        m = R + r
        self._add(TORUS, [*c, *rows, R, r], c - m, c + m, k)

    def __len__(self):
        return len(self.kinds)


class Field:
    def __init__(self, lo, hi, h):
        self.lo = np.asarray(lo, float); self.h = float(h)
        self.shape = tuple(int(math.ceil((hi[i] - lo[i]) / h)) + 1 for i in range(3))
        self.G = np.full(self.shape, FAR, dtype=np.float32)

    def blank(self):
        f = Field.__new__(Field); f.lo = self.lo; f.h = self.h; f.shape = self.shape
        f.G = np.full(self.shape, FAR, dtype=np.float32)
        return f

    def apply(self, batch, op='union', pad=None):
        if len(batch) == 0:
            return self
        opn = {'union': 0, 'sub': 1, 'inter': 2, 'set': 3}[op]
        kinds = np.array(batch.kinds, np.int64); params = np.array(batch.params, np.float64)
        ks = np.array(batch.ks, np.float64)
        boxes = np.zeros((len(batch), 6), np.int64)
        for n, (lo, hi) in enumerate(batch.bounds):
            p = (pad if pad is not None else 0.0) + ks[n] + 2.5 * self.h
            a = np.floor((lo - p - self.lo) / self.h).astype(int)
            b = np.ceil((hi + p - self.lo) / self.h).astype(int) + 1
            a = np.clip(a, 0, self.shape); b = np.clip(b, 0, self.shape)
            boxes[n] = (a[0], b[0], a[1], b[1], a[2], b[2])
        if op == 'inter':  # intersection must touch whole grid
            boxes[:] = (0, self.shape[0], 0, self.shape[1], 0, self.shape[2])
        _apply(self.G, self.lo[0], self.lo[1], self.lo[2], self.h, kinds, params, boxes, opn, ks)
        return self

    def combine(self, other, op='union', k=0.0):
        _combine(self.G, other.G, {'union': 0, 'sub': 1, 'inter': 2}[op], float(k))
        return self

    def coords(self):
        return [self.lo[i] + np.arange(self.shape[i]) * self.h for i in range(3)]

    def mesh(self, level=0.0, step=1):
        from skimage.measure import marching_cubes
        G = self.G
        # force closed surface at the grid border
        G[0, :, :] = FAR; G[-1, :, :] = FAR; G[:, 0, :] = FAR; G[:, -1, :] = FAR; G[:, :, 0] = FAR; G[:, :, -1] = FAR
        v, f, n, _ = marching_cubes(G, level=level, spacing=(self.h,) * 3, step_size=step, allow_degenerate=False)
        v += self.lo
        return v.astype(np.float32), f.astype(np.int32)


def save_ply(path, v, f):
    v = np.ascontiguousarray(v, np.float32); f = np.ascontiguousarray(f, np.int32)
    with open(path, 'wb') as fh:
        fh.write((f"ply\nformat binary_little_endian 1.0\nelement vertex {len(v)}\n"
                  "property float x\nproperty float y\nproperty float z\n"
                  f"element face {len(f)}\nproperty list uchar int vertex_indices\nend_header\n").encode())
        fh.write(v.tobytes())
        rec = np.zeros(len(f), dtype=[('n', 'u1'), ('i', '<i4', (3,))])
        rec['n'] = 3; rec['i'] = f
        fh.write(rec.tobytes())


def save_stl(path, v, f):
    v = np.asarray(v, np.float32); f = np.asarray(f, np.int64)
    tri = v[f]
    nrm = np.cross(tri[:, 1] - tri[:, 0], tri[:, 2] - tri[:, 0])
    nrm /= (np.linalg.norm(nrm, axis=1, keepdims=True) + 1e-20)
    rec = np.zeros(len(f), dtype=[('n', '<f4', (3,)), ('v', '<f4', (3, 3)), ('a', '<u2')])
    rec['n'] = nrm; rec['v'] = tri
    with open(path, 'wb') as fh:
        fh.write(b'Angel jewelry dish'.ljust(80, b' '))
        fh.write(np.uint32(len(f)).tobytes())
        fh.write(rec.tobytes())


# ---------------------------------------------------------------- curve helpers
def catmull(pts, n=None, per=8, closed=False):
    """Centripetal-ish Catmull-Rom through pts -> dense polyline."""
    P = np.asarray(pts, float)
    if closed:
        P = np.vstack([P[-1], P, P[0], P[1]])
    else:
        P = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, per, endpoint=False):
            t2 = t * t; t3 = t2 * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(P[-2])
    out = np.array(out)
    if n is not None:
        out = resample(out, n)
    return out


def resample(poly, n):
    poly = np.asarray(poly, float)
    seg = np.linalg.norm(np.diff(poly, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    t = np.linspace(0, s[-1], n)
    return np.stack([np.interp(t, s, poly[:, i]) for i in range(poly.shape[1])], 1)


def bezier(ctrl, n=50):
    ctrl = np.asarray(ctrl, float); t = np.linspace(0, 1, n)[:, None, None]
    P = np.repeat(ctrl[None], n, 0)
    for r in range(1, len(ctrl)):
        P = (1 - t) * P[:, :-1] + t * P[:, 1:]
    return P[:, 0]
