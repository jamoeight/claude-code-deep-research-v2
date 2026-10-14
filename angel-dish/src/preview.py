"""One-shot preview: build -> mesh -> Blender render -> compare crops.
   python3 preview.py TAG [--h 0.5] [--parts dish,figure,head,wings] [--views ref,front,top,back,threeq,left,right,face,faceF]
                          [--regions full,figure,face,wingR,wingL,front,torso,skirt] [--res 900] [--samples 24]
                          [--box x0,y0,z0,x1,y1,z1]  (restrict the build grid to a sub-box: use with small --h for detail checks,
                           e.g. head close-up at --h 0.12 --box -40,0,60,10,40,105 --views face,faceF)
Outputs in out/TAG/: model.ply, r_<view>.png, cmp_<region>.png  (compare = reference | render)."""
import sys, os, subprocess, time
HERE = os.path.dirname(os.path.abspath(__file__))
a = sys.argv[1:]
tag = a[0]
def opt(name, default):
    return a[a.index(name) + 1] if name in a else default
h = opt('--h', '0.5'); parts = opt('--parts', 'dish,figure,head,wings'); views = opt('--views', 'ref')
regions = opt('--regions', 'full'); res = opt('--res', '900'); samples = opt('--samples', '24')
od = os.path.join(HERE, 'out', tag); os.makedirs(od, exist_ok=True)
t = time.time()
box = ['--box', opt('--box', '')] if '--box' in a else []
subprocess.run([sys.executable, os.path.join(HERE, 'model.py'), os.path.join(od, 'model.ply'), h, '--parts', parts] + box, check=True, cwd=HERE)
r = subprocess.run([sys.executable, os.path.join(HERE, 'render.py'), os.path.join(od, 'model.ply'), os.path.join(od, 'r'), views, '--res', res, '--samples', samples],
                   cwd=HERE, capture_output=True, text=True)
if r.returncode:
    print(r.stdout[-2000:], r.stderr[-2000:]); sys.exit(1)
if 'ref' in views.split(','):
    for reg in regions.split(','):
        lm = ['--lm'] if reg == 'full' and '--lm' in a else []
        subprocess.run([sys.executable, os.path.join(HERE, 'compare.py'), os.path.join(od, 'r_ref.png'), os.path.join(od, f'cmp_{reg}.png'), '--region', reg] + lm, check=True, cwd=HERE)
print('done in %.0fs ->' % (time.time() - t), od)
for f in sorted(os.listdir(od)):
    if f.endswith('.png'):
        print('  ', os.path.join(od, f))
