"""Head pose: local frame (x = her left, y = face forward, z = up; origin = skull centre at eye level)
mapped to world.  Shared by head.py and the fitting / debug scripts."""
import math
import numpy as np


def rot_matrix(turn, pitch, roll):
    """Columns = world directions of local x, y, z."""
    t, p, r = (math.radians(a) for a in (turn, pitch, roll))
    # roll about local forward (y): top (z) tilts toward +x (her left)
    Rr = np.array([[math.cos(r), 0, math.sin(r)], [0, 1, 0], [-math.sin(r), 0, math.cos(r)]])
    # pitch about local x: forward (y) tilts down
    Rp = np.array([[1, 0, 0], [0, math.cos(p), math.sin(p)], [0, -math.sin(p), math.cos(p)]])
    M0 = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]], float)  # local -> world unrotated (face looks to -Y)
    Rt = np.array([[math.cos(t), -math.sin(t), 0], [math.sin(t), math.cos(t), 0], [0, 0, 1]])
    return Rt @ M0 @ Rp @ Rr


class Pose:
    def __init__(self, O, turn, pitch, roll):
        self.O = np.asarray(O, float); self.R = rot_matrix(turn, pitch, roll)
        self.turn, self.pitch, self.roll = turn, pitch, roll

    def P(self, x, y=None, z=None):
        p = np.asarray(x if y is None else (x, y, z), float)
        return self.O + p @ self.R.T

    def D(self, x, y=None, z=None):
        d = np.asarray(x if y is None else (x, y, z), float)
        return d @ self.R.T

    def to_local(self, pw):
        return (np.asarray(pw, float) - self.O) @ self.R


if __name__ == '__main__':
    R = rot_matrix(30, 0, 0)
    print('fwd', R[:, 1], 'left', R[:, 0], 'up', R[:, 2])
    R = rot_matrix(0, 20, 0); print('pitch fwd', R[:, 1])
    R = rot_matrix(0, 0, 10); print('roll up', R[:, 2])
