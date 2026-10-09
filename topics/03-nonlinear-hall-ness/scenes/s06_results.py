import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def blues(n):
    cm = matplotlib.colormaps['Blues']
    return [rgb_to_color(cm(0.35 + 0.65 * i / (n - 1))[:3]) for i in range(n)]


class S06_Results(NScene):
    def construct(self):
        d = load('fig1b.npz')
        E = np.r_[0, d['E']]
        J = np.r_[np.zeros((1, len(d['mus']))), d['JyE']] * 1e3
        ax = Axes(x_range=[0, 0.35, 0.05], y_range=[0, 2.4, 0.5], x_length=9.6, y_length=5.2, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=24,
                                   decimal_number_config=dict(num_decimal_places=2)),
                  y_axis_config=dict(decimal_number_config=dict(num_decimal_places=1)))
        ax.shift(0.05 * DOWN + 0.9 * LEFT)
        xl = MathTex('E', font_size=36).next_to(ax.x_axis, DOWN, buff=0.45)
        yl = MathTex(r'J_y/E\ \ (\times 10^{-3})', font_size=32).rotate(PI / 2).next_to(ax.y_axis, LEFT, buff=0.55)
        cols = blues(len(d['mus']))
        curves = VGroup(*[ax.plot_line_graph(E, J[:, i], add_vertex_dots=False, line_color=cols[i],
                                             stroke_width=3.5) for i in range(len(d['mus']))])
        leg = VGroup(*[VGroup(Line(ORIGIN, 0.4 * RIGHT, color=cols[i], stroke_width=4),
                              MathTex(rf'\mu={m:.2f}', font_size=24)).arrange(RIGHT, buff=0.1)
                       for i, m in enumerate(d['mus'])])
        leg.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax, RIGHT, buff=0.35).align_to(ax, UP)
        gam = MathTex(r'\Gamma = 0.1', font_size=30).next_to(leg, DOWN, aligned_edge=LEFT, buff=0.15)
        src = zh('按论文的常数-Γ 热库 NEGF 方法重新计算', 18, GREY_C).to_corner(DR, buff=0.2)
        with self.narrate('res1') as b:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(src), run_time=1.5)
            self.play(FadeIn(leg), FadeIn(gam), run_time=0.8)
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.15), run_time=max(0.8, b.remaining() - 0.3))

        with self.narrate('res2') as b:
            win = Rectangle(width=ax.c2p(0.022, 0)[0] - ax.c2p(0, 0)[0], height=5.2, stroke_width=0,
                            fill_color=C_J, fill_opacity=0.12).move_to(ax.c2p(0.011, 1.2))
            # straight-line guide for mu = 0.42 at weak field: Jy/E ~ slope * E
            slope = J[3, -1] / E[3]
            guide = DashedLine(ax.c2p(0, 0), ax.c2p(0.05, 0.05 * slope), color=WHITE, stroke_width=2.5)
            law = MathTex(r'J_y/E \propto E', r'\ \Rightarrow\ ', r'J_y\propto E^2', font_size=36)
            law[2].set_color(C_J)
            law.next_to(ax.c2p(0.012, 2.3), DR, buff=0.05)
            self.play(FadeIn(win), Create(guide), run_time=1.5)
            self.play(Write(law), run_time=1.5)

        with self.narrate('res3') as b:
            box1 = Rectangle(width=ax.c2p(0.045, 0)[0] - ax.c2p(0.018, 0)[0],
                             height=ax.c2p(0, 0.85)[1] - ax.c2p(0, 0.2)[1], color=C_BOX1, stroke_width=4)
            box1.move_to(ax.c2p(0.0315, 0.525))
            l1 = MathTex(r"E\approx 0.03", font_size=30, color=C_BOX1).next_to(box1, UP, buff=0.12)
            self.play(FadeOut(win), FadeOut(guide), law.animate.set_opacity(0.4), run_time=0.6)
            self.play(Create(box1), FadeIn(l1), run_time=1.2)
            self.play(*[c.animate.set_stroke(width=6) for c in curves[5:]], run_time=0.8)
            self.play(*[c.animate.set_stroke(width=3.5) for c in curves[5:]], run_time=0.6)

        with self.narrate('res4') as b:
            box2 = Rectangle(width=ax.c2p(0.125, 0)[0] - ax.c2p(0.08, 0)[0],
                             height=ax.c2p(0, 0.52)[1] - ax.c2p(0, 0.27)[1], color=C_BOX2, stroke_width=4)
            box2.move_to(ax.c2p(0.1025, 0.395))
            l2 = MathTex(r'E\sim\Gamma', font_size=30, color=C_BOX2).next_to(box2, DOWN, buff=0.12)
            self.play(Create(box2), FadeIn(l2), run_time=1.2)
            b.wait_sentence(1)
            dec = Arrow(ax.c2p(0.262, 2.32), ax.c2p(0.30, 1.98), buff=0, color=C_HOT, stroke_width=5)
            dl = zh('随电场减小', 24, C_HOT).next_to(dec, LEFT, buff=0.1).shift(0.15 * DOWN)
            self.play(GrowArrow(dec), FadeIn(dl), run_time=1.2)

        with self.narrate('res5') as b:
            lens = Circle(radius=0.75, color=WHITE, stroke_width=3).move_to(ax.c2p(0.14, 1.32))
            lzs = VGroup(zh('朗道–齐纳–斯图克尔贝格干涉', 26), zh('上下两带相干振幅之间', 22, GREY_A)
                         ).arrange(DOWN, buff=0.08).next_to(ax, UP, buff=0.1).set_x(lens.get_x())
            if LANG == 'zh':
                lzs.next_to(lens, UP, buff=0.12)
            self.play(Create(lens), run_time=0.8)
            self.play(FadeIn(lzs), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
