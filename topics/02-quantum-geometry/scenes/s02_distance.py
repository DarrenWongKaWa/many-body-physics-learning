import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class S02_Distance(NScene):
    def construct(self):
        title = txt('How far apart are two quantum states?', 40, bold=True).to_edge(UP, buff=0.4)

        # ---------------- dist1: naive distance
        O = np.array([-3.6, -1.6, 0])
        u_tip, v_tip = O + np.array([2.6, 2.4, 0]), O + np.array([3.4, 1.0, 0])
        u = Arrow(O, u_tip, buff=0, color=WHITE, stroke_width=5)
        v = Arrow(O, v_tip, buff=0, color=GREY_B, stroke_width=5)
        ul = MathTex(r'|u\rangle', font_size=38).next_to(u_tip, UL, buff=0.05)
        vl = MathTex(r'|v\rangle', font_size=38, color=GREY_B).next_to(v_tip, RIGHT, buff=0.1)
        diff = DashedLine(v_tip, u_tip, color=YELLOW, stroke_width=4)
        naive = MathTex(r'\| u - v \|^2', '=', r'\langle u-v\,|\,u-v\rangle', font_size=40).move_to([3.1, 1.6, 0])
        naive[0].set_color(YELLOW)
        with self.narrate('dist1') as b:
            self.play(Write(title), run_time=1.4)
            self.play(GrowArrow(u), GrowArrow(v), FadeIn(ul), FadeIn(vl), run_time=1.2)
            b.wait_sentence(1)
            self.play(Create(diff), Write(naive), run_time=1.5)
            b.wait_sentence(2)
            cross = Cross(naive, stroke_color=C_POS, stroke_width=5)
            self.play(Create(cross), run_time=0.6)

        # ---------------- dist2: global phase -> rays
        phi = ValueTracker(0.0)
        circ_c, R = np.array([-2.6, -0.6, 0]), 1.9
        circle = DashedVMobject(Circle(radius=R, color=GREY_B, stroke_width=2).move_to(circ_c), num_dashes=50)
        u0 = Arrow(circ_c, circ_c + R * RIGHT, buff=0, color=WHITE, stroke_width=5)
        u0l = MathTex(r'|u\rangle', font_size=36).next_to(u0.get_end(), DR, buff=0.08)
        uphi = always_redraw(lambda: Arrow(circ_c, circ_c + R * np.array([np.cos(phi.get_value()), np.sin(phi.get_value()), 0]),
                                           buff=0, color=C_A, stroke_width=5))
        uphil = always_redraw(lambda: MathTex(r'e^{i\varphi}|u\rangle', font_size=36, color=C_A).move_to(
            circ_c + 1.32 * R * np.array([np.cos(phi.get_value()), np.sin(phi.get_value()), 0])))
        chord = always_redraw(lambda: Line(circ_c + R * RIGHT,
                                           circ_c + R * np.array([np.cos(phi.get_value()), np.sin(phi.get_value()), 0]),
                                           color=YELLOW, stroke_width=4))
        lhs = MathTex(r'\|\,u - e^{i\varphi}u\,\| =', font_size=38)
        num = always_redraw(lambda: DecimalNumber(2 * abs(np.sin(phi.get_value() / 2)), num_decimal_places=2,
                                                  font_size=38, color=YELLOW).next_to(lhs, RIGHT, buff=0.15))
        rhs2 = MathTex(r'|\langle u\,|\,e^{i\varphi}u\rangle|^2 = 1', font_size=38, color=C_J)
        grp = VGroup(lhs, rhs2).arrange(DOWN, aligned_edge=LEFT, buff=0.6).move_to([3.2, 0.6, 0])
        same = txt('same physical state', 30, C_J).next_to(rhs2, DOWN, buff=0.3, aligned_edge=LEFT)
        ray = txt('a state is a \\emph{ray}: a whole circle of phases', 32, GREY_A).move_to([1.3, -3.1, 0])
        with self.narrate('dist2') as b:
            self.play(FadeOut(VGroup(u, v, ul, vl, diff, cross)), naive.animate.scale(0.8).move_to([3.2, 2.2, 0]).set_opacity(0.35),
                      run_time=0.9)
            self.play(GrowArrow(u0), FadeIn(u0l), run_time=0.7)
            self.add(uphi, chord, uphil)
            self.play(FadeIn(lhs), FadeIn(rhs2), run_time=0.8)
            self.add(num)
            self.play(phi.animate.set_value(2.4), run_time=b.until_sentence(1, 1.0))
            self.play(Indicate(num, color=YELLOW), run_time=1.0)
            self.play(phi.animate.set_value(PI), FadeIn(same), run_time=1.2)
            b.wait_sentence(2)
            self.play(Create(circle), phi.animate.set_value(TAU + 0.6), run_time=3.0)
            self.play(FadeIn(ray, shift=0.2 * UP), run_time=0.8)

        # ---------------- dist3: decompose a small change (Fig. 2 of the review)
        self.play(FadeOut(VGroup(circle, u0, u0l, uphi, uphil, chord, lhs, num, rhs2, same, ray, naive)), run_time=0.8)
        O = np.array([-5.8, -2.7, 0])
        d_u = np.array([3.3, 2.3, 0])
        A = O + d_u                                # tip of |u(lambda)>
        uhat = d_u / np.linalg.norm(d_u)
        perp = np.array([-uhat[1], uhat[0], 0])
        par_len, perp_len = 1.1, 1.7
        B = A + par_len * uhat + perp_len * perp    # tip of |u(lambda + dlambda)>
        ray_line = DashedLine(O - 0.4 * uhat, A + 2.7 * uhat, color=GREY_B, stroke_width=2, dash_length=0.12)
        vu = Arrow(O, A, buff=0, color=WHITE, stroke_width=5)
        vu2 = Arrow(O, B, buff=0, color=GREY_B, stroke_width=4)
        lu = MathTex(r'|u(\lambda)\rangle', font_size=34).next_to(vu.get_center(), DR, buff=0.12)
        lu2 = MathTex(r'|u(\lambda+d\lambda)\rangle', font_size=34, color=GREY_B).next_to(B, UP, buff=0.12)
        du = Arrow(A, B, buff=0, color=YELLOW, stroke_width=5, max_tip_length_to_length_ratio=0.25)
        ldu = MathTex(r'|du\rangle', font_size=34, color=YELLOW).next_to(du.get_center(), LEFT, buff=0.15)
        dpar = Arrow(A, A + par_len * uhat, buff=0, color=C_POS, stroke_width=5, max_tip_length_to_length_ratio=0.4)
        dperp = Arrow(A + par_len * uhat, B, buff=0, color=C_G, stroke_width=5, max_tip_length_to_length_ratio=0.3)
        lpar = MathTex(r'|d_\parallel u\rangle', font_size=32, color=C_POS).next_to(dpar, DR, buff=0.05)
        lperp = MathTex(r'|d_\perp u\rangle', font_size=32, color=C_G).next_to(dperp, RIGHT, buff=0.1)
        ra = RightAngle(Line(A + par_len * uhat, A), Line(A + par_len * uhat, B), length=0.2, color=GREY_B, quadrant=(1, 1))
        rl = txt('ray', 26, GREY_B).next_to(ray_line.get_end(), DOWN, buff=0.12)

        eq_par = MathTex(r'|d_\parallel u\rangle', '=', r'|u\rangle\langle u|du\rangle', font_size=38)
        eq_par[0].set_color(C_POS)
        eq_perp = MathTex(r'|d_\perp u\rangle', '=', r'|du\rangle - |u\rangle\langle u|du\rangle', font_size=38)
        eq_perp[0].set_color(C_G)
        tag_par = txt('change of phase only', 26, C_POS)
        tag_perp = txt('genuine change of the state', 26, C_G)
        col = VGroup(eq_par, tag_par, eq_perp, tag_perp).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        tag_par.shift(0.3 * RIGHT); tag_perp.shift(0.3 * RIGHT)
        eq_perp.shift(0.25 * DOWN); tag_perp.shift(0.25 * DOWN)
        col.move_to([3.0, 1.2, 0])
        with self.narrate('dist3') as b:
            self.play(Create(ray_line), GrowArrow(vu), FadeIn(lu), FadeIn(rl), run_time=1.2)
            self.play(GrowArrow(vu2), FadeIn(lu2), run_time=0.8)
            self.play(GrowArrow(du), FadeIn(ldu), run_time=0.8)
            b.wait_sentence(1)
            self.play(GrowArrow(dpar), FadeIn(lpar), FadeIn(eq_par), FadeIn(tag_par), run_time=1.3)
            b.wait_sentence(2)
            self.play(GrowArrow(dperp), Create(ra), FadeIn(lperp), FadeIn(eq_perp), FadeIn(tag_perp), run_time=1.3)

        # ---------------- dist4: the metric
        ds = MathTex(r'ds^2', '=', r'\|\,d_\perp u\,\|^2', '=', r'\sum_{ij} g_{ij}(\lambda)\, d\lambda_i\, d\lambda_j',
                     font_size=40)
        ds[2].set_color(C_G); ds[4].set_color(C_G)
        fid = MathTex(r'1 - |\langle u(\lambda)\,|\,u(\lambda+d\lambda)\rangle|^2', '=', r'\sum_{ij} g_{ij}\, d\lambda_i\, d\lambda_j',
                      font_size=40)
        fid[2].set_color(C_G)
        VGroup(ds, fid).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([2.2, -1.9, 0])
        with self.narrate('dist4') as b:
            self.play(Indicate(dperp, color=C_G, scale_factor=1.3), run_time=1.0)
            self.play(Write(ds), run_time=2.0)
            mlab = txt('quantum metric', 30, C_G).next_to(ds[4], UP, buff=0.12)
            self.play(FadeIn(mlab), run_time=0.6)
            b.wait_sentence(1)
            self.play(Write(fid), run_time=2.0)

        # ---------------- dist5: Berry connection & curvature
        figure = VGroup(ray_line, vu, vu2, lu, lu2, du, ldu, dpar, dperp, lpar, lperp, ra, rl)
        bc1 = MathTex(r'a_i(\lambda)', '=', r'i\langle u\,|\,\partial_i u\rangle', font_size=40)
        bc1[0].set_color(C_POS)
        bc2 = MathTex(r'|u\rangle \to e^{i\phi(\lambda)}|u\rangle:\quad', r'a_i \to a_i - \partial_i\phi', font_size=36)
        bc3 = MathTex(r'\Omega_{ij}', '=', r'\partial_i a_j - \partial_j a_i', font_size=40)
        bc3[0].set_color(C_POS)
        conn = txt('Berry connection', 30, C_POS)
        curv = txt('Berry curvature (gauge invariant)', 30, C_POS)
        right = VGroup(VGroup(conn, bc1).arrange(DOWN, buff=0.15, aligned_edge=LEFT), bc2,
                       VGroup(curv, bc3).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
                       ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([2.9, 0.1, 0])
        with self.narrate('dist5') as b:
            self.play(FadeOut(VGroup(col, ds, fid, mlab)), figure.animate.scale(0.85).to_corner(DL, buff=0.5), run_time=1.0)
            self.play(Indicate(dpar, color=C_POS, scale_factor=1.4), run_time=0.7)
            b.wait_sentence(1)
            self.play(FadeIn(conn), Write(bc1), run_time=1.3)
            b.wait_sentence(2)
            self.play(FadeIn(bc2), run_time=1.0)
            self.play(FadeIn(curv), Write(bc3), run_time=1.4)

        # ---------------- dist6: the quantum geometric tensor
        qgt = MathTex(r'G_{ij}', '=', r'\langle \partial_i u\,|', r'\,(1 - |u\rangle\langle u|)\,', r'|\,\partial_j u\rangle',
                      font_size=48).move_to([0, 1.3, 0])
        proj = txt('projects out the phase direction', 26, GREY_T).next_to(qgt[3], UP, buff=0.25)
        re_ = MathTex(r'\mathrm{Re}\,G_{ij}', '=', r'g_{ij} = g_{ji}', font_size=42)
        re_[2].set_color(C_G)
        im_ = MathTex(r'\mathrm{Im}\,G_{ij}', '=', r'-\tfrac12\,\Omega_{ij} = \tfrac12\,\Omega_{ji}', font_size=42)
        im_[2].set_color(C_POS)
        re_t = txt('symmetric: quantum metric', 28, C_G)
        im_t = txt('antisymmetric: Berry curvature', 28, C_POS)
        rows = VGroup(VGroup(re_, re_t).arrange(RIGHT, buff=0.5), VGroup(im_, im_t).arrange(RIGHT, buff=0.5)
                      ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, -1.2, 0])
        with self.narrate('dist6') as b:
            self.play(FadeOut(VGroup(figure, right)), title.animate.set_opacity(0.0), run_time=0.9)
            t2 = txt('Quantum geometric tensor', 40, bold=True).to_edge(UP, buff=0.4)
            self.play(FadeIn(t2), Write(qgt), run_time=2.0)
            self.play(qgt[3].animate.set_color(YELLOW), FadeIn(proj), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(rows[0]), run_time=1.2)
            b.wait_sentence(2)
            self.play(FadeIn(rows[1]), run_time=1.2)
        self.play(FadeOut(VGroup(t2, qgt, proj, rows, title)), run_time=0.8)
