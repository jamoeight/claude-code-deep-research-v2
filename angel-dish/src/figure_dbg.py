"""Debug: ref-camera depth difference (displaced - base) and the texture D map, side by side."""
import sys, os
import numpy as np
from PIL import Image
import model, figure, figure_folds as FD, figure_tex as TXM
from sdf import Field, Batch
import figure_rc as rc, figure_skirt as SK
h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.45
F = Field(model.LO, model.HI, h).blank()
sl, lo = figure.block_slices(F)
F.apply(rc.merge(figure.torso(), figure.legs()), pad=3.0)
Gb = F.G[sl]
xs, ys, zs = [lo[i] + np.arange(Gb.shape[i]) * F.h for i in range(3)]
kz = int(np.searchsorted(zs, 46.0))
Gs, _ = SK.sdf_block(xs, ys, zs[:kz], F.h)
Gb[:, :, :kz] = figure._smin_np(Gb[:, :, :kz], Gs, 3.0)
G0 = Gb.copy()
T = FD.apply_all(G0, Gb, lo, h, False)
T2 = TXM.CamTex(T.c, (T.u0, T.v0, T.u0 + T.nu / T.ts, T.v0 + T.nv / T.ts), T.ts, np.ascontiguousarray(Gb), lo, h)
loc = np.asarray(T.c['loc'])
d0 = np.linalg.norm(T.X - loc, axis=2); d1 = np.linalg.norm(T2.X - loc, axis=2)
diff = np.nan_to_num(d0 - d1, nan=0.0)
def col(a, s):
    a = np.clip(a / s, -1, 1)
    im = np.zeros(a.shape + (3,), np.uint8)
    im[..., 0] = (128 + 127 * np.clip(a, 0, 1)).astype(np.uint8); im[..., 2] = (128 - 127 * np.clip(a, -1, 0)).astype(np.uint8)
    im[..., 1] = 128 - (60 * np.abs(a)).astype(np.uint8)
    return im
A = col(diff, 3.0); B = col(T.D, 3.0)
o = np.concatenate([A, B], 1)
Image.fromarray(o).save(sys.argv[1])
print('diff range', diff.min(), diff.max(), 'D range', T.D.min(), T.D.max())
