import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NK = 24


def column(head, color, lines, center):
    h = txt(head, 32, color, bold=True)
    body = VGroup(*[txt(l, 24, GREY_A) for l in lines]).arrange(DOWN, buff=0.14)
    g = VGroup(h, body).arrange(DOWN, buff=0.3)
    box = RoundedRectangle(width=4.2, height=3.3, corner_radius=0.15, stroke_color=color, stroke_width=2,
                           fill_color=C_PANEL, fill_opacity=0.9).move_to(center)
    g.move_to(box)
    return VGroup(box, g)


class S10_Outro(NScene):
    def construct(self):
        title = txt('Three papers, one picture', 40, bold=True).to_edge(UP, buff=0.35)
        c1 = column('H1: distance', C_UP, ['principal angles', 'Hilbert--Schmidt distance', 'distance table $\\to$ shape (MDS)'], [-4.5, 0.4, 0])
        c2 = column('H2: derivative', C_G, ['$P\\to dP\\to g,\\ \\Omega$', 'geodesics, Berry phases', 'Wilson loops, winding, $\\mathbb Z_2$'], [0, 0.4, 0])
        c3 = column('H3: curvature', C_FOLD, ['folds and signed area', 'regular $+$ fold $= 0$', 'signed: $4\\pi C$'], [4.5, 0.4, 0])

        with self.narrate('end1') as b:
            self.play(Write(title), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(c1, shift=0.2 * UP), run_time=1.2)
        with self.narrate('end2') as b:
            self.play(FadeIn(c2, shift=0.2 * UP), run_time=1.2)
            b.wait_sentence(1)
            self.play(Indicate(c2[1][1][2], color=C_G), run_time=1.2)
        with self.narrate('end3') as b:
            self.play(FadeIn(c3, shift=0.2 * UP), run_time=1.2)

        # final picture: the painted map, the dependency chain, credits
        chain = MathTex(r'P \;\to\; dP \;\to\; q = g - \tfrac{i}{2}\Omega \;\to\; \text{geometry and topology}', font_size=38)
        chain.move_to([0, 2.55, 0])
        X, cols, om = sphere_cells(NK)
        cam = Cam(0.42, 0.55, 1.8, np.array([-3.2, -0.6, 0]))
        sphere = Sphere2D(radius=1.8, el=0.42, az=0.55, n_merid=0).move_to([-3.2, -0.6, 0])
        pic = mesh(cam, X, cols, opacity=0.8, back_opacity=0.1, stroke_width=0.3, cull_center=np.zeros(3), on_top=om < 0)
        fimg = VGroup(*[polyline3d(cam, np.moveaxis(qwz_n(seg[:, 0], seg[:, 1]), 0, -1) * 1.035, color=C_FOLD, width=3,
                                   back_opacity=0.2, cull_center=np.zeros(3)) for seg in fold_points()])
        credits = VGroup(
            txt('S.-M. Huang, D. Giataganas, arXiv:2412.20046 (H1)', 24, GREY_A),
            txt('S.-M. Huang, arXiv:2608.06777 (H2)', 24, GREY_A),
            txt('S.-M. Huang, arXiv:2510.15760 (H3)', 24, GREY_A),
            txt('multiband part: our proposal (unpublished)', 24, C_PROP),
            txt('model: Qi--Wu--Zhang, $m=1$ and $3.2$; all curves computed', 22, GREY_T),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([2.6, -0.7, 0])
        with self.narrate('end4') as b:
            self.play(FadeOut(VGroup(c1, c2, c3, title)), run_time=0.8)
            self.play(Write(chain), run_time=2.0)
            self.play(FadeIn(sphere), FadeIn(pic), run_time=1.5)
            self.play(Create(fimg), run_time=1.5)
            self.play(FadeIn(credits, shift=0.2 * LEFT), run_time=1.2)
            b.wait_sentence(1)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)
