import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

XR, YR = (-2.5, 2.5), (-1.25, 1.25)
NX, NY = 440, 220
xs = np.linspace(*XR, NX)
ys = np.linspace(*YR, NY)
KX, KY = np.meshgrid(xs, ys)
OM = berry(KX, KY)
MU, TV = 0.3, 0.02

# fine grid for the pocket integrals
_f = np.linspace(-np.pi, np.pi, 900, endpoint=False) + np.pi / 900
FX, FY = np.meshgrid(_f, _f)
FOM = berry(FX, FY)
DA = (2 * np.pi / 900) ** 2 / (2 * np.pi) ** 2


def occ(s, X=KX, Y=KY):
    return 1 / (1 + np.exp(np.clip((eps(X - s, Y) - MU) / TV, -50, 50)))


def pocket_integrals(s):
    n = occ(s, FX, FY)
    L = (n * FOM * (FX < 0)).sum() * DA
    R = (n * FOM * (FX >= 0)).sum() * DA
    return L, R


def product_rgba(s):
    n = occ(s)
    rgba = signed_rgba(OM, 2.5).astype(float)
    bg = np.array(color_to_rgb(BG)) * 255
    w = 0.22 + 0.78 * n
    rgba[..., :3] = bg + (rgba[..., :3] - bg) * w[..., None]
    return rgba.astype(np.uint8)


class S03_Dipole(NScene):
    def construct(self):
        # start from the end state of S02 (full BZ map on the left)
        ax0 = kspace_axes(5.4).to_edge(LEFT, buff=0.7).shift(0.2 * DOWN)
        g = np.linspace(-np.pi, np.pi, 360)
        GX, GY = np.meshgrid(g, g)
        img0 = image_on_axes(signed_rgba(berry(GX, GY), 2.5), ax0, (-np.pi, np.pi), (-np.pi, np.pi))
        box0 = frame_box(ax0, (-np.pi, np.pi), (-np.pi, np.pi))
        cont0 = contour_mobject(ax0, eps(GX, GY), g, g, MU, color=WHITE, width=3)
        self.add(img0, box0, ax0, cont0)

        ax = Axes(x_range=[*XR, 1], y_range=[*YR, 1], x_length=8.0, y_length=4.0, tips=False,
                  axis_config=dict(stroke_color=GREY_B, stroke_width=1.2, include_ticks=False))
        ax.to_edge(LEFT, buff=0.45).to_edge(UP, buff=1.0)
        lx = MathTex(r'k_x', font_size=28, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.08)
        ly = MathTex(r'k_y', font_size=28, color=GREY_B).next_to(ax.y_axis, UP, buff=0.08)
        box = frame_box(ax, XR, YR)
        s = ValueTracker(0.0)
        img = image_on_axes(product_rgba(0), ax, XR, YR)
        img.add_updater(lambda m: m.__setattr__('pixel_array', product_rgba(s.get_value())))
        base = contour_mobject(ax, eps(KX, KY), xs, ys, MU, color=WHITE, width=3)
        cont = base.copy()
        cont.add_updater(lambda m: m.become(base.copy().shift(RIGHT * s.get_value() * ax.x_length / (XR[1] - XR[0]))))
        ghost = VGroup(*[DashedVMobject(m, num_dashes=24) for m in base.copy().set_stroke(GREY_B, 1.5)])
        nodes = node_marks(ax, 0.08)

        # bar meters
        bx0 = 4.2
        y0 = ax.c2p(0, 0)[1]
        sc = 1.6 / 0.006
        labels = VGroup(zh('左口袋', 22, C_POS), zh('右口袋', 22, C_NEG), zh('净值×4', 22, C_J))
        for i, l in enumerate(labels):
            l.move_to([bx0 + 1.1 * i, y0 - 2.1, 0])
        axis_line = Line([bx0 - 0.5, y0, 0], [bx0 + 2.7, y0, 0], color=GREY_B, stroke_width=1.5)
        mtitle = MathTex(r'\int n\,\Omega', font_size=36).move_to([bx0 + 1.1, y0 + 2.0, 0])

        def bars():
            L, R = pocket_integrals(s.get_value())
            vals = [L, R, -4 * (L + R)]
            cols = [C_POS, C_NEG, C_J]
            grp = VGroup()
            for i, (v, c) in enumerate(zip(vals, cols)):
                h = max(abs(v) * sc, 0.001)
                r = Rectangle(width=0.6, height=h, fill_color=c, fill_opacity=0.9, stroke_width=0)
                r.move_to([bx0 + 1.1 * i, y0 + np.sign(v) * h / 2, 0])
                grp.add(r)
            return grp
        meter = always_redraw(bars)

        Ear = Arrow(ax.c2p(-2.4, 1.52), ax.c2p(-0.5, 1.52), color=C_E, buff=0, stroke_width=5)
        Elb = MathTex(r'\mathbf E', color=C_E, font_size=34).next_to(Ear, RIGHT, buff=0.1)

        with self.narrate('bcd1') as b:
            self.play(ReplacementTransform(VGroup(ax0, box0), VGroup(ax, box)),
                      FadeOut(img0), FadeOut(cont0), FadeIn(img), FadeIn(base), run_time=1.5)
            self.add(lx, ly, nodes)
            self.remove(base)
            self.add(ghost, cont)
            self.play(GrowArrow(Ear), FadeIn(Elb), run_time=0.8)
            self.play(s.animate.set_value(0.12), run_time=2.5)
            dk = MathTex(r'\Delta k_x = E\tau', font_size=34).next_to(Elb, RIGHT, buff=0.5)
            self.play(FadeIn(dk), run_time=0.6)

        with self.narrate('bcd2') as b:
            self.play(FadeIn(axis_line), FadeIn(labels), FadeIn(mtitle), run_time=0.8)
            self.add(meter)
            self.play(s.animate.set_value(0.0), run_time=1.5)
            self.play(s.animate.set_value(0.15), run_time=2.5)
            b.wait_sentence(1)
            chain = MathTex(r'J_y = E\!\int n\,\Omega', r'\;\approx\; E\cdot \Delta k_x\, D', r'\;\propto\; D\,E^2',
                            font_size=40).to_edge(DOWN, buff=0.75).shift(LEFT * 1.2)
            dlab = MathTex(r'D = \int n_0\,\partial_{k_x}\Omega', font_size=32, color=GREY_A).next_to(chain, RIGHT, buff=0.6)
            self.play(Write(chain[0]), run_time=1.2)
            self.play(Write(chain[1]), FadeIn(dlab), run_time=1.4)
            self.play(Write(chain[2]), run_time=1.0)
            self.play(Circumscribe(chain[2], color=C_J), run_time=1.0)

        bcd_name = zh('贝里曲率偶极子', 30, C_J).next_to(chain, UP, buff=0.25).align_to(chain, LEFT)
        cards = VGroup()
        for name, cn, ref in [(r'\mathrm{WTe_2}', '（双层 / 少层）', 'Nature 2019; Nat. Mater. 2019'),
                              (r'\mathrm{TaIrTe_4}', '', 'Nat. Nanotechnol. 2021'),
                              (r'\mathrm{Ce_3Bi_4Pd_3}', '（外尔–近藤半金属）', 'PNAS 2021')]:
            t = VGroup(MathTex(name, font_size=34))
            if cn:
                t.add(zh(cn, 20, GREY_A))
            t.arrange(DOWN, buff=0.08)
            r = Text(ref, font_size=18, color=GREY_B)
            c = VGroup(t, r).arrange(DOWN, buff=0.15)
            c.add_to_back(RoundedRectangle(corner_radius=0.1, width=4.1, height=1.45, stroke_color=GREY_C,
                                           stroke_width=1.5, fill_color='#141925', fill_opacity=1))
            cards.add(c)
        cards.arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.narrate('bcd3') as b:
            self.play(FadeIn(bcd_name, shift=0.2 * UP), run_time=0.8)
            b.wait_until(2.2)
            self.play(FadeOut(VGroup(chain, dlab, bcd_name)), run_time=0.6)
            self.play(LaggedStartMap(FadeIn, cards[:2], shift=0.2 * UP, lag_ratio=0.3), run_time=1.5)

        with self.narrate('bcd4') as b:
            self.play(FadeIn(cards[2], shift=0.2 * UP), cards[:2].animate.set_opacity(0.35),
                      FadeOut(VGroup(meter, labels, axis_line, mtitle)), run_time=1.0)
            giant = VGroup(zh('巨大的霍尔响应', 26, C_HOT), zh('偏离 E² 标度', 26, C_HOT)).arrange(DOWN, buff=0.1)
            giant.next_to(cards[2], UP, buff=0.25)
            self.play(Circumscribe(cards[2], color=C_HOT), FadeIn(giant), run_time=1.8)

        with self.narrate('bcd5') as b:
            self.play(FadeOut(cards), FadeOut(giant), FadeIn(VGroup(meter, labels, axis_line, mtitle)), run_time=0.8)
            pert = VGroup(zh('微扰前提：', 28, GREY_A), MathTex(r'\Delta k_x \ll', font_size=36),
                          zh('到热点的距离', 28)).arrange(RIGHT, buff=0.15).to_edge(DOWN, buff=1.4)
            pert.shift(LEFT * 1.3)
            self.play(FadeIn(pert), run_time=0.8)
            b.wait_until(4.0)
            self.play(s.animate.set_value(DKX), run_time=3.0)
            hot = Circle(radius=0.32, color=C_HOT, stroke_width=5).move_to(ax.c2p(-NODE, 0))
            hotl = zh('热点', 26, C_HOT).next_to(hot, DOWN, buff=0.1)
            self.play(Create(hot), FadeIn(hotl), Flash(ax.c2p(-NODE, 0), color=C_HOT, flash_radius=0.45),
                      run_time=1.2)
            self.play(s.animate.set_value(0.45), run_time=2.0)
            # interband cartoon
            meter.clear_updaters()
            self.play(FadeOut(meter), FadeOut(axis_line), FadeOut(labels), FadeOut(mtitle), run_time=0.6)
            cax = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=2.6, y_length=2.6, tips=False,
                       axis_config=dict(include_ticks=False, stroke_opacity=0)).move_to([bx0 + 1.1, y0, 0])
            up = cax.plot(lambda x: abs(x), color=ORANGE, stroke_width=4)
            dn = cax.plot(lambda x: -abs(x), color=BLUE, stroke_width=4)
            jump = Arrow(cax.c2p(0.15, -0.15), cax.c2p(0.15, 0.15), buff=0, color=C_BOX2, stroke_width=5,
                         max_tip_length_to_length_ratio=0.45)
            il = zh('带间跃迁', 26, C_BOX2).next_to(cax, DOWN, buff=0.15)
            self.play(Create(up), Create(dn), GrowArrow(jump), FadeIn(il), run_time=1.5)
            b.wait_sentence(2)
            fail = zh('微扰展开失效  →  需要非微扰理论', 32, C_E).to_edge(DOWN, buff=0.5)
            self.play(FadeOut(pert), Write(fail), run_time=1.5)
        meter.clear_updaters()
        img.clear_updaters()
        cont.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
