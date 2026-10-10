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
        metric = MathTex(r'ds^2 = g_{ij}\,dk^i dk^j', font_size=38, color=C_G).move_to([-5.1, -1.1, 0])
        fast = txt('long axis: fastest change of the state', 24, YELLOW).move_to([-5.0, -1.75, 0])
        # inset: the ellipse in the tangent plane (seen from outside), enlarged
        F = 5.2
        ins = inset_frame(INS_C, label='close-up of the tangent plane')
        Jt = 0.5 * np.array([[a @ t1, b @ t1], [a @ t2, b @ t2]])          # radius-1/2 sphere
        ell_pts = [INS_C + F * rc * np.array([*(Jt @ np.array([np.cos(t), np.sin(t)])), 0]) for t in th]
        ell = VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly(ell_pts)
        with self.narrate('zoo2') as bt:
            self.play(FadeIn(ins), Create(ell), run_time=1.2)
            self.play(Write(metric), run_time=1.2)
            bt.wait_sentence(1)
            self.play(Create(axl), run_time=1.5)
            bt.wait_sentence(2)
            self.play(FadeIn(fast), run_time=0.8)

        # ---------------- zoo3: built from dP, no phase
        h2 = MathTex(r'g_{ij} = \tfrac12\,\mathrm{tr}\big(\partial_i P\,\partial_j P\big)', font_size=40, color=C_G)
        h2.move_to([4.75, -1.25, 0])
        nophase = txt('$P$ has no phase to choose', 26, GREY_A).next_to(h2, DOWN, buff=0.2)
        with self.narrate('zoo3') as bt:
            self.play(FadeOut(mk), FadeOut(ms), run_time=0.4)
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

        def inset_par(center, Jm, scale, color):
            o = np.asarray(center, float) - scale * ds * np.array([*(Jm @ np.array([0.5, 0.5])), 0])
            vx = scale * ds * np.array([*(Jm @ np.array([1.0, 0.0])), 0])
            vy = scale * ds * np.array([*(Jm @ np.array([0.0, 1.0])), 0])
            poly = Polygon(o, o + vx, o + vx + vy, o + vy, stroke_color=WHITE, stroke_width=2, fill_color=color, fill_opacity=0.65)
            ar = VGroup(Arrow(o, o + vx, buff=0, color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.25),
                        Arrow(o, o + vy, buff=0, color=C_PROP, stroke_width=5, max_tip_length_to_length_ratio=0.25))
            return VGroup(poly, ar)
        par_in = inset_par(INS_C, Jt, F, C_UP)
        area = MathTex(r'\text{area} = \sqrt{\det g}\;\delta k_x\,\delta k_y', font_size=34).move_to([-5.1, -1.1, 0])
        legend_e = VGroup(VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=YELLOW, stroke_width=4), MathTex(r'\delta k_x', font_size=26)).arrange(RIGHT, buff=0.1),
                          VGroup(Arrow(LEFT * 0.3, RIGHT * 0.3, buff=0, color=C_PROP, stroke_width=4), MathTex(r'\delta k_y', font_size=26)).arrange(RIGHT, buff=0.1)
                          ).arrange(RIGHT, buff=0.4).move_to([-5.0, -1.75, 0])
        with self.narrate('zoo4') as bt:
            self.play(FadeOut(VGroup(kcirc, img, axl, ell, metric, fast)), run_time=0.6)
            self.play(FadeIn(ksq), GrowArrow(ex_k), GrowArrow(ey_k), run_time=1.0)
            bt.wait_sentence(1)
            self.play(FadeIn(par), FadeIn(par_in), run_time=1.4)
            bt.wait_sentence(2)
            self.play(FadeIn(area), FadeIn(legend_e), run_time=1.0)

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
        F1 = F * 2.0
        par_in1 = inset_par(INS_C + np.array([0.95, 0.1, 0]), Jt1, F1, C_FLIP)
        enl = txt('(2$\\times$ enlarged)', 20, GREY_T).next_to(par_in1, DOWN, buff=0.12)
        lab_up = txt('face up: $\\Omega>0$', 24, C_UP)
        lab_fl = txt('flipped: $\\Omega<0$', 24, C_FLIP)
        berry = MathTex(r'\Omega_{xy}\,\delta k_x\,\delta k_y = \pm\, 2\times\text{area}', font_size=36).move_to([-5.0, -2.45, 0])
        with self.narrate('zoo5') as bt:
            self.play(FadeOut(h2), FadeOut(nophase), par_in.animate.shift(0.9 * LEFT), run_time=0.8)
            lab_up.next_to(par_in, DOWN, buff=0.35)
            self.play(FadeIn(lab_up), run_time=0.5)
            self.play(FadeIn(ksq1), FadeIn(par1), FadeIn(par_in1), FadeIn(enl), run_time=1.4)
            lab_fl.next_to(enl, DOWN, buff=0.1)
            self.play(FadeIn(lab_fl), run_time=0.5)
            bt.wait_sentence(1)
            self.play(Write(berry), run_time=1.8)

        # ---------------- zoo6: the other band: same shape, flipped
        mirror = Jt.copy()
        mirror[0, :] *= -1                     # antipode seen from outside: x -> -x in the tangent plane
        par_other = inset_par(INS_C + np.array([0, -2.95, 0]), mirror, F, C_FLIP)
        oth_box = inset_frame(INS_C + np.array([0, -2.95, 0]), h=2.0, label='the other band ($-\\mathbf n$, antipodal point)')
        rel = MathTex(r'g_{-} = g_{+},\qquad \Omega_{-} = -\,\Omega_{+}', font_size=38, color=C_FOLD).move_to([-4.9, -3.3, 0])
        with self.narrate('zoo6') as bt:
            self.play(FadeOut(VGroup(ksq1, par1, par_in1, enl, lab_fl)), par_in.animate.shift(0.9 * RIGHT),
                      lab_up.animate.shift(0.9 * RIGHT), run_time=0.8)
            bt.wait_sentence(1)
            self.play(FadeIn(oth_box), run_time=0.6)
            self.play(TransformFromCopy(par_in, par_other), run_time=1.6)
            bt.wait_sentence(2)
            self.play(Write(rel), run_time=1.6)

        # ---------------- zoo7: same Gaussian curvature for both bands
        kg = MathTex(r'\text{both bands: sphere of radius } \tfrac12,\quad K_G = 4', font_size=34).move_to([-0.4, 3.1, 0])
        neq = MathTex(r'\Omega \;\neq\; K_G', font_size=46, color=C_FOLD).move_to([-0.4, 2.35, 0])
        with self.narrate('zoo7') as bt:
            self.play(FadeOut(title), Write(kg), run_time=1.8)
            bt.wait_sentence(1)
            self.play(Write(neq), run_time=1.2)
            bt.wait_sentence(2)
            self.play(Circumscribe(neq, color=C_FOLD), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
