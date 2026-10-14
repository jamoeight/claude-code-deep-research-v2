"""Helper: pixel <-> 3D for the reference camera."""
import numpy as np, cam
loc, fwd, right, up = cam.frame(); C = cam.load()
W, H = C['w'], C['h']; f = C['lens'] / 36.0 * W
def ray(u, v):
    dx = (u - W / 2) / f; dy = -(v - H / 2) / f
    d = fwd + dx * right + dy * up; return d / np.linalg.norm(d)
def at_z(u, v, z):
    d = ray(u, v); s = (z - loc[2]) / d[2]; return loc + s * d
def at_y(u, v, y):
    d = ray(u, v); s = (y - loc[1]) / d[1]; return loc + s * d
def at_x(u, v, x):
    d = ray(u, v); s = (x - loc[0]) / d[0]; return loc + s * d
def px(P):
    return cam.project(np.atleast_2d(P))
