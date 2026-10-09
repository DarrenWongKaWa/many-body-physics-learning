import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def wavy(p, q, amp=0.06, n=7, color=GREY_A, width=2.5):
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    L = np.linalg.norm(d)
    u, v = d / L, np.array([-d[1], d[0], 0]) / L
    return ParametricFunction(lambda s: p + u * s * L + v * amp * np.sin(2 * np.pi * n * s), t_range=[0, 1],
                              color=color, stroke_width=width)


def fermion(p, q, color=C_FWD, width=3):
    line = Line(p, q, color=color, stroke_width=width)
    tip = Triangle(fill_color=color, fill_opacity=1, stroke_width=0).scale(0.07)
    d = line.get_unit_vector()
    tip.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(line.get_center())
    return VGroup(line, tip)


def diagram(kind):
    g = VGroup()
    if kind == 'fock':           # exchange: wavy arc on the line
        g.add(fermion([-1.1, 0, 0], [1.1, 0, 0]))
        g.add(ArcBetweenPoints([-0.5, 0, 0], [0.5, 0, 0], angle=-PI * 0.9).set_stroke(GREY_A, 2.5))
    elif kind == 'hartree':      # tadpole
        g.add(fermion([-1.1, 0, 0], [1.1, 0, 0]))
        g.add(wavy([0, 0, 0], [0, 0.55, 0], n=3))
        g.add(Circle(radius=0.25, color=C_FWD, stroke_width=3).move_to([0, 0.8, 0]))
    else:                        # disconnected: bare line + vacuum bubble
        g.add(fermion([-1.1, 0, 0], [1.1, 0, 0]))
        bub = VGroup(Circle(radius=0.32, color=C_FWD, stroke_width=3), wavy([-0.32, 0, 0], [0.32, 0, 0], n=3))
        g.add(bub.move_to([0, 0.75, 0]))
    return g


class S02_Equilibrium(NScene):
    def construct(self):
        G = MathTex(r"G(x,t;x',t') = -i\,\frac{\langle", r'\Psi_0', r"|\,T\{\psi_H(x,t)\,\psi_H^\dagger(x',t')\}\,|",
                    r'\Psi_0', r'\rangle}{\langle\Psi_0|\Psi_0\rangle}', font_size=42).to_edge(UP, buff=0.5)
        with self.narrate('eq1') as b:
            self.play(Write(G), run_time=2.5)
            exact = zh('精确基态', 26, C_HI).next_to(G[3], DOWN, buff=0.35)
            self.play(G[1].animate.set_color(C_HI), G[3].animate.set_color(C_HI), FadeIn(exact, shift=0.1 * UP),
                      run_time=1.0)
        with self.narrate('eq2') as b:
            q = Text('?', font_size=80, color=C_HI).next_to(exact, DOWN, buff=0.2)
            self.play(FadeIn(q, scale=1.5), run_time=0.8)
        self.play(FadeOut(q), FadeOut(exact), G.animate.scale(0.75).to_edge(UP, buff=0.25), run_time=0.7)

        # S-matrix and adiabatic switching
        S = MathTex(r"S(t,t') = T\exp\Big[-i\!\int_{t'}^{t}\! dt_1\,\hat V(t_1)\Big]", font_size=38)
        grp = MathTex(r"S(t,t') = S(t,t'')\,S(t'',t')", font_size=36, color=GREY_A)
        VGroup(S, grp).arrange(RIGHT, buff=0.9).next_to(G, DOWN, buff=0.45)
        ax = Axes(x_range=[-6, 6, 1], y_range=[0, 1.2, 1], x_length=11, y_length=1.6, tips=False,
                  axis_config=dict(include_ticks=False, stroke_color=GREY_B)).shift(0.6 * DOWN)
        lam = ax.plot(lambda t: np.exp(-0.55 * abs(t)), x_range=[-6, 6, 0.02], color=C_LESS, stroke_width=4)
        laml = MathTex(r'\lambda(t) = e^{-\eta|t|}', font_size=30, color=C_LESS).next_to(ax.c2p(1.6, 0.8), RIGHT)
        tl = VGroup(MathTex(r'-\infty', font_size=30).next_to(ax.c2p(-6, 0), DOWN),
                    MathTex(r'0', font_size=30).next_to(ax.c2p(0, 0), DOWN),
                    MathTex(r'+\infty', font_size=30).next_to(ax.c2p(6, 0), DOWN))
        phi0 = MathTex(r'|\Phi_0\rangle', font_size=36, color=C_FWD).next_to(ax.c2p(-6, 0), DOWN, buff=0.7)
        psi0 = MathTex(r'|\Psi_0\rangle = S(0,-\infty)\,|\Phi_0\rangle', font_size=36, color=C_HI).next_to(ax.c2p(0, 0), DOWN, buff=0.7)
        gml = zh('盖尔曼–洛定理', 24, GREY_A).next_to(psi0, DOWN, buff=0.15)
        with self.narrate('eq3') as b:
            self.play(Write(S), run_time=1.6)
            self.play(FadeIn(grp), run_time=0.8)
            b.wait_sentence(1)
            self.play(Create(ax), FadeIn(tl), run_time=0.8)
            self.play(Create(lam), FadeIn(laml), run_time=1.5)
            b.wait_sentence(2)
            self.play(FadeIn(phi0), run_time=0.6)
            mover = Dot(ax.c2p(-6, 0), color=C_FWD, radius=0.08)
            self.play(MoveAlongPath(mover, Line(ax.c2p(-6, 0), ax.c2p(0, 0))), run_time=1.5)
            self.play(TransformFromCopy(phi0, psi0), FadeIn(gml), run_time=1.2)
        with self.narrate('eq4') as b:
            self.play(MoveAlongPath(mover, Line(ax.c2p(0, 0), ax.c2p(6, 0))), run_time=2.0)
            back = MathTex(r'e^{iL}\,|\Phi_0\rangle', font_size=36, color=C_FWD).next_to(ax.c2p(6, 0), DOWN, buff=0.7)
            self.play(FadeIn(back, shift=0.2 * LEFT), Flash(mover, color=C_FWD), run_time=1.2)
            b.wait_sentence(2)
            bra = MathTex(r'\langle\Psi_0| = \langle\Phi_0|\,S(\infty,0)', font_size=36, color=C_HI)
            bra.next_to(psi0, RIGHT, buff=0.6).shift(0.0 * DOWN)
            bra.next_to(gml, DOWN, buff=0.2)
            self.play(Write(bra), run_time=1.5)
        self.play(FadeOut(VGroup(ax, lam, laml, tl, phi0, psi0, gml, back, bra, mover, S, grp)), run_time=0.7)

        G2 = MathTex(r'G = -i\,\frac{\langle\Phi_0|\,T\{S(\infty,-\infty)\,\hat\psi\,\hat\psi^\dagger\}\,|\Phi_0\rangle}'
                     r'{\langle\Phi_0|\,S(\infty,-\infty)\,|\Phi_0\rangle}', font_size=42).next_to(G, DOWN, buff=0.5)
        wick = zh('威克定理：两两收缩', 26, GREY_A)
        d1, d2, d3 = diagram('fock'), diagram('hartree'), diagram('disc')
        diags = VGroup(d1, d2, d3).arrange(RIGHT, buff=1.4).shift(1.2 * DOWN)
        conn = VGroup(zh('连通', 24, C_LESS).next_to(VGroup(d1, d2), DOWN, buff=0.4))
        cross = Cross(d3, stroke_color=RED, stroke_width=5)
        disc = zh('不连通：被分母抵消', 24, RED).next_to(d3, DOWN, buff=0.4)
        with self.narrate('eq5') as b:
            self.play(TransformMatchingShapes(G.copy(), G2), run_time=1.5)
            b.wait_sentence(1)
            wick.next_to(G2, DOWN, buff=0.4)
            self.play(FadeIn(wick), run_time=0.6)
            self.play(LaggedStart(*[Create(d) for d in diags], lag_ratio=0.3), run_time=2.0)
            self.play(FadeIn(conn), Create(cross), FadeIn(disc), run_time=1.2)
        self.clear()
