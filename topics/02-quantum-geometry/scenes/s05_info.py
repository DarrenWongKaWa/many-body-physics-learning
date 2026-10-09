import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def bell(ax, mu, sig=0.55, color=WHITE, opacity=0.35):
    f = lambda x: np.exp(-(x - mu) ** 2 / (2 * sig ** 2))
    curve = ax.plot(f, x_range=[-3, 3, 0.02], color=color, stroke_width=3)
    area = ax.get_area(curve, x_range=[-3, 3], color=color, opacity=opacity)
    return VGroup(area, curve)


def state_pair(center, angle, color2, label2):
    """Two unit 'state' arrows separated by `angle` (a cartoon of neighbouring states)."""
    c = np.asarray(center, float)
    a1 = Arrow(c, c + 1.5 * np.array([np.cos(PI / 2 + angle / 2), np.sin(PI / 2 + angle / 2), 0]), buff=0,
               color=WHITE, stroke_width=5)
    a2 = Arrow(c, c + 1.5 * np.array([np.cos(PI / 2 - angle / 2), np.sin(PI / 2 - angle / 2), 0]), buff=0,
               color=color2, stroke_width=5)
    l1 = MathTex(r'|\psi(\lambda)\rangle', font_size=30).next_to(a1.get_end(), LEFT, buff=0.15)
    l2 = MathTex(label2, font_size=30, color=color2).next_to(a2.get_end(), RIGHT, buff=0.15)
    return VGroup(a1, a2, l1, l2)


class S05_Info(NScene):
    def construct(self):
        title = txt('The quantum metric as information', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- info1: parameter estimation
        lam_line = NumberLine(x_range=[0, 1, 0.25], length=4.0, include_ticks=True, color=GREY_B).move_to([-3.6, -1.6, 0])
        lt = ValueTracker(0.35)
        knob = always_redraw(lambda: Triangle(fill_color=YELLOW, fill_opacity=1, stroke_width=0).scale(0.12).rotate(PI)
                             .next_to(lam_line.n2p(lt.get_value()), UP, buff=0.02))
        lam_l = MathTex(r'\lambda', font_size=38, color=YELLOW).next_to(lam_line, LEFT, buff=0.3)
        src = Circle(radius=0.95, stroke_color=GREY_B).move_to([-3.6, 0.6, 0])
        st_arrow = always_redraw(lambda: Arrow(src.get_center(), src.get_center() + 0.95 * np.array(
            [np.sin(2.6 * lt.get_value()), np.cos(2.6 * lt.get_value()), 0]), buff=0, color=C_A, stroke_width=5))
        st_l = MathTex(r'|\psi(\lambda)\rangle', font_size=36, color=C_A).next_to(src, UP, buff=0.2)
        meter = RoundedRectangle(width=2.0, height=1.3, corner_radius=0.15, stroke_color=GREY_B, fill_color=C_PANEL,
                                 fill_opacity=1).move_to([0.8, 0.6, 0])
        needle_arc = Arc(radius=0.6, start_angle=PI * 0.15, angle=PI * 0.7, color=GREY_B).move_arc_center_to(meter.get_center() + 0.4 * DOWN)
        needle = always_redraw(lambda: Line(meter.get_center() + 0.4 * DOWN, meter.get_center() + 0.4 * DOWN + 0.55 * np.array(
            [np.cos(PI * (0.85 - 0.7 * lt.get_value())), np.sin(PI * (0.85 - 0.7 * lt.get_value())), 0]), color=YELLOW, stroke_width=3))
        meas_l = txt('measure', 28, GREY_A).next_to(meter, UP, buff=0.15)
        flow = Arrow(src.get_right(), meter.get_left(), buff=0.25, color=GREY_B, stroke_width=3)
        est = MathTex(r'\Rightarrow\ \text{estimate}\ \hat\lambda', font_size=38).next_to(meter, RIGHT, buff=0.4)
        with self.narrate('info1') as b:
            self.play(Write(title), run_time=1.5)
            b.wait_sentence(1)
            self.play(Create(lam_line), FadeIn(lam_l), FadeIn(knob), Create(src), FadeIn(st_l), GrowArrow(st_arrow), run_time=1.4)
            self.play(lt.animate.set_value(0.7), run_time=1.3)
            self.play(GrowArrow(flow), FadeIn(meter), Create(needle_arc), FadeIn(needle), FadeIn(meas_l), run_time=1.0)
            self.play(FadeIn(est), lt.animate.set_value(0.5), run_time=1.3)

        # ---------------- info2: close vs far states; QFI = 4 g
        left = state_pair([-4.2, 0.0, 0], 0.18, GREY_B, r'|\psi(\lambda+d\lambda)\rangle')
        right = state_pair([1.6, 0.0, 0], 1.3, C_G, r'|\psi(\lambda+d\lambda)\rangle')
        axl = Axes(x_range=[-3, 3, 1], y_range=[0, 1.2, 1], x_length=3.6, y_length=1.2, tips=False,
                   axis_config=dict(stroke_color=GREY_D, include_ticks=False)).move_to([-4.2, -1.8, 0])
        axr = axl.copy().move_to([1.6, -1.8, 0])
        hl = VGroup(bell(axl, -0.12, color=WHITE), bell(axl, 0.12, color=GREY_B))
        hr = VGroup(bell(axr, -1.1, color=WHITE), bell(axr, 1.1, color=C_G))
        cap_l = txt('small $g$: outcomes overlap', 28, GREY_A).next_to(axl, DOWN, buff=0.25)
        cap_r = txt('large $g$: easy to tell apart', 28, C_G).next_to(axr, DOWN, buff=0.25)
        qfi = MathTex(r'F_Q(\lambda)', '=', r'4\,g_{\lambda\lambda}(\lambda)', font_size=48)
        qfi[2].set_color(C_G)
        crb = MathTex(r'\delta\lambda\ \ge\ \frac{1}{\sqrt{N\,F_Q}}', font_size=40)
        qfi_t = txt('quantum Fisher information', 28, GREY_A)
        crb_t = txt('Cram\\\'er--Rao bound ($N$ repetitions)', 28, GREY_A)
        box_q = VGroup(VGroup(qfi_t, qfi).arrange(DOWN, buff=0.15), VGroup(crb_t, crb).arrange(DOWN, buff=0.15)
                       ).arrange(DOWN, buff=0.4).move_to([4.6, 0.0, 0])
        with self.narrate('info2') as b:
            self.play(FadeOut(VGroup(lam_line, lam_l, src, st_l, meter, needle_arc, meas_l, flow, est)), FadeOut(knob),
                      FadeOut(st_arrow), FadeOut(needle), run_time=0.8)
            self.play(FadeIn(left), Create(axl), FadeIn(hl), run_time=1.2)
            self.play(FadeIn(cap_l), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(right), Create(axr), FadeIn(hr), FadeIn(cap_r), run_time=1.4)
            b.wait_sentence(2)
            grp = VGroup(left, axl, hl, cap_l, right, axr, hr, cap_r)
            self.play(grp.animate.scale(0.8).shift(1.3 * LEFT), run_time=0.8)
            self.play(FadeIn(qfi_t), Write(qfi), run_time=1.6)
            self.play(FadeIn(crb_t), Write(crb), run_time=1.6)
            self.play(Indicate(qfi[2], color=C_G), run_time=1.0)

        # ---------------- info3: sudden-quench measurement of g
        lax = Axes(x_range=[0, 4, 1], y_range=[-2, 2, 1], x_length=5.0, y_length=4.0, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-3.3, -0.4, 0])
        lxl = MathTex(r'\lambda', font_size=34, color=GREY_B).next_to(lax.x_axis, RIGHT, buff=0.1)
        lyl = MathTex(r'E', font_size=34, color=GREY_B).next_to(lax.y_axis, UP, buff=0.1)
        ep = lambda x: np.sqrt(0.35 + 0.6 * (x - 2) ** 2)
        up = lax.plot(ep, x_range=[0, 4], color=C_B, stroke_width=4)
        dn = lax.plot(lambda x: -ep(x), x_range=[0, 4], color=C_A, stroke_width=4)
        upl = MathTex(r'|u_+\rangle', font_size=32, color=C_B).next_to(up.get_end(), RIGHT, buff=0.1)
        dnl = MathTex(r'|u_-\rangle', font_size=32, color=C_A).next_to(dn.get_end(), RIGHT, buff=0.1)
        x0, dx = 1.55, 0.55
        g0 = Dot(lax.c2p(x0, -ep(x0)), color=WHITE, radius=0.09)
        v1 = DashedLine(lax.c2p(x0, -2), lax.c2p(x0, 2), color=GREY_D)
        v2 = DashedLine(lax.c2p(x0 + dx, -2), lax.c2p(x0 + dx, 2), color=YELLOW)
        kick = Arrow(lax.c2p(x0, 1.75), lax.c2p(x0 + dx, 1.75), buff=0, color=YELLOW, stroke_width=4,
                     max_tip_length_to_length_ratio=0.35)
        kl = MathTex(r'\delta\lambda', font_size=32, color=YELLOW).next_to(kick, UP, buff=0.05)
        pe = Dot(lax.c2p(x0 + dx, ep(x0 + dx)), color=C_B, radius=0.09)
        pg = Dot(lax.c2p(x0 + dx, -ep(x0 + dx)), color=C_A, radius=0.09)
        steps = VGroup(txt('1. prepare the ground state at $\\lambda_0$', 28),
                       txt('2. suddenly jump to $\\lambda_0+\\delta\\lambda$', 28),
                       txt('3. measure: probability $P_+$ of being excited', 28)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps.move_to([3.2, 1.3, 0])
        res = MathTex(r'P_+', r'\ \simeq\ ', r'g(\lambda_0)', r'\,\delta\lambda^2', font_size=52).move_to([3.0, -1.2, 0])
        res[0].set_color(C_B); res[2].set_color(C_G)
        with self.narrate('info3') as b:
            self.play(FadeOut(VGroup(grp, box_q)), title.animate.become(txt('Measuring the metric directly', 40, bold=True).to_edge(UP, buff=0.4)),
                      run_time=0.9)
            self.play(Create(lax), FadeIn(lxl), FadeIn(lyl), Create(up), Create(dn), FadeIn(upl), FadeIn(dnl), run_time=1.5)
            b.wait_sentence(1)
            self.play(FadeIn(g0, scale=2), Create(v1), FadeIn(steps[0]), run_time=1.0)
            self.play(GrowArrow(kick), FadeIn(kl), Create(v2), FadeIn(steps[1]), run_time=1.2)
            self.play(ReplacementTransform(g0.copy(), pg), ReplacementTransform(g0.copy().set_opacity(0.6), pe), FadeOut(g0), run_time=1.2)
            self.play(Flash(pe, color=C_B), FadeIn(steps[2]), run_time=1.0)
            b.wait_sentence(2)
            self.play(Write(res), run_time=1.5)
            self.play(Circumscribe(res, color=C_G), run_time=1.2)

        # ---------------- info4: first measurements (schematic)
        k0 = 1.3
        gk = lambda k: min(2.6, 0.025 / (((k - k0) ** 2 + 0.012)) + 0.025 / (((k + k0) ** 2 + 0.012)))
        gax = Axes(x_range=[-2.6, 2.6, 1], y_range=[0, 2.8, 1], x_length=5.0, y_length=2.6, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([2.6, -1.0, 0])
        gcurve = gax.plot(gk, x_range=[-2.6, 2.6, 0.005], color=C_G, stroke_width=4)
        gxl = MathTex('k', font_size=30, color=GREY_B).next_to(gax.x_axis, RIGHT, buff=0.1)
        gyl = MathTex('g(k)', font_size=30, color=C_G).next_to(gax.y_axis, UP, buff=0.1)
        dps = VGroup(*[txt('Dirac point', 24, GREY_A).next_to(gax.c2p(s * k0, 0), DOWN, buff=0.15) for s in (-1, 1)])
        sch = txt('(schematic)', 22, GREY_D).next_to(gax, DOWN, buff=0.55)
        refs = VGroup(txt('superconducting qubit', 30, C_A), txt('Tan \\emph{et al.}, 2019', 24, GREY_T),
                      txt('exciton-polariton microcavity', 30, C_B), txt('Gianfrate \\emph{et al.}, 2020', 24, GREY_T))
        refs.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        refs[2].shift(0.3 * DOWN); refs[3].shift(0.3 * DOWN)
        refs.move_to([-3.8, 0.4, 0])
        with self.narrate('info4') as b:
            self.play(FadeOut(VGroup(lax, lxl, lyl, up, dn, upl, dnl, v1, v2, kick, kl, pe, pg, steps)),
                      res.animate.scale(0.75).move_to([2.6, 2.0, 0]), run_time=0.9)
            self.play(FadeIn(refs[:2], shift=0.2 * RIGHT), run_time=1.0)
            self.play(FadeIn(refs[2:], shift=0.2 * RIGHT), Create(gax), FadeIn(gxl), FadeIn(gyl), run_time=1.2)
            self.play(Create(gcurve), FadeIn(dps), FadeIn(sch), run_time=2.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
