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
- **Coincident sheets flicker or show stripes.** In topic 04, three sheets cover the same region near the north pole.
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

## Added by the author of topics 01 and 03

> **Who wrote this section.** Claude Opus 5.5 (Anthropic), working as a coding agent for the repository owner in
> one Claude Code session (`f80d935c`). In that session I made:
> - **topic 03**, *Nonperturbative nonlinear Hall effect in NESS* (10 min), including the NEGF solver `compute/negf.py`;
> - **topic 01**, *The Keldysh nonequilibrium Green's function technique*: version 1 (10.7 min) followed the notes;
>   version 2 (15.1 min) added twelve physical-picture beats after the owner's review;
> - the first layout of this repository, the first version of `pipeline/README.md`, `tools/burn_subs.py` in topics 01
>   and 03, and `pipeline/tools/check_overlap.py`.
>
> Topics 02 and 04, the sections above and `pipeline/tools/check_tts.py` were written in other sessions; I have not
> changed them. Below are only problems that are not already listed above.
> My checks were back-transcription and sampled frames: I cannot hear the audio or watch a video the way a viewer does.
> The most important problem below, the first one, was found by the owner, not by me.

### Teaching and intuition

- **The video is correct, but it does not build intuition.**
  - Example: topic 01, version 1. The owner, who knows the subject, said most physical pictures were missing.
  - Cause: the narration was planned from the derivation in the source. Each formula was explained through the
    previous formula, never through something the viewer can picture.
  - Fix: give every key formula a picture card before writing any narration: the question it answers, the picture,
    the formula, a limiting case, and one sentence to remember. Topic 01 version 2 is the result. For example:
    - lesser function = how full the states are;
    - Langreth rule = a path that switches branch exactly once;
    - Keldysh equation = injection rate × dwell time;
    - current = in-flow minus out-flow.

    Show the cards to the person who asked for the video before animating anything.
- **The voice reads a formula symbol by symbol.**
  - Example: "C lesser equals A retarded times B lesser, plus A lesser times B advanced" (topic 01, beat `la5`).
    It is still in the video.
  - Cause: the formula was turned into a sentence instead of an idea.
  - Fix: the screen shows the formula; the voice says what it means and which part to look at.
- **Too many new symbols at once.**
  - Example: topic 01 scene S04 introduces G_c, G_c̃, G^>, G^<, G^r and G^a within about a minute.
  - Fix:
    - at most one new symbol every 20–30 seconds;
    - one colour per symbol, kept across scenes and videos (topic 01: retarded blue, advanced orange, lesser green).
- **The voice repeats a quantitative claim from the source that the computed picture does not show.**
  - Example: topic 03's first draft said that the excitations at μ = 0 sit about E/Γ from the nodes, as the paper
    states. In the computed Δn₊ map the peak moves by only about half of that.
  - Cause: the narration was drafted from the paper before the data existed.
  - Fix: write the narration's numbers after the data exist. Check every "about", "twice" and "exponentially"
    against the plot it accompanies.
- **One picture belongs to two evidence classes.**
  - Example: "each lead resets the dot, and the dot copies the last lead that touched it" (topic 01, beat `re3b`).
    It is exact for the master equation, but only an analogy for the coherent Green's-function result.
  - Fix: say in which framework the picture is exact. **The current topic 01 video does not say this yet.**

### Voice

- **The package resolver picks an ancient `transformers`.**
  - Symptom: installing `kokoro` and `misaki[zh]` in one command with the rest of the stack selected transformers
    4.12, which needs a Rust build of `tokenizers`, and the install failed.
  - Fix: require `transformers>=4.40`, as `requirements.txt` does.
- **Mandarin narration with English terms and Greek letters.** (The Chinese scripts are kept in topics 01 and 03.)
  - Kokoro-82M-v1.1-zh reads English words through an English G2P callback. Single letters and Greek symbols are
    unreliable.
  - Fix:
    - write symbols as Chinese words (伽马, 德尔塔, "E 除以伽马");
    - transliterate names (凯尔迪什, 朗格雷斯);
    - expect the back-transcription to report homophones that are not errors (星积/星基, 电场/电厂).
- **Translating a finished video breaks its timing.**
  - Cause: scenes wait for the i-th sentence (`b.wait_sentence(i)`) and size animations from the time left in a beat.
  - Fix:
    - keep the same number of sentences per beat in every language, and check it with a script before generating audio;
    - clamp every duration computed from the voice, e.g. `max(0.5, b.remaining() - 0.3)` (`b.rest()` in topic 01).

      Two run times in topic 03 were unclamped and had to be guarded before the English build.

### Layout and translation

- **English labels overflow where the Chinese ones fitted.**
  - Examples:
    - topic 03 S08: the question "No Fermi surface: where does the current come from?" ran past the right edge in the
      first English 1080p build;
    - topic 01 S08: `scale_to_fit_width` shrank a note to about 65 %.
  - Fix:
    - design in the final language;
    - if a translation dictionary is used (`i18n_en.py`), fail on missing keys (an empty table cell was one of them);
    - wrap long labels with `\\` instead of shrinking them;
    - run the visual pass again on the translated version.
- **A frame taken during a transition looks like a layout bug.**
  - Example: a highlight box in topic 01 S05 looked misplaced. It was halfway between two terms.
  - Fix: take review frames near the end of each beat, at t₀ + 0.9 × duration:
    - t₀ is the beat's start, in `media/sublog*/<Scene>.json`;
    - the duration is in `audio/<voice>/manifest.json`.
- **zsh does not split an unquoted variable into words.**
  - Symptom: `set -- $spec` in a frame-sampling loop received a single word.
  - Fix: use separate variables or `${=spec}`.

### 3D

- **A clipped surface has a jagged rim.** (Topic 03, band structure.)
  - Cause: faces above an energy cap were deleted, so the rim follows the grid.
  - Fix: parametrise the region radially so that the rim is a grid line, and put special points (the cone tips) on
    grid vertices.

### Data and numerics

- **Reading numbers off a paper's figure.**
  - Vector figures: read the marker positions from the PDF (`pymupdf`, `page.get_drawings()`) and calibrate with the
    tick labels (`page.get_text('dict')`). This is exact (topic 03, Fig. 2(c,d)).
  - Raster figures:
    - mask by colour and calibrate with the gridlines;
    - mask the legend;
    - draw known curves analytically instead of tracing them, e.g. the dashed equilibrium Fermi function in Fig. 3(d).
- **One bad column sets the colour scale.**
  - Example: an off-by-one in topic 03's trajectory sampling never recorded κ_x = −π. The map's minimum became 0 and
    the colour scale was useless.
  - Fix:
    - in the code: `ik = (s // m_sub) % Nkx`;
    - in general: set colour limits from percentiles of the displayed region, and look at a raw map's edges once.

### Publishing

- **The narration repeats the source's wording.**
  - Fix: run `pipeline/tools/check_overlap.py` with your local copy of the source.
    - It lists passages of ten or more words shared with the topic's narration, labels and documents.
    - Only titles and citations should remain.
    - Topic 01 had one such phrase. It was reworded and the scene re-rendered before publishing.
- **Third-party material other than the PDF.**
  - Crops of a paper's figures (used for digitising) and full-text extractions (`paper.txt`) are also the source's
    content.
  - Fix: keep them in the ignored `ref/` folder.
- **A commit needs an identity, and the global git config is empty.**
  - Fix: set `user.name` and `user.email` for this repository only, with the GitHub noreply address, so no personal
    email is published.

## Added by the author of topics 02 and 04

> **Who wrote this section.** Claude Opus 5.5 (Anthropic), working as a coding agent for the repository owner in
> one Claude Code session (`98f5ca3a`). In that session I made:
> - **topic 02**, *Quantum geometry* (13 min), from the review by Gao, Nagaosa, Ni and Xu;
> - **topic 04**, *Quantum geometry on the Grassmannian*: version 1 (10.1 min), then version 2 (14.6 min) after the
>   owner's review;
> - the first versions of `METHOD.md`, this file and `pipeline/tools/check_tts.py`.
>
> Above this section I corrected two statements of my own that version 2 proved wrong (the "polar cap" in *3D on a 2D
> canvas*, and the stage 5 claim in `METHOD.md` that topic 04's audio passed the Whisper check). Nothing written by
> another author was changed. The teaching problems below were found by the owner, who watched version 1 and listed
> 19 places where they got lost; I found none of them in my own review passes. The topic 04 README maps each note to
> its fix.

### Teaching: what the viewer could not find

- **A map is shown but never written down.**
  - Example: "How does a momentum land on the Bloch sphere? What is the formula?" Version 1 painted the zone onto
    the sphere cell by cell, but `n(k) = d(k)/|d(k)|` never appeared.
  - Fix: write the formula, follow one point through it (Γ → X → M → Γ in both pictures), and say where two or three
    anchor points land and why (Γ: d points down, south pole).
- **A parameter value appears without its role.**
  - Example: "What is m = 3.2? It seems unrelated to everything before." Version 1 named the trivial band only by
    its value.
  - Fix: before using a value, show the parameter on an axis with its regimes (C = 1 for 0 < m < 2, C = 0 for
    m > 2) and what changes at the boundary.
- **A symbol is in the formula but not on the picture.**
  - Example: "θ, D_HS and d_FS do not show up on the sphere."
  - Fix: mark every symbol of a formula on the picture (the angle at the centre, the arc, the chord) and, if it
    changes, show its live value.
- **An image has no axes and no colour scale.**
  - Example: "I cannot tell what the black-and-white image means" (the table of 484 × 484 distances).
  - Fix: label the rows and columns, add a colour bar that says what both ends mean, and explain one marked entry
    and the diagonal.
- **A colour bar hides the values that carry the story.**
  - Example: "The map went from two colours to shades. What do the shades mean?" The bar showed two blocks, +1 and
    −1, while the map's dark band (cos θ_K ≈ 0) was the point.
  - Fix: build the bar from the same colour map as the image, with its middle value labelled.
- **A number next to an object is read as a different kind of number.**
  - Example: the signs +1, +1, −1 next to three sheets were read as Chern numbers, with "no reason given" for them.
    They are orientation signs.
  - Fix: say what kind of number it is and what it is not ("orientation signs, not Chern numbers"), and show where
    each object comes from (here, the regions of the zone around X, Y and M).
- **A count is named but not defined.**
  - Example: "count every sheet" and "count with signs": the viewer could not tell what a sheet is, or how the two
    counts are related.
  - Fix: define the word ("a piece of the zone laid down once"), write each count as a formula next to its name,
    and show the arithmetic that links them (1.189 = 1 + 2 × 0.0945).
- **A new quantity is used before it is defined.**
  - Example: "What is det g?" Version 1 first said it at the fold, as "the determinant of the metric", and never
    said what it measures.
  - Fix: one line of meaning at first use (det g = λ₁λ₂, the factor by which the map magnifies area). Search the
    narration and the scenes for the first use of every symbol.
- **A device is shown without the problem it solves.**
  - Example: "It looks like we added a parameter, but neither the problem nor why this is the answer is clear"
    (the surface (s, t², εt)).
  - Fix: three steps on screen: what goes wrong (a fold needs a direction of motion that stops changing the state),
    the simplest case where it goes wrong ((s, t²)), then the fix ((s, t², εt)).
- **The summary is text only.**
  - Example: "The three stories could each have a representative picture underneath."
  - Fix: end with the key picture of each act next to its words.

### Correctness

- **A shape named after how it looked from one camera.**
  - Example: version 1 said the north-pole region is "a polar cap covered three times", and my first version 2 draft
    called it a curved triangle. The image of the fold has four cusps (on the diagonals, at n_z = 1/√3), so the
    region is a four-pointed star.
  - Cause: from the camera of the painted sphere only two or three cusps are visible.
  - Fix: compute the shape's invariants (cusps, area) before naming it, and show it once from a camera that sees
    all of it (S07 now looks from 63° elevation).

### Voice

- **A two-letter symbol read as one word.**
  - Example: "k y" written as "ky" was read as one syllable in three beats of version 1. The Whisper check printed
    "chi" there, and I filed it under formatting.
  - Fix: write symbols letter by letter in the narration ("delta k x delta k y"). In the check, treat every word
    that is neither in the script nor a different spelling of a number as an error until you have explained it.

### Manim

- **A live readout or a redrawn object shows an old state.**
  - Example: topic 04 version 2, S03: the chord was drawn to the antipode and the readout said ϑ = 1.569 while
    v sat at ϑ = 0.65.
  - Cause: `always_redraw` objects are refreshed only by updaters. `FadeIn` suspends the updaters of what it fades
    in, and a `wait()` without time-based updaters is a frozen frame, so an object keeps the state it had when it was
    created, here with the tracker at an earlier value.
  - Fix: call `.update()` on such objects right before adding or fading them in.
- **A label lands on the wrong side.**
  - Example: `next_to(axis_end, UR)` put the √λ₁ label inside the ellipse, because the eigenvector happened to
    point the other way.
  - Fix: place labels from the geometry: beyond the end of an axis, or perpendicular to a chord on the side away
    from other labels.
