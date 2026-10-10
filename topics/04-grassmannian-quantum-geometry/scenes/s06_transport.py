import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

EL, AZ = 0.42, 0.35
SPH_C, SPH_R = np.array([-2.2, -0.45, 0]), 2.7
BG = np.load(ROOT / 'data' / 'bargmann.npz')


def rot(axis, ang):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    K = np.array([[0, -axis[2], axis[1]], [axis[2], 0, -axis[0]], [-axis[1], axis[0], 0]])
    return np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * K @ K


def spinor(n):
    th = np.arccos(np.clip(n[2], -1, 1))
    ph = np.arctan2(n[1], n[0])
    return np.array([np.cos(th / 2), np.exp(1j * ph) * np.sin(th / 2)])


def solid_angle(a, b, c):
    return 2 * np.arctan2(np.dot(a, np.cross(b, c)), 1 + a @ b + b @ c + c @ a)


def loop_pts(t):
    th = 0.95 + 0.28 * np.cos(3 * t)
    return np.stack([np.sin(th) * np.cos(t), np.sin(th) * np.sin(t), np.cos(th)], -1)


class S06_Transport(NScene):
    def construct(self):
        tag = txt('[H2]', 26, GREY_T).to_corner(UL, buff=0.4)
        title = txt('Geodesics and holonomy', 40, bold=True).to_edge(UP, buff=0.35)
        sph = Sphere2D(radius=SPH_R, el=EL, az=AZ, n_merid=3).move_to(SPH_C)
        sph_first = sph
        cam_dir = sph.basis()[0]

        # octant triangle rotated to face the viewer
        tgt = cam_dir + 0.25 * np.array([0, 0, 1.0])
        tgt /= np.linalg.norm(tgt)
        o = np.ones(3) / np.sqrt(3)
        R = rot(np.cross(o, tgt), np.arccos(np.clip(o @ tgt, -1, 1)))
        V = [R @ e for e in np.eye(3)]
        v1, v2, v3 = V[0], V[1], V[2]
        S = solid_angle(v1, v2, v3)
        if S < 0:
            v2, v3 = v3, v2
            S = solid_angle(v1, v2, v3)

        # ---------------- tra1: geodesics
        geo = MathTex(r'P(t) = e^{tX}P_0\,e^{-tX},\qquad X = [\dot P_0, P_0]', font_size=36).move_to([3.9, 2.45, 0])
        geo_l = txt('geodesic: exponentiate the projector\'s derivative', 24, GREY_A).next_to(geo, DOWN, buff=0.2)
        full_gc = sph.curve([rot(np.cross(v1, v2), t) @ v1 for t in np.linspace(0, TAU, 200)], color=GREY_B, width=1.5,
                            back_opacity=0.15, front_opacity=0.55)
        arc12 = sph.curve(slerp_path(v1, v2, 60), color=C_GEO, width=5)
        d1, d2 = sph.dot(v1, WHITE, 0.08), sph.dot(v2, WHITE, 0.08)
        gcl = txt('great circle', 26, GREY_B).move_to(SPH_C + 3.0 * DOWN + 1.6 * RIGHT)
        with self.narrate('tra1') as b:
            self.play(FadeIn(tag), Write(title), FadeIn(sph), run_time=1.2)
            self.play(FadeIn(d1), FadeIn(d2), run_time=0.6)
            self.play(Create(arc12), run_time=1.2)
            b.wait_sentence(1)
            self.play(Write(geo), FadeIn(geo_l), run_time=2.0)
            b.wait_sentence(2)
            self.play(Create(full_gc), FadeIn(gcl), run_time=1.5)

        # ---------------- tra2: parallel transport around a geodesic triangle
        arc23 = sph.curve(slerp_path(v2, v3, 60), color=C_GEO, width=5)
        arc31 = sph.curve(slerp_path(v3, v1, 60), color=C_GEO, width=5)
        d3 = sph.dot(v3, WHITE, 0.08)
        tri_fill = Polygon(*[sph.p(p) for p in slerp_path(v1, v2, 30) + slerp_path(v2, v3, 30) + slerp_path(v3, v1, 30)],
                           stroke_width=0, fill_color=C_UP, fill_opacity=0.18)
        # transported vector: rotation about each edge's pole is parallel transport along a great circle
        t_dir = np.cross(np.cross(v1, v2), v1)
        w0 = rot(v1, 0.9) @ (t_dir / np.linalg.norm(t_dir))
        legs = [(v1, v2), (v2, v3), (v3, v1)]
        s = ValueTracker(0.0)

        def state(sv):
            sv = min(max(sv, 0.0), 3.0)
            p, w = v1.copy(), w0.copy()
            for i, (a, c) in enumerate(legs):
                ang = np.arccos(np.clip(a @ c, -1, 1))
                f = min(max(sv - i, 0.0), 1.0)
                Rm = rot(np.cross(a, c), f * ang)
                p, w = Rm @ a, Rm @ w
                if sv < i + 1:
                    break
            return p, w

        L = 0.55

        def arrow_at(p, w, color=C_FOLD, op=1.0):
            return Arrow(sph.p(p), sph.p(p + L * w), buff=0, color=color, stroke_width=5, max_tip_length_to_length_ratio=0.3,
                         stroke_opacity=op, fill_opacity=op)
        arr = always_redraw(lambda: arrow_at(*state(s.get_value())))
        ghosts = VGroup(*[arrow_at(*state(x), color=C_FOLD, op=0.35) for x in np.linspace(0.3, 2.7, 7)])
        with self.narrate('tra2') as b:
            self.play(FadeOut(full_gc), FadeOut(gcl), Create(arc23), Create(arc31), FadeIn(d3), FadeIn(tri_fill), run_time=1.4)
            self.add(arr)
            self.play(FadeIn(arr), run_time=0.4)
            self.play(s.animate.set_value(3.0), LaggedStart(*[FadeIn(g) for g in ghosts], lag_ratio=0.35),
                      run_time=b.until_sentence(1, 3.0), rate_func=linear)
            start = arrow_at(v1, w0, color=WHITE, op=0.9)
            self.play(FadeIn(start), run_time=0.6)

        # ---------------- tra3: turning angle = K x area = solid angle
        _, wend = state(3.0)
        turn = np.arctan2(np.dot(v1, np.cross(w0, wend)), w0 @ wend)
        ang_arc = sph.curve([v1 + 0.32 * (rot(v1, t) @ w0) for t in np.linspace(0, turn, 30)], color=YELLOW, width=4)
        rule = MathTex(r'\text{turn} = K_G\times\text{area} = 4\times\tfrac{S}{4} = S', font_size=38).move_to([3.9, 1.0, 0])
        val = MathTex(r'S = ' + f'{abs(S):.4f}' + r'\ (=\pi/2)', font_size=34, color=YELLOW).next_to(rule, DOWN, buff=0.25)
        with self.narrate('tra3') as b:
            self.play(Create(ang_arc), run_time=0.8)
            self.play(Write(rule), run_time=2.0)
            self.play(FadeIn(val), run_time=0.8)

        # ---------------- tra4: Bargmann invariant
        u = [spinor(v) for v in (v1, v2, v3)]
        Bv = np.vdot(u[0], u[1]) * np.vdot(u[1], u[2]) * np.vdot(u[2], u[0])
        labs = VGroup(*[MathTex(rf'|u_{i}\rangle', font_size=32).next_to(sph.p(v), d, buff=0.08)
                        for i, (v, d) in enumerate([(v1, DL), (v2, UR), (v3, DR)], start=1)])
        barg = MathTex(r'B = \langle u_1|u_2\rangle\langle u_2|u_3\rangle\langle u_3|u_1\rangle = \mathrm{tr}(P_1P_2P_3)', font_size=34)
        barg.move_to([3.9, -0.5, 0])
        bval = MathTex(r'\arg B = ' + f'{np.angle(Bv):.4f}' + r' = \tfrac{S}{2}', font_size=34, color=C_G).next_to(barg, DOWN, buff=0.25)
        berry = MathTex(r'\gamma_{\rm Berry} = -\arg B', font_size=34, color=C_G).next_to(bval, DOWN, buff=0.2)
        with self.narrate('tra4') as b:
            self.play(FadeIn(labs), run_time=0.8)
            b.wait_sentence(1)
            self.play(Write(barg), run_time=2.4)
            b.wait_sentence(2)
            self.play(Write(bval), run_time=1.6)
            self.play(FadeIn(berry), run_time=0.8)

        # ---------------- tra5: arrow S, state S/2
        cmp = VGroup(txt('tangent arrow turns by $S$', 30, C_FOLD), txt('quantum state: phase $S/2$', 30, C_G)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.9, -2.85, 0])
        with self.narrate('tra5') as b:
            self.play(FadeIn(cmp[0]), run_time=0.8)
            self.play(FadeIn(cmp[1]), run_time=0.8)
            b.wait_sentence(1)
            self.play(Indicate(cmp, scale_factor=1.05), run_time=1.2)

        # ---------------- tra6: polygons converge to the smooth-loop Berry phase
        arr.clear_updaters()
        tt = np.linspace(0, TAU, 300)
        sph = Sphere2D(radius=SPH_R, el=1.0, az=AZ, n_merid=3).move_to(SPH_C)      # look down on the loop
        smooth = sph.curve(list(loop_pts(tt)), color=WHITE, width=3, back_opacity=0.3)
        Ns, phases, Sloop = BG['Ns'], BG['phases'], float(BG['S'])
        Ni = ValueTracker(0)

        def poly():
            N = int(Ns[int(Ni.get_value())])
            vs = loop_pts(TAU * np.arange(N) / N)
            pts = []
            for i in range(N):
                pts += slerp_path(vs[i], vs[(i + 1) % N], 20)
            g = VGroup(sph.curve(pts, color=C_G, width=3.5, back_opacity=0.3))
            for v in vs:
                g.add(sph.dot(v, C_G, 0.05))
            return g
        pol = always_redraw(poly)

        def table():
            k = int(Ni.get_value())
            rows = VGroup(*[MathTex(rf'N={int(Ns[i])}:\ \ \gamma = {phases[i]:+.4f}', font_size=28,
                                    color=C_G if i == k else GREY_B) for i in range(k + 1)])
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.08).move_to([4.0, 0.6, 0], aligned_edge=UP)
            return rows
        tab = always_redraw(table)
        target = MathTex(r'\text{smooth loop: } -\tfrac{S}{2} = ' + f'{-Sloop / 2:+.4f}', font_size=30, color=WHITE).move_to([4.0, 1.2, 0])
        with self.narrate('tra6') as b:
            self.play(FadeOut(VGroup(arc12, arc23, arc31, d1, d2, d3, tri_fill, ghosts, start, ang_arc, labs, rule, val,
                                     barg, bval, berry, cmp, geo, geo_l, sph_first)), FadeOut(arr), FadeIn(sph), run_time=0.9)
            b.wait_sentence(1)
            self.play(Create(smooth), FadeIn(target), run_time=1.4)
            self.add(pol, tab)
            for i in range(1, len(Ns)):
                self.play(Ni.animate.set_value(i), run_time=0.55, rate_func=lambda x: 1.0 if x > 0.5 else 0.0)
            self.wait(0.3)
            self.play(Circumscribe(target, color=C_G), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
