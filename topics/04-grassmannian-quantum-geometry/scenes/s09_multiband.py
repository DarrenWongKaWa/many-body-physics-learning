import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

KD = np.load(ROOT / 'data' / 'kahler.npz')


def banner():
    t = txt('PROPOSAL \\;(unpublished)', 26, C_PROP, bold=True)
    box = SurroundingRectangle(t, buff=0.14, corner_radius=0.08, stroke_color=C_PROP, stroke_width=2)
    return VGroup(box, t).to_corner(UR, buff=0.35)


def fold_surface(eps, n=22):
    s = np.linspace(-1, 1, n + 1)[:, None]
    t = np.linspace(-1, 1, n + 1)[None, :]
    X = np.stack([s + 0 * t, t ** 2 + 0 * s, eps * t + 0 * s], -1)
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

        # ---------------- mul2: the fold escapes into a new direction
        dims = MathTex(r'\mathbb{CP}^1 \ (2 \text{ real dims}) \;\longrightarrow\; \mathbb{CP}^2 \ (4 \text{ real dims})', font_size=36)
        dims.move_to([0, 2.45, 0])
        eps = ValueTracker(0.0)
        cam = Cam(0.3, 0.32, 2.3, center=[-3.4, -0.6, 0])

        def surf():
            X, cols, on_top = fold_surface(eps.get_value())
            return mesh(cam, X, cols, opacity=0.8, stroke_width=0.6, on_top=on_top)
        sf = always_redraw(surf)
        f0 = MathTex(r'f(s,t) = (s,\ t^2)', font_size=36).move_to([3.6, 0.9, 0])
        fe = MathTex(r'f_\varepsilon(s,t) = (s,\ t^2,\ \varepsilon t)', font_size=36, color=C_PROP).move_to([3.6, 0.0, 0])
        ge = MathTex(r'g_\varepsilon = \mathrm{diag}(1,\ 4t^2+\varepsilon^2),\quad \det g_\varepsilon > 0', font_size=32).move_to([3.6, -0.8, 0])
        epsl = always_redraw(lambda: MathTex(r'\varepsilon = ' + f'{eps.get_value():.2f}', font_size=32, color=C_PROP).move_to([3.6, -1.6, 0]))
        teach = txt('(a Euclidean teaching picture)', 22, GREY_T).move_to([3.6, -2.3, 0])
        with self.narrate('mul2') as b:
            self.play(FadeOut(q), FadeOut(note), FadeIn(dims), run_time=1.0)
            b.wait_sentence(1)
            self.add(sf)
            self.play(FadeIn(sf), Write(f0), run_time=1.5)
            b.wait_sentence(2)
            self.add(epsl)
            self.play(Write(fe), FadeIn(teach), run_time=1.2)
            self.play(eps.animate.set_value(0.9), run_time=2.8, rate_func=smooth)
            self.play(FadeIn(ge), run_time=1.0)

        # ---------------- mul3: the Kahler angle; two-band vs three-band maps
        sf.clear_updaters()
        kahler = MathTex(r'\Omega_{xy} = 2\cos\theta_K\,\sqrt{\det g}', font_size=42, color=C_PROP).move_to([0, 2.6, 0])
        ks = KD['ks']
        ax2, bz2 = bz_axes(3.4, center=[-3.4, -0.75, 0])
        ax3, bz3 = bz_axes(3.4, center=[2.2, -0.75, 0])
        img2 = image_on_axes(signed_rgba(KD['two_cos'].T, 1.0, pos=C_UP, neg=C_FLIP, gamma=1.0), ax2, (0, TAU_K), (0, TAU_K))
        img3 = image_on_axes(signed_rgba(KD['three_cos'].T, 1.0, pos=C_UP, neg=C_FLIP, gamma=1.0), ax3, (0, TAU_K), (0, TAU_K))
        l2 = txt('two bands: $\\cos\\theta_K = \\pm 1$, jumps at the fold', 26).next_to(bz2, UP, buff=0.3)
        l3 = txt('three bands: varies smoothly', 26, C_PROP).next_to(bz3, UP, buff=0.3)
        cbar = VGroup(Rectangle(width=0.25, height=0.9, fill_color=C_UP, fill_opacity=1, stroke_width=0),
                      Rectangle(width=0.25, height=0.9, fill_color=C_FLIP, fill_opacity=1, stroke_width=0)
                      ).arrange(DOWN, buff=0).next_to(bz3, RIGHT, buff=0.5)
        cbl = VGroup(MathTex('+1', font_size=26).next_to(cbar[0], RIGHT, buff=0.08), MathTex('-1', font_size=26).next_to(cbar[1], RIGHT, buff=0.08))
        conv = VGroup(txt('sign normalised:', 20, GREY_T), txt('$+1$ agrees with $C$', 20, GREY_T)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).next_to(cbar, DOWN, buff=0.25, aligned_edge=LEFT)
        with self.narrate('mul3') as b:
            self.play(FadeOut(VGroup(sf, f0, fe, ge, teach, dims)), FadeOut(epsl), run_time=0.8)
            b.wait_sentence(1)
            self.play(Write(kahler), run_time=1.8)
            b.wait_sentence(3)
            self.play(FadeIn(bz2), FadeIn(img2), FadeIn(l2), run_time=1.2)
            self.bring_to_front(bz2)
            b.wait_sentence(4)
            self.play(FadeIn(bz3), FadeIn(img3), FadeIn(l3), FadeIn(cbar), FadeIn(cbl), FadeIn(conv), run_time=1.2)
            self.bring_to_front(bz3)

        # ---------------- mul4: complex points
        cps = KD['cp']
        marks = VGroup()
        for kx, ky, w in cps:
            p = ax3.c2p(kx, ky)
            if w > 0:
                m = VGroup(Line(p + 0.13 * LEFT, p + 0.13 * RIGHT), Line(p + 0.13 * DOWN, p + 0.13 * UP)).set_stroke(WHITE, 4)
            else:
                m = VGroup(Line(p + 0.11 * (LEFT + DOWN), p + 0.11 * (RIGHT + UP)), Line(p + 0.11 * (LEFT + UP), p + 0.11 * (RIGHT + DOWN))).set_stroke(YELLOW, 4)
            marks.add(m)
        cline = txt('complex points: $|\\cos\\theta_K| = 1$, the tangent plane is a complex line', 24, C_PROP).move_to([0, -2.95, 0])
        cnt = MathTex(r'(+1)\times 4 + (-1)\times 1 = 3 = 3\,|C|', font_size=36, color=C_PROP).move_to([0, -3.55, 0])
        with self.narrate('mul4') as b:
            self.play(FadeIn(cline), run_time=1.0)
            b.wait_sentence(1)
            self.play(LaggedStart(*[GrowFromCenter(m) for m in marks], lag_ratio=0.3), run_time=2.0)
            b.wait_sentence(2)
            self.play(Write(cnt), run_time=2.0)

        # ---------------- mul5: Gauss-Bonnet holds again
        gb3 = VGroup(MathTex(r'\text{three bands (no fold): }\ \frac{1}{2\pi}\int K_G\,dA = 1.6\times10^{-5} \approx 0 = \chi(T^2)', font_size=32),
                     txt('the Gaussian curvature no longer carries the Chern number', 26, GREY_A)).arrange(DOWN, buff=0.15)
        gb3.move_to([0, -3.15, 0])
        with self.narrate('mul5') as b:
            self.play(FadeOut(cnt), FadeOut(cline), FadeIn(gb3[0]), run_time=1.4)
            b.wait_sentence(1)
            self.play(FadeIn(gb3[1]), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
