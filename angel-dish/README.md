# Angel jewelry dish — 3D-printable replica (work in progress)

Procedural SDF sculpt of a pink angel jewelry dish, built to match a single reference photo.

- `src/` — snapshot of the generator. `model.py` assembles `dish.py`, `figure.py`, `head.py`, `wings.py`
  (plus their `*_` helpers) on the numba SDF engine in `sdf.py`. `preview.py` builds + renders with Blender (bpy)
  from the reference camera (`camera.json`). `export.py` writes the final watertight STL, scaled by
  `layout.EXPORT_SCALE`.
- `progress/` — render comparisons against the reference photo at each stage.

Requirements: `numpy numba scipy scikit-image trimesh fast-simplification bpy`.
