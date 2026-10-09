"""Render all scenes, concatenate, normalise loudness and attach English subtitles.

    python build.py                                   # 1080p60 render of every scene + final assembly
    python build.py --quality l --only S03_Bloch      # quick 480p15 render of some scenes
    python build.py --assemble-only
Output: out/qgeom_en_subtitled.mp4 (English subtitles burned in), out/qgeom_en.mp4 (soft, switchable\nsubtitles) and out/qgeom_en.srt
"""
import argparse, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable          # run build.py with the python of your environment
SCENES = [('s01_intro', 'S01_Intro'), ('s02_distance', 'S02_Distance'), ('s03_bloch', 'S03_Bloch'),
          ('s04_wrap', 'S04_Wrap'), ('s05_info', 'S05_Info'), ('s06_berry', 'S06_Berry'),
          ('s07_metric', 'S07_Metric'), ('s08_nlhe', 'S08_NLHE'), ('s09_flatband', 'S09_FlatBand'),
          ('s10_measure', 'S10_Measure'), ('s11_outlook', 'S11_Outlook')]
QDIR = {'l': '480p15', 'm': '720p30', 'h': '1080p60', 'k': '2160p60'}
NAME = 'qgeom_en'


def video_path(f, c, q):
    return ROOT / 'media' / f'r_{c}' / 'videos' / f / QDIR[q] / f'{c}.mp4'


def render(f, c, q, voice):
    # separate media dir per process: manim's Tex cache is not safe for parallel writers
    cmd = [PY, '-m', 'manim', f'-q{q}', '--disable_caching', '--media_dir', str(ROOT / 'media' / f'r_{c}'),
           str(ROOT / 'scenes' / f'{f}.py'), c]
    env = dict(os.environ, QG_VOICE=voice)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    ok = r.returncode == 0 and video_path(f, c, q).exists()
    (ROOT / 'media' / f'render_{c}.log').write_text(r.stdout + r.stderr)
    return c, ok


def duration(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def chunks_en(text, maxcue=84, maxline=44):
    """Split a sentence into balanced subtitle cues of <= maxcue chars (cuts prefer a nearby comma),
    each wrapped onto at most two lines."""
    def cut(t, n):
        spaces = [i for i, ch in enumerate(t) if ch == ' ']
        out, last = [], 0
        for k in range(1, n):
            target = k * len(t) / n
            i = min((j for j in spaces if j > last), key=lambda j: abs(j - target) - (12 if t[j - 1] in ',;:' else 0))
            out.append(t[last:i].strip())
            last = i
        out.append(t[last:].strip())
        return out
    res = []
    for c in cut(text, -(-len(text) // maxcue)):
        c = re.sub(r'[,;:]$', '', c)
        if len(c) > maxline:
            c = '\n'.join(cut(c, 2))
        res.append(c)
    return res


def ts(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', ',')


def assemble(q, voice):
    manifest = json.loads((ROOT / 'audio' / voice / 'manifest.json').read_text())
    outdir = ROOT / 'out'
    outdir.mkdir(exist_ok=True)
    lst, srt, offset, n = [], [], 0.0, 1
    for f, c in SCENES:
        v = video_path(f, c, q)
        lst.append(f"file '{v}'")
        log = json.loads((ROOT / 'media' / 'sublog' / f'{c}.json').read_text())
        for beat in log['beats']:
            for s in manifest[beat['key']]['sentences']:
                t0, t1 = offset + beat['t0'] + s['start'], offset + beat['t0'] + s['end']
                lines = chunks_en(s['text'])
                tot = sum(len(x) for x in lines)
                t = t0
                for line in lines:
                    dt = (t1 - t0) * len(line) / tot
                    srt.append(f'{n}\n{ts(t)} --> {ts(t + dt - 0.02)}\n{line}\n')
                    n += 1
                    t += dt
        offset += duration(v)
    (outdir / 'concat.txt').write_text('\n'.join(lst) + '\n')
    srt_path = outdir / f'{NAME}.srt'
    srt_path.write_text('\n'.join(srt), encoding='utf-8')
    raw = outdir / f'{NAME}_raw.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(outdir / 'concat.txt'),
                    '-c:v', 'copy', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    str(raw)], check=True)
    final = outdir / f'{NAME}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-i', str(srt_path),
                    '-map', '0', '-map', '1', '-c', 'copy', '-c:s', 'mov_text',
                    '-metadata:s:s:0', 'language=eng', '-metadata:s:s:0', 'title=English',
                    '-movflags', '+faststart', str(final)], check=True)
    raw.unlink()
    print(f'{final}  ({offset / 60:.1f} min, {n - 1} subtitle cues)')
    # visible (burned-in) English subtitles in a band below the slightly shrunk animation
    subbed = outdir / f'{NAME}_subtitled.mp4'
    subprocess.run([PY, str(ROOT / 'tools' / 'burn_subs.py'), str(final), str(srt_path), str(subbed)], check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quality', default='h', choices=list(QDIR))
    ap.add_argument('--only', default='')
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--assemble-only', action='store_true')
    ap.add_argument('--voice', default='af_bella')
    a = ap.parse_args()
    if not a.assemble_only:
        todo = [(f, c) for f, c in SCENES if not a.only or c in a.only.split(',')]
        with ThreadPoolExecutor(a.jobs) as ex:
            for c, ok in ex.map(lambda fc: render(*fc, a.quality, a.voice), todo):
                print(('OK   ' if ok else 'FAIL ') + c, flush=True)
    if not a.only:
        assemble(a.quality, a.voice)


if __name__ == '__main__':
    sys.exit(main())
