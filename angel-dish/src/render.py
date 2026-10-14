"""Blender (bpy) renderer: python3 render.py mesh.ply outprefix [views] [--res W] [--samples N]

Views: ref (matches reference photo camera), front, left, right, back, top, threeq, face, wingR, wingL
Units: mm. Pink wax/resin material with subsurface scattering on a pale marble-ish table.
"""
import sys, math, json, os
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CAM = json.load(open(os.path.join(HERE, 'camera.json')))


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def setup(mesh_path, res, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'NONE'
    bpy.ops.wm.ply_import(filepath=mesh_path)
    ob = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_smooth()
    # material: pink wax
    m = bpy.data.materials.new('wax'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    P = os.environ.get('LIGHTING', 'photo')
    b.inputs['Base Color'].default_value = (0.50, 0.255, 0.27, 1) if P != 'old' else (0.62, 0.29, 0.27, 1)
    b.inputs['Roughness'].default_value = 0.5
    b.inputs['Subsurface Weight'].default_value = 0.4
    b.inputs['Subsurface Radius'].default_value = (1.6, 0.7, 0.6)
    b.inputs['Subsurface Scale'].default_value = 1.0
    try:
        b.inputs['Specular IOR Level'].default_value = 0.4
        b.inputs['Sheen Weight'].default_value = 0.25 if P != 'old' else 0.0
        b.inputs['Sheen Roughness'].default_value = 0.35
    except Exception:
        pass
    ob.data.materials.append(m)
    # table
    bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, -0.01))
    pl = bpy.context.active_object
    tm = bpy.data.materials.new('table'); tm.use_nodes = True
    tb = tm.node_tree.nodes['Principled BSDF']
    tb.inputs['Base Color'].default_value = (0.50, 0.44, 0.40, 1); tb.inputs['Roughness'].default_value = 0.3
    pl.data.materials.append(tm)
    # world
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.42, 0.31, 0.24, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35
    def area(name, loc, energy, size, color=(1, 0.92, 0.85), tgt=(0, 0, 40)):
        L = bpy.data.lights.new(name, 'AREA'); L.energy = energy; L.size = size; L.color = color
        o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
        look_at(o, tgt)
    if P == 'old':
        area('key', (-300, -250, 380), 5.5e6, 300)
        area('fill', (380, -300, 140), 1.6e6, 350, (1, 0.95, 0.92))
        area('rim', (120, 380, 300), 2.0e6, 250)
    elif P == 'photo':
        # warm window light from upper-right-behind, soft left window, dim front fill
        area('key', (260, 260, 360), 6.0e6, 320, (1.0, 0.86, 0.72))
        area('left', (-420, 60, 260), 2.6e6, 300, (1.0, 0.9, 0.82))
        area('fill', (60, -420, 220), 1.1e6, 400, (1.0, 0.93, 0.88))
    elif P == 'photo2':
        area('key', (200, 120, 420), 6.5e6, 260, (1.0, 0.86, 0.72))
        area('left', (-400, -120, 240), 2.2e6, 300, (1.0, 0.9, 0.82))
        area('fill', (100, -420, 160), 0.9e6, 400, (1.0, 0.93, 0.88))
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = samples; sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception:
        pass
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'None'
    sc.view_settings.exposure = -0.4 if os.environ.get('LIGHTING', 'photo') != 'old' else 0.0
    sc.render.film_transparent = False
    return sc, ob


def add_cam(sc, loc, target, lens, shift=(0, 0), ortho=None):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = 36; c.sensor_fit = 'HORIZONTAL'
    c.clip_start = 1; c.clip_end = 10000
    c.shift_x, c.shift_y = shift
    if ortho:
        c.type = 'ORTHO'; c.ortho_scale = ortho
    o = bpy.data.objects.new('cam', c); sc.collection.objects.link(o)
    o.location = loc; look_at(o, target)
    sc.camera = o
    return o


def view_params(name, bbox):
    (x0, y0, z0), (x1, y1, z1) = bbox
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    size = max(x1 - x0, y1 - y0, z1 - z0)
    d = size * 3.2
    if name == 'ref':
        r = CAM
        az, el = math.radians(r['az']), math.radians(r['el'])
        t = r['target']
        loc = (t[0] + r['dist'] * math.sin(az) * math.cos(el), t[1] - r['dist'] * math.cos(az) * math.cos(el), t[2] + r['dist'] * math.sin(el))
        return loc, t, r['lens'], (r.get('shift_x', 0), r.get('shift_y', 0)), (r['w'], r['h'])
    views = {
        'front': (0, 8), 'left': (-90, 15), 'right': (90, 15), 'back': (180, 20), 'top': (0, 89.5),
        'threeq': (-35, 25), 'threeqR': (40, 25), 'backL': (-140, 25), 'backR': (140, 25), 'low': (0, 2),
    }
    if name in views:
        az, el = (math.radians(a) for a in views[name])
        t = (cx, cy, cz)
        loc = (cx + d * math.sin(az) * math.cos(el), cy - d * math.cos(az) * math.cos(el), cz + d * math.sin(el))
        return loc, t, 105, (0, 0), None
    if name == 'face':
        f = CAM.get('face_target', [-20, 20, 85])
        az, el = math.radians(CAM['az'] + 10), math.radians(12)
        dd = 120
        loc = (f[0] + dd * math.sin(az) * math.cos(el), f[1] - dd * math.cos(az) * math.cos(el), f[2] + dd * math.sin(el))
        return loc, f, 105, (0, 0), (800, 800)
    if name == 'faceF':
        f = CAM.get('face_target', [-20, 20, 85])
        loc = (f[0] + 40, f[1] - 110, f[2] + 5)
        return loc, f, 105, (0, 0), (800, 800)
    raise KeyError(name)


def main():
    args = sys.argv[1:]
    mesh, prefix = args[0], args[1]
    views = ['ref']
    res = 700; samples = 48
    rest = args[2:]
    i = 0
    while i < len(rest):
        if rest[i] == '--res':
            res = int(rest[i + 1]); i += 2
        elif rest[i] == '--samples':
            samples = int(rest[i + 1]); i += 2
        else:
            views = rest[i].split(','); i += 1
    sc, ob = setup(mesh, res, samples)
    import numpy as np
    co = np.empty(len(ob.data.vertices) * 3, np.float32); ob.data.vertices.foreach_get('co', co); co = co.reshape(-1, 3)
    bbox = (co.min(0), co.max(0))
    for v in views:
        loc, t, lens, shift, wh = view_params(v, bbox)
        add_cam(sc, loc, t, lens, shift)
        if wh:
            s = res / max(wh)
            sc.render.resolution_x = int(wh[0] * s); sc.render.resolution_y = int(wh[1] * s)
        else:
            sc.render.resolution_x = res; sc.render.resolution_y = int(res * 0.8)
        sc.render.filepath = f'{prefix}_{v}.png'
        bpy.ops.render.render(write_still=True)
        print('wrote', sc.render.filepath)


main()
