import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

KD = np.load(ROOT / 'data' / 'kahler.npz')


def banner():
    t = txt('PROPOSAL \\;(unpublished)', 26, C_PROP, bold=True)
    box = SurroundingRectangle(t, buff=0.14, corner_radius=0.08, stroke_color=C_PROP, stroke_width=2)
    return VGroup(box, t).to_corner(UR, buff=0.35)


def fold_surface(eps, n=22, lam=1.0):
    """lam = 0: the flat sheet (s, t); lam = 1: the fold (s, t^2); eps > 0 lifts it to (s, t^2, eps t)."""
    s = np.linspace(-1, 1, n + 1)[:, None]
    t = np.linspace(-1, 1, n + 1)[None, :]
    X = np.stack([s + 0 * t, (1 - lam) * t + lam * t ** 2 + 0 * s, eps * t + 0 * s], -1)
    cols = [[(C_UP if (j + 0.5) / n > 0.5 else C_FLIP) for j in range(n)] for i in range(n)]
    on_top = np.array([[(j + 0.5) / n < 0.5 for j in range(n)] for i in range(n)])
    return X, cols, on_top


class S09_Multiband(NScene):
    def construct(self):
        ban = banner()
        title = txt('More than two bands?', 40, bold=True).to_edge(UP, buff=0.35)

        # ---------------- mul1: open question, our proposal
        q = VGroup(txt('open question at the end of H3:', 30, GREY_A),
                   txt('what replaces the fold picture beyond two bands?', 34)).arrange(DOWN, buff=0.2).move_to([0, 1.0, 0])
        note = txt('green = our proposal, not in the three papers', 26, C_PROP).move_to([0, -0.4, 0])
        with self.narrate('mul1') as b:
            self.play(Write(title), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(q), run_time=1.2)
            b.wait_sentence(2)
            self.play(FadeIn(ban, scale=1.1), run_time=0.8)
            b.wait_sentence(3)
            self.play(FadeIn(note), run_time=0.8)

        # ---------------- mul2: counting dimensions
        cnt = MathTex(r'N \text{ complex amplitudes: } 2N \;-\; 1\ (\text{normalisation}) \;-\; 1\ (\text{phase}) \;=\; 2N-2', font_size=32)
        cnt.move_to([0, 1.7, 0])
        rows = VGroup(MathTex(r'N=2:\quad 2 \text{ real dims} \quad \mathbb{CP}^1 = \text{Bloch sphere}', font_size=32),
                      MathTex(r'N=3:\quad 4 \text{ real dims} \quad \mathbb{CP}^2', font_size=32, color=C_PROP)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 0.5, 0])
        surf_l = txt('the zone (2D) maps to a surface inside a 4D space', 28, GREY_A).move_to([0, -0.9, 0])
        with self.narrate('mul2') as b:
            self.play(FadeOut(q), FadeOut(note), Write(cnt), run_time=2.2)
            b.wait_sentence(1)
            self.play(FadeIn(rows[0]), run_time=1.0)
            self.play(FadeIn(rows[1]), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(surf_l), run_time=1.0)

        # ---------------- mul2b: a fold needs a direction that stops moving the state; the model fold (s, t^2)
        eps = ValueTracker(0.0)
        lam = ValueTracker(0.0)
        cam = Cam(0.3, 0.32, 2.0, center=[-3.7, -1.3, 0])

        def surf():
            X, cols, on_top = fold_surface(eps.get_value(), lam=lam.get_value())
            g = mesh(cam, X, cols, opacity=0.8, stroke_width=0.6, on_top=on_top)
            g.add(Line(cam.p([-1, 0, 0]), cam.p([1, 0, 0]), color=C_FOLD, stroke_width=4))   # the crease t = 0
            return g
        sf = always_redraw(surf)
        need = txt('fold: one direction of motion stops changing the state', 26, GREY_A).move_to([0, 2.0, 0])
        gen = txt('with 2 extra dimensions, a generic surface never has to do that', 26, C_PROP).move_to([0, 1.45, 0])
        f0 = MathTex(r'f(s,t) = (s,\ t^2):\quad f(s,t) = f(s,-t),\quad \partial_t f\big|_{t=0} = 0', font_size=32).move_to([3.0, 0.4, 0])
        with self.narrate('mul2b') as b:
            self.play(FadeOut(VGroup(cnt, rows, surf_l)), FadeIn(need), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(gen), run_time=1.0)
            b.wait_sentence(2)
            self.add(sf)
            self.play(FadeIn(sf), run_time=0.8)
            self.play(lam.animate.set_value(1.0), run_time=1.8, rate_func=smooth)
            b.wait_sentence(3)
            self.play(Write(f0), run_time=1.6)

        # ---------------- mul2c: the third orbital opens the crease
        fe = MathTex(r'f_\varepsilon(s,t) = (s,\ t^2,\ \varepsilon t):\quad \partial_t f_\varepsilon = (0,\ 2t,\ \varepsilon) \neq 0', font_size=32, color=C_PROP)
        fe.move_to([3.0, -0.4, 0])
        epsl = always_redraw(lambda: MathTex(r'\varepsilon = ' + f'{eps.get_value():.2f}', font_size=32, color=C_PROP).move_to([3.0, -1.2, 0]))
        teach = txt('(a Euclidean teaching picture)', 22, GREY_T).move_to([3.0, -1.8, 0])
        chk = MathTex(r'\text{three-band model: } \min_{\mathbf k}\det g = 1.0\times10^{-5} > 0', font_size=30).move_to([3.0, -2.6, 0])
        with self.narrate('mul2c') as b:
            self.add(epsl)
            self.play(Write(fe), FadeIn(teach), run_time=1.6)
            b.wait_sentence(1)
            self.play(eps.animate.set_value(0.9), run_time=2.8, rate_func=smooth)
            b.wait_sentence(2)
            self.play(FadeIn(chk), run_time=1.0)

        # ---------------- mul3: the Kahler angle; two-band vs three-band maps
        sf.clear_updaters()
        epsl.clear_updaters()
        bound = MathTex(r'|\Omega_{xy}| \le 2\sqrt{\det g}', font_size=38).move_to([-3.2, 2.6, 0])
        kahler = MathTex(r'\cos\theta_K = \frac{\Omega_{xy}}{2\sqrt{\det g}}', font_size=40, color=C_PROP).move_to([2.6, 2.55, 0])
        ax2, bz2 = bz_axes(3.3, center=[-3.4, -0.85, 0])
        ax3, bz3 = bz_axes(3.3, center=[2.2, -0.85, 0])
        img2 = image_on_axes(signed_rgba(KD['two_cos'].T, 1.0, pos=C_UP, neg=C_FLIP, gamma=1.0), ax2, (0, TAU_K), (0, TAU_K))
        img3 = image_on_axes(signed_rgba(KD['three_cos'].T, 1.0, pos=C_UP, neg=C_FLIP, gamma=1.0), ax3, (0, TAU_K), (0, TAU_K))
        l2 = txt('two bands: always $\\pm 1$', 26).next_to(bz2, UP, buff=0.3)
        l3 = txt('three bands: varies smoothly', 26, C_PROP).next_to(bz3, UP, buff=0.3)
        # the colour bar uses the same map as the images: +1 blue, 0 dark, -1 red
        bar_v = np.linspace(1, -1, 256)[:, None] * np.ones((1, 8))
        cbar = ImageMobject(signed_rgba(bar_v, 1.0, pos=C_UP, neg=C_FLIP, gamma=1.0))
        cbar.set_resampling_algorithm(RESAMPLING_ALGORITHMS['bilinear'])
        cbar.stretch_to_fit_width(0.25).stretch_to_fit_height(1.8).next_to(bz3, RIGHT, buff=0.5)
        cbar = Group(cbar, Rectangle(width=0.25, height=1.8, stroke_color=GREY_C, stroke_width=1).move_to(cbar))
        cbl = VGroup(MathTex('+1', font_size=26).next_to(cbar.get_corner(UR), RIGHT, buff=0.08).shift(0.1 * DOWN),
                     MathTex('0', font_size=26).next_to(cbar, RIGHT, buff=0.08),
                     MathTex('-1', font_size=26).next_to(cbar.get_corner(DR), RIGHT, buff=0.08).shift(0.1 * UP),
                     MathTex(r'\cos\theta_K', font_size=26, color=C_PROP).next_to(cbar, UP, buff=0.15))
        conv = VGroup(MathTex(r'\text{dark: } |\Omega| \ll 2\sqrt{\det g}', font_size=22, color=GREY_T),
                      txt('sign: $+1$ agrees with $C$', 20, GREY_T)
                      ).arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(cbar, DOWN, buff=0.25, aligned_edge=LEFT)
        with self.narrate('mul3') as b:
            self.play(FadeOut(VGroup(sf, f0, fe, teach, chk, need, gen)), FadeOut(epsl), run_time=0.8)
            b.wait_sentence(2)
            self.play(Write(bound), run_time=1.4)
            self.play(Write(kahler), run_time=1.8)
            b.wait_sentence(3)
            self.play(FadeIn(bz2), FadeIn(img2), FadeIn(l2), run_time=1.2)
            self.bring_to_front(bz2)
            b.wait_sentence(4)
            self.play(FadeIn(bz3), FadeIn(img3), FadeIn(l3), FadeIn(cbar), FadeIn(cbl), FadeIn(conv), run_time=1.2)
            self.bring_to_front(bz3)

        # ---------------- mul4: complex points and their indices
        cps = KD['cp']
        marks = VGroup()
        for kx, ky, w in cps:
            p = ax3.c2p(kx, ky)
            if w > 0:
                m = VGroup(Line(p + 0.13 * LEFT, p + 0.13 * RIGHT), Line(p + 0.13 * DOWN, p + 0.13 * UP)).set_stroke(WHITE, 4)
            else:
                m = VGroup(Line(p + 0.11 * (LEFT + DOWN), p + 0.11 * (RIGHT + UP)), Line(p + 0.11 * (LEFT + UP), p + 0.11 * (RIGHT + DOWN))).set_stroke(YELLOW, 4)
            marks.add(m)
        cline = MathTex(r'\text{complex points: } |\cos\theta_K| = 1', font_size=32, color=C_PROP).move_to([-2.6, -3.0, 0])
        vortex = VGroup(Circle(radius=0.32, color=GREY_B, stroke_width=2),
                        *[Arrow(ORIGIN, 0.25 * np.array([np.cos(a + PI / 2), np.sin(a + PI / 2), 0]), buff=0, color=C_PROP,
                                stroke_width=3, max_tip_length_to_length_ratio=0.4).shift(0.32 * np.array([np.cos(a), np.sin(a), 0]))
                          for a in np.linspace(0, TAU, 8, endpoint=False)])
        vortex.move_to([2.2, -3.0, 0])
        vlab = txt('index $\\pm1$: a phase winds once', 22, GREY_A).next_to(vortex, RIGHT, buff=0.2)
        mk_leg = VGroup(VGroup(marks[0].copy().scale(0.8), txt('index $+1$', 20, GREY_A)).arrange(RIGHT, buff=0.15),
                        VGroup(marks[-1].copy().scale(0.8), txt('index $-1$', 20, GREY_A)).arrange(RIGHT, buff=0.15)
                        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([6.15, -0.55, 0])
        cnt3 = MathTex(r'\sum \text{indices} = 3|C|', r'\qquad (+1)\times 4 + (-1)\times 1 = 3', font_size=32, color=C_PROP).move_to([0, -3.6, 0])
        with self.narrate('mul4') as b:
            self.play(FadeIn(cline), run_time=1.0)
            b.wait_sentence(1)
            self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.3), run_time=1.6)
            b.wait_sentence(2)
            self.play(FadeIn(vortex), FadeIn(vlab), FadeIn(mk_leg), run_time=0.8)
            self.play(Rotate(vortex, angle=PI / 2), run_time=1.0)
            b.wait_sentence(3)
            self.play(Write(cnt3[0]), run_time=1.4)
            b.wait_sentence(4)
            self.play(Write(cnt3[1]), Indicate(marks, scale_factor=1.3), run_time=2.0)

        # ---------------- mul5: Gauss-Bonnet holds again
        gb3 = VGroup(MathTex(r'\text{three bands (no fold): }\ \frac{1}{2\pi}\int K_G\,dA = 1.6\times10^{-5} \approx 0 = \chi(T^2)', font_size=30),
                     txt('the Gaussian curvature no longer carries the Chern number', 24, GREY_A)).arrange(DOWN, buff=0.12)
        gb3.move_to([0, -3.3, 0])
        with self.narrate('mul5') as b:
            self.play(FadeOut(VGroup(cline, vortex, vlab, cnt3)), FadeIn(gb3[0]), run_time=1.4)
            b.wait_sentence(1)
            self.play(FadeIn(gb3[1]), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
