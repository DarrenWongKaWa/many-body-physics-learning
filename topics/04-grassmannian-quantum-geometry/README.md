# 04 · Quantum geometry on the Grassmannian: projectors, distances, folds

**Status:** study materials, numerical checks and an explainer video (scenes and build in [Video](#video) below).

**Watch:** [`04-grassmannian-quantum-geometry.mp4`](https://github.com/DarrenWongKaWa/many-body-physics-learning/releases/download/v1.0/04-grassmannian-quantum-geometry.mp4) · subtitles: [`videos/04-grassmannian-quantum-geometry.srt`](../../videos/04-grassmannian-quantum-geometry.srt)

This topic follows three preprints by Shin-Ming Huang (National Sun Yat-sen University, Kaohsiung),
which treat a band structure as a map from the Brillouin torus into the Grassmannian of occupied subspaces
and derive distance, metric, Berry curvature, geodesics, holonomy, Gauss curvature and topology from the
projector alone, without ever fixing a gauge.

| Label | Paper | arXiv | Posted |
|---|---|---|---|
| H1 | S.-M. Huang, D. Giataganas, *Exploring Grassmann manifolds in topological systems via quantum distance* (Phys. Rev. B, accepted 2026) | [2412.20046](https://arxiv.org/abs/2412.20046) | Dec 2024 |
| H2 | S.-M. Huang, *Quantum-State Projectors on Grassmannian: Geometry, Holonomy, and Topology* | [2608.06777](https://arxiv.org/abs/2608.06777) | Aug 2026 |
| H3 | S.-M. Huang, *A Gauss-Bonnet Theorem for Quantum States: Gauss Curvature and Topology in the Projective Hilbert Space* | [2510.15760](https://arxiv.org/abs/2510.15760) | Oct 2025 |

The labels H1 → H2 → H3 are the **conceptual** reading order used in the study guide, not the chronological one
(H3 was posted before H2). H2 is the general toolbox; H3 applies it to the two-band case.
The papers are not redistributed here; see [`materials/`](../../materials/README.md).

## The story in three steps

1. **Compare whole subspaces at a finite distance (H1).** The occupied states at two momenta are two
   subspaces. Principal angles between them are gauge independent; the Hilbert–Schmidt distance of the
   projectors is a Euclidean distance, so a table of distances can be fed to multidimensional scaling and the
   sampled state manifold reconstructed as a surface in Euclidean space.
2. **Differentiate and transport (H2).** `dP` is the tangent vector of the projector map. Its interband block
   gives the quantum metric and Berry curvature at once; exponentiating the horizontal generator gives
   geodesics whose principal angles are the singular values of that block; products of projectors give the
   Berry phase of geodesic polygons and the Wilson loop of degenerate multiplets; wedge products of `dP`
   give Chern characters, winding numbers and the Z2 index.
3. **Integrate curvature and keep track of folds and signs (H3).** For two bands the states live on the Bloch
   sphere, and a torus cannot cover a sphere without folding. Along the fold the metric degenerates, the image
   sheets overlap with opposite orientations, and the Berry curvature is exactly the *signed* area density.
   A Gauss–Bonnet theorem with a singular-curvature term along the fold recovers the Chern number.
   H3 ends with an open question: what replaces this picture when there are more than two bands?

## Files

```
guide/     illustrated study guide (21 pages), one-page poster, two-page "sphere → Bloch" bridge; TikZ sources + PDFs
verify/    gauge-free projector code that checks the multiband extension on 2-, 3- and 4-band models
notes/     study notes in Chinese: the story, the open question, the proposed answer, status and risks;
           video_plan_zh.md is the video plan with the checked numbers
compute/   make_data.py: precomputed data for the video (MDS iterations, Bargmann phases, Kähler-angle maps)
data/      its output, read by the scenes
narration.py, tts.py, common.py, scenes/, build.py, tools/   the video (same pipeline as topic 02)
```

- `guide/quantum_geometry_visual_guide.pdf` — physics-first guide for a final-year undergraduate: states, rays,
  projectors, distances, the quantum geometric tensor, connections, curvature, folds, the three-paper story and
  the proposed multiband extension. Blue = established, green = proposed, gray = teaching calculation, amber =
  assumptions. Start with `guide/README.txt`.
- `guide/three_papers_story.pdf` — one-page poster of the H1 → H2 → H3 chain.
- `guide/sphere_to_bloch_bridge.pdf` — the classical Gauss-equation calculation on a sphere, then the same
  tangent/normal split for the Bloch surface inside the Grassmannian.
- `verify/verify_kahler_gauss.py` — exact projector derivatives (first-order perturbation theory, Sylvester
  equation and idempotency for second derivatives), the Kähler angle, the Gauss-equation decomposition of the
  Gauss curvature, an independent Brioschi check, Gauss–Bonnet integrals, and the complex-point count.
  `verification_log.txt` is its output; `kahler_gauss_check.png` the figure.

## The proposed multiband extension (unpublished, work in progress)

Everything in green in the guide is a proposed answer to H3's open question, not something the three papers
contain. In the standard convention `q = g − (i/2) Ω`, `g = ½ tr(∂P ∂P)`:

- **Kähler angle.** `Ω_xy = 2 cos θ_K √det g`. Beyond two bands the Berry curvature is the quantum area
  density weighted by the alignment of the tangent plane with the complex structure. Two bands: `cos θ_K = ±1`
  with sign flips across folds. Three or more bands: generically no folds, `cos θ_K` varies continuously.
- **Lagrange identity.** `det g = Ω²/4 + ‖B_x ∧ B_y‖²` (rank one), so a fold needs `Ω = 0` and `B_x ∧ B_y = 0`
  together: codimension 1 for two bands, ≥ 3 otherwise.
- **Gauss equation on the Grassmannian.** `K_G = K_Gr + K_II` with
  `K_Gr = (‖F_occ‖²_F + ‖F_unocc‖²_F) / (2 det g)`, which equals `1 + 3 cos² θ_K` for one occupied band.
  For an immersed torus `∫ K_G dA = 2π χ(T²) = 0`: the Gauss curvature carries no Chern number beyond two bands.
- **Complex points.** For three bands the points where the determinant bound saturates (`|cos θ_K| = 1`) are
  isolated and their signed count is `3|C|` (a band-language instance of Lai's complex-point formula).
  For four or more bands they are generically absent; for two bands the bound saturates everywhere.
- **Two-band fold counting.** Quine's formula `−2 χ(M⁻) + Σ μ(p_k) = 2C` fixes the relation between the
  orientation-reversing region and the signed number of cusps; and the singular-curvature integral along the
  fold equals minus the quantum volume.

What the numerics show (see `verify/verification_log.txt`): all algebraic identities hold to ~1e-14; the
Gauss-equation curvature agrees with the intrinsic Brioschi curvature with O(h²) convergence; Gauss–Bonnet
integrals vanish for the 3- and 4-band models; the two-band control reproduces H3's `∫K dÂ = 2.3779 × 2π`;
the three-band model has five complex points with indices +1, +1, +1, +1, −1, signed sum 3 = 3|C|.

Literature closest to this: Mera and Ozawa (Kähler bands, PRB 104, 045104) for the pullback picture;
Avdoshkin and Popov (PRB 107, 245136, Appendix D) for the Gauss–Codazzi setup of the state manifold;
Lai (Trans. AMS 172, 1972) for complex points; Quine (Trans. AMS 236, 1978) for cusps of surface maps.
None of them states the results above in band language, but any write-up must start from them.

## Run the checks

```bash
cd topics/04-grassmannian-quantum-geometry/verify
python verify_kahler_gauss.py        # ~1 min; prints the log and writes kahler_gauss_check.png
```

Needs only numpy, scipy and matplotlib (already in `requirements.txt`).

## Rebuild the guide

```bash
cd topics/04-grassmannian-quantum-geometry/guide
pdflatex quantum_geometry_visual_guide.tex && pdflatex quantum_geometry_visual_guide.tex
pdflatex three_papers_story.tex && pdflatex three_papers_story.tex
pdflatex sphere_to_bloch_bridge.tex && pdflatex sphere_to_bloch_bridge.tex
```

All figures are native TikZ; no external images or bibliography database are needed.

## Video

English narration (Kokoro-82M, voice `af_bella`), 1920×1080, 60 fps, English subtitles burned in.
It follows the plan below: one picture (the Brillouin torus pressed onto the Bloch sphere), a cold open with the puzzle,
then three acts for H1, H2, H3 and a fourth act for the proposal, marked **PROPOSAL (unpublished)** in green on screen.
The video runs 10 minutes instead of the planned 14 because the narration came out tighter; none of the planned pictures was dropped.

| Scene | Content | Source |
|---|---|---|
| S01 | cold open: a sheet rolls into a cylinder and a torus; the torus pressed onto the sphere by the actual QWZ map must fold | H3 |
| S02 | the stage: Brillouin zone = torus, Bloch sphere; the grid painted onto the sphere cell by cell, blue face up, red flipped; the fold curve and its image with cusps | — |
| S03 | principal angle; chord = D_HS = sin θ and arc = d_FS = θ on the radius-1/2 sphere; principal angles of two planes from the SVD of the overlap matrix | H1 |
| S04 | the Hilbert–Schmidt distance table of 484 states; SMACOF iterations rebuild a closed sphere (Chern band, m = 1) and an open cap (trivial band, m = 3.2) | H1 |
| S05 | small circle → metric ellipse, g = ½ tr(∂P ∂P); small square → oriented parallelogram, Berry curvature = signed area; the other band: same g, opposite Ω, both K_G = 4 | H2, guide p. 6 |
| S06 | geodesics as exponentials of the horizontal generator; parallel transport around a geodesic triangle turns by the solid angle; Bargmann invariant = half the solid angle; geodesic polygons converge to the Berry phase | H2 |
| S07 | Tissot-style metric ellipses collapsing to segments on the fold; a folded film with mirrored arrows; the polar cap covered three times; unsigned 1.189 vs signed 1.000 spheres | H3 |
| S08 | Gauss–Bonnet: regular sheets +2.378 × 2π, fold −2.378 × 2π, total 0 = 2πχ(T²); signed: 4πC; Huang's doubled metric gives the same 2.378 | H3 |
| S09 | proposal: the fold (s, t²) lifted by εt; Kähler angle, cos θ_K = ±1 (two bands) vs smooth (three bands); five complex points with indices +1, +1, +1, +1, −1, signed sum 3 = 3\|C\|; ∫K_G dA = 0 | proposal, `verify/` |
| S10 | summary of H1–H3 and credits | — |

**What is computed.** Every map, ellipse, parallelogram, fold curve, area counter, MDS step and Kähler-angle map comes
from the two-band formulas in `common.py` (g = ¼ ∂n·∂n, Ω = −½ n·(∂ₓn × ∂ᵧn), the band with Bloch vector n = d/|d|,
C = +1 at m = 1) or from `compute/make_data.py`, which reuses `verify/verify_kahler_gauss.py` for the three-band model.
The parallelogram insets in S05 are the linearised map at the sample momentum; the bars in S08 are drawn to scale.
The film fold in S07 and the lifted fold in S09 are teaching pictures and are labelled as such.

**Build** (from this folder, with the environment in [`pipeline/`](../../pipeline/README.md)):

```bash
python compute/make_data.py                     # data/*.npz (a few seconds)
python tts.py                                   # narration (only changed beats are regenerated)
python build.py                                 # 1080p60 + out/grassmann_en_subtitled.mp4
python build.py --quality l --only S07_Fold     # quick 480p preview of one scene
python tools/sheet.py S07_Fold s07_fold         # contact sheet of that preview
```

## Video plan

The full plan, in Chinese, is [`notes/video_plan_zh.md`](notes/video_plan_zh.md).

The video has one main character: the map that presses the Brillouin-zone torus onto the Bloch sphere.
The three papers ask three questions about this one picture, and the guide is the dictionary for reading it.
The video opens with a puzzle and builds the tools afterwards, instead of going through H1, H2 and H3 in order.

| Part | Length | Content | Source |
|---|---|---|---|
| Cold open | 1 min | A sheet rolls into a cylinder, but a torus-shaped membrane cannot be put smoothly over a sphere: it must fold. Electrons in a crystal do exactly this, and the folds hide the Chern number. | H3 |
| Act 1: the map | 3 min | Brillouin zone (a square with opposite edges glued) on the left, Bloch sphere on the right; the grid is swept onto the sphere cell by cell. Chord and arc length are the two quantum distances (`D_HS = sin θ`, `d_FS = θ` on the radius-1/2 sphere). From the table of all pairwise distances, multidimensional scaling rebuilds the shape. | H1 |
| Act 2: zoom in | 4 min | A small circle in k-space maps to a small ellipse (the metric); a small square maps to an oriented parallelogram whose signed area is the Berry curvature. Then parallel transport and geodesics. | H2 |
| Act 3: back to the fold | 4 min | On the fold the ellipses collapse to segments; on the other side the grid is mirrored, and a polar cap is covered three times. Unsigned area gives the quantum volume, signed area gives the Chern number. Gauss–Bonnet: the torus has total curvature zero, so the fold's singular curvature cancels the positive regular part. | H3 |
| Act 4 (optional) | 2 min | A third band: the sphere becomes CP², the fold has room to open up into a smooth bend. Marked **proposal** on screen. | proposed |

The seven pictures that have to be animated, all computed from the two-band formulas:

1. The coloured grid map, blue where orientation is kept and red where it is reversed; the video keeps returning to it.
2. The fold triptych: a folded transparent sheet with mirrored arrows, the closed `det g = 0` curve of QWZ, three
   stacked sheets over the polar cap; two counters for unsigned and signed area that stop at 1.19 and 1 (in units of π|C|).
3. Tissot ellipses for the metric over the whole Brillouin zone, collapsing to segments on the fold.
4. Berry curvature as the signed area of a small parallelogram; then the other band: same metric, opposite curvature (guide p. 6).
5. Two planes and their two principal angles; then the MDS reconstruction as a spring-like relaxation (SMACOF iterations).
   The Chern band closes into a whole sphere; the trivial band gives only an open cap around the north pole.
6. Parallel transport around a geodesic triangle; then a loop replaced by a geodesic polygon, whose Bargmann invariant is
   the numerical Berry phase. The tangent vector turns by the enclosed solid angle; the Berry phase is half of it.
7. The two Gauss–Bonnet ledgers: regular part +2.3779 × 2π, fold −2.3779 × 2π, total 0 on the torus;
   with signs, three sheets become one net sheet and the answer is 4πC.

Act 4 adds an eighth: the fold `(s, t²)` lifted by a third direction `εt` (bridge p. 2), then the `cos θ_K` maps
from `verify/` (hard ±1 boundary for two bands, smooth for three bands, five complex points with indices +1, +1, +1, +1, −1).

Left out on purpose: drawings of Gr(2,4), the Lie-algebra decomposition (only "a global phase does not move the point;
a change of relative amplitude does", guide p. 5), and Wilson loops, Z2 and chiral winding, which get one sentence at the end.

One model throughout, as in topic 02: QWZ with m = 1 (Chern band) and m = 3.2 (trivial). Conventions follow the guide
(p. 18): standard metric, sphere of radius 1/2 and curvature 4. When the narration quotes Huang's numbers, it must say that
he uses the doubled metric (curvature 2); H3's displayed Berry curvature has the opposite sign to H2's.
The numbers above were checked; see the table in the plan.
