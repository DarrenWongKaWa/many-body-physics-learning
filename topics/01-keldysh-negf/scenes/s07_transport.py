import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def energy_diagram(muL, muR, e0, y0=-2.6, sc=1.5, coupled=False):
    Y = lambda e: y0 + sc * (e + 1.4)
    seaL = Rectangle(width=3.2, height=Y(muL) - y0, fill_color=C_L, fill_opacity=0.35, stroke_width=0)
    seaL.align_to([-5.0, 0, 0], LEFT).align_to([0, y0, 0], DOWN)
    seaR = Rectangle(width=3.2, height=Y(muR) - y0, fill_color=C_R, fill_opacity=0.35, stroke_width=0)
    seaR.align_to([1.8, 0, 0], LEFT).align_to([0, y0, 0], DOWN)
    lvl = Line([-0.5, Y(e0), 0], [0.5, Y(e0), 0], color=C_DOT, stroke_width=6)
    tL = MathTex(r'\mu_L', font_size=32, color=C_L).next_to([-5.0, Y(muL), 0], LEFT, buff=0.1)
    tR = MathTex(r'\mu_R', font_size=32, color=C_R).next_to([5.0, Y(muR), 0], RIGHT, buff=0.1)
    te = MathTex(r'\varepsilon_m', font_size=32, color=C_DOT).next_to(lvl, UP, buff=0.1)
    g = VGroup(seaL, seaR, lvl, tL, tR, te)
    g.Y = Y
    return g


class S07_Model(NScene):
    def construct(self):
        boxes = VGroup(*[VGroup(RoundedRectangle(corner_radius=0.15, width=w, height=1.4, stroke_color=c, fill_color=c,
                                                 fill_opacity=0.15), zh(t, 28, c))
                         for t, c, w in (('左电极', C_L, 3.2), ('中心区域', C_DOT, 2.6), ('右电极', C_R, 3.2))])
        boxes.arrange(RIGHT, buff=0.9).shift(1.8 * UP)
        for bx in boxes:
            bx[1].move_to(bx[0])
        with self.narrate('mo1') as b:
            self.play(LaggedStart(*[FadeIn(bx, shift=0.2 * UP) for bx in boxes], lag_ratio=0.3), run_time=1.8)
        ed = energy_diagram(0.9, -0.5, 0.15)
        past = zh('遥远的过去：互不耦合，各自热平衡', 26, GREY_A).to_edge(DOWN, buff=0.35)
        with self.narrate('mo2') as b:
            self.play(FadeIn(ed[:2]), FadeIn(ed[2]), FadeIn(ed[3:]), FadeIn(past), run_time=1.5)
            b.wait_sentence(1)
            Y = ed.Y
            bias = DoubleArrow([5.9, Y(-0.5), 0], [5.9, Y(0.9), 0], buff=0, color=WHITE, stroke_width=3,
                               max_tip_length_to_length_ratio=0.12)
            self.play(GrowFromCenter(bias), run_time=0.8)
        links = VGroup(*[CurvedDoubleArrow(p, q, angle=-0.6, color=C_LESS, stroke_width=3, tip_length=0.15)
                         for p, q in (([-1.7, ed.Y(0.5), 0], [-0.6, ed.Y(0.15), 0]), ([0.6, ed.Y(0.15), 0], [1.7, ed.Y(-0.2), 0]))])
        VL = MathTex('V', font_size=32, color=C_LESS).next_to(links[0], UP, buff=0.05)
        VR = MathTex('V', font_size=32, color=C_LESS).next_to(links[1], UP, buff=0.05)
        conn = VGroup(*[Line(boxes[i][0].get_right(), boxes[i + 1][0].get_left(), color=C_LESS, stroke_width=4)
                        for i in range(2)])
        allord = zh('打开隧穿耦合：在双分支回路上，求和到所有阶', 26, C_LESS).to_edge(DOWN, buff=0.35)
        with self.narrate('mo3') as b:
            self.play(FadeOut(past), Create(conn), Create(links), FadeIn(VL), FadeIn(VR), run_time=1.5)
            self.play(FadeIn(allord), run_time=0.8)
        self.play(FadeOut(VGroup(ed, bias, links, VL, VR, allord)), run_time=0.6)
        H = MathTex(r'H =', r'H_c', '+', r'H_T', '+', r'H_{\rm cen}', font_size=48).next_to(boxes, DOWN, buff=0.5)
        H[1].set_color(C_L)
        H[3].set_color(C_LESS)
        H[5].set_color(C_DOT)
        Hc = MathTex(r'H_c = \sum_{k,\alpha\in L,R}\varepsilon_{k\alpha}\,c^\dagger_{k\alpha}c_{k\alpha}', font_size=32, color=C_L)
        HT = MathTex(r'H_T = \sum_{k\alpha,n}\big[V_{k\alpha,n}\,c^\dagger_{k\alpha}d_n + \mathrm{h.c.}\big]', font_size=32, color=C_LESS)
        VGroup(Hc, HT).arrange(RIGHT, buff=1.0).next_to(H, DOWN, buff=0.4)
        cens = VGroup(MathTex(r'\sum_m \varepsilon_m\,d_m^\dagger d_m', font_size=30),
                      MathTex(r'\varepsilon_0 d^\dagger d + d^\dagger d\sum_q M_q(a_q^\dagger + a_{-q})', font_size=30),
                      MathTex(r'\sum_\sigma\varepsilon_0\,d_\sigma^\dagger d_\sigma + U n_\uparrow n_\downarrow', font_size=30))
        tags = ['非相互作用能级', '电声耦合', '安德森模型']
        cb = VGroup()
        for m, t in zip(cens, tags):
            g = VGroup(zh(t, 22, C_DOT), m).arrange(DOWN, buff=0.15)
            g.add_to_back(RoundedRectangle(corner_radius=0.1, width=max(3.6, g.width + 0.3), height=1.3, stroke_color=C_DOT,
                                           stroke_width=1.5, fill_color='#141925', fill_opacity=1))
            cb.add(g)
        cb.arrange(RIGHT, buff=0.3).to_edge(DOWN, buff=0.4)
        if cb.width > 13.6:
            cb.scale_to_fit_width(13.6)
        with self.narrate('mo4') as b:
            self.play(Write(H), run_time=1.5)
            b.wait_sentence(1)
            self.play(FadeIn(Hc), FadeIn(HT), run_time=1.2)
            b.wait_sentence(2)
            self.play(LaggedStart(*[FadeIn(c, shift=0.2 * UP) for c in cb], lag_ratio=0.3), run_time=2.0)
        self.clear()


class S08_Current(NScene):
    def construct(self):
        j1 = MathTex(r'J_L = -e\,\langle\dot N_L\rangle = -\frac{ie}{\hbar}\langle[H,N_L]\rangle', font_size=42).to_edge(UP, buff=0.5)
        j2 = MathTex(r'J_L = \frac{2e}{\hbar}\,\mathrm{Re}\Big\{\sum_{k\alpha\in L,\,n} V_{k\alpha,n}\,', r'G^<_{n,k\alpha}(t,t)', r'\Big\}',
                     font_size=40).next_to(j1, DOWN, buff=0.45)
        j2[1].set_color(C_LESS)
        with self.narrate('cu1') as b:
            self.play(Write(j1), run_time=2.0)
            b.wait_sentence(1)
            self.play(Write(j2), run_time=2.0)
            mix = zh('电极–中心区域的混合格林函数', 24, C_LESS).next_to(j2, DOWN, buff=0.2)
            self.play(FadeIn(mix), run_time=0.6)
        gam = MathTex(r'\Gamma^L_{mn}(\varepsilon) = 2\pi\sum_{\alpha\in L}\rho_\alpha(\varepsilon)\,V_{\alpha,n}V^*_{\alpha,m}', font_size=36)
        j3 = MathTex(r'J_L = \frac{ie}{\hbar}\int\!\frac{d\varepsilon}{2\pi}\,\mathrm{Tr}\Big\{\Gamma^L\big[G^<', r'+ f_L\,(G^r - G^a)', r'\big]\Big\}',
                     font_size=40)
        VGroup(gam, j3).arrange(DOWN, buff=0.4).next_to(j1, DOWN, buff=0.5)
        with self.narrate('cu2') as b:
            self.play(FadeOut(j2), FadeOut(mix), run_time=0.5)
            steps = VGroup(zh('零温运动方程', 24, GREY_A), MathTex(r'\to', font_size=32), zh('朗格雷斯延拓', 24, GREY_A),
                           MathTex(r'\to', font_size=32), zh('积掉电极', 24, GREY_A)).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.5)
            self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.3), run_time=2.0)
            self.play(Write(gam), run_time=1.6)
            self.play(Write(j3), run_time=2.0)
        self.play(FadeOut(VGroup(j1, gam, steps)), j3.animate.scale(0.8).to_edge(UP, buff=0.3), run_time=0.7)

        # ----- the current as a ledger: in-flow minus out-flow at the left barrier
        led = MathTex(r'J_L = \frac{e}{\hbar}\int\!\frac{d\varepsilon}{2\pi}\,\Gamma^L\,\big[\,f_L\,A - n\,\big]', font_size=40)
        led.next_to(j3, DOWN, buff=0.35)
        sl = en(r'single level: $n = -iG^<$, $A = i(G^r - G^a)$', 22, GREY_A).next_to(led, DOWN, buff=0.15)
        lead = Rectangle(width=2.4, height=2.0, fill_color=C_L, fill_opacity=0.3, stroke_color=C_L).move_to([-4.6, -2.2, 0])
        leadl = en('left lead', 22, C_L).move_to(lead)
        dotc = Circle(radius=0.45, color=C_DOT, fill_opacity=0.2).move_to([-0.6, -2.2, 0])
        dotl = en('dot', 22, C_DOT).move_to(dotc)
        a_in = CurvedArrow(lead.get_right() + 0.5 * UP, dotc.get_left() + 0.25 * UP, angle=-PI / 4, color=C_LESS)
        a_out = CurvedArrow(dotc.get_left() + 0.25 * DOWN, lead.get_right() + 0.5 * DOWN, angle=-PI / 4, color=C_GTR)
        l_in = MathTex(r'\text{in: } \Gamma^L f_L\,(A - n)', font_size=30, color=C_LESS).next_to(a_in, UP, buff=0.05)
        l_out = MathTex(r'\text{out: } \Gamma^L (1 - f_L)\, n', font_size=30, color=C_GTR).next_to(a_out, DOWN, buff=0.05)
        diff = MathTex(r'\text{in} - \text{out} = \Gamma^L\big[f_L A', r'- f_L n', r'- n', r'+ f_L n', r'\big]', font_size=34)
        diff.move_to([3.6, -1.7, 0])
        res = MathTex(r'= \Gamma^L\,[\,f_L A - n\,]', font_size=34, color=C_LESS).next_to(diff, DOWN, buff=0.3).align_to(diff, LEFT)
        pauli = en('Pauli blocking factors cancel', 22, GREY_A).next_to(res, DOWN, buff=0.2).align_to(res, LEFT)
        with self.narrate('cu2b') as b:
            self.play(Write(led), FadeIn(sl), run_time=1.5)
            self.play(FadeIn(lead), FadeIn(leadl), FadeIn(dotc), FadeIn(dotl), run_time=0.8)
            b.wait_sentence(1)
            self.play(Create(a_in), FadeIn(l_in), run_time=1.0)
            self.play(Create(a_out), FadeIn(l_out), run_time=1.0)
            b.wait_sentence(2)
            self.play(Write(diff), run_time=1.5)
            self.play(Create(Cross(diff[1], stroke_color=RED, stroke_width=3)), Create(Cross(diff[3], stroke_color=RED, stroke_width=3)),
                      run_time=0.8)
            self.play(FadeIn(res), FadeIn(pauli), run_time=0.8)
            b.wait_sentence(3)
            me = en(r'same rates as in the master equation', 24, C_HI).next_to(l_out, DOWN, buff=0.25)
            self.play(FadeIn(me, shift=0.2 * UP), run_time=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not j3], run_time=0.6)
        prop = MathTex(r'\Gamma^L(\varepsilon) = \lambda\,\Gamma^R(\varepsilon)', font_size=36, color=GREY_A).next_to(j3, DOWN, buff=0.3)
        J = MathTex(r'J = \frac{ie}{\hbar}\int\!\frac{d\varepsilon}{2\pi}\,', r'[f_L(\varepsilon) - f_R(\varepsilon)]', r'\,\mathcal T(\varepsilon)',
                    font_size=44).next_to(prop, DOWN, buff=0.35)
        T = MathTex(r'\mathcal T(\varepsilon) = \mathrm{Tr}\Big\{\frac{\Gamma^L\Gamma^R}{\Gamma^L + \Gamma^R}\,', r'[G^r(\varepsilon) - G^a(\varepsilon)]', r'\Big\}',
                    font_size=40).next_to(J, DOWN, buff=0.3)
        box = SurroundingRectangle(VGroup(J, T), color=C_LESS, buff=0.2)
        with self.narrate('cu3') as b:
            self.play(FadeIn(prop), run_time=0.8)
            self.play(Write(J), run_time=2.0)
            self.play(Write(T), Create(box), run_time=2.0)
        # bias window picture
        self.play(FadeOut(VGroup(j3, prop)), VGroup(J, T, box).animate.scale(0.8).to_edge(UP, buff=0.3), run_time=0.7)
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 1.15, 0.5], x_length=9, y_length=3.4, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_ticks=False)).shift(1.6 * DOWN)
        xl = MathTex(r'\varepsilon', font_size=32).next_to(ax.x_axis, RIGHT, buff=0.1)
        kT, muL, muR = 0.06, 0.6, -0.6
        fL = ax.plot(lambda e: fermi(e, muL, kT), x_range=[-2, 2, 0.01], color=C_L, stroke_width=3.5)
        fR = ax.plot(lambda e: fermi(e, muR, kT), x_range=[-2, 2, 0.01], color=C_R, stroke_width=3.5)
        win = ax.get_area(fL, x_range=[-2, 2], bounded_graph=fR, color=C_LESS, opacity=0.25)
        Tc = ax.plot(lambda e: 0.95 * transmission(e, 0.1, 0.12, 0.12) / transmission(0.1, 0.1, 0.12, 0.12),
                     x_range=[-2, 2, 0.005], color=C_DOT, stroke_width=3.5)
        labs = VGroup(MathTex('f_L', color=C_L, font_size=32).next_to(ax.c2p(muL + 0.08, 0.55), RIGHT, buff=0.05),
                      MathTex('f_R', color=C_R, font_size=32).next_to(ax.c2p(muR - 0.08, 0.55), LEFT, buff=0.05),
                      MathTex(r'\mathcal T(\varepsilon)', color=C_DOT, font_size=32).next_to(ax.c2p(0.45, 0.9), RIGHT, buff=0.05))
        wl = zh('偏压窗口', 26, C_LESS).move_to(ax.c2p(0, 0.25))
        with self.narrate('cu4') as b:
            self.play(Create(ax), FadeIn(xl), Create(fL), Create(fR), FadeIn(labs[:2]), run_time=1.5)
            self.play(FadeIn(win), FadeIn(wl), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(Tc), FadeIn(labs[2]), Indicate(T[1], color=C_DOT), run_time=1.5)
        # ----- two counter-flowing streams at every energy
        self.play(FadeOut(VGroup(ax, xl, fL, fR, win, Tc, labs, wl)), run_time=0.6)
        Ey = lambda e: -2.0 + 1.25 * e          # energy -> screen y
        seaL = Rectangle(width=3.6, height=Ey(muL) - Ey(-1.25), fill_color=C_L, fill_opacity=0.3, stroke_width=0)
        seaL.align_to([-6.0, 0, 0], LEFT).align_to([0, Ey(-1.25), 0], DOWN)
        seaR = Rectangle(width=3.6, height=Ey(muR) - Ey(-1.25), fill_color=C_R, fill_opacity=0.3, stroke_width=0)
        seaR.align_to([2.4, 0, 0], LEFT).align_to([0, Ey(-1.25), 0], DOWN)
        barrier = Rectangle(width=1.0, height=Ey(1.1) - Ey(-1.25), fill_color=GREY_D, fill_opacity=0.6, stroke_width=0)
        barrier.move_to([0, (Ey(1.1) + Ey(-1.25)) / 2, 0])
        bl = MathTex(r'\mathcal T', font_size=30).move_to(barrier).shift(UP * 1.1)
        mlL = VGroup(DashedLine([-6.0, Ey(muL), 0], [-2.4, Ey(muL), 0], color=C_L),
                     MathTex(r'\mu_L', font_size=28, color=C_L).next_to([-6.0, Ey(muL), 0], LEFT, buff=0.1))
        mlR = VGroup(DashedLine([2.4, Ey(muR), 0], [6.0, Ey(muR), 0], color=C_R),
                     MathTex(r'\mu_R', font_size=28, color=C_R).next_to([6.0, Ey(muR), 0], RIGHT, buff=0.1))
        below, window = VGroup(), VGroup()
        for e in np.linspace(-1.1, 0.95, 8):
            if e > muL:
                continue
            y = Ey(e)
            r_ar = Arrow([-2.3, y + 0.07, 0], [2.3, y + 0.07, 0], buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.05,
                         color=C_LESS if e > muR else GREY_B)
            if e < muR:
                l_ar = Arrow([2.3, y - 0.07, 0], [-2.3, y - 0.07, 0], buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.05, color=GREY_B)
                below.add(r_ar, l_ar)
            else:
                window.add(r_ar)
        cl = en('cancel', 24, GREY_B).next_to(below, RIGHT, buff=0.2).shift(2.0 * RIGHT + 0.2 * DOWN)
        cl.move_to([4.3, Ey(-0.95), 0])
        nl_ = en('net flow', 24, C_LESS).move_to([4.3, (Ey(muL) + Ey(muR)) / 2 + 0.15, 0])
        with self.narrate('cu4b') as b:
            self.play(FadeIn(seaL), FadeIn(seaR), FadeIn(barrier), FadeIn(bl), Create(mlL), Create(mlR), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in below], lag_ratio=0.1), run_time=1.5)
            self.play(LaggedStart(*[GrowArrow(a) for a in window], lag_ratio=0.15), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(cl), *[a.animate.set_opacity(0.35) for a in below], run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(nl_), *[Indicate(a, color=C_LESS) for a in window], run_time=1.2)
        with self.narrate('cu5') as b:
            n1 = zh('对相互作用系统同样成立', 26, C_LESS)
            n2 = VGroup(zh('关键：能否算出', 26, C_HI), MathTex(r'G^r,\ G^a,\ G^<', font_size=32, color=C_HI)).arrange(RIGHT, buff=0.15)
            notes = VGroup(n1, n2).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
            notes.scale_to_fit_width(min(notes.width, 6.7 - box.get_right()[0] - 0.3)).next_to(box, RIGHT, buff=0.3)
            self.play(FadeIn(n1), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(n2), run_time=0.8)
        self.clear()
