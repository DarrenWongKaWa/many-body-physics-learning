import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def unsigned_area_over_pi(n=600):
    ks = (np.arange(n) + 0.5) * TAU_K / n
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    _, _, om, dg = qwz_geom(KX, KY)
    return np.sqrt(np.clip(dg, 0, None)).sum() * (TAU_K / n) ** 2 / np.pi


class S08_GaussBonnet(NScene):
    def construct(self):
        tag = txt('[H3]', 26, GREY_T).to_corner(UL, buff=0.4)
        title = txt('What does curvature know about topology?', 40, bold=True).to_edge(UP, buff=0.35)
        A = unsigned_area_over_pi()            # 1.189
        REG = 4 * A / 2                        # regular part in units of 2 pi: 2.378

        # ---------------- gab1
        with self.narrate('gab1') as b:
            self.play(FadeIn(tag), Write(title), run_time=1.8)

        # ---------------- gab2: classical Gauss-Bonnet
        gb = MathTex(r'\int_\Sigma K_G\,dA = 2\pi\,\chi(\Sigma)', font_size=46).move_to([0, 2.0, 0])
        sph = Sphere2D(radius=1.0, el=0.35, az=0.5, n_merid=2).move_to([-3.2, -0.6, 0])
        tor = torus_wire(Cam(0.6, -0.6, 0.85, center=[3.2, -0.6, 0]), nu=12, nv=10)
        sl = MathTex(r'\chi = 2:\ \ 4\pi', font_size=38).next_to(sph, DOWN, buff=0.35)
        tl = MathTex(r'\chi = 0:\ \ 0', font_size=38).move_to([3.2, -2.1, 0])
        with self.narrate('gab2') as b:
            self.play(Write(gb), run_time=2.2)
            b.wait_sentence(1)
            self.play(FadeIn(sph), FadeIn(sl), run_time=1.2)
            b.wait_sentence(2)
            self.play(FadeIn(tor), FadeIn(tl), run_time=1.2)

        # ---------------- gab3: the regular sheets
        base_y = -0.9
        U = 0.8                                   # screen units per (2 pi)
        x_reg, x_fold, x_tot = -1.5, 0.6, 2.7
        axis = Line([-3.0, base_y, 0], [4.0, base_y, 0], color=GREY_B, stroke_width=2)
        zero = MathTex('0', font_size=28, color=GREY_B).next_to(axis, LEFT, buff=0.15)
        bar_reg = Rectangle(width=1.3, height=REG * U, stroke_width=0, fill_color=C_UP, fill_opacity=0.9)
        bar_reg.move_to([x_reg, base_y + REG * U / 2, 0])
        lab_reg = VGroup(txt('regular sheets', 26), MathTex(r'K_G = 4', font_size=30, color=C_UP)).arrange(DOWN, buff=0.08)
        lab_reg.next_to(bar_reg, LEFT, buff=0.25)
        val_reg = MathTex(r'+' + f'{REG:.3f}' + r'\times 2\pi', font_size=32, color=C_UP).next_to(bar_reg, UP, buff=0.15)
        unit = txt('in units of $2\\pi$', 22, GREY_T).next_to(axis, RIGHT, buff=0.2)
        with self.narrate('gab3') as b:
            self.play(FadeOut(VGroup(sph, sl, tor, tl)), gb.animate.scale(0.75).move_to([0, 2.55, 0]), run_time=1.0)
            self.play(Create(axis), FadeIn(zero), FadeIn(unit), FadeIn(lab_reg), run_time=1.2)
            b.wait_sentence(1)
            self.play(GrowFromEdge(bar_reg, DOWN), run_time=2.0)
            self.play(Write(val_reg), run_time=1.0)
            b.wait_sentence(2)
            notz = txt('not zero!', 32, C_FLIP).next_to(val_reg, RIGHT, buff=0.4)
            self.play(FadeIn(notz, scale=1.2), run_time=0.6)

        # ---------------- gab4: the fold's singular curvature balances the books
        bar_fold = Rectangle(width=1.3, height=REG * U, stroke_width=0, fill_color=C_FOLD, fill_opacity=0.9)
        bar_fold.move_to([x_fold, base_y - REG * U / 2, 0])
        lab_fold = VGroup(txt('fold', 26), txt('(singular curvature)', 22, GREY_A)).arrange(DOWN, buff=0.06).next_to(bar_fold, LEFT, buff=0.25)
        val_fold = MathTex(r'-' + f'{REG:.3f}' + r'\times 2\pi', font_size=32, color=C_FOLD).next_to(bar_fold, RIGHT, buff=0.2).shift(0.6 * UP)
        tot = Dot([x_tot, base_y, 0], radius=0.12, color=WHITE)
        tot_l = VGroup(txt('total', 26), MathTex(r'0 = 2\pi\chi(T^2)', font_size=32)).arrange(DOWN, buff=0.08).next_to(tot, UP, buff=0.25)
        h3f = MathTex(r'\int_{\rm regular} K_G\,dA \;+\; 2\int_{\rm fold}\kappa_s\,ds \;=\; 2\pi\chi(T^2) = 0', font_size=34)
        h3f.move_to([0.5, -3.55, 0])
        with self.narrate('gab4') as b:
            self.play(FadeOut(notz), run_time=0.4)
            b.wait_sentence(1)
            self.play(GrowFromEdge(bar_fold, UP), FadeIn(lab_fold), run_time=2.0)
            self.play(Write(val_fold), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(tot, scale=2), FadeIn(tot_l), run_time=1.0)
            self.play(Write(h3f), run_time=2.0)

        # ---------------- gab5: signed bookkeeping
        signed = MathTex(r'\frac{1}{4\pi}\int_{\rm regular} K_G\,\mathrm{sgn}(\Omega)\,dA = C', font_size=40, color=C_UP)
        signed.move_to([0, 0.4, 0])
        sheets = MathTex(r'(+1) + (+1) + (-1) = 1', font_size=36).next_to(signed, DOWN, buff=0.35)
        four = MathTex(r'4\times\pi = 4\pi C', font_size=34, color=GREY_A).next_to(sheets, DOWN, buff=0.25)
        with self.narrate('gab5') as b:
            self.play(FadeOut(VGroup(axis, zero, unit, bar_reg, lab_reg, val_reg, bar_fold, lab_fold, val_fold, tot, tot_l)),
                      h3f.animate.scale(0.85).move_to([0, 1.75, 0]).set_opacity(0.6), FadeOut(gb), run_time=0.9)
            self.play(Write(signed), run_time=2.0)
            b.wait_sentence(1)
            self.play(FadeIn(sheets), run_time=1.0)
            self.play(FadeIn(four), run_time=0.8)

        # ---------------- gab6: normalisation does not matter
        conv = VGroup(MathTex(r'\text{Huang: } g_H = 2g:\quad \text{radius } \tfrac{1}{\sqrt2},\ \ K_G = 2', font_size=32),
                      MathTex(r'K_G\,dA\ \text{unchanged} \;\Rightarrow\; \text{the same } 2.378', font_size=32, color=C_FOLD),
                      txt('(also: H3\'s Berry curvature has the opposite sign to H2\'s)', 22, GREY_T)
                      ).arrange(DOWN, buff=0.22).move_to([0, -2.6, 0])
        with self.narrate('gab6') as b:
            self.play(FadeIn(conv[0]), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(conv[1]), run_time=1.2)
            self.play(FadeIn(conv[2]), run_time=0.8)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
