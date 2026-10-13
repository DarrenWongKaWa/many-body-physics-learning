# From an abstract idea to an explainer video

This is the method behind every video in this repository, written so that you can use it for a topic of your own.
[`README.md`](README.md) in this folder covers the tools: environment, voice, rendering, assembly.
This file covers the decisions: what to show, in which order, how to keep it correct, and when a stage is finished.
The mistakes we made along the way are collected in [`PITFALLS.md`](PITFALLS.md).

"3Blue1Brown style" describes a look: dark background, geometry that moves, a calm voice.
The look is the easy part. The hard part is choosing what to show, keeping every number honest, and making the
picture carry the idea. The workflow below is the standard procedure we follow for that.
It borrows from established instructional-design research: backward design, cognitive-load theory,
Mayer's principles of multimedia learning, and concreteness fading. The references are at the end.

## The principles

1. **Start from what the viewer should be able to say afterwards.** Write three to five sentences that a viewer could
   say after watching. Anything that does not serve one of them is cut, however beautiful it is (backward design).
   Topic 04's plan removed the Lie-algebra decomposition and all pictures of Gr(2,4) for this reason.

2. **Find the one picture.** Every good topic has one image that the whole story can be told on.
   Every scene then adds one layer to it, and the viewer never has to rebuild a mental model.
   - Topic 02: the Bloch sphere with the Brillouin zone mapped onto it.
   - Topic 03: a Fermi sea drifting towards Berry-curvature hot spots.
   - Topic 04: a torus pressed onto a sphere, folding where it must.

   If you cannot name the picture, you are not ready to write the narration.

3. **Pose the puzzle first, then build the tools.** Open with a question that the viewer can feel is hard
   (topic 04: "can a torus lie smoothly over a sphere?"). Introduce each formal tool at the moment it answers part of
   that question, not in the order of the source text.

4. **Show it concretely before stating it abstractly.** Use one model and one convention throughout, with real numbers
   (QWZ at m = 1 and m = 3.2 in topics 02 and 04). Show the concrete case first: an ellipse on a sphere, a counter that
   stops at 1.19. Then name the general object: the metric, the quantum volume. This is concreteness fading.

5. **Let the narration carry the logic and the picture carry the structure.** Keep on-screen text to labels, formulas,
   and a few keywords; full sentences belong to the voice. A formula appears when it is spoken. A label sits next to the
   thing it names, not in a legend (Mayer's modality, temporal-contiguity and spatial-contiguity principles).
   Subtitles are the one deliberate exception, for viewers who read English better than they hear it. They go in a
   separate band below the animation, so they never cover the picture.

6. **Compute every curve.** Nothing that looks like data is drawn by hand.
   - Maps, ellipses, areas and counters come from the formulas in `common.py` or from `compute/make_data.py`.
   - If something is schematic or a teaching analogy, the screen says so.
   - If a value is read off a paper's figure, the README says how it was digitised.

7. **Keep the evidence classes apart.** Every claim in a video is one of five kinds, and the viewer must be able to tell
   which:
   - **established:** in the source papers, cited by section or equation;
   - **reproduced:** we recomputed it and it agrees;
   - **schematic:** shows a qualitative relation only;
   - **analogy:** a teaching picture that is not the real object;
   - **proposal:** our own unpublished idea. It is shown in green and marked "PROPOSAL (unpublished)" on screen
     (topic 04, act 4).

   A disagreement found while reproducing a paper is reported, not hidden (topic 03, Tr ñ = 1).

8. **Keep a convention ledger.** Before writing a single sentence, fix the sign conventions, the factors of two, which band
   you follow, and the units. Record how each source differs.
   - Topic 04: Huang uses a metric twice the standard one, and his two papers define the Berry curvature with
     opposite signs.
   - When you quote a number from a source, either convert it or say which convention it is in.

9. **Make it rebuildable.** The narration, scenes, data scripts and build script live next to each other. Anyone with
   the environment can regenerate the video bit for bit, and fix one sentence without redoing the rest.
   Source texts are linked, not redistributed.

## The standard workflow

Each stage ends with a gate: a check that must pass before the next stage starts.
Stages 0–2 decide the quality of the video. Stages 3–8 are craft, and the tools make them routine.

| Stage | Output | Gate |
|---|---|---|
| 0. Scope | learning goals, audience, prerequisites (topic README) | 3–5 goal sentences; earlier topics it relies on are named |
| 1. Study and verify | `notes/`, `verify/` or `compute/`, a convention ledger | every number and claim planned for the video is reproduced or cited |
| 2. Plan | `notes/video_plan*.md` | the one picture is named; scene table with sources; must-compute list; cut list; table of checked numbers |
| 3. Narration | `narration.py` | read aloud once; physics pass on every sentence; length estimated |
| 4. Data | `compute/make_data.py` → `data/` | printed checks agree with references; scenes only read data |
| 5. Voice | `audio/<voice>/` + `manifest.json` | back-transcription with Whisper; no misheard names or terms |
| 6. Scenes | `scenes/`, `common.py` | contact sheet at the end of every beat; no overlaps or clipped text |
| 7. Review | — | physics, visual and audio passes (checklists below) |
| 8. Build and publish | `out/`, `videos/`, release asset, README rows | stream check, duration, loudness; download link and checksum |

### 0. Scope

- Pick one source: lecture notes, a review, a paper, or your own study guide.
- Write down who the viewer is. All four videos here assume a final-year physics undergraduate.
- Write the goal sentences.
  - Topic 04: "A two-band band structure is a map from a torus to a sphere."
  - Topic 04: "Such a map must fold; the folds carry the Chern number."
  - Topic 04: "Signed area counts the Chern number, unsigned area gives the quantum volume."

### 1. Study and verify

- **Read until you can derive the key results yourself**, then write study notes in your own words (`notes/`).
- **Reproduce every number you intend to show.**
  - Topic 03 re-implemented the paper's NEGF solver and matches its currents to 1–2 %.
  - Topic 04's `verify/` checks every identity to 10⁻¹⁴ and the Gauss–Bonnet integrals to grid accuracy.
- **Write the convention ledger.** Topic 04's study guide has one on page 18.
- **List the open questions and the things you are unsure about.** These become the honest caveats in the video.

### 2. Plan

The plan is a short document that someone else could read and predict the video from. It contains:

1. **The one picture** and why it carries the story.
2. **A scene table**: scene, length, content, source (section or equation).
3. **The must-compute list.** These are the pictures where seeing beats reading (topic 04 had seven),
   with the data each one needs.
4. **The cut list**: what is deliberately left out, so that it does not creep back in.
5. **Model and conventions**, matching the ledger.
6. **A table of checked numbers**, with where each was checked.

Choose the format from the source. The same pipeline handles four formats:

| Format | Example | Shape of the story |
|---|---|---|
| Lecture-notes companion | 01 Keldysh | follows the notes, but adds a physical picture after every key formula |
| Concept map of a review | 02 Quantum geometry | one running example (a two-band model) carries many phenomena |
| Paper explainer with reproduction | 03 Nonlinear Hall in NESS | motivation, method, the reproduced key figure, where the simple picture breaks |
| One-picture narrative from a study guide | 04 Grassmannian | a puzzle, three acts that each ask one question of the same picture, then our proposal |

### 3. Narration

Rules that make the text work as speech and as a timing source:

- One idea per beat. Short sentences, under about 25 words.
- Introduce a symbol when the viewer first needs it, and say what it measures, not only its name.
- Write numbers and symbols as words: "three point two", "E over Gamma", "d P times d P".
  The sentence splitter cuts at `. ! ? ;`, so a written "3.2" breaks a beat in two.
- Wording is part of the physics review. Check:
  - "always" versus "generically";
  - "is" versus "is proportional to";
  - the sign and the factor of two;
  - which band, which convention.
- Estimate the length. Our voice speaks about 165–185 words per minute including pauses, so minutes ≈ words / 175.
  Topic 04's plan said 14 minutes; the text came out at 1775 words and the video at 10 minutes. That is fine.
  Padding to reach a planned length is not.

### 4. Data

- Put anything slower than a fraction of a second in `compute/make_data.py`, writing `data/*.npz`.
  Scenes only read these files.
- Print the checks when the script runs (Chern number, areas, convergence) so the log documents the data.
- Fix random seeds so the animation of an iterative algorithm is reproducible.
  Topic 04's SMACOF reconstruction uses fixed seeds and is compared against classical MDS.

### 5. Voice

```bash
python tts.py                                      # local Kokoro-82M, only changed beats are regenerated
python ../../pipeline/tools/check_tts.py           # Whisper back-transcription, lists beats with WER > 4 %
```

- **Names and jargon need pronunciation overrides**, for example `[Kähler](/kˈAləɹ/)`. Check them with Kokoro's G2P
  before generating (see [`PITFALLS.md`](PITFALLS.md)).
- **A misheard name shows up as the same wrong word in every beat that uses it.** Digits versus words and homophones
  ("Chern"/"churn") are harmless.
- **Topic 04's first version reached a 4.3 % word error rate over 1775 words**, which I read as formatting and
  homophones. One real error was among them: "ky" was read as one word (Whisper wrote "chi"). See the section by the
  author of topics 02 and 04 in `PITFALLS.md`.

### 6. Scenes

- **Use one scene per section of the plan, and one `with self.narrate(key)` block per beat.** Inside a beat, wait for
  sentences with `b.wait_sentence(i)` and size slow animations with `b.until_sentence(i)` or `b.remaining()`.
- **Use a fixed visual grammar for the whole video:**
  - one colour, one meaning;
  - the same object always in the same place (k-space on the left, state space on the right);
  - formulas in the same font as the narration's symbols.

  Topic 04's grammar:

  | Colour | Meaning |
  |---|---|
  | blue | face up |
  | red | flipped |
  | purple | metric |
  | yellow | fold |
  | green | proposal |
- **Draw 3D with the orthographic helpers** (`Sphere2D`, `Cam`, `mesh` in topics 02 and 04), so that 3D objects
  compose with 2D panels and formulas.
- **Preview at 480p, one scene at a time, and look at a contact sheet of the last frame of every beat:**
  `python build.py --quality l --only S05_Zoom` and `python tools/sheet.py S05_Zoom s05_zoom`.
  Most layout bugs only show up there.

### 7. Review

Three separate passes. Each one catches mistakes the others miss.

**Physics pass**
- Every number on screen matches the table of checked numbers.
- Every sign and factor of two matches the ledger.
- Every claim has its evidence class, and the class is visible where it matters (schematic, analogy, proposal).
- Statements about what a method cannot see are included. Example: distances alone do not give orientation.

**Visual pass**
- Contact sheets at the end of every beat and in the middle of long transitions.
- No overlapping labels.
- Nothing past the frame edge.
- Text no smaller than about 22 pt, because the picture is shrunk to 88 % for the subtitle band.

**Audio pass**
- The Whisper check.
- Pacing: no beat where the picture is idle for long while the voice runs, or the reverse.

### 8. Build and publish

```bash
python build.py                       # 1080p60 render in parallel, concatenation, loudness, SRT, burned-in subtitles
```

- **Check the output**: `ffprobe` for the streams and duration, `ffmpeg -af volumedetect` for loudness
  (we get about −19 dB mean and −1.5 dB peak after `loudnorm`).
- **Publish in this repository's layout**:
  - code and data in `topics/NN-name/`;
  - the `.srt` in `videos/`;
  - the MP4 as a release asset (never in git);
  - one row each in `README.md` and `videos/README.md`;
  - sources linked in `materials/`.

  After uploading, compare the asset's digest with the local file and open the download link once.

## Start a topic of your own

1. **Copy a reference topic.** Copy `tts.py`, `build.py`, `common.py` and `tools/` from `topics/04-grassmannian-quantum-geometry`
   (the most complete helpers) into `topics/NN-your-topic/`. Rename `NAME` and the scene list in `build.py`.
2. **Write the documents for stages 0–2**: goals, study notes, checks, plan.
3. **Write `narration.py`**, run `python tts.py`, then run the Whisper check.
4. **Write `compute/make_data.py`** if any picture needs real computation.
5. **Write the scenes** one at a time, previewing each at 480p.
6. **Run the review passes**, then `python build.py`.
7. **Add the README rows**, the subtitle file, and the release asset.

A typical 10-minute video renders at 1080p60 in about 10 minutes on 10 cores. Most of the time goes into
stages 1–2 and into the scene iterations of stage 6.

## Additions from the author of topics 01 and 03

> Written by Claude Opus 5.5 (Anthropic), the Claude Code session `f80d935c` that made topic 03
> (*Nonperturbative nonlinear Hall effect in NESS*) and topic 01 (*The Keldysh nonequilibrium Green's function
> technique*, versions 1 and 2). The full statement is in the last section of [`PITFALLS.md`](PITFALLS.md).
> Nothing above this section was changed.

### What we already do (applied in topics 01 and 03)

1. **Follow each key formula with a picture and a limit.** In a lecture-notes companion, the notes fix the order
   of the formulas. The video adds a picture right after each one, answering "what does this mean physically?".
   Where possible it also shows a limiting case the viewer already trusts:
   - Γ → 0 gives the master equation;
   - in equilibrium −iG^< = f·A (fluctuation–dissipation).

   This complements principle 2: the one picture carries the story, and the per-formula pictures carry the details.
2. **Give every key formula a knob.** The beats that worked best move one parameter and show the consequence.
   Each one is a `ValueTracker` driving a computed curve:
   - Γ broadening the Lorentzian;
   - E pushing the Fermi sea into the hot spot (topic 03);
   - the asymmetry Γ^L/Γ lowering the peak transmission;
   - Γ → 0 merging the Green's-function and master-equation currents;
   - three initial occupations relaxing to one steady value.
3. **Check the wording against the source before publishing.** Run `pipeline/tools/check_overlap.py` with your local
   copy of the source; only titles and citations may remain (see the last section of `PITFALLS.md`).

### Proposed changes (not yet applied to any topic)

These follow from the problems in the last section of `PITFALLS.md`. The reviewer should decide which to adopt.

1. **Get the plan approved and pilot one minute first.**
   - Stage 2's gate: the person who asked for the video reads the picture cards and says which formulas still feel
     opaque.
   - Stage 6 starts with one finished minute (voice, animation, subtitles) for approval.

   In topic 01, the switch from Chinese to English and the missing pictures were both found only after the full
   video had been rendered. These were the two most expensive rounds of rework.
2. **Make episodes shorter.** Aim for 6–8 minutes and one or two pictures per episode (Mayer's segmenting principle).
   Topic 01 version 2 is 15 minutes; it could be three episodes:
   - the contour and the components;
   - Langreth rules and the Keldysh equation;
   - transport.
3. **Leave room to think.**
   - After the key result of a scene, hold the picture still for one to two seconds (a longer `pad` for that beat).
   - End each scene with a one-sentence takeaway on screen.

   In topics 01 and 03 a beat ends 0.35 s after the voice.
4. **Sync to words, not sentences.** Whisper returns word timestamps. A helper such as `b.wait_word('lesser')` would
   make a highlight land when the word is spoken, instead of at the start of its sentence.
5. **Automate the gates.**
   - A layout check on the end-of-beat frames: boxes outside the safe area, overlapping labels, text below 22 pt.
   - Assertions in the scene code for every number the narration says.
   - A pacing report: words per minute, and new symbols per beat.
6. **Test the intuition, not only the facts.**
   - Give each topic three concept questions that can be answered from the pictures alone, for example "at μ = 0,
     why is Tr ñ exactly 1?".
   - Optionally, add an interactive page with the same sliders as the video.

## Additions from the author of topics 02 and 04

> Written by Claude Opus 5.5 (Anthropic), the Claude Code session `98f5ca3a` that made topic 02 (*Quantum geometry*)
> and topic 04 (*Quantum geometry on the Grassmannian*, versions 1 and 2), and the first versions of this file,
> `PITFALLS.md` and `pipeline/tools/check_tts.py`. Above this section I changed one sentence of my own (stage 5);
> nothing written by another author was changed. The details are in my section of [`PITFALLS.md`](PITFALLS.md).

### What a viewer review found

The repository owner watched topic 04, version 1, and wrote down 19 places where they got lost, each with a
timestamp. My three review passes (physics, visual, audio) had found none of them, because each pass checks what is
on screen: whether it is correct, readable and well pronounced. None of them checks what is missing. The notes fall
into six groups:

| What was missing | Examples in topic 04, version 1 |
|---|---|
| a definition | the map `n(k) = d/\|d\|`; det g; the word "sheet"; the parameter m |
| a key to a picture | the distance-table image had no axes or colour bar; the cos θ_K bar showed only ±1 |
| the meaning of a number | +1, +1, −1 next to the sheets were read as Chern numbers |
| a mark on the picture | ϑ, D_HS and d_FS were in formulas but not on the sphere; u and v were drawn as two separate angle diagrams, not as directions inside the two planes |
| the problem before the device | the surface (s, t², εt) appeared before the problem it solves |
| pictures in the summary | the three closing cards were text only |

Version 2 answers every note in the video itself, and runs 14.6 minutes instead of 10.1. Stage 3 above calls the
shorter version 1 "fine". In hindsight, the four minutes it saved were these missing steps.

### Proposed changes

1. **Make a viewer test the last gate of stage 7.** Someone who has not read the plan watches the whole video and
   writes down every moment they could not follow, with the time. Each note is answered in the video, or listed in
   the topic README as deliberately left out. This complements the one-minute pilot proposed by the author of
   topics 01 and 03: the pilot catches problems of form early, the viewer test catches missing steps at the end.
2. **Add a first-use table to the plan (stage 2).** One row for every symbol, parameter, word of jargon and number
   that will appear on screen: the beat where it is defined, its formula or meaning, and where it is marked on the
   picture. A row without a defining beat is a gap. Version 1 of topic 04 would have failed on `n(k)`, m, det g,
   "sheet", the signs ±1 and the colour scale of cos θ_K.
3. **Give every image a key.** Axes with labels, a colour bar built from the image's own colour map, and one entry
   explained in words.
4. **Say what kind of number a number is.** "Orientation signs, not Chern numbers"; "in spheres: one sphere has
   area π".
5. **State the problem before the device.** On screen: what goes wrong, the simplest case where it goes wrong, then
   the fix.
6. **Name a shape only after computing it.** Count its cusps and compute its area; show it once from a camera that
   sees all of it.
7. **End with pictures.** The summary of each act shows that act's key picture.
8. **In the Whisper check, treat an unexplained word as an error** until the phonemes (Kokoro's G2P) explain it.
9. **Show every invariance by varying what it is invariant under**, with the invariant on screen.
10. **Label every piece of a partition**, and say what each piece covers.

A second viewer review, of version 2, found five more gaps, all relations that were stated but not shown (my section
of `PITFALLS.md`, "the second review"). Version 2.1 answers them. Proposals 9 and 10 come from that review.

## References

- G. Wiggins and J. McTighe, *Understanding by Design* (ASCD, 1998; 2nd ed. 2005). Backward design: start from the goals.
- J. Sweller, *Cognitive load during problem solving: effects on learning*, Cognitive Science **12**, 257–285 (1988).
  Working memory is the bottleneck; sequence material and remove what does not serve the goal.
- R. E. Mayer, *Multimedia Learning*, 3rd ed. (Cambridge University Press, 2020). Evidence-based principles:
  - coherence, signalling, redundancy;
  - spatial and temporal contiguity;
  - segmenting, pre-training;
  - modality, personalisation, voice.

  The voice principle favours a human voice. We use a local synthetic voice because it can be regenerated whenever a
  sentence changes, and we check it with back-transcription.
- E. R. Fyfe, N. M. McNeil, J. Y. Son and R. L. Goldstone, *Concreteness fading in mathematics and science instruction:
  a systematic review*, Educational Psychology Review **26**, 9–25 (2014). Concrete first, then fade towards the abstract.
- [Manim Community](https://docs.manim.community/), [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M),
  and the 3Blue1Brown videos by Grant Sanderson that this style comes from.
