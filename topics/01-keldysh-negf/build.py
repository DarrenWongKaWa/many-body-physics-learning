"""Render all scenes, concatenate, normalise loudness and attach Chinese subtitles.

    python build.py            # 1080p60 render of every scene + final assembly
    python build.py --quality l --only S06_Results,S07_Crossover
    python build.py --assemble-only
    python build.py --lang en                 # English (voice af_bella, English labels)
Output: out/keldysh_<lang>.mp4 (soft subtitles) and out/keldysh_<lang>.srt
"""
import argparse, json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable          # run build.py with the python of your environment
SCENES = [('s01_intro', 'S01_Intro'), ('s02_equilibrium', 'S02_Equilibrium'), ('s03_contour', 'S03_Contour'),
          ('s03_contour', 'S04_Components'), ('s05_langreth', 'S05_Langreth'), ('s05_langreth', 'S06_Keldysh'),
          ('s07_transport', 'S07_Model'), ('s07_transport', 'S08_Current'), ('s09_resonant', 'S09_Resonant'),
          ('s09_resonant', 'S10_Master'), ('s09_resonant', 'S11_Summary')]
QDIR = {'l': '480p15', 'm': '720p30', 'h': '1080p60', 'k': '2160p60'}


VOICES = {'zh': 'zm_010', 'en': 'af_bella'}


def sfx(lang):
    return '' if lang == 'zh' else f'_{lang}'


def video_path(f, c, q, lang):
    return ROOT / 'media' / f'r_{c}{sfx(lang)}' / 'videos' / f / QDIR[q] / f'{c}.mp4'


def render(f, c, q, lang, voice):
    # separate media dir per process: manim's Tex cache is not safe for parallel writers
    cmd = [PY, '-m', 'manim', f'-q{q}', '--disable_caching', '--media_dir', str(ROOT / 'media' / f'r_{c}{sfx(lang)}'),
           str(ROOT / 'scenes' / f'{f}.py'), c]
    env = dict(os.environ, NLHE_LANG=lang, NLHE_VOICE=voice)
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, env=env)
    ok = r.returncode == 0 and video_path(f, c, q, lang).exists()
    if not ok:
        (ROOT / 'media' / f'render_{c}.log').write_text(r.stdout + r.stderr)
    return c, ok


def duration(p):
    out = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(p)],
                         capture_output=True, text=True).stdout
    return float(out.strip())


def chunks_en(text, maxcue=84, maxline=44):
    """Split an English sentence into balanced subtitle cues of <= maxcue chars (cuts prefer a
    nearby comma), each wrapped onto at most two lines."""
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
    cues = cut(text, -(-len(text) // maxcue))
    res = []
    for c in cues:
        c = re.sub(r'[,;:]$', '', c)
        if len(c) > maxline:
            c = '\n'.join(cut(c, 2))
        res.append(c)
    return res


def chunks(text, maxlen=20):
    """Split a sentence into subtitle lines at Chinese punctuation, each <= maxlen chars if possible."""
    parts = [p for p in re.split(r'(?<=[，、：；])', text) if p]
    out, cur = [], ''
    for p in parts:
        if cur and len(cur) + len(p) > maxlen:
            out.append(cur)
            cur = p
        else:
            cur += p
    if cur:
        out.append(cur)
    return [re.sub(r'[，。、；：！？]+$', '', c).strip() for c in out]


def ts(t):
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f'{int(h):02d}:{int(m):02d}:{s:06.3f}'.replace('.', ',')


def assemble(q, voice, lang):
    manifest = json.loads((ROOT / 'audio' / voice / 'manifest.json').read_text())
    split = chunks_en if lang == 'en' else chunks
    name = f'keldysh_{lang}'
    outdir = ROOT / 'out'
    outdir.mkdir(exist_ok=True)
    lst, srt, offset, n = [], [], 0.0, 1
    for f, c in SCENES:
        v = video_path(f, c, q, lang)
        lst.append(f"file '{v}'")
        log = json.loads((ROOT / 'media' / f'sublog{sfx(lang)}' / f'{c}.json').read_text())
        for beat in log['beats']:
            seg = manifest[beat['key']]
            for s in seg['sentences']:
                t0, t1 = offset + beat['t0'] + s['start'], offset + beat['t0'] + s['end']
                lines = split(s['text'])
                tot = sum(len(x) for x in lines)
                t = t0
                for line in lines:
                    dt = (t1 - t0) * len(line) / tot
                    srt.append(f'{n}\n{ts(t)} --> {ts(t + dt - 0.02)}\n{line}\n')
                    n += 1
                    t += dt
        offset += duration(v)
    (outdir / f'concat_{lang}.txt').write_text('\n'.join(lst) + '\n')
    (outdir / f'{name}.srt').write_text('\n'.join(srt), encoding='utf-8')
    raw = outdir / f'{name}_raw.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', str(outdir / f'concat_{lang}.txt'),
                    '-c:v', 'copy', '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000',
                    str(raw)], check=True)
    final = outdir / f'{name}.mp4'
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', str(raw), '-i', str(outdir / f'{name}.srt'),
                    '-map', '0', '-map', '1', '-c', 'copy', '-c:s', 'mov_text',
                    '-metadata:s:s:0', 'language=' + ('eng' if lang == 'en' else 'chi'),
                    '-metadata:s:s:0', 'title=' + ('English' if lang == 'en' else '中文'),
                    '-movflags', '+faststart', str(final)], check=True)
    raw.unlink()
    print(f'{final}  ({offset / 60:.1f} min, {n - 1} subtitle lines)')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quality', default='h', choices=list(QDIR))
    ap.add_argument('--only', default='')
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--assemble-only', action='store_true')
    ap.add_argument('--lang', default='zh', choices=list(VOICES))
    ap.add_argument('--voice', default=None)
    ap.add_argument('--no-burn', action='store_true', help='skip burning the English subtitles into the picture')
    a = ap.parse_args()
    voice = a.voice or VOICES[a.lang]
    if not a.assemble_only:
        todo = [(f, c) for f, c in SCENES if not a.only or c in a.only.split(',')]
        with ThreadPoolExecutor(a.jobs) as ex:
            for c, ok in ex.map(lambda fc: render(*fc, a.quality, a.lang, voice), todo):
                print(('OK   ' if ok else 'FAIL ') + c, flush=True)
    if not a.only:
        assemble(a.quality, voice, a.lang)
        if a.lang == 'en' and not a.no_burn:
            # hard subtitles in their own band below the animation (tools/burn_subs.py)
            base = ROOT / 'out' / ('keldysh_en' if 'keldysh' in str(ROOT) else 'nlhe_en')
            subprocess.run([PY, str(ROOT / 'tools' / 'burn_subs.py'), f'{base}.mp4', f'{base}.srt',
                            f'{base}_subtitled.mp4'], check=True)


if __name__ == '__main__':
    sys.exit(main())
