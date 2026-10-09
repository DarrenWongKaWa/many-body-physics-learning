import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def spectrum(w):
    """A cartoon absorption spectrum of a band insulator: zero below the gap Eg = 1."""
    w = np.asarray(w, float)
    edge = np.clip(w - 1.0, 0, None)
    return (1.6 * np.sqrt(edge) * np.exp(-0.9 * edge) + 0.9 * np.exp(-((w - 2.6) ** 2) / 0.08)) * (w > 1.0)


def kagome(center, a=0.55, n=3, color=GREY_B):
    a1, a2 = a * np.array([2, 0, 0]), a * np.array([1, np.sqrt(3), 0])
    g, dots = VGroup(), VGroup()
    c = np.asarray(center, float)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            o = c + i * a1 + j * a2 - (a1 + a2) * 0.5 * 0
            A, B, C = o, o + a1 / 2, o + a2 / 2
            if np.linalg.norm(o - c) > 1.9 * a * n * 0.5 + 0.6:
                continue
            g.add(Polygon(A, B, C, stroke_color=color, stroke_width=1.6))
            g.add(Polygon(B, o + a1, o + a1 - a2 / 2, stroke_color=color, stroke_width=1.6))
            for p in (A, B, C):
                dots.add(Dot(p, radius=0.045, color=C_A))
    return VGroup(g, dots)


class S10_Measure(NScene):
    def construct(self):
        title = txt('Seeing quantum geometry in crystals', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- mea1: optical sum rule
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1.3, 1], x_length=5.6, y_length=3.0, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-3.2, -0.2, 0])
        xl = MathTex(r'\hbar\omega', font_size=32, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex(r'\mathrm{Re}\,\sigma_{xx}(\omega)', font_size=32, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        sp = ax.plot(spectrum, x_range=[0, 4, 0.005], color=C_B, stroke_width=4)
        weighted = ax.plot(lambda w: spectrum(w) / max(w, 1e-3), x_range=[0.02, 4, 0.005], color=C_G, stroke_width=4)
        area = ax.get_area(weighted, x_range=[1.0, 4], color=C_G, opacity=0.35)
        gap = DashedLine(ax.c2p(1.0, 0), ax.c2p(1.0, 1.25), color=GREY_B)
        gapl = MathTex(r'E_g', font_size=30, color=GREY_B).next_to(ax.c2p(1.0, 0), DOWN, buff=0.12)
        sch = txt('(schematic spectrum)', 22, GREY_D).next_to(ax, DOWN, buff=0.45)
        swm = MathTex(r'\int_0^\infty \frac{d\omega}{\omega}\,\mathrm{Re}\,\sigma_{xx}(\omega)', r'\ \propto\ ',
                      r'\int_{\rm BZ} d^dk\ g_{xx}(\mathbf k)', font_size=40).move_to([2.9, 1.3, 0])
        swm[0].set_color(C_G); swm[2].set_color(C_G)
        swm_t = txt('Souza--Wilkens--Martin sum rule', 30, YELLOW).next_to(swm, DOWN, buff=0.35)
        with self.narrate('mea1') as b:
            self.play(Write(title), run_time=1.4)
            b.wait_sentence(1)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(sp), Create(gap), FadeIn(gapl), FadeIn(sch), run_time=1.5)
            b.wait_sentence(2)
            self.play(ReplacementTransform(sp.copy(), weighted), run_time=1.2)
            self.play(FadeIn(area), run_time=0.8)
            self.play(Write(swm), run_time=2.2)
            b.wait_sentence(3)
            self.play(FadeIn(swm_t, shift=0.15 * UP), run_time=0.9)

        # ---------------- mea2: bound on the gap
        chain = MathTex(r'\frac{e^2}{2m}G_{xx}', '=', r'\int\frac{d\omega}{2\pi}\,\frac{\sigma^{\rm abs}(\omega)}{\omega}', r'\ \le\ ',
                        r'\frac{1}{E_g}\int\frac{d\omega}{2\pi}\,\sigma^{\rm abs}(\omega)', '=', r'\frac{e^2 n}{2mE_g}', font_size=34)
        chain.move_to([2.7, -0.6, 0])
        if chain.width > 7.2:
            chain.scale_to_fit_width(7.2).move_to([2.7, -0.6, 0])
        bound = MathTex(r'E_g\ \le\ \frac{n}{G_{xx}}', font_size=46, color=YELLOW).move_to([2.7, -2.0, 0])
        units = txt('($\\hbar = 1$; $n$: electron density, $G$: integrated metric)', 22, GREY_T).next_to(bound, DOWN, buff=0.2)
        with self.narrate('mea2') as b:
            self.play(FadeOut(swm_t), swm.animate.scale(0.8).move_to([2.8, 2.1, 0]), run_time=0.8)
            self.play(Indicate(gap, color=YELLOW), run_time=1.0)
            self.play(Write(chain), run_time=3.0)
            self.play(Write(bound), FadeIn(units), run_time=1.6)

        # ---------------- mea3: ARPES quasi-QGT
        sample = Polygon([-5.6, -1.7, 0], [-3.0, -1.7, 0], [-2.4, -1.1, 0], [-5.0, -1.1, 0], stroke_color=GREY_C,
                         fill_color='#2b3350', fill_opacity=1)
        photon = VGroup(*[ParametricFunction(lambda t: np.array([-6.2 + 2.0 * t, 0.6 - 1.9 * t + 0.08 * np.sin(40 * t), 0]),
                                             t_range=[0, 1], color=C_E, stroke_width=3)])
        hv = MathTex(r'h\nu\ (\circlearrowleft / \circlearrowright)', font_size=28, color=C_E).move_to([-6.0, 0.95, 0])
        elec = Arrow([-4.0, -1.35, 0], [-2.6, 0.6, 0], buff=0, color=C_ELEC, stroke_width=4)
        el = MathTex(r'e^-(\mathbf k, \text{spin})', font_size=28, color=C_ELEC).next_to(elec.get_end(), RIGHT, buff=0.12)
        arpes_l = txt('photoemission (ARPES)', 28, GREY_A).next_to(sample, DOWN, buff=0.25)
        qgt = MathTex(r'Q^n_{ij}', '=', r'\sum_{m\neq n}\frac{\langle u_n|\partial_i H|u_m\rangle\langle u_m|\partial_j H|u_n\rangle}{(E_m-E_n)^2}',
                      font_size=32)
        qq = MathTex(r'q^n_{ij}', '=', r'\sum_{m\neq n}\frac{\langle u_n|\partial_i H|u_m\rangle\langle u_m|\partial_j H|u_n\rangle}{E_m-E_n}',
                     font_size=32)
        qq[0].set_color(YELLOW)
        two = MathTex(r'\text{two bands:}\quad g \approx \mathrm{Re}\,q\,/\,\Delta\varepsilon', font_size=34, color=C_G)
        eqs = VGroup(VGroup(txt('quantum geometric tensor', 24, GREY_T), qgt).arrange(DOWN, buff=0.1),
                     VGroup(txt('quasi-QGT (from band curvature and circular dichroism)', 24, YELLOW), qq).arrange(DOWN, buff=0.1),
                     two).arrange(DOWN, buff=0.35).move_to([2.6, 0.2, 0])
        cosn = kagome([-4.0, 1.85, 0], a=0.42, n=2)
        cosn_l = txt('kagome metal CoSn', 26, C_A).next_to(cosn, RIGHT, buff=0.25)
        agree = txt('measured metric $\\approx$ theory (Kang \\emph{et al.}, 2025)', 28, C_J).to_edge(DOWN, buff=0.4).shift(2.0 * RIGHT)
        with self.narrate('mea3') as b:
            self.play(FadeOut(VGroup(ax, xl, yl, sp, weighted, area, gap, gapl, sch, swm, chain, bound, units)), run_time=0.8)
            self.play(FadeIn(sample), Create(photon), FadeIn(hv), run_time=1.0)
            self.play(GrowArrow(elec), FadeIn(el), FadeIn(arpes_l), run_time=1.0)
            self.play(FadeIn(eqs[0]), run_time=1.2)
            self.play(FadeIn(eqs[1]), run_time=1.2)
            self.play(FadeIn(eqs[2]), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(cosn), FadeIn(cosn_l), run_time=1.2)
            self.play(FadeIn(agree, shift=0.15 * UP), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
