import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def card(title, body, color, width=6.2, height=2.15):
    box = RoundedRectangle(width=width, height=height, corner_radius=0.15, stroke_color=color, stroke_width=2,
                           fill_color=C_PANEL, fill_opacity=0.95)
    t = txt(title, 30, color, bold=True)
    bd = txt(body, 24, GREY_A)
    VGroup(t, bd).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to(box).align_to(box, LEFT).shift(0.3 * RIGHT)
    return VGroup(box, t, bd)


def skyrmion(center, r=0.85, n=3):
    g = VGroup()
    c = np.asarray(center, float)
    g.add(Dot(c, radius=0.06, color=C_POS))
    for ring_i in range(1, n + 1):
        rr = r * ring_i / n
        m = 6 * ring_i
        for j in range(m):
            ph = TAU * j / m
            p = c + rr * np.array([np.cos(ph), np.sin(ph), 0])
            tilt = PI * ring_i / n            # out-of-plane angle grows outward
            d = np.array([np.cos(ph), np.sin(ph), 0]) * 0.18 * np.sin(tilt)
            col = interpolate_color(ManimColor(C_POS), ManimColor(C_NEG), ring_i / n)
            if np.linalg.norm(d) < 0.02:
                g.add(Dot(p, radius=0.045, color=col))
            else:
                g.add(Arrow(p - d, p + d, buff=0, color=col, stroke_width=3, max_tip_length_to_length_ratio=0.45))
    return g


class S11_Outlook(NScene):
    def construct(self):
        # ---------------- out1: one tensor, two geometries
        qgt = MathTex(r'G_{ij}', '=', r'g_{ij}', '-', r'\frac{i}{2}', r'\Omega_{ij}', font_size=60).to_edge(UP, buff=0.5)
        qgt[2].set_color(C_G); qgt[5].set_color(C_POS)
        with self.narrate('out1') as b:
            b.wait_sentence(1)
            self.play(Write(qgt), run_time=1.8)

        # ---------------- out2: summary table
        lh = VGroup(txt('Berry curvature', 34, C_POS, bold=True), txt('imaginary part', 24, GREY_T)).arrange(DOWN, buff=0.08)
        rh = VGroup(txt('quantum metric', 34, C_G, bold=True), txt('real part', 24, GREY_T)).arrange(DOWN, buff=0.08)
        litems = VGroup(*[txt(s, 28) for s in ['anomalous Hall effect', 'quantum anomalous Hall (and fractional)',
                                                'valley, spin, layer Hall effects', 'Berry curvature dipole Hall effect']])
        ritems = VGroup(*[txt(s, 28) for s in ['size of Wannier orbitals', 'optical sum rules, gap bounds',
                                                'flat-band superfluid stiffness', 'intrinsic nonlinear Hall effect']])
        litems.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        ritems.arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        lcol = VGroup(lh, litems).arrange(DOWN, buff=0.4).move_to([-3.4, -0.6, 0])
        rcol = VGroup(rh, ritems).arrange(DOWN, buff=0.4).move_to([3.4, -0.6, 0])
        sep = Line([0, 1.6, 0], [0, -3.0, 0], color=GREY_D)
        with self.narrate('out2') as b:
            self.play(FadeIn(lh, shift=0.2 * DOWN), Indicate(qgt[5], color=C_POS), Create(sep), run_time=1.2)
            for it in litems:
                self.play(FadeIn(it, shift=0.15 * RIGHT), run_time=0.7)
            b.wait_sentence(1)
            self.play(FadeIn(rh, shift=0.2 * DOWN), Indicate(qgt[2], color=C_G), run_time=1.2)
            for it in ritems:
                self.play(FadeIn(it, shift=0.15 * RIGHT), run_time=0.9)
                self.wait(0.6)

        # ---------------- out3: outlook part 1
        otitle = txt('Outlook', 44, bold=True).to_edge(UP, buff=0.45)
        c1 = card('High-harmonic generation', 'divergent geometry at band crossings:\\\\nonperturbative even at weak fields', C_E)
        c2 = card('Fractional Chern insulators', 'band geometry guides where they appear;\\\\metric fluctuations = chiral gravitons', C_G)
        c3 = card('Real-space geometry', 'skyrmion spin textures,\\\\topological Hall effect', C_POS)
        c4 = card('Quantum information', 'quantum Fisher information\\\\as an entanglement witness', C_B)
        grid4 = VGroup(c1, c2, c3, c4).arrange_in_grid(2, 2, buff=(0.45, 0.4)).move_to([0, -0.5, 0])
        # icons
        hh = VGroup(*[Rectangle(width=0.16, height=h, stroke_width=0, fill_color=C_E, fill_opacity=0.9)
                      for h in [0.9, 0.55, 0.42, 0.33, 0.28]]).arrange(RIGHT, buff=0.09, aligned_edge=DOWN)
        hh.move_to(c1[0].get_right() + 0.75 * LEFT + 0.05 * DOWN)
        cone = MathTex(r'\nu = \tfrac23', font_size=32, color=C_G).move_to(c2[0].get_right() + 0.5 * LEFT + 0.55 * UP)
        sk = skyrmion(c3[0].get_right() + 0.85 * LEFT, r=0.6, n=3)
        ent = VGroup(Circle(radius=0.22, color=C_B), Circle(radius=0.22, color=C_B).shift(0.62 * RIGHT))
        ent.add(Line(ent[0].get_right(), ent[1].get_left(), color=C_B, stroke_width=3))
        ent.move_to(c4[0].get_right() + 0.8 * LEFT)
        with self.narrate('out3') as b:
            self.play(FadeOut(VGroup(lcol, rcol, sep)), qgt.animate.scale(0.5).to_corner(UR, buff=0.4), run_time=0.9)
            self.play(FadeIn(otitle), run_time=0.6)
            b.wait_sentence(1)
            self.play(FadeIn(c1, shift=0.2 * UP), run_time=1.0)
            self.play(LaggedStartMap(GrowFromEdge, hh, edge=DOWN, lag_ratio=0.2), run_time=1.4)
            b.wait_sentence(2)
            self.play(FadeIn(c2, shift=0.2 * UP), run_time=1.0)
            self.play(Write(cone), run_time=0.8)

        # ---------------- out4: outlook part 2
        with self.narrate('out4') as b:
            self.play(FadeIn(c3, shift=0.2 * UP), FadeIn(sk), run_time=1.2)
            self.play(Rotate(sk, angle=PI / 3), run_time=1.6)
            b.wait_sentence(1)
            self.play(FadeIn(c4, shift=0.2 * UP), FadeIn(ent), run_time=1.2)

        # ---------------- out5: closing
        big = MathTex(r'g_{ij}(\mathbf k)', font_size=110, color=C_G)
        credit = VGroup(txt('Based on: A. Gao, N. Nagaosa, N. Ni, S.-Y. Xu,', 26, GREY_A),
                        txt('\\emph{Quantum geometry phenomena in condensed matter systems},', 26, GREY_A),
                        txt('Rev. Mod. Phys. \\textbf{98}, 035005 (2026)', 26, GREY_A)).arrange(DOWN, buff=0.12)
        credit.to_edge(DOWN, buff=0.6)
        with self.narrate('out5') as b:
            self.play(FadeOut(Group(grid4, hh, cone, sk, ent, otitle, qgt)), run_time=1.0)
            self.play(FadeIn(big, scale=0.8), run_time=1.4)
            b.wait_sentence(1)
            self.play(big.animate.shift(0.8 * UP), FadeIn(credit, shift=0.2 * UP), run_time=1.0)
        self.wait(1.5)
        self.play(FadeOut(Group(*self.mobjects)), run_time=1.2)
