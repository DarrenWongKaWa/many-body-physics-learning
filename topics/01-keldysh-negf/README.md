# 01 · The Keldysh nonequilibrium Green's function technique

A 15-minute 3Blue1Brown-style explainer that follows A.-P. Jauho's lecture notes
*Introduction to the Keldysh nonequilibrium Green function technique* and adds a physical picture after every key formula.
The notes themselves are not included here (see [`materials/`](../../materials/README.md)); the narration is written from scratch.

**Watch:** [`01-keldysh-negf.mp4`](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/01-keldysh-negf.mp4) · subtitles: [`videos/01-keldysh-negf.srt`](../../videos/01-keldysh-negf.srt)

## Scenes

| Scene | Formalism (as in the notes) | Physical picture added |
|---|---|---|
| S01 | quantum dot under bias, roadmap | |
| S02 | S-matrix, Gell-Mann–Low, Wick, connected diagrams | |
| S03 | why the state never returns → Keldysh contour, imaginary-time leg, t₀ → −∞ | closed loop: U(t₀,t)U(t,t₀) = 1, so no denominator and no vacuum bubbles |
| S04 | contour-ordered G, four components, G^r − G^a = G^> − G^< | G^r = spectrum, G^< = occupation; fluctuation–dissipation locks them in equilibrium and unlocks out of it |
| S05 | Langreth theorem: contour deformation, rules table, e–ph self-energy | a product is a path from the ket branch to the bra branch that switches exactly once |
| S06 | Keldysh equation, G^< = G^r Σ^< G^a | occupation = injection rate × dwell time; the initial-state memory decays as e^{−Γt/ħ} (exact n(t)) |
| S07 | partitioned tunnelling model H = H_c + H_T + H_cen | |
| S08 | current formula, proportional coupling, bias window | in-flow − out-flow ledger (Pauli factors cancel); two counter-flowing streams per energy |
| S09 | non-interacting resonant level, f̄, Breit–Wigner transmission, I–V step | decay in time ↔ Lorentzian; the dot copies the last lead that touched it; T = 1 on resonance; series bottleneck |
| S10 | master equation and comparison with the Green's-function result | level outside the window: thermal activation e^{−d/kT} vs quantum tails Γ²/d² |
| S11 | summary | inject → propagate with a finite lifetime → occupation set by kinetics |

All curves in S06, S09 and S10 are computed on the fly from wide-band-limit formulas in `common.py`
(`current_gf`, `current_me`, `occupation_relax`).

## Files

| File | Role |
|---|---|
| `narration.py` | `SCRIPT_EN`: English narration, one entry per animation beat (an older Chinese `SCRIPT` is kept for reference) |
| `tts.py` | local TTS with Kokoro-82M (voice `af_bella`); writes `audio/af_bella/*.wav` plus per-sentence timings |
| `common.py` | colours, `narrate()` audio sync, contour drawing, resonant-level physics |
| `i18n_en.py` | English on-screen labels for scenes written with `zh(...)` |
| `scenes/` | Manim scenes |
| `build.py` | parallel render → concatenate → loudness-normalise → subtitles → burn subtitles |

## Build

From this folder, with the environment described in [`pipeline/`](../../pipeline/README.md):

```bash
python tts.py --lang en --voice af_bella                    # narration (only changed beats are regenerated)
python build.py --lang en                                   # 1080p60 + out/keldysh_en_subtitled.mp4
python build.py --lang en --quality l --only S06_Keldysh    # quick 480p preview of one scene
```
