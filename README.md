# Many-body physics, learned through animation

A personal study repository for many-body and nonequilibrium condensed-matter physics.
Each topic pairs a source text (lecture notes, a review, a paper) with a 3Blue1Brown-style explainer video
that is generated from code. The scripts, the calculations behind every curve, and the whole production
pipeline are included, so any video can be edited and rebuilt.

## Learning path

| # | Topic | Source | Video | Code |
|---|---|---|---|---|
| 01 | The Keldysh nonequilibrium Green's function technique: contour, Langreth rules, Keldysh equation, current through a quantum dot, master equation | A.-P. Jauho, lecture notes | [watch (15 min)](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/01-keldysh-negf.mp4) | [`topics/01-keldysh-negf`](topics/01-keldysh-negf) |
| 02 | Quantum geometry: quantum metric, Berry curvature, quantum geometric tensor and their phenomena | Gao, Nagaosa, Ni, Xu, Rev. Mod. Phys. 98, 035005 (2026) | [watch (13 min)](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/02-quantum-geometry.mp4) | [`topics/02-quantum-geometry`](topics/02-quantum-geometry) |
| 03 | Nonperturbative nonlinear Hall effect in nonequilibrium steady states (uses 01 and 02, with a reproduction of the paper's NEGF calculation) | Geng et al., arXiv:2607.01519 | [watch (10 min)](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/03-nonlinear-hall-ness.mp4) | [`topics/03-nonlinear-hall-ness`](topics/03-nonlinear-hall-ness) |

Links to the source texts are in [`materials/`](materials/README.md); the texts themselves are not redistributed here.
Subtitles are in [`videos/`](videos/README.md).

## How the videos are made

[Manim](https://www.manim.community/) for the animation, [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) for the narration
(runs locally), ffmpeg for assembly, and a small amount of glue that keeps the animation in sync with the voice and
burns in subtitles. The full workflow, environment setup and pitfalls are in [`pipeline/`](pipeline/README.md).

## Layout

```
materials/   links to the source texts
pipeline/    how the videos are made
videos/      subtitles and links to the MP4 files (attached to the GitHub release)
topics/NN-*/ one self-contained project per video: narration, scenes, physics code, build script
```
