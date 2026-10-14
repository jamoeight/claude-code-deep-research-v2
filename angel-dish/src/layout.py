"""Shared key points (design units ~ mm; final STL is scaled by EXPORT_SCALE).
X = viewer's right, Y = away from viewer, Z = up. Table at z=0.
"Her right" = viewer's left (-X).
"""
import numpy as np

EXPORT_SCALE = 1.2          # design width ~155 -> ~186 mm real

H = 16.0                    # head height (chin to crown)

# figure skeleton (world)
PELVIS = np.array([-18.0, 22.0, 30.0])
WAIST = np.array([-18.0, 22.5, 44.0])
CHEST = np.array([-17.5, 22.0, 58.0])
NECK_BASE = np.array([-17.0, 22.5, 71.0])
HEAD_C = np.array([-14.5, 20.0, 86.0])         # centre of cranium-ish
SHOULDER_R = np.array([-30.5, 23.0, 68.5])      # her right (viewer left)
SHOULDER_L = np.array([-4.0, 22.0, 68.5])
# wings attach on the upper back
WING_ROOT_R = np.array([-25.0, 30.0, 66.0])    # viewer's left wing root
WING_ROOT_L = np.array([-9.0, 30.0, 66.0])     # viewer's right wing root

# dish
DISH_C = np.array([2.0, -4.0])
FLOOR_Z = 7.0
