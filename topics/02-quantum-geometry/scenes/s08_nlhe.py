import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def ring(center, r, weight, cmap_color, n=72, width=9, base=C_PANEL):
    """Fermi-surface ring whose colour intensity follows weight(theta) in [0, 1]."""
    g = VGroup()
    c0 = ManimColor(BG)
    for i in range(n):
        a0, a1 = TAU * i / n, TAU * (i + 1) / n
        w = float(np.clip(weight(0.5 * (a0 + a1)), 0, 1))
        col = interpolate_color(ManimColor('#2a2f3a'), ManimColor(cmap_color), w)
        g.add(Arc(radius=r, start_angle=a0, angle=a1 - a0 + 0.01, stroke_color=col, stroke_width=width).move_arc_center_to(center))
    return g


def kbox(center, w=3.2, h=2.2):
    b = Rectangle(width=w, height=h, stroke_color=GREY_C, stroke_width=1.5).move_to(center)
    kx = MathTex('k_x', font_size=26, color=GREY_B).next_to(b, DOWN, buff=0.08)
    ky = MathTex('k_y', font_size=26, color=GREY_B).next_to(b, LEFT, buff=0.08)
    return VGroup(b, kx, ky)


def afm_slab(center, n_layers=2, width=4.4, depth=0.5, h=1.6, n_spins=5, flip=False):
    c = np.asarray(center, float)
    front = Rectangle(width=width, height=h, stroke_color=GREY_C, fill_color='#20263a', fill_opacity=1).move_to(c)
    top = Polygon(front.get_corner(UL), front.get_corner(UR), front.get_corner(UR) + depth * np.array([0.6, 0.5, 0]),
                  front.get_corner(UL) + depth * np.array([0.6, 0.5, 0]), stroke_color=GREY_C, fill_color='#2b3350', fill_opacity=1)
    side = Polygon(front.get_corner(UR), front.get_corner(DR), front.get_corner(DR) + depth * np.array([0.6, 0.5, 0]),
                   front.get_corner(UR) + depth * np.array([0.6, 0.5, 0]), stroke_color=GREY_C, fill_color='#171c2b', fill_opacity=1)
    spins = VGroup()
    for j in range(n_layers):
        y = c[1] + (j - (n_layers - 1) / 2) * (h / n_layers)
        s = (1 if j % 2 == 0 else -1) * (-1 if flip else 1)
        for i in range(n_spins):
            x = c[0] + (i - (n_spins - 1) / 2) * (width / n_spins)
            spins.add(Arrow([x, y - s * 0.28, 0], [x, y + s * 0.28, 0], buff=0, color='#C86BFA', stroke_width=5,
                            max_tip_length_to_length_ratio=0.35))
    return VGroup(side, top, front, spins)


class S08_NLHE(NScene):
    def construct(self):
        title = txt('The intrinsic nonlinear Hall effect', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- nl1: quantum metric dipole
        kc = np.array([-3.4, -0.4, 0])
        kb = kbox(kc, 5.0, 3.0)
        gring = ring(kc, 1.05, lambda a: 0.55 + 0.45 * np.cos(a), C_G)
        dip = Arrow(kc + 0.55 * LEFT, kc + 0.55 * RIGHT, buff=0, color=WHITE, stroke_width=5)
        gl = VGroup(txt('quantum metric', 26, C_G), MathTex('g', font_size=30, color=C_G)).arrange(RIGHT, buff=0.12)
        gl.next_to(kb[0], UP, buff=0.15)
        more = txt('larger', 24, C_G).next_to(kc + 1.05 * RIGHT, RIGHT, buff=0.2)
        less = txt('smaller', 24, GREY_B).next_to(kc + 1.05 * LEFT, LEFT, buff=0.2)
        dqm = MathTex(r'\sigma_{yxx}\ \propto\ D^{\rm QM}', font_size=44).move_to([2.8, 1.2, 0])
        dqm2 = MathTex(r'D^{\rm QM} \sim \sum_{\mathbf k}\big(v_y\,g_{xx} - v_x\,g_{yx}\big)\,\delta(\varepsilon_{\mathbf k}-\varepsilon_F)',
                       font_size=36).next_to(dqm, DOWN, buff=0.4)
        dqt = txt('quantum metric dipole', 30, C_G).next_to(dqm, UP, buff=0.3)
        with self.narrate('nl1') as b:
            self.play(Write(title), run_time=1.4)
            b.wait_sentence(1)
            self.play(FadeIn(kb), FadeIn(gl), Create(gring), run_time=1.6)
            self.play(FadeIn(more), FadeIn(less), GrowArrow(dip), run_time=1.0)
            self.play(FadeIn(dqt), Write(dqm), run_time=1.4)
            self.play(FadeIn(dqm2), run_time=1.2)

        # ---------------- nl2: symmetry table (cf. Fig. 21 of the review)
        hdr = VGroup(*[MathTex(s, font_size=40) for s in [r'\mathcal T', r'\mathcal P', r'\mathcal{PT}']])
        r_qm = VGroup(MathTex(r'D^{\rm QM}', font_size=40, color=C_G), *[txt(s, 32, c) for s, c in
                      [('odd', C_POS), ('odd', C_POS), ('even', C_J)]])
        r_bc = VGroup(MathTex(r'D^{\rm BC}', font_size=40, color=C_POS), *[txt(s, 32, c) for s, c in
                      [('even', C_J), ('odd', C_POS), ('odd', C_POS)]])
        xs = [-1.0, 1.2, 2.9, 4.6]
        y0 = 1.3
        for j, m in enumerate(hdr):
            m.move_to([xs[j + 1], y0, 0])
        for row, y in ((r_qm, y0 - 0.9), (r_bc, y0 - 1.8)):
            for j, m in enumerate(row):
                m.move_to([xs[j], y, 0])
        hline = Line([-1.9, y0 - 0.45, 0], [5.4, y0 - 0.45, 0], color=GREY_D)
        table = VGroup(hdr, r_qm, r_bc, hline)
        concl = VGroup(txt('$D^{\\rm QM}$: break $\\mathcal T$ and $\\mathcal P$, keep $\\mathcal{PT}$', 30, C_G),
                       txt('$\\Rightarrow$ $\\mathcal{PT}$-symmetric antiferromagnets', 32, YELLOW)).arrange(DOWN, buff=0.2)
        concl.move_to([1.8, -2.4, 0])
        with self.narrate('nl2') as b:
            self.play(FadeOut(VGroup(dqm, dqm2, dqt, more, less)), VGroup(kb, gl, gring, dip).animate.scale(0.75).move_to([-5.0, 0.4, 0]),
                      run_time=0.9)
            self.play(FadeIn(hdr), Create(hline), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(r_qm[0]), run_time=0.5)
            for m in r_qm[1:]:
                self.play(FadeIn(m, shift=0.1 * DOWN), run_time=0.7)
            b.wait_sentence(2)
            self.play(FadeIn(r_bc[0]), run_time=0.5)
            self.play(FadeIn(r_bc[1], shift=0.1 * DOWN), run_time=0.7)
            self.play(FadeIn(r_bc[2:], shift=0.1 * DOWN), run_time=0.7)
            b.wait_sentence(3)
            self.play(FadeIn(concl, shift=0.2 * UP), run_time=1.2)

        # ---------------- nl3: PT-symmetric AFM, no Berry curvature (cf. Fig. 22)
        slab = afm_slab([-3.2, 0.9, 0], n_layers=2)
        slab_l = txt('$\\mathcal{PT}$-symmetric antiferromagnet', 28, GREY_A).next_to(slab, UP, buff=0.35)
        kc2 = np.array([3.3, 0.9, 0])
        kb2 = kbox(kc2, 3.6, 2.6)
        gring2 = ring(kc2, 0.85, lambda a: 0.55 + 0.45 * np.cos(a), C_G)
        dip2 = Arrow(kc2 + 0.45 * LEFT, kc2 + 0.45 * RIGHT, buff=0, color=WHITE, stroke_width=5)
        zero = VGroup(MathTex(r'\Omega(\mathbf k) = 0', font_size=38, color=C_POS),
                      MathTex(r'\sigma_{xy} = 0', font_size=38)).arrange(RIGHT, buff=0.8).next_to(kb2, DOWN, buff=0.35)
        zero.move_to([0.0, -1.3, 0])
        with self.narrate('nl3') as b:
            self.play(FadeOut(VGroup(table, concl, kb, gl, gring, dip)), run_time=0.8)
            self.play(FadeIn(slab, shift=0.2 * UP), FadeIn(slab_l), FadeIn(kb2), Create(gring2), GrowArrow(dip2), run_time=1.4)
            b.wait_sentence(1)
            self.play(Write(zero), run_time=1.4)

        # ---------------- nl4: field-induced Berry curvature -> Hall current ~ E^2
        Ex = Arrow(slab[2].get_left() + 0.3 * RIGHT + 0.05 * DOWN, slab[2].get_right() + 0.3 * LEFT + 0.05 * DOWN, buff=0,
                   color=C_E, stroke_width=6).shift(0.0 * UP)
        Exl = MathTex(r'E_x', font_size=34, color=C_E).next_to(slab, DOWN, buff=0.15)
        oring = ring(kc2, 0.85, lambda a: 1.0, C_POS)
        oE = MathTex(r'\Omega_E', r'\ \propto\ ', r'D^{\rm QM}E_x', font_size=40).move_to([0.0, -1.3, 0])
        oE[0].set_color(C_POS)
        sE = MathTex(r'\sigma_{xy}(E)', r'\ \propto\ ', r'D^{\rm QM}E_x', font_size=40)
        jy = MathTex(r'J_y', '=', r'\sigma_{xy}(E)\,E_x', r'\ \propto\ ', r'D^{\rm QM}E_x^2', font_size=46)
        jy[0].set_color(C_J); jy[4].set_color(YELLOW)
        VGroup(oE, sE, jy).arrange(DOWN, buff=0.35).move_to([0.0, -1.9, 0])
        Jar = Arrow(slab[2].get_right() + 0.75 * RIGHT + 0.8 * DOWN, slab[2].get_right() + 0.75 * RIGHT + 0.8 * UP, buff=0,
                    color=C_J, stroke_width=7)
        Jl = MathTex(r'J_y', font_size=34, color=C_J).next_to(Jar, RIGHT, buff=0.1)
        with self.narrate('nl4') as b:
            self.play(FadeOut(zero), GrowArrow(Ex), FadeIn(Exl), run_time=1.0)
            self.play(FadeOut(gring2), FadeIn(oring), dip2.animate.set_opacity(0.3), run_time=1.6)
            self.play(Write(oE), run_time=1.4)
            b.wait_sentence(1)
            self.play(Write(sE), run_time=1.4)
            b.wait_sentence(2)
            self.play(Write(jy), GrowArrow(Jar), FadeIn(Jl), run_time=1.8)
            self.play(Circumscribe(jy[4], color=YELLOW), run_time=1.2)

        # ---------------- nl5: the material: BP / even-layer MnBi2Te4 / BP
        layers = VGroup()
        y = -1.2
        for kind in ['bp', 'bp', 'm', 'm', 'm', 'm', 'm', 'm', 'bp', 'bp']:
            h = 0.22 if kind == 'bp' else 0.3
            col = '#3f6f5a' if kind == 'bp' else '#3a4a8a'
            layers.add(Rectangle(width=4.2, height=h, stroke_color=GREY_C, stroke_width=1, fill_color=col, fill_opacity=1)
                       .move_to([-3.2, y + h / 2, 0]))
            y += h + 0.04
        mspins = VGroup()
        for j, lay in enumerate(layers[2:8]):
            s = 1 if j % 2 == 0 else -1
            for i in range(6):
                x = -3.2 + (i - 2.5) * 0.65
                mspins.add(Arrow([x, lay.get_center()[1] - s * 0.12, 0], [x, lay.get_center()[1] + s * 0.12, 0], buff=0,
                                 color='#C86BFA', stroke_width=4, max_tip_length_to_length_ratio=0.5))
        dev = VGroup(layers, mspins)
        lab_bp = txt('black phosphorus', 26, '#7fd1a8').next_to(layers[9], RIGHT, buff=0.3)
        lab_bp2 = txt('black phosphorus', 26, '#7fd1a8').next_to(layers[0], RIGHT, buff=0.3)
        lab_m = VGroup(txt('6-layer MnBi$_2$Te$_4$', 28, '#9fb2ff'), txt('$\\mathcal{PT}$-symmetric AFM,', 24, GREY_A),
                       txt('topological bands', 24, GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        lab_m.next_to(layers[2:8], RIGHT, buff=0.3)
        c3 = VGroup(RegularPolygon(3, color=GREY_B, stroke_width=3).scale(0.45),
                    Arc(radius=0.75, start_angle=0.3, angle=PI * 1.2, color=GREY_B, stroke_width=3).add_tip(tip_length=0.15))
        c3l = MathTex(r'C_{3z}', font_size=34).next_to(c3, DOWN, buff=0.15)
        c3g = VGroup(c3, c3l).move_to([4.6, 1.3, 0])
        c3x = Cross(c3, stroke_color=C_POS, stroke_width=5)
        c3t = txt('$C_{3z}$ forces $\\sigma_{yxx}=\\sigma_{xyx}$: no Hall', 24, GREY_A).next_to(c3g, DOWN, buff=0.25)
        refs = txt('A. Gao \\emph{et al.}, Science (2023); N. Wang \\emph{et al.}, Nature (2023)', 24, GREY_T).to_edge(DOWN, buff=0.35)
        with self.narrate('nl5') as b:
            self.play(FadeOut(VGroup(slab, slab_l, kb2, oring, dip2, Ex, Exl, Jar, Jl)), VGroup(oE, sE, jy).animate.scale(0.7).move_to([3.6, 2.0, 0]).set_opacity(0),
                      run_time=0.9)
            self.play(LaggedStartMap(FadeIn, layers[2:8], shift=0.1 * DOWN, lag_ratio=0.1), FadeIn(mspins), run_time=1.6)
            self.play(FadeIn(lab_m), FadeIn(refs), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(layers[:2], shift=0.2 * UP), FadeIn(layers[8:], shift=0.2 * DOWN), FadeIn(lab_bp), FadeIn(lab_bp2),
                      run_time=1.2)
            self.play(FadeIn(c3g), run_time=0.8)
            self.play(Create(c3x), FadeIn(c3t), run_time=1.0)

        # ---------------- nl6: the evidence
        items = [
            'flips sign with the AFM order: $\\mathcal T$-odd (not a Berry curvature dipole)',
            'vanishes above the N\\\'eel temperature $T_N$',
            'independent of the scattering time $\\tau$',
            'antisymmetric: $\\sigma_{xyx}\\approx-\\sigma_{yxx}$',
            'doping dependence follows the calculated $D^{\\rm QM}$',
        ]
        checks = VGroup()
        for s in items:
            mark = MathTex(r'\checkmark', font_size=40, color=C_J)
            checks.add(VGroup(mark, txt(s, 28)).arrange(RIGHT, buff=0.25))
        checks.arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([1.2, -1.0, 0])
        # mini plot for the sign flip (schematic)
        pax = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=2.4, y_length=1.9, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-5.0, 1.85, 0])
        pp = pax.plot(lambda x: 0.85 * x ** 2, x_range=[-1, 1], color='#C86BFA', stroke_width=4)
        pm = pax.plot(lambda x: -0.85 * x ** 2, x_range=[-1, 1], color=C_B, stroke_width=4)
        pxl = MathTex(r'I^{\omega}', font_size=26, color=GREY_B).next_to(pax.x_axis, RIGHT, buff=0.05)
        pyl = MathTex(r'V^{2\omega}_{\perp}', font_size=26, color=GREY_B).next_to(pax.y_axis, UP, buff=0.05)
        ps = VGroup(MathTex(r'\Uparrow\Downarrow', font_size=26, color='#C86BFA').next_to(pp.get_end(), RIGHT, buff=0.05),
                    MathTex(r'\Downarrow\Uparrow', font_size=26, color=C_B).next_to(pm.get_end(), RIGHT, buff=0.05))
        psch = txt('(schematic)', 20, GREY_D).next_to(pax, DOWN, buff=0.1)
        with self.narrate('nl6') as b:
            self.play(FadeOut(VGroup(dev, lab_bp, lab_bp2, lab_m, c3g, c3x, c3t)), run_time=0.8)
            b.wait_sentence(1)
            self.play(Create(pax), FadeIn(pxl), FadeIn(pyl), run_time=0.6)
            self.play(Create(pp), Create(pm), FadeIn(ps), FadeIn(psch), run_time=1.4)
            self.play(FadeIn(checks[0], shift=0.2 * RIGHT), run_time=0.9)
            for i in range(1, 5):
                b.wait_sentence(i + 1)
                self.play(FadeIn(checks[i], shift=0.2 * RIGHT), run_time=0.8)

        # ---------------- nl7: applications and third order
        ant = VGroup(Line(ORIGIN, 0.9 * UP, color=GREY_A, stroke_width=4),
                     Line(0.9 * UP, 0.9 * UP + 0.35 * LEFT + 0.35 * UP, color=GREY_A, stroke_width=4),
                     Line(0.9 * UP, 0.9 * UP + 0.35 * RIGHT + 0.35 * UP, color=GREY_A, stroke_width=4))
        waves = VGroup(*[Arc(radius=0.3 + 0.22 * i, start_angle=-PI / 4, angle=PI / 2, color=C_E, stroke_width=3)
                         for i in range(3)]).next_to(ant, RIGHT, buff=0.1).shift(0.3 * UP)
        devb = RoundedRectangle(width=1.6, height=0.9, corner_radius=0.12, stroke_color=GREY_B, fill_color=C_PANEL,
                                fill_opacity=1)
        devt = MathTex(r'\sigma_{yxx}', font_size=30, color=C_G).move_to(devb)
        dcv = MathTex(r'V_{\rm DC}', font_size=36, color=C_J)
        rect = VGroup(VGroup(ant, waves), Arrow(LEFT, RIGHT, color=GREY_B, stroke_width=3).scale(0.5), VGroup(devb, devt),
                      Arrow(LEFT, RIGHT, color=GREY_B, stroke_width=3).scale(0.5), dcv).arrange(RIGHT, buff=0.3)
        rect.move_to([-2.2, 1.7, 0])
        rect_t = txt('microwave $\\to$ DC rectification', 28, GREY_A).next_to(rect, DOWN, buff=0.25)
        rt = VGroup(txt('Mn$_3$Sn / Pt films:', 28, '#C86BFA'), txt('up to room temperature', 28)).arrange(RIGHT, buff=0.2)
        rt.next_to(rect_t, DOWN, buff=0.4)
        third = MathTex(r'J_y\ \propto\ ', r'(\text{quantum metric quadrupole})', r'\,E^3', font_size=40).move_to([0, -1.7, 0])
        third[1].set_color(C_G)
        third_t = txt('third-order Hall effect: no symmetry breaking needed (MoTe$_2$, 2021)', 28, GREY_A).next_to(third, DOWN, buff=0.3)
        with self.narrate('nl7') as b:
            self.play(FadeOut(VGroup(checks, pax, pp, pm, pxl, pyl, ps, psch, refs)), run_time=0.8)
            self.play(FadeIn(rect), FadeIn(rect_t), run_time=1.4)
            self.play(LaggedStartMap(Create, waves, lag_ratio=0.3), run_time=1.2)
            self.play(FadeIn(rt, shift=0.2 * LEFT), run_time=1.0)
            b.wait_sentence(1)
            self.play(Write(third), run_time=1.8)
            self.play(FadeIn(third_t), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
