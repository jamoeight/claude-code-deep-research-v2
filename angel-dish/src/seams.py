"""Integration fixes applied to the fully assembled field (owned by the integrator).
model.py calls apply(F) after all parts are unioned and the floor is cut.
Field ops live in seams_ops.py:
  soft_close(F, box, r, dmin) : closing (fills gaps narrower than ~2r) inside a tight box; dmin>0 fills only the part of a
                                gap deeper than dmin below the closed surface, so shallow carved grooves keep their profile
  smooth_zone(F, segs, ...)   : local low-pass of the field around junction segments (fades sub-mm striae, keeps folds)
  base_fill(F, ...)           : flat print base with a smooth SDF (replaces post.flat_base: no binary layers, no strip,
                                nothing below z=0, every footprint column solid up to its first overhang)"""
import post
import seams_ops as so

# (box x0,y0,z0,x1,y1,z1, closing radius, min depth, tag) - junction pits / slits between components
CLOSINGS = [
    # --- base
    ((58, 22, 0, 72, 35, 5), 1.4, 0.0, 'base slit: right wing foot / dish foot (back-right)'),
    # --- back-left: chimney slit + tunnels between the left wing foot, dish back wall and the train column end
    ((-58, 22, 0, -42, 40, 20), 1.2, 0.0, 'left wing foot / dish back wall / train end'),
    ((-57.5, 22.5, 8, -50.5, 30, 23), 1.7, 0.0, 'left wing foot / dish back wall: top of the chimney well'),
    # --- left wall: knife slot + V-trough between the left wing's inner lower face and the dish's first whirl roll
    ((-64, -34, 12, -55.5, 4, 32), 1.5, 0.0, 'left wing / dish wall trough'),
    # --- right wing tip on the rim lump: concave fillet from the rim crest into the tongue underside
    ((70, -3, 31, 86, 10, 39), 1.5, 0.0, 'right wing tip / rim lump fillet'),
    # --- behind the figure: right wing root meets the dish back wall (pocket B + slit)
    ((-15, 35.5, 16, -7, 40.5, 26), 1.0, 0.0, 'right wing / dish back wall behind figure'),
    ((-3, 33, 18, 7, 39, 31), 1.2, 0.0, 'figure back drapery / dish back rim slot (right window floor)'),
    # --- pinhole tunnels (genus) at component contacts
    ((-37, 19.5, 37.5, -32.5, 23.5, 42), 0.8, 0.0, 'pinhole: left wing tips / figure arm'),
    ((-31.5, 22, 45.5, -27.5, 26, 50), 0.8, 0.0, 'pinhole: arm-torso slot back web'),
    ((-15.5, 28, 45.5, -11.5, 32, 50), 0.8, 0.0, 'pinhole: wing roots / back'),
    ((4.5, 35, 27, 9, 39, 31.5), 0.8, 0.0, 'pinhole: right wing root / back rim'),
    ((0.5, 34, 22, 4, 37.5, 25.5), 0.8, 0.0, 'pinhole: right wing root / back rim low'),
]

# smoothing zones: (segments, r_in, r_out, sigma, tag)
SMOOTH = [
    # dish whirl striae (pitch ~1.15) where they run out from under the figure's train: fade them (washboard)
    ([((-37.2, 10.9, 24.1), (-53.6, 2.2, 19.4)), ((-36.9, 6.0, 18.0), (-49.0, -3.2, 15.7))], 3.0, 7.0, 0.45,
     'train / dish striae'),
]

# global knife-slit rule: gaps narrower than 2*SLIT_R are filled where they are deeper than SLIT_DMIN below the
# closed surface (shallow carved grooves - combing, barbs, striae - are left untouched)
SLIT_R, SLIT_DMIN = 0.6, 0.7

# per-region overrides for the base column fill: (x0,y0,x1,y1,zmax) and 2D mouth closings (x0,y0,x1,y1,r)
BASE_ZMAX = [(-66, 12, -44, 40, 24.0)]          # back-left pocket between the left wing foot and the dish wall
BASE_CLOSE = [(-66, 12, -44, 40, 2.0)]


def fillers(F):
    """Extra smooth-union primitives (fillets at junction pits)."""
    return None


def apply(F):
    B = fillers(F)
    if B is not None and len(B):
        F.apply(B)
    for segs, ri, ro, sg, tag in SMOOTH:
        so.smooth_zone(F, segs, ri, ro, sg, tag=tag)
    for box, r, dmin, tag in CLOSINGS:
        so.soft_close(F, box, r, dmin=dmin, tag=tag)
    so.soft_close(F, (-95, -70, 0.5, 100, 60, 130), SLIT_R, dmin=SLIT_DMIN, tag='global knife slits')
    so.base_fill(F, zfoot=1.2, zmax=6.0, boxes_zmax=BASE_ZMAX, close_boxes=BASE_CLOSE)
    post.fill_voids(F)
    so.drop_specks(F, vmin=2.0)
    return F
