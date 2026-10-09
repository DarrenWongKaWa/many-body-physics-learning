"""Local English TTS for the narration with Kokoro-82M v1.0 (Apache-2.0, runs on CPU).

    python tts.py [--voice af_bella] [--speed 1.0] [--only key1,key2]

Writes audio/<voice>/<key>.wav and audio/<voice>/manifest.json with the duration of
every beat and the start/end of each sentence (used for subtitles and animation sync).
Only beats whose text changed are regenerated.
"""
import argparse, json, re, warnings
from pathlib import Path
import numpy as np
import soundfile as sf

warnings.filterwarnings('ignore')
REPO = 'hexgrad/Kokoro-82M'
SR = 24000
GAP = 0.25          # pause between sentences (s)
HEAD, TAIL = 0.05, 0.15


def split_sentences(text):
    parts = re.split(r'(?<=[.!?;])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def plain(text):
    """Drop [word](/phonemes/) pronunciation overrides (for subtitles)."""
    return re.sub(r'\[([^\]]+)\]\(/[^)]*/\)', r'\1', text)


def synth(pipe, text, voice, speed):
    chunks = [r.audio.numpy() for r in pipe(text, voice=voice, speed=speed)]
    a = np.concatenate(chunks) if chunks else np.zeros(1)
    idx = np.where(np.abs(a) > 0.01)[0]          # trim near-silence at both ends
    if len(idx):
        a = a[max(0, idx[0] - 240): idx[-1] + 480]
    return a.astype(np.float32)


def main():
    from narration import SCRIPT
    from kokoro import KPipeline
    ap = argparse.ArgumentParser()
    ap.add_argument('--voice', default='af_bella')
    ap.add_argument('--speed', type=float, default=1.0)
    ap.add_argument('--only', default='')
    args = ap.parse_args()
    out = Path('audio') / args.voice
    out.mkdir(parents=True, exist_ok=True)
    mpath = out / 'manifest.json'
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    only = set(filter(None, args.only.split(',')))
    pipe = KPipeline(lang_code='a', repo_id=REPO)
    for scene, beats in SCRIPT.items():
        for key, text in beats:
            if only and key not in only:
                continue
            if not only and key in manifest and manifest[key]['text'] == text \
                    and (out / f'{key}.wav').exists():
                continue
            pieces, sents, t = [np.zeros(int(HEAD * SR), np.float32)], [], HEAD
            for s in split_sentences(text):
                a = synth(pipe, s, args.voice, args.speed)
                sents.append(dict(text=plain(s), start=round(t, 3), end=round(t + len(a) / SR, 3)))
                pieces += [a, np.zeros(int(GAP * SR), np.float32)]
                t += len(a) / SR + GAP
            pieces[-1] = np.zeros(int(TAIL * SR), np.float32)
            audio = np.concatenate(pieces)
            sf.write(out / f'{key}.wav', audio, SR)
            manifest[key] = dict(scene=scene, text=text, dur=round(len(audio) / SR, 3), sentences=sents)
            print(f'{key}: {len(audio)/SR:5.1f}s', flush=True)
            mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    total = sum(v['dur'] for v in manifest.values())
    print(f'total narration: {total/60:.1f} min')


if __name__ == '__main__':
    main()
