import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def loop(x0, x1, ytop, ybot, c_top, c_bot, width=4):
    """Out along ytop to x1, U-turn, back along ybot to x0."""
    top = Line([x0, ytop, 0], [x1, ytop, 0]).set_stroke(c_top, width)
    turn = ArcBetweenPoints([x1, ytop, 0], [x1, ybot, 0], angle=-PI).set_stroke(GREY_B, width)
    bot = Line([x1, ybot, 0], [x0, ybot, 0]).set_stroke(c_bot, width)
    return VGroup(top, turn, bot)


class S05_Langreth(NScene):
    def construct(self):
        title = zh('朗格雷斯定理', 40, weight=BOLD).to_edge(UP, buff=0.4)
        arrow = VGroup(zh('回路上的戴森方程', 28, GREY_A), MathTex(r'\Longrightarrow', font_size=40),
                       zh('实时间的推迟 / 超前 / 小于分量', 28, C_LESS)).arrange(RIGHT, buff=0.3).next_to(title, DOWN, buff=0.5)
        with self.narrate('la1') as b:
            self.play(FadeIn(arrow), run_time=1.5)
            b.wait_sentence(1)
            self.play(Write(title), run_time=1.0)
        self.play(FadeOut(arrow), run_time=0.5)

        conv = MathTex(r"C(t_1,t_{1'}) = \int_C d\tau\,A(t_1,\tau)\,B(\tau,t_{1'})", font_size=40).next_to(title, DOWN, buff=0.4)
        x0, a, bpos = -5.5, 0.0, 2.6
        orig = loop(x0, 4.0, 0.45, -0.45, C_FWD, C_BWD).shift(0.3 * UP)
        m1 = VGroup(Cross(scale_factor=0.1, stroke_color=WHITE, stroke_width=4).move_to([a, 0.75, 0]),
                    MathTex('t_1', font_size=30).move_to([a, 1.1, 0]))
        m2 = VGroup(Cross(scale_factor=0.1, stroke_color=C_HI, stroke_width=4).move_to([bpos, -0.15, 0]),
                    MathTex("t_{1'}", font_size=30, color=C_HI).move_to([bpos, -0.55, 0]))
        want = MathTex(r"\Rightarrow\ C^<(t_1,t_{1'})", font_size=38, color=C_LESS).next_to(orig, RIGHT, buff=0.2)
        with self.narrate('la2') as b:
            self.play(Write(conv), run_time=1.8)
            self.play(Create(orig), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(m1), FadeIn(m2), run_time=0.8)
            self.play(FadeIn(want), run_time=0.8)
        # deformed contour: C1 loops around t1, C1' loops around t1'
        c1 = loop(x0, a, 1.0, 0.4, C_FWD, C_FWD)
        link = ArcBetweenPoints([x0, 0.4, 0], [x0, -0.2, 0], angle=PI).set_stroke(GREY_C, 4)
        c2 = loop(x0, bpos, -0.2, -0.8, C_BWD, C_BWD)
        c2.shift(UP * 0)
        lab1 = MathTex('C_1', font_size=32, color=C_FWD).next_to(c1, LEFT, buff=0.15)
        lab2 = MathTex("C_1'", font_size=32, color=C_BWD).next_to(c2, LEFT, buff=0.15)
        with self.narrate('la3') as b:
            self.play(ReplacementTransform(orig, VGroup(c1, link, c2)),
                      m1.animate.move_to([a + 0.3, 0.7, 0]), m2.animate.move_to([bpos + 0.3, -0.5, 0]),
                      FadeOut(want), run_time=2.5)
            self.play(FadeIn(lab1), FadeIn(lab2), run_time=0.8)
        eq25 = MathTex(r"C^<(t_1,t_{1'}) =", r"\int_{C_1}\! d\tau\,A(t_1,\tau)\,B^<(\tau,t_{1'})", r"+",
                       r"\int_{C_1'}\! d\tau\,A^<(t_1,\tau)\,B(\tau,t_{1'})", font_size=34).to_edge(DOWN, buff=1.4)
        eq25[1].set_color(C_FWD)
        eq25[3].set_color(C_BWD)
        eq26 = MathTex(r"\int_{C_1}\!\!=\int_{-\infty}^{t_1}\!\! dt\,A^>B^< + \int_{t_1}^{-\infty}\!\! dt\,A^<B^<",
                       r"= \int_{-\infty}^{\infty}\! dt\,", r"A^r(t_1,t)\,B^<(t,t_{1'})", font_size=34).to_edge(DOWN, buff=0.35)
        eq26[2].set_color(C_FWD)
        with self.narrate('la4') as b:
            self.play(Write(eq25), run_time=2.0)
            self.play(Indicate(c1, color=C_FWD), run_time=0.8)
            self.play(Write(eq26[0]), run_time=1.6)
            self.play(Write(eq26[1:]), run_time=1.2)
            b.wait_sentence(1)
            self.play(Indicate(c2, color=C_BWD), Indicate(eq25[3], color=C_BWD), run_time=1.2)
        self.play(FadeOut(VGroup(conv, c1, link, c2, lab1, lab2, m1, m2, eq25, eq26)), run_time=0.7)

        r1 = MathTex(r'C^<', r'=', r'A^r B^<', r'+', r'A^< B^a', font_size=48).next_to(title, DOWN, buff=0.6)
        r1[2][0:2].set_color(C_FWD)
        r1[2][2:].set_color(C_LESS)
        r1[4][0:2].set_color(C_LESS)
        r1[4][2:].set_color(C_BWD)
        r2 = MathTex(r'D^<', '=', r'A^rB^rC^<', '+', r'A^rB^<C^a', '+', r'A^<B^aC^a', font_size=44).next_to(r1, DOWN, buff=0.6)
        for term, k in ((r2[2], 2), (r2[4], 1), (r2[6], 0)):
            pass
        slide = SurroundingRectangle(r2[2][4:6], color=C_LESS, buff=0.05)
        rule = VGroup(MathTex('<', font_size=36, color=C_LESS), zh('左边全是推迟，右边全是超前', 26, GREY_A)).arrange(RIGHT, buff=0.3)
        rule.next_to(r2, DOWN, buff=0.4)
        r3 = MathTex(r'C^r = A^r B^r', font_size=44, color=C_FWD).next_to(rule, DOWN, buff=0.5)
        with self.narrate('la5') as b:
            self.play(Write(r1), run_time=2.0)
            b.wait_sentence(1)
            self.play(Write(r2), run_time=2.0)
            self.play(Create(slide), FadeIn(rule), run_time=0.8)
            self.play(slide.animate.become(SurroundingRectangle(r2[4][2:4], color=C_LESS, buff=0.05)), run_time=0.8)
            self.play(slide.animate.become(SurroundingRectangle(r2[6][0:2], color=C_LESS, buff=0.05)), run_time=0.8)
            b.wait_sentence(2)
            self.play(Write(r3), run_time=1.2)
        # ----- the path picture: switch from the ket branch to the bra branch exactly once
        self.play(FadeOut(VGroup(r1, slide, rule, r3)), r2.animate.next_to(title, DOWN, buff=0.45), run_time=0.8)
        ytop, ybot = 0.6, -1.4
        xs = [-4.2, -1.4, 1.4, 4.2]
        rails = VGroup(Line([-5.4, ytop, 0], [5.4, ytop, 0], color=C_FWD, stroke_width=3, stroke_opacity=0.6),
                       Line([-5.4, ybot, 0], [5.4, ybot, 0], color=C_BWD, stroke_width=3, stroke_opacity=0.6))
        rl = VGroup(en(r'forward branch: ket history $\rightarrow$ retarded', 24, C_FWD).next_to(rails[0], UP, buff=0.15),
                    en(r'backward branch: bra history $\rightarrow$ advanced', 24, C_BWD).next_to(rails[1], DOWN, buff=0.75))
        names = [r"t_1", r"\tau_1", r"\tau_2", r"t_{1'}"]
        letters = ['A', 'B', 'C']

        def config(k):
            # link k is the one that switches branches
            ys = [ytop, ytop if k >= 1 else ybot, ytop if k >= 2 else ybot, ybot]
            g = VGroup()
            pts = [np.array([x, y, 0]) for x, y in zip(xs, ys)]
            for i in range(3):
                top0, top1 = ys[i] == ytop, ys[i + 1] == ytop
                c, sup = (C_FWD, 'r') if top0 and top1 else ((C_LESS, '<') if top0 else (C_BWD, 'a'))
                arr = Arrow(pts[i], pts[i + 1], buff=0.12, color=c, stroke_width=5, max_tip_length_to_length_ratio=0.12)
                lab = MathTex(rf'{letters[i]}^{sup}', font_size=34, color=c).next_to(arr.get_center(), RIGHT if top0 != top1 else UP, buff=0.12)
                g.add(arr, lab)
            for i, pnt in enumerate(pts):
                g.add(Dot(pnt, radius=0.09, color=WHITE),
                      MathTex(names[i], font_size=30).next_to(pnt, UP if ys[i] == ytop else DOWN, buff=0.15 if ys[i] == ytop else 0.15))
            return g
        terms = [r2[6], r2[4], r2[2]]
        with self.narrate('la5b') as b:
            self.play(Create(rails), FadeIn(rl), run_time=1.2)
            b.wait_sentence(1)
            path = config(2)
            self.play(FadeIn(path), run_time=1.2)
            box = SurroundingRectangle(terms[2], color=C_LESS, buff=0.08)
            self.play(Create(box), run_time=0.6)
            b.wait_sentence(2)
            per = max(1.2, (b.remaining() - 0.8) / 2)
            for k in (1, 0):
                self.play(Transform(path, config(k)), box.animate.become(SurroundingRectangle(terms[k], color=C_LESS, buff=0.08)),
                          run_time=per * 0.6)
                self.wait(per * 0.4)
        self.play(FadeOut(VGroup(r2, rails, rl, path, box)), run_time=0.6)

        rows = [(r'C=\int_C AB', r'C^<=\int_t[A^rB^<+A^<B^a]', r'C^r=\int_t A^rB^r'),
                (r'D=\int_C ABC', r'D^<=\int_t[A^rB^rC^<+A^rB^<C^a+A^<B^aC^a]', r'D^r=\int_t A^rB^rC^r'),
                (r"C(\tau,\tau')=A(\tau,\tau')B(\tau,\tau')", r"C^<=A^<B^<", r"C^r=A^<B^r+A^rB^<+A^rB^r"),
                (r"D(\tau,\tau')=A(\tau,\tau')B(\tau',\tau)", r"D^<=A^<(t,t')B^>(t',t)", r"D^r=A^<B^a+A^rB^<")]
        tab = VGroup()
        for i, (c, l, r) in enumerate(rows):
            row = VGroup(MathTex(c, font_size=28), MathTex(l, font_size=28, color=C_LESS), MathTex(r, font_size=28, color=C_FWD))
            for j, m in enumerate(row):
                m.move_to([[-4.3, 0.2, 4.6][j], 1.3 - 0.75 * i, 0])
            tab.add(row)
        hdr = VGroup(zh('回路', 24, GREY_A).move_to([-4.3, 2.0, 0]), zh('实时间', 24, GREY_A).move_to([2.4, 2.0, 0]))
        rule_l = Line([-6.5, 1.7, 0], [6.8, 1.7, 0], color=GREY_D)
        eph = MathTex(r"\Sigma^r_{\rm ph}(k,\omega) = \sum_q M_q^2\Big[\frac{N_q + 1 - n_F(\varepsilon_{k-q})}{\omega-\omega_q-\varepsilon_{k-q}+i\eta}"
                      r"+\frac{N_q + n_F(\varepsilon_{k-q})}{\omega+\omega_q-\varepsilon_{k-q}+i\eta}\Big]", font_size=32)
        eph0 = MathTex(r"\Sigma_{\rm ph}(k,\tau,\tau') = i\sum_q |M_q|^2\, G(k-q,\tau,\tau')\,D(q,\tau,\tau')", font_size=32)
        ephs = VGroup(eph0, eph).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)
        with self.narrate('la6') as b:
            self.play(FadeIn(hdr), Create(rule_l), LaggedStart(*[FadeIn(r, shift=0.1 * UP) for r in tab], lag_ratio=0.3),
                      run_time=2.5)
            b.wait_sentence(1)
            self.play(FadeIn(eph0), Indicate(tab[2], color=C_HI), run_time=1.5)
            self.play(Write(eph), run_time=2.0)
        self.clear()


class S06_Keldysh(NScene):
    def construct(self):
        e37 = MathTex(r'G^< = G_0^< + G_0^r\Sigma^rG^< + G_0^r\Sigma^<G^a + G_0^<\Sigma^aG^a', font_size=42).shift(1.8 * UP)
        with self.narrate('ke1') as b:
            self.play(Write(e37), run_time=2.5)
        e39 = MathTex(r'G^< =', r'(1 + G^r\Sigma^r)\,G_0^<\,(1 + \Sigma^aG^a)', r'+', r'G^r\,\Sigma^<\,G^a', font_size=46)
        e39[1].set_color(GREY_A)
        e39[3].set_color(C_LESS)
        it = zh('迭代到所有阶', 24, GREY_A).next_to(e37, DOWN, buff=0.35)
        with self.narrate('ke2') as b:
            self.play(FadeIn(it), run_time=0.6)
            self.play(TransformMatchingShapes(e37.copy(), e39), run_time=2.0)
            lab1 = zh('初始状态', 24, GREY_A).next_to(e39[1], DOWN, buff=0.3)
            lab2 = zh('推迟 × 小于自能 × 超前', 24, C_LESS).next_to(e39[3], DOWN, buff=0.3)
            self.play(FadeIn(lab1), run_time=0.6)
            self.play(FadeIn(lab2), run_time=0.6)
        with self.narrate('ke3') as b:
            cross = Cross(e39[1], stroke_color=RED, stroke_width=5)
            ss = zh('稳态：远古无相互作用', 24, RED).next_to(lab1, DOWN, buff=0.2)
            self.play(Create(cross), FadeIn(ss), run_time=1.2)
            fin = MathTex(r'G^< = G^r\,\Sigma^<\,G^a', font_size=56, color=C_LESS).shift(2.0 * DOWN)
            box = SurroundingRectangle(fin, color=C_LESS, buff=0.2)
            self.play(TransformFromCopy(e39[3], fin), Create(box), run_time=1.5)
            b.wait_sentence(1)
            note = MathTex(r'\Sigma^< = \Sigma^<[G^<]', font_size=36, color=C_HI).next_to(box, RIGHT, buff=0.5)
            nl = zh('积分方程（自洽）', 24, C_HI).next_to(note, DOWN, buff=0.15)
            self.play(FadeIn(note), FadeIn(nl), run_time=1.0)

        # ----- occupation = injection rate x dwell time
        keep = VGroup(fin, box)
        self.play(FadeOut(VGroup(e37, it, e39, lab1, lab2, cross, ss, note, nl)), keep.animate.scale(0.8).to_edge(UP, buff=0.3),
                  run_time=0.8)
        e0, Gm, muL, muR, kT = 0.25, 0.3, 0.7, -0.7, 0.05
        sin = lambda e: 0.5 * fermi(e, muL, kT) + 0.5 * fermi(e, muR, kT)
        dwell = lambda e: (Gm / 2) ** 2 / ((e - e0) ** 2 + (Gm / 2) ** 2)
        panels = VGroup()
        for f, c, lbl in ((sin, C_LESS, r'injection $\Sigma_{\rm in}(\varepsilon)$'),
                          (dwell, C_DOT, r'dwell time $|G^r(\varepsilon)|^2$'),
                          (lambda e: sin(e) * dwell(e), C_HI, r'occupation $n(\varepsilon)$')):
            a = Axes(x_range=[-1.6, 1.6, 1], y_range=[0, 1.1, 1], x_length=3.4, y_length=2.2, tips=False,
                     axis_config=dict(include_ticks=False, stroke_color=GREY_B))
            curve = a.plot(f, x_range=[-1.6, 1.6, 0.01], color=c, stroke_width=4)
            area = a.get_area(curve, x_range=[-1.6, 1.6], color=c, opacity=0.25)
            panels.add(VGroup(a, area, curve, en(lbl, 24, c).next_to(a, DOWN, buff=0.2)))
        ops = [MathTex(r'\times', font_size=48), MathTex('=', font_size=48)]
        row = VGroup(panels[0], ops[0], panels[1], ops[1], panels[2]).arrange(RIGHT, buff=0.35).shift(0.4 * DOWN)
        ops[0].align_to(panels[0][0], DOWN).shift(0.9 * UP)
        ops[1].align_to(panels[0][0], DOWN).shift(0.9 * UP)
        nform = MathTex(r'-iG^<(\varepsilon) = |G^r(\varepsilon)|^2\,[\Gamma^L f_L + \Gamma^R f_R]', font_size=38)
        nform.next_to(keep, DOWN, buff=0.35)
        with self.narrate('ke4') as b:
            self.play(Write(nform), run_time=1.5)
            b.wait_sentence(1)
            self.play(FadeIn(panels[0]), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(ops[0]), FadeIn(panels[1]), run_time=1.0)
            self.play(FadeIn(ops[1]), FadeIn(panels[2]), run_time=1.0)

        # ----- the memory term dies out: n(t) relaxes from any initial value
        self.play(FadeOut(VGroup(row, nform)), run_time=0.6)
        Gt = 0.1
        ts = np.linspace(0, 60, 121)
        tax = Axes(x_range=[0, 6, 1], y_range=[0, 1.05, 0.5], x_length=8.5, y_length=3.6, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                    decimal_number_config=dict(num_decimal_places=0)),
                   y_axis_config=dict(decimal_number_config=dict(num_decimal_places=1))).shift(0.6 * DOWN + 0.6 * LEFT)
        txl = MathTex(r't\ \ (\hbar/\Gamma)', font_size=28).next_to(tax.x_axis, DOWN, buff=0.4)
        tyl = MathTex(r'n(t)', font_size=30).next_to(tax.y_axis, UP, buff=0.1)
        curves = VGroup()
        for n0, c in ((1.0, C_BWD), (0.5, C_FWD), (0.0, C_GTR)):
            n = occupation_relax(ts, n0, 0.3, 0.05, 0.05, 0.5, -0.5)
            curves.add(tax.plot_line_graph(ts * Gt, n, add_vertex_dots=False, line_color=c, stroke_width=4))
        nss = occupation_relax(np.array([200.0]), 0.0, 0.3, 0.05, 0.05, 0.5, -0.5)[0]
        ssl = DashedLine(tax.c2p(0, nss), tax.c2p(6, nss), color=WHITE, stroke_width=2)
        ssl_lab = en('steady state, set by the leads', 22).next_to(tax.c2p(6, nss), UP, buff=0.1).shift(0.3 * LEFT)
        mem = MathTex(r'(1+G^r\Sigma^r)\,G_0^<\,(1+\Sigma^aG^a)\ \sim\ n_0\,e^{-\Gamma t/\hbar}', font_size=34, color=GREY_A)
        mem.next_to(tax, RIGHT, buff=0.3).shift(0.8 * UP)
        mem.next_to(keep, DOWN, buff=0.3)
        with self.narrate('ke5') as b:
            self.play(Create(tax), FadeIn(txl), FadeIn(tyl), FadeIn(mem), run_time=1.2)
            b.wait_sentence(1)
            self.play(*[Create(c) for c in curves], run_time=3.0, rate_func=linear)
            self.play(Create(ssl), FadeIn(ssl_lab), run_time=0.8)
            b.wait_sentence(2)
            self.play(Indicate(keep, color=C_LESS), run_time=1.2)
        self.clear()
