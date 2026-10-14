"""Blender renderer for the figure agent (same material/lights as render.py) with crop + orbit cameras.
python3 figure_render.py mesh.ply prefix views [--res N] [--samples N] [--scale S]"""
import sys, math, json, os
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
CAM = json.load(open(os.path.join(HERE, 'camera.json')))
REG = {'full': (0, 0, 1179, 1078), 'figure': (250, 90, 620, 640), 'face': (360, 110, 540, 300),
       'wingR': (480, 30, 1179, 620), 'wingL': (0, 30, 430, 900), 'front': (0, 580, 1179, 1078),
       'torso': (300, 250, 600, 560), 'skirt': (280, 430, 820, 760), 'body': (300, 240, 680, 720),
       'arm': (300, 280, 420, 560), 'neck': (400, 230, 560, 400)}


def look_at(obj, target):
    d = Vector(target) - obj.location
    obj.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def setup(mesh_path, samples):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'NONE'
    bpy.ops.wm.ply_import(filepath=mesh_path)
    ob = bpy.context.selected_objects[0]
    bpy.context.view_layer.objects.active = ob
    bpy.ops.object.shade_smooth()
    m = bpy.data.materials.new('wax'); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (0.50, 0.255, 0.27, 1)
    b.inputs['Roughness'].default_value = 0.5
    b.inputs['Subsurface Weight'].default_value = 0.4
    b.inputs['Subsurface Radius'].default_value = (1.6, 0.7, 0.6)
    b.inputs['Subsurface Scale'].default_value = 1.0
    try:
        b.inputs['Specular IOR Level'].default_value = 0.4
        b.inputs['Sheen Weight'].default_value = 0.25
        b.inputs['Sheen Roughness'].default_value = 0.35
    except Exception:
        pass
    ob.data.materials.append(m)
    bpy.ops.mesh.primitive_plane_add(size=2000, location=(0, 0, -0.01))
    pl = bpy.context.active_object
    tm = bpy.data.materials.new('table'); tm.use_nodes = True
    tb = tm.node_tree.nodes['Principled BSDF']
    tb.inputs['Base Color'].default_value = (0.50, 0.44, 0.40, 1); tb.inputs['Roughness'].default_value = 0.3
    pl.data.materials.append(tm)
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.42, 0.31, 0.24, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35

    def area(name, loc, energy, size, color=(1, 0.92, 0.85)):
        L = bpy.data.lights.new(name, 'AREA'); L.energy = energy; L.size = size; L.color = color
        o = bpy.data.objects.new(name, L); sc.collection.objects.link(o); o.location = loc
        look_at(o, (0, 0, 40))
    area('key', (260, 260, 360), 6.0e6, 320, (1.0, 0.86, 0.72))
    area('left', (-420, 60, 260), 2.6e6, 300, (1.0, 0.9, 0.82))
    area('fill', (60, -420, 220), 1.1e6, 400, (1.0, 0.93, 0.88))
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = samples; sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = 'OPENIMAGEDENOISE'
    except Exception:
        pass
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.look = 'None'
    sc.view_settings.exposure = -0.4
    return sc, ob


def add_cam(sc, loc, target, lens, shift=(0, 0)):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = 36; c.sensor_fit = 'HORIZONTAL'
    c.clip_start = 1; c.clip_end = 10000
    c.shift_x, c.shift_y = shift
    o = bpy.data.objects.new('cam', c); sc.collection.objects.link(o)
    o.location = loc; look_at(o, target)
    sc.camera = o


def ref_loc():
    r = CAM; az, el = math.radians(r['az']), math.radians(r['el']); t = r['target']
    return (t[0] + r['dist'] * math.sin(az) * math.cos(el), t[1] - r['dist'] * math.cos(az) * math.cos(el), t[2] + r['dist'] * math.sin(el)), t


ORB = {'fFront': (0, 12), 'fBack': (180, 18), 'fLeft': (-90, 12), 'fRight': (90, 14), 'fTQL': (-40, 20), 'fTQR': (40, 20),
       'fBackL': (-140, 20), 'fBackR': (140, 20), 'fTop': (0, 70), 'fLow': (10, 3)}


CLOSE = {'cHand': ((-35.0, 21.0, 36.0), -30, 15, 80, 60), 'cBust': ((-17.0, 18.0, 62.0), 15, 10, 90, 60),
         'cBack': ((-20.0, 30.0, 52.0), 180, 15, 110, 60), 'cKnee': ((0.0, 8.0, 28.0), 35, 15, 110, 60),
         'cSide': ((-18.0, 22.0, 45.0), 90, 10, 150, 60), 'cHem': ((-18.0, 4.0, 16.0), -15, 22, 120, 60), 'cBackSk': ((-14.0, 36.0, 22.0), 180, 18, 110, 60), 'cRightSk': ((0.0, 20.0, 30.0), 75, 12, 110, 60), 'cScroll': ((6.0, 4.0, 16.0), 5, 25, 75, 60), 'cPocket': ((-18.0, 6.0, 22.0), 5, 22, 70, 60),
         'cHemR': ((5.0, 8.0, 16.0), 40, 22, 120, 60), 'cHemL': ((-35.0, 12.0, 18.0), -70, 22, 120, 60)}


def main():
    args = sys.argv[1:]
    mesh, prefix, views = args[0], args[1], args[2].split(',')
    res = int(args[args.index('--res') + 1]) if '--res' in args else 900
    samples = int(args[args.index('--samples') + 1]) if '--samples' in args else 16
    scale = float(args[args.index('--scale') + 1]) if '--scale' in args else 2.0
    sc, ob = setup(mesh, samples)
    W, H = CAM['w'], CAM['h']
    for v in views:
        if v == 'ref':
            loc, t = ref_loc(); add_cam(sc, loc, t, CAM['lens'])
            s = res / W; sc.render.resolution_x = int(W * s); sc.render.resolution_y = int(H * s)
        elif v.startswith('c_'):
            x0, y0, x1, y1 = REG[v[2:]]
            w = x1 - x0; hh = y1 - y0; cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
            loc, t = ref_loc()
            add_cam(sc, loc, t, CAM['lens'] * W / w, ((cx - W / 2) / w, (H / 2 - cy) / w))
            sc.render.resolution_x = int(w * scale); sc.render.resolution_y = int(hh * scale)
        elif v in CLOSE:
            tgt, az, el, d, lens = CLOSE[v]
            az, el = math.radians(az), math.radians(el)
            loc = (tgt[0] + d * math.sin(az) * math.cos(el), tgt[1] - d * math.cos(az) * math.cos(el), tgt[2] + d * math.sin(el))
            add_cam(sc, loc, tgt, lens)
            sc.render.resolution_x = res; sc.render.resolution_y = res
        else:
            az, el = (math.radians(q) for q in ORB[v])
            tgt = (-14.0, 18.0, 50.0); d = 175.0
            loc = (tgt[0] + d * math.sin(az) * math.cos(el), tgt[1] - d * math.cos(az) * math.cos(el), tgt[2] + d * math.sin(el))
            add_cam(sc, loc, tgt, 75)
            sc.render.resolution_x = int(res * 0.8); sc.render.resolution_y = res
        sc.render.filepath = f'{prefix}_{v}.png'
        bpy.ops.render.render(write_still=True)


main()
