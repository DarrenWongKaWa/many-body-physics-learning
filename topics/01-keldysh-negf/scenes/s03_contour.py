import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S03_Contour(NScene):
    def construct(self):
        # ----- the state at +infinity is not the initial state
        axis = Arrow([-6, 1.5, 0], [6, 1.5, 0], buff=0, color=GREY_B, stroke_width=3)
        tl = VGroup(MathTex(r'-\infty', font_size=32).next_to([-6, 1.5, 0], DOWN, buff=0.2),
                    MathTex(r'+\infty', font_size=32).next_to([6, 1.5, 0], DOWN, buff=0.2))
        st0 = MathTex(r'|\Phi_0\rangle', font_size=40, color=C_FWD).next_to([-6, 1.5, 0], UP, buff=0.25)
        stf = MathTex(r'|\,?\,\rangle \neq |\Phi_0\rangle', font_size=40, color=C_HI).next_to([5.6, 1.5, 0], UP, buff=0.25)
        with self.narrate('co1') as b:
            self.play(GrowArrow(axis), FadeIn(tl), FadeIn(st0), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(stf, shift=0.2 * LEFT), run_time=1.0)

        # ----- atom hitting a surface exchanges charge
        surf = Rectangle(width=6, height=0.6, fill_color=GREY_D, fill_opacity=1, stroke_width=0).move_to([0, -2.9, 0])
        atom = Circle(radius=0.35, color=C_FWD, fill_opacity=0.25).move_to([-3.5, 0.2, 0])
        e = Dot(radius=0.08, color=WHITE).move_to(atom.get_center() + 0.2 * UR)
        with self.narrate('co2') as b:
            self.play(FadeIn(surf), FadeIn(atom), FadeIn(e), run_time=0.8)
            path_in = Line(atom.get_center(), [0, -2.2, 0])
            self.play(MoveAlongPath(atom, path_in), MoveAlongPath(e, path_in.copy().shift(0.2 * UR)), run_time=1.5)
            self.play(e.animate.move_to([0.4, -2.9, 0]), run_time=0.7)
            plus = MathTex('+', font_size=36, color=C_HI)
            atom.add(plus.move_to(atom))
            self.play(atom.animate.move_to([3.5, 0.2, 0]), run_time=1.5)
            lab = VGroup(zh('初态', 26, C_FWD), MathTex(r'\neq', font_size=36), zh('末态', 26, C_HI)).arrange(RIGHT, buff=0.2)
            lab.move_to([0, -0.6, 0])
            self.play(FadeIn(lab), run_time=0.8)
        self.clear()

        # ----- go forward, then come back: the Keldysh contour
        expv = MathTex(r'\langle O(t)\rangle = \mathrm{Tr}\big[\rho_0\,', r'U(t_0,t)', r'\,O\,', r'U(t,t_0)', r'\big]',
                       font_size=42).to_edge(UP, buff=0.5)
        expv[3].set_color(C_FWD)
        expv[1].set_color(C_BWD)
        cont = keldysh_contour(-5.0, 3.0, 0.3, 0.9)
        t0 = MathTex('t_0', font_size=34).next_to([-5.0, 0.3, 0], LEFT, buff=0.15)
        tt = MathTex('t', font_size=34).next_to([3.45, 0.3, 0], RIGHT, buff=0.1)
        Ot = MathTex('O', font_size=34, color=C_HI).next_to([3.45, 0.3, 0], UP, buff=0.35)
        with self.narrate('co3') as b:
            self.play(Write(expv), run_time=2.0)
            b.wait_sentence(1)
            self.play(Create(cont[0]), FadeIn(t0), Indicate(expv[3], color=C_FWD), run_time=1.5)
            self.play(Create(cont[1]), FadeIn(tt), FadeIn(Ot), run_time=0.8)
            self.play(Create(cont[2]), Indicate(expv[1], color=C_BWD), FadeIn(cont[3:]), run_time=1.5)
            rider = Dot(color=WHITE, radius=0.08)
            path = VMobject().set_points_as_corners([cont[0].get_start(), cont[0].get_end()])
            path.append_vectorized_mobject(cont[1].copy())
            path.add_line_to(cont[2].get_end())
            self.play(MoveAlongPath(rider, path), run_time=b.rest(1.5))
        labs = VGroup(VGroup(zh('前向分支', 24, C_FWD), MathTex('C_1', font_size=30, color=C_FWD)).arrange(RIGHT, buff=0.1)
                      .next_to(cont[0], UP, buff=0.15).shift(1.0 * LEFT),
                      VGroup(zh('后向分支', 24, C_BWD), MathTex('C_2', font_size=30, color=C_BWD)).arrange(RIGHT, buff=0.1)
                      .next_to(cont[2], DOWN, buff=0.15).shift(1.0 * LEFT))
        with self.narrate('co4') as b:
            self.play(FadeIn(labs), run_time=0.8)
            plus = VGroup(zh('期望值：相对于明确的初始态', 26, C_LESS), zh('代价：两条时间分支同等对待', 26, C_HI)
                          ).arrange(DOWN, buff=0.25, aligned_edge=LEFT).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(plus[0], shift=0.2 * UP), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(plus[1], shift=0.2 * UP), run_time=0.8)
            b.wait_sentence(2)
            name = zh('凯尔迪什回路', 32, WHITE).next_to(cont, RIGHT, buff=0.3)
            self.play(Write(name), run_time=1.0)
        # ----- closed contour: evolution around the loop is the identity -> no denominator
        with self.narrate('co4b') as b:
            self.play(FadeOut(plus), FadeOut(name), run_time=0.5)
            rider = Dot(color=WHITE, radius=0.08)
            loop_path = VMobject().set_points_as_corners([cont[0].get_start(), cont[0].get_end()])
            loop_path.append_vectorized_mobject(cont[1].copy())
            loop_path.add_line_to(cont[2].get_end())
            uu = MathTex(r"U(t_0,t)\,U(t,t_0) = 1", font_size=40, color=C_LESS).move_to([0, -1.25, 0])
            self.play(MoveAlongPath(rider, loop_path), run_time=2.0)
            self.play(Write(uu), FadeOut(rider), run_time=1.0)
            b.wait_sentence(1)
            norm = MathTex(r"\big\langle T_C\, e^{-i\oint_C d\tau\, H'(\tau)}\big\rangle = 1", font_size=38).move_to([0, -2.1, 0])
            self.play(Write(norm), run_time=1.5)
            b.wait_sentence(2)
            eqden = MathTex(r"\frac{\cdots}{\langle\Phi_0|S(\infty,-\infty)|\Phi_0\rangle}", font_size=34, color=GREY_B)
            bub = VGroup(Circle(radius=0.22, color=C_FWD, stroke_width=3),
                         ParametricFunction(lambda t: np.array([-0.22 + 0.44 * t, 0.04 * np.sin(6 * PI * t), 0]),
                                            t_range=[0, 1], color=GREY_A, stroke_width=2))
            old = VGroup(en('equilibrium:', 24, GREY_B), eqden, bub).arrange(RIGHT, buff=0.3).move_to([0, -3.15, 0])
            cr = Cross(VGroup(eqden, bub), stroke_color=RED, stroke_width=4)
            gone = en('no denominator, no vacuum bubbles', 26, C_LESS).next_to(old, RIGHT, buff=0.4)
            self.play(FadeIn(old), run_time=0.8)
            self.play(Create(cr), run_time=0.6)
            if gone.get_right()[0] > 6.9:
                VGroup(old, cr, gone).shift(LEFT * (gone.get_right()[0] - 6.9))
            self.play(FadeIn(gone, shift=0.2 * LEFT), run_time=0.8)
        co4b_grp = VGroup(uu, norm, old, cr, gone)
        # ----- imaginary-time leg and t0 -> -infinity
        leg = Arrow([-5.0, -0.15, 0], [-5.0, -2.3, 0], buff=0, color=C_IM, stroke_width=4)
        legl = MathTex(r't_0 - i\beta', font_size=32, color=C_IM).next_to(leg, DOWN, buff=0.1)
        rho = MathTex(r'\rho_0 = \frac{e^{-\beta h}}{\mathrm{Tr}\,e^{-\beta h}}', font_size=36).move_to([-1.5, -1.9, 0])
        with self.narrate('co5') as b:
            self.play(FadeOut(co4b_grp), run_time=0.5)
            self.play(GrowArrow(leg), FadeIn(legl), Write(rho), run_time=1.8)
            b.wait_sentence(1)
            whole = VGroup(cont, t0, leg, legl)
            self.play(cont.animate.stretch(1.13, 0, about_point=[3.25, 0.3, 0]),
                      t0.animate.shift(1.0 * LEFT).set_opacity(0), leg.animate.shift(1.0 * LEFT).set_opacity(0.0),
                      legl.animate.shift(1.0 * LEFT).set_opacity(0.0), labs.animate.shift(0.6 * LEFT), run_time=2.0)
            minf = MathTex(r't_0\to-\infty', font_size=32).next_to(cont, UP, buff=0.15).align_to(cont, LEFT)
            self.play(ReplacementTransform(t0, minf), run_time=0.8)
            b.wait_sentence(2)
            lost = VGroup(zh('丢掉初始关联', 26, C_HI), zh('（稳态问题通常无妨）', 22, GREY_A)).arrange(DOWN, buff=0.1)
            lost.next_to(rho, RIGHT, buff=1.0)
            self.play(FadeIn(lost), run_time=0.8)
        self.clear()


class S04_Components(NScene):
    def construct(self):
        Gc = MathTex(r"G(1,1') = -i\,\langle T_C\,[\psi_H(1)\,\psi_H^\dagger(1')]\rangle", font_size=42).to_edge(UP, buff=0.4)
        with self.narrate('cm1') as b:
            self.play(Write(Gc), run_time=2.0)
        dy = MathTex(r'G = G_0 + \int_C G_0\,U\,G + \int_C\!\!\int_C G_0\,\Sigma\,G', font_size=40).next_to(Gc, DOWN, buff=0.4)
        # diagrammatic Dyson equation
        def dline(x0, x1, double=False, y=-0.6):
            if double:
                return VGroup(Line([x0, y + 0.05, 0], [x1, y + 0.05, 0]), Line([x0, y - 0.05, 0], [x1, y - 0.05, 0])).set_stroke(C_FWD, 3)
            return Line([x0, y, 0], [x1, y, 0], color=C_FWD, stroke_width=3)
        sig = Circle(radius=0.3, color=C_HI, fill_opacity=0.3).move_to([2.6, -0.6, 0])
        sigl = MathTex(r'\Sigma', font_size=30).move_to(sig)
        dd = VGroup(dline(-5.5, -3.8, True), MathTex('=', font_size=36).move_to([-3.3, -0.6, 0]), dline(-2.8, -1.1),
                    MathTex('+', font_size=36).move_to([-0.6, -0.6, 0]), dline(-0.1, 2.3), sig, sigl, dline(2.9, 4.6, True))
        same = zh('与平衡态相同的拓扑结构；积分沿回路进行', 26, C_LESS).next_to(dd, DOWN, buff=0.5)
        with self.narrate('cm2') as b:
            self.play(Write(dy), run_time=2.0)
            self.play(FadeIn(dd), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(same, shift=0.2 * UP), run_time=0.8)
        self.play(FadeOut(VGroup(dy, dd, same)), run_time=0.6)

        # four components
        cont = keldysh_contour(-6.0, -0.4, 0.4, 1.2)
        brl = VGroup(MathTex('C_1', font_size=30, color=C_FWD).next_to(cont[0], UP, buff=0.1),
                     MathTex('C_2', font_size=30, color=C_BWD).next_to(cont[2], DOWN, buff=0.1))
        p1 = VGroup(Dot(radius=0.11, color=WHITE), MathTex('1', font_size=28))
        p2 = VGroup(Dot(radius=0.11, color=C_HI), MathTex("1'", font_size=28, color=C_HI))
        top, bot = 1.0, -0.2

        def place(p, x, branch):
            y = top if branch == 1 else bot
            p[0].move_to([x, y, 0])
            p[1].next_to(p[0], UP if branch == 1 else DOWN, buff=0.1)
            return p
        names = [[r'G_c', r'G^<'], [r'G^>', r'G_{\tilde c}']]
        cells = VGroup()
        for i in range(2):
            for j in range(2):
                r = Square(side_length=1.3, stroke_color=GREY_C, stroke_width=2).move_to([2.6 + 1.3 * j, 0.95 - 1.3 * i, 0])
                cells.add(VGroup(r, MathTex(names[i][j], font_size=40).move_to(r)))
        rowl = VGroup(MathTex(r'1\in C_1', font_size=26).next_to(cells[0], LEFT, buff=0.15),
                      MathTex(r'1\in C_2', font_size=26).next_to(cells[2], LEFT, buff=0.15))
        coll = VGroup(MathTex(r"1'\in C_1", font_size=26, color=C_HI).next_to(cells[0], UP, buff=0.15),
                      MathTex(r"1'\in C_2", font_size=26, color=C_HI).next_to(cells[1], UP, buff=0.15))
        defs = VGroup(MathTex(r"G^>(1,1') = -i\langle\psi_H(1)\psi_H^\dagger(1')\rangle", font_size=32, color=C_GTR),
                      MathTex(r"G^<(1,1') = +i\langle\psi_H^\dagger(1')\psi_H(1)\rangle", font_size=32, color=C_LESS)
                      ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)
        with self.narrate('cm3') as b:
            self.play(Create(cont), FadeIn(brl), run_time=1.2)
            self.play(FadeIn(cells), FadeIn(rowl), FadeIn(coll), run_time=1.0)
            configs = [(1, 1, 0), (1, 2, 1), (2, 1, 2), (2, 2, 3)]
            place(p1, -4.6, 1)
            place(p2, -2.4, 1)
            self.play(FadeIn(p1), FadeIn(p2), run_time=0.5)
            per = max(0.6, (b.remaining() - 2.5) / 4)
            for b1, b2, k in configs:
                self.play(p1.animate.become(place(p1.copy(), -4.6, b1)), p2.animate.become(place(p2.copy(), -2.4, b2)),
                          cells[k][0].animate.set_fill(C_FWD, 0.3), run_time=per * 0.6)
                self.wait(per * 0.4)
                if k == 1:
                    cells[k][1].set_color(C_LESS)
                if k == 2:
                    cells[k][1].set_color(C_GTR)
            self.play(FadeIn(defs), run_time=1.0)
        self.play(FadeOut(VGroup(cont, brl, p1, p2, defs)), VGroup(cells, rowl, coll).animate.to_edge(LEFT, buff=1.4),
                  run_time=0.8)
        ident = MathTex(r'G_c + G_{\tilde c} = G^< + G^>', font_size=38).move_to([3.0, 1.0, 0])
        three = zh('只有三个线性独立', 24, C_HI).next_to(ident, DOWN, buff=0.15)
        ra = VGroup(MathTex(r"G^r = \theta(t_1-t_{1'})\,[G^> - G^<]", font_size=32, color=C_FWD),
                    MathTex(r"G^a = \theta(t_{1'}-t_1)\,[G^< - G^>]", font_size=32, color=C_BWD)
                    ).arrange(DOWN, buff=0.15, aligned_edge=LEFT).next_to(three, DOWN, buff=0.4)
        with self.narrate('cm4') as b:
            self.play(Write(ident), run_time=1.5)
            self.play(FadeIn(three), run_time=0.6)
            b.wait_sentence(1)
            self.play(FadeIn(ra, shift=0.2 * UP), run_time=1.2)
        self.play(FadeOut(VGroup(rowl, coll, three, ident)),
                  cells.animate.scale(0.75).to_edge(LEFT, buff=0.6).shift(0.2 * DOWN), ra.animate.to_edge(LEFT, buff=0.5).shift(2.0 * DOWN),
                  run_time=0.8)
        key = MathTex(r'G^r - G^a = G^> - G^<', font_size=44).next_to(Gc, DOWN, buff=0.5)
        # density-of-states pictogram
        ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.1, 1], x_length=5.2, y_length=2.6, tips=False,
                  axis_config=dict(include_ticks=False, stroke_color=GREY_B)).move_to([3.2, -1.2, 0])
        dos = lambda e: 0.9 * np.exp(-0.5 * e**2)
        full = ax.plot(dos, x_range=[-3, 3, 0.02], color=WHITE, stroke_width=3)
        occ = ax.get_area(ax.plot(dos, x_range=[-3, 0.4, 0.02]), x_range=[-3, 0.4], color=C_LESS, opacity=0.5)
        emp = ax.get_area(ax.plot(dos, x_range=[0.4, 3, 0.02]), x_range=[0.4, 3], color=C_GTR, opacity=0.5)
        mu = DashedLine(ax.c2p(0.4, 0), ax.c2p(0.4, 1.05), color=WHITE)
        lab = VGroup(MathTex(r'G^<', color=C_LESS, font_size=32).next_to(ax.c2p(-1.4, 0.45), UP),
                     MathTex(r'G^>', color=C_GTR, font_size=32).next_to(ax.c2p(1.6, 0.25), UP),
                     MathTex(r'A = i(G^r - G^a)', font_size=32).next_to(ax, UP, buff=0.05))
        words = VGroup(zh('占据态', 22, C_LESS).next_to(lab[0], UP, buff=0.05), zh('空态', 22, C_GTR).next_to(lab[1], UP, buff=0.05),
                       zh('谱函数 = 态密度', 22).next_to(lab[2], UP, buff=0.05))
        with self.narrate('cm5') as b:
            self.play(Write(key), run_time=1.5)
            b.wait_sentence(1)
            self.play(Create(ax), Create(full), Create(mu), run_time=1.0)
            self.play(FadeIn(occ), FadeIn(lab[0]), FadeIn(words[0]), run_time=1.0)
            self.play(FadeIn(emp), FadeIn(lab[1]), FadeIn(words[1]), run_time=1.0)
            self.play(FadeIn(lab[2]), FadeIn(words[2]), Indicate(full, color=WHITE), run_time=1.2)
        self.play(FadeOut(VGroup(cells, ra, key, ax, full, occ, emp, mu, lab, words)), run_time=0.7)

        # ----- spectrum (G^r) versus occupation (G^<)
        sax = Axes(x_range=[-3, 3, 1], y_range=[0, 1.1, 1], x_length=7.5, y_length=3.0, tips=False,
                   axis_config=dict(include_ticks=False, stroke_color=GREY_B)).move_to([-2.2, -1.3, 0])
        sxl = MathTex(r'\varepsilon', font_size=30).next_to(sax.x_axis, RIGHT, buff=0.1)
        dosf = lambda e: 0.95 * (0.75 * np.exp(-1.6 * (e + 1.1) ** 2) + np.exp(-1.6 * (e - 1.0) ** 2))
        feq = lambda e: fermi(e, 0.0, 0.12)
        fneq = lambda e: 0.5 * fermi(e, 1.3, 0.12) + 0.5 * fermi(e, -1.3, 0.12)
        mix = ValueTracker(0.0)

        def filled():
            m = mix.get_value()
            es = np.linspace(-3, 3, 300)
            ys = dosf(es) * ((1 - m) * feq(es) + m * fneq(es))
            pts = [sax.c2p(-3, 0)] + [sax.c2p(e, y) for e, y in zip(es, ys)] + [sax.c2p(3, 0)]
            return Polygon(*pts, stroke_width=0, fill_color=C_LESS, fill_opacity=0.55)
        fill = always_redraw(filled)
        spec = sax.plot(dosf, x_range=[-3, 3, 0.01], color=WHITE, stroke_width=3.5)
        r1 = VGroup(MathTex(r'G^r', font_size=38, color=C_FWD), en(r'$\rightarrow$ spectrum $A(\varepsilon)$: which states, how long they live', 26)
                    ).arrange(RIGHT, buff=0.25)
        r2 = VGroup(MathTex(r'G^<', font_size=38, color=C_LESS), en(r'$\rightarrow$ occupation $n(\varepsilon)$: how full they are', 26)
                    ).arrange(RIGHT, buff=0.25)
        rr = VGroup(r1, r2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(Gc, DOWN, buff=0.5)
        with self.narrate('cm6') as b:
            self.play(Create(sax), FadeIn(sxl), Create(spec), FadeIn(r1, shift=0.2 * RIGHT), run_time=1.5)
            b.wait_sentence(1)
            self.add(fill)
            self.play(FadeIn(fill), FadeIn(r2, shift=0.2 * RIGHT), run_time=1.2)
        fdt = VGroup(en('equilibrium (fluctuation--dissipation):', 24, GREY_A),
                     MathTex(r'G^<(\varepsilon) = i\,f(\varepsilon)\,A(\varepsilon)', font_size=36, color=C_LESS)).arrange(DOWN, buff=0.15)
        fdt.move_to([4.4, -0.5, 0])
        neq = VGroup(en('out of equilibrium:', 24, GREY_A),
                     MathTex(r'-iG^<(\varepsilon) = n(\varepsilon)', font_size=36, color=C_HI),
                     en('set by kinetics, not by $T$', 24, C_HI)).arrange(DOWN, buff=0.15).move_to([4.4, -2.2, 0])
        with self.narrate('cm7') as b:
            self.play(FadeIn(fdt), run_time=1.0)
            b.wait_sentence(1)
            self.play(mix.animate.set_value(1.0), FadeIn(neq), run_time=2.5)
            b.wait_sentence(2)
            self.play(Indicate(neq[1], color=C_HI), Indicate(spec, color=WHITE), run_time=1.2)
        fill.clear_updaters()
        self.clear()
