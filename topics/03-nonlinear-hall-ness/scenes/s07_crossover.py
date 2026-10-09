import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

XR, YR = (-2.2, 2.2), (-1.25, 1.25)
GAM = 0.1
EDGE = -np.arccos(0.2)          # outer Fermi edge of the left pocket (ky = 0)


class OccMaps:
    """Steady-state occupation Tr n(kappa) from data/maps.npz, interpolated in E."""

    def __init__(self, mu_index, transform=lambda a: a):
        d = load('maps.npz')
        kx, ky = d['kxs'], d['kys']
        ix = (kx >= XR[0]) & (kx <= XR[1])
        iy = (ky >= YR[0]) & (ky <= YR[1])
        self.kx, self.ky = kx[ix], ky[iy]
        mu = float(d['mus'][mu_index])
        KX, KY = np.meshgrid(self.kx, self.ky)
        npl, nmi = n_eq(KX, KY, mu, GAM)
        eq = (npl + nmi)[None]
        occ = d['occ'][:, mu_index][:, iy][:, :, ix]
        self.E = np.r_[0.0, d['E']]
        self.maps = transform(np.concatenate([eq, occ], 0))
        self.JyE = np.r_[0.0, d['JyE'][:, mu_index]]

    def at(self, E):
        i = int(np.clip(np.searchsorted(self.E, E) - 1, 0, len(self.E) - 2))
        w = np.clip((E - self.E[i]) / (self.E[i + 1] - self.E[i]), 0, 1)
        return (1 - w) * self.maps[i] + w * self.maps[i + 1]


class S07_Crossover(NScene):
    def construct(self):
        om = OccMaps(1)
        cmap = matplotlib.colormaps['magma']
        vmin, vmax = 0.95, float(np.percentile(om.maps[: np.searchsorted(om.E, 0.08)], 99.7))
        Et = ValueTracker(0.0)

        ax = Axes(x_range=[*XR, 1], y_range=[*YR, 0.5], x_length=6.6, y_length=6.6 * 2.5 / 4.4, tips=False,
                  axis_config=dict(include_ticks=False, stroke_color=GREY_B, stroke_width=1))
        ax.to_edge(LEFT, buff=0.5).shift(0.5 * UP)
        img = image_on_axes(rgba_from(om.at(0), cmap, vmin, vmax), ax, XR, YR)
        img.add_updater(lambda m: m.__setattr__('pixel_array', rgba_from(om.at(Et.get_value()), cmap, vmin, vmax)))
        box = frame_box(ax, XR, YR)
        xs = np.linspace(*XR, 400)
        ys = np.linspace(*YR, 240)
        KX, KY = np.meshgrid(xs, ys)
        fs = contour_mobject(ax, eps(KX, KY), xs, ys, 0.3, color=WHITE, width=2.5)
        nodes = node_marks(ax, 0.08, color=WHITE)
        title = VGroup(MathTex(r'\mathrm{Tr}\,\tilde n(\boldsymbol\kappa)', font_size=34),
                       MathTex(r'\mu = 0.3,\ \Gamma = 0.1', font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.4)
        title.next_to(box, UP, buff=0.2)
        kl = VGroup(MathTex(r'\kappa_x', font_size=28, color=GREY_B).next_to(box, DOWN, buff=0.1),
                    MathTex(r'\kappa_y', font_size=28, color=GREY_B).next_to(box, LEFT, buff=0.1))
        # Delta kappa_x markers (as in the paper's Fig. 2a)
        dl = VGroup(*[DashedLine(ax.c2p(x, YR[0]), ax.c2p(x, 0), color=WHITE, stroke_width=2) for x in (EDGE, -NODE)])
        br = BraceBetweenPoints(ax.c2p(EDGE, -0.75), ax.c2p(-NODE, -0.75), DOWN, color=WHITE)
        dkl = MathTex(r'\Delta\kappa_x = 0.3222', font_size=30).next_to(br, DOWN, buff=0.05).shift(0.3 * RIGHT)

        with self.narrate('cro1') as b:
            self.play(FadeIn(img), Create(box), FadeIn(title), FadeIn(kl), run_time=1.5)
            self.play(Create(fs), FadeIn(nodes), run_time=1.2)
            b.wait_sentence(1)
            self.play(Create(dl), GrowFromCenter(br), Write(dkl), run_time=1.5)

        # right panel: Jy/E vs E (mu = 0.3, Gamma = 0.1)
        d1 = load('fig1b.npz')
        Eg = np.r_[0, d1['E']]
        Jg = np.r_[0, d1['JyE'][:, list(d1['mus']).index(0.30)]] * 1e4
        sel = Eg <= 0.0801
        pax = Axes(x_range=[0, 0.08, 0.02], y_range=[0, 5, 1], x_length=5.2, y_length=3.6, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                    decimal_number_config=dict(num_decimal_places=2)),
                   y_axis_config=dict(decimal_number_config=dict(num_decimal_places=0)))
        pax.to_edge(RIGHT, buff=0.55).shift(0.5 * UP)
        pyl = MathTex(r'J_y/E\ (\times10^{-4})', font_size=26).next_to(pax, UP, buff=0.15)
        pxl = MathTex('E', font_size=28).next_to(pax.x_axis, DOWN, buff=0.35)
        curve = pax.plot_line_graph(Eg[sel], Jg[sel], add_vertex_dots=False, line_color=BLUE_B, stroke_width=3.5)
        tracer = always_redraw(lambda: Dot(pax.c2p(Et.get_value(), np.interp(Et.get_value(), Eg, Jg)),
                                           color=C_E, radius=0.08))
        Eread = VGroup(MathTex('E =', font_size=34), DecimalNumber(0, num_decimal_places=4, font_size=34),
                       MathTex(r'\quad E/\Gamma =', font_size=34), DecimalNumber(0, num_decimal_places=3, font_size=34))
        Eread.arrange(RIGHT, buff=0.12)
        Eread[2:].shift(0.35 * RIGHT)
        Eread.next_to(box, DOWN, buff=0.7)
        Eread[1].add_updater(lambda m: m.set_value(Et.get_value()))
        Eread[3].add_updater(lambda m: m.set_value(Et.get_value() / GAM))
        drift = always_redraw(lambda: Arrow(ax.c2p(EDGE, -1.05), ax.c2p(EDGE + max(Et.get_value() / GAM, 1e-3), -1.05),
                                            buff=0, color=C_E, stroke_width=5, max_tip_length_to_length_ratio=0.25,
                                            max_stroke_width_to_length_ratio=40))
        with self.narrate('cro2') as b:
            self.play(Create(pax), FadeIn(pyl), FadeIn(pxl), Create(curve), FadeIn(Eread), run_time=1.5)
            self.add(tracer, drift)
            b.wait_sentence(1)
            self.play(Et.animate.set_value(0.022), run_time=max(0.5, b.remaining() - 0.5), rate_func=smooth)

        with self.narrate('cro3') as b:
            self.play(Et.animate.set_value(0.0322), run_time=3.0, rate_func=smooth)
            hot = Circle(radius=0.3, color=C_HOT, stroke_width=5).move_to(ax.c2p(-NODE, 0))
            self.play(Create(hot), Flash(ax.c2p(-NODE, 0), color=C_HOT, flash_radius=0.4), run_time=1.0)
            vline = DashedLine(pax.c2p(0.0322, 0), pax.c2p(0.0322, 5), color=C_BOX1, stroke_width=3)
            self.play(Create(vline), run_time=0.8)
            b.wait_sentence(2)
            estar = MathTex(r'E^* \approx \Gamma\,\Delta\kappa_x = 0.0322', font_size=40, color=C_BOX1)
            estar.next_to(Eread, DOWN, buff=0.4)
            self.play(Write(estar), run_time=1.5)
            self.play(Et.animate.set_value(0.06), run_time=max(1.0, b.remaining() - 0.4), rate_func=smooth)

        # Gamma check (paper Fig. 1c, recomputed)
        d2 = load('fig1c.npz')
        G = d2['Gam']
        E2 = np.r_[0, d2['E']]
        J2 = np.c_[np.zeros(len(G)), d2['JyE']] * 1e4
        oranges = [rgb_to_color(matplotlib.colormaps['Oranges'](0.3 + 0.7 * i / (len(G) - 1))[:3]) for i in range(len(G))]
        qax = Axes(x_range=[0, 0.08, 0.02], y_range=[0, 5, 1], x_length=5.2, y_length=3.6, tips=False,
                   axis_config=dict(stroke_color=GREY_B, include_numbers=True, font_size=22,
                                    decimal_number_config=dict(num_decimal_places=2)),
                   y_axis_config=dict(decimal_number_config=dict(num_decimal_places=0))).move_to(pax)
        gcurves = VGroup(*[qax.plot_line_graph(E2, J2[i], add_vertex_dots=False, line_color=oranges[i], stroke_width=3)
                           for i in range(len(G))])
        Es = np.array(G) * DKX
        dots = VGroup(*[Dot(qax.c2p(e, np.interp(e, E2, J2[i])), color=WHITE, radius=0.07) for i, e in enumerate(Es)])
        link = DashedVMobject(VMobject().set_points_as_corners([d.get_center() for d in dots]).set_stroke(WHITE, 2),
                              num_dashes=18)
        gleg = VGroup(*[VGroup(Line(ORIGIN, 0.35 * RIGHT, color=oranges[i], stroke_width=4),
                               MathTex(rf'\Gamma={g:g}', font_size=22)).arrange(RIGHT, buff=0.08)
                        for i, g in enumerate(G)]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        gleg.next_to(qax.c2p(0.08, 0), UL, buff=0.1)
        cond = MathTex(r'E/\Gamma = 0.3222', font_size=30).next_to(qax.c2p(0.0, 5), DR, buff=0.15)
        with self.narrate('cro4') as b:
            tracer.clear_updaters()
            self.play(FadeOut(VGroup(curve, tracer, vline)), ReplacementTransform(pax, qax), run_time=1.0)
            self.play(LaggedStart(*[Create(c) for c in gcurves], lag_ratio=0.2), FadeIn(gleg), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.2), run_time=1.5)
            self.play(Create(link), FadeIn(cond), run_time=1.5)
        img.clear_updaters()
        drift.clear_updaters()
        for m in Eread:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
