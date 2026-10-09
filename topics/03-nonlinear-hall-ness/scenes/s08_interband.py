import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *
from scenes.s07_crossover import XR, YR, GAM


def cone_cartoon(width=2.6, height=2.4, mu=0.0):
    cax = Axes(x_range=[-1, 1, 1], y_range=[-1, 1, 1], x_length=width, y_length=height, tips=False,
               axis_config=dict(include_ticks=False, stroke_opacity=0))
    up = cax.plot(lambda x: abs(x), color='#FF8A3D', stroke_width=4)
    dn = cax.plot(lambda x: -abs(x), color='#3D7BFF', stroke_width=4)
    fill = cax.get_area(dn, x_range=[-1, 1], bounded_graph=cax.plot(lambda x: -1.0), color='#3D7BFF', opacity=0.35)
    ml = DashedLine(cax.c2p(-1, mu), cax.c2p(1, mu), color=WHITE, stroke_width=2)
    mlab = MathTex(rf'\mu = {mu:g}', font_size=26).next_to(ml, RIGHT, buff=0.08)
    return VGroup(cax, fill, up, dn, ml, mlab), cax


class S08_Interband(NScene):
    def construct(self):
        # field-induced upper-band population dn+ = n+(E) - n+(0).  At mu = 0, Tr n = 1 exactly
        # (sigma_y H* sigma_y = -H for a traceless 2x2 H), so every excited electron leaves a
        # hole in the lower band at the same kappa.
        d = load('maps.npz')
        kx, ky = d['kxs'], d['kys']
        ix = (kx >= XR[0]) & (kx <= XR[1])
        iy = (ky >= YR[0]) & (ky <= YR[1])
        KX, KY = np.meshgrid(kx[ix], ky[iy])
        n0 = n_eq(KX, KY, 0.0, GAM)[0]
        Eg = np.r_[0.0, d['E']]
        dn = np.concatenate([np.zeros((1,) + n0.shape), d['nup'][:, 0][:, iy][:, :, ix] - n0[None]], 0)

        def dn_at(E):
            i = int(np.clip(np.searchsorted(Eg, E) - 1, 0, len(Eg) - 2))
            w = np.clip((E - Eg[i]) / (Eg[i + 1] - Eg[i]), 0, 1)
            return (1 - w) * dn[i] + w * dn[i + 1]
        vmax = 0.45
        Et = ValueTracker(0.0)
        ax = Axes(x_range=[*XR, 1], y_range=[*YR, 0.5], x_length=6.6, y_length=6.6 * 2.5 / 4.4, tips=False,
                  axis_config=dict(include_ticks=False, stroke_color=GREY_B, stroke_width=1))
        ax.to_edge(LEFT, buff=0.5).shift(0.6 * UP)
        img = image_on_axes(signed_rgba(dn_at(0), vmax, pos=C_POS, neg=C_NEG), ax, XR, YR)
        img.add_updater(lambda m: m.__setattr__('pixel_array', signed_rgba(dn_at(Et.get_value()), vmax, pos=C_POS, neg=C_NEG)))
        box = frame_box(ax, XR, YR)
        nodes = node_marks(ax, 0.08, color=WHITE)
        title = VGroup(MathTex(r'\Delta n_+(\boldsymbol\kappa)', font_size=34), zh('上能带被激发的电子', 24, GREY_A),
                       MathTex(r'\mu = 0,\ \Gamma = 0.1', font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.25)
        if title.width > box.width + 0.4:
            title.scale_to_fit_width(box.width + 0.4)
        title.next_to(box, UP, buff=0.2)
        cart, cax = cone_cartoon(mu=0.0)
        cart.to_edge(RIGHT, buff=1.2).shift(0.6 * UP)
        q = zh('没有费米面，电流从哪里来？', 30, C_HOT).next_to(cart, DOWN, buff=0.4)
        with self.narrate('int1') as b:
            self.play(FadeIn(img), Create(box), FadeIn(title), FadeIn(nodes), run_time=1.2)
            self.play(FadeIn(cart), run_time=1.2)
            self.play(FadeIn(q), run_time=0.8)

        Eread = VGroup(MathTex('E =', font_size=34), DecimalNumber(0, num_decimal_places=4, font_size=34))
        Eread.arrange(RIGHT, buff=0.12).next_to(box, DOWN, buff=0.35)
        Eread[1].add_updater(lambda m: m.set_value(Et.get_value()))
        shift_ar = Arrow(ax.c2p(-1.6, 0.85), ax.c2p(1.6, 0.85), buff=0, color=C_E, stroke_width=5)
        shl = MathTex(r'\mathbf E', font_size=30, color=C_E).next_to(shift_ar, RIGHT, buff=0.1)
        tr = zh('同一 κ：上带多一个电子 = 下带多一个空穴', 22, GREY_A).next_to(box, DOWN, buff=0.95)
        with self.narrate('int2') as b:
            jump = Arrow(cax.c2p(0.12, -0.12), cax.c2p(0.12, 0.12), buff=0, color=C_BOX2, stroke_width=5,
                         max_tip_length_to_length_ratio=0.45)
            jl = zh('带间跃迁（朗道–齐纳）', 24, C_BOX2).next_to(cart, DOWN, buff=0.4)
            self.play(FadeOut(q), GrowArrow(jump), FadeIn(jl), FadeIn(Eread), run_time=1.2)
            self.play(GrowArrow(shift_ar), FadeIn(shl), run_time=0.8)
            self.play(Et.animate.set_value(0.02), FadeIn(tr), run_time=3.5, rate_func=smooth)
            b.wait_sentence(1)
            self.play(Et.animate.set_value(0.06), run_time=max(1.0, b.remaining() - 0.5), rate_func=smooth)

        img.clear_updaters()
        Eread[1].clear_updaters()
        self.play(FadeOut(Group(img, box, nodes, title, cart, jump, jl, Eread, shift_ar, shl, tr)), run_time=0.8)

        # ------------- comparison of Hall-current formulas (paper Fig. 2c,d)
        dig = json.loads((ROOT / 'data' / 'fig2cd_digitized.json').read_text())
        series = [('negf', C_NEG, r'\mathrm{Tr}[v_y\tilde n]/E', Dot),
                  ('bc', C_POS, r'\tilde n\,\Omega', Square),
                  ('shift', '#3DBB6B', r'n_0(\mathbf k + E/2\Gamma)\,\Omega', Triangle)]

        def panel(key, ymax, step, label):
            a = Axes(x_range=[0, 0.1, 0.05], y_range=[0, ymax, step], x_length=5.4, y_length=3.6, tips=False,
                     axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                      decimal_number_config=dict(num_decimal_places=2)),
                     y_axis_config=dict(decimal_number_config=dict(num_decimal_places=0)))
            t = MathTex(label, font_size=32)
            return a, t

        axL, tL = panel('mu0.3', 13, 4, r'\mu = 0.3')
        axR, tR = panel('mu0', 3.5, 1, r'\mu = 0')
        VGroup(axL, axR).arrange(RIGHT, buff=1.0).shift(0.6 * DOWN + 0.35 * RIGHT)
        tL.next_to(axL, UP, buff=0.15)
        tR.next_to(axR, UP, buff=0.15)
        ylab = MathTex(r'J_y/E\ (\times 10^{-4})', font_size=26).rotate(PI / 2).next_to(axL, LEFT, buff=0.45)
        xls = VGroup(MathTex('E', font_size=28).next_to(axL.x_axis, DOWN, buff=0.4),
                     MathTex('E', font_size=28).next_to(axR.x_axis, DOWN, buff=0.4))

        def plot(axx, key, k, col, shape):
            E = dig[key][k]['E']
            J = dig[key][k]['JyE_1e-4']
            line = axx.plot_line_graph(E, J, add_vertex_dots=False, line_color=col, stroke_width=3)
            marks = VGroup(*[shape(color=col, fill_opacity=1).scale(0.07 if shape is not Dot else 1.0)
                             .move_to(axx.c2p(e, j)) for e, j in zip(E, J)])
            if shape is Dot:
                marks = VGroup(*[Dot(axx.c2p(e, j), radius=0.06, color=col) for e, j in zip(E, J)])
            return VGroup(line, marks)

        legend = VGroup()
        for k, col, tex, shape in series:
            legend.add(VGroup(Line(ORIGIN, 0.45 * RIGHT, color=col, stroke_width=4), MathTex(tex, font_size=28))
                       .arrange(RIGHT, buff=0.12))
        legend.arrange(RIGHT, buff=0.6).to_edge(UP, buff=0.45)
        src = zh('数据：论文 Fig. 2(c,d)', 18, GREY_C).to_corner(DR, buff=0.2)
        with self.narrate('int3') as b:
            self.play(Create(axL), Create(axR), FadeIn(tL), FadeIn(tR), FadeIn(ylab), FadeIn(xls), FadeIn(src), run_time=1.5)
            self.play(LaggedStartMap(FadeIn, legend, shift=0.2 * DOWN, lag_ratio=0.3), run_time=1.5)

        with self.narrate('int4') as b:
            pl = [plot(axL, 'mu0.3', k, col, shape) for k, col, _, shape in series]
            self.play(*[Create(p[0]) for p in pl], *[FadeIn(p[1]) for p in pl], run_time=2.5)
            weak = Rectangle(width=axL.c2p(0.025, 0)[0] - axL.c2p(0, 0)[0], height=3.6, stroke_width=0,
                             fill_color=C_J, fill_opacity=0.12).move_to(axL.c2p(0.0125, 6.5))
            self.play(FadeIn(weak), run_time=0.8)
            b.wait_sentence(1)
            gap = DoubleArrow(axL.c2p(0.08, 4.0), axL.c2p(0.08, 1.9), buff=0, color=C_HOT, stroke_width=4,
                              max_tip_length_to_length_ratio=0.15)
            self.play(GrowFromCenter(gap), Indicate(pl[1], color=C_POS), run_time=1.5)

        with self.narrate('int5') as b:
            pr = [plot(axR, 'mu0', k, col, shape) for k, col, _, shape in series]
            self.play(*[Create(p[0]) for p in pr], *[FadeIn(p[1]) for p in pr], run_time=2.5)
            zl = zh('恒为零', 24, '#3DBB6B').move_to(axR.c2p(0.045, 0.55))
            self.play(Indicate(pr[2], color='#3DBB6B'), FadeIn(zl), run_time=1.5)

        self.play(FadeOut(VGroup(axL, axR, tL, tR, ylab, xls, legend, weak, gap, zl, *pl, *pr)), FadeOut(src), run_time=0.8)
        r1 = VGroup(zh('常数-Γ 热库', 30), MathTex(r'\Delta\kappa = E/\Gamma', font_size=40),
                    MathTex(r'E^*_\Gamma \approx \Gamma\,\Delta\kappa_x', font_size=40, color=C_BOX1))
        r2 = VGroup(zh('常数弛豫时间', 30), MathTex(r'\tau_B = 1/2\Gamma:\ \ \Delta\kappa = E/2\Gamma', font_size=40),
                    MathTex(r'E^*_{\tau} \approx 2\Gamma\,\Delta\kappa_x', font_size=40, color=C_BOX2))
        for r in (r1, r2):
            r.arrange(RIGHT, buff=0.6)
        rows = VGroup(r1, r2).arrange(DOWN, buff=0.6, aligned_edge=LEFT).shift(0.6 * UP)
        concl = VGroup(zh('热点判据：普适', 30, C_J), zh('临界电场：依赖耗散机制', 30, C_HOT)).arrange(RIGHT, buff=1.0)
        concl.next_to(rows, DOWN, buff=0.9)
        with self.narrate('int6') as b:
            self.play(FadeIn(r1, shift=0.2 * RIGHT), run_time=1.2)
            self.play(FadeIn(r2, shift=0.2 * RIGHT), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(concl[0]), run_time=0.8)
            self.play(FadeIn(concl[1]), run_time=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
