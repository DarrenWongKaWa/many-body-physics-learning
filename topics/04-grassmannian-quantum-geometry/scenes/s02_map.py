import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NK = 24
SPH_C, SPH_R = np.array([3.4, -0.25, 0]), 2.25
EL, AZ = 0.42, 0.55


def edge_arrows(ax, color=GREY_A):
    """Identification marks: single arrows on left/right edges, double arrows on bottom/top edges."""
    g = VGroup()
    for x in (0, TAU_K):
        g.add(Arrow(ax.c2p(x, 1.6), ax.c2p(x, 2.9), buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.35))
    for y in (0, TAU_K):
        for dx in (0.0, 0.32):
            g.add(Arrow(ax.c2p(1.6 + dx, y), ax.c2p(2.7 + dx, y), buff=0, color=C_FOLD, stroke_width=4,
                        max_tip_length_to_length_ratio=0.35))
    return g


def painted_mesh(cam, m, opacity=0.78):
    X, cols, om_c = sphere_cells(NK, m)
    return mesh(cam, X, cols, opacity=opacity, back_opacity=0.12, stroke_width=0.4, cull_center=np.zeros(3),
                on_top=om_c < 0), X, cols, om_c


class S02_Map(NScene):
    def construct(self):
        ax, bz = bz_axes(4.4, center=[-3.7, -0.3, 0])
        ticks = VGroup(*[MathTex(s, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.38)
                         for v, s in [(np.pi, r'\pi'), (TAU_K, r'2\pi')]])
        pts = bz_point_labels(ax)
        Ylab = VGroup(Dot(ax.c2p(0, np.pi), radius=0.04, color=GREY_A),
                      MathTex('Y', font_size=26, color=GREY_A).next_to(ax.c2p(0, np.pi), RIGHT, buff=0.08))
        title = txt('the map: momentum $\\to$ state', 38, bold=True).to_edge(UP, buff=0.35)

        # ---------------- map1: the Brillouin zone is a torus
        glue = edge_arrows(ax)
        cam_t = Cam(0.6, -0.6, 0.62, center=[-3.7, 2.55, 0])
        tor = torus_wire(cam_t)
        eq_t = txt('$=$', 34).next_to(tor, LEFT, buff=0.2)
        with self.narrate('map1') as b:
            self.play(Write(title), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(bz), FadeIn(ticks), FadeIn(pts), FadeIn(Ylab), run_time=1.5)
            b.wait_sentence(2)
            self.play(LaggedStart(*[GrowArrow(a) for a in glue], lag_ratio=0.15), run_time=1.5)
            self.play(title.animate.set_opacity(0), FadeIn(tor), FadeIn(eq_t), run_time=1.2)

        # ---------------- map2: a state up to its phase is a point on the sphere
        sph = Sphere2D(radius=SPH_R, el=EL, az=AZ, n_merid=3).move_to(SPH_C)
        poles = sph.pole_labels(34)
        nb = MathTex(r'\mathbf n = \langle u|\boldsymbol\sigma|u\rangle', font_size=36).move_to([0.6, 3.2, 0])
        Pn = MathTex(r'P = |u\rangle\langle u| = \tfrac12(1 + \mathbf n\cdot\boldsymbol\sigma)', font_size=32, color=GREY_A)
        Pn.next_to(nb, DOWN, buff=0.15)
        with self.narrate('map2') as b:
            self.play(FadeIn(sph), FadeIn(poles), run_time=1.2)
            b.wait_sentence(1)
            self.play(Write(nb), run_time=1.4)
            self.play(FadeIn(Pn), run_time=0.8)

        # ---------------- map3: the map is k -> n(k) = d(k)/|d(k)|
        f1 = MathTex(r'H(\mathbf k) = \mathbf d(\mathbf k)\cdot\boldsymbol\sigma', font_size=36)
        f2 = MathTex(r'\text{upper band: } \langle u_+|\boldsymbol\sigma|u_+\rangle = \hat{\mathbf d}', font_size=32, color=GREY_A)
        f3 = MathTex(r'\mathbf k \;\longmapsto\; \mathbf n(\mathbf k) = \frac{\mathbf d(\mathbf k)}{|\mathbf d(\mathbf k)|}', font_size=36, color=C_FOLD)
        VGroup(f1, f2).arrange(RIGHT, buff=0.6).move_to([0, 3.55, 0])
        f3.move_to([0, 2.6, 0])
        path_k = np.concatenate([np.stack([np.linspace(0.05, np.pi, 60), np.full(60, 0.05)], 1),
                                 np.stack([np.full(60, np.pi), np.linspace(0.05, np.pi, 60)], 1),
                                 np.stack([np.linspace(np.pi, 0.05, 60), np.linspace(np.pi, 0.05, 60)], 1)])
        s = ValueTracker(0.0)

        def kpt():
            i = s.get_value() * (len(path_k) - 1)
            i0 = int(np.floor(i)); i1 = min(i0 + 1, len(path_k) - 1); f = i - i0
            return path_k[i0] * (1 - f) + path_k[i1] * f
        kdot = always_redraw(lambda: Dot(ax.c2p(*kpt()), radius=0.08, color=WHITE).set_stroke(BLACK, 2))
        ktr = always_redraw(lambda: VMobject(stroke_color=WHITE, stroke_width=2, stroke_opacity=0.6).set_points_as_corners(
            [ax.c2p(*p) for p in path_k[:max(2, int(s.get_value() * (len(path_k) - 1)) + 1)]] + [ax.c2p(*kpt())]))
        sdot = always_redraw(lambda: sph.dot(qwz_n(*kpt()), WHITE, 0.08))
        strace = always_redraw(lambda: sph.curve([qwz_n(*p) for p in path_k[:max(2, int(s.get_value() * (len(path_k) - 1)) + 1)]]
                                                 + [qwz_n(*kpt())], color=WHITE, width=2.5, back_opacity=0.3))
        with self.narrate('map3') as b:
            self.play(FadeOut(tor), FadeOut(eq_t), FadeOut(nb), FadeOut(Pn), run_time=0.6)
            self.play(Write(f1), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(f2), run_time=1.0)
            b.wait_sentence(2)
            self.play(Write(f3), run_time=1.4)
            self.add(ktr, strace, kdot, sdot)
            self.play(s.animate.set_value(1.0), run_time=b.remaining(-0.3), rate_func=linear)

        # ---------------- map3b: the QWZ model and three anchor points
        model = MathTex(r'\mathbf d(\mathbf k) = (\sin k_x,\ \sin k_y,\ m - \cos k_x - \cos k_y)', font_size=34).move_to([0.6, 3.3, 0])
        amarks = VGroup(*[Circle(radius=0.13, color=YELLOW, stroke_width=4).move_to(ax.c2p(*k))
                          for k in [(0.0, 0.0), (np.pi, 0.0), (np.pi, np.pi)]])
        south = VGroup(Dot(sph.p([0, 0, -1]), radius=0.09, color=YELLOW),
                       MathTex(r'\Gamma', font_size=30, color=YELLOW).next_to(sph.p([0, 0, -1]), LEFT, buff=0.15))
        north = VGroup(Dot(sph.p([0, 0, 1]), radius=0.09, color=YELLOW),
                       MathTex(r'X,\ M', font_size=30, color=YELLOW).next_to(sph.p([0, 0, 1]), RIGHT, buff=0.18))
        dvals = VGroup(MathTex(r'\Gamma:\ \mathbf d = (0,0,-1)', font_size=28), MathTex(r'X:\ \mathbf d = (0,0,1)', font_size=28),
                       MathTex(r'M:\ \mathbf d = (0,0,3)', font_size=26)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for d_ in dvals[:2]:
            d_.scale(26 / 28)
        dvals.move_to([-0.2, -0.3, 0])
        with self.narrate('map3b') as b:
            self.play(FadeOut(VGroup(f1, f2)), f3.animate.scale(0.9).move_to([0.6, 2.5, 0]), FadeOut(kdot), FadeOut(ktr),
                      FadeOut(sdot), FadeOut(strace), run_time=0.8)
            self.play(Write(model), run_time=1.6)
            b.wait_sentence(1)
            self.play(Create(amarks[0]), FadeIn(dvals[0]), FadeIn(south), run_time=1.2)
            b.wait_sentence(2)
            self.play(Create(amarks[1]), Create(amarks[2]), FadeIn(dvals[1:]), FadeIn(north), run_time=1.4)

        # ---------------- map3c: the mass m and the topology; m = 3.2 stays in a cap
        line = NumberLine(x_range=[0, 4, 1], length=4.0, include_numbers=False, color=GREY_B).move_to([1.0, -3.45, 0])
        mlab = MathTex('m', font_size=30, color=GREY_B).next_to(line, RIGHT, buff=0.15)
        nums = VGroup(*[MathTex(str(v), font_size=24, color=GREY_B).next_to(line.n2p(v), DOWN, buff=0.12) for v in (0, 2, 4)])
        seg_c = Line(line.n2p(0), line.n2p(2), color=C_UP, stroke_width=8)
        seg_t = Line(line.n2p(2), line.n2p(4), color=GREY_C, stroke_width=8)
        lab_c = MathTex('C = 1', font_size=28, color=C_UP).next_to(seg_c, UP, buff=0.12)
        lab_t = MathTex('C = 0', font_size=28, color=GREY_B).next_to(seg_t, UP, buff=0.12)
        m1 = VGroup(Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI).next_to(line.n2p(1), UP, buff=0.0),
                    MathTex('1', font_size=24).next_to(line.n2p(1), DOWN, buff=0.12))
        m32 = VGroup(Triangle(fill_color=WHITE, fill_opacity=1, stroke_width=0).scale(0.09).rotate(PI).next_to(line.n2p(3.2), UP, buff=0.0),
                     MathTex('3.2', font_size=24).next_to(line.n2p(3.2), DOWN, buff=0.12))
        mini_c = np.array([-0.2, 0.35, 0])
        mini = Sphere2D(radius=0.85, el=EL, az=AZ, n_merid=0).move_to(mini_c)
        mini_mesh, _, _, _ = painted_mesh(Cam(EL, AZ, 0.85, mini_c), M_TRIV, opacity=0.85)
        mini_l = VGroup(txt('$m=3.2$:', 22, GREY_A), txt('all $n_z \\ge 0.87$', 22, GREY_A)).arrange(DOWN, buff=0.06).next_to(mini, DOWN, buff=0.12)
        with self.narrate('map3c') as b:
            self.play(FadeOut(dvals), Create(line), FadeIn(mlab), FadeIn(nums), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(seg_c), FadeIn(lab_c), run_time=1.0)
            b.wait_sentence(2)
            self.play(FadeIn(m1), run_time=0.8)
            b.wait_sentence(3)
            self.play(Create(seg_t), FadeIn(lab_t), run_time=1.0)
            b.wait_sentence(4)
            self.play(FadeIn(m32), FadeIn(mini), FadeIn(mini_mesh), FadeIn(mini_l), run_time=1.4)

        # ---------------- map4: paint the grid cell by cell
        cols, om_c = cell_orient(NK)
        cells = bz_cells(ax, NK, opacity=0.0, stroke=GREY_E, width=0.5)
        cam = Cam(EL, AZ, SPH_R, SPH_C)
        X, _, _ = sphere_cells(NK)
        flipped = om_c < 0
        quads = mesh(cam, X, cols, opacity=0.78, back_opacity=0.12, stroke_width=0.4, cull_center=np.zeros(3), on_top=flipped)
        A, B, Cc, D = X[:-1, :-1], X[1:, :-1], X[1:, 1:], X[:-1, 1:]
        cen = (A + B + Cc + D) / 4
        dep = cen @ cam.basis()[0] + 100.0 * (flipped & ((cen @ cam.basis()[0]) > 0))
        order = np.argsort(dep, axis=None)
        rank_q = np.array([int(idx) for idx in order], float)          # cell index i*NK + j of each polygon
        op_q = np.array([q.get_fill_opacity() for q in quads])
        prog = ValueTracker(-1.0)
        FADE = 6.0

        def upd_quads(grp):
            a = np.clip((prog.get_value() - rank_q) / FADE, 0, 1)
            for q, ai, oi in zip(grp, a, op_q):
                q.set_fill(opacity=ai * oi)
                q.set_stroke(opacity=min(1.0, ai * oi * 1.1))

        def upd_cells(grp):
            for r, cell in enumerate(grp):
                i, j = divmod(r, NK)
                ai = float(np.clip((prog.get_value() - r) / FADE, 0, 1))
                cell.set_fill(cols[i][j], opacity=0.85 * ai)
        upd_quads(quads)
        quads.add_updater(upd_quads)
        cells.add_updater(upd_cells)
        legend = VGroup(VGroup(Square(0.25, fill_color=C_UP, fill_opacity=1, stroke_width=0), txt('face up', 26)).arrange(RIGHT, buff=0.15),
                        VGroup(Square(0.25, fill_color=C_FLIP, fill_opacity=1, stroke_width=0), txt('flipped (mirror image)', 26)).arrange(RIGHT, buff=0.15)
                        ).arrange(RIGHT, buff=0.5).next_to(bz, DOWN, buff=0.55)
        ccw = VGroup(Arc(radius=0.32, start_angle=0.2, angle=1.7 * PI, color=WHITE, stroke_width=3).add_tip(tip_length=0.14),
                     txt('counterclockwise in $k$', 20, GREY_A)).arrange(DOWN, buff=0.1).move_to([-0.2, 1.0, 0])
        with self.narrate('map4') as b:
            self.play(FadeOut(VGroup(line, mlab, nums, seg_c, seg_t, lab_c, lab_t, m1, m32, mini, mini_mesh, mini_l, amarks,
                                     model, south, north)), f3.animate.move_to([0.0, 3.1, 0]), run_time=0.8)
            self.add(cells, quads)
            self.bring_to_front(pts, glue, Ylab)
            self.play(prog.animate.set_value(NK * NK * 0.35), run_time=2.0, rate_func=linear)
            b.wait_sentence(1)
            self.play(FadeIn(ccw), prog.animate.set_value(NK * NK * 0.6), run_time=1.5, rate_func=linear)
            b.wait_sentence(2)
            self.play(FadeIn(legend), prog.animate.set_value(NK * NK + FADE), run_time=max(1.0, b.until_sentence(3, 2.0)), rate_func=linear)
            quads.clear_updaters()
            cells.clear_updaters()
            self.play(Indicate(pts[5], color=C_FLIP, scale_factor=1.6), run_time=1.0)

        # ---------------- map5: the fold
        fcurve = fold_curve(ax)
        fimg = VGroup(*[polyline3d(cam, np.moveaxis(qwz_n(seg[:, 0], seg[:, 1]), 0, -1) * 1.035, color=C_FOLD, width=4,
                                   back_opacity=0.25, cull_center=np.zeros(3)) for seg in fold_points()])
        fl = txt('fold', 30, C_FOLD).next_to(ax.c2p(np.pi + 1.25, np.pi + 1.25), UR, buff=0.05)
        with self.narrate('map5') as b:
            self.play(FadeOut(ccw), Create(fcurve), Create(fimg), run_time=1.6)
            self.play(FadeIn(fl), run_time=0.6)
            b.wait_sentence(2)
            self.play(Circumscribe(VGroup(bz, sph), color=GREY_B, buff=0.15), run_time=1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
