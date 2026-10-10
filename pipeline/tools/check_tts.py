"""Check the narration audio by transcribing it back with Whisper (we cannot listen to every take).

Run from a topic folder after `python tts.py`:

    python ../../pipeline/tools/check_tts.py                  # voice af_bella, report beats with WER > 4 %
    python ../../pipeline/tools/check_tts.py --threshold 0 --only open5,dis1

Needs `mlx-whisper` (Apple Silicon; listed as optional in requirements.txt). The model is downloaded from
Hugging Face on first use. Digits versus spelled-out numbers ("3.2" / "three point two"), hyphenation and
homophones ("Chern" / "churn") count as errors, so read the listed beats rather than trusting the number alone:
a mispronounced name shows up as a different word in the same place in every beat that uses it.
"""
import argparse, json, re, warnings
from pathlib import Path

warnings.filterwarnings('ignore')


def words(s):
    return re.sub(r"[^a-z0-9' ]", ' ', s.lower()).split()


def wer(ref, hyp):
    r, h = words(ref), words(hyp)
    d = list(range(len(h) + 1))
    for i in range(1, len(r) + 1):
        prev, d[0] = d[0], i
        for j in range(1, len(h) + 1):
            cur = min(d[j] + 1, d[j - 1] + 1, prev + (r[i - 1] != h[j - 1]))
            prev, d[j] = d[j], cur
    return d[-1] / max(1, len(r)), len(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--voice', default='af_bella')
    ap.add_argument('--model', default='mlx-community/whisper-large-v3-turbo')
    ap.add_argument('--threshold', type=float, default=0.04, help='print beats whose WER is above this')
    ap.add_argument('--only', default='')
    a = ap.parse_args()
    import mlx_whisper
    audio = Path('audio') / a.voice
    manifest = json.loads((audio / 'manifest.json').read_text())
    only = set(filter(None, a.only.split(',')))
    err = tot = 0.0
    for key, seg in manifest.items():
        if only and key not in only:
            continue
        ref = ' '.join(s['text'] for s in seg['sentences'])
        hyp = mlx_whisper.transcribe(str(audio / f'{key}.wav'), path_or_hf_repo=a.model, language='en')['text'].strip()
        w, n = wer(ref, hyp)
        err, tot = err + w * n, tot + n
        if w > a.threshold:
            print(f'{key}: WER {w:.2f}\n  said:  {ref}\n  heard: {hyp}')
    print(f'overall WER {err / max(tot, 1):.3f} over {int(tot)} words')


if __name__ == '__main__':
    main()
