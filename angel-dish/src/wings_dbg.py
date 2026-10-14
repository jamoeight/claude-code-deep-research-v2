"""Debug helpers for wings: project a relief layout onto the reference photo (no Blender)."""
import os, sys
import numpy as np
from PIL import Image, ImageDraw
from scipy.spatial import cKDTree
import cam

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, '..', 'ref', 'reference.png')


def pix2uv(sheet, ur, vr, pix, ds=0.3, pick='near', umin=-1e9, umax=1e9):
    U = np.arange(ur[0], ur[1], ds); V = np.arange(vr[0], vr[1], ds)
    uu, vv = np.meshgrid(U, V, indexing='ij'); uu = uu.ravel(); vv = vv.ravel()
    keep = (uu >= umin) & (uu <= umax); uu = uu[keep]; vv = vv[keep]
    P = sheet.P(uu, vv)
    q = cam.project(P)
    loc, fwd, _, _ = cam.frame()
    depth = (P - loc) @ fwd
    tr = cKDTree(q)
    out = []
    for p in np.atleast_2d(pix):
        ii = tr.query_ball_point(p, 2.5)
        if not ii:
            _, i = tr.query(p); ii = [i]
        ii = np.array(ii)
        j = ii[np.argmin(depth[ii])] if pick == 'near' else ii[np.argmax(depth[ii])]
        out.append((uu[j], vv[j]))
    return np.array(out)


def overlay(sheet, relief, path, box=None, step=0.3, alpha=0.55, light=(-0.55, 0.6, 0.75)):
    """Splat a shaded front-face relief + feather boundaries over the reference photo."""
    ref = Image.open(REF).convert('RGB')
    Wd, Ht = ref.size
    H = relief.final['f'][0]
    ID = relief.ID
    hr = relief.hr
    st = max(int(round(step / hr)), 1)
    Hs = H[::st, ::st]; IDs = ID[::st, ::st]
    iu = np.arange(0, H.shape[0], st); iv = np.arange(0, H.shape[1], st)
    uu, vv = np.meshgrid(relief.u0 + iu * hr, relief.v0 + iv * hr, indexing='ij')
    gu, gv = np.gradient(H, hr)
    gus = gu[::st, ::st]; gvs = gv[::st, ::st]
    m = Hs > 0.05
    u = uu[m]; v = vv[m]; h = Hs[m]
    nl = np.stack([-gus[m], -gvs[m], np.ones_like(h)], 1); nl /= np.linalg.norm(nl, axis=1, keepdims=True)
    L = np.asarray(light, float); L /= np.linalg.norm(L)
    sh = np.clip(nl @ L, 0, 1)
    # boundaries
    idm = IDs
    edge = np.zeros_like(idm, bool)
    edge[1:, :] |= idm[1:, :] != idm[:-1, :]
    edge[:, 1:] |= idm[:, 1:] != idm[:, :-1]
    e = edge[m]
    P = sheet.P(u, v)
    eps = 0.05
    Pu = (sheet.P(u + eps, v) - sheet.P(u - eps, v)); Pv = (sheet.P(u, v + eps) - sheet.P(u, v - eps))
    n = np.cross(Pu, Pv); n /= np.linalg.norm(n, axis=1, keepdims=True)
    nx, ny = sheet.nrm_xy(u)
    sg = np.sign(n[:, 0] * nx + n[:, 1] * ny); n *= sg[:, None]
    X = P + n * h[:, None]
    q = cam.project(X)
    loc, fwd, _, _ = cam.frame()
    depth = (X - loc) @ fwd
    img = np.array(ref).astype(np.float32)
    shade = np.zeros((Ht, Wd), np.float32); zb = np.full((Ht, Wd), 1e9, np.float32); eb = np.zeros((Ht, Wd), bool)
    xi = np.round(q[:, 0]).astype(int); yi = np.round(q[:, 1]).astype(int)
    order = np.argsort(-depth)       # far first, near overwrite
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            x = xi[order] + dx; y = yi[order] + dy
            ok = (x >= 0) & (x < Wd) & (y >= 0) & (y < Ht)
            shade[y[ok], x[ok]] = sh[order][ok]
            zb[y[ok], x[ok]] = depth[order][ok]
            eb[y[ok], x[ok]] = e[order][ok] if (dx == 0 and dy == 0) else eb[y[ok], x[ok]]
    cov = zb < 1e8
    out_s = img.copy()
    col = np.stack([0.25 + 0.75 * shade] * 3, -1) * np.array([235, 170, 165])
    out_s[cov] = col[cov]
    out_b = img.copy()
    out_b[cov] = (1 - alpha) * img[cov] + alpha * col[cov]
    out_b[eb] = [0, 255, 255]
    A = Image.fromarray(out_s.clip(0, 255).astype(np.uint8)); B = Image.fromarray(out_b.clip(0, 255).astype(np.uint8))
    if box:
        A = A.crop(box); B = B.crop(box); R = ref.crop(box)
    else:
        R = ref
    s = min(1.0, 2400 / (3 * R.width))
    sz = (int(R.width * s), int(R.height * s))
    o = Image.new('RGB', (sz[0] * 3, sz[1]))
    for i, im in enumerate((R, B, A)):
        o.paste(im.resize(sz, Image.LANCZOS), (i * sz[0], 0))
    o.save(path)
    return path
