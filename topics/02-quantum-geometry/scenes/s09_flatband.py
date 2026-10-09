import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def pair(p, color=C_J):
    a, b = Dot(p + 0.13 * LEFT, radius=0.07, color=color), Dot(p + 0.13 * RIGHT, radius=0.07, color=color)
    link = Line(a.get_center(), b.get_center(), color=color, stroke_width=2)
    return VGroup(link, a, b)


def tri_lattice(a, angle, R, color, center=ORIGIN, radius=0.028):
    g = VGroup()
    a1 = a * np.array([1, 0, 0])
    a2 = a * np.array([0.5, np.sqrt(3) / 2, 0])
    rot = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    n = int(R / a) + 3
    for i in range(-2 * n, 2 * n):
        for j in range(-2 * n, 2 * n):
            p = rot @ (i * a1 + j * a2)
            if np.linalg.norm(p) < R:
                g.add(Dot(center + p, radius=radius, color=color))
    return g


class S09_FlatBand(NScene):
    def construct(self):
        title = txt('Superconductivity in a flat band', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- fb1: flat band + pairs
        ax = Axes(x_range=[-np.pi, np.pi, np.pi], y_range=[-1.5, 1.5, 1], x_length=4.6, y_length=3.0, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-3.4, -0.2, 0])
        kxl = MathTex('k', font_size=30, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        eyl = MathTex(r'\varepsilon', font_size=30, color=GREY_B).next_to(ax.y_axis, UP, buff=0.1)
        tw = ValueTracker(1.0)
        band = always_redraw(lambda: ax.plot(lambda k: -tw.get_value() * np.cos(k), x_range=[-np.pi, np.pi], color=C_G, stroke_width=5))
        pairs = VGroup(*[pair(ax.c2p(x, 0.0) + 0.0 * UP) for x in (-2.0, 0.0, 2.0)])
        flat_l = txt('no dispersion', 28, C_G).next_to(ax, DOWN, buff=0.3)
        paradox = txt('a paradox?', 40, YELLOW).move_to([3.0, 0.0, 0])
        with self.narrate('fb1') as b:
            self.play(Write(title), run_time=1.3)
            self.play(Create(ax), FadeIn(kxl), FadeIn(eyl), Create(band), run_time=1.2)
            self.add(band)
            b.wait_sentence(1)
            self.play(tw.animate.set_value(0.0), FadeIn(flat_l), run_time=2.0)
            self.play(LaggedStartMap(FadeIn, pairs, lag_ratio=0.3, scale=0.5), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(paradox, scale=1.2), run_time=1.0)

        # ---------------- fb2: Ds ~ ns/m* -> 0
        ds = MathTex(r'D_s', r'\ \propto\ ', r'\frac{n_s}{m^*}', font_size=56).move_to([2.8, 1.0, 0])
        ds_t = txt('superfluid stiffness', 30, GREY_A).next_to(ds, UP, buff=0.3)
        inf = MathTex(r'm^*\to\infty\ \Rightarrow\ D_s\to 0', font_size=44, color=C_POS).next_to(ds, DOWN, buff=0.5)
        no_sc = txt('no supercurrent?', 32, C_POS).next_to(inf, DOWN, buff=0.3)
        with self.narrate('fb2') as b:
            self.play(FadeOut(paradox), run_time=0.5)
            self.play(FadeIn(ds_t), Write(ds), run_time=1.6)
            # a supercurrent: pairs sliding
            self.play(*[p.animate.shift(0.6 * RIGHT) for p in pairs], run_time=1.2, rate_func=there_and_back)
            b.wait_sentence(1)
            self.play(Indicate(ds[2], color=YELLOW), run_time=1.2)
            b.wait_sentence(2)
            self.play(Write(inf), run_time=1.5)
            self.play(FadeIn(no_sc), run_time=0.8)

        # ---------------- fb3: geometric contribution
        gl = MathTex(r'\Delta(\mathbf x) = \Delta_0\, e^{i\mathbf q\cdot\mathbf x}', font_size=38)
        gl2 = MathTex(r'|\langle u_{\mathbf k+\mathbf q/2}|u_{\mathbf k-\mathbf q/2}\rangle|^2', '=', '1', '-',
                      r'\sum_{ab} g_{ab}(\mathbf k)\, q_a q_b', font_size=36)
        gl2[4].set_color(C_G)
        rho = MathTex(r'\rho_s', '=', r'\rho_s^{\rm kinetic}', '+', r'\rho_s^{\rm geometric}', font_size=50)
        rho[4].set_color(C_G)
        ptm = MathTex(r'\rho_s^{\rm geometric}\ \propto\ \Delta\int_{\rm BZ} g(\mathbf k)\,d^2k', font_size=38, color=C_G)
        stack = VGroup(gl, gl2, rho, ptm).arrange(DOWN, buff=0.4).move_to([1.3, -0.4, 0])
        brk = Brace(rho[2], DOWN, color=GREY_B)
        brk_t = txt('band dispersion', 24, GREY_A).next_to(brk, DOWN, buff=0.08)
        with self.narrate('fb3') as b:
            self.play(FadeOut(VGroup(ds, ds_t, inf, no_sc)), Group(ax, kxl, eyl, band, pairs, flat_l).animate.scale(0.7).to_corner(UL, buff=0.6).shift(0.9 * DOWN),
                      run_time=1.0)
            b.wait_sentence(1)
            stack.shift(1.3 * RIGHT)
            self.play(Write(gl), run_time=1.4)
            self.play(Write(gl2), run_time=2.2)
            b.wait_sentence(2)
            self.play(Indicate(gl2[4], color=C_G), run_time=1.2)
            b.wait_sentence(3)
            self.play(Write(rho), run_time=1.6)
            self.play(FadeIn(ptm), run_time=1.0)

        # ---------------- fb4: real-space picture
        def chain(y, width, label, col):
            xs = np.arange(-2.4, 2.41, 1.2)
            curves = VGroup()
            for x0 in xs:
                f = lambda x, x0=x0: 0.75 * np.exp(-((x - x0) ** 2) / (2 * width ** 2))
                pts = [np.array([x, y + f(x), 0]) for x in np.linspace(max(x0 - 1.6, -3.6), min(x0 + 1.6, 3.6), 120)]
                c = VMobject(stroke_color=col, stroke_width=3).set_points_smoothly(pts)
                c.set_fill(col, opacity=0.18)
                curves.add(c)
            base = Line([-3.6, y, 0], [3.6, y, 0], color=GREY_D, stroke_width=1.5)
            sites = VGroup(*[Dot([x, y, 0], radius=0.05, color=GREY_B) for x in xs])
            lab = txt(label, 28, col).next_to(base, LEFT, buff=0.3)
            return VGroup(base, curves, sites, lab)
        c1 = chain(1.0, 0.18, 'trivial $g$', GREY_B).shift(0.6 * RIGHT)
        c2 = chain(-1.4, 0.55, 'nontrivial $g$', C_G).shift(0.6 * RIGHT)
        p1 = pair(np.array([0.6 - 1.2, 1.2, 0]), C_J)
        p2 = pair(np.array([0.6 - 1.2, -1.2, 0]), C_J)
        stuck = txt('pairs stuck', 26, C_POS).next_to(c1, RIGHT, buff=0.2)
        hop = txt('pairs can hop', 26, C_J).next_to(c2, RIGHT, buff=0.2)
        bound = MathTex(r'\text{spread} \ \ge \int_{\rm BZ}\frac{d^2k}{2\pi}\,\mathrm{tr}\,g', r'\ \ge\ ', r'|C|', font_size=38)
        bound[2].set_color(C_POS)
        bound.to_edge(DOWN, buff=0.35)
        topo = txt('topology $\\Rightarrow$ minimum stiffness', 30, YELLOW).next_to(bound, UP, buff=0.2)
        with self.narrate('fb4') as b:
            self.play(FadeOut(VGroup(gl, gl2, rho, ptm)), FadeOut(Group(ax, kxl, eyl, band, pairs, flat_l)), run_time=0.9)
            b.wait_sentence(1)
            self.play(FadeIn(c1), FadeIn(p1), run_time=1.2)
            self.play(p1.animate.shift(0.12 * RIGHT), run_time=0.4, rate_func=wiggle)
            self.play(FadeIn(stuck), run_time=0.6)
            b.wait_sentence(2)
            self.play(FadeIn(c2), FadeIn(p2), run_time=1.2)
            self.play(p2.animate.shift(1.2 * RIGHT), run_time=0.9)
            self.play(p2.animate.shift(1.2 * RIGHT), FadeIn(hop), run_time=0.9)
            b.wait_sentence(3)
            self.play(Write(bound), run_time=1.8)
            b.wait_sentence(4)
            self.play(FadeIn(topo, shift=0.15 * UP), run_time=0.9)

        # ---------------- fb5: twisted bilayer graphene
        moire = VGroup(tri_lattice(0.24, 0.0, 2.3, GREY_B), tri_lattice(0.24, np.radians(6.0), 2.3, C_B)).move_to([-3.6, -0.3, 0])
        mo_t = txt('twisted bilayer graphene', 30).next_to(moire, UP, buff=0.25)
        mo_t2 = txt('(twist exaggerated)', 22, GREY_D).next_to(moire, DOWN, buff=0.15)
        v_t = VGroup(MathTex(r'v \sim 10^3\ \mathrm{m/s}', font_size=40),
                     txt('$\\approx$ 1/1000 of graphene', 28, GREY_A)).arrange(DOWN, buff=0.15).move_to([2.8, 2.0, 0])
        base = np.array([1.3, -2.2, 0])
        floor = Line(base + 0.4 * LEFT, base + 3.6 * RIGHT, color=GREY_B)
        b_conv = Rectangle(width=1.0, height=0.55, stroke_width=0, fill_color=GREY_B, fill_opacity=0.9).move_to(base + 0.7 * RIGHT + 0.275 * UP)
        b_meas = Rectangle(width=1.0, height=2.4, stroke_width=0, fill_color=C_G, fill_opacity=0.95).move_to(base + 2.4 * RIGHT + 1.2 * UP)
        l_conv = txt('conventional', 24).next_to(b_conv, DOWN, buff=0.12)
        l_meas = txt('measured', 24, C_G).next_to(b_meas, DOWN, buff=0.12)
        dsl = MathTex('D_s', font_size=34).next_to(floor, LEFT, buff=0.2).shift(1.0 * UP)
        sch = txt('(schematic)', 20, GREY_D).next_to(floor, DOWN, buff=0.5).shift(1.2 * RIGHT)
        refs = txt('Tian \\emph{et al.} (2023); Tanaka \\emph{et al.}, Banerjee \\emph{et al.} (2025)', 22, GREY_T).to_edge(DOWN, buff=0.25)
        refs.shift(1.6 * RIGHT)
        open_q = txt('quantitative theory: still open', 28, YELLOW).move_to([2.9, 0.75, 0])
        with self.narrate('fb5') as b:
            self.play(FadeOut(VGroup(c1, c2, p1, p2, stuck, hop, bound, topo)), run_time=0.8)
            self.play(FadeIn(moire), FadeIn(mo_t), FadeIn(mo_t2), run_time=1.6)
            b.wait_sentence(1)
            self.play(FadeIn(v_t), run_time=1.2)
            b.wait_sentence(2)
            self.play(Create(floor), FadeIn(dsl), GrowFromEdge(b_conv, DOWN), FadeIn(l_conv), run_time=1.2)
            self.play(GrowFromEdge(b_meas, DOWN), FadeIn(l_meas), FadeIn(sch), FadeIn(refs), run_time=1.5)
            b.wait_sentence(3)
            self.play(FadeIn(open_q, shift=0.2 * UP), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
