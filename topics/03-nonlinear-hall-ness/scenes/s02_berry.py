import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

BZ = (-np.pi, np.pi)


def bc_image(ax, xr=BZ, yr=BZ, n=360, vmax=2.5, alpha=1.0):
    xs = np.linspace(*xr, n)
    ys = np.linspace(*yr, n)
    KX, KY = np.meshgrid(xs, ys)
    rgba = signed_rgba(berry(KX, KY), vmax)
    if alpha < 1:
        rgba[..., :3] = (rgba[..., :3] * alpha + (np.array(color_to_rgb(BG)) * 255) * (1 - alpha)).astype(np.uint8)
    return image_on_axes(rgba, ax, xr, yr)


def pocket_contours(ax, mu=0.3, color=WHITE, width=3, xr=BZ, yr=BZ, n=500):
    xs = np.linspace(*xr, n)
    ys = np.linspace(*yr, n)
    KX, KY = np.meshgrid(xs, ys)
    return contour_mobject(ax, eps(KX, KY), xs, ys, mu, color=color, width=width)


class S02_Berry(NScene):
    def construct(self):
        # ---------------- classical Hall effect
        sample = RoundedRectangle(corner_radius=0.12, width=6.0, height=3.0, fill_color='#161c2a',
                                  fill_opacity=1, stroke_color=GREY_C, stroke_width=2).shift(0.2 * DOWN)
        bsyms = VGroup(*[VGroup(Circle(radius=0.11, stroke_color=GREY_B, stroke_width=1.5),
                                Dot(radius=0.025, color=GREY_B)).move_to([x, y - 0.2, 0])
                         for x in np.arange(-2.5, 2.51, 0.71) for y in np.arange(-1.1, 1.11, 0.72)])
        Blab = MathTex(r'\mathbf{B}\ \odot', font_size=40).next_to(sample, UR, buff=0.1).shift(0.3 * LEFT)
        title = zh('普通霍尔效应：洛伦兹力', 34).to_edge(UP, buff=0.4)
        paths = VGroup(*[ArcBetweenPoints(sample.get_left() + RIGHT * 0.15 + UP * (y - 0.2) * 1,
                                          [x1, 1.15, 0], angle=-PI / 2.6)
                         for y, x1 in [(-1.0, 1.6), (-0.3, 0.7), (0.4, -0.3)]])
        paths.set_stroke(C_ELEC, 2.5, opacity=0.7)
        force = MathTex(r'\mathbf{F} = -e\,\mathbf{v}\times\mathbf{B}', font_size=40).next_to(sample, DOWN, buff=0.35)
        with self.narrate('hall1') as b:
            self.play(FadeIn(title), FadeIn(sample), LaggedStartMap(FadeIn, bsyms, lag_ratio=0.02), FadeIn(Blab),
                      run_time=1.5)
            dots = VGroup(*[Dot(color=C_ELEC, radius=0.07) for _ in paths])
            self.play(LaggedStart(*[MoveAlongPath(d, p, rate_func=linear) for d, p in zip(dots, paths)],
                                  lag_ratio=0.25),
                      LaggedStart(*[Create(p, rate_func=linear) for p in paths], lag_ratio=0.25), run_time=3.0)
            self.play(Write(force), run_time=1.2)
        classical = VGroup(title, sample, bsyms, Blab, paths, dots, force)

        # ---------------- Berry curvature as a k-space magnetic field
        ax = kspace_axes(5.4).to_edge(RIGHT, buff=0.8).shift(0.2 * DOWN)
        img = bc_image(ax)
        box = frame_box(ax, BZ, BZ)
        omg = VGroup(zh('贝里曲率', 30), MathTex(r'\Omega(\mathbf{k})', font_size=36)).arrange(RIGHT, buff=0.15)
        omg.next_to(ax, UP, buff=0.25)
        cbar = VGroup(Rectangle(width=0.25, height=0.9, fill_color=C_POS, fill_opacity=1, stroke_width=0),
                      Rectangle(width=0.25, height=0.9, fill_color=C_NEG, fill_opacity=1, stroke_width=0)
                      ).arrange(DOWN, buff=0).next_to(ax, RIGHT, buff=0.2)
        cbl = VGroup(MathTex('+', font_size=30).next_to(cbar[0], RIGHT, buff=0.08),
                     MathTex('-', font_size=30).next_to(cbar[1], RIGHT, buff=0.08))
        with self.narrate('hall2') as b:
            self.play(classical.animate.scale(0.62).to_edge(LEFT, buff=0.4), run_time=1.3)
            b.wait_sentence(1)
            self.play(FadeIn(box), Create(ax), run_time=0.8)
            self.play(FadeIn(img), FadeIn(cbar), FadeIn(cbl), Write(omg), run_time=2.0)
            b.wait_sentence(2)
            arrow = CurvedArrow(classical[1].get_right() + 0.1 * RIGHT + 0.6 * UP, ax.get_left() + 0.6 * UP + 0.1 * LEFT,
                                angle=-PI / 4, color=GREY_B)
            eq = VGroup(MathTex(r'\mathbf{B}(\mathbf{r})', font_size=34),
                        MathTex(r'\longleftrightarrow', font_size=34),
                        MathTex(r'\Omega(\mathbf{k})', font_size=34)).arrange(RIGHT, buff=0.15)
            eq.next_to(arrow, UP, buff=0.05)
            self.play(Create(arrow), FadeIn(eq), run_time=1.2)

        # ---------------- anomalous velocity
        kmap = Group(ax, img, box, cbar, cbl, omg)
        semi = MathTex(r'\dot{\mathbf r} = \frac{\partial \varepsilon}{\partial \mathbf k}',
                       r'- \dot{\mathbf k}\times\Omega(\mathbf k)', font_size=38)
        vanom = MathTex(r'\mathbf v_{\rm anom} = -\mathbf E\times\Omega(\mathbf k)', font_size=38)
        vanom[0][0:6].set_color(C_J)
        eq2 = MathTex(r'\frac{J_y}{E_x} = \sum_\nu \int_{\rm BZ}\frac{d^2k}{(2\pi)^2}\,',
                      r'n_\nu(\mathbf k)', r'\,\Omega^z_\nu(\mathbf k)', font_size=38)
        eq2[1].set_color(BLUE_B)
        trs = MathTex(r'\Omega(-\mathbf k) = -\,\Omega(\mathbf k)', font_size=38)
        zero = MathTex(r'\sum_\nu\int n_\nu\,\Omega_\nu = 0', font_size=38, color=YELLOW)
        nolin = zh('线性霍尔效应消失', 28, C_E)
        col = VGroup(semi, vanom, eq2, trs, zero, nolin).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        col.scale_to_fit_height(min(col.height, 6.9))
        col.move_to([3.6, -0.05, 0])
        if col.width > 6.0:
            col.scale_to_fit_width(6.0).move_to([3.6, -0.05, 0])
        with self.narrate('hall3') as b:
            self.play(FadeOut(classical), FadeOut(arrow), FadeOut(eq), run_time=0.8)
            self.play(kmap.animate.to_edge(LEFT, buff=0.7), run_time=1.0)
            self.play(Write(semi), run_time=1.5)
            self.play(semi[1].animate.set_color(C_J), run_time=0.5)
            self.play(TransformFromCopy(semi[1], vanom), run_time=1.0)
            E_ar = Arrow(ax.c2p(-2.2, 2.75), ax.c2p(2.2, 2.75), color=C_E, buff=0, stroke_width=5)
            E_lb = MathTex(r'\mathbf E', color=C_E, font_size=34).next_to(E_ar, RIGHT, buff=0.1)
            pk = VGroup()
            for s in (-1, 1):
                p = ax.c2p(s * NODE, 0.45)
                pk.add(Dot(p, radius=0.08, color=WHITE),
                       Arrow(p, p + (-s) * 0.9 * UP, buff=0, color=C_J, stroke_width=5,
                             max_tip_length_to_length_ratio=0.3))
            self.play(GrowArrow(E_ar), FadeIn(E_lb), FadeIn(pk), run_time=1.0)

        # ---------------- Hall current = sum over occupied states
        pockets = pocket_contours(ax, 0.3, color=WHITE, width=3)
        with self.narrate('hall4') as b:
            self.play(Write(eq2), run_time=1.6)
            self.play(Create(pockets), FadeOut(pk), run_time=1.4)
            self.play(Indicate(eq2[1], color=BLUE_B), run_time=1.0)

        # ---------------- time-reversal: Omega(-k) = -Omega(k)
        with self.narrate('hall5') as b:
            self.play(Write(trs), run_time=1.2)
            ka, kb = ax.c2p(-1.2, 0.35), ax.c2p(1.2, -0.35)
            da, db = Dot(ka, color=C_POS, radius=0.09), Dot(kb, color=C_NEG, radius=0.09)
            la = MathTex(r'\mathbf k', font_size=30).next_to(da, UL, buff=0.05)
            lb = MathTex(r'-\mathbf k', font_size=30).next_to(db, DR, buff=0.05)
            dl = DashedLine(ka, kb, color=GREY_B, stroke_width=2)
            self.play(Create(dl), FadeIn(da, scale=2), FadeIn(db, scale=2), FadeIn(la), FadeIn(lb), run_time=1.5)
            self.play(Flash(da, color=C_POS), Flash(db, color=C_NEG), run_time=1.0)
            b.wait_sentence(1)
            self.play(Write(zero), run_time=1.2)
            self.play(FadeIn(nolin, shift=0.2 * UP), run_time=0.8)
        self.play(FadeOut(VGroup(semi, vanom, eq2, trs, zero, nolin, dl, da, db, la, lb, E_ar, E_lb)),
                  run_time=0.8)
