import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NU, NV = 36, 36                 # quads along u (-> k_x) and v (-> k_y)
W, HH = 4.4, 2.6                # sheet size before rolling
R1, r1 = W / TAU, HH / TAU      # torus radii after rolling and bending
RS = 0.82                       # sphere radius used for the pressed torus
PAPER = ['#5d6f93', '#4b5b7c']


def surface(b, c, tau=0.0):
    """Sheet (b = c = 0) -> cylinder (b = 1) -> torus (c = 1) -> pressed onto the Bloch sphere (tau = 1)."""
    u = np.linspace(0, 1, NU + 1)[:, None]
    v = np.linspace(0, 1, NV + 1)[None, :]
    bb, cc = max(b, 1e-4), max(c, 1e-4)
    rb = HH / (TAU * bb)
    al = TAU * bb * (v - 0.5)
    sec_y, sec_z = rb * np.sin(al), rb * (1 - np.cos(al))          # cross-section of the roll
    Rc = W / (TAU * cc)
    be = TAU * cc * (u - 0.5)
    ax_x, ax_y = Rc * np.sin(be), Rc * (1 - np.cos(be))             # bent axis (in the x-y plane)
    nin_x, nin_y = -np.sin(be), np.cos(be)
    X = ax_x + sec_y * nin_x
    Y = ax_y + sec_y * nin_y
    Z = sec_z + 0 * X
    P = np.stack([X, Y, Z], -1)
    if tau > 0:
        kx, ky = TAU * (u + 0 * v), TAU * (v - 0.5 + 0 * u)
        n, _, om, _ = qwz_geom(kx, ky)
        lift = 1 + 0.05 / (1 + np.exp(om / 0.008))            # the flipped sheet sits slightly above the others
        S = np.stack([n[0], n[1], n[2]], -1) * (RS * lift)[..., None] + np.array([0.0, R1, r1])
        P = (1 - tau) * P + tau * S
    return P


def colors_for(mix):
    """Paper checkerboard blended into the orientation colours (mix = 1)."""
    h = 1.0 / NU
    uc = (np.arange(NU) + 0.5) / NU
    vc = (np.arange(NV) + 0.5) / NV
    KX, KY = np.meshgrid(TAU * uc, TAU * (vc - 0.5), indexing='ij')
    _, _, om, _ = qwz_geom(KX, KY)
    out = []
    for i in range(NU):
        row = []
        for j in range(NV):
            base = ManimColor(PAPER[(i + j) % 2])
            tgt = ManimColor(C_UP if om[i, j] >= 0 else C_FLIP)
            row.append(interpolate_color(base, tgt, mix))
        out.append(row)
    return out


class S01_ColdOpen(NScene):
    def construct(self):
        b, c, tau, mix = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        el, az = ValueTracker(0.95), ValueTracker(-1.25)
        sc = ValueTracker(1.25)
        ctr = np.array([0.0, -0.3, 0])
        shift3 = ValueTracker(0.0)      # moves the object's 3D centre from the sheet to the torus centre

        def draw():
            cam = Cam(el.get_value(), az.get_value(), sc.get_value(), ctr)
            P = surface(b.get_value(), c.get_value(), tau.get_value())
            P = P - shift3.get_value() * np.array([0.0, R1, r1])
            return mesh(cam, P, colors_for(mix.get_value()), opacity=0.92, stroke_width=0.5)

        obj = always_redraw(draw)

        # ---- open1: a flat sheet rolls into a cylinder
        with self.narrate('open1') as bt:
            self.play(FadeIn(obj), run_time=1.0)
            bt.wait_sentence(1)
            self.play(b.animate.set_value(1.0), el.animate.set_value(0.55), shift3.animate.set_value(0.0),
                      run_time=bt.remaining(-0.3), rate_func=smooth)
        lab_cyl = txt('no stretching, no crease', 30, GREY_A).to_edge(DOWN, buff=0.6)

        # ---- open2: bend and glue -> torus
        with self.narrate('open2') as bt:
            self.play(FadeIn(lab_cyl), run_time=0.5)
            self.play(c.animate.set_value(1.0), shift3.animate.set_value(1.0), az.animate.set_value(-0.9),
                      sc.animate.set_value(2.1), FadeOut(lab_cyl), run_time=bt.until_sentence(1, 2.0) + 0.6, rate_func=smooth)
            torus_l = txt('torus', 34, bold=True).to_edge(DOWN, buff=0.6)
            self.play(FadeIn(torus_l), az.animate.set_value(-0.55), run_time=bt.remaining(-0.2), rate_func=linear)

        # ---- open3: can a torus lie smoothly over a sphere? It must fold.
        q = txt('a torus over a sphere, without creases?', 34).to_edge(UP, buff=0.5)
        with self.narrate('open3') as bt:
            self.play(FadeOut(torus_l), FadeIn(q), az.animate.set_value(-0.35), run_time=1.4, rate_func=linear)
            bt.wait_sentence(1)
            self.play(tau.animate.set_value(1.0), mix.animate.set_value(1.0), el.animate.set_value(0.42),
                      sc.animate.set_value(2.3), run_time=bt.until_sentence(2, 3.0), rate_func=smooth)
            no = txt('impossible: it must fold', 34, C_FLIP).to_edge(UP, buff=0.5)
            self.play(ReplacementTransform(q, no), az.animate.set_value(-0.1), run_time=1.0, rate_func=linear)
            self.play(az.animate.set_value(0.6), run_time=bt.remaining(-0.2), rate_func=linear)

        # ---- open4: electrons do this; the folds hide the Chern number
        legend = VGroup(VGroup(Square(0.25, fill_color=C_UP, fill_opacity=1, stroke_width=0), txt('lands face up', 26)).arrange(RIGHT, buff=0.15),
                        VGroup(Square(0.25, fill_color=C_FLIP, fill_opacity=1, stroke_width=0), txt('lands flipped', 26)).arrange(RIGHT, buff=0.15)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(DR, buff=0.6)
        roles = VGroup(txt('momentum torus (Brillouin zone)', 28, GREY_A), MathTex(r'\longrightarrow', font_size=36),
                       txt('state sphere (two bands)', 28, GREY_A)).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.55)
        chern = txt('the folds hide the Chern number', 34, C_FOLD).to_edge(UP, buff=0.5)
        with self.narrate('open4') as bt:
            self.play(FadeOut(no), FadeIn(roles), az.animate.set_value(1.2), run_time=bt.until_sentence(1, 1.5), rate_func=linear)
            self.play(FadeIn(legend), az.animate.set_value(2.0), run_time=2.5, rate_func=linear)
            self.play(FadeIn(chern, shift=0.15 * DOWN), az.animate.set_value(3.2), run_time=bt.remaining(-0.2), rate_func=linear)

        # ---- open5: title card
        title = txt('Quantum geometry on the Grassmannian', 50, bold=True)
        sub = txt('projectors, distances, folds', 36, GREY_A)
        refs = VGroup(txt('after Shin-Ming Huang:', 28, GREY_A),
                      txt('H1 (with D. Giataganas) arXiv:2412.20046', 26, GREY_T),
                      txt('H2 arXiv:2608.06777 \\quad H3 arXiv:2510.15760', 26, GREY_T)).arrange(DOWN, buff=0.12)
        Pform = MathTex(r'P(\mathbf k) = \sum_{n\in\mathrm{occ}} |u_n(\mathbf k)\rangle\langle u_n(\mathbf k)|', font_size=44, color=C_FOLD)
        card = VGroup(title, sub, Pform, refs).arrange(DOWN, buff=0.4).move_to(ORIGIN)
        with self.narrate('open5') as bt:
            self.play(FadeOut(VGroup(roles, legend, chern)), FadeOut(obj), run_time=1.0)
            self.play(Write(title), FadeIn(sub, shift=0.15 * UP), run_time=1.8)
            self.play(FadeIn(refs), run_time=1.0)
            self.play(Write(Pform), run_time=2.0)
        self.play(FadeOut(card), run_time=0.8)
