"""Numpy projection identical to the Blender 'ref' camera, plus compare-image tools."""
import json, math, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))

def load():
    return json.load(open(os.path.join(HERE, 'camera.json')))

def frame(c=None):
    c = c or load()
    az, el = math.radians(c['az']), math.radians(c['el']); t = np.array(c['target'], float)
    loc = t + c['dist'] * np.array([math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)])
    fwd = t - loc; fwd /= np.linalg.norm(fwd)
    right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    return loc, fwd, right, up

def project(P, c=None):
    c = c or load(); loc, fwd, right, up = frame(c)
    P = np.atleast_2d(np.asarray(P, float)) - loc
    zc = P @ fwd; xc = P @ right; yc = P @ up
    W, H = c['w'], c['h']; f = c['lens'] / 36.0 * W
    u = W / 2 + f * xc / zc + c.get('shift_x', 0) * W
    v = H / 2 - f * yc / zc - c.get('shift_y', 0) * W
    return np.stack([u, v], 1)

def unproject(uv, plane_y=None, depth_point=None, c=None):
    """Pixel -> 3D point on the plane y=plane_y (world)."""
    c = c or load(); loc, fwd, right, up = frame(c)
    W, H = c['w'], c['h']; f = c['lens'] / 36.0 * W
    u, v = uv
    dx = (u - W / 2 - c.get('shift_x', 0) * W) / f; dy = -(v - H / 2 + c.get('shift_y', 0) * W) / f
    d = fwd + dx * right + dy * up
    s = (plane_y - loc[1]) / d[1]
    return loc + s * d
