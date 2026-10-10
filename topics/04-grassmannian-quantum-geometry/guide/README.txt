QUANTUM GEOMETRY: A PHYSICS-FIRST VISUAL GUIDE
Prepared 10 October 2026

START HERE

quantum_geometry_visual_guide.pdf
  A 21-page illustrated guide for a final-year undergraduate physics reader.
  It builds from Bloch eigenvectors and projectors to the quantum geometric
  tensor, connections, curvature, folds, and the proposed multiband extension.

three_papers_story.pdf
  A one-page landscape TikZ poster containing only the story of the three
  Huang papers. Its conceptual order is H1 -> H2 -> H3, not publication order.

EDITABLE SOURCES

quantum_geometry_visual_guide.tex
three_papers_story.tex

Each .tex file is self-contained. All illustrations are native TikZ; no
external image files, bibliography database, or shell escape are required.
Standard TeX Live or MiKTeX installations with the listed packages suffice.
For an online LaTeX editor, upload one .tex file and select pdfLaTeX.

Compile each source twice to resolve page references and hyperlinks:

  pdflatex quantum_geometry_visual_guide.tex
  pdflatex quantum_geometry_visual_guide.tex

  pdflatex three_papers_story.tex
  pdflatex three_papers_story.tex

The guide has a page comment before each topic, so individual tikzpicture
environments can be located easily. To reuse a figure, retain its macros,
color definitions, TikZ styles, and required packages from the preamble.

COLOR AND EVIDENCE LEGEND

Blue / [H1], [H2], [H3], [R], etc.:
  Established material used or reported in the cited sources. This does not
  claim that these authors originally invented every mathematical concept.

Green / [E]:
  The proposed multiband application in the supplied research discussion,
  with qualifications and references to its classical ingredients.
  Green is not a certification of literature priority or publication status.

Gray / [Calc]:
  Standard background or an explicitly worked teaching calculation.

Amber:
  Assumptions, distinctions, and open questions.

SUGGESTED READING ORDER

Pages 2-6: states, rays, projectors, subspaces, distances, and one worked QGT.
Pages 7-8: connections, transport, intrinsic curvature, and bending.
Pages 9-10: the three-paper story and the two-band fold picture.
Pages 11-15: the proposed multiband interpretation and its assumptions.
Page 16: the connection to optical and Hall-response language in the review.
Pages 17-19: dictionary, convention ledger, and short self-checks.
Page 20: linked references.
Page 21: optional projector derivations and numerical evidence.

CONVENTIONS

The guide uses A_i = i <u|partial_i u>, q = g - i Omega/2, and
g_ij = (1/2) tr(partial_i P partial_j P). Thus a regular two-level Bloch
sphere has Gaussian curvature 4. Huang's doubled metric has curvature 2.
Page 18 separately explains the Berry-curvature sign difference between
the displayed definitions in H2 and H3.

READING CLARIFICATION (10 October 2026)

Page 6 now labels its worked results as calculated from the chosen spinor,
displays the full QGT, and distinguishes the Berry connection A_a from the
quantum area element dA. The QGT determines the metric and Berry curvature;
it does not select the gauge-dependent Berry connection uniquely.

SOURCE KEYS

H1: Huang and Giataganas, Exploring Grassmann manifolds in topological
    systems via quantum distance, arXiv:2412.20046v2.
    https://arxiv.org/html/2412.20046v2

H2: Huang, Quantum-State Projectors on Grassmannian: Geometry, Holonomy,
    and Topology, arXiv:2608.06777v1.
    https://arxiv.org/html/2608.06777v1

H3: Huang, A Gauss-Bonnet Theorem for Quantum States: Gauss Curvature and
    Topology in the Projective Hilbert Space, arXiv:2510.15760v1.
    https://arxiv.org/html/2510.15760v1

R:  Gao, Nagaosa, Ni, and Xu, Quantum geometry phenomena in condensed
    matter systems, Reviews of Modern Physics 98, 035005 (2026).
    https://doi.org/10.1103/f78t-ky69
    The supplied review was used as the physics reference.

Additional mathematical sources, including Mera-Ozawa, Avdoshkin-Popov,
Lai, and Forstneric, are linked on page 20 and cited beside the relevant
relations. No source PDF is redistributed in this bundle.

The earlier numerical audit is a separate archive named
kahler_gauss_audit_2026-10-10.zip. This guide summarizes that evidence;
it does not claim that finite grids prove global immersion or certify a
complete count of all complex points.

VALIDATION

Both sources were compiled successfully with pdfLaTeX. The guide has
21 pages; the poster has 1 landscape page. Final PDFs were rendered and
visually checked, and the final compilation logs had no overfull boxes,
unresolved references, or LaTeX errors. The mathematical conventions and
physical interpretations were independently reviewed before packaging.
