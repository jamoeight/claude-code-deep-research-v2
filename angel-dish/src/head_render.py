"""Close-up renders for the head agent (does not touch shared files).
python3 head_render.py mesh.ply outprefix [--box x0,y0,x1,y1] [--scale 4] [--samples 24] [--views refzoom,front,q3,profile,back,q3back]
refzoom = the reference camera, rendering only the ref-pixel box at `scale` x resolution (exact viewpoint match).
Other views orbit the head (local frame from head.POSE)."""
import sys, math, json, os
import bpy
from mathutils import Vector
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CAM = json.load(open(os.path.join(HERE, 'camera.json')))


def look_at(obj, target, up_hint=None):
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
    # same 'photo' lighting as render.py
    area('key', (260, 260, 360), 6.0e6, 320, (1.0, 0.86, 0.72))
    area('left', (-420, 60, 260), 2.6e6, 300, (1.0, 0.9, 0.82))
    area('fill', (60, -420, 220), 1.1e6, 400, (1.0, 0.93, 0.88))
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'
    sc.cycles.samples = samples; sc.cycles.use_denoising = True
    sc.view_settings.view_transform = 'AgX'
    sc.view_settings.exposure = -0.4
    return sc


def add_cam(sc, loc, target, lens, shift=(0, 0)):
    c = bpy.data.cameras.new('cam'); c.lens = lens; c.sensor_width = 36; c.sensor_fit = 'HORIZONTAL'
    c.clip_start = 1; c.clip_end = 10000; c.shift_x, c.shift_y = shift
    o = bpy.data.objects.new('cam', c); sc.collection.objects.link(o)
    o.location = loc; look_at(o, target); sc.camera = o
    return o


def main():
    a = sys.argv[1:]
    mesh, prefix = a[0], a[1]
    def opt(n, d):
        return a[a.index(n) + 1] if n in a else d
    box = [int(v) for v in opt('--box', '360,110,540,300').split(',')]
    scale = float(opt('--scale', '4')); samples = int(opt('--samples', '24'))
    views = opt('--views', 'refzoom,front,q3,profile').split(',')
    res = int(opt('--res', '700'))
    sc = setup(mesh, samples)
    from head import POSE
    O = POSE.O
    for v in views:
        sc.render.use_border = False; sc.render.use_crop_to_border = False
        if v == 'refzoom':
            r = CAM; az, el = math.radians(r['az']), math.radians(r['el']); t = r['target']
            loc = (t[0] + r['dist'] * math.sin(az) * math.cos(el), t[1] - r['dist'] * math.cos(az) * math.cos(el), t[2] + r['dist'] * math.sin(el))
            add_cam(sc, loc, t, r['lens'])
            W, H = r['w'], r['h']
            sc.render.resolution_x = int(W * scale); sc.render.resolution_y = int(H * scale)
            sc.render.use_border = True; sc.render.use_crop_to_border = True
            x0, y0, x1, y1 = box
            sc.render.border_min_x = x0 / W; sc.render.border_max_x = x1 / W
            sc.render.border_min_y = 1 - y1 / H; sc.render.border_max_y = 1 - y0 / H
        elif v.startswith('z'):
            # zoomed world orbit on her right shoulder / flare: zB, zBR, zL, zS, zF
            az = {'zB': 180, 'zBR': 140, 'zL': -45, 'zS': -90, 'zF': 0, 'zBL': -140}[v]
            azr, elr = math.radians(az), math.radians(15)
            tgt = np.array([-25.0, 24.0, 76.0]); dist = 60
            loc = tgt + dist * np.array([math.sin(azr) * math.cos(elr), -math.cos(azr) * math.cos(elr), math.sin(elr)])
            add_cam(sc, tuple(loc), tuple(tgt), 80)
            sc.render.resolution_x = res; sc.render.resolution_y = res
        elif v.startswith('w'):
            # world orbit around the upper body: wL (az -45), wR (az +45), wS (az -90), wB (az 180), wBL (-140), wBR (140)
            az = {'wL': -45, 'wR': 45, 'wS': -90, 'wSR': 90, 'wB': 180, 'wBL': -140, 'wBR': 140, 'wF': 0}[v]
            azr, elr = math.radians(az), math.radians(12)
            tgt = np.array([-17.0, 22.0, 78.0]); dist = 120
            loc = tgt + dist * np.array([math.sin(azr) * math.cos(elr), -math.cos(azr) * math.cos(elr), math.sin(elr)])
            add_cam(sc, tuple(loc), tuple(tgt), 80)
            sc.render.resolution_x = res; sc.render.resolution_y = res
        else:
            # orbit around the face centre in the head-local frame
            ang = {'front': (0, 0), 'q3': (35, 5), 'profile': (85, 0), 'q3R': (-40, 5), 'back': (180, 10), 'q3back': (140, 10),
                   'top': (0, 70), 'below': (0, -25)}[v]
            yaw, elv = (math.radians(x) for x in ang)
            dl = np.array([math.sin(yaw) * math.cos(elv), math.cos(yaw) * math.cos(elv), math.sin(elv)])  # local dir (x left, y fwd, z up)
            tgt = POSE.P((0, 2.0, -2.5)) if v not in ('back', 'q3back') else POSE.P((0, -2.0, -6.0))
            dw = POSE.D(dl)
            dist = 52 if v not in ('back', 'q3back') else 140
            loc = tgt + dist * dw
            add_cam(sc, tuple(loc), tuple(tgt), 105 if v not in ('back', 'q3back') else 80)
            sc.render.resolution_x = res; sc.render.resolution_y = res
        sc.render.filepath = f'{prefix}_{v}.png'
        bpy.ops.render.render(write_still=True)


main()
