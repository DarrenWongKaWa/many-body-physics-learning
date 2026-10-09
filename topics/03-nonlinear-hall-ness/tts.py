"""Local TTS for the narration with Kokoro-82M v1.1-zh (Apache-2.0, runs on CPU).

    python tts.py [--voice zm_010] [--speed 1.0] [--only key1,key2]
    python tts.py --lang en --voice af_heart        # English (Kokoro-82M v1.0)

Writes audio/<voice>/<key>.wav and audio/<voice>/manifest.json with the duration of
every beat and the start/end of each sentence (used for subtitles and animation sync).
"""
import argparse, json, re, warnings
from pathlib import Path
import numpy as np
import soundfile as sf

warnings.filterwarnings('ignore')
REPO = 'hexgrad/Kokoro-82M-v1.1-zh'
REPO_EN = 'hexgrad/Kokoro-82M'
SR = 24000
GAP = 0.22          # pause between sentences (s)
HEAD, TAIL = 0.05, 0.15


def split_sentences(text, lang='zh'):
    if lang == 'en':
        parts = re.split(r'(?<=[.!?;])\s+', text)
    else:
        parts = re.split(r'(?<=[。！？；])', text)
    return [p.strip() for p in parts if p.strip()]


def plain(text):
    """Drop [word](/phonemes/) pronunciation overrides (for subtitles)."""
    return re.sub(r'\[([^\]]+)\]\(/[^)]*/\)', r'\1', text)


def load_pipeline(lang='zh'):
    from kokoro import KModel, KPipeline
    if lang == 'en':
        return KPipeline(lang_code='a', repo_id=REPO_EN)
    en = KPipeline(lang_code='a', repo_id=REPO, model=False)

    def en_callable(t):
        return next(en(t)).phonemes

    model = KModel(repo_id=REPO).eval()
    return KPipeline(lang_code='z', repo_id=REPO, model=model, en_callable=en_callable)


def synth(pipe, text, voice, speed):
    chunks = [r.audio.numpy() for r in pipe(text, voice=voice, speed=speed)]
    a = np.concatenate(chunks) if chunks else np.zeros(1)
    # trim leading/trailing near-silence
    idx = np.where(np.abs(a) > 0.01)[0]
    if len(idx):
        a = a[max(0, idx[0] - 240): idx[-1] + 480]
    return a.astype(np.float32)


def main():
    from narration import SCRIPT, SCRIPT_EN
    ap = argparse.ArgumentParser()
    ap.add_argument('--lang', default='zh', choices=['zh', 'en'])
    ap.add_argument('--voice', default='zm_010')
    ap.add_argument('--speed', type=float, default=1.0)
    ap.add_argument('--only', default='')
    args = ap.parse_args()
    out = Path('audio') / args.voice
    out.mkdir(parents=True, exist_ok=True)
    mpath = out / 'manifest.json'
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {}
    only = set(filter(None, args.only.split(',')))
    pipe = load_pipeline(args.lang)
    script = SCRIPT_EN if args.lang == 'en' else SCRIPT
    for scene, beats in script.items():
        for key, text in beats:
            if only and key not in only:
                continue
            if not only and key in manifest and manifest[key]['text'] == text \
                    and (out / f'{key}.wav').exists():
                continue
            pieces, sents, t = [np.zeros(int(HEAD * SR), np.float32)], [], HEAD
            for s in split_sentences(text, args.lang):
                a = synth(pipe, s, args.voice, args.speed)
                sents.append(dict(text=plain(s), start=round(t, 3), end=round(t + len(a) / SR, 3)))
                pieces += [a, np.zeros(int(GAP * SR), np.float32)]
                t += len(a) / SR + GAP
            pieces[-1] = np.zeros(int(TAIL * SR), np.float32)
            audio = np.concatenate(pieces)
            sf.write(out / f'{key}.wav', audio, SR)
            manifest[key] = dict(scene=scene, text=text, dur=round(len(audio) / SR, 3),
                                 sentences=sents)
            print(f'{key}: {len(audio)/SR:5.1f}s', flush=True)
            mpath.write_text(json.dumps(manifest, ensure_ascii=False, indent=1))
    total = sum(v['dur'] for v in manifest.values())
    print(f'total narration: {total/60:.1f} min')


if __name__ == '__main__':
    main()
