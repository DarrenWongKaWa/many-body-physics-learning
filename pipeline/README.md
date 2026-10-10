# How the videos are made

This file is the technical how-to. The method behind it (how to choose what to show, the stages and their checks)
is in [`METHOD.md`](METHOD.md), and every problem we ran into is in [`PITFALLS.md`](PITFALLS.md).

Every topic folder is a self-contained project with the same pipeline:

```
source text ──► narration.py ──► tts.py ──► audio/<voice>/*.wav + manifest.json (per-sentence timings)
                     │                                      │
                     └──────────► scenes/*.py (Manim) ◄──────┘  with self.narrate(key): animations wait for the voice
                                        │
                                   build.py  ──► render scenes in parallel ──► concatenate ──► loudness-normalise
                                        │                                                 ──► SRT from the timings
                                        └──► tools/burn_subs.py ──► <name>_subtitled.mp4 (subtitles burned into the picture)
```

## 1. Environment (macOS, Apple Silicon)

```bash
brew install ffmpeg dvisvgm uv
# LaTeX: BasicTeX or MacTeX, plus two packages Manim needs (no sudo required)
tlmgr init-usertree && tlmgr --usermode install standalone preview
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -r requirements.txt
```

The Kokoro voices (Apache-2.0) are downloaded from Hugging Face on first use and then run locally on the CPU,
roughly 4× faster than real time on an M4 Pro.

## 2. Write the narration

- `narration.py` holds one `(key, text)` entry per animation **beat**, grouped by scene.
- The scene code synchronises with sentence boundaries through `b.wait_sentence(i)`, so the text is the timing source.
- When a script is translated, keep the same number of sentences per beat.
- Write numbers and symbols as words ("E over Gamma"). Fix pronunciations inline with `[Weyl](/vˈIl/)`;
  the markup is stripped from the subtitles.

## 3. Generate the voice

```bash
python tts.py --lang en --voice af_bella      # only beats whose text changed are regenerated
```

We cannot listen to the output during development, so the voice was chosen by transcribing candidates back with
Whisper (`mlx-whisper`) and keeping the one with the lowest word error rate. The same check runs on every new
narration:

```bash
python ../../pipeline/tools/check_tts.py      # from a topic folder; lists beats whose transcription differs
```

## 4. Animate

- Scenes use `with self.narrate(key) as b:` from `common.py`. It adds the audio, logs the start time for the subtitles,
  and pads the scene until the speech ends.
- Inside a beat, `b.wait_sentence(i)` waits for the i-th sentence, `b.until_sentence(i)` gives the time left until it
  starts (useful as a `run_time`), and `b.remaining()` the time left in the beat (`b.rest()` in topic 01).
- Whenever possible, curves come from real calculations, not drawings.
  Examples: the NEGF solver in topic 03, the resonant-level formulas in topic 01, the two-band geometry in topic 02.
  Anything schematic is labelled on screen.

## 5. Preview and check

```bash
python build.py --lang en --quality l --only S05_Langreth     # 480p15 render of one scene
```

Check frames with a contact sheet (`tools/tools_sheet.sh` or `tools/sheet.py`) before the full 1080p60 build.
A full build of a 10–15 minute video takes about 10–15 minutes on 6 cores.

## 6. Build

```bash
python build.py --lang en      # out/<name>_en.mp4 (soft subtitles), .srt, and out/<name>_en_subtitled.mp4
```

The Homebrew ffmpeg has no libass/drawtext. `tools/burn_subs.py` therefore draws each subtitle cue to a PNG with Pillow
and overlays it with ffmpeg. It also shrinks the animation to 88 % and puts the subtitles in a band of the background colour
underneath, so they never cover equations.

## Pitfalls

The list of problems we hit, with symptoms and fixes, is in [`PITFALLS.md`](PITFALLS.md).
