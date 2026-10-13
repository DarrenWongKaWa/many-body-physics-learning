import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

K0 = np.array([1.84, 0.56])          # face-up sample momentum (front of the sphere, anisotropic metric)
K1 = np.array([2.92, 2.97])          # flipped sample momentum near M
EL, AZ = 0.38, 0.5
SPH_C, SPH_R = np.array([-0.4, -0.55, 0]), 2.35
INS_C = np.array([4.75, 0.95, 0])     # inset centre (tangent-plane close-up)


def jac(k):
    """n(k0) and the derivatives dn/dkx, dn/dky."""
    h = 1e-5
    n0 = qwz_n(*k)
    a = (qwz_n(k[0] + h, k[1]) - qwz_n(k[0] - h, k[1])) / (2 * h)
    b = (qwz_n(k[0], k[1] + h) - qwz_n(k[0], k[1] - h)) / (2 * h)
    return n0, a, b


def tangent_basis(n0):
    t1 = np.cross([0, 0, 1.0], n0)
    if np.linalg.norm(t1) < 1e-6:
        t1 = np.array([1.0, 0, 0])
    t1 /= np.linalg.norm(t1)
    t2 = np.cross(n0, t1)              # (t1, t2, n0) right-handed: the plane as seen from outside
    return t1, t2


def inset_frame(center, w=3.6, h=2.6, label=''):
    box = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=GREY_C, stroke_width=1.5,
                           fill_color=C_PANEL, fill_opacity=0.9).move_to(center)
    lab = txt(label, 24, GREY_A).next_to(box, UP, buff=0.1)
    return VGroup(box, lab)


class S05_Zoom(NScene):
    def construct(self):
        tag = txt('[H2]', 26, GREY_T).to_corner(UL, buff=0.4)
        title = txt('Zoom in', 40, bold=True).to_edge(UP, buff=0.35)
        ax, bz = bz_axes(2.9, center=[-5.1, 1.0, 0])
        cols, _ = cell_orient(24)
        bg = bz_cells(ax, 24, cols, opacity=0.28, stroke=None, width=0)
        sph = Sphere2D(radius=SPH_R, el=EL, az=AZ, n_merid=3).move_to(SPH_C)
        cam = Cam(EL, AZ, SPH_R, SPH_C)
        n0, a, b = jac(K0)
        t1, t2 = tangent_basis(n0)

        # ---------------- zoo1: small circle -> small ellipse
        rc = 0.42
        th = np.linspace(0, TAU, 160)
        circ_k = np.stack([K0[0] + rc * np.cos(th), K0[1] + rc * np.sin(th)], 1)
        kcirc = VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly([ax.c2p(*p) for p in circ_k])
        img = sph.curve([qwz_n(*p) for p in circ_k], color=WHITE, width=3.5)
        kd = Dot(ax.c2p(*K0), radius=0.05, color=WHITE)
        sd = sph.dot(n0, WHITE, 0.06)
        ph = ValueTracker(0.0)
        mk = always_redraw(lambda: Dot(ax.c2p(K0[0] + rc * np.cos(ph.get_value()), K0[1] + rc * np.sin(ph.get_value())),
                                       radius=0.06, color=YELLOW))
        ms = always_redraw(lambda: sph.dot(qwz_n(K0[0] + rc * np.cos(ph.get_value()), K0[1] + rc * np.sin(ph.get_value())),
                                           YELLOW, 0.07))
        with self.narrate('zoo1') as bt:
            self.play(FadeIn(tag), Write(title), FadeIn(bz), FadeIn(bg), FadeIn(sph), run_time=1.2)
            self.play(FadeIn(kd), FadeIn(sd), run_time=0.4)
            bt.wait_sentence(1)
            self.add(mk, ms)
            self.play(Create(kcirc), Create(img), ph.animate.set_value(TAU), run_time=bt.remaining(-0.2), rate_func=linear)

        # ---------------- zoo2: the ellipse is the metric; its axes
        g0 = qwz_geom(*K0)[1]
        lam, V = np.linalg.eigh(g0)
        long_k, short_k = V[:, 1], V[:, 0]
        axl = VGroup()
        for vec, col in ((long_k, YELLOW), (short_k, C_G)):
            seg = np.stack([K0 + s_ * rc * vec for s_ in np.linspace(-1, 1, 30)])
            axl.add(Line(ax.c2p(*seg[0]), ax.c2p(*seg[-1]), color=col, stroke_width=3),
                    sph.curve([qwz_n(*p) for p in seg], color=col, width=4))
        metric = MathTex(r'ds^2 = g_{ij}\,\delta k^i \delta k^j', font_size=32, color=C_G)
        gdef = MathTex(r'g_{ij} = \tfrac14\,\partial_i\mathbf n\cdot\partial_j\mathbf n', font_size=32, color=C_G)
        eig = MathTex(r'g = \lambda_1 e_1e_1^{\mathsf T} + \lambda_2 e_2e_2^{\mathsf T}', font_size=28)
        ellf = MathTex(r'\text{circle: }\ \delta\mathbf k = \varepsilon(\cos t\, e_1 + \sin t\, e_2)', font_size=25)
        mcol = VGroup(metric, gdef, eig, ellf).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to([-4.85, -1.9, 0])
        fast = txt('long axis: fastest change of the state', 24, YELLOW).next_to(mcol, DOWN, buff=0.25)
        # inset: the ellipse in the tangent plane (seen from outside), enlarged
        F = 5.2
        ins = inset_frame(INS_C, label='close-up of the tangent plane')
        Jt = 0.5 * np.array([[a @ t1, b @ t1], [a @ t2, b @ t2]])          # radius-1/2 sphere
        ell_pts = [INS_C + F * rc * np.array([*(Jt @ np.array([np.cos(t), np.sin(t)])), 0]) for t in th]
        ell = VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly(ell_pts)
        sq_l = VGroup(MathTex(r'\sqrt{\lambda_1}', font_size=26, color=YELLOW), MathTex(r'\sqrt{\lambda_2}', font_size=26, color=C_G))
        e_long = INS_C + F * rc * np.array([*(Jt @ long_k), 0])
        e_short = INS_C + F * rc * np.array([*(Jt @ short_k), 0])
        ins_ax = VGroup(Line(2 * INS_C - e_long, e_long, color=YELLOW, stroke_width=3), Line(2 * INS_C - e_short, e_short, color=C_G, stroke_width=3))
        # semi-axis labels outside the ellipse: beside the upper half of the long axis, beyond the right end of the short one
        up_end = e_long if e_long[1] > INS_C[1] else 2 * INS_C - e_long
        d_l = (up_end - INS_C) / np.linalg.norm(up_end - INS_C)
        perp = np.array([d_l[1], -d_l[0], 0]) if d_l[1] > 0 else np.array([-d_l[1], d_l[0], 0])
        s_len = np.linalg.norm(e_short - INS_C)
        sq_l[0].move_to(INS_C + 0.55 * (up_end - INS_C) + (s_len + 0.3) * perp)
        r_end = e_short if e_short[0] > INS_C[0] else 2 * INS_C - e_short
        sq_l[1].move_to(r_end + 0.32 * (r_end - INS_C) / s_len)
        imgf = MathTex(r'\text{image: }\ \varepsilon\big(\sqrt{\lambda_1}\cos t\, f_1 + \sqrt{\lambda_2}\sin t\, f_2\big)', font_size=26)
        imgf.move_to([4.4, -0.85, 0])
        imgc = txt('$f_1, f_2$: unit vectors along the images of $e_1, e_2$', 22, GREY_A).next_to(imgf, DOWN, buff=0.15)
        with self.narrate('zoo2') as bt:
            self.play(FadeIn(ins), Create(ell), run_time=1.2)
            bt.wait_sentence(1)
            self.play(Write(metric), run_time=1.4)
            self.play(Write(gdef), run_time=1.4)
        with self.narrate('zoo2b') as bt:
            self.play(FadeIn(eig), Create(axl), Create(ins_ax), FadeIn(sq_l), run_time=1.8)
            self.play(FadeIn(ellf), FadeIn(imgf), FadeIn(imgc), run_time=1.0)
            bt.wait_sentence(1)
            self.play(FadeIn(fast), run_time=0.8)

        # ---------------- zoo3: built from dP, no phase
        h2 = MathTex(r'g_{ij} = \tfrac12\,\mathrm{tr}\big(\partial_i P\,\partial_j P\big)', font_size=40, color=C_G)
        h2.move_to([4.75, -1.25, 0])
        nophase = txt('$P$ has no phase to choose', 26, GREY_A).next_to(h2, DOWN, buff=0.2)
        with self.narrate('zoo3') as bt:
            self.play(FadeOut(mk), FadeOut(ms), FadeOut(imgf), FadeOut(imgc), run_time=0.4)
            bt.wait_sentence(1)
            self.play(Write(h2), run_time=1.8)
            self.play(FadeIn(nophase), run_time=0.8)

        # ---------------- zoo4: a small square -> an oriented parallelogram
        ds = 0.42
        sq_k = [K0 + np.array(p) * ds - ds / 2 for p in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        ksq = Polygon(*[ax.c2p(*p) for p in sq_k], stroke_color=WHITE, stroke_width=2.5, fill_color=C_UP, fill_opacity=0.5)
        edge = []
        for p, q in zip(sq_k, sq_k[1:] + sq_k[:1]):
            edge += [p + (q - p) * t for t in np.linspace(0, 1, 25)]
        par = Polygon(*[sph.p(qwz_n(*p)) for p in edge], stroke_color=WHITE, stroke_width=2.5, fill_color=C_UP, fill_opacity=0.6)
        ex_k = Arrow(ax.c2p(*sq_k[0]), ax.c2p(*sq_k[1]), buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.3)
        ey_k = Arrow(ax.c2p(*sq_k[0]), ax.c2p(*sq_k[3]), buff=0, color=C_PROP, stroke_width=4, max_tip_length_to_length_ratio=0.3)

        def circulation(corners, color=WHITE, size=0.13):
            """Arrowheads at the edge midpoints, in the order of the corners (the image of a counterclockwise walk)."""
            g = VGroup()
            for p, q in zip(corners, corners[1:] + corners[:1]):
                d = q - p
                if np.linalg.norm(d) < 1e-6:
                    continue
                d = d / np.linalg.norm(d)
                m = (p + q) / 2
                nrm = np.array([-d[1], d[0], 0])
                g.add(Polygon(m + size * d, m - 0.6 * size * d + 0.6 * size * nrm, m - 0.6 * size * d - 0.6 * size * nrm,
                              stroke_width=0, fill_color=color, fill_opacity=1))
            return g

        def inset_par(center, Jm, scale, color, head=0.13):
            o = np.asarray(center, float) - scale * ds * np.array([*(Jm @ np.array([0.5, 0.5])), 0])
            vx = scale * ds * np.array([*(Jm @ np.array([1.0, 0.0])), 0])
            vy = scale * ds * np.array([*(Jm @ np.array([0.0, 1.0])), 0])
            poly = Polygon(o, o + vx, o + vx + vy, o + vy, stroke_color=WHITE, stroke_width=2, fill_color=color, fill_opacity=0.65)
            ar = VGroup(Arrow(o, o + vx, buff=0, color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.25),
                        Arrow(o, o + vy, buff=0, color=C_PROP, stroke_width=5, max_tip_length_to_length_ratio=0.25))
            return VGroup(poly, ar, circulation([o, o + vx, o + vx + vy, o + vy], size=head))
        par_in = inset_par(INS_C, Jt, F, C_UP)
        area = MathTex(r'\text{area} = \sqrt{\det g}\;\delta k_x\,\delta k_y', font_size=34).move_to([-5.1, -1.1, 0])
        detg = MathTex(r'\det g = \lambda_1\lambda_2', font_size=32).next_to(area, DOWN, buff=0.2)
        sq_c = [ax.c2p(*p) for p in sq_k]
        kcirc_ar = circulation(sq_c, size=0.07)
        legend_e = VGroup(VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=YELLOW, stroke_width=4), MathTex(r'\delta k_x', font_size=26)).arrange(RIGHT, buff=0.1),
                          VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=C_PROP, stroke_width=4), MathTex(r'\delta k_y', font_size=26)).arrange(RIGHT, buff=0.1)
                          ).arrange(RIGHT, buff=0.4).move_to([-5.0, -1.75, 0])
        with self.narrate('zoo4') as bt:
            self.play(FadeOut(VGroup(kcirc, img, axl, ell, metric, gdef, eig, ellf, fast, ins_ax, sq_l)), run_time=0.6)
            self.play(FadeIn(ksq), GrowArrow(ex_k), GrowArrow(ey_k), FadeIn(kcirc_ar), run_time=1.0)
            self.play(FadeIn(par), FadeIn(par_in), run_time=1.4)
            self.play(FadeIn(area), FadeIn(legend_e.next_to(detg, DOWN, buff=0.25)), run_time=1.0)
            bt.wait_sentence(1)
            self.play(Write(detg), run_time=1.2)

        # ---------------- zoo5: Berry curvature = signed area; a flipped cell near M
        n1_, a1, b1 = jac(K1)
        t1b, t2b = tangent_basis(n1_)
        Jt1 = 0.5 * np.array([[a1 @ t1b, b1 @ t1b], [a1 @ t2b, b1 @ t2b]])
        ds1 = 0.42
        sq1 = [K1 + np.array(p) * ds1 - ds1 / 2 for p in [(0, 0), (1, 0), (1, 1), (0, 1)]]
        ksq1 = Polygon(*[ax.c2p(*p) for p in sq1], stroke_color=WHITE, stroke_width=2.5, fill_color=C_FLIP, fill_opacity=0.6)
        edge1 = []
        for p, q in zip(sq1, sq1[1:] + sq1[:1]):
            edge1 += [p + (q - p) * t for t in np.linspace(0, 1, 25)]
        par1 = Polygon(*[sph.p(qwz_n(*p) * 1.01) for p in edge1], stroke_color=WHITE, stroke_width=2, fill_color=C_FLIP, fill_opacity=0.8)
        ins2c = INS_C + np.array([0, -0.0, 0])
        par_in_left = par_in.copy()
        par_in1 = inset_par(INS_C + np.array([0.95, 0.1, 0]), Jt1, F, C_FLIP, head=0.08)   # true scale: it covers less area
        enl = txt('(same scale)', 20, GREY_T).next_to(par_in1, DOWN, buff=0.12)
        lab_up = VGroup(txt('same way as most', 20, C_UP), txt('face up, $\\Omega>0$', 20, C_UP)).arrange(DOWN, buff=0.04)
        lab_fl = VGroup(txt('mirror way', 20, C_FLIP), txt('flipped, $\\Omega<0$', 20, C_FLIP)).arrange(DOWN, buff=0.04)
        berry = MathTex(r'\Omega_{xy} = \pm\,2\sqrt{\det g}', font_size=36).move_to([-5.0, -2.75, 0])
        two_l = VGroup(MathTex(r'2 = \tfrac12 \times 4', font_size=30, color=GREY_A),
                       txt('a Berry phase is half a solid angle;', 22, GREY_A),
                       txt('on a sphere of radius $\\tfrac12$, solid angle $= 4\\times$ area', 22, GREY_A)
                       ).arrange(DOWN, buff=0.08).move_to([4.45, -1.35, 0])
        with self.narrate('zoo5') as bt:
            self.play(FadeOut(h2), FadeOut(nophase), par_in.animate.shift(0.9 * LEFT), run_time=0.8)
            lab_up.next_to(par_in, DOWN, buff=0.12)
            self.play(FadeIn(lab_up), run_time=0.5)
            self.play(FadeIn(ksq1), FadeIn(par1), FadeIn(par_in1), FadeIn(enl), run_time=1.4)
            lab_fl.next_to(enl, DOWN, buff=0.06)
            self.play(FadeIn(lab_fl), run_time=0.5)
            bt.wait_sentence(2)
            self.play(Write(berry), run_time=1.8)
            bt.wait_sentence(3)
            self.play(FadeIn(two_l), run_time=1.0)

        # ---------------- zoo6: the other band: same shape, flipped
        mirror = Jt.copy()
        mirror[0, :] *= -1                     # antipode seen from outside: x -> -x in the tangent plane
        par_other = inset_par(INS_C + np.array([0, -2.95, 0]), mirror, F, C_FLIP)
        oth_box = inset_frame(INS_C + np.array([0, -2.95, 0]), h=2.0, label='the other band ($-\\mathbf n$, antipodal point)')
        rel = MathTex(r'g_{-} = g_{+},\qquad \Omega_{-} = -\,\Omega_{+}', font_size=36, color=C_FOLD).move_to([-4.9, -3.45, 0])
        with self.narrate('zoo6') as bt:
            self.play(FadeOut(VGroup(ksq1, par1, par_in1, enl, lab_fl, two_l)), par_in.animate.shift(0.9 * RIGHT),
                      lab_up.animate.shift(0.9 * RIGHT), run_time=0.8)
            bt.wait_sentence(1)
            self.play(FadeIn(oth_box), run_time=0.6)
            self.play(TransformFromCopy(par_in, par_other), run_time=1.6)
            bt.wait_sentence(2)
            self.play(Write(rel), run_time=1.6)
            bt.wait_sentence(3)
            known = txt('(the known two-band result)', 22, GREY_A).next_to(rel, RIGHT, buff=0.3)
            self.play(FadeIn(known), Circumscribe(rel, color=C_FOLD), run_time=1.2)

        # ---------------- zoo7: same Gaussian curvature for both bands
        kg = MathTex(r'K_G = 4 \text{ everywhere: the shape of the sphere (both bands)}', font_size=28).move_to([-0.4, 3.15, 0])
        neq = MathTex(r'\Omega \neq K_G:\ \ \Omega \text{ is how the zone is laid onto it}', font_size=28, color=C_FOLD).move_to([-0.4, 2.6, 0])
        with self.narrate('zoo7') as bt:
            self.play(FadeOut(title), run_time=0.6)
            bt.wait_sentence(1)
            self.play(Write(kg), run_time=1.8)
            bt.wait_sentence(2)
            self.play(Write(neq), run_time=1.6)
            self.play(Circumscribe(neq, color=C_FOLD), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
