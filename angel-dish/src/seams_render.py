"""Close-up junction renders (integrator tool; reuses render.py's scene setup).
   python3 seams_render.py model.ply outprefix NAME:tx,ty,tz,az,el,dist[,lens] ... [--res 700] [--samples 24]
az/el in degrees (az 0 = from front (-Y), +90 = from +X), dist in mm."""
import sys, os, math
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'render.py')).read()
src = src[:src.rindex('\nmain()')]
g = {'__name__': 'render_lib', '__file__': os.path.join(HERE, 'render.py')}
exec(compile(src, 'render.py', 'exec'), g)
args = sys.argv[1:]
mesh, prefix = args[0], args[1]
res = 700; samples = 24; cams = []
i = 2
while i < len(args):
    if args[i] == '--res':
        res = int(args[i + 1]); i += 2
    elif args[i] == '--samples':
        samples = int(args[i + 1]); i += 2
    else:
        cams.append(args[i]); i += 1
sc, ob = g['setup'](mesh, res, samples)
for c in cams:
    name, p = c.split(':')
    v = [float(t) for t in p.split(',')]
    tx, ty, tz, az, el, d = v[:6]
    lens = v[6] if len(v) > 6 else 105
    az, el = math.radians(az), math.radians(el)
    loc = (tx + d * math.sin(az) * math.cos(el), ty - d * math.cos(az) * math.cos(el), tz + d * math.sin(el))
    g['add_cam'](sc, loc, (tx, ty, tz), lens)
    sc.render.resolution_x = res; sc.render.resolution_y = res
    sc.render.filepath = f'{prefix}_{name}.png'
    g['bpy'].ops.render.render(write_still=True)
    print('wrote', sc.render.filepath, flush=True)
