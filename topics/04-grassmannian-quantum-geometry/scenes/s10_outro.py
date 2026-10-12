import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NK = 24
MDS = np.load(ROOT / 'data' / 'mds.npz')


def column(head, color, lines, center):
    h = txt(head, 30, color, bold=True)
    body = VGroup(*[txt(l, 23, GREY_A) for l in lines]).arrange(DOWN, buff=0.12)
    g = VGroup(h, body).arrange(DOWN, buff=0.25)
    box = RoundedRectangle(width=4.2, height=2.5, corner_radius=0.15, stroke_color=color, stroke_width=2,
                           fill_color=C_PANEL, fill_opacity=0.9).move_to(center)
    g.move_to(box)
    return VGroup(box, g)


def pic_h1(center, r=1.05):
    """H1: the Bloch sphere rebuilt from the distance table (final SMACOF configuration)."""
    X = MDS['chern_iters'][-1].astype(float)
    _, _, om, _ = qwz_geom(MDS['chern_kx'], MDS['chern_ky'])
    cam = Cam(0.35, 0.8, 2 * r, np.asarray(center, float))
    P, dep = cam.p(X), cam.depth(X)
    dn = (dep - dep.min()) / (dep.max() - dep.min())
    g = VGroup(*[Dot(p, radius=0.022, color=C_UP if o >= 0 else C_FLIP).set_opacity(0.25 + 0.75 * a) for p, o, a in zip(P, om, dn)])
    return g


def pic_h2(center, r=1.05):
    """H2: a metric ellipse, an oriented parallelogram and a geodesic triangle on the sphere."""
    sph = Sphere2D(radius=r, el=0.42, az=0.35, n_merid=0).move_to(center)
    g = VGroup(sph)
    cdir, e1, e2 = sph.basis()
    unit = lambda x: x / np.linalg.norm(x)
    # geodesic triangle on the left half of the visible side
    tc = unit(cdir - 0.5 * e1 + 0.05 * e2)
    v = [unit(tc + 0.42 * (np.cos(a) * e1 + np.sin(a) * e2)) for a in (PI / 2, PI / 2 + TAU / 3, PI / 2 + 2 * TAU / 3)]
    for a, b2 in zip(v, v[1:] + v[:1]):
        g.add(sph.curve(slerp_path(a, b2, 30), color=C_GEO, width=3))
    # metric ellipse: the computed image of a small circle of momenta whose centre lands on the right half
    target = unit(cdir + 0.38 * e1 - 0.12 * e2)
    ks = np.linspace(0, TAU_K, 121)
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    N = np.moveaxis(qwz_n(KX, KY), 0, -1)
    i, j = np.unravel_index(np.argmin(np.linalg.norm(N - target, axis=-1)), KX.shape)
    k0 = np.array([KX[i, j], KY[i, j]])
    t = np.linspace(0, TAU, 80)
    g.add(sph.curve([qwz_n(*(k0 + 0.25 * np.array([np.cos(s), np.sin(s)]))) for s in t], color=C_G, width=3))
    return g


def pic_h3(center, r=1.05):
    """H3: the painted map with the fold's image."""
    cam = Cam(0.42, 0.55, r, np.asarray(center, float))
    X, cols, om = sphere_cells(NK)
    g = VGroup(Sphere2D(radius=r, el=0.42, az=0.55, n_merid=0).move_to(center),
               mesh(cam, X, cols, opacity=0.8, back_opacity=0.1, stroke_width=0.2, cull_center=np.zeros(3), on_top=om < 0))
    for seg in fold_points():
        g.add(polyline3d(cam, np.moveaxis(qwz_n(seg[:, 0], seg[:, 1]), 0, -1) * 1.035, color=C_FOLD, width=2.5,
                         back_opacity=0.2, cull_center=np.zeros(3)))
    return g


class S10_Outro(NScene):
    def construct(self):
        title = txt('Three papers, one picture', 40, bold=True).to_edge(UP, buff=0.35)
        xs = (-4.5, 0.0, 4.5)
        c1 = column('H1: distance', C_UP, ['principal angles', 'Hilbert--Schmidt distance', 'distance table $\\to$ shape (MDS)'], [xs[0], 1.15, 0])
        c2 = column('H2: derivative', C_G, ['$P\\to dP\\to g,\\ \\Omega$', 'geodesics, Berry phases', 'Wilson loops, winding, $\\mathbb Z_2$'], [xs[1], 1.15, 0])
        c3 = column('H3: curvature', C_FOLD, ['folds and signed area', 'regular $+$ fold $= 0$', 'signed: $4\\pi C$'], [xs[2], 1.15, 0])
        p1, p2, p3 = pic_h1([xs[0], -1.85, 0]), pic_h2([xs[1], -1.85, 0]), pic_h3([xs[2], -1.85, 0])
        cap1 = txt('the Bloch sphere rebuilt from distances', 20, GREY_T).move_to([xs[0], -3.15, 0])
        cap2 = txt('metric ellipse and a geodesic triangle', 20, GREY_T).move_to([xs[1], -3.15, 0])
        cap3 = txt('the map, its fold and the flipped sheet', 20, GREY_T).move_to([xs[2], -3.15, 0])

        with self.narrate('end1') as b:
            self.play(Write(title), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(c1, shift=0.2 * UP), FadeIn(p1), FadeIn(cap1), run_time=1.4)
        with self.narrate('end2') as b:
            self.play(FadeIn(c2, shift=0.2 * UP), FadeIn(p2), FadeIn(cap2), run_time=1.4)
            b.wait_sentence(1)
            self.play(Indicate(c2[1][1][2], color=C_G), run_time=1.2)
        with self.narrate('end3') as b:
            self.play(FadeIn(c3, shift=0.2 * UP), FadeIn(p3), FadeIn(cap3), run_time=1.4)

        # final picture: the painted map, the dependency chain, credits
        chain = MathTex(r'P \;\to\; dP \;\to\; q = g - \tfrac{i}{2}\Omega \;\to\; \text{geometry and topology}', font_size=38)
        chain.move_to([0, 2.55, 0])
        pic = pic_h3([-3.2, -0.6, 0], r=1.8)
        credits = VGroup(
            txt('S.-M. Huang, D. Giataganas, arXiv:2412.20046 (H1)', 24, GREY_A),
            txt('S.-M. Huang, arXiv:2608.06777 (H2)', 24, GREY_A),
            txt('S.-M. Huang, arXiv:2510.15760 (H3)', 24, GREY_A),
            txt('multiband part: our proposal (unpublished)', 24, C_PROP),
            txt('model: Qi--Wu--Zhang, $m=1$ and $3.2$; all curves computed', 22, GREY_T),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, -0.7, 0])
        with self.narrate('end4') as b:
            self.play(FadeOut(Group(c1, c2, c3, p1, p2, p3, cap1, cap2, cap3, title)), run_time=0.8)
            self.play(Write(chain), run_time=2.0)
            self.play(FadeIn(pic), run_time=1.5)
            self.play(FadeIn(credits, shift=0.2 * LEFT), run_time=1.2)
            b.wait_sentence(1)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)
