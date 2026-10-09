import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def glow(point, color, r=0.55, n=8, peak=0.85):
    g = VGroup()
    for i in range(n, 0, -1):
        rr = r * i / n
        g.add(Circle(radius=rr, stroke_width=0, fill_color=color, fill_opacity=peak / n * 1.6).move_to(point))
    return g


class S06_Berry(NScene):
    def construct(self):
        title = txt('Berry curvature in action', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- ber1: lambda -> k
        lat = VGroup(*[Dot([x, y, 0], radius=0.07, color=GREY_B) for x in np.arange(-6.2, -2.0, 0.7) for y in np.arange(-2.3, 1.9, 0.7)])
        lat_l = txt('crystal', 28, GREY_A).next_to(lat, UP, buff=0.2)
        maps = MathTex(r'\lambda\ \longrightarrow\ \mathbf k', font_size=46).move_to([-0.6, 0.0, 0])
        ax = kspace_axes(3.6).move_to([3.6, -0.3, 0])
        gxx, gyy, gxy, om = geometry(lambda kx, ky: unit(qwz_d(kx, ky, 1.2)), *grid(200))
        img = image_on_axes(signed_rgba(om, 0.6), ax, (-np.pi, np.pi), (-np.pi, np.pi))
        bx = frame_box(ax, (-np.pi, np.pi), (-np.pi, np.pi))
        bz_l = VGroup(txt('Berry curvature', 28, C_POS), MathTex(r'\Omega_n(\mathbf k)', font_size=32, color=C_POS)
                      ).arrange(RIGHT, buff=0.15).next_to(bx, UP, buff=0.55)
        with self.narrate('ber1') as b:
            self.play(Write(title), run_time=1.2)
            b.wait_sentence(1)
            self.play(LaggedStartMap(FadeIn, lat, lag_ratio=0.01), FadeIn(lat_l), run_time=1.2)
            self.play(Write(maps), run_time=1.0)
            self.play(Create(ax), FadeIn(bx), FadeIn(img), FadeIn(bz_l), run_time=1.5)

        # ---------------- ber2: wave packet, anomalous velocity
        eom1 = MathTex(r'\hbar\dot{\mathbf k}', '=', r'-e\mathbf E', font_size=42)
        eom2 = MathTex(r'\dot{\mathbf r}', '=', r'\frac{1}{\hbar}\frac{\partial\varepsilon_n}{\partial\mathbf k}', '-',
                       r'\dot{\mathbf k}\times\Omega_n(\mathbf k)', font_size=42)
        eom1[2].set_color(C_E)
        eqs = VGroup(eom1, eom2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([2.7, 1.3, 0])
        gv = txt('group velocity', 26, GREY_A).next_to(eom2[2], DOWN, buff=0.3)
        av = txt('anomalous velocity', 26, C_J).next_to(eom2[4], DOWN, buff=0.3)
        # real-space stage
        stage = RoundedRectangle(width=5.6, height=4.2, corner_radius=0.15, stroke_color=GREY_D, fill_color=C_PANEL,
                                 fill_opacity=0.8).move_to([-3.6, -0.6, 0])
        Ear = Arrow(stage.get_corner(UL) + 0.4 * DOWN + 2.0 * RIGHT, stage.get_corner(UL) + 0.4 * DOWN + 0.3 * RIGHT, buff=0,
                    color=C_E, stroke_width=5)
        El = MathTex(r'\mathbf E', font_size=34, color=C_E).next_to(Ear, RIGHT, buff=0.1)
        t = ValueTracker(0.0)
        start = stage.get_left() + 0.8 * RIGHT + 0.9 * DOWN

        def path(tt):
            return start + np.array([4.0 * tt, 1.9 * tt ** 1.0 * 0 + 1.8 * tt, 0])

        def packet():
            p = path(t.get_value())
            g = VGroup(*[Circle(radius=0.08 + 0.05 * i, stroke_width=0, fill_color=C_ELEC, fill_opacity=0.22).move_to(p)
                         for i in range(6)])
            g.add(Dot(p, radius=0.06, color=WHITE))
            return g
        wp = always_redraw(packet)
        trail = always_redraw(lambda: Line(start, path(max(t.get_value(), 1e-3)), color=C_ELEC, stroke_width=2, stroke_opacity=0.6))
        ghost = DashedLine(start, start + 4.0 * RIGHT, color=GREY_B, stroke_width=2)
        ghost_l = txt('without $\\Omega$', 22, GREY_B).next_to(ghost.get_end(), DOWN, buff=0.1)
        side = Arrow(start + 4.0 * RIGHT + 0.05 * UP, path(1.0) + 0.05 * DOWN, buff=0.05, color=C_J, stroke_width=4,
                     max_tip_length_to_length_ratio=0.25)
        with self.narrate('ber2') as b:
            self.play(FadeOut(VGroup(lat, lat_l, maps)), FadeOut(Group(ax, bx, img, bz_l)), run_time=0.9)
            self.play(FadeIn(stage), GrowArrow(Ear), FadeIn(El), run_time=0.8)
            self.add(trail, wp)
            self.play(FadeIn(wp), run_time=0.5)
            b.wait_sentence(1)
            self.play(Write(eom1), run_time=1.2)
            b.wait_sentence(2)
            self.play(Write(eom2), run_time=2.0)
            self.play(FadeIn(gv), run_time=0.6)
            self.play(FadeIn(av), eom2[4].animate.set_color(C_J), run_time=0.6)
            self.play(Create(ghost), FadeIn(ghost_l), t.animate.set_value(1.0), run_time=2.6, rate_func=linear)
            self.play(GrowArrow(side), run_time=0.6)

        # ---------------- ber3: intrinsic AHE, quantization
        ahe = MathTex(r'\sigma_{xy}', '=', r'\frac{e^2}{\hbar}\sum_n\int\frac{d^2k}{(2\pi)^2}\,f_n(\mathbf k)\,\Omega_n(\mathbf k)',
                      font_size=42).move_to([2.6, -1.4, 0])
        tags = txt('no magnetic field, no scattering', 28, GREY_A).next_to(ahe, DOWN, buff=0.3)
        qah = MathTex(r'\sigma_{xy}', '=', r'C\,\frac{e^2}{h}', font_size=54, color=YELLOW).move_to([2.6, -1.6, 0])
        qah_t = txt('filled Chern band: exactly quantized', 28, YELLOW).next_to(qah, DOWN, buff=0.25)
        with self.narrate('ber3') as b:
            self.play(FadeOut(VGroup(gv, av, ghost, ghost_l)), run_time=0.6)
            self.play(Write(ahe), run_time=2.0)
            self.play(FadeIn(tags), run_time=0.8)
            # many packets all drifting sideways
            many = VGroup(*[Dot(start + np.array([0.2 * i, -0.2 + 0.25 * (i % 3), 0]), radius=0.05, color=C_ELEC) for i in range(10)])
            self.play(FadeOut(wp), FadeOut(trail), FadeOut(side), FadeIn(many), run_time=0.6)
            self.play(*[d.animate.shift(np.array([1.6, 1.9, 0])) for d in many], run_time=2.0)
            jy = Arrow(stage.get_center() + 1.4 * DOWN + 1.8 * RIGHT, stage.get_center() + 1.4 * UP + 1.8 * RIGHT, buff=0,
                       color=C_J, stroke_width=6)
            jl = MathTex(r'J_y', font_size=34, color=C_J).next_to(jy, RIGHT, buff=0.1)
            self.play(GrowArrow(jy), FadeIn(jl), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeOut(tags), ReplacementTransform(ahe, qah), run_time=1.4)
            self.play(FadeIn(qah_t), run_time=0.8)

        # ---------------- ber4: experiments
        cards = VGroup(
            VGroup(txt('quantum anomalous Hall', 30, YELLOW), txt('Cr-doped (Bi,Sb)$_2$Te$_3$ (2013), MnBi$_2$Te$_4$', 26, GREY_A)),
            VGroup(txt('fractional quantum anomalous Hall', 30, YELLOW), txt('twisted MoTe$_2$, rhombohedral graphene (2023--24)', 26, GREY_A)),
        )
        for c in cards:
            c.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        cards.arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([2.6, 0.9, 0])
        with self.narrate('ber4') as b:
            self.play(FadeOut(VGroup(eom1, eom2)), run_time=0.6)
            self.play(FadeIn(cards[0], shift=0.2 * LEFT), run_time=1.0)
            self.wait(2.5)
            self.play(FadeIn(cards[1], shift=0.2 * LEFT), run_time=1.0)

        # ---------------- ber5: symmetry
        ax5 = kspace_axes(3.6).move_to([-3.7, -0.4, 0])
        bx5 = frame_box(ax5, (-np.pi, np.pi), (-np.pi, np.pi))
        ka, kb = ax5.c2p(1.3, 0.8), ax5.c2p(-1.3, -0.8)
        dk1, dk2 = Dot(ka, color=WHITE), Dot(kb, color=WHITE)
        lk1 = MathTex(r'\mathbf k', font_size=32).next_to(dk1, UR, buff=0.05)
        lk2 = MathTex(r'-\mathbf k', font_size=32).next_to(dk2, DL, buff=0.05)
        dl = DashedLine(ka, kb, color=GREY_B)
        trs = VGroup(txt('time reversal $\\mathcal T$:', 30), MathTex(r'\Omega(-\mathbf k) = -\,\Omega(\mathbf k)', font_size=38))
        inv = VGroup(txt('inversion $\\mathcal P$:', 30), MathTex(r'\Omega(-\mathbf k) = +\,\Omega(\mathbf k)', font_size=38))
        both = VGroup(txt('both:', 30, YELLOW), MathTex(r'\Omega(\mathbf k) = 0\ \ \text{everywhere}', font_size=38, color=YELLOW))
        for r in (trs, inv, both):
            r.arrange(RIGHT, buff=0.25)
        sym = VGroup(trs, inv, both).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([2.6, 0.0, 0])
        with self.narrate('ber5') as b:
            self.play(FadeOut(VGroup(stage, Ear, El, many, jy, jl, qah, qah_t, cards)), run_time=0.8)
            self.play(Create(ax5), FadeIn(bx5), run_time=0.8)
            b.wait_sentence(1)
            self.play(Create(dl), FadeIn(dk1), FadeIn(dk2), FadeIn(lk1), FadeIn(lk2), run_time=0.8)
            g1, g2 = glow(ka, C_POS, 0.5), glow(kb, C_NEG, 0.5)
            self.play(FadeIn(trs), FadeIn(g1), FadeIn(g2), run_time=1.0)
            g2b = glow(kb, C_POS, 0.5)
            self.play(FadeIn(inv), Transform(g2, g2b), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(both), FadeOut(g1), FadeOut(g2), run_time=1.0)

        # ---------------- ber6: break T or P
        hexr = 1.55
        hexc = np.array([-3.7, 0.05, 0])
        corners = [hexc + hexr * np.array([np.cos(PI / 6 + j * PI / 3), np.sin(PI / 6 + j * PI / 3), 0]) for j in range(6)]
        hexagon = Polygon(*corners, stroke_color=GREY_B, stroke_width=2)
        valleys = VGroup()
        for j, c in enumerate(corners):
            col = C_POS if j % 2 == 0 else C_NEG
            valleys.add(glow(c, col, 0.42))
        Kl = MathTex('K', font_size=30, color=C_POS).next_to(corners[0], RIGHT, buff=0.12)
        Kpl = MathTex("K'", font_size=30, color=C_NEG).next_to(corners[1], UP, buff=0.12)
        row1 = VGroup(txt('break $\\mathcal T$ (magnetism)', 30, C_POS), MathTex(r'\Rightarrow', font_size=36),
                      txt('anomalous Hall effect', 30)).arrange(RIGHT, buff=0.25)
        row2 = VGroup(txt('keep $\\mathcal T$, break $\\mathcal P$', 30, C_NEG), MathTex(r'\Rightarrow', font_size=36),
                      txt('$\\Omega$ locked to valley, spin, layer', 30)).arrange(RIGHT, buff=0.25)
        row3 = txt('valley Hall $\\cdot$ spin Hall $\\cdot$ layer Hall', 30, YELLOW)
        rows = VGroup(row1, row2, row3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([2.6, 0.4, 0])
        with self.narrate('ber6') as b:
            self.play(FadeOut(VGroup(ax5, bx5, dk1, dk2, lk1, lk2, dl)), sym.animate.scale(0.7).move_to([2.7, -2.55, 0]),
                      run_time=0.9)
            self.play(FadeIn(row1), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(hexagon), FadeIn(valleys), FadeIn(Kl), FadeIn(Kpl), FadeIn(row2), run_time=1.6)
            # valley Hall: the two valleys drift to opposite sides
            bar = RoundedRectangle(width=3.2, height=1.3, corner_radius=0.1, stroke_color=GREY_C).move_to([-3.7, -2.9, 0])
            ev = VGroup(*[Dot(bar.get_center() + np.array([-1.2 + 0.3 * i, 0, 0]), radius=0.06, color=C_POS if i % 2 else C_NEG)
                          for i in range(9)])
            self.play(FadeIn(bar), FadeIn(ev), FadeIn(row3), run_time=0.8)
            self.play(*[d.animate.shift(np.array([0.35, 0.45 if d.get_color() == ManimColor(C_POS) else -0.45, 0])) for d in ev],
                      run_time=1.5)

        # ---------------- ber7: Berry curvature dipole
        ax7 = kspace_axes(3.8, xr=(-1.6, 1.6), yr=(-1.6, 1.6)).move_to([-3.6, -0.3, 0])
        xs = np.linspace(-1.6, 1.6, 220)
        X, Y = np.meshgrid(xs, xs)
        omd = X * np.exp(-(X ** 2 + Y ** 2) / 0.35) / 0.35
        img7 = image_on_axes(signed_rgba(omd, 1.2), ax7, (-1.6, 1.6), (-1.6, 1.6))
        bx7 = frame_box(ax7, (-1.6, 1.6), (-1.6, 1.6))
        shift = ValueTracker(0.0)
        R0 = 0.75
        sea = always_redraw(lambda: Circle(radius=R0 * ax7.x_length / 3.2, stroke_color=WHITE, stroke_width=3, fill_color=WHITE,
                                           fill_opacity=0.12).move_to(ax7.c2p(shift.get_value(), 0)))
        sea_l = txt('Fermi sea', 24, GREY_A).next_to(bx7, DOWN, buff=0.15)

        def net(s):
            mask = (X - s) ** 2 + Y ** 2 < R0 ** 2
            return (omd * mask).sum() * (xs[1] - xs[0]) ** 2

        nlab = MathTex(r'\int_{\rm occ}\Omega\,d^2k =', font_size=36).move_to([1.2, -1.5, 0])
        nval = always_redraw(lambda: DecimalNumber(net(shift.get_value()), num_decimal_places=2, font_size=36, color=C_J,
                                                   include_sign=True).next_to(nlab, RIGHT, buff=0.15))
        E7 = Arrow(ax7.c2p(-1.4, 1.35), ax7.c2p(-0.4, 1.35), buff=0, color=C_E, stroke_width=5)
        E7l = MathTex(r'\delta\mathbf k \propto \tau\mathbf E', font_size=30, color=C_E).next_to(E7, RIGHT, buff=0.1)
        bcd = MathTex(r'J_y', r'\ \propto\ ', r'\tau\, D_{\rm BC}\, E_x^2', font_size=44).move_to([2.6, 1.6, 0])
        bcd[0].set_color(C_J)
        dbc = MathTex(r'D_{\rm BC} = \int f\,\partial_{k_x}\Omega', font_size=36).next_to(bcd, DOWN, buff=0.35)
        wte2 = txt('first seen in few-layer WTe$_2$', 28, YELLOW).move_to([2.6, -2.6, 0])
        with self.narrate('ber7') as b:
            self.play(FadeOut(VGroup(hexagon, valleys, Kl, Kpl, bar, ev, rows, sym)), run_time=0.8)
            self.play(Create(ax7), FadeIn(bx7), FadeIn(img7), run_time=1.0)
            self.add(sea)
            self.play(FadeIn(sea), FadeIn(sea_l), FadeIn(nlab), FadeIn(nval), run_time=1.0)
            b.wait_sentence(1)
            self.play(GrowArrow(E7), FadeIn(E7l), run_time=0.8)
            self.play(shift.animate.set_value(0.35), run_time=2.5)
            self.play(Write(bcd), run_time=1.5)
            self.play(FadeIn(dbc), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(wte2, shift=0.2 * UP), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
