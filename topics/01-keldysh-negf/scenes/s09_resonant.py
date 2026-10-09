import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

E0, KT = 0.5, 0.025


class S09_Resonant(NScene):
    def construct(self):
        sig = MathTex(r'\Sigma^{r,a}(\varepsilon) = \Lambda(\varepsilon) \mp \tfrac{i}{2}\,\Gamma(\varepsilon),\qquad \Gamma = \Gamma^L + \Gamma^R',
                      font_size=38).to_edge(UP, buff=0.4)
        Aeq = MathTex(r'A(\varepsilon) = \frac{\Gamma}{(\varepsilon - \varepsilon_0 - \Lambda)^2 + (\Gamma/2)^2}', font_size=40)
        Aeq.next_to(sig, DOWN, buff=0.35)
        ax = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[0, 30, 10], x_length=8, y_length=3.4, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_ticks=False)).shift(1.8 * DOWN)
        xl = MathTex(r'\varepsilon - \varepsilon_0', font_size=30).next_to(ax.x_axis, RIGHT, buff=0.1)
        G = ValueTracker(0.15)
        peak = always_redraw(lambda: ax.plot(lambda e: lorentz_A(e, 0, G.get_value()), x_range=[-1.5, 1.5, 0.004],
                                             color=C_DOT, stroke_width=4))
        gl = always_redraw(lambda: MathTex(rf'\Gamma = {G.get_value():.2f}', font_size=32, color=C_DOT)
                           .next_to(ax.c2p(0.55, 22), RIGHT))
        with self.narrate('re1') as b:
            self.play(Write(sig), run_time=2.0)
            b.wait_sentence(1)
            self.play(Write(Aeq), Create(ax), FadeIn(xl), run_time=1.5)
            self.add(peak, gl)
            self.play(FadeIn(peak), run_time=0.6)
        with self.narrate('re2') as b:
            unc = MathTex(r'\Delta t \sim \hbar/\Gamma', font_size=36, color=C_HI).next_to(ax.c2p(-1.4, 22), RIGHT)
            self.play(G.animate.set_value(0.5), FadeIn(unc), run_time=2.5)
            self.play(G.animate.set_value(0.2), run_time=max(1.0, b.remaining() - 0.3))
        # time domain: an electron placed on the dot leaks out
        self.play(VGroup(ax, xl, unc).animate.scale(0.62).move_to([3.6, -1.6, 0]), run_time=1.0)
        tax = Axes(x_range=[0, 40, 10], y_range=[-1.05, 1.05, 1], x_length=6.2, y_length=3.0, tips=False,
                   axis_config=dict(include_ticks=False, stroke_color=GREY_B)).move_to([-3.4, -1.6, 0])
        ttl = MathTex(r't', font_size=30).next_to(tax.x_axis, RIGHT, buff=0.1)
        osc = always_redraw(lambda: tax.plot(lambda t: np.exp(-G.get_value() * t / 2) * np.cos(1.6 * t), x_range=[0, 40, 0.02],
                                             color=C_FWD, stroke_width=2.5))
        prob = always_redraw(lambda: tax.plot(lambda t: np.exp(-G.get_value() * t), x_range=[0, 40, 0.05],
                                              color=C_DOT, stroke_width=4.5))
        tl = VGroup(MathTex(r'\mathrm{Re}\,G^r(t)', font_size=28, color=C_FWD),
                    MathTex(r'|G^r(t)|^2 = e^{-\Gamma t/\hbar}', font_size=30, color=C_DOT)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tl.next_to(tax, UP, buff=0.1).align_to(tax, RIGHT)
        fourier = VGroup(MathTex(r'\longleftrightarrow', font_size=48), en('Fourier', 22, GREY_A)).arrange(DOWN, buff=0.05)
        fourier.move_to([0.45, -1.3, 0])
        with self.narrate('re2b') as b:
            self.play(Create(tax), FadeIn(ttl), run_time=0.8)
            b.wait_sentence(1)
            self.add(osc, prob)
            self.play(FadeIn(osc), FadeIn(prob), FadeIn(tl), run_time=1.2)
            b.wait_sentence(2)
            self.play(FadeIn(fourier), run_time=0.6)
            self.play(G.animate.set_value(0.45), run_time=max(1.2, (b.remaining() - 0.5) / 2))
            self.play(G.animate.set_value(0.18), run_time=max(1.2, b.remaining() - 0.4))
        for m in (peak, gl, osc, prob):
            m.clear_updaters()
        self.play(FadeOut(VGroup(sig, Aeq, ax, xl, peak, gl, unc, tax, ttl, osc, prob, tl, fourier)), run_time=0.6)

        s_less = MathTex(r'\Sigma^<(\varepsilon) = i\,[\Gamma^L f_L(\varepsilon) + \Gamma^R f_R(\varepsilon)]', font_size=38).to_edge(UP, buff=0.4)
        gless = MathTex(r'G^< = G^r\Sigma^<G^a = i\,A(\varepsilon)\,\bar f(\varepsilon)', r',\qquad',
                        r'\bar f = \frac{\Gamma^L f_L + \Gamma^R f_R}{\Gamma}', font_size=38).next_to(s_less, DOWN, buff=0.35)
        gless[2].set_color(C_LESS)
        ax2 = Axes(x_range=[-1.5, 1.5, 0.5], y_range=[0, 1.1, 0.5], x_length=8, y_length=3.0, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).shift(1.8 * DOWN)
        al = ValueTracker(0.5)
        fL = ax2.plot(lambda e: fermi(e, 0.6, 0.05), x_range=[-1.5, 1.5, 0.01], color=C_L, stroke_width=2.5)
        fR = ax2.plot(lambda e: fermi(e, -0.6, 0.05), x_range=[-1.5, 1.5, 0.01], color=C_R, stroke_width=2.5)
        fL, fR = DashedVMobject(fL, num_dashes=50), DashedVMobject(fR, num_dashes=50)
        fb = always_redraw(lambda: ax2.plot(lambda e: al.get_value() * fermi(e, 0.6, 0.05) + (1 - al.get_value()) * fermi(e, -0.6, 0.05),
                                            x_range=[-1.5, 1.5, 0.01], color=C_LESS, stroke_width=4.5))
        labs = VGroup(MathTex('f_L', color=C_L, font_size=30).next_to(ax2.c2p(0.6, 0.55), RIGHT, buff=0.1),
                      MathTex('f_R', color=C_R, font_size=30).next_to(ax2.c2p(-0.6, 0.55), LEFT, buff=0.1),
                      MathTex(r'\bar f', color=C_LESS, font_size=34).next_to(ax2.c2p(0, 0.6), UP, buff=0.1))
        ratio = always_redraw(lambda: MathTex(rf'\Gamma^L/\Gamma = {al.get_value():.2f}', font_size=30)
                              .next_to(ax2, UP, buff=0.05).align_to(ax2, RIGHT))
        with self.narrate('re3') as b:
            self.play(Write(s_less), run_time=1.8)
            self.play(Create(ax2), Create(fL), Create(fR), FadeIn(labs[:2]), run_time=1.2)
            b.wait_sentence(1)
            self.play(Write(gless), run_time=2.0)
            self.add(fb, ratio)
            self.play(FadeIn(labs[2]), run_time=0.5)
            self.play(al.animate.set_value(0.85), run_time=1.5)
            self.play(al.animate.set_value(0.25), run_time=max(1.0, b.remaining() - 0.3))
        fb.clear_updaters()
        ratio.clear_updaters()
        self.play(FadeOut(VGroup(s_less, gless, ax2, fL, fR, fb, labs, ratio)), run_time=0.6)

        fbar = MathTex(r'\bar f = \frac{\Gamma^L}{\Gamma}\,f_L + \frac{\Gamma^R}{\Gamma}\,f_R', font_size=44).to_edge(UP, buff=0.4)
        plast = en(r'$\Gamma^\alpha/\Gamma$ = probability that lead $\alpha$ touched the dot last', 26, GREY_A).next_to(fbar, DOWN, buff=0.25)
        rng = np.random.default_rng(11)
        tline = Arrow([-6.2, -2.3, 0], [6.4, -2.3, 0], buff=0, color=GREY_B, stroke_width=2.5)
        tlab = MathTex('t', font_size=28).next_to(tline, RIGHT, buff=0.1)
        x, events = -6.0, []
        while True:
            x += rng.exponential(0.42)
            if x > 6.0:
                break
            events.append((x, 'L' if rng.random() < 0.7 else 'R'))
        ticks = VGroup(*[Line([ex, -2.55, 0], [ex, -2.05, 0], color=C_L if who == 'L' else C_R, stroke_width=4) for ex, who in events])
        y0, y1 = -1.6, -0.2
        pts, state = [[-6.0, y0, 0]], 0
        for ex, who in events:
            new_state = 1 if who == 'L' else 0
            pts.append([ex, y1 if state else y0, 0])
            pts.append([ex, y1 if new_state else y0, 0])
            state = new_state
        pts.append([6.0, y1 if state else y0, 0])
        trace = VMobject(stroke_color=C_LESS, stroke_width=4).set_points_as_corners(pts)
        occ_time = 0.0
        prev_x, prev_s = -6.0, 0
        for ex, who in events:
            occ_time += (ex - prev_x) * prev_s
            prev_x, prev_s = ex, (1 if who == 'L' else 0)
        occ_time += (6.0 - prev_x) * prev_s
        ylabs = VGroup(en('filled', 22, C_LESS).next_to([-6.0, y1, 0], LEFT, buff=0.1),
                       en('empty', 22, GREY_A).next_to([-6.0, y0, 0], LEFT, buff=0.1))
        legend = VGroup(VGroup(Line(ORIGIN, 0.35 * UP, color=C_L, stroke_width=4), en(r'lead L resets it: filled ($f_L = 1$)', 22, C_L)).arrange(RIGHT, buff=0.15),
                        VGroup(Line(ORIGIN, 0.35 * UP, color=C_R, stroke_width=4), en(r'lead R resets it: empty ($f_R = 0$)', 22, C_R)).arrange(RIGHT, buff=0.15)
                        ).arrange(RIGHT, buff=0.8).next_to(tline, DOWN, buff=0.45)
        frac = en(rf'time filled: {occ_time / 12.0:.2f} $\approx \Gamma^L/\Gamma = 0.70$', 26, C_LESS).move_to([0, 0.75, 0])
        with self.narrate('re3b') as b:
            self.play(Write(fbar), run_time=1.2)
            self.play(Create(tline), FadeIn(tlab), FadeIn(ylabs), FadeIn(legend), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(trace, rate_func=linear), LaggedStart(*[FadeIn(t) for t in ticks], lag_ratio=1.0, rate_func=linear),
                      run_time=max(3.0, b.sentence_start(2) - b.elapsed() + 1.5))
            b.wait_sentence(2)
            self.play(FadeIn(plast), FadeIn(frac), run_time=1.0)
        self.play(FadeOut(VGroup(fbar, plast, tline, tlab, ticks, trace, ylabs, legend, frac)), run_time=0.6)

        J = MathTex(r'J = \frac{e}{\hbar}\int\!\frac{d\varepsilon}{2\pi}\,', r'\frac{\Gamma^L\Gamma^R}{(\varepsilon-\varepsilon_0-\Lambda)^2 + (\Gamma/2)^2}',
                    r'\,[f_L(\varepsilon) - f_R(\varepsilon)]', font_size=42).to_edge(UP, buff=0.4)
        J[1].set_color(C_DOT)
        bw = VGroup(MathTex(r'T(\varepsilon)', font_size=32, color=C_DOT), zh('布赖特–维格纳', 26, C_DOT)).arrange(RIGHT, buff=0.2)
        bw.next_to(J[1], DOWN, buff=0.25)
        with self.narrate('re4') as b:
            self.play(Write(J), run_time=2.5)
            b.wait_sentence(1)
            self.play(FadeIn(bw), Indicate(J[1], color=C_DOT), run_time=1.2)

        # I-V: level enters the bias window
        GL = GR = 0.04
        Vs = np.linspace(0, 2.0, 161)
        I1 = np.array([current_gf(v, E0, GL, GR, KT) for v in Vs]) / (GL * GR / (GL + GR))
        I2 = np.array([current_gf(v, E0, 0.15, 0.15, KT) for v in Vs]) / (0.15 * 0.15 / 0.3)
        iax = Axes(x_range=[0, 2, 0.5], y_range=[0, 1.1, 0.5], x_length=5.6, y_length=3.6, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                    decimal_number_config=dict(num_decimal_places=1))).to_edge(RIGHT, buff=0.6).shift(1.0 * DOWN)
        ixl = MathTex('V', font_size=30).next_to(iax.x_axis, DOWN, buff=0.35)
        iyl = MathTex(r'J / J_{\max}', font_size=28).next_to(iax, UP, buff=0.1)
        V = ValueTracker(0.0)
        # energy diagram on the left
        eax = Axes(x_range=[-1, 1, 1], y_range=[-1.3, 1.3, 1], x_length=5.6, y_length=4.2, tips=False,
                   axis_config=dict(stroke_opacity=0)).to_edge(LEFT, buff=0.6).shift(1.0 * DOWN)

        def diagram():
            v = V.get_value()
            g = VGroup()
            g.add(Rectangle(width=1.8, height=eax.c2p(0, v / 2)[1] - eax.c2p(0, -1.3)[1], fill_color=C_L, fill_opacity=0.35,
                            stroke_width=0).align_to(eax.c2p(-1, -1.3), DL))
            g.add(Rectangle(width=1.8, height=eax.c2p(0, -v / 2)[1] - eax.c2p(0, -1.3)[1], fill_color=C_R, fill_opacity=0.35,
                            stroke_width=0).align_to(eax.c2p(1, -1.3), DR))
            prof = eax.plot_parametric_curve(lambda e: np.array([0.32 * lorentz_A(e, E0, 0.08) / lorentz_A(E0, E0, 0.08), e, 0]),
                                             t_range=[-1.2, 1.2, 0.005], color=C_DOT, stroke_width=3)
            g.add(prof)
            g.add(MathTex(r'\mu_L', font_size=28, color=C_L).next_to(eax.c2p(-1, v / 2), LEFT, buff=0.08))
            g.add(MathTex(r'\mu_R', font_size=28, color=C_R).next_to(eax.c2p(1, -v / 2), RIGHT, buff=0.08))
            return g
        dia = always_redraw(diagram)
        e0l = MathTex(r'\varepsilon_0', font_size=28, color=C_DOT).next_to(eax.c2p(0.35, E0), RIGHT, buff=0.05)
        trace = always_redraw(lambda: iax.plot_line_graph(Vs[Vs <= V.get_value() + 1e-9], I1[Vs <= V.get_value() + 1e-9],
                                                          add_vertex_dots=False, line_color=C_LESS, stroke_width=4)
                              if V.get_value() > 0.02 else VMobject())
        tdot = always_redraw(lambda: Dot(iax.c2p(V.get_value(), np.interp(V.get_value(), Vs, I1)), color=WHITE, radius=0.07))
        r = ValueTracker(0.5)
        rax = Axes(x_range=[-1, 1, 1], y_range=[0, 1.1, 0.5], x_length=5.4, y_length=3.0, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-3.3, -1.5, 0])
        rxl = MathTex(r'\varepsilon - \varepsilon_0', font_size=26).next_to(rax.x_axis, RIGHT, buff=0.1)
        one = DashedLine(rax.c2p(-1, 1), rax.c2p(1, 1), color=GREY_B, stroke_width=2)
        onel = MathTex('1', font_size=26).next_to(rax.c2p(-1, 1), LEFT, buff=0.1)
        tcur = always_redraw(lambda: rax.plot(lambda e: 4 * r.get_value() * (1 - r.get_value()) / (1 + (e / 0.15) ** 2),
                                              x_range=[-1, 1, 0.005], color=C_DOT, stroke_width=4))
        rlab = always_redraw(lambda: MathTex(rf'\Gamma^L/\Gamma = {r.get_value():.2f}', font_size=28).next_to(rax, UP, buff=0.1).align_to(rax, LEFT))
        pk = MathTex(r'\mathcal T_{\max} = \frac{4\,\Gamma^L\Gamma^R}{(\Gamma^L+\Gamma^R)^2}', font_size=32).next_to(rax, UP, buff=0.1).align_to(rax, RIGHT)
        fp = en(r"symmetric barriers: $\mathcal T = 1$ on resonance (Fabry--P\'erot)", 22, C_DOT).next_to(rax, DOWN, buff=0.3)

        def resistor(p, w=1.6, color=WHITE):
            xs_ = np.linspace(0, w, 9)
            pts_ = [np.array(p) + np.array([x, (0.18 if i % 2 else -0.18) if 0 < i < 8 else 0, 0]) for i, x in enumerate(xs_)]
            return VMobject(stroke_color=color, stroke_width=4).set_points_as_corners(pts_)
        r1_ = resistor([1.2, -0.9, 0], color=C_L)
        r2_ = resistor([3.4, -0.9, 0], color=C_R)
        wires = VGroup(Line([0.6, -0.9, 0], [1.2, -0.9, 0]), Line([2.8, -0.9, 0], [3.4, -0.9, 0]), Line([5.0, -0.9, 0], [5.6, -0.9, 0]))
        rl_ = VGroup(MathTex(r'1/\Gamma^L', font_size=28, color=C_L).next_to(r1_, UP, buff=0.15),
                     MathTex(r'1/\Gamma^R', font_size=28, color=C_R).next_to(r2_, UP, buff=0.15))
        ser = MathTex(r'J_{\max} = \frac{e}{\hbar}\,\frac{\Gamma^L\Gamma^R}{\Gamma^L+\Gamma^R}', r'\quad\Leftrightarrow\quad',
                      r'\frac{1}{J_{\max}} \propto \frac{1}{\Gamma^L} + \frac{1}{\Gamma^R}', font_size=32).move_to([3.3, -2.1, 0])
        if ser.get_right()[0] > 6.9:
            ser.scale_to_fit_width(6.9 - 0.0 - (ser.get_left()[0] if ser.get_left()[0] > -0.2 else -0.2)).move_to([3.3, -2.1, 0])
        neck = en('the weaker barrier is the bottleneck', 24, C_HI).next_to(ser, DOWN, buff=0.25)
        with self.narrate('re4b') as b:
            self.play(Create(rax), FadeIn(rxl), Create(one), FadeIn(onel), run_time=0.8)
            self.add(tcur, rlab)
            self.play(FadeIn(tcur), FadeIn(rlab), FadeIn(pk), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(fp), Indicate(one, color=C_DOT), run_time=1.0)
            self.play(r.animate.set_value(0.9), run_time=1.5)
            self.play(r.animate.set_value(0.5), run_time=1.2)
            b.wait_sentence(2)
            self.play(Create(wires), Create(r1_), Create(r2_), FadeIn(rl_), run_time=1.2)
            self.play(Write(ser), run_time=1.5)
            self.play(FadeIn(neck), run_time=0.8)
        tcur.clear_updaters()
        rlab.clear_updaters()
        self.play(FadeOut(VGroup(rax, rxl, one, onel, tcur, rlab, pk, fp, r1_, r2_, wires, rl_, ser, neck)), run_time=0.6)
        with self.narrate('re5') as b:
            self.play(FadeOut(bw), J.animate.scale(0.75).to_edge(UP, buff=0.25), run_time=0.6)
            self.play(Create(iax), FadeIn(ixl), FadeIn(iyl), FadeIn(dia), FadeIn(e0l), run_time=1.2)
            self.add(trace, tdot)
            self.play(V.animate.set_value(2.0), run_time=max(3.0, b.sentence_start(2) - b.elapsed() + 1.0), rate_func=linear)
            b.wait_sentence(2)
            c2 = iax.plot_line_graph(Vs, I2, add_vertex_dots=False, line_color=C_HI, stroke_width=3)
            l2 = VGroup(zh('能级宽度更大', 22, C_HI)).next_to(iax.c2p(1.25, 0.35), RIGHT, buff=0.05)
            self.play(Create(c2), FadeIn(l2), run_time=1.5)
        for m in (dia, trace, tdot):
            m.clear_updaters()
        self.clear()


class S10_Master(NScene):
    def construct(self):
        s0 = VGroup(Circle(radius=0.55, color=GREY_B), MathTex('0', font_size=40)).move_to([-2.2, 1.6, 0])
        s1 = VGroup(Circle(radius=0.55, color=C_DOT, fill_opacity=0.3), MathTex('1', font_size=40)).move_to([2.2, 1.6, 0])
        l0 = zh('空', 24, GREY_A).next_to(s0, DOWN, buff=0.15)
        l1 = zh('占据', 24, C_DOT).next_to(s1, DOWN, buff=0.15)
        a01 = CurvedArrow(s0.get_top() + 0.1 * UP, s1.get_top() + 0.1 * UP, angle=-PI / 3, color=C_LESS)
        a10 = CurvedArrow(s1.get_bottom() + 0.1 * DOWN + 0.0 * LEFT, s0.get_bottom() + 0.1 * DOWN, angle=-PI / 3, color=C_GTR)
        P = MathTex('P_0 + P_1 = 1', font_size=34).move_to([0, 1.6, 0])
        with self.narrate('ma1') as b:
            self.play(FadeIn(s0), FadeIn(s1), FadeIn(l0), FadeIn(l1), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(P), run_time=0.6)
        r01 = MathTex(r'\hbar\Gamma_{0\to1} = \Gamma^L f_L + \Gamma^R f_R', font_size=34, color=C_LESS).next_to(a01, UP, buff=0.1)
        r10 = MathTex(r'\hbar\Gamma_{1\to0} = \Gamma^L(1-f_L) + \Gamma^R(1-f_R)', font_size=34, color=C_GTR).next_to(a10, DOWN, buff=0.4)
        # stochastic hopping across a mini junction (large bias: in from L, out to R)
        y = -2.5
        lead_l = Rectangle(width=2.4, height=1.2, fill_color=C_L, fill_opacity=0.35, stroke_width=0).move_to([-3.4, y, 0])
        lead_r = Rectangle(width=2.4, height=1.2, fill_color=C_R, fill_opacity=0.35, stroke_width=0).move_to([3.4, y, 0])
        dot = Circle(radius=0.3, color=C_DOT).move_to([0, y, 0])
        cnt = ValueTracker(0)
        counter = always_redraw(lambda: VGroup(zh('穿过的电子', 22, GREY_A), Integer(int(cnt.get_value()), font_size=30))
                                .arrange(RIGHT, buff=0.15).next_to(lead_r, UP, buff=0.2))
        with self.narrate('ma2') as b:
            self.play(Create(a01), Create(a10), run_time=1.0)
            self.play(FadeIn(lead_l), FadeIn(lead_r), FadeIn(dot), FadeIn(counter), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(r01), FadeIn(r10), run_time=1.2)
            rng = np.random.default_rng(7)
            occ = False
            while b.remaining() > 1.4:
                wait = float(rng.exponential(0.5))
                self.wait(min(wait, max(0.0, b.remaining() - 1.3)))
                e = Dot(radius=0.09, color=WHITE)
                if not occ:
                    e.move_to([-2.4, y, 0])
                    self.play(e.animate.move_to(dot), s1[0].animate.set_fill(C_DOT, 0.8), run_time=0.35)
                    dot.set_fill(C_DOT, 0.8)
                    self.remove(e)
                else:
                    e.move_to(dot)
                    self.add(e)
                    dot.set_fill(C_DOT, 0)
                    self.play(e.animate.move_to([2.4, y, 0]), s1[0].animate.set_fill(C_DOT, 0.3), run_time=0.35)
                    self.remove(e)
                    cnt.increment_value(1)
                occ = not occ
        counter.clear_updaters()
        self.play(FadeOut(VGroup(lead_l, lead_r, dot, counter, P)), VGroup(s0, s1, l0, l1, a01, a10, r01, r10).animate.scale(0.7).to_edge(UP, buff=0.2),
                  run_time=0.7)
        ss = MathTex(r'P_1 = \frac{\Gamma^L f_L + \Gamma^R f_R}{\Gamma^L + \Gamma^R}', font_size=40)
        Ime = MathTex(r'I = \frac{e}{\hbar}\,\frac{\Gamma^L\Gamma^R}{\Gamma}\,[f_L(\varepsilon_0) - f_R(\varepsilon_0)]', font_size=40)
        VGroup(ss, Ime).arrange(RIGHT, buff=1.0).shift(0.2 * UP)
        with self.narrate('ma3') as b:
            self.play(Write(ss), run_time=1.5)
            self.play(Write(Ime), run_time=1.5)
        self.play(FadeOut(VGroup(s0, s1, l0, l1, a01, a10, r01, r10)), VGroup(ss, Ime).animate.scale(0.8).to_edge(UP, buff=0.3),
                  run_time=0.6)
        Vs = np.linspace(0, 2.0, 121)
        me = np.array([current_me(v, E0, 1, 1, KT) for v in Vs]) / 0.5
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 1.1, 0.5], x_length=8, y_length=4.0, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                   decimal_number_config=dict(num_decimal_places=1))).shift(1.3 * DOWN)
        xl = MathTex('V', font_size=30).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = MathTex(r'J/J_{\max}', font_size=28).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        mec = DashedVMobject(ax.plot_line_graph(Vs, me, add_vertex_dots=False, line_color=WHITE, stroke_width=3)['line_graph'],
                             num_dashes=60)
        Gt = ValueTracker(0.25)

        def gf_curve():
            g = Gt.get_value()
            I = np.array([current_gf(v, E0, g / 2, g / 2, KT, n=3001) for v in Vs]) / (g / 4)
            return ax.plot_line_graph(Vs, I, add_vertex_dots=False, line_color=C_LESS, stroke_width=4)
        gfc = always_redraw(gf_curve)
        gl = always_redraw(lambda: MathTex(rf'\Gamma/k_BT = {Gt.get_value() / KT:.1f}', font_size=30, color=C_LESS)
                           .next_to(ax.c2p(1.25, 0.45), RIGHT))
        leg = VGroup(VGroup(DashedLine(ORIGIN, 0.5 * RIGHT, color=WHITE), zh('主方程', 22)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, 0.5 * RIGHT, color=C_LESS, stroke_width=4), zh('格林函数（精确）', 22)).arrange(RIGHT, buff=0.1)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(ax.c2p(0.05, 1.05), DR, buff=0.05)
        with self.narrate('ma4') as b:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), Create(mec), FadeIn(leg), run_time=1.5)
            self.add(gfc, gl)
            self.play(Gt.animate.set_value(0.004), run_time=4.0)
            ok = zh('弱耦合：一致', 24, C_LESS).next_to(ax.c2p(1.25, 0.25), RIGHT)
            self.play(FadeIn(ok), run_time=0.6)
            b.wait_sentence(1)
            self.play(Gt.animate.set_value(0.2), FadeOut(ok), run_time=2.5)
            bad = zh('Γ ≳ kT：主方程失效', 24, C_HI).next_to(ax.c2p(1.25, 0.25), RIGHT)
            self.play(FadeIn(bad), run_time=0.6)
        gfc.clear_updaters()
        gl.clear_updaters()
        self.play(FadeOut(VGroup(ax, xl, yl, mec, gfc, gl, leg, bad, ss, Ime)), run_time=0.6)

        Vb, gl_, kt_ = 0.4, 0.01, 0.025
        ds = np.linspace(0.02, 0.8, 40)
        jg = np.array([current_gf(Vb, Vb / 2 + d, gl_, gl_, kt_) for d in ds]) / (gl_ / 2)
        jm = np.array([current_me(Vb, Vb / 2 + d, gl_, gl_, kt_) for d in ds]) / (gl_ / 2)
        lg, lm = np.log10(np.maximum(jg, 1e-12)), np.log10(np.maximum(jm, 1e-12))
        lg, lm = lg + 9, lm + 9                    # plot log10(J/Jmax) + 9 so the x axis sits at the bottom
        lax = Axes(x_range=[0, 0.8, 0.2], y_range=[0, 9, 3], x_length=7.6, y_length=4.4, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_numbers=False)).shift(0.5 * DOWN + 1.2 * RIGHT)
        ylab = VGroup(*[MathTex(rf'10^{{{k}}}', font_size=24).next_to(lax.c2p(0, k + 9), LEFT, buff=0.1) for k in (0, -3, -6, -9)])
        xlab = VGroup(MathTex('d', font_size=28), en('= distance of the level above the bias window', 22, GREY_A)).arrange(RIGHT, buff=0.1)
        xlab.next_to(lax, DOWN, buff=0.3)
        ttl = MathTex(r'J/J_{\max}', font_size=28).next_to(lax, UP, buff=0.1).align_to(lax, LEFT)
        sel = lm > 0
        cme = DashedVMobject(lax.plot_line_graph(ds[sel], lm[sel], add_vertex_dots=False, line_color=WHITE, stroke_width=3)['line_graph'],
                             num_dashes=40)
        cgf = lax.plot_line_graph(ds, lg, add_vertex_dots=False, line_color=C_LESS, stroke_width=4)
        lme = en(r'master eq.: thermal activation $\propto e^{-d/k_BT}$', 22, WHITE).next_to(lax.c2p(0.42, np.interp(0.42, ds, lm)), RIGHT, buff=0.3)
        lgf = en(r"Green's function: quantum tails $\propto \Gamma^2/d^2$", 22, C_LESS).next_to(lax.c2p(0.5, np.interp(0.5, ds, lg)), UP, buff=0.25)
        # inset: the level sits above the window
        inset = VGroup(Rectangle(width=1.6, height=0.5, fill_color=C_LESS, fill_opacity=0.25, stroke_width=0),
                       Line(LEFT * 0.4, RIGHT * 0.4, color=C_DOT, stroke_width=5).shift(0.75 * UP))
        inset.add(en('window', 18, C_LESS).move_to(inset[0]), MathTex(r'\varepsilon_0', font_size=24, color=C_DOT).next_to(inset[1], RIGHT, buff=0.1),
                  DoubleArrow(inset[0].get_top(), inset[1].get_center(), buff=0, color=GREY_B, stroke_width=2, tip_length=0.1))
        inset.add(MathTex('d', font_size=24).next_to(inset[4], LEFT, buff=0.05))
        inset.to_edge(LEFT, buff=0.7).shift(0.6 * UP)
        with self.narrate('ma4b') as b:
            self.play(FadeIn(inset), Create(lax), FadeIn(ylab), FadeIn(xlab), FadeIn(ttl), run_time=1.2)
            b.wait_sentence(1)
            self.play(Create(cme), FadeIn(lme), run_time=1.5)
            b.wait_sentence(2)
            self.play(Create(cgf), FadeIn(lgf), run_time=1.8)
        self.play(FadeOut(VGroup(inset, lax, ylab, xlab, ttl, cme, cgf, lme, lgf)), run_time=0.6)
        eom = MathTex(r'\frac{\partial P_1}{\partial t} = \sum_\alpha \Gamma^\alpha f_\alpha(\varepsilon_0)\,P_0 - \sum_\alpha\Gamma^\alpha'
                      r'\,[1 - f_\alpha(\varepsilon_0)]\,P_1', font_size=42).shift(0.6 * UP)
        warn = VGroup(Triangle(color=YELLOW, fill_opacity=0.2).scale(0.3), zh('宽带极限 · 几处可疑的近似', 26, YELLOW)).arrange(RIGHT, buff=0.3)
        warn.next_to(eom, DOWN, buff=0.6)
        with self.narrate('ma5') as b:
            self.play(Write(eom), run_time=2.0)
            self.play(FadeIn(warn), run_time=1.0)
        self.clear()


class S11_Summary(NScene):
    def construct(self):
        t = zh('总结', 44, weight=BOLD).to_edge(UP, buff=0.5)
        with self.narrate('su1') as b:
            self.play(Write(t), run_time=1.0)
        items = [('1', '不回到初态 → 沿凯尔迪什回路先向前、再向后', C_FWD),
                 ('2', '回路上的戴森方程 + 朗格雷斯规则 → 实时间分量', C_BWD),
                 ('3', '凯尔迪什方程与电流公式；共振能级 = 布赖特–维格纳，弱耦合回到主方程', C_LESS),
                 ('4', '注入 → 有限寿命传播 → 占据由动力学决定', C_HI)]
        rows = VGroup()
        for n, txt, c in items:
            num = VGroup(Circle(radius=0.3, color=c, stroke_width=3), Text(n, font_size=30, color=c))
            body = zh(txt, 26)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.6).next_to(t, DOWN, buff=0.7)
        if rows.width > 13.0:
            rows.scale_to_fit_width(13.0)
        rows.set_x(0)
        eqs = VGroup(MathTex(r'G^< = G^r\Sigma^<G^a', font_size=34, color=C_LESS),
                     MathTex(r'J = \frac{ie}{\hbar}\int\!\frac{d\varepsilon}{2\pi}[f_L - f_R]\,\mathcal T(\varepsilon)', font_size=34)
                     ).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.7)
        for key, row in zip(['su2', 'su3', 'su4', 'su4b'], rows):
            with self.narrate(key) as b:
                self.play(FadeIn(row[0], scale=1.5), FadeIn(row[1], shift=0.2 * RIGHT), run_time=1.2)
                if key == 'su4':
                    self.play(FadeIn(eqs), run_time=1.0)
        with self.narrate('su5') as b:
            self.play(FadeOut(VGroup(t, rows, eqs)), run_time=0.8)
            ref = VGroup(Text('A.-P. Jauho', font_size=28),
                         Text('Introduction to the Keldysh nonequilibrium Green function technique', font_size=26, color=BLUE_B),
                         zh('（讲义）', 22, GREY_B)).arrange(DOWN, buff=0.25)
            cred = zh('动画：Manim  ·  配音：Kokoro-82M（本地）', 20, GREY_C).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(ref, shift=0.2 * UP), run_time=1.2)
            self.play(FadeIn(cred), run_time=0.8)
        self.wait(1.5)
        self.clear(1.0)
