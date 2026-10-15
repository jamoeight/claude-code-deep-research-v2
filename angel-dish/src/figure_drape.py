"""Solid drapery folds for the figure's gown (helper for figure.py) -- round 3.

Large satin folds are real volume, not a displacement texture: each fold is a soft band with a flattened
elliptical section lying on the base surface (crest `hgt` above it, half-width `w`, tapered in height AND width at
both ends), hard-unioned along its length (no beading) and then smooth-unioned into the gown with a wide blend
(k ~2), so its flanks fillet into the cloth.  `lean` tilts the section toward one side (steep / undercut flank on
that side, gentle ramp on the other).  Recesses (pockets / valleys between heavy folds) are the same band
subtracted.  Paths are traced on the reference photo (pixel polylines ray-cast onto the base surface) or given in
3D for the sides the photo does not show.
"""
import math
import numpy as np
from sdf import Batch, Field, catmull, resample, FAR
import figure_tex as TXM


def FB(pix=None, p3=None, w=3.0, hgt=2.0, t=None, ta=0.3, tb=0.3, lean=0.0, k=2.0, wend=0.45, off=0.0, sub=False, floor=False):
    return dict(pix=pix, p3=p3, w=w, hgt=hgt, t=t, ta=ta, tb=tb, lean=lean, k=k, wend=wend, off=off, sub=sub, floor=floor)


def CH(pix=None, p3=None, w=1.8, depth=1.5, t=None, ta=0.3, tb=0.3, lean=0.0, k=1.4, wend=0.5):
    return dict(pix=pix, p3=p3, w=w, hgt=depth, t=t, ta=ta, tb=tb, lean=lean, k=k, wend=wend, off=0.0, sub=True, floor=False)


def under(p3, d, n=(0.0, -1.0, 0.0)):
    """offset a 3D path by d (scalar or per point) sideways in the surface (+ = the side cross(n, tangent))."""
    P = np.asarray(p3, float); n = np.asarray(n, float)
    T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True)
    S = np.cross(n, T); S /= np.linalg.norm(S, axis=1, keepdims=True)
    d = np.broadcast_to(np.asarray(d, float), (len(P),))
    return [tuple(v) for v in (P + S * d[:, None])]


# ------------------------------------------------------------------ folds traced on the photo (ref camera px)
# her right hip: heavy vertical folds hanging below the hand, the outer one turning into the swag at the bottom
HIP = [
    FB([(355, 514), (353, 540), (354, 566), (359, 590), (370, 609), (390, 622), (414, 630)], w=[2.4, 2.8, 3.0, 3.0, 2.8, 2.6, 2.4],
       hgt=[1.6, 2.0, 2.2, 2.1, 1.8, 1.5, 1.0], ta=0.3, tb=0.35, lean=-0.1, k=2.0, wend=0.8),
    FB([(385, 504), (387, 532), (390, 560), (395, 586), (403, 606)], w=[1.8, 2.2, 2.4, 2.2, 2.0], hgt=[1.2, 1.6, 1.7, 1.4, 1.0],
       ta=0.35, tb=0.4, lean=0.0, k=1.8, wend=0.8),
]

# the swag between her right hip and the knee (round 3c2b): the lap cloth hangs as a big convex bag (lit top-left,
# turning down into shade) whose rounded bottom edge tucks under in a dark crease; the hem roll (HEM[0]) runs below it.
# (Lean sign: + = steep flank on cross(N, T): for a left->right path that is the UPPER side.)
SWAG = [
    FB([(376, 560), (402, 590), (438, 614), (476, 616), (506, 600), (530, 576)], w=[2.6, 4.0, 4.6, 4.6, 3.8, 2.4],
       hgt=[0.5, 1.3, 1.75, 1.75, 1.3, 0.5], t=[2.0, 3.0, 3.4, 3.4, 2.8, 1.8], ta=0.25, tb=0.3, lean=-0.5, k=1.2, wend=0.8),
]

# the fall off the knee (round 3c2): a few long separate falls (low, wide) with one bright crisp crease, a soft
# valley (not a cliff) left of it; the cloth spills off the knee into a big S-cowl lobe bulging right that curls back
# left under its lip, and two rolls run on right along the floor under the ring
KNEE = [
    FB([(552, 534), (547, 565), (542, 596), (537, 620), (533, 642)], w=[1.0, 1.4, 1.5, 1.4, 1.1], hgt=[0.3, 0.65, 0.75, 0.7, 0.4],
       ta=0.3, tb=0.35, lean=-0.6, k=0.7, wend=0.8),
    CH([(537, 540), (534, 572), (531, 604), (529, 636)], w=[1.0, 1.5, 1.5, 1.2], depth=[0.15, 0.4, 0.4, 0.2], ta=0.3, tb=0.35,
       k=1.5, wend=0.8),
    FB([(512, 588), (516, 614), (521, 640), (526, 664)], w=[1.6, 2.4, 2.6, 2.0], hgt=[0.2, 0.6, 0.7, 0.35], ta=0.35, tb=0.4,
       lean=0.1, k=1.4, wend=0.8),
    # an inner fold of the lobe
    FB([(572, 596), (590, 620), (603, 644), (606, 660)], w=[1.2, 1.7, 1.8, 1.3], hgt=[0.2, 0.55, 0.6, 0.25], ta=0.35, tb=0.4,
       lean=-0.2, k=1.2, wend=0.8),
    # crease under the cowl's lip
    CH([(620, 677), (606, 687), (590, 692), (574, 693)], w=[0.9, 1.2, 1.1, 0.7], depth=[0.2, 0.5, 0.4, 0.1],
       ta=0.3, tb=0.35, k=1.4, wend=0.8),
    # rolls running right along the floor under the ring
    FB([(575, 702), (602, 706), (632, 708), (664, 704), (694, 697)], w=[1.8, 2.4, 2.6, 2.3, 1.6], hgt=[0.5, 1.0, 1.15, 0.9, 0.35],
       ta=0.25, tb=0.4, lean=-0.15, k=1.5, wend=0.8),
    FB([(590, 722), (622, 725), (656, 721), (690, 713)], w=[1.8, 2.3, 2.3, 1.6], hgt=[0.45, 0.9, 0.85, 0.3], ta=0.3, tb=0.4,
       lean=-0.15, k=1.5, wend=0.8),
]

# the companion fold below the hip toward the swag
SEC = [
    FB([(370, 640), (395, 656), (425, 668)], w=[1.2, 1.6, 1.3], hgt=[0.5, 0.9, 0.5], ta=0.4, tb=0.45, lean=0.1, k=1.4, wend=0.8),
]

# lower skirt: stacked rolls sweeping from the knee side toward the front-left onto the floor (S-curved, uneven),
# with soft troughs between them
HEM = [
    FB([(584, 650), (558, 662), (522, 671), (474, 677), (424, 672), (372, 662), (318, 654), (290, 652)],
       w=[1.8, 2.4, 2.8, 2.7, 2.6, 2.7, 2.4, 2.0], hgt=[0.6, 1.2, 1.6, 1.5, 1.4, 1.5, 1.3, 0.9], ta=0.4, tb=0.3,
       lean=0.1, k=1.5, wend=0.8),
    FB([(566, 690), (528, 693), (482, 696), (432, 690), (384, 680), (336, 672), (300, 669)],
       w=[1.4, 1.9, 2.2, 2.1, 2.0, 1.8, 1.5], hgt=[0.4, 0.9, 1.2, 1.1, 1.0, 0.9, 0.6], ta=0.35, tb=0.35, lean=0.1, k=1.4, wend=0.8),
    FB([(596, 706), (548, 714), (488, 718), (428, 711), (372, 699), (318, 691), (284, 689)],
       w=[2.0, 2.6, 3.0, 3.0, 2.7, 2.5, 2.1], hgt=[1.0, 1.6, 1.9, 1.9, 1.7, 1.4, 0.9], ta=0.3, tb=0.35, lean=0.15, k=1.5, wend=0.8),
]

# the lap (round 3c2): three long broad tension folds from her right hip across the thigh toward the knee, each with a
# gentle upper flank, a crisp crest and a steep lower flank ending in a thin crease; smooth planes between them
LAP = [
    FB([(440, 468), (466, 484), (494, 502), (521, 520), (545, 535)], w=[1.6, 2.4, 2.8, 2.6, 1.8], hgt=[0.4, 1.05, 1.3, 1.15, 0.45],
       ta=0.3, tb=0.35, lean=-0.5, k=1.0, wend=0.8),
    FB([(408, 506), (438, 526), (469, 546), (500, 563), (530, 580)], w=[1.8, 2.7, 3.1, 2.9, 2.0], hgt=[0.45, 1.2, 1.5, 1.3, 0.5],
       ta=0.3, tb=0.35, lean=-0.5, k=1.1, wend=0.8),
    FB([(400, 540), (425, 558), (450, 575), (475, 593), (498, 610)], w=[1.6, 2.4, 2.7, 2.5, 1.7], hgt=[0.35, 0.9, 1.1, 1.0, 0.4],
       ta=0.3, tb=0.35, lean=-0.45, k=1.0, wend=0.8),
]
LAPCH = []     # (round 3c2b) no carved creases: the steep flanks with a small blend make the shadow lines

# the bodice (round 3c2): all 3D (laid with T.surf, no camera-space ray-casts near the silhouette / grazing neck):
# rolled V-neck edges, armhole edge, one soft under-bust valley, and two long diagonal wrap folds from under her left
# breast down across the waist to her right hip (started well inside the contour; gentle upper flank, steep lower
# flank with a thin crease below)
BOD = [
    # (round 3c3) the neckline / straps / armhole are crisp cloth edges (figure_cloth); here only the satin's diagonal
    # tension folds, pulled from her left bust side down-left across the waist toward her right hip (traced on the
    # photo; irregular spacing / lengths; gentle upper flank, steeper lower flank)
    FB([(499, 371), (489, 389), (477, 410), (461, 434), (446, 457)], w=[0.9, 1.3, 1.45, 1.35, 1.0],
       hgt=[0.20, 0.57, 0.68, 0.61, 0.27], ta=0.25, tb=0.35, lean=0.45, k=0.8, wend=0.8),
    FB([(493, 405), (484, 422), (471, 444), (456, 468), (443, 488)], w=[0.9, 1.25, 1.4, 1.3, 0.9],
       hgt=[0.16, 0.51, 0.62, 0.54, 0.20], ta=0.3, tb=0.35, lean=0.45, k=0.8, wend=0.8),
    # the wrap: the top lapel's edge carries on past the V bottom, softly across her right breast (no bare dome)
    FB([(467, 363), (452, 371), (436, 379), (419, 388), (401, 398)], w=[0.8, 1.15, 1.3, 1.15, 0.8],
       hgt=[0.12, 0.3, 0.36, 0.3, 0.1], ta=0.2, tb=0.35, lean=0.45, k=0.8, wend=0.75),
    FB([(474, 373), (457, 391), (439, 408), (420, 425), (403, 440)], w=[0.8, 1.1, 1.25, 1.1, 0.8],
       hgt=[0.14, 0.41, 0.49, 0.41, 0.14], ta=0.3, tb=0.4, lean=0.4, k=0.8, wend=0.8),
    FB([(486, 437), (476, 457), (463, 478), (449, 499)], w=[0.8, 1.15, 1.2, 0.9],
       hgt=[0.14, 0.43, 0.49, 0.16], ta=0.35, tb=0.4, lean=0.4, k=0.8, wend=0.8),
]
BOD3 = []
BODCH = [
    # soft under-bust valley on her right side (no engraved line)
    CH(p3=[(-25.6, 16.4, 61.4), (-24.0, 15.3, 59.9), (-22.0, 14.8, 59.0), (-19.8, 14.9, 58.3), (-17.6, 15.4, 58.1)],
       w=[0.7, 1.0, 1.1, 1.0, 0.7], depth=[0.1, 0.25, 0.3, 0.25, 0.08], ta=0.35, tb=0.4, k=1.0, wend=0.8),
]

# (round 3c3) the skirt as thin clinging satin: ~9 long narrow streamline ridges traced on the photo (high-pass of the
# reference), closely spaced (~3.5 apart), each with a gentle upper flank and a steeper outer / lower flank, tapered at
# both ends, rounded valleys between them.  On her right side they fall nearly straight down from below the hand, then
# sweep right along the floor as the train (the outer ones lowest); the inner ones sag between the hip and the knee and
# rise to the knee; over the thigh they run diagonally down to the knee; one falls off the knee to the floor.
# (lean -: steep flank on the lower / outer side for paths running down / right)
STREAM = [
    FB([(340, 524), (338, 560), (343, 600), (358, 640), (392, 671), (445, 693), (510, 705), (575, 707), (640, 701), (688, 693)],
       w=[1.0, 1.3, 1.45, 1.5, 1.6, 1.6, 1.55, 1.5, 1.35, 1.0], hgt=[0.38, 0.69, 0.83, 0.88, 0.90, 0.85, 0.88, 0.78, 0.62, 0.31],
       ta=0.12, tb=0.15, lean=-0.4, k=1.1, wend=0.7),
    FB([(364, 508), (361, 548), (366, 588), (382, 626), (414, 659), (466, 682), (528, 687), (588, 680), (646, 668)],
       w=[1.0, 1.3, 1.45, 1.5, 1.3, 1.15, 1.35, 1.3, 1.0], hgt=[0.38, 0.72, 0.82, 0.8, 0.55, 0.42, 0.66, 0.6, 0.3],
       ta=0.12, tb=0.18, lean=-0.4, k=1.1, wend=0.7),
    FB([(389, 497), (390, 536), (400, 572), (420, 602), (452, 622), (492, 630), (528, 625)],
       w=[0.9, 1.2, 1.35, 1.45, 1.4, 1.25, 0.9], hgt=[0.25, 0.52, 0.62, 0.66, 0.6, 0.45, 0.15],
       ta=0.15, tb=0.3, lean=-0.4, k=1.1, wend=0.7),
    # a short branch splitting off between the second and third falls (no evenly nested arcs)
    FB([(374, 588), (388, 614), (412, 636), (446, 651), (480, 655)], w=[0.7, 1.0, 1.15, 1.05, 0.7],
       hgt=[0.12, 0.36, 0.44, 0.36, 0.1], ta=0.25, tb=0.35, lean=-0.35, k=1.0, wend=0.7),
    # long diagonals from her right hip down across the lap toward the knee fall (uneven spacing / heights / bends)
    FB([(414, 488), (427, 519), (450, 551), (480, 577), (514, 597), (548, 611)], w=[0.9, 1.2, 1.4, 1.4, 1.25, 0.85],
       hgt=[0.2, 0.5, 0.64, 0.62, 0.5, 0.15], ta=0.15, tb=0.25, lean=-0.4, k=1.0, wend=0.7),
    FB([(432, 480), (456, 501), (483, 525), (511, 550), (536, 572)], w=[0.8, 1.1, 1.2, 1.1, 0.8],
       hgt=[0.15, 0.4, 0.46, 0.38, 0.12], ta=0.2, tb=0.3, lean=-0.35, k=1.0, wend=0.7),
    # over the thigh: diagonals from the waist down to the knee
    FB([(446, 461), (471, 475), (497, 493), (521, 512), (544, 531)], w=[0.9, 1.2, 1.3, 1.2, 0.9],
       hgt=[0.2, 0.45, 0.52, 0.45, 0.2], ta=0.2, tb=0.25, lean=-0.4, k=1.0, wend=0.7),
    FB([(474, 455), (497, 469), (519, 487), (538, 505)], w=[0.7, 1.0, 1.05, 0.7],
       hgt=[0.12, 0.32, 0.34, 0.12], ta=0.25, tb=0.3, lean=-0.35, k=0.9, wend=0.7),
    # off the knee down to the floor, sweeping right into the train
    FB([(548, 540), (558, 574), (568, 608), (584, 640), (610, 668), (648, 688), (684, 698)],
       w=[0.9, 1.25, 1.4, 1.45, 1.45, 1.3, 0.9], hgt=[0.2, 0.5, 0.6, 0.64, 0.6, 0.5, 0.2],
       ta=0.15, tb=0.2, lean=-0.4, k=1.1, wend=0.7),
    # (r3c3b) her right side: below the column the train sweeps left onto the bowl's left wall as two long rolls
    # (photo px 205-335, 610-720), uneven, tapering into the wall
    FB([(338, 614), (311, 630), (283, 645), (255, 658), (228, 669), (206, 675)], w=[1.8, 2.5, 2.8, 2.7, 2.4, 1.6],
       hgt=[0.3, 0.8, 0.95, 0.9, 0.7, 0.2], ta=0.3, tb=0.3, lean=-0.3, k=1.6, wend=0.7),
    FB([(338, 666), (307, 684), (277, 699), (249, 710), (223, 718)], w=[1.6, 2.2, 2.5, 2.3, 1.5],
       hgt=[0.25, 0.72, 0.85, 0.7, 0.2], ta=0.3, tb=0.3, lean=-0.3, k=1.6, wend=0.7),
    # the hem curling over off the knee (photo px 578-640, 556-670): a hooked rolled edge, steep / shadowed outer flank
    FB([(578, 556), (596, 578), (612, 602), (622, 628), (621, 652), (609, 667), (594, 671)],
       w=[1.0, 1.4, 1.6, 1.65, 1.55, 1.3, 0.9], hgt=[0.2, 0.5, 0.62, 0.66, 0.6, 0.45, 0.15],
       ta=0.15, tb=0.25, lean=0.15, k=1.3, wend=0.7),      # (r3c3b: small lean -- no thin overhanging lip)
]

SKIRT_GAIN = 1.3      # (round 3c2b) the skirt satin needs bolder relief than the bodice to read in the photo's light
for _sp in STREAM:
    _sp['gain'] = SKIRT_GAIN
PX = BOD + STREAM

# ------------------------------------------------------------------ 3D folds (sides / back / floor the photo hides)
# back of the gown: five broad falls fanning from the small of the back / hips down to the floor (uneven widths,
# heights and spacing), rounded cushions blended into the cloth
BACK = [
    FB(p3=[(-24.5, 30.5, 45), (-28, 33, 36), (-31, 35.5, 27), (-33, 35.5, 18)], w=[1.6, 2.2, 2.4, 2.2], hgt=[0.8, 1.4, 1.7, 1.3],
       ta=0.35, tb=0.4, lean=0.15, k=2.0, wend=0.8),
    FB(p3=[(-20, 31, 46), (-21, 35, 35), (-22.5, 38.5, 26), (-23.5, 37.5, 16)], w=[1.8, 2.4, 2.6, 2.4], hgt=[0.9, 1.6, 1.9, 1.4],
       ta=0.35, tb=0.4, lean=-0.1, k=2.0, wend=0.8),
    FB(p3=[(-16, 31, 44), (-15.5, 35.5, 35), (-15, 39, 26), (-14.5, 37.5, 16)], w=[1.4, 1.9, 2.1, 1.9], hgt=[0.7, 1.2, 1.4, 1.1],
       ta=0.4, tb=0.4, lean=0.1, k=1.8, wend=0.8),
    FB(p3=[(-12, 31, 42), (-9.5, 34.5, 34), (-7, 37.5, 26), (-5, 36.5, 17)], w=[1.7, 2.3, 2.5, 2.2], hgt=[0.8, 1.5, 1.8, 1.3],
       ta=0.35, tb=0.4, lean=-0.15, k=2.0, wend=0.8),
    FB(p3=[(-7, 30, 39), (-3, 31, 32), (0.5, 33, 25), (3, 33.5, 17)], w=[1.4, 2.0, 2.2, 1.9], hgt=[0.6, 1.2, 1.4, 1.0],
       ta=0.4, tb=0.4, lean=-0.1, k=1.8, wend=0.8),
]

# the hem flaring out on the floor toward the front-left (her right side): broad rolls sweeping out from the skirt
# foot and dying into the bowl floor (dish floor z ~7.6-8)
FLOOR = [
    FB(p3=[(-14, 0.5, 7.7), (-23, -2.5, 7.7), (-32, -6, 7.8), (-39, -10.5, 8.0), (-44, -15.5, 8.6)], w=[2.6, 2.8, 2.6, 2.3, 1.9],
       hgt=[1.6, 2.0, 1.8, 1.4, 0.8], ta=0.25, tb=0.45, lean=0.2, k=2.0, wend=0.8, floor=True),
    FB(p3=[(-22, 6, 7.8), (-30, 3.5, 7.8), (-37, 0.5, 7.9), (-43, -3, 8.4)], w=[2.4, 2.6, 2.3, 1.8], hgt=[1.6, 1.8, 1.4, 0.7],
       ta=0.3, tb=0.45, lean=0.2, k=2.0, wend=0.8, floor=True),
    FB(p3=[(-3, -3.5, 7.6), (-12, -7.5, 7.6), (-22, -11, 7.6), (-31, -14.5, 7.7), (-37, -19, 8.2)], w=[2.2, 2.4, 2.3, 2.0, 1.6],
       hgt=[1.2, 1.5, 1.4, 1.1, 0.6], ta=0.3, tb=0.45, lean=0.15, k=2.0, wend=0.8, floor=True),
]

# her right side: the long hem roll continues past the hip foot, sweeping left and up onto the bowl's left wall
# (photo px 220-330, 590-650), with a lower roll under it near the floor
SIDE = [
    FB(p3=[(-37.0, 11.5, 22.0), (-41.5, 13.0, 23.0), (-46, 14.0, 23.5), (-50, 13.5, 22.5), (-53, 11.0, 20.0)],
       w=[2.4, 2.7, 2.9, 2.7, 2.2], hgt=[1.4, 1.9, 2.1, 1.8, 1.0], t=[3.4, 4.4, 5.4, 5.8, 5.4], ta=0.25, tb=0.35, lean=0.2,
       k=1.8, wend=0.85, floor=True),
    FB(p3=[(-38, 8.5, 18.0), (-42.5, 9.8, 18.6), (-47, 10.2, 18.6), (-51.5, 9.0, 17.6), (-54.0, 7.0, 16.0)],
       w=[2.0, 2.4, 2.5, 2.3, 1.8], hgt=[1.1, 1.6, 1.7, 1.4, 0.7], t=[2.8, 3.5, 4.0, 4.0, 3.6], ta=0.3, tb=0.35, lean=0.2,
       k=1.6, wend=0.85, floor=True),
    FB(p3=[(-39, 5.0, 14.0), (-43.5, 6.0, 14.5), (-47.5, 6.5, 14.6), (-51.0, 6.5, 14.2), (-54.5, 5.0, 13.2)], w=[2.2, 2.6, 2.5, 2.3, 1.8],
       hgt=[1.2, 1.7, 1.6, 1.3, 0.7], t=[3.0, 3.8, 4.2, 4.2, 4.0], ta=0.3, tb=0.35, lean=0.2, k=1.8, wend=0.85, floor=True),
]

# the outer side of the knee (her left knee side, seen from the right): long folds fanning down off the knee to the
# floor, uneven spacing, soft troughs between
KSIDE = [
    # (round 3c2: the first side fold is replaced by the 3D cowl lobe -- figure.cowl)
    FB(p3=[(5.5, 7.5, 30.5), (9.0, 8.5, 24.5), (12.0, 9.5, 18.0), (14.5, 10.0, 12.0)], w=[1.1, 1.6, 1.9, 1.6],
       hgt=[0.35, 0.8, 1.0, 0.6], ta=0.3, tb=0.4, lean=0.15, k=1.1, wend=0.8),
    FB(p3=[(6.0, 13.0, 27.5), (9.5, 14.5, 21.5), (12.5, 16.0, 15.5), (14.5, 17.0, 11.0)], w=[1.1, 1.7, 2.0, 1.6],
       hgt=[0.35, 0.9, 1.1, 0.6], ta=0.3, tb=0.4, lean=0.1, k=1.1, wend=0.8),
    FB(p3=[(4.0, 19.5, 24.5), (7.0, 21.0, 19.5), (9.5, 22.5, 14.5), (11.0, 23.5, 10.5)], w=[1.0, 1.5, 1.7, 1.4],
       hgt=[0.3, 0.7, 0.85, 0.5], ta=0.3, tb=0.4, lean=0.1, k=1.1, wend=0.8),
]

# shoulder straps of the chiton (3D, over the shoulder tops into the back)
STRAP = []     # (round 3c3) straps are part of the cloth layer (figure_cloth)

D3 = BACK + FLOOR + STRAP + KSIDE + BOD3 + BODCH     # (r3c3b: SIDE floor rolls replaced by traced rolls in STREAM)


def _env(m, ta, tb):
    s = np.linspace(0, 1, m)
    e = np.minimum(np.clip(s / max(ta, 1e-6), 0, 1), np.clip((1 - s) / max(tb, 1e-6), 0, 1))
    return np.sin(e * math.pi / 2)


def _prof(v, m):
    """scalar or per-control-point list -> per-sample profile (smooth interpolation along the path)."""
    if np.ndim(v) == 0:
        return np.full(m, float(v))
    v = np.asarray(v, float)
    x = np.linspace(0, 1, len(v)); xi = np.linspace(0, 1, m)
    from scipy.interpolate import PchipInterpolator
    return PchipInterpolator(x, v)(xi)


def band_batch(P, N, sp):
    """eseg chain (k=0 inside the band) for one fold along surface polyline P with normals N.
    Section: a flattened ellipse (cushion) sitting on the surface -- crest `hgt` above it, half-width `w`;
    the ends fade by flattening (height -> 0) while staying broad (the fold dies into the cloth, no sausage tip)."""
    B = Batch()
    m = len(P)
    if m < 3:
        return B
    env = _env(m, sp['ta'], sp['tb'])
    T = np.gradient(P, axis=0); T /= np.linalg.norm(T, axis=1, keepdims=True) + 1e-12
    side = np.cross(N, T); side /= np.linalg.norm(side, axis=1, keepdims=True) + 1e-12
    w = _prof(sp['w'], m) * (sp['wend'] + (1 - sp['wend']) * env)
    hh = _prof(sp['hgt'], m) * env ** 1.3
    if sp['t'] is not None:
        t = _prof(sp['t'], m) * (0.5 + 0.5 * env)
        t = np.maximum(t, hh * 0.75 + 0.3)
    else:
        t = hh * 0.92 + 0.3                   # centre just under the surface: full width where the fold meets it
    lean = _prof(sp['lean'], m)
    up = N + lean[:, None] * side
    up /= np.linalg.norm(up, axis=1, keepdims=True)
    if sp['sub']:
        C = P + N * (t - hh)[:, None]            # digs hh into the surface
    else:
        C = P + N * (hh - t + sp['off'])[:, None]
    C = C + side * (0.3 * lean * w)[:, None]
    for i in range(m - 1):
        B.eseg(C[i], C[i + 1], up[i] + up[i + 1], max(w[i], 0.35), max(w[i + 1], 0.35), max(t[i], 0.3), max(t[i + 1], 0.3), 0.0)
    return B


def blend_into(F, B, k, sub=False):
    """Evaluate batch B (hard union) in a sub-block and smooth-union / smooth-subtract it into F.G with radius k."""
    if len(B) == 0 or not np.isfinite(np.array([b[0] for b in B.bounds] + [b[1] for b in B.bounds])).all():
        return
    lo = np.min([b[0] for b in B.bounds], axis=0) - (k + 2.0 + 3 * F.h)
    hi = np.max([b[1] for b in B.bounds], axis=0) + (k + 2.0 + 3 * F.h)
    a = np.clip(np.floor((lo - F.lo) / F.h).astype(int), 0, F.shape)
    b = np.clip(np.ceil((hi - F.lo) / F.h).astype(int) + 1, 0, F.shape)
    if np.any(b <= a):
        return
    S = Field.__new__(Field); S.lo = F.lo + a * F.h; S.h = F.h; S.shape = tuple(int(v) for v in (b - a))
    S.G = np.full(S.shape, FAR, np.float32)
    S.apply(B, 'union', pad=k + 1.5)
    V = F.G[a[0]:b[0], a[1]:b[1], a[2]:b[2]]
    d = S.G
    if sub:
        d = -d
        hk = np.clip(k - np.abs(V - d), 0, None) / k
        V[...] = np.maximum(V, d) + hk * hk * k * 0.25
    else:
        hk = np.clip(k - np.abs(V - d), 0, None) / k
        V[...] = np.minimum(V, d) - hk * hk * k * 0.25


def smooth_path(P, N, step=0.5):
    L = np.sum(np.linalg.norm(np.diff(P, axis=0), axis=1))
    n = max(4, int(L / step) + 1)
    idx = np.linspace(0, len(P) - 1, n)
    Pi = np.stack([np.interp(idx, np.arange(len(P)), P[:, j]) for j in range(3)], 1)
    Ni = np.stack([np.interp(idx, np.arange(len(P)), N[:, j]) for j in range(3)], 1)
    # smooth normals along the path (no wobble from the surface relief)
    from scipy.ndimage import gaussian_filter1d
    Ni = gaussian_filter1d(Ni, 2.0, axis=0, mode='nearest')
    Ni /= np.linalg.norm(Ni, axis=1, keepdims=True)
    return Pi, Ni


HGAIN, DGAIN = 1.45, 1.3


def apply(F, G0, lo, h, only=None):
    """Add all folds to F (full field).  G0: base block (copy) at lo used for tracing / normals."""
    T = TXM.CamTex(TXM.ref_camera(), (0, 0, 1179, 1078), 1.0, G0, lo, h, full=False)
    adds, subs = [], []
    for sp in (PX + D3) if only is None else only:
        if sp['pix'] is not None:
            P = T.trace(sp['pix'], step=0.25)
            N = T.normals(P) if len(P) >= 4 else None
        elif sp.get('floor'):
            P = resample(catmull(np.asarray(sp['p3'], float), per=10), 120)
            N = np.tile([0.0, 0.0, 1.0], (len(P), 1))
        else:
            P = T.surf(sp['p3'], step=0.25)
            N = T.normals(P) if len(P) >= 4 else None
        if len(P) < 4 or N is None:
            continue
        ok = np.isfinite(P).all(1) & np.isfinite(N).all(1) & (np.linalg.norm(N, axis=1) > 0.5)
        P, N = P[ok], N[ok]
        if len(P) < 4:
            continue
        P, N = smooth_path(P, N)
        if not (np.isfinite(P).all() and np.isfinite(N).all()):
            continue
        sp = dict(sp)
        g = (DGAIN if sp['sub'] else HGAIN) * sp.get('gain', 1.0)
        sp['hgt'] = (np.asarray(sp['hgt'], float) * g).tolist() if np.ndim(sp['hgt']) else sp['hgt'] * g
        (subs if sp['sub'] else adds).append((band_batch(P, N, sp), sp['k']))
    for B, k in adds:
        blend_into(F, B, k)
    for B, k in subs:
        blend_into(F, B, k, sub=True)
