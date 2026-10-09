import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S05_Method(NScene):
    def construct(self):
        q = zh('如何非微扰地描述被恒定电场驱动的晶格？', 38)
        with self.narrate('met1') as b:
            self.play(Write(q), run_time=2.0)
        self.play(q.animate.scale(0.7).to_edge(UP, buff=0.3), run_time=0.8)

        # ---------------- Bloch oscillation: k sweeps the Brillouin zone
        ax = Axes(x_range=[-np.pi, np.pi, np.pi], y_range=[-1.4, 1.4, 1], x_length=7, y_length=3.2, tips=False,
                  axis_config=dict(include_ticks=False, stroke_color=GREY_B)).shift(0.2 * DOWN)
        band = ax.plot(lambda k: -np.cos(k), x_range=[-np.pi, np.pi], color=WHITE, stroke_width=4)
        xl = MathTex('k', font_size=34).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = MathTex(r'\varepsilon', font_size=34).next_to(ax.y_axis, UP, buff=0.1)
        bzl = VGroup(MathTex(r'-\pi', font_size=28).next_to(ax.c2p(-np.pi, -1.4), DOWN, buff=0.1),
                     MathTex(r'\pi', font_size=28).next_to(ax.c2p(np.pi, -1.4), DOWN, buff=0.1))
        walls = VGroup(DashedLine(ax.c2p(-np.pi, -1.4), ax.c2p(-np.pi, 1.4), color=GREY_C),
                       DashedLine(ax.c2p(np.pi, -1.4), ax.c2p(np.pi, 1.4), color=GREY_C))
        t = ValueTracker(0.0)
        Ev = 1.6

        def kpos():
            return (-2.4 + Ev * t.get_value() + np.pi) % (2 * np.pi) - np.pi
        dot = always_redraw(lambda: Dot(ax.c2p(kpos(), -np.cos(kpos())), radius=0.12, color=C_ELEC))
        kt = MathTex(r'k(t) = k_0 + E\,t', font_size=40).next_to(ax, UP, buff=0.35)
        Ear = Arrow(ax.c2p(-1.2, 1.75), ax.c2p(1.2, 1.75), color=C_E, buff=0).next_to(kt, DOWN, buff=0.05)
        with self.narrate('met2') as b:
            self.play(Create(ax), Create(band), FadeIn(xl), FadeIn(yl), FadeIn(bzl), FadeIn(walls), run_time=1.5)
            self.add(dot)
            self.play(Write(kt), run_time=1.0)
            self.play(t.animate.set_value(b.dur * 0.62), run_time=b.dur * 0.62 - 2.5, rate_func=linear)
            nodiss = zh('没有耗散：电场做的功无处释放  →  没有稳态', 30, C_HOT).to_edge(DOWN, buff=0.5)
            self.play(FadeIn(nodiss), t.animate.increment_value(3.0), run_time=b.remaining() if b.remaining() > 0.5 else 0.5,
                      rate_func=linear)
        dot.clear_updaters()
        self.play(FadeOut(VGroup(ax, band, xl, yl, bzl, walls, dot, kt, nodiss)), run_time=0.7)

        # ---------------- lattice coupled to fermionic reservoirs
        n = 7
        sites = VGroup(*[Dot([x, 0.9, 0], radius=0.14, color=C_ELEC) for x in np.linspace(-4.2, 4.2, n)])
        bonds = VGroup(*[Line(sites[i].get_center(), sites[i + 1].get_center(), color=GREY_B, stroke_width=3)
                         for i in range(n - 1)])
        baths = VGroup()
        links = VGroup()
        for s in sites:
            r = RoundedRectangle(corner_radius=0.12, width=0.9, height=0.6, fill_color='#3a1e1e', fill_opacity=1,
                                 stroke_color=C_POS, stroke_width=1.5).move_to(s.get_center() + 2.0 * DOWN)
            baths.add(r)
            pts = [s.get_center() + DOWN * (0.15 + 0.12 * k) + RIGHT * 0.1 * np.sin(k * 1.6) for k in range(13)]
            links.add(VMobject(stroke_color=GREY_B, stroke_width=2).set_points_smoothly(pts))
        bl = zh('费米子热库', 26, C_POS).next_to(baths, DOWN, buff=0.25)
        sig = MathTex(r'\Sigma^R_{\rm bath} = -i\Gamma', font_size=36).next_to(bl, RIGHT, buff=0.8)
        Ear2 = Arrow(LEFT * 3, RIGHT * 3, color=C_E, buff=0).move_to(UP * 2.35)
        El2 = MathTex(r'\mathbf E', color=C_E, font_size=36).next_to(Ear2, RIGHT, buff=0.1)
        with self.narrate('met3') as b:
            self.play(LaggedStartMap(FadeIn, sites, lag_ratio=0.1), Create(bonds), GrowArrow(Ear2), FadeIn(El2),
                      run_time=1.5)
            self.play(LaggedStartMap(Create, links, lag_ratio=0.08), LaggedStartMap(FadeIn, baths, lag_ratio=0.08),
                      FadeIn(bl), run_time=2.0)
            self.play(Write(sig), run_time=1.0)
            b.wait_sentence(2)
            inflow = VGroup(*[Arrow(UP * 2.1 + RIGHT * x, UP * 1.2 + RIGHT * x, color=C_E, buff=0, stroke_width=4)
                              for x in (-2.8, 0, 2.8)])
            outflow = VGroup(*[Arrow(s.get_center() + 0.45 * DOWN + 0.35 * RIGHT, s.get_center() + 1.55 * DOWN + 0.35 * RIGHT,
                                     color=C_POS, buff=0, stroke_width=4) for s in sites[::2]])
            il = zh('能量注入', 24, C_E).next_to(inflow[2], RIGHT, buff=0.1)
            ol = zh('耗散', 24, C_POS).next_to(outflow[-1], RIGHT, buff=0.1)
            self.play(LaggedStart(*[GrowArrow(a) for a in inflow], lag_ratio=0.2), FadeIn(il), run_time=1.2)
            self.play(LaggedStart(*[GrowArrow(a) for a in outflow], lag_ratio=0.15), FadeIn(ol), run_time=1.2)
            ness = VGroup(zh('注入 = 耗散', 30), MathTex(r'\Rightarrow', font_size=36), zh('非平衡稳态', 30, C_J)
                          ).arrange(RIGHT, buff=0.2).to_edge(DOWN, buff=0.3)
            self.play(FadeIn(ness, shift=0.2 * UP), run_time=1.0)
        lattice = VGroup(sites, bonds, baths, links, bl, sig, Ear2, El2, inflow, outflow, il, ol, ness)
        self.play(FadeOut(lattice), run_time=0.7)

        # ---------------- drift + relaxation: occupation shifts by E/Gamma
        kax = NumberLine(x_range=[-3, 3, 1], length=10, include_ticks=False, color=GREY_B).shift(0.2 * DOWN)
        kxl = MathTex(r'\kappa_x', font_size=34).next_to(kax, RIGHT, buff=0.15)
        rng = np.random.default_rng(3)
        N, kF, Gam = 360, 1.0, 1.0
        state = dict(k=rng.uniform(-kF, kF, N), y=rng.uniform(0, 1, N), E=0.0)
        dots = VGroup(*[Dot(radius=0.03, color=C_ELEC) for _ in range(N)])
        unit = kax.get_unit_size()
        nb = 30
        edges = np.linspace(-3, 3, nb + 1)

        def upd_dots(m, dt):
            k = state['k']
            k += state['E'] * dt
            reset = rng.random(N) < Gam * dt
            k[reset] = rng.uniform(-kF, kF, reset.sum())
            state['y'][reset] = rng.uniform(0, 1, reset.sum())
            for d, kk, yy in zip(m, k, state['y']):
                d.move_to(kax.n2p(kk) + UP * (0.15 + 0.9 * yy))
        dots.add_updater(upd_dots)

        def hist():
            h, _ = np.histogram(state['k'], edges)
            g = VGroup()
            for i, c in enumerate(h):
                hh = 1.6 * c / (N * (edges[1] - edges[0]) / (2 * kF))
                if hh > 0:
                    g.add(Rectangle(width=unit * (edges[1] - edges[0]) * 0.92, height=hh, fill_color=BLUE_D,
                                    fill_opacity=0.65, stroke_width=0)
                          .move_to(kax.n2p(0.5 * (edges[i] + edges[i + 1])) + DOWN * (0.1 + hh / 2)))
            return g
        hg = always_redraw(hist)
        eqf = VGroup(MathTex(r'\kappa(t) = \kappa_0 + E\,t', font_size=36),
                     VGroup(zh('寿命', 28), MathTex(r'\sim 1/\Gamma', font_size=36)).arrange(RIGHT, buff=0.1),
                     MathTex(r'\Delta\kappa \approx E/\Gamma', font_size=40, color=C_J)).arrange(RIGHT, buff=0.9)
        eqf.to_edge(DOWN, buff=0.45)
        with self.narrate('met4') as b:
            self.play(Create(kax), FadeIn(kxl), FadeIn(dots), run_time=1.0)
            self.add(hg)
            self.play(FadeIn(eqf[0]), run_time=0.6)
            state['E'] = 0.6
            self.wait(1.8)
            self.play(FadeIn(eqf[1]), run_time=0.6)
            self.wait(max(0.1, b.sentence_start(2) - b.elapsed()))
            arr = Arrow(kax.n2p(0) + UP * 1.45, kax.n2p(0.6) + UP * 1.45, buff=0, color=C_J, stroke_width=5,
                        max_tip_length_to_length_ratio=0.35)
            zero = DashedLine(kax.n2p(0) + DOWN * 1.9, kax.n2p(0) + UP * 1.6, color=GREY_C)
            self.play(FadeIn(eqf[2]), GrowArrow(arr), Create(zero), run_time=1.2)
        dots.clear_updaters()
        hg.clear_updaters()
        self.play(FadeOut(VGroup(kax, kxl, dots, hg, eqf, arr, zero)), run_time=0.7)

        # ---------------- NEGF in the Wigner representation
        e1 = MathTex(r'(A\star B)(\omega,\boldsymbol\kappa) = A\,\exp\!\Big[\tfrac{i}{2}\,\mathbf E\cdot'
                     r'\big(\overleftarrow{\partial_\omega}\overrightarrow{\nabla_{\boldsymbol\kappa}}'
                     r'-\overleftarrow{\nabla_{\boldsymbol\kappa}}\overrightarrow{\partial_\omega}\big)\Big]\,B',
                     font_size=38)
        e2 = MathTex(r'\big[\omega + i\Gamma - H(\boldsymbol\kappa)\big]\star G^R = 1', r'\qquad',
                     r'G^< = G^R\star\Sigma^<\star G^A', font_size=38)
        e3 = MathTex(r'G^R(\tau,\boldsymbol\kappa) = -i\theta(\tau)\,e^{-\Gamma\tau}\,'
                     r'\mathcal T\exp\!\Big[-i\!\int_{-\tau/2}^{\tau/2}\! d\tau\,'
                     r'H(', r'\boldsymbol\kappa + \mathbf E\tau', r')\Big]', font_size=38)
        eqs = VGroup(e1, e2, e3).arrange(DOWN, buff=0.55).shift(0.1 * DOWN)
        tags = VGroup(zh('维格纳表象', 24, GREY_A), zh('莫亚尔星积', 24, GREY_A), zh('规范协变动量 κ', 24, GREY_A)
                      ).arrange(RIGHT, buff=0.6).next_to(eqs, UP, buff=0.4)
        with self.narrate('met5') as b:
            self.play(FadeIn(tags[0]), Write(e1), run_time=2.5)
            self.play(FadeIn(tags[1]), run_time=0.5)
            b.wait_sentence(1)
            self.play(FadeIn(tags[2]), Write(e2), run_time=2.5)
            self.play(Write(e3), run_time=2.5)
            self.play(e3[2].animate.set_color(C_E), Circumscribe(e3[2], color=C_E), run_time=1.2)
            nopow = zh('不按电场的幂次展开', 28, C_J).to_edge(DOWN, buff=0.45)
            self.play(FadeIn(nopow, shift=0.2 * UP), run_time=0.8)
        self.play(FadeOut(VGroup(eqs, tags, nopow)), run_time=0.6)

        n_eq = MathTex(r'\tilde n(\boldsymbol\kappa) = -i\,G^<(\tau = 0,\boldsymbol\kappa)', font_size=42)
        j_eq = MathTex(r'J_y = \int_{\rm BZ}\frac{d^2\kappa}{(2\pi)^2}\,\mathrm{Tr}\big[v_y(\boldsymbol\kappa)\,'
                       r'\tilde n(\boldsymbol\kappa)\big]', font_size=46)
        v_eq = MathTex(r'v_y = \partial H/\partial\kappa_y', font_size=34, color=GREY_A)
        VGroup(n_eq, j_eq, v_eq).arrange(DOWN, buff=0.5)
        with self.narrate('met6') as b:
            self.play(Write(n_eq), run_time=1.5)
            self.play(Write(j_eq), run_time=2.0)
            self.play(FadeIn(v_eq), Circumscribe(j_eq, color=C_J), run_time=1.5)
        self.play(FadeOut(VGroup(n_eq, v_eq)), j_eq.animate.scale(0.75).next_to(q, DOWN, buff=0.35), run_time=0.8)

        # ---------------- comparison table
        rows = ['带间量子相干', '准粒子近似', '频率依赖的自能（相互作用 / 电声）', '电场']
        left = [r'\times', zh('需要', 26), MathTex(r'\times', color=RED), zh('半经典', 26)]
        right = [r'\checkmark', zh('不需要', 26, C_J), MathTex(r'\checkmark', color=GREEN), zh('非微扰', 26, C_J)]
        hdr = VGroup(zh('', 26), zh('玻尔兹曼方程', 28, GREY_A), zh('非平衡稳态格林函数', 28, C_J))
        table = VGroup()
        for name, l, r in zip(rows, left, right):
            lm = MathTex(l, color=RED) if isinstance(l, str) else l
            rm = MathTex(r, color=GREEN) if isinstance(r, str) else r
            table.add(VGroup(zh(name, 26), lm, rm))
        grid = VGroup(hdr, *table)
        xs = [-3.6, 0.6, 4.0]
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 0.9 - 0.8 * i, 0])
        rules = VGroup(Line([-5.8, 0.5, 0], [5.8, 0.5, 0], color=GREY_D))
        with self.narrate('met7') as b:
            self.play(FadeIn(hdr), Create(rules), run_time=1.0)
            for row in table:
                self.play(FadeIn(row, shift=0.15 * UP), run_time=0.7)
                self.wait(0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
