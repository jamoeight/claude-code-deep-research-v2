import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))
import waterfalls as wf
from concurrent.futures import ThreadPoolExecutor
REG = {"Guiana": (1, 7, -66, -57), "NewGuinea": (-7, -2, 135, 147), "EHimalaya": (27, 30, 92, 97),
       "Albertine": (-5, 1, 27, 30), "PeruBolivia": (-17, -5, -79, -67), "Ethiopia": (6, 14, 36, 40),
       "Madagascar": (-25, -12, 46, 51), "Borneo": (-1, 6, 112, 118)}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "waterfalls", "tiles"); os.makedirs(OUT, exist_ok=True)
def job(t):
    fn = os.path.join(OUT, f"{t[0]}_{t[1]}.json")
    if os.path.exists(fn): return
    try: json.dump(wf.scan_tile(*t), open(fn, "w"))
    except Exception as e: json.dump({"error": repr(e)}, open(fn + ".err", "w"))
for name in sys.argv[1:]:
    a0, a1, o0, o1 = REG[name]; t0 = time.time()
    tiles = [(a, o) for a in range(a0, a1) for o in range(o0, o1)]
    with ThreadPoolExecutor(int(os.environ.get("NTH", "2"))) as ex: list(ex.map(job, tiles))
    print(name, len(tiles), f"{time.time()-t0:.0f}s", flush=True)
