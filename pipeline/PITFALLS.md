# Pitfalls we hit

Every entry happened while making videos 01–04. Each one has the same three parts:
- **Symptom:** what you see;
- **Cause:** why it happens;
- **Fix:** what to do about it.

The workflow these belong to is in [`METHOD.md`](METHOD.md); the commands are in [`README.md`](README.md).

## Environment and tools

- **LaTeX errors on the first `MathTex`.**
  - Cause: BasicTeX lacks two packages Manim needs.
  - Fix: `tlmgr init-usertree && tlmgr --usermode install standalone preview`, and `brew install dvisvgm`.
- **ffmpeg stops with a missing dynamic library** after a Homebrew upgrade (for example x265).
  - Fix: `brew upgrade ffmpeg`.
- **There is no way to burn subtitles with ffmpeg filters.**
  - Cause: Homebrew's ffmpeg is built without libass and drawtext.
  - Fix: `tools/burn_subs.py` draws each cue with Pillow and overlays the PNGs with the concat demuxer.
- **A zsh command dies with "no matches found".**
  - Cause: a glob matched nothing, or a word such as `====` started with `=`.
  - Fix: use `find ... -delete` in scripts, and quote such words.
- **A long computation makes the machine busy without explanation.**
  - Fix: say up front what runs in the background and for how long. Topic 03's NEGF datasets take about 35 minutes
    on all cores.

## Voice (Kokoro TTS)

- **Names and jargon come out wrong.**
  - Fix: check the phonemes before generating:
    `next(KPipeline(lang_code='a', repo_id='hexgrad/Kokoro-82M', model=False)(word)).phonemes`.
  - Then override inline with misaki IPA. Overrides we needed:

    | Word | Override |
    |---|---|
    | Wannier | `[Wannier](/vˈɑnjA/)` |
    | Brillouin | `[Brillouin](/bɹilwˈæn/)` |
    | Néel | `[Néel](/nAˈɛl/)` |
    | Kähler | `[Kähler](/kˈAləɹ/)` |
    | Bargmann | `[Bargmann](/bˈɑɹɡmən/)` |
    | Fubini | `[Fubini](/fubˈini/)` |
    | Study | `[Study](/ʃtˈudi/)` |
    | Gauss | `[Gauss](/ɡˈWs/)` |
    | Bonnet | `[Bonnet](/bɔnˈA/)` |
    | Euler | `[Euler](/ˈYləɹ/)` |
    | Huang | `[Huang](/hwˈɑŋ/)` |
    | Qi | `[Qi](/ʧˈi/)` |
    | Zhang | `[Zhang](/ʤˈɑŋ/)` |
    | Giataganas | `[Giataganas](/jˌɑtəɡˈɑnəs/)` |
    | Weyl | `[Weyl](/vˈIl/)` |
    | Moyal | `[Moyal](/mˈYəl/)` |
    | Dirac | `[Dirac](/dɪɹˈæk/)` |
    | polariton | `[polariton](/pəlˈɛɹɪtˌɑn/)` |
    | skyrmion | `[skyrmion](/skˈɜɹmiˌɑn/)` |
- **A beat is cut in the wrong place, or the animation waits for a sentence that never comes.**
  - Cause: the splitter cuts at `. ! ? ;` followed by a space, so "3.2" or "e.g." splits a sentence.
  - Fix: write numbers as words and avoid abbreviations.
- **You cannot listen to every take.**
  - Fix: `pipeline/tools/check_tts.py` transcribes the audio back with Whisper and lists the beats that differ.
  - Formatting differences ("3.2" against "three point two") and homophones ("Chern"/"churn") are harmless.
  - A real mispronunciation shows up as the same wrong word every time.
- **The video is much shorter or longer than planned.**
  - Fix: measure instead of guessing. The voice runs at 165–185 words per minute with pauses, and the manifest has
    every beat's duration.
- **Viewers never saw the subtitles.**
  - Cause: soft `mov_text` subtitles are off by default in most players.
  - Fix: burn them in, in a band below the shrunk animation.

## Manim

- **Parallel renders fail at random on LaTeX.**
  - Cause: they share the Tex cache.
  - Fix: `build.py` gives each scene its own `--media_dir`.
- **`\'` inside a raw string becomes an accent command.**
  - Fix: write `r"G(x,t;x',t')"` with double quotes.
- **`\;` inside `Tex` breaks Manim's string splitting.**
  - Fix: use `\quad` or plain spaces.
- **`plot_line_graph` returns a `VDict`.**
  - Fix: take `['line_graph']` before wrapping it in `DashedVMobject`.
- **`TypeError: Only values of type VMobject can be added`.**
  - Cause: an `ImageMobject` (heat map) is inside a `VGroup`.
  - Fix: use `Group` for anything that mixes images and vectors.
- **`LaggedStartMap(GrowArrow, group)` fails with a colour-parsing error.**
  - Fix: write `LaggedStart(*[GrowArrow(a) for a in group])`.
- **Painter's order breaks after an animation.** Faces that should be hidden end up in front.
  - Cause: animating submobjects of a depth-sorted group (for example one `Restore` per face in a `LaggedStart`)
    re-adds each one as a top-level mobject in animation order.
  - Fix: reveal with an updater on the whole group that sets opacities, and keep the group's order.
- **An object jumps when a later part of the scene runs.**
  - Cause: `always_redraw` closures capture variables by reference, so reassigning a variable they use (such as a
    new `sph`) changes the old drawing too.
  - Fix: call `clear_updaters()` on the old mobject first, or use a new variable name.
- **Moving a group leaves some of its parts behind.**
  - Cause: the parts are `always_redraw` objects built from fixed coordinates.
  - Fix: build them at their final positions, or drive the position with a `ValueTracker`.
- **Rendering is slow.**
  - Cause: static `wait()` frames are cheap; per-frame redraws of meshes or many `Tex` objects are not.
  - Fix: precompute meshes for a still camera, prefer `DecimalNumber` to re-typeset `MathTex`, and keep heavy numerics
    in `compute/`.

## 3D on a 2D canvas

- **3D objects do not sit well next to 2D panels and formulas.**
  - Cause: `ThreeDScene` makes this awkward.
  - Fix: use the orthographic helpers (`Sphere2D`, `Cam`, `mesh`, `polyline3d` in topics 02 and 04). They project to 2D,
    shade, sort faces by depth, and draw back faces faint.
- **Coincident sheets flicker or show stripes.** In topic 04, three sheets cover the same polar cap.
  - Fix: lift the sheet that should be seen by a few percent along the normal, and give it draw-on-top priority
    (`mesh(..., on_top=...)`).
- **Large faces cover nearer small ones.**
  - Cause: sorting faces by centroid depth fails for faces of very different size.
  - Fix: use a finer mesh or explicit priorities.
- **NaN on a geodesic.**
  - Cause: the great circle between antipodal points is not unique.
  - Fix: never `slerp` between antipodes; draw full great circles by rotating about an axis.

## Layout

- **An overlap only shows up in a contact sheet.** Examples:
  - a panel title on top of the `k_y` axis label;
  - a long formula running past the frame edge (|x| > 7.1);
  - a label sitting on a moving point cloud;
  - two labels converging as two points approach each other.
  - Fix: take a contact sheet at the end of every beat and look at it; fade a label out when its anchor gets crowded.
- **Small text is unreadable in the final video.**
  - Cause: the burned-in subtitle band shrinks the picture to 88 %.
  - Fix: keep on-screen text at 22 pt or more.

## Physics and mathematics

- **A sign that does not match the source.**
  - Cause: conventions differ between papers. Huang's H2 and H3 define the Berry curvature with opposite signs.
    In topic 04, the band we follow has Chern number +1, but its map to the sphere has degree −1.
  - Fix: keep a convention ledger. Show the exact signed formula on screen. Where only relative orientation matters,
    say "face up relative to the majority sheet" instead of committing to an absolute sign.
- **A factor of two that a sharp viewer will catch.** Examples:
  - Huang's metric is twice the standard one: sphere radius 1/√2 and curvature 2, instead of 1/2 and 4.
  - A tangent arrow transported around a loop turns by the full solid angle, while the state's Berry phase is half
    of it.
  - The Bloch-sphere angle between two states is twice their principal angle.
  - Fix: write each one into the ledger and say it out loud where it matters.
- **Overclaiming.** Examples: "generically" written as "always"; "is proportional to" written as "is"; a local
  statement presented as a global one.
  - Fix: do a physics pass that reads only the narration, sentence by sentence.
- **A method shown without its blind spots.**
  - Example: multidimensional scaling of a distance table rebuilds a shape, but cannot see orientation or how many
    times a region is covered.
  - Fix: say so on screen. It motivates the next step.
- **A schematic that looks like data.**
  - Fix: label it "(schematic)" on screen, and in the README say what is computed and what is not.
- **The reproduction does not agree with the paper.**
  - Fix: report it in the topic README with the most likely reasons, and choose a picture that is correct either way
    (topic 03, Tr ñ).

## Data and numerics

- **An iterative algorithm stalls.**
  - Example: SMACOF from a random start can sit in a local minimum for a nearly flat shape (topic 04's trivial cap).
  - Fix: more iterations, several seeds, and a comparison with a closed-form result (classical MDS).
- **Finite differences blow up at degeneracies or folds.**
  - Fix: use analytic derivatives (topic 04's `qwz_geom`, `verify/`), and mask near-singular points when comparing.
- **A numerical integral has the wrong value.**
  - Fix: sample at cell centres (half-step offset) and check the result against a known invariant, such as a Chern
    number that must come out as an integer.

## Publishing

- **The repository grows by hundreds of megabytes.**
  - Fix: MP4 and WAV files are git-ignored. Videos go to the GitHub release (`gh release upload v1.0 file.mp4`).
- **The released file is not the local one.**
  - Fix: compare `shasum -a 256` with the asset's digest (`gh release view v1.0 --json assets`), and request the
    download URL once (it should answer with a redirect).
- **Source PDFs end up in the repository.**
  - Fix: `*.pdf` is ignored except for our own compiled guides. Link the sources in `materials/README.md`.
- **The tables disagree with each other.**
  - Fix: one video touches the topic README, the root `README.md`, `videos/README.md`, the subtitle file and the
    release notes. Update them in the same commit.
