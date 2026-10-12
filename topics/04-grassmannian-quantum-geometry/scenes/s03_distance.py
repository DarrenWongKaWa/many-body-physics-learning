import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

SPH_C, SPH_R = np.array([3.3, -0.55, 0]), 2.2
EL, AZ = 0.3, 0.35
PHI_DOOR = np.radians(50)


def rotate_about(axis, v, ang):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    v = np.asarray(v, float)
    return v * np.cos(ang) + np.cross(axis, v) * np.sin(ang) + axis * (axis @ v) * (1 - np.cos(ang))


class S03_Distance(NScene):
    def construct(self):
        tag = txt('[H1] Huang \\& Giataganas', 26, GREY_T).to_corner(UL, buff=0.4)
        title = txt('How far apart are two states?', 40, bold=True).to_edge(UP, buff=0.4)
        sph = Sphere2D(radius=SPH_R, el=EL, az=AZ, n_merid=2).move_to(SPH_C)
        # a great circle tilted 30 degrees towards the viewer: n1 on the outline, the arc on the front
        cdir, e1, e2 = sph.basis()
        A = -0.62 * e1 + 0.78 * e2
        A /= np.linalg.norm(A)
        u2 = np.cross(cdir, A)
        B = 0.5 * cdir + 0.866 * (u2 / np.linalg.norm(u2))
        n1 = A
        tt = ValueTracker(1.3)                       # angle between the Bloch vectors = 2 theta

        def n2():
            t = tt.get_value()
            return np.cos(t) * A + np.sin(t) * B

        d1 = sph.dot(n1, WHITE, 0.09)
        d2 = always_redraw(lambda: sph.dot(n2(), C_G, 0.09))
        l1 = MathTex(r'|u\rangle', font_size=32).next_to(sph.p(n1), UL, buff=0.08)
        l2 = always_redraw(lambda: MathTex(r'|v\rangle', font_size=32, color=C_G).next_to(sph.p(n2()), RIGHT, buff=0.1)
                           .set_opacity(float(np.clip((tt.get_value() - 0.35) / 0.4, 0, 1))))

        # ---------------- dis1
        with self.narrate('dis1') as b:
            self.play(FadeIn(tag), Write(title), FadeIn(sph), run_time=1.6)
            self.add(d2, l2)
            self.play(FadeIn(d1), FadeIn(l1), FadeIn(d2), FadeIn(l2), run_time=1.0)

        # ---------------- dis2: projectors, the angle theta
        proj = MathTex(r'P = |u\rangle\langle u|', r'\quad\text{unchanged by}\quad', r'|u\rangle\to e^{i\chi}|u\rangle', font_size=36)
        ang = MathTex(r'\cos\vartheta = |\langle u|v\rangle|', font_size=42, color=YELLOW)
        left = VGroup(proj, ang).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([-3.4, 1.9, 0])
        with self.narrate('dis2') as b:
            self.play(Write(proj), run_time=2.0)
            b.wait_sentence(1)
            self.play(Write(ang), run_time=1.5)

        # ---------------- dis3: two theta at the centre; orthogonal states are antipodal
        c0 = sph.get_center()
        r1 = DashedLine(c0, sph.p(n1), color=GREY_A, stroke_width=2.5)
        r2 = always_redraw(lambda: DashedLine(c0, sph.p(n2()), color=GREY_A, stroke_width=2.5))
        cang = always_redraw(lambda: sph.curve(slerp_path(n1, n2(), 30), color=YELLOW, width=3.5, r=0.3, back_opacity=1.0))
        cang_l = always_redraw(lambda: MathTex(r'2\vartheta', font_size=30, color=YELLOW).move_to(
            sph.p((n1 + n2()) / max(1e-6, np.linalg.norm(n1 + n2())), 0.48) if np.linalg.norm(n1 + n2()) > 0.2
            else c0 + 0.45 * UP).set_opacity(float(np.clip((tt.get_value() - 0.8) / 0.4, 0, 1))))
        orth = VGroup(MathTex(r'\vartheta = 90^\circ', font_size=32), txt('orthogonal states: opposite points', 26, GREY_A)
                      ).arrange(DOWN, buff=0.1).move_to([-3.4, -0.2, 0])
        with self.narrate('dis3') as b:
            self.add(r2, cang, cang_l)
            self.play(Create(r1), FadeIn(r2), FadeIn(cang), FadeIn(cang_l), run_time=1.4)
            b.wait_sentence(1)
            self.play(tt.animate.set_value(np.pi * 0.999), FadeIn(orth), run_time=2.2)

        # ---------------- dis3b: radius 1/2, arc = theta, chord = sin theta
        rad = MathTex(r'\tfrac12', font_size=30, color=GREY_A).next_to(r1.get_center(), UR, buff=0.08)
        rad_t = txt('radius $\\tfrac12$ in the quantum metric', 22, GREY_A).next_to(sph, DOWN, buff=0.15)
        fade_small = lambda m: m.set_opacity(float(np.clip((tt.get_value() - 0.8) / 0.4, 0, 1)))
        arc = always_redraw(lambda: sph.curve(slerp_path(n1, n2(), 60), color=C_G, width=6))
        chord = always_redraw(lambda: Line(sph.p(n1), sph.p(n2()), color=C_UP, stroke_width=5))
        arc_l = always_redraw(lambda: fade_small(MathTex(r'\vartheta', font_size=32, color=C_G).move_to(
            sph.p(slerp_path(n1, n2(), 3)[1], 1.12))))

        def chord_label():
            # beside the chord, a third of the way from u, on the side of the centre (clear of the 2 theta label)
            a_, b_ = sph.p(n1), sph.p(n2())
            pt = a_ + 0.3 * (b_ - a_)
            d_ = (b_ - a_) / max(1e-6, np.linalg.norm(b_ - a_))
            perp = np.array([d_[1], -d_[0], 0])
            if np.dot(perp, c0 - pt) < 0:
                perp = -perp
            return fade_small(MathTex(r'\sin\vartheta', font_size=30, color=C_UP).move_to(pt + 0.35 * perp))
        chord_l = always_redraw(chord_label)
        dfs = MathTex(r'd_{\rm FS} = \vartheta', r'\quad\text{(arc)}', font_size=36)
        dfs[0].set_color(C_G)
        dhs = MathTex(r'D_{\rm HS} = \sqrt{\tfrac12\mathrm{tr}(P_1-P_2)^2} = \sin\vartheta', r'\quad\text{(chord)}', font_size=34)
        dhs[0].set_color(C_UP)
        rows = VGroup(dfs, dhs).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, -0.5, 0])
        vals = always_redraw(lambda: VGroup(
            MathTex(r'\vartheta = ' + f'{tt.get_value() / 2:.3f}', font_size=30, color=C_G),
            MathTex(r'\sin\vartheta = ' + f'{np.sin(tt.get_value() / 2):.3f}', font_size=30, color=C_UP)
        ).arrange(RIGHT, buff=0.6).move_to([-3.4, -2.2, 0]))
        with self.narrate('dis3b') as b:
            self.play(FadeOut(orth), tt.animate.set_value(1.3), run_time=1.0)
            self.play(FadeIn(rad), FadeIn(rad_t), run_time=0.8)
            b.wait_sentence(1)
            # FadeIn suspends updaters, and the redraw functions last ran while v sat at the antipode: refresh first
            for m in (arc, arc_l, chord, chord_l):
                m.update()
            self.add(arc, arc_l)
            self.play(FadeIn(arc), FadeIn(arc_l), FadeIn(dfs), run_time=1.4)
            b.wait_sentence(2)
            self.add(chord, chord_l)
            self.play(FadeIn(chord), FadeIn(chord_l), FadeIn(dhs), run_time=1.4)
            vals.update()                                   # always_redraw is not refreshed during a frozen wait
            self.add(vals)
            b.wait_sentence(3)
            self.play(tt.animate.set_value(0.5), run_time=max(1.0, b.remaining(-0.3)), rate_func=smooth)

        # ---------------- dis4/dis5: occupied planes, the floor and the door
        live = [d2, l2, r2, cang, cang_l, arc, chord, arc_l, chord_l, vals]
        for m in live:
            m.clear_updaters()
        cam = Cam(0.42, -0.95, 1.25, center=[3.5, -0.3, 0])
        door = ValueTracker(0.0)
        L = 1.8

        def plane(normal_rot, color, op):
            # unit square spanned by x (hinge) and y rotated about x by normal_rot
            ey = np.array([0, np.cos(normal_rot), np.sin(normal_rot)])
            ex = np.array([1.0, 0, 0])
            P = [-L * ex - 0.1 * ey, L * ex - 0.1 * ey, L * ex + 1.6 * ey, -L * ex + 1.6 * ey]
            return Polygon(*cam.p(np.array(P)), fill_color=color, fill_opacity=op, stroke_color=color, stroke_width=2)
        floor = plane(0.0, C_UP, 0.25)
        door_m = always_redraw(lambda: plane(door.get_value(), C_G, 0.28))
        hinge = Line(cam.p([-L * 1.1, 0, 0]), cam.p([L * 1.1, 0, 0]), color=YELLOW, stroke_width=5)
        o = np.array([0.6, 0, 0])
        u2 = Arrow(cam.p(o), cam.p(o + np.array([0, 1.4, 0])), buff=0, color=C_UP, stroke_width=5)
        v2 = always_redraw(lambda: Arrow(cam.p(o), cam.p(o + 1.4 * np.array([0, np.cos(door.get_value()), np.sin(door.get_value())])),
                                         buff=0, color=C_G, stroke_width=5))
        u1 = Arrow(cam.p(o), cam.p(o + np.array([1.0, 0, 0])), buff=0, color=YELLOW, stroke_width=5)
        darc = always_redraw(lambda: VMobject(stroke_color=WHITE, stroke_width=3).set_points_as_corners(
            [cam.p(o + 0.55 * np.array([0, np.cos(a), np.sin(a)])) for a in np.linspace(0, max(1e-3, door.get_value()), 20)]))
        lab_f = txt('occupied states at $\\mathbf k_1$', 24, C_UP).move_to(cam.p([-1.0, -0.1, 0]) + 0.6 * DOWN)
        lab_d = always_redraw(lambda: txt('occupied states at $\\mathbf k_2$', 24, C_G).move_to(
            cam.p(np.array([-1.3, 1.6 * np.cos(door.get_value()), 1.6 * np.sin(door.get_value())])) + 0.35 * UP))
        lu1 = MathTex(r'u_1 = v_1', font_size=30, color=YELLOW).next_to(u1.get_end(), DOWN, buff=0.12)
        lu2 = MathTex('u_2', font_size=30, color=C_UP).next_to(u2.get_end(), RIGHT, buff=0.08)
        lv2 = always_redraw(lambda: MathTex('v_2', font_size=30, color=C_G).next_to(v2.get_end(), UP, buff=0.08))
        ang1 = MathTex(r'\vartheta_1 = 0', font_size=32, color=YELLOW)
        ang2 = MathTex(r'\vartheta_2 = \text{opening angle}', font_size=32, color=C_G)
        angs = VGroup(ang1, ang2).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-4.0, 1.3, 0])
        two = txt('two occupied bands: a 2D subspace at each $\\mathbf k$', 28, GREY_A).move_to([-3.2, 2.3, 0])
        with self.narrate('dis4') as b:
            self.play(FadeOut(VGroup(sph, d1, l1, r1, rad, rad_t, rows, proj, ang, *live)), run_time=0.9)
            self.play(FadeIn(two), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(floor), FadeIn(lab_f), run_time=1.2)
            b.wait_sentence(3)
            self.add(door_m, lab_d)
            self.play(FadeIn(door_m), FadeIn(lab_d), door.animate.set_value(PHI_DOOR * 0.4), run_time=1.4)
        with self.narrate('dis5') as b:
            self.play(door.animate.set_value(PHI_DOOR), run_time=1.6)
            b.wait_sentence(1)
            self.play(Create(hinge), GrowArrow(u1), FadeIn(lu1), FadeIn(ang1), run_time=1.4)
            b.wait_sentence(2)
            self.add(v2, darc, lv2)
            self.play(GrowArrow(u2), FadeIn(lu2), FadeIn(v2), FadeIn(darc), FadeIn(lv2), FadeIn(ang2), run_time=1.6)

        # ---------------- dis5b: SVD of the overlap matrix; basis independence; the distance
        svd = MathTex(r'\Psi_1^\dagger\Psi_2 = U\,\mathrm{diag}(\cos\vartheta_1,\cos\vartheta_2)\,V^\dagger', font_size=34)
        pair = MathTex(r'u = \Psi_1U,\quad v = \Psi_2V:\qquad \langle u_a|v_b\rangle = \delta_{ab}\cos\vartheta_a', font_size=32)
        inv = txt('the same angles for any basis inside each plane', 26, GREY_A)
        hs = MathTex(r'D_{\rm HS}^2 = \tfrac12\mathrm{tr}(P_1-P_2)^2 = \sin^2\vartheta_1 + \sin^2\vartheta_2', font_size=34, color=C_UP)
        sk = txt('(a real sketch: for complex planes in more dimensions both angles can be nonzero)', 22, GREY_B)
        block = VGroup(svd, pair, inv, hs, sk).arrange(DOWN, buff=0.2, aligned_edge=LEFT).scale(0.9).move_to([-3.4, -1.75, 0])
        with self.narrate('dis5b') as b:
            self.play(FadeOut(two), Write(svd), run_time=2.0)
            self.play(FadeIn(pair), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(inv), run_time=0.8)
            self.play(Write(hs), FadeIn(sk), run_time=1.6)
        for m in (door_m, lab_d, v2, darc, lv2):
            m.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
