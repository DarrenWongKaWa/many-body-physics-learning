# 02 · Quantum geometry in condensed matter

A 13-minute 3Blue1Brown-style explainer based on the review
A. Gao, N. Nagaosa, N. Ni, S.-Y. Xu, *Quantum geometry phenomena in condensed matter systems*,
Rev. Mod. Phys. **98**, 035005 (2026) — [arXiv:2508.00469](https://arxiv.org/abs/2508.00469).
The review is not included here; the narration is written from scratch.

**Watch:** [`02-quantum-geometry.mp4`](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/02-quantum-geometry.mp4) · subtitles: [`videos/02-quantum-geometry.srt`](../../videos/02-quantum-geometry.srt)

## Scenes

| Scene | Content | Where in the review |
|---|---|---|
| S01 | bands and the Bloch sphere; quantum geometric tensor = metric − (i/2) Berry curvature | Sec. I, Fig. 1 |
| S02 | rays, parallel/perpendicular split, metric, Berry connection and curvature | Sec. II.A |
| S03 | two-band picture: distance ↔ metric, solid angle ↔ curvature; atomic insulator vs band inversion | Fig. 1 |
| S04 | the whole Brillouin zone mapped onto the sphere; Chern number = wrapping number; tr g ≥ \|Ω\| | — |
| S05 | quantum Fisher information = 4g; measuring the metric with quenches; qubit and polariton experiments | Sec. II.B, V |
| S06 | wave-packet dynamics, anomalous velocity, AHE/QAH/FQAH, valley/spin/layer Hall, Berry curvature dipole | Sec. III.A, IV |
| S07 | field-induced Berry connection, Berry-connection polarizability; two routes to suppress the Drude term | — |
| S08 | quantum-metric-dipole nonlinear Hall effect: symmetry table, picture, MnBi₂Te₄ / black phosphorus evidence, third-order Hall | Sec. V.C |
| S09 | flat-band superconductivity: the D_s ∝ n_s/m* puzzle, geometric superfluid weight, Wannier-spread bound, TBG | Sec. III.F, V.B |
| S10 | Souza–Wilkens–Martin sum rule, optical-gap bound, ARPES quasi-QGT | — |
| S11 | summary and outlook | Sec. VI |

## What is computed and what is schematic

- **Computed:** the Bloch-sphere maps, distance/area read-outs, Berry curvature and tr g heat maps, Chern number and
  ∫ tr g / 2π = 1.43 for the QWZ model at m = 1 in S03–S04 come from `common.geometry()`
  (two-band formulas g = ¼ ∂n·∂n, Ω = −½ n·(∂ₓn × ∂ᵧn)).
- **Schematic (labelled on screen):** the measurement distributions and polariton g(k) in S05, the Drude/metric bars in S07,
  the sign-flip sketch in S08, the D_s bars in S09 and the absorption spectrum in S10. They show qualitative relations only.

## Files

`narration.py` (English narration), `tts.py` (Kokoro-82M, voice `af_bella`), `common.py` (style, `narrate()` sync,
two-band geometry, an orthographic Bloch sphere `Sphere2D`), `scenes/`, `build.py`, `tools/burn_subs.py`, `tools/sheet.py`.

## Build

From this folder, with the environment described in [`pipeline/`](../../pipeline/README.md):

```bash
python tts.py                                   # narration (only changed beats are regenerated)
python build.py                                 # 1080p60 + out/qgeom_en_subtitled.mp4
python build.py --quality l --only S04_Wrap     # quick 480p preview of one scene
python tools/sheet.py S04_Wrap s04_wrap         # contact sheet of that preview
```
