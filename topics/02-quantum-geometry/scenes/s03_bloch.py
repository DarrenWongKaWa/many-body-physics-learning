import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

KR = 1.2   # k-space window [-KR, KR]^2


def dmod(kx, ky, s):
    """s = 0: atomic insulator (every k is pure alpha). s = 1: band inversion around |k| ~ 0.67."""
    return np.array([s * kx, s * ky, 1 - s * 2.2 * (kx ** 2 + ky ** 2)])


def nmod(kx, ky, s):
    d = dmod(kx, ky, s)
    return d / np.linalg.norm(d)


def orb_color(nz):
    return interpolate_color(ManimColor(C_B), ManimColor(C_A), (nz + 1) / 2)


def orbital_alpha(r=0.42):
    c = Circle(radius=r, stroke_color=C_A, stroke_width=3, fill_color=C_A, fill_opacity=0.35)
    return VGroup(c, MathTex(r'|\alpha\rangle', font_size=36, color=C_A).next_to(c, DOWN, buff=0.15))


def orbital_beta(r=0.42):
    l1 = Ellipse(width=0.42, height=0.62, stroke_color=C_B, stroke_width=3, fill_color=C_B, fill_opacity=0.35).shift(0.32 * UP)
    l2 = l1.copy().shift(0.64 * DOWN).set_fill(opacity=0.15)
    g = VGroup(l1, l2)
    return VGroup(g, MathTex(r'|\beta\rangle', font_size=36, color=C_B).next_to(g, DOWN, buff=0.15))


class S03_Bloch(NScene):
    def construct(self):
        sph = Sphere2D(radius=2.0, n_merid=3).move_to([3.4, -0.3, 0])
        poles = sph.pole_labels(38)

        # ---------------- blo1: two orbitals -> Bloch sphere
        oa, ob = orbital_alpha(), orbital_beta()
        orbs = VGroup(oa, ob).arrange(RIGHT, buff=1.4).move_to([-3.6, 1.7, 0])
        two = txt('two orbitals', 32, GREY_A).next_to(orbs, UP, buff=0.35)
        sup = MathTex(r'|u\rangle', '=', r'\cos\tfrac{\theta}{2}', r'|\alpha\rangle', '+', r'e^{i\varphi}\sin\tfrac{\theta}{2}',
                      r'|\beta\rangle', font_size=40).move_to([-3.4, -0.4, 0])
        sup[3].set_color(C_A); sup[6].set_color(C_B)
        th, ph = 1.05, 0.9
        n0 = bloch_vec(th, ph)
        arr = sph.arrow(n0, color=WHITE)
        theta_arc = sph.curve([bloch_vec(t, ph) for t in np.linspace(0, th, 20)], color=YELLOW, width=3, r=0.42)
        thl = MathTex(r'\theta', font_size=32, color=YELLOW).move_to(sph.p(bloch_vec(th / 2, ph), 0.6) + 0.12 * RIGHT)
        bl = txt('Bloch sphere', 32, GREY_A).next_to(sph, UP, buff=0.55)
        with self.narrate('blo1') as b:
            self.play(FadeIn(two), FadeIn(oa, shift=0.2 * UP), FadeIn(ob, shift=0.2 * UP), run_time=1.5)
            b.wait_sentence(1)
            self.play(Write(sup), run_time=1.6)
            self.play(FadeIn(sph), FadeIn(bl), run_time=1.0)
            self.play(GrowArrow(arr), Create(theta_arc), FadeIn(thl), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(poles[0], shift=0.2 * DOWN), Indicate(oa[0], color=C_A), run_time=1.0)
            self.play(FadeIn(poles[1], shift=0.2 * UP), Indicate(ob[0], color=C_B), run_time=1.0)

        # ---------------- blo2: H = h . sigma ; n = h/|h|
        ham = MathTex(r'H(\mathbf k)', '=', r'h_0(\mathbf k) + \mathbf h(\mathbf k)\cdot\boldsymbol\sigma', font_size=42)
        nn = MathTex(r'\mathbf n(\mathbf k) = \mathbf h / |\mathbf h|', font_size=42, color=YELLOW)
        VGroup(ham, nn).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([-3.3, 0.6, 0])
        with self.narrate('blo2') as b:
            self.play(FadeOut(VGroup(two, orbs)), sup.animate.scale(0.8).move_to([-3.4, -2.6, 0]).set_opacity(0.6), run_time=1.0)
            self.play(Write(ham), run_time=1.6)
            b.wait_sentence(1)
            self.play(Write(nn), arr.animate.set_color(YELLOW), run_time=1.4)
            nl = MathTex(r'\mathbf n', font_size=36, color=YELLOW).next_to(sph.p(n0), UR, buff=0.05)
            self.play(FadeIn(nl), run_time=0.6)

        # ---------------- blo3: QGT on the sphere
        G = MathTex(r'G_{ij}', '=', r'\tfrac14\,\partial_i\mathbf n\cdot\partial_j\mathbf n', r'\pm\,\tfrac{i}{4}\,\mathbf n\cdot(\partial_i\mathbf n\times\partial_j\mathbf n)',
                    font_size=38).move_to([-3.1, 1.8, 0])
        G[2].set_color(C_G); G[3].set_color(C_POS)
        gl = MathTex(r'ds^2 = \tfrac14\,|d\mathbf n|^2', font_size=40, color=C_G)
        gt = txt('metric = $\\tfrac14\\times$ (distance on sphere)$^2$', 28, C_G)
        ol = MathTex(r'\Omega\, dk_x dk_y = \tfrac12\, d(\text{solid angle})', font_size=38, color=C_POS)
        ot = txt('curvature = $\\tfrac12\\times$ solid angle swept', 28, C_POS)
        colm = VGroup(VGroup(gl, gt).arrange(DOWN, buff=0.12, aligned_edge=LEFT),
                      VGroup(ol, ot).arrange(DOWN, buff=0.12, aligned_edge=LEFT)).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        colm.move_to([-3.3, -0.6, 0])
        n1v, n2v = bloch_vec(0.75, 0.25), bloch_vec(1.25, 0.6)
        d1_, d2_ = sph.dot(n1v, C_G), sph.dot(n2v, C_G)
        arc = sph.curve(slerp_path(n1v, n2v), color=C_G, width=6)
        c0 = bloch_vec(1.0, 1.0)
        ea = np.cross(c0, [0, 0, 1]); ea /= np.linalg.norm(ea)
        eb = np.cross(c0, ea)
        lp = [(c0 + 0.35 * (np.cos(t) * ea + np.sin(t) * eb)) for t in np.linspace(0, TAU, 60)]
        lp = [q / np.linalg.norm(q) for q in lp]
        loop = sph.curve(lp, color=C_POS, width=4)
        patch = Polygon(*[sph.p(q) for q in lp[:-1]], stroke_width=0, fill_color=C_POS, fill_opacity=0.4)
        with self.narrate('blo3') as b:
            self.play(FadeOut(VGroup(ham, nn, nl, sup, thl, theta_arc)), arr.animate.set_opacity(0.0), run_time=0.8)
            self.play(Write(G), run_time=2.4)
            b.wait_sentence(1)
            self.play(FadeIn(d1_), FadeIn(d2_), Create(arc), run_time=1.0)
            self.play(FadeIn(colm[0]), run_time=1.0)
            b.wait_sentence(2)
            self.play(Create(loop), FadeIn(patch), run_time=1.2)
            self.play(FadeIn(colm[1]), run_time=1.0)

        # ---------------- blo4 / blo5: atomic insulator vs band inversion
        s = ValueTracker(0.0)
        bax = Axes(x_range=[-KR, KR, KR], y_range=[-2.6, 2.6, 1], x_length=3.4, y_length=2.7, tips=False,
                   axis_config=dict(stroke_color=GREY_B, stroke_width=1.5, include_ticks=False)).move_to([-4.6, 1.3, 0])
        bxl = MathTex('k', font_size=28, color=GREY_B).next_to(bax.x_axis, RIGHT, buff=0.1)
        byl = MathTex('E', font_size=28, color=GREY_B).next_to(bax.y_axis, UP, buff=0.1)

        def bands():
            g = VGroup()
            ks = np.linspace(-KR, KR, 81)
            for sgn in (1, -1):
                for a, c in zip(ks[:-1], ks[1:]):
                    ea_ = np.linalg.norm(dmod(a, 0, s.get_value()))
                    ec_ = np.linalg.norm(dmod(c, 0, s.get_value()))
                    col = orb_color(sgn * nmod(0.5 * (a + c), 0, s.get_value())[2])
                    g.add(Line(bax.c2p(a, sgn * min(ea_, 2.5)), bax.c2p(c, sgn * min(ec_, 2.5)), stroke_color=col, stroke_width=4))
            return g
        band_m = always_redraw(bands)

        kax = Axes(x_range=[-KR, KR, KR], y_range=[-KR, KR, KR], x_length=2.7, y_length=2.7, tips=False,
                   axis_config=dict(stroke_color=GREY_D, stroke_width=1.2, include_ticks=False)).move_to([-4.6, -1.9, 0])
        kbox = frame_box(kax, (-KR, KR), (-KR, KR))
        klx = MathTex('k_x', font_size=26, color=GREY_B).next_to(kax, RIGHT, buff=0.1)
        kly = MathTex('k_y', font_size=26, color=GREY_B).next_to(kax, UP, buff=0.05)
        k1, k2 = (0.42, -0.1), (0.78, -0.1)
        kd1, kd2 = Dot(kax.c2p(*k1), color=C_G, radius=0.07), Dot(kax.c2p(*k2), color=C_G, radius=0.07)
        kc, kr = np.array([0.45, 0.5]), 0.24
        kloop_pts = [kc + kr * np.array([np.cos(t), np.sin(t)]) for t in np.linspace(0, TAU, 64)]
        kloop = VMobject(stroke_color=C_POS, stroke_width=3).set_points_smoothly([kax.c2p(*p) for p in kloop_pts])
        kpanel = VGroup(kax, kbox, klx, kly, kd1, kd2, kloop)

        def sph_marks():
            sv = s.get_value()
            m1, m2 = nmod(*k1, sv), nmod(*k2, sv)
            g = VGroup(sph.curve(slerp_path(m1, m2), color=C_G, width=6), sph.dot(m1, C_G, 0.08), sph.dot(m2, C_G, 0.08))
            lpts = [nmod(*p, sv) for p in kloop_pts]
            g.add(Polygon(*[sph.p(q) for q in lpts[:-1]], stroke_width=0, fill_color=C_POS, fill_opacity=0.45),
                  sph.curve(lpts, color=C_POS, width=3.5))
            return g

        def solid_angle(sv):
            # area of the image of the k-loop (spherical polygon via triangle fan from its centre)
            c = nmod(*kc, sv)
            pts = [nmod(*p, sv) for p in kloop_pts[:-1]]
            tot = 0.0
            for a, bb in zip(pts, pts[1:] + pts[:1]):
                num = np.dot(c, np.cross(a, bb))
                den = 1 + np.dot(c, a) + np.dot(a, bb) + np.dot(bb, c)
                tot += 2 * np.arctan2(num, den)
            return abs(tot)

        marks = always_redraw(sph_marks)
        dist_l = MathTex(r'\text{distance} =', font_size=34, color=C_G)
        area_l = MathTex(r'\text{area} =', font_size=34, color=C_POS)
        dist_v = always_redraw(lambda: DecimalNumber(np.arccos(np.clip(np.dot(nmod(*k1, s.get_value()), nmod(*k2, s.get_value())), -1, 1)),
                                                     num_decimal_places=2, font_size=34, color=C_G).next_to(dist_l, RIGHT, buff=0.15))
        area_v = always_redraw(lambda: DecimalNumber(solid_angle(s.get_value()), num_decimal_places=2, font_size=34,
                                                     color=C_POS).next_to(area_l, RIGHT, buff=0.15))
        readout = VGroup(dist_l, area_l).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([-0.9, 0.9, 0])
        kind = txt('atomic insulator', 34, bold=True).move_to([-4.6, 3.35, 0])
        with self.narrate('blo4') as b:
            self.play(FadeOut(VGroup(G, colm, d1_, d2_, arc, loop, patch, arr, bl)), sph.animate.shift(0.6 * RIGHT),
                      poles.animate.shift(0.6 * RIGHT), run_time=1.0)
            self.play(FadeIn(kind), Create(bax), FadeIn(bxl), FadeIn(byl), run_time=1.0)
            self.add(band_m)
            self.play(FadeIn(band_m), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(kpanel), run_time=1.0)
            self.add(marks)
            self.play(FadeIn(marks), run_time=0.6)
            b.wait_sentence(2)
            self.play(FadeIn(dist_l), FadeIn(dist_v), run_time=0.6)
            gz = MathTex(r'g = 0', font_size=38, color=C_G).next_to(readout, DOWN, buff=0.6, aligned_edge=LEFT)
            self.play(Write(gz), run_time=0.8)
            b.wait_sentence(3)
            self.play(FadeIn(area_l), FadeIn(area_v), run_time=0.6)
            oz = MathTex(r'\Omega = 0', font_size=38, color=C_POS).next_to(gz, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(oz), run_time=0.8)

        with self.narrate('blo5') as b:
            kind2 = txt('band inversion', 34, bold=True).move_to(kind)
            self.play(FadeOut(gz), FadeOut(oz), Transform(kind, kind2), run_time=0.8)
            self.play(s.animate.set_value(1.0), run_time=b.until_sentence(2, 2.0) + 1.0, rate_func=smooth)
            self.play(Indicate(dist_v, color=C_G), run_time=0.8)
            gl2 = MathTex(r'g\ \text{large}', font_size=38, color=C_G).next_to(readout, DOWN, buff=0.6, aligned_edge=LEFT)
            self.play(Write(gl2), run_time=0.8)
            b.wait_sentence(3)
            self.play(Indicate(area_v, color=C_POS), run_time=0.8)
            ol2 = MathTex(r'\Omega\ \text{large}', font_size=38, color=C_POS).next_to(gl2, DOWN, buff=0.3, aligned_edge=LEFT)
            self.play(Write(ol2), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
