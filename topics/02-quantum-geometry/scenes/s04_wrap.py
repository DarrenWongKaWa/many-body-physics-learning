import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NG = 10                                      # grid lines per direction
KS = -np.pi + 2 * np.pi * np.arange(NG) / NG
TT = np.linspace(-np.pi, np.pi, 241)
C_GX, C_GY = '#F2F2F2', '#E8C468'           # constant-kx lines, constant-ky lines
KX, KY = grid(150)
DK = (2 * np.pi / 150) ** 2


def nq(m):
    return lambda kx, ky: unit(qwz_d(kx, ky, m))


def chern(m):
    return (geometry(nq(m), KX, KY)[3].sum() * DK) / (2 * np.pi)


def int_trg(m):
    gxx, gyy, _, _ = geometry(nq(m), KX, KY)
    return ((gxx + gyy).sum() * DK) / (2 * np.pi)


class S04_Wrap(NScene):
    def construct(self):
        m = ValueTracker(3.2)
        az = ValueTracker(0.5)
        sx, sr = ValueTracker(3.3), ValueTracker(2.25)

        # ---------------- BZ panel with the grid
        ax = kspace_axes(3.9, labels=True).move_to([-3.9, -0.1, 0])
        box = frame_box(ax, (-np.pi, np.pi), (-np.pi, np.pi), color=GREY_C)
        glines = VGroup()
        for k in KS:
            glines.add(Line(ax.c2p(k, -np.pi), ax.c2p(k, np.pi), stroke_color=C_GX, stroke_width=1.6, stroke_opacity=0.8))
            glines.add(Line(ax.c2p(-np.pi, k), ax.c2p(np.pi, k), stroke_color=C_GY, stroke_width=1.6, stroke_opacity=0.8))
        bzl = txt('Brillouin zone', 30, GREY_A).next_to(box, UP, buff=0.5)

        def sphere_and_grid():
            sph = Sphere2D(radius=sr.get_value(), el=0.38, az=az.get_value(), n_merid=0).move_to([sx.get_value(), -0.1, 0])
            f = nq(m.get_value())
            g = VGroup()
            for k in KS:
                g.add(sph.curve([np.array(f(k, t)) for t in TT], color=C_GX, width=1.8, back_opacity=0.18, front_opacity=0.9))
                g.add(sph.curve([np.array(f(t, k)) for t in TT], color=C_GY, width=1.8, back_opacity=0.18, front_opacity=0.9))
            return VGroup(sph, g, sph.pole_labels(32))

        live = always_redraw(sphere_and_grid)
        model = MathTex(r'\mathbf h(\mathbf k) = \big(\sin k_x,\ \sin k_y,\ m - \cos k_x - \cos k_y\big)', font_size=38)
        model.to_edge(UP, buff=0.35)
        mlab = MathTex('m =', font_size=40)
        mval = always_redraw(lambda: DecimalNumber(m.get_value(), num_decimal_places=2, font_size=40,
                                                   color=YELLOW).next_to(mlab, RIGHT, buff=0.15))
        mgrp = VGroup(mlab).next_to(box, DOWN, buff=0.35).shift(0.35 * LEFT)

        # ---- wrap1
        with self.narrate('wrap1') as b:
            self.play(Create(box), Create(ax), FadeIn(bzl), run_time=1.2)
            b.wait_sentence(1)
            self.play(Write(model), FadeIn(mlab), FadeIn(mval), run_time=1.6)
            b.wait_sentence(2)
            self.play(LaggedStartMap(Create, glines, lag_ratio=0.05), run_time=1.5)
            self.play(FadeIn(live), run_time=1.2)

        # ---- wrap2: trivial, crumpled near the pole
        triv = txt('trivial: image stays near the north pole', 30, GREY_A).move_to([3.3, -3.1, 0])
        with self.narrate('wrap2') as b:
            self.play(az.animate.set_value(0.9), run_time=2.0)
            self.play(FadeIn(triv), run_time=0.8)
            gsm = MathTex(r'g \approx 0', font_size=40, color=C_G).next_to(live, UP, buff=-0.2).shift(2.2 * RIGHT + 0.2 * DOWN)
            self.play(FadeIn(gsm), az.animate.set_value(1.3), run_time=b.remaining(-0.4))

        # ---- wrap3: lower m through the inversion -> wraps once
        clab = MathTex(r'\frac{1}{2\pi}\int_{\rm BZ}\Omega\, d^2k =', font_size=34)
        cgrp = VGroup(clab).move_to([-4.4, -3.3, 0])
        cval = always_redraw(lambda: Integer(int(round(chern(m.get_value()))), font_size=44, color=C_POS).next_to(clab, RIGHT, buff=0.2))
        with self.narrate('wrap3') as b:
            self.play(FadeOut(triv), FadeOut(gsm), run_time=0.6)
            b.wait_sentence(1)
            self.play(m.animate.set_value(1.0), az.animate.set_value(2.6), run_time=b.until_sentence(2, 3.0) + 1.0,
                      rate_func=smooth)
            self.play(az.animate.set_value(3.6), run_time=max(0.5, b.sentence_start(2) - b.elapsed()), rate_func=linear)
            self.play(FadeIn(clab), FadeIn(cval), az.animate.set_value(4.4), run_time=1.5, rate_func=linear)
            b.wait_sentence(3)
            cn = txt('= Chern number $C$', 32, C_POS).next_to(cgrp, RIGHT, buff=0.75)
            self.play(FadeIn(cn, shift=0.15 * UP), az.animate.set_value(4.9), run_time=1.0, rate_func=linear)

        # ---- wrap4: curvature (global) vs metric (local, >= 0)
        mm = 1.0
        gxx, gyy, gxy, om = geometry(nq(mm), KX, KY)
        trg = gxx + gyy
        ax2 = kspace_axes(3.0, labels=True).move_to([-4.3, 0.2, 0])
        ax3 = kspace_axes(3.0, labels=True).move_to([-0.4, 0.2, 0])
        img_om = image_on_axes(signed_rgba(om, 0.5), ax2, (-np.pi, np.pi), (-np.pi, np.pi))
        img_g = image_on_axes(mono_rgba(trg, 0.5), ax3, (-np.pi, np.pi), (-np.pi, np.pi))
        b2 = frame_box(ax2, (-np.pi, np.pi), (-np.pi, np.pi))
        b3 = frame_box(ax3, (-np.pi, np.pi), (-np.pi, np.pi))
        t2 = VGroup(txt('Berry curvature', 30, C_POS), MathTex(r'\Omega(\mathbf k)', font_size=34, color=C_POS)).arrange(RIGHT, buff=0.15).next_to(b2, UP, buff=0.5)
        t3 = VGroup(txt('quantum metric', 30, C_G), MathTex(r'\mathrm{tr}\,g(\mathbf k)', font_size=34, color=C_G)).arrange(RIGHT, buff=0.15).next_to(b3, UP, buff=0.5)
        s2 = VGroup(txt('integral: global, quantized', 26, GREY_A), MathTex(r'\int\Omega\,d^2k = 2\pi C', font_size=32)).arrange(DOWN, buff=0.12).next_to(b2, DOWN, buff=0.3)
        s3 = VGroup(txt('local, never negative', 26, GREY_A), MathTex(r'g_{ij}\ \succeq\ 0', font_size=32)).arrange(DOWN, buff=0.12).next_to(b3, DOWN, buff=0.3)
        bz_grp = VGroup(ax, box, glines, bzl)
        with self.narrate('wrap4') as b:
            self.play(FadeOut(VGroup(mlab, model, cn)), FadeOut(mval), FadeOut(clab), FadeOut(cval),
                      ReplacementTransform(bz_grp, VGroup(ax2, b2)), sx.animate.set_value(4.75), sr.animate.set_value(1.7), run_time=1.2)
            self.play(FadeIn(img_om), FadeIn(t2), run_time=1.0)
            self.bring_to_front(b2)
            self.play(FadeIn(s2), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(ax3), FadeIn(b3), FadeIn(img_g), FadeIn(t3), run_time=1.0)
            self.play(FadeIn(s3), run_time=0.8)

        # ---- wrap5: positivity -> tr g >= |Omega|
        ineq = MathTex(r'G_{ij}\succeq 0', r'\ \Longrightarrow\ ', r'\mathrm{tr}\,g(\mathbf k)\ \ge\ |\Omega(\mathbf k)|',
                       font_size=38)
        ineq[2].set_color(C_G)
        ineq2 = MathTex(r'\int_{\rm BZ}\frac{d^2k}{2\pi}\,\mathrm{tr}\,g', r'\ \ge\ ', r'|C|', font_size=38)
        ineq2[0].set_color(C_G); ineq2[2].set_color(C_POS)
        vals = MathTex(r'\int \tfrac{d^2k}{2\pi}\mathrm{tr}\,g = ' + f'{int_trg(mm):.2f}', r'\ \ \ge\ \ ', r'|C| = 1', font_size=32)
        vals[0].set_color(C_G); vals[2].set_color(C_POS)
        stack = VGroup(ineq, ineq2, vals).arrange(DOWN, buff=0.22).move_to([-2.3, -2.3, 0])
        with self.narrate('wrap5') as b:
            self.play(FadeOut(s2), FadeOut(s3), Group(ax2, b2, img_om, t2, ax3, b3, img_g, t3).animate.shift(0.75 * UP), run_time=0.8)
            self.play(Write(ineq[0]), run_time=1.0)
            b.wait_sentence(1)
            self.play(Write(ineq[1:]), run_time=1.5)
            b.wait_sentence(2)
            self.play(Write(ineq2), run_time=1.5)
            self.play(FadeIn(vals), run_time=1.0)
            self.play(az.animate.set_value(az.get_value() + 1.2), run_time=max(0.5, b.remaining(-0.3)), rate_func=linear)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
