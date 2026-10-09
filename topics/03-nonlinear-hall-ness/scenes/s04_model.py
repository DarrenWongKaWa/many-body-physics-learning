import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

CAP = 1.2
BZ = (-np.pi, np.pi)


class S04_Model(N3DScene):
    def construct(self):
        H = MathTex(r'H(\mathbf k) = (\cos k_x - D_x)\,\sigma_x + \sin k_y\,\sigma_y + (\cos k_y - D_y)\,\sigma_z',
                    font_size=40).to_edge(UP, buff=0.35)
        par = MathTex(r'D_x = 0.5,\quad D_y = 1', font_size=34, color=GREY_A).next_to(H, DOWN, buff=0.2)
        self.add_fixed_in_frame_mobjects(H, par)
        self.remove(H, par)
        with self.narrate('mod1') as b:
            self.play(Write(H), run_time=2.5)

        ax = ThreeDAxes(x_range=[-np.pi, np.pi, np.pi / 2], y_range=[-1.5, 1.5, 0.5], z_range=[-1.3, 1.3, 0.5],
                        x_length=7.0, y_length=3.4, z_length=3.0, tips=False,
                        axis_config=dict(include_ticks=False, stroke_color=GREY_B, stroke_width=1.5))
        ax.shift(0.6 * DOWN)

        # radial parametrisation of the region eps(k) <= CAP, so the rim is smooth;
        # the radial grid hits the two nodes exactly (theta = 0, pi)
        def rim(th):
            lo, hi = 0.0, 3.2
            for _ in range(40):
                mid = 0.5 * (lo + hi)
                if eps(mid * np.cos(th), mid * np.sin(th)) <= CAP:
                    lo = mid
                else:
                    hi = mid
            return lo
        r0 = rim(0.0)
        s_node = NODE / r0
        NS, u_node = 36, 14 / 36

        def warp(u):
            return u / u_node * s_node if u <= u_node else s_node + (u - u_node) / (1 - u_node) * (1 - s_node)

        def band(sign):
            def f(u, v):
                r = warp(u) * rim(v)
                kx, ky = r * np.cos(v), r * np.sin(v)
                return ax.c2p(kx, ky, sign * eps(kx, ky))
            s = Surface(f, u_range=[0, 1], v_range=[0, 2 * np.pi], resolution=(NS, 72),
                        checkerboard_colors=False, stroke_width=0.3, stroke_color=BG, fill_opacity=0.9)
            if sign > 0:
                s.set_fill_by_value(axes=ax, colorscale=[('#FF8A3D', 0.0), ('#E8452C', CAP)], axis=2)
            else:
                s.set_fill_by_value(axes=ax, colorscale=[('#3D7BFF', -CAP), ('#7FB2FF', 0.0)], axis=2)
            return s

        up, dn = band(+1), band(-1)
        lab_k = VGroup(MathTex('k_x', font_size=34).move_to(ax.c2p(np.pi + 0.4, 0, 0)),
                       MathTex('k_y', font_size=34).move_to(ax.c2p(0, 1.85, 0)),
                       MathTex(r'\varepsilon', font_size=34).move_to(ax.c2p(0, 0, 1.6)))
        for m in lab_k:
            m.rotate(PI / 2, axis=RIGHT)
        self.set_camera_orientation(phi=68 * DEGREES, theta=-62 * DEGREES, zoom=1.0)
        with self.narrate('mod2') as b:
            self.play(FadeIn(par), Create(ax), run_time=1.2)
            self.play(FadeIn(dn), FadeIn(up), FadeIn(lab_k), run_time=2.0)
            self.begin_ambient_camera_rotation(rate=0.06)
            b.wait_until(b.dur * 0.55)
            nl = VGroup()
            for sgn in (-1, 1):
                d = Dot3D(ax.c2p(sgn * NODE, 0, 0), radius=0.07, color=WHITE)
                nl.add(d)
            self.play(FadeIn(nl, scale=2), run_time=1.0)
            self.play(*[Flash(d.get_center(), color=WHITE, flash_radius=0.35) for d in nl], run_time=1.0)

        # ---- Berry curvature: go to top view, swap in the 2D map
        with self.narrate('mod3') as b:
            self.stop_ambient_camera_rotation()
            self.move_camera(phi=0, theta=-90 * DEGREES, run_time=2.5)
            ax2 = kspace_axes(7.0, 7.0 * 2.8 / (2 * np.pi), xr=BZ, yr=(-1.4, 1.4), labels=False)
            ax2.move_to(ax.c2p(0, 0, 0))
            xs = np.linspace(*BZ, 560)
            ys = np.linspace(-1.4, 1.4, 250)
            KX, KY = np.meshgrid(xs, ys)
            img = image_on_axes(signed_rgba(berry(KX, KY), 2.5), ax2, BZ, (-1.4, 1.4))
            frame = frame_box(ax2, BZ, (-1.4, 1.4))
            nm = node_marks(ax2, 0.1)
            self.add_fixed_in_frame_mobjects(img, frame, nm)
            self.remove(img, frame, nm)
            self.play(FadeIn(img), FadeIn(frame), FadeOut(up), FadeOut(dn), FadeOut(lab_k), FadeOut(ax),
                      FadeOut(nl), FadeIn(nm), run_time=1.8)
            hot = VGroup(*[Circle(radius=0.42, color=C_HOT, stroke_width=4).move_to(ax2.c2p(s * NODE, 0))
                           for s in (-1, 1)])
            hl = zh('贝里曲率热点', 28, C_HOT).next_to(frame, DOWN, buff=0.25)
            self.add_fixed_in_frame_mobjects(hot, hl)
            self.remove(hot, hl)
            b.wait_sentence(1)
            self.play(Create(hot), FadeIn(hl), run_time=1.2)
            sgn = VGroup(MathTex(r'\Omega>0', font_size=30, color=C_POS).next_to(hot[0], UP, buff=0.1),
                         MathTex(r'\Omega<0', font_size=30, color=C_NEG).next_to(hot[1], UP, buff=0.1))
            self.add_fixed_in_frame_mobjects(sgn)
            self.remove(sgn)
            self.play(FadeIn(sgn), run_time=0.8)

        mapg = Group(img, frame, nm, hot, sgn)
        with self.narrate('mod4') as b:
            self.play(FadeOut(hl), FadeOut(par), mapg.animate.scale(0.78).to_edge(LEFT, buff=0.4).shift(0.3 * DOWN),
                      run_time=1.2)
            t1 = VGroup(zh('时间反演', 28), MathTex(r'\checkmark', color=GREEN), MathTex(r'\Omega(-\mathbf k)=-\Omega(\mathbf k)', font_size=32)).arrange(RIGHT, buff=0.2)
            t2 = VGroup(zh('空间反演', 28), MathTex(r'\times', color=RED)).arrange(RIGHT, buff=0.2)
            t3 = VGroup(zh('线性霍尔', 28), MathTex(r'=0', font_size=34)).arrange(RIGHT, buff=0.15)
            t4 = VGroup(zh('非线性霍尔', 28, C_J), MathTex(r'\neq 0', font_size=34, color=C_J)).arrange(RIGHT, buff=0.15)
            col = VGroup(t1, t2, t3, t4).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.5).shift(0.2 * DOWN)
            self.add_fixed_in_frame_mobjects(col)
            self.remove(col)
            self.play(FadeIn(t1, shift=0.2 * LEFT), run_time=1.0)
            self.play(FadeIn(t2, shift=0.2 * LEFT), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(t3, shift=0.2 * LEFT), run_time=0.8)
            self.play(FadeIn(t4, shift=0.2 * LEFT), run_time=0.8)

        with self.narrate('mod5') as b:
            ax3 = kspace_axes(7.0 * 0.78, 7.0 * 0.78 * 2.8 / (2 * np.pi), xr=BZ, yr=(-1.4, 1.4), labels=False)
            ax3.move_to(frame.get_center())
            cont = contour_mobject(ax3, eps(KX, KY), xs, ys, 0.3, color=WHITE, width=3.5)
            mu = MathTex(r'\mu = 0.3', font_size=32).next_to(frame, DOWN, buff=0.2)
            # side view of the cones along ky = 0
            sax = Axes(x_range=[-np.pi, np.pi, np.pi], y_range=[-1.2, 1.2, 1], x_length=4.6, y_length=2.2, tips=False,
                       axis_config=dict(include_ticks=False, stroke_color=GREY_B, stroke_width=1.2))
            sax.to_edge(RIGHT, buff=0.6).shift(2.3 * DOWN)
            cu = sax.plot(lambda k: min(abs(np.cos(k) - 0.5), 1.2), x_range=[-np.pi, np.pi, 0.01], color='#FF8A3D')
            cd = sax.plot(lambda k: -min(abs(np.cos(k) - 0.5), 1.2), x_range=[-np.pi, np.pi, 0.01], color='#3D7BFF')
            ml = DashedLine(sax.c2p(-np.pi, 0.3), sax.c2p(np.pi, 0.3), color=WHITE, stroke_width=2)
            fill = VGroup(*[sax.get_area(sax.plot(lambda k: abs(np.cos(k) - 0.5), x_range=r), x_range=r,
                                         bounded_graph=sax.plot(lambda k: 0.3, x_range=r), color=BLUE_B, opacity=0.5)
                            for r in [(-np.arccos(0.2), -np.arccos(0.8)), (np.arccos(0.8), np.arccos(0.2))]])
            side = VGroup(sax, cu, cd, ml, fill, MathTex(r'k_y=0', font_size=26, color=GREY_B).next_to(sax, UP, buff=0.05))
            self.add_fixed_in_frame_mobjects(cont, mu, side)
            self.remove(cont, mu, side)
            self.play(FadeOut(col), Create(cont), FadeIn(mu), run_time=1.5)
            self.play(FadeIn(side), run_time=1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
