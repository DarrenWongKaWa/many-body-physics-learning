import sys, pathlib, json
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

DIG = json.loads((ROOT / 'data' / 'fig3d_4a_digitized.json').read_text())


def clean_curve(w, f, grid):
    w, f = np.asarray(w), np.asarray(f)
    o = np.argsort(w)
    g = np.interp(grid, w[o], f[o])
    k = np.ones(5) / 5
    g = np.convolve(np.pad(g, 2, mode='edge'), k, mode='valid')
    return np.clip(g, 0, 1)


class S09_Spectral(NScene):
    def construct(self):
        ax = Axes(x_range=[-2, 2, 1], y_range=[0, 1.05, 0.2], x_length=9, y_length=5, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=24),
                  y_axis_config=dict(decimal_number_config=dict(num_decimal_places=1))).shift(0.4 * DOWN)
        xl = MathTex(r'\omega', font_size=34).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = MathTex(r'f_{\rm eff}(\omega)', font_size=34).next_to(ax.y_axis, UP, buff=0.15)
        defn = MathTex(r'f_{\rm eff}(\omega) = \frac{\mathrm{Tr}\,A_{\rm loc,occ}(\omega)}{\mathrm{Tr}\,A_{\rm loc}(\omega)}',
                       font_size=36).to_corner(UR, buff=0.5)
        setup = zh('洛伦兹热库 Γ=0.1, W=4, T=1/30, μ=0.3', 20, GREY_C).to_corner(DR, buff=0.2)
        src = zh('数据：论文 Fig. 3(d)', 18, GREY_C).next_to(setup, UP, buff=0.08, aligned_edge=RIGHT)
        eq = ax.plot(lambda w: 1 / (1 + np.exp(np.clip((w - 0.3) * 30, -50, 50))), x_range=[-2, 2, 0.005],
                     color=WHITE, stroke_width=3)
        eqd = DashedVMobject(eq, num_dashes=60)
        grid = np.linspace(-1.98, 1.98, 400)
        cols = {'E0.04': '#1FB59A', 'E0.09': '#FF7A45', 'E0.15': '#F2C12E'}
        curves = {k: ax.plot_line_graph(grid, clean_curve(DIG['fig3d'][k]['w'], DIG['fig3d'][k]['f'], grid),
                                        add_vertex_dots=False, line_color=c, stroke_width=4) for k, c in cols.items()}
        leg = VGroup(VGroup(DashedLine(ORIGIN, 0.5 * RIGHT, color=WHITE), zh('平衡态', 24)).arrange(RIGHT, buff=0.15),
                     *[VGroup(Line(ORIGIN, 0.5 * RIGHT, color=c, stroke_width=4),
                              MathTex(rf'E = {k[1:]}', font_size=28)).arrange(RIGHT, buff=0.15)
                       for k, c in cols.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        leg.next_to(ax.c2p(-1.9, 0.05), UR, buff=0.1)
        with self.narrate('spe1') as b:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(setup), FadeIn(src), run_time=1.5)
            self.play(Write(defn), run_time=1.5)
            self.play(Create(eqd), FadeIn(leg[0]), run_time=1.5)
        with self.narrate('spe2') as b:
            self.play(Create(curves['E0.04']), FadeIn(leg[1]), run_time=1.5)
            b.wait_sentence(1)
            self.play(Create(curves['E0.09']), FadeIn(leg[2]), run_time=1.3)
            self.play(Create(curves['E0.15']), FadeIn(leg[3]), run_time=1.3)
            w1 = Ellipse(width=1.6, height=0.9, color=WHITE, stroke_width=2.5).move_to(ax.c2p(-0.3, 0.9))
            w2 = Ellipse(width=2.2, height=0.6, color=WHITE, stroke_width=2.5).move_to(ax.c2p(1.1, 0.04))
            lab = zh('摆动 + 左右不对称', 26, C_HOT).move_to(ax.c2p(-1.25, 0.72))
            self.play(Create(w1), Create(w2), FadeIn(lab), run_time=1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


def path_points(n=240):
    """Gamma-X-M-Gamma path; returns k-points and the cumulative path coordinate."""
    G, X, M = np.array([0, 0]), np.array([np.pi, 0]), np.array([np.pi, np.pi])
    segs = [(G, X), (X, M), (M, G)]
    pts, s, s0 = [], [], 0.0
    for a, b in segs:
        L = np.linalg.norm(b - a)
        t = np.linspace(0, 1, n, endpoint=False)
        pts.append(a + t[:, None] * (b - a))
        s.append(s0 + t * L)
        s0 += L
    pts.append(G[None])
    s.append([s0])
    return np.concatenate(pts), np.concatenate(s)


class S10_Interactions(NScene):
    def construct(self):
        boxes = VGroup()
        for t1, t2, c in [('费米子热库', r'\Gamma', C_NEG), ('+ 声子', r'\omega_0 = 1\ \ (\mathrm{Migdal})', C_POS),
                          ('+ 哈伯德相互作用', r'U = 0.8\ \ (\mathrm{DMFT})', '#3DBB6B')]:
            g = VGroup(zh(t1, 28, c), MathTex(t2, font_size=30)).arrange(DOWN, buff=0.15)
            g.add_to_back(RoundedRectangle(corner_radius=0.12, width=3.8, height=1.4, stroke_color=c,
                                           stroke_width=2, fill_color='#141925', fill_opacity=1))
            boxes.add(g)
        boxes.arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.5)
        with self.narrate('ia1') as b:
            self.play(FadeIn(boxes[0], shift=0.2 * DOWN), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(boxes[1], shift=0.2 * DOWN), run_time=1.0)
            self.play(FadeIn(boxes[2], shift=0.2 * DOWN), run_time=1.0)

        f4 = DIG['fig4a']
        ax = Axes(x_range=[0, 0.1, 0.02], y_range=[0, 12.5, 2], x_length=7.5, y_length=4.0, tips=False,
                  axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                   decimal_number_config=dict(num_decimal_places=2)),
                  y_axis_config=dict(decimal_number_config=dict(num_decimal_places=0))).shift(1.0 * DOWN)
        yl = MathTex(r'J_y/E\ (\times10^{-4})', font_size=26).next_to(ax, UP, buff=0.1).align_to(ax, LEFT)
        xl = MathTex('E', font_size=28).next_to(ax.x_axis, DOWN, buff=0.35)
        src = zh('数据：论文 Fig. 4(a)', 18, GREY_C).to_corner(DR, buff=0.2)
        cols = {'fermion': C_NEG, 'phonon': C_POS, 'interaction': '#3DBB6B'}
        plots = {}
        for k, c in cols.items():
            E, J = f4[k]['E'], f4[k]['JyE_e4']
            plots[k] = VGroup(ax.plot_line_graph(E, J, add_vertex_dots=False, line_color=c, stroke_width=3.5),
                              VGroup(*[Dot(ax.c2p(e, j), radius=0.06, color=c) for e, j in zip(E, J)]))
        with self.narrate('ia2') as b:
            self.play(Create(ax), FadeIn(yl), FadeIn(xl), FadeIn(src), run_time=1.2)
            self.play(Create(plots['fermion']), run_time=1.5)
            b.wait_sentence(1)
            self.play(Create(plots['phonon']), Create(plots['interaction']), run_time=2.0)
            enh = Arrow(ax.c2p(0.06, 4.0), ax.c2p(0.06, 9.6), buff=0, color=C_HOT, stroke_width=5)
            el = zh('显著增强', 26, C_HOT).next_to(enh, RIGHT, buff=0.1)
            self.play(GrowArrow(enh), FadeIn(el), run_time=1.0)
        self.play(FadeOut(VGroup(ax, yl, xl, src, enh, el, *plots.values())), FadeOut(boxes), run_time=0.8)

        # ----- band renormalisation (illustrative: D_y -> D_y^eff, slight flattening)
        DYE, Z = 0.985, 0.95
        k, s = path_points()
        e0 = eps(k[:, 0], k[:, 1])
        e1 = Z * eps(k[:, 0], k[:, 1], Dy=DYE)
        L = s[-1]
        bax = Axes(x_range=[0, L, 1], y_range=[-2.8, 2.8, 1], x_length=6.0, y_length=4.4, tips=False,
                   axis_config=dict(include_ticks=False, stroke_color=GREY_B)).to_edge(LEFT, buff=0.8).shift(0.3 * DOWN)
        bare = VGroup(bax.plot_line_graph(s, e0, add_vertex_dots=False, line_color='#FF8A3D', stroke_width=3),
                      bax.plot_line_graph(s, -e0, add_vertex_dots=False, line_color='#3D7BFF', stroke_width=3))
        ren = VGroup(*[DashedVMobject(bax.plot_line_graph(s, sg * e1, add_vertex_dots=False, line_color=WHITE,
                                                          stroke_width=2.5)["line_graph"], num_dashes=70) for sg in (1, -1)])
        ticks = VGroup()
        for name, x in [(r'\Gamma', 0), ('X', np.pi), ('M', 2 * np.pi), (r'\Gamma', L)]:
            ticks.add(MathTex(name, font_size=28).next_to(bax.c2p(x, -2.8), DOWN, buff=0.1))
            ticks.add(DashedLine(bax.c2p(x, -2.8), bax.c2p(x, 2.8), color=GREY_D, stroke_width=1))
        # zoom on the node along Gamma-X
        zax = Axes(x_range=[NODE - 0.06, NODE + 0.06, 0.05], y_range=[-0.05, 0.05, 0.05], x_length=4.2, y_length=3.0,
                   tips=False, axis_config=dict(include_ticks=False, stroke_color=GREY_C)).to_edge(RIGHT, buff=0.8).shift(0.6 * UP)
        zb = VGroup(zax.plot(lambda x: abs(np.cos(x) - 0.5), color='#FF8A3D', stroke_width=3),
                    zax.plot(lambda x: -abs(np.cos(x) - 0.5), color='#3D7BFF', stroke_width=3))
        zr = VGroup(*[DashedVMobject(zax.plot(lambda x, sg=sg: sg * Z * np.sqrt((np.cos(x) - 0.5) ** 2 + (1 - DYE) ** 2),
                                              color=WHITE, stroke_width=3), num_dashes=24) for sg in (1, -1)])
        zbox = SurroundingRectangle(zax, color=GREY_C, buff=0.05)
        zt = zh('节点附近放大', 24, GREY_A).next_to(zbox, UP, buff=0.1)
        gap = DoubleArrow(zax.c2p(NODE, -Z * (1 - DYE)), zax.c2p(NODE, Z * (1 - DYE)), buff=0, color=C_HOT,
                          stroke_width=3, max_tip_length_to_length_ratio=0.25)
        gl = zh('小能隙', 24, C_HOT).next_to(gap, RIGHT, buff=0.1)
        leg = VGroup(VGroup(Line(ORIGIN, 0.45 * RIGHT, color='#FF8A3D'), zh('裸能带', 22)).arrange(RIGHT, buff=0.1),
                     VGroup(DashedLine(ORIGIN, 0.45 * RIGHT, color=WHITE), zh('重整化能带（示意）', 22)).arrange(RIGHT, buff=0.1)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(bax, UP, buff=0.15)
        with self.narrate('ia3') as b:
            sig = MathTex(r'\mathrm{Re}\,\Sigma^R', r'\quad\text{vs}\quad', r'\mathrm{Im}\,\Sigma^R', font_size=40).to_edge(UP, buff=0.4)
            self.play(Write(sig), run_time=1.2)
            self.play(Indicate(sig[0], color=C_HOT), sig[2].animate.set_opacity(0.4), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeOut(sig), Create(bax), FadeIn(ticks), Create(bare), FadeIn(leg), run_time=1.5)
            self.play(Create(ren), run_time=1.5)
            self.play(Create(zbox), FadeIn(zt), Create(zb), run_time=1.0)
            self.play(Create(zr), GrowFromCenter(gap), FadeIn(gl), run_time=1.5)
        self.play(FadeOut(VGroup(bax, ticks, bare, ren, leg, zbox, zt, zb, zr, gap, gl, zax)), run_time=0.7)

        # ----- Berry curvature hot spots: bare vs renormalised
        XR, YR = (-np.pi, np.pi), (-2.6, 2.6)
        xs = np.linspace(*XR, 420)
        ys = np.linspace(*YR, 350)
        KX, KY = np.meshgrid(xs, ys)
        mL = kspace_axes(5.6, 5.6 * (YR[1] - YR[0]) / (XR[1] - XR[0]), xr=XR, yr=YR, labels=False).shift(3.3 * LEFT + 0.4 * DOWN)
        mR = kspace_axes(5.6, 5.6 * (YR[1] - YR[0]) / (XR[1] - XR[0]), xr=XR, yr=YR, labels=False).shift(3.3 * RIGHT + 0.4 * DOWN)
        clip = 0.6
        imL = image_on_axes(signed_rgba(berry(KX, KY), clip, gamma=1.0), mL, XR, YR)
        dy = ValueTracker(1.0)
        imR = image_on_axes(signed_rgba(berry(KX, KY), clip, gamma=1.0), mR, XR, YR)
        imR.add_updater(lambda m: m.__setattr__('pixel_array', signed_rgba(berry(KX, KY, Dy=dy.get_value()), clip, gamma=1.0)))
        tL = zh('裸能带', 28).next_to(mL, UP, buff=0.2)
        tR = VGroup(zh('重整化后', 28), MathTex(r'D_y^{\rm eff}=', font_size=32),
                    DecimalNumber(1.0, num_decimal_places=3, font_size=32)).arrange(RIGHT, buff=0.12).next_to(mR, UP, buff=0.2)
        tR[2].add_updater(lambda m: m.set_value(dy.get_value()))
        note = VGroup(zh('示意：取', 18, GREY_C), MathTex(r'D_y^{\rm eff} = 0.985', font_size=22, color=GREY_C)).arrange(RIGHT, buff=0.08).to_corner(UR, buff=0.2)
        with self.narrate('ia4') as b:
            self.play(FadeIn(imL), FadeIn(imR), FadeIn(frame_box(mL, XR, YR)), FadeIn(frame_box(mR, XR, YR)),
                      FadeIn(tL), FadeIn(tR), FadeIn(note), run_time=1.0)
            self.play(dy.animate.set_value(DYE), run_time=2.0)
            self.play(*[Flash(mR.c2p(sg * NODE, 0), color=C_HOT, flash_radius=0.45) for sg in (-1, 1)], run_time=1.0)
        imR.clear_updaters()
        tR[2].clear_updaters()
        with self.narrate('ia5') as b:
            f = MathTex(r'D_y^{\rm eff} = D_y - \mathrm{Re}\,\Sigma^R_z(0)', font_size=44).to_edge(UP, buff=0.35)
            self.play(Write(f), run_time=1.5)
            ok = zh('无相互作用有效模型：在百分之几内重现电声结果（E ≲ 0.1）', 26, C_J).to_edge(DOWN, buff=0.35)
            b.wait_sentence(0)
            self.play(FadeIn(ok, shift=0.2 * UP), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)


class S11_Summary(NScene):
    def construct(self):
        t = zh('总结', 44, weight=BOLD).to_edge(UP, buff=0.5)
        with self.narrate('sum1') as b:
            self.play(Write(t), run_time=1.0)
        items = [
            ('1', '贝里曲率偶极子图像：只在大掺杂、弱电场下可控', C_J),
            ('2', '费米面边缘到达热点，或带间转移变得重要时失效；\n贝里曲率加权占据公式也不再可靠', C_BOX1),
            ('3', '非平衡稳态格林函数：非微扰计算完整霍尔电流；\n耗散、相互作用、电声耦合通过自能与能带重整化改变热点', C_BOX2),
        ]
        rows = VGroup()
        for n, txt, c in items:
            num = VGroup(Circle(radius=0.3, color=c, stroke_width=3), Text(n, font_size=30, color=c))
            body = zh(txt, 28, line_spacing=0.9)
            rows.add(VGroup(num, body).arrange(RIGHT, buff=0.4, aligned_edge=UP))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(t, DOWN, buff=0.6).set_x(0)
        for key, row in zip(['sum2', 'sum3', 'sum4'], rows):
            with self.narrate(key) as b:
                self.play(FadeIn(row[0], scale=1.5), FadeIn(row[1], shift=0.2 * RIGHT), run_time=1.2)
        with self.narrate('sum5') as b:
            self.play(FadeOut(rows), FadeOut(t), run_time=0.8)
            ref = VGroup(Text('L. Geng, M. Eckstein, L. Chen, S. Sur, S. Paschen, Q. Si, P. Werner', font_size=24),
                         Text('Nonperturbative Nonlinear Hall Effect in Nonequilibrium Steady States', font_size=26,
                              color=BLUE_B),
                         Text('arXiv:2607.01519', font_size=24, color=GREY_B)).arrange(DOWN, buff=0.25)
            cred = zh('动画：Manim  ·  配音：Kokoro-82M（本地）  ·  部分数据按论文方法重新计算', 20, GREY_C)
            cred.to_edge(DOWN, buff=0.5)
            self.play(FadeIn(ref, shift=0.2 * UP), run_time=1.2)
            self.play(FadeIn(cred), run_time=0.8)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
