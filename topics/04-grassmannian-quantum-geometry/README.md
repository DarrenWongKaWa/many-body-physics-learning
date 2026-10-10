# 04 · Quantum geometry on the Grassmannian: projectors, distances, folds

**Status:** study materials and numerical checks. The explainer video is not made yet; a draft scene list is at the end.

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
notes/     study notes in Chinese: the story, the open question, the proposed answer, status and risks
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

## Draft scene list for the video (to do)

| Scene | Content | Source |
|---|---|---|
| S01 | one map, three questions: how far apart, how does it move, what does the curvature add up to | all three |
| S02 | a subspace instead of a state; principal angles; Hilbert–Schmidt distance; reconstructing the image from distances | H1 |
| S03 | zoom in: distance → metric; `dP` as a tangent vector; the interband block | H2 |
| S04 | the quantum geometric tensor as a Gram matrix: metric and Berry curvature from one object | H2, topic 02 |
| S05 | geodesics on the Grassmannian; Berry phase of a geodesic polygon; Wilson loops without splitting a multiplet | H2 |
| S06 | a torus cannot cover a sphere: folds, overlapping sheets, signed versus unsigned area | H3 |
| S07 | Gauss–Bonnet with a singular curvature along the fold; the Chern number comes out | H3 |
| S08 | beyond two bands: the fold opens up, the Kähler angle takes over | proposed |
| S09 | complex points and the count `3|C|`; what the Gauss curvature does and does not know | proposed |
| S10 | open questions | H3 §V, notes |

Conventions for the video should follow the guide (page 18): standard metric, `q = g − (i/2) Ω`,
regular two-band sphere of radius 1/2 and curvature 4. Huang's papers use the doubled metric (curvature 2),
and H3's displayed Berry curvature has the opposite sign to H2's.
