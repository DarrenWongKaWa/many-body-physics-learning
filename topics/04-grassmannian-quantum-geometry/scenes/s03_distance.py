import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

TH1, TH2 = 0.64, 1.12          # principal angles of the two-plane example


def dial(center, radius, angle_tracker, final, color_a=C_UP, color_b=C_G, label='1'):
    c = np.asarray(center, float)
    circ = Circle(radius=radius, stroke_color=GREY_D, stroke_width=1.5).move_to(c)
    ua = Arrow(c, c + radius * RIGHT, buff=0, color=color_a, stroke_width=5)
    ub = always_redraw(lambda: Arrow(c, c + radius * np.array([np.cos(angle_tracker.get_value() * final),
                                                                np.sin(angle_tracker.get_value() * final), 0]),
                                     buff=0, color=color_b, stroke_width=5))
    arc = always_redraw(lambda: Arc(radius=0.45 * radius, start_angle=0, angle=max(1e-3, angle_tracker.get_value() * final),
                                    color=YELLOW, stroke_width=3).move_arc_center_to(c))
    lu = MathTex(rf'u_{label}', font_size=30, color=color_a).next_to(c + radius * RIGHT, DOWN, buff=0.1)
    lv = MathTex(rf'v_{label}', font_size=30, color=color_b).move_to(c + 1.22 * radius * np.array([np.cos(final), np.sin(final), 0]))
    lth = MathTex(rf'\vartheta_{label}', font_size=30, color=YELLOW).move_to(c + 0.62 * radius * np.array([np.cos(final / 2), np.sin(final / 2), 0]))
    return VGroup(circ, ua, ub, arc, lu, lv, lth)


class S03_Distance(NScene):
    def construct(self):
        tag = txt('[H1] Huang \\& Giataganas', 26, GREY_T).to_corner(UL, buff=0.4)
        title = txt('How far apart are two states?', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- dis1
        with self.narrate('dis1') as b:
            self.play(FadeIn(tag), Write(title), run_time=1.6)

        # ---------------- dis2: projectors, principal angle
        proj = MathTex(r'P = |u\rangle\langle u|', r'\quad\text{unchanged by}\quad', r'|u\rangle\to e^{i\chi}|u\rangle', font_size=38)
        ang = MathTex(r'\cos\vartheta = |\langle u|v\rangle|', font_size=42, color=YELLOW)
        left = VGroup(proj, ang).arrange(DOWN, buff=0.5, aligned_edge=LEFT).move_to([-3.3, 1.2, 0])
        with self.narrate('dis2') as b:
            self.play(Write(proj), run_time=2.2)
            b.wait_sentence(1)
            self.play(Write(ang), run_time=1.6)

        # ---------------- dis3: chord and arc on the sphere of radius 1/2
        sph = Sphere2D(radius=2.1, el=0.3, az=0.35, n_merid=2).move_to([3.5, -0.6, 0])
        rad = MathTex(r'\text{radius } \tfrac12', font_size=28, color=GREY_B).next_to(sph, DOWN, buff=0.2)
        n1 = bloch_vec(1.05, 0.15)
        tt = ValueTracker(1.5)                                 # Bloch-sphere angle between the two states (= 2 theta)

        def n2():
            # rotate n1 about an axis orthogonal to it by tt
            ax_ = np.cross(n1, [0, 0, 1.0]); ax_ /= np.linalg.norm(ax_)
            ax_ = np.cos(0.6) * ax_ + np.sin(0.6) * np.cross(n1, ax_)
            t = tt.get_value()
            return np.cos(t) * n1 + np.sin(t) * np.cross(ax_, n1)

        d1 = sph.dot(n1, WHITE, 0.09)
        d2 = always_redraw(lambda: sph.dot(n2(), C_G, 0.09))
        chord = always_redraw(lambda: Line(sph.p(n1), sph.p(n2()), color=C_UP, stroke_width=5))
        arc = always_redraw(lambda: sph.curve(slerp_path(n1, n2(), 60), color=YELLOW, width=5))
        l1 = MathTex(r'P_1', font_size=32).next_to(sph.p(n1), UL, buff=0.06)
        l2 = always_redraw(lambda: MathTex(r'P_2', font_size=32, color=C_G).next_to(sph.p(n2()), DR, buff=0.06)
                           .set_opacity(float(np.clip((tt.get_value() - 0.35) / 0.4, 0, 1))))
        dhs = MathTex(r'D_{\rm HS} = \sqrt{\tfrac12\mathrm{tr}(P_1-P_2)^2} = \sin\vartheta', font_size=36, color=C_UP)
        dfs = MathTex(r'd_{\rm FS} = \vartheta', font_size=36, color=YELLOW)
        lab_c = txt('chord', 28, C_UP)
        lab_a = txt('arc', 28, YELLOW)
        rows = VGroup(VGroup(lab_c, dhs).arrange(RIGHT, buff=0.3), VGroup(lab_a, dfs).arrange(RIGHT, buff=0.3)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-3.3, -1.0, 0])
        vals = always_redraw(lambda: VGroup(
            MathTex(r'\vartheta = ' + f'{tt.get_value() / 2:.3f}', font_size=32, color=YELLOW),
            MathTex(r'\sin\vartheta = ' + f'{np.sin(tt.get_value() / 2):.3f}', font_size=32, color=C_UP)
        ).arrange(RIGHT, buff=0.6).move_to([-3.3, -2.75, 0]))
        with self.narrate('dis3') as b:
            self.play(FadeIn(sph), FadeIn(rad), FadeIn(d1), FadeIn(l1), run_time=1.0)
            self.add(chord, arc, d2, l2)
            self.play(FadeIn(d2), FadeIn(l2), run_time=0.6)
            b.wait_sentence(1)
            self.play(Create(chord), FadeIn(rows[0]), run_time=1.4)
            b.wait_sentence(2)
            self.play(FadeIn(rows[1]), run_time=1.2)
            self.add(vals)
            b.wait_sentence(3)
            self.play(tt.animate.set_value(0.12), run_time=b.remaining(-0.3), rate_func=smooth)

        # ---------------- dis4: several bands: planes and principal angles
        st = ValueTracker(0.0)
        dA = dial([-4.8, -0.9, 0], 1.25, st, TH1, label='1')
        dB = dial([-1.2, -0.9, 0], 1.25, st, TH2, label='2')
        planes = txt('occupied states of two bands: a plane in $\\mathbb C^N$', 30, GREY_A).move_to([-3.0, 1.65, 0])
        pa = txt('matching pairs turn by their own angles', 28, GREY_A).move_to([-3.0, 0.95, 0])
        sk = txt('(a real sketch of complex planes)', 22, GREY_D).next_to(VGroup(dA, dB), DOWN, buff=0.25)
        with self.narrate('dis4') as b:
            self.play(FadeOut(VGroup(sph, rad, d1, l1, rows, proj, ang)), FadeOut(chord), FadeOut(arc), FadeOut(d2), FadeOut(l2),
                      FadeOut(vals), run_time=0.8)
            self.play(FadeIn(planes), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(dA), FadeIn(dB), FadeIn(pa), FadeIn(sk), run_time=1.0)
            self.play(st.animate.set_value(1.0), run_time=2.5, rate_func=smooth)

        # ---------------- dis5: SVD, basis independence, the HS distance
        e = np.eye(4)
        Psi1 = np.stack([e[0], e[1]], 1).astype(complex)
        Psi2 = np.stack([np.cos(TH1) * e[0] + np.sin(TH1) * e[2], np.cos(TH2) * e[1] + np.sin(TH2) * e[3]], 1).astype(complex)
        rot = ValueTracker(0.0)

        def U(t):
            a, b2, c2 = 1.3 * t, 0.7 * t, 2.1 * t
            return np.array([[np.cos(a), -np.exp(1j * b2) * np.sin(a)], [np.exp(1j * c2) * np.sin(a), np.exp(1j * (b2 + c2)) * np.cos(a)]])

        def overlap():
            return (Psi1 @ U(rot.get_value())).conj().T @ Psi2

        def mat():
            M = overlap()
            ent = [[f'{abs(M[i, j]):.2f}' for j in range(2)] for i in range(2)]
            return MathTex(r'|\Psi_1^\dagger\Psi_2| = \begin{pmatrix}' + ent[0][0] + '&' + ent[0][1] + r'\\' + ent[1][0] + '&' + ent[1][1]
                           + r'\end{pmatrix}', font_size=34).move_to([4.0, 1.0, 0])

        def svals():
            s = np.linalg.svd(overlap(), compute_uv=False)
            return MathTex(r'\text{singular values: } ' + f'{s[0]:.2f},\\ {s[1]:.2f}', font_size=32, color=YELLOW).move_to([4.0, -0.15, 0])
        M_ = always_redraw(mat)
        S_ = always_redraw(svals)
        cosl = MathTex(r'= \cos\vartheta_1,\ \cos\vartheta_2', font_size=32, color=YELLOW).move_to([4.0, -0.75, 0])
        hs = MathTex(r'D_{\rm HS}^2 = \tfrac12\mathrm{tr}(P_1-P_2)^2 = \sin^2\vartheta_1 + \sin^2\vartheta_2', font_size=38, color=C_UP)
        hs.to_edge(DOWN, buff=0.45)
        with self.narrate('dis5') as b:
            self.play(FadeOut(pa), run_time=0.6)
            self.add(M_, S_)
            self.play(FadeIn(M_), FadeIn(S_), FadeIn(cosl), run_time=1.0)
            rl = txt('rotate the basis inside plane 1', 24, GREY_T).next_to(M_, UP, buff=0.3)
            self.play(FadeIn(rl), rot.animate.set_value(2.5), run_time=b.until_sentence(1, 2.0), rate_func=linear)
            self.play(Write(hs), rot.animate.set_value(3.2), run_time=2.2, rate_func=linear)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
