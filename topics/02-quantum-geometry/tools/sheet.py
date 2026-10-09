"""Contact sheet of frames from a 480p render:  python tools/sheet.py S02_Distance s02_distance 5 12 30 ...
If no times are given, takes one frame near the end of every narration beat."""
import json, subprocess, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parents[1]
c, f, *ts = sys.argv[1:]
v = ROOT / f'media/r_{c}/videos/{f}/480p15/{c}.mp4'
if not ts:
    log = json.loads((ROOT / f'media/sublog/{c}.json').read_text())
    man = json.loads((ROOT / 'audio/af_bella/manifest.json').read_text())
    ts = [b['t0'] + man[b['key']]['dur'] - 0.2 for b in log['beats']]
out = ROOT / 'media/frames'
out.mkdir(parents=True, exist_ok=True)
ims = []
for t in ts:
    p = out / f'{c}_{float(t):.1f}.png'
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(t), '-i', str(v), '-frames:v', '1', str(p)], check=True)
    ims.append(Image.open(p))
w, h = ims[0].size
cols = 2
sheet = Image.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)), 'white')
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * w, (i // cols) * h))
sheet.save(out / f'sheet_{c}.png')
print(out / f'sheet_{c}.png', [round(float(t), 1) for t in ts])
