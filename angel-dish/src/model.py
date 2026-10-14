"""Assemble the angel dish.
   python3 model.py out/name.ply [h] [--parts dish,figure,head,wings]
Each component module exposes component(F) which fills a blank Field and returns it.
Blend radii between components are defined here (owned by the integrator)."""
import sys, time, importlib
import numpy as np
from sdf import Field, Batch, save_ply, save_stl

LO = (-90, -66, -1.0)
HI = (96, 54, 124)
PARTS = ['dish', 'figure', 'head', 'wings']
# (part, blend radius used when union-ing into the running result)
BLEND = {'dish': 0.0, 'figure': 3.0, 'head': 1.2, 'wings': 1.5}


def build(h=0.6, parts=PARTS, verbose=True, lo=None, hi=None):
    t0 = time.time()
    log = (lambda *a: print(f'[{time.time() - t0:6.1f}s]', *a, flush=True)) if verbose else (lambda *a: None)
    F = Field(lo or LO, hi or HI, h)
    first = True
    for p in PARTS:
        if p not in parts:
            continue
        mod = importlib.import_module(p if p != 'dish' else 'dish')
        G = mod.component(F.blank())
        if first:
            F = G; first = False
        else:
            F.combine(G, 'union', BLEND[p])
        del G
        log(p)
    floor = Batch(); floor.rbox((0, 0, -400), (400, 400, 400))
    F.apply(floor, 'sub')
    return F


if __name__ == '__main__':
    out = sys.argv[1]
    h = float(sys.argv[2]) if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else 0.6
    parts = PARTS
    if '--parts' in sys.argv:
        parts = sys.argv[sys.argv.index('--parts') + 1].split(',')
    lo = hi = None
    if '--box' in sys.argv:
        b = [float(x) for x in sys.argv[sys.argv.index('--box') + 1].split(',')]
        lo, hi = tuple(b[:3]), tuple(b[3:])
    F = build(h, parts, lo=lo, hi=hi)
    v, f = F.mesh()
    print('mesh', len(v), len(f))
    (save_stl if out.endswith('.stl') else save_ply)(out, v, f)
