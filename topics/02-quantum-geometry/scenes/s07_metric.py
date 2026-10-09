import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S07_Metric(NScene):
    def construct(self):
        title = txt('How the quantum metric moves electrons', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- met1: field mixes in the other band
        ax = Axes(x_range=[-np.pi, np.pi, np.pi], y_range=[-2.4, 2.4, 1], x_length=4.8, y_length=4.2, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-3.6, -0.5, 0])
        eb = lambda k: np.sqrt(0.5 + 1.2 * (1 - np.cos(k)))
        up = ax.plot(eb, x_range=[-np.pi, np.pi], color=C_B, stroke_width=4)
        dn = ax.plot(lambda k: -eb(k), x_range=[-np.pi, np.pi], color=C_A, stroke_width=4)
        upl = MathTex(r'm', font_size=32, color=C_B).next_to(up.get_end(), RIGHT, buff=0.1)
        dnl = MathTex(r'n', font_size=32, color=C_A).next_to(dn.get_end(), RIGHT, buff=0.1)
        kxl = MathTex('k', font_size=30, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.1)
        k0 = 0.8
        st = Dot(ax.c2p(k0, -eb(k0)), radius=0.1, color=WHITE)
        virt = CurvedArrow(ax.c2p(k0 + 0.05, -eb(k0) + 0.15), ax.c2p(k0 + 0.05, eb(k0) - 0.15), angle=-PI / 3, color=C_G,
                           stroke_width=4)
        ghost = Dot(ax.c2p(k0, eb(k0)), radius=0.1, color=C_G).set_opacity(0.5)
        Ear = Arrow(ax.c2p(-2.8, 2.15), ax.c2p(-1.3, 2.15), buff=0, color=C_E, stroke_width=5)
        El = MathTex(r'\mathbf E', font_size=32, color=C_E).next_to(Ear, RIGHT, buff=0.1)
        mix = MathTex(r'|\tilde u_n\rangle', '=', r'|u_n\rangle', '+', r'\sum_{m\neq n}|u_m\rangle\,\frac{\langle u_m|\,e\mathbf E\cdot\hat{\mathbf r}\,|u_n\rangle}{\varepsilon_n-\varepsilon_m}',
                      font_size=38).move_to([2.6, 1.3, 0])
        mix[4].set_color(C_G)
        with self.narrate('met1') as b:
            self.play(Write(title), run_time=1.4)
            self.play(Create(ax), Create(up), Create(dn), FadeIn(upl), FadeIn(dnl), FadeIn(kxl), run_time=1.6)
            b.wait_sentence(1)
            self.play(FadeIn(st, scale=2), run_time=0.6)
            b.wait_sentence(2)
            self.play(GrowArrow(Ear), FadeIn(El), run_time=0.6)
            self.play(Create(virt), FadeIn(ghost), Write(mix), run_time=2.0)

        # ---------------- met2: positional shift inside the unit cell
        cell = RoundedRectangle(width=5.0, height=2.4, corner_radius=0.15, stroke_color=GREY_C, fill_color=C_PANEL,
                                fill_opacity=0.9).move_to([-3.4, -1.3, 0])
        cell_l = txt('one unit cell', 24, GREY_T).next_to(cell, DOWN, buff=0.12)
        pa, pb = cell.get_center() + 1.3 * LEFT, cell.get_center() + 1.3 * RIGHT
        w = ValueTracker(0.0)          # extra weight on orbital beta

        def clouds():
            wa, wb = 0.75 - w.get_value(), 0.25 + w.get_value()
            g = VGroup(Circle(radius=0.15 + 0.75 * wa, stroke_width=0, fill_color=C_A, fill_opacity=0.45).move_to(pa),
                       Circle(radius=0.15 + 0.75 * wb, stroke_width=0, fill_color=C_B, fill_opacity=0.45).move_to(pb))
            cx = pa * wa + pb * wb
            g.add(Line(cx + 0.55 * UP, cx + 0.55 * DOWN, color=WHITE, stroke_width=4))
            return g
        cl = always_redraw(clouds)
        lab_a = MathTex(r'\alpha', font_size=30, color=C_A).next_to(pa, UP, buff=0.75)
        lab_b = MathTex(r'\beta', font_size=30, color=C_B).next_to(pb, UP, buff=0.75)
        cpos0 = pa * 0.75 + pb * 0.25
        ref = DashedLine(cpos0 + 0.75 * UP, cpos0 + 0.75 * DOWN, color=GREY_B, stroke_width=2)
        shift_ar = Arrow(cpos0 + 0.85 * DOWN, cpos0 + 0.85 * DOWN + 0.78 * RIGHT, buff=0, color=C_G, stroke_width=4,
                         max_tip_length_to_length_ratio=0.3)
        shift_l = MathTex(r'\delta\mathbf r', font_size=30, color=C_G).next_to(shift_ar, DOWN, buff=0.05)
        bcp = MathTex(r'a^{E}_{a}', '=', r'-e\,', r'\mathcal G_{ab}', r'\,E_b', font_size=46).move_to([2.6, -0.4, 0])
        bcp[0].set_color(C_G); bcp[3].set_color(YELLOW)
        bcp_t1 = txt('field-induced Berry connection', 28, C_G).next_to(bcp, UP, buff=0.3)
        bcp_t2 = txt('Berry connection polarizability', 28, YELLOW).next_to(bcp, DOWN, buff=0.3)
        with self.narrate('met2') as b:
            self.play(Group(ax, up, dn, upl, dnl, kxl, st, virt, ghost, Ear, El).animate.scale(0.6).move_to([-4.1, 1.35, 0]),
                      mix.animate.scale(0.8).move_to([2.6, 1.9, 0]), run_time=1.0)
            self.play(FadeIn(cell), FadeIn(cell_l), FadeIn(cl), FadeIn(lab_a), FadeIn(lab_b), run_time=1.0)
            self.add(ref)
            self.play(w.animate.set_value(0.25), run_time=1.6)
            self.play(GrowArrow(shift_ar), FadeIn(shift_l), run_time=0.6)
            b.wait_sentence(1)
            self.play(FadeIn(bcp_t1), Write(bcp), run_time=2.0)
            self.play(FadeIn(bcp_t2), run_time=0.8)

        # ---------------- met3: two-band result
        two = MathTex(r'\mathcal G_{ab}', '=', r'-\,\frac{g_{ab}(\mathbf k)}{h(\mathbf k)}', font_size=50).move_to([2.6, -0.4, 0])
        two[0].set_color(YELLOW); two[2].set_color(C_G)
        gap_t = txt('two bands: $2h(\\mathbf k)$ = band gap', 28, GREY_A).next_to(two, DOWN, buff=0.35)
        big = VGroup(txt('large $g$', 30, C_G), txt('small gap', 30, C_B)).arrange(RIGHT, buff=0.3)
        bigr = VGroup(big, MathTex(r'\Rightarrow\ \text{large shift}', font_size=36)).arrange(RIGHT, buff=0.3).next_to(gap_t, DOWN, buff=0.4)
        with self.narrate('met3') as b:
            self.play(FadeOut(bcp_t1), FadeOut(bcp_t2), ReplacementTransform(bcp, two), run_time=1.4)
            self.play(FadeIn(gap_t), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(bigr), run_time=1.0)
            self.play(w.animate.set_value(0.42), run_time=1.5)

        # ---------------- met4: tiny compared with Drude
        old = Group(ax, up, dn, upl, dnl, kxl, st, virt, ghost, Ear, El, mix, cell, cell_l, cl, lab_a, lab_b, ref, shift_ar,
                    shift_l, two, gap_t, bigr)
        base = np.array([-2.5, -2.3, 0])
        bar_d = Rectangle(width=1.3, height=4.0, stroke_width=0, fill_color=GREY_B, fill_opacity=0.85).move_to(base + 2.0 * UP)
        bar_g = Rectangle(width=1.3, height=0.25, stroke_width=0, fill_color=C_G, fill_opacity=0.95).move_to(base + 2.2 * RIGHT + 0.125 * UP)
        floor = Line(base + 1.2 * LEFT, base + 3.4 * RIGHT, color=GREY_B)
        bl_d = txt('Drude', 28).next_to(bar_d, DOWN, buff=0.15)
        bl_g = txt('quantum metric', 28, C_G).next_to(bar_g, DOWN, buff=0.15)
        sch = txt('(schematic)', 22, GREY_D).next_to(floor, DOWN, buff=0.6)
        dr = VGroup(txt('electrons accelerate until they scatter', 28, GREY_A),
                    MathTex(r'\sigma_{\rm Drude}\ \propto\ \tau', font_size=40)).arrange(DOWN, buff=0.2).move_to([3.4, 1.0, 0])
        sup = txt('$\\Rightarrow$ suppress the Drude part', 32, YELLOW).move_to([3.4, -0.6, 0])
        with self.narrate('met4') as b:
            self.play(FadeOut(old), run_time=0.8)
            b.wait_sentence(1)
            self.play(Create(floor), GrowFromEdge(bar_d, DOWN), FadeIn(bl_d), run_time=1.5)
            self.play(GrowFromEdge(bar_g, DOWN), FadeIn(bl_g), FadeIn(sch), run_time=1.0)
            self.play(FadeIn(dr), run_time=1.2)
            b.wait_sentence(2)
            self.play(FadeIn(sup, shift=0.2 * UP), run_time=1.0)

        # ---------------- met5: route 1, flat bands
        fax = Axes(x_range=[-np.pi, np.pi, np.pi], y_range=[-1.6, 1.6, 1], x_length=4.2, y_length=2.6, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([-3.5, -0.6, 0])
        tt = ValueTracker(1.0)
        fb = always_redraw(lambda: fax.plot(lambda k: -tt.get_value() * np.cos(k), x_range=[-np.pi, np.pi], color=C_G, stroke_width=5))
        r1 = txt('route 1: flat band', 34, bold=True).next_to(fax, UP, buff=0.4)
        r1b = MathTex(r'v = \frac{\partial\varepsilon}{\partial k} \to 0', font_size=38).next_to(fax, DOWN, buff=0.35)
        with self.narrate('met5') as b:
            self.play(FadeOut(VGroup(bar_d, bar_g, floor, bl_d, bl_g, sch, dr)), sup.animate.to_edge(UP, buff=1.25), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(r1), Create(fax), Create(fb), run_time=1.0)
            self.add(fb)
            self.play(tt.animate.set_value(0.03), FadeIn(r1b), run_time=2.4)

        # ---------------- met6: route 2, higher order + tau scaling
        r2 = txt('route 2: nonlinear response', 34, bold=True).move_to([3.3, 2.0, 0])
        lax = Axes(x_range=[0, 3, 1], y_range=[0, 4, 1], x_length=3.6, y_length=3.0, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_ticks=False)).move_to([2.9, -0.7, 0])
        lxl = MathTex(r'\log\tau', font_size=30, color=GREY_B).next_to(lax.x_axis, RIGHT, buff=0.1)
        lyl = MathTex(r'\log\sigma^{(2)}', font_size=30, color=GREY_B).next_to(lax.y_axis, UP, buff=0.1)
        l2 = lax.plot(lambda x: 0.3 + 1.2 * x, x_range=[0, 3], color=GREY_B, stroke_width=4)
        l1 = lax.plot(lambda x: 0.9 + 0.6 * x, x_range=[0, 3], color=C_POS, stroke_width=4)
        l0 = lax.plot(lambda x: 1.6 + 0 * x, x_range=[0, 3], color=C_G, stroke_width=5)
        t2 = MathTex(r'\tau^2', font_size=32, color=GREY_B).next_to(l2.get_end(), RIGHT, buff=0.1)
        t1 = MathTex(r'\tau^1', font_size=32, color=C_POS).next_to(l1.get_end(), RIGHT, buff=0.1)
        t0 = MathTex(r'\tau^0', font_size=32, color=C_G).next_to(l0.get_end(), RIGHT, buff=0.1)
        legend = VGroup(txt('nonlinear Drude', 26, GREY_B), txt('Berry curvature dipole', 26, C_POS),
                        txt('quantum metric dipole (intrinsic)', 26, C_G)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        legend.next_to(lax, DOWN, buff=0.35)
        with self.narrate('met6') as b:
            self.play(FadeIn(r2), Create(lax), FadeIn(lxl), FadeIn(lyl), run_time=1.2)
            self.play(Create(l2), FadeIn(t2), FadeIn(legend[0]), run_time=1.0)
            self.play(Create(l1), FadeIn(t1), FadeIn(legend[1]), run_time=1.0)
            self.play(Create(l0), FadeIn(t0), FadeIn(legend[2]), run_time=1.0)
            b.wait_sentence(1)
            self.play(Indicate(t2, scale_factor=1.4), run_time=1.0)
            self.play(Indicate(t1, scale_factor=1.4, color=C_POS), run_time=1.0)
            self.play(Indicate(VGroup(l0, t0), scale_factor=1.15, color=C_G), run_time=1.4)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
