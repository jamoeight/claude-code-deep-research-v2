"""Pose study: project head-local features for candidate poses (head agent tool)."""
import sys, math
import numpy as np
import cam
from head_pose import Pose
CAP_C = np.array([-0.3, -1.8, 1.6]); CAP_R = np.array([6.7, 7.6, 8.2])
FEAT = {'nose': (0, 6.92, -2.5), 'chin': (0, 5.6, -7.4), 'mouth': (0, 6.4, -4.8), 'eyeR': (-2.15, 4.8, 0.0), 'eyeL': (2.15, 4.8, 0.0),
        'brow': (0, 5.4, 1.2)}
PHOTO = {'nose': (471, 228), 'chin': (469, 255), 'mouth': (468, 242)}
def report(O, turn, pitch, roll):
    ps = Pose(O, turn, pitch, roll)
    out = {}
    for k, v in FEAT.items():
        w = ps.P(v); out[k] = cam.project(w)[0]
    # silhouette top of the hair cap
    th = np.radians(np.linspace(-90, 90, 91)); ph = np.radians(np.linspace(-180, 180, 181))
    T, Ph = np.meshgrid(th, ph)
    L = CAP_C + CAP_R * np.stack([np.cos(T) * np.sin(Ph), np.cos(T) * np.cos(Ph), np.sin(T)], -1).reshape(-1, 3)
    uv = cam.project(ps.P(L))
    i = np.argmin(uv[:, 1]); out['top'] = uv[i]
    out['topW'] = ps.P(L[i])
    out['chinW'] = ps.P(FEAT['chin'])
    return out
if __name__ == '__main__':
    O = np.array([float(x) for x in sys.argv[1].split(',')]); t, p, r = (float(x) for x in sys.argv[2:5])
    o = report(O, t, p, r)
    for k, v in o.items():
        print(k, np.round(v, 1))
    e = 0.5 * (o['eyeR'] + o['eyeL'])
    print('eye mid', e.round(1), ' nose-chin/eye-chin %.2f' % ((o['chin'][1] - o['nose'][1]) / (o['chin'][1] - e[1])))
    print('nose x frac from far eye: %.2f' % ((o['eyeL'][0] - o['nose'][0]) / (o['eyeL'][0] - o['eyeR'][0])))


def fit(O0, t, p, r, target=None):
    from scipy.optimize import least_squares
    target = target or {'eyeM': (466, 204.5), 'nose': (471, 228), 'mouth': (469, 242), 'chin': (468, 256), 'top': (442, 123.5)}
    loc, fwd, right, up = cam.frame()
    def res(q):
        O = np.asarray(O0) + q[0] * right + q[1] * up
        o = report(O, t, p, r); o['eyeM'] = 0.5 * (o['eyeR'] + o['eyeL'])
        return np.concatenate([o[k] - np.array(v) for k, v in target.items()])
    s = least_squares(res, [0, 0])
    O = np.asarray(O0) + s.x[0] * right + s.x[1] * up
    return O, res(s.x).reshape(-1, 2)
