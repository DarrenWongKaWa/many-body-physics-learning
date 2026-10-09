import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def d1(k):
    """1D two-band chain with a band inversion between k = 0 (alpha) and k = pi (beta)."""
    return np.array([0.8 * np.sin(k), 0.0 * k, 1 - 1.6 * (1 - np.cos(k))])


def e1(k):
    return np.linalg.norm(d1(k), axis=0)


def n1(k):
    d = d1(k)
    return d / np.linalg.norm(d, axis=0)


def orb_color(nz):
    return interpolate_color(ManimColor(C_B), ManimColor(C_A), (nz + 1) / 2)


def band_curve(ax, sign=1, n=240, width=5):
    ks = np.linspace(-np.pi, np.pi, n + 1)
    g = VGroup()
    for a, b in zip(ks[:-1], ks[1:]):
        km = 0.5 * (a + b)
        col = orb_color(sign * n1(km)[2])
        g.add(Line(ax.c2p(a, sign * e1(a)), ax.c2p(b, sign * e1(b)), stroke_color=col, stroke_width=width))
    return g


class S01_Intro(NScene):
    def construct(self):
        ax = Axes(x_range=[-np.pi, np.pi, np.pi], y_range=[-2.6, 2.6, 1], x_length=5.6, y_length=4.6, tips=False,
                  axis_config=dict(stroke_color=GREY_B, stroke_width=1.5, include_ticks=False)).shift(0.3 * DOWN)
        kl = MathTex('k', font_size=36, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.35)
        El = MathTex('E', font_size=36, color=GREY_B).next_to(ax.y_axis, UP, buff=0.15)
        ticks = VGroup(*[MathTex(s, font_size=26, color=GREY_B).next_to(ax.c2p(x, 0), DOWN, buff=0.15)
                         for x, s in [(-np.pi, r'-\pi'), (np.pi, r'\pi')]])
        cb, vb = band_curve(ax, 1), band_curve(ax, -1)

        # ---- intro1: states labelled by k and E -> band structure
        with self.narrate('intro1') as b:
            self.play(Create(ax), FadeIn(kl), FadeIn(El), FadeIn(ticks), run_time=1.5)
            ks = np.linspace(-np.pi, np.pi, 15)
            pts = VGroup(*[Dot(ax.c2p(k, s * e1(k)), radius=0.06, color=WHITE) for s in (1, -1) for k in ks])
            self.play(LaggedStartMap(FadeIn, pts, lag_ratio=0.04, scale=0.5), run_time=2.2)
            b.wait_sentence(1)
            self.play(Create(cb), Create(vb), run_time=2.5)
            self.play(FadeOut(pts), run_time=0.8)

        # ---- intro2: each state is a wavefunction -> Bloch sphere
        plot = VGroup(ax, kl, El, ticks, cb, vb)
        sph = Sphere2D(radius=1.75, n_merid=3).move_to([3.5, -0.2, 0])
        poles = sph.pole_labels()
        kt = ValueTracker(-np.pi)
        with self.narrate('intro2') as b:
            self.play(plot.animate.shift(2.9 * LEFT), run_time=1.2)
            self.play(FadeIn(sph), run_time=1.0)
            dot = always_redraw(lambda: Dot(ax.c2p(kt.get_value(), e1(kt.get_value())), radius=0.09,
                                            color=WHITE).set_stroke(BLACK, 2))
            arrow = always_redraw(lambda: sph.arrow(n1(kt.get_value()), color=orb_color(n1(kt.get_value())[2])))
            trace = always_redraw(lambda: sph.curve([n1(k) for k in np.linspace(-np.pi, kt.get_value(), 80)],
                                                    color=WHITE, width=2.5, back_opacity=0.3))
            self.add(trace)
            self.play(FadeIn(dot), GrowArrow(arrow), run_time=0.8)
            b.wait_sentence(1)
            self.play(kt.animate.set_value(np.pi), run_time=b.until_sentence(2) - 0.1, rate_func=smooth)
            self.play(FadeIn(poles), run_time=0.8)
            sup = MathTex(r'|u_k\rangle', '=', r'C_\alpha(k)', r'|\alpha\rangle', '+', r'C_\beta(k)', r'|\beta\rangle',
                          font_size=36).next_to(sph, UP, buff=0.45)
            sup[3].set_color(C_A)
            sup[6].set_color(C_B)
            self.play(Write(sup), run_time=1.3)
            self.play(kt.animate.set_value(0.0), run_time=2.5)

        # ---- intro3: how fast does it change, how does it twist?
        with self.narrate('intro3') as b:
            k1, k2 = 0.95, 1.35
            d_a = Dot(ax.c2p(k1, e1(k1)), radius=0.08, color=C_G)
            d_b = Dot(ax.c2p(k2, e1(k2)), radius=0.08, color=C_G)
            s_a, s_b = sph.dot(n1(k1), C_G, 0.08), sph.dot(n1(k2), C_G, 0.08)
            arc = sph.curve(slerp_path(n1(k1), n1(k2)), color=C_G, width=6)
            self.play(kt.animate.set_value(k1), run_time=1.0)
            self.play(FadeIn(d_a), FadeIn(s_a), run_time=0.4)
            self.play(kt.animate.set_value(k2), run_time=1.0)
            self.play(FadeIn(d_b), FadeIn(s_b), Create(arc), run_time=0.8)
            dist = MathTex(r'ds', font_size=34, color=C_G).next_to(arc, LEFT, buff=0.12)
            self.play(FadeIn(dist), run_time=0.5)
            # a small loop of states sweeping an area (twisting)
            c0 = bloch_vec(0.8, 1.15)
            e_a = np.cross(c0, [0, 0, 1]); e_a /= np.linalg.norm(e_a)
            e_b = np.cross(c0, e_a)
            loop_pts = [(c0 + 0.32 * (np.cos(t) * e_a + np.sin(t) * e_b)) for t in np.linspace(0, TAU, 60)]
            loop_pts = [q / np.linalg.norm(q) for q in loop_pts]
            loop = sph.curve(loop_pts, color=C_POS, width=4)
            patch = Polygon(*[sph.p(q) for q in loop_pts[:-1]], stroke_width=0, fill_color=C_POS, fill_opacity=0.35)
            self.play(Create(loop), FadeIn(patch), run_time=1.2)
            b.wait_sentence(2)
            title = txt('Quantum geometry', 52, bold=True).to_edge(UP, buff=0.35)
            self.play(Write(title), run_time=1.2)

        # ---- intro4: the quantum geometric tensor
        old = VGroup(plot, sph, poles, sup, d_a, d_b, s_a, s_b, arc, dist, loop, patch)
        qgt = MathTex(r'G_{ij}(\mathbf k)', '=', r'g_{ij}(\mathbf k)', '-', r'\frac{i}{2}', r'\Omega_{ij}(\mathbf k)',
                      font_size=64).shift(0.9 * UP)
        qgt[2].set_color(C_G)
        qgt[5].set_color(C_POS)
        name = txt('quantum geometric tensor', 34, GREY_T).next_to(qgt, UP, buff=0.35)
        with self.narrate('intro4') as b:
            self.play(FadeOut(old), FadeOut(dot), FadeOut(arrow), FadeOut(trace), title.animate.scale(0.75).to_edge(UP, buff=0.25),
                      run_time=1.0)
            self.play(Write(qgt), FadeIn(name), run_time=1.6)
            b.wait_sentence(1)
            br1 = Brace(qgt[2], DOWN, color=C_G)
            lab1 = VGroup(txt('real part:', 30, GREY_T), txt('quantum metric', 34, C_G),
                          txt('distance between states', 26, GREY_T)).arrange(DOWN, buff=0.12).next_to(br1, DOWN, buff=0.15)
            self.play(GrowFromCenter(br1), FadeIn(lab1, shift=0.2 * DOWN), run_time=1.0)
            b.wait_sentence(2)
            br2 = Brace(qgt[4:], DOWN, color=C_POS)
            lab2 = VGroup(txt('imaginary part:', 30, GREY_T), txt('Berry curvature', 34, C_POS),
                          txt('twisting of the phase', 26, GREY_T)).arrange(DOWN, buff=0.12).next_to(br2, DOWN, buff=0.15)
            lab2.shift(0.6 * RIGHT)
            lab1.shift(0.6 * LEFT)
            self.play(GrowFromCenter(br2), FadeIn(lab2, shift=0.2 * DOWN), run_time=1.0)

        # ---- intro5: famous vs neglected
        bc_list = VGroup(*[txt(s, 26) for s in ['anomalous Hall effect', 'quantum Hall effect', 'topology, Chern number']]
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(lab2, DOWN, buff=0.4)
        qm_list = VGroup(*[txt(s, 26) for s in ['nonlinear transport', 'flat-band superconductivity', 'nonlinear optics']]
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.14).next_to(lab1, DOWN, buff=0.4)
        with self.narrate('intro5') as b:
            self.play(LaggedStartMap(FadeIn, bc_list, shift=0.15 * RIGHT, lag_ratio=0.35), run_time=2.0)
            b.wait_sentence(1)
            tag = txt('largely ignored... until recently', 24, GREY_T).next_to(lab1, DOWN, buff=0.2)
            self.play(FadeIn(tag), run_time=0.8)
            self.wait(1.5)
            self.play(tag.animate.next_to(qm_list, DOWN, buff=0.25).set_opacity(0),
                      LaggedStartMap(FadeIn, qm_list, shift=0.15 * RIGHT, lag_ratio=0.45), run_time=3.0)
            self.play(Indicate(qgt[2], color=C_G, scale_factor=1.15), run_time=1.2)

        # ---- intro6: the review
        with self.narrate('intro6') as b:
            self.play(FadeOut(VGroup(qgt, name, br1, br2, lab1, lab2, bc_list, qm_list, title, tag)), run_time=0.9)
            t1 = txt('Quantum geometry phenomena\\\\in condensed matter systems', 50, bold=True)
            t2 = txt('Anyuan Gao, Naoto Nagaosa, Ni Ni, Su-Yang Xu', 32, GREY_A)
            t3 = txt('Reviews of Modern Physics \\textbf{98}, 035005 (2026)', 28, GREY_T)
            card = VGroup(t1, t2, t3).arrange(DOWN, buff=0.45)
            self.play(Write(t1), run_time=2.0)
            self.play(FadeIn(t2, shift=0.2 * UP), FadeIn(t3, shift=0.2 * UP), run_time=1.2)
            b.wait_sentence(1)
        self.play(FadeOut(card), run_time=0.8)
