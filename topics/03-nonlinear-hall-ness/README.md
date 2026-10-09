# 03 · Nonperturbative nonlinear Hall effect in nonequilibrium steady states

A 10-minute 3Blue1Brown-style explainer of
L. Geng, M. Eckstein, L. Chen, S. Sur, S. Paschen, Q. Si, P. Werner,
*Nonperturbative Nonlinear Hall Effect in Nonequilibrium Steady States*, [arXiv:2607.01519](https://arxiv.org/abs/2607.01519).
It puts topic 01 (steady-state Green's functions) and topic 02 (Berry curvature) to work.
The paper is not included here; the narration is written from scratch.

**Watch:** [`03-nonlinear-hall-ness.mp4`](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/03-nonlinear-hall-ness.mp4) · subtitles: [`videos/03-nonlinear-hall-ness.srt`](../../videos/03-nonlinear-hall-ness.srt)

## Scenes

S01 hook · S02 Hall effect, Berry curvature, why time reversal kills the linear response ·
S03 Berry curvature dipole (the shifted Fermi sea, pocket-resolved ∫nΩ) · S04 the two-band model, 3D bands, hot spots ·
S05 the method: Bloch oscillations, reservoirs, drift E/Γ, Wigner/Moyal NEGF, current formula ·
S06 J_y/E versus E for eight chemical potentials · S07 the crossover E* ≈ Γ Δκ_x, with the steady-state occupation drifting into the hot spot ·
S08 μ = 0 interband transfer and the comparison of Hall-current formulas · S09 effective distribution function ·
S10 phonons and interactions, band renormalisation and sharper hot spots · S11 summary.

## Data provenance

- **Recomputed here:** `compute/negf.py` solves the constant-Γ reservoir model of the paper. Each bath frequency ω drives a
  damped 2×2 amplitude along the drifting trajectory κ(t) = κ₀ + Et, so one trajectory per k_y sweeps all k_x once per Bloch period.
  It reproduces the paper's NEGF values of J_y/E to about 1–2 % (e.g. μ = 0.3, E = 0.03: 2.98 vs 3.03 ×10⁻⁴) and its Fig. 1(b).
  `compute/make_data.py` regenerates `data/fig1b.npz`, `data/fig1c.npz` and the occupation maps `data/maps.npz`
  (≈ 36 MB, not committed; run `python compute/make_data.py maps`).
- **Read off the paper's figures:** Fig. 2(c,d) from the vector markers in the PDF, Fig. 3(d) and 4(a) by colour from the raster figures
  (`data/*_digitized.json`, numbers only).
- **Illustrative:** the renormalised bands and Berry-curvature maps in S10 use D_y^eff = 0.985, Z = 0.95 (the paper gives no value of Re Σ_z(0)).

## A note from the reproduction

At μ = 0 the solver gives Tr ñ(κ) = 1 to 10⁻⁶ at every field. This is exact: any traceless 2×2 Hamiltonian obeys
σ_y H* σ_y = −H, and with a particle–hole-symmetric wide-band bath at μ = 0 this gives Tr ñ_occ = Tr ñ_hole,
while ñ_occ + ñ_hole = 1. The paper's Fig. 2(b) shows hole-like dips of about 2 % in Tr ñ; they may be discretisation effects
(the paper's note [56] mentions a uniform offset of that origin) or a model detail not reproduced here.
The video therefore shows the upper-band excitation Δn₊(κ) instead, which equals the lower-band hole density at the same κ.
The Hall current itself agrees with the paper.

## Build

From this folder, with the environment described in [`pipeline/`](../../pipeline/README.md):

```bash
python compute/make_data.py fig1b fig1c maps   # NEGF datasets (numba, uses all cores, about 35 min)
python tts.py --lang en --voice af_bella        # narration
python build.py --lang en                       # 1080p60 + out/nlhe_en_subtitled.mp4
```
