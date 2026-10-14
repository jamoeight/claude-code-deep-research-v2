"""Workspace protocol for parallel sculptors.
  python3 sync.py init    <comp>   create work_<comp>/ (copy of the shared project, own out/)
  python3 sync.py pull    <comp>   refresh OTHER components' published files into work_<comp>/ (never touches yours)
  python3 sync.py publish <comp>   quick build check (h=0.9, all parts) in work_<comp>/, then copy YOUR files to the shared root
                                   (previous published version backed up to snapshots/)
comp in: wings dish figure head.  Your files = <comp>.py and <comp>_*.py
"""
import sys, os, shutil, glob, subprocess, time
ROOT = os.path.dirname(os.path.abspath(__file__))
COMPS = ['wings', 'dish', 'figure', 'head']


def own(comp, name):
    b = os.path.basename(name)
    return b == f'{comp}.py' or b.startswith(f'{comp}_')


def shared_files(d):
    return [f for f in glob.glob(os.path.join(d, '*.py')) + glob.glob(os.path.join(d, '*.json')) if os.path.basename(f) != 'sync.py']


def main():
    cmd, comp = sys.argv[1], sys.argv[2]
    assert comp in COMPS
    W = os.path.join(ROOT, f'work_{comp}')
    if cmd == 'init':
        os.makedirs(os.path.join(W, 'out'), exist_ok=True)
        for f in shared_files(ROOT):
            shutil.copy2(f, W)
        print('workspace', W)
    elif cmd == 'pull':
        n = 0
        for f in shared_files(ROOT):
            if own(comp, f):
                continue
            shutil.copy2(f, W); n += 1
        print(f'pulled {n} files into {W}')
    elif cmd == 'publish':
        t = time.time()
        r = subprocess.run([sys.executable, 'model.py', '/tmp/_pubcheck_%s.ply' % comp, '0.9'], cwd=W, capture_output=True, text=True)
        if r.returncode:
            print('BUILD CHECK FAILED - not published\n', r.stdout[-1500:], r.stderr[-3000:]); sys.exit(1)
        snap = os.path.join(ROOT, 'snapshots', f'{comp}_{time.strftime("%H%M%S")}')
        os.makedirs(snap, exist_ok=True)
        for f in glob.glob(os.path.join(ROOT, '*.py')):
            if own(comp, f):
                shutil.copy2(f, snap)
        files = [f for f in glob.glob(os.path.join(W, '*.py')) if own(comp, f)]
        for f in files:
            shutil.copy2(f, ROOT)
        print(f'published {[os.path.basename(f) for f in files]} (check {time.time() - t:.0f}s); backup in {snap}')


main()
