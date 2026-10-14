"""2D layout overlay of the right/left wing relief over the photo (wings agent tool).
   python3 wings_ov.py right|left out.png [box]"""
import sys, os
import numpy as np
os.environ.setdefault('WINGS_ONLY', 'right')
import wings
from wings_dbg import overlay
from sdf import Field


class _F:  # fake field with h for detail gating
    h = float(os.environ.get('OV_H', '0.45'))


side = sys.argv[1]; out = sys.argv[2]
box = tuple(int(x) for x in sys.argv[3].split(',')) if len(sys.argv) > 3 else None
S, rel = (wings.build_right if side == 'right' else wings.build_left)(_F())
overlay(S, rel, out, box=box)
print('ok', out)
