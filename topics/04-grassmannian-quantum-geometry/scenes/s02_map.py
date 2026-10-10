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
        a = Arrow(ax.c2p(x, 1.6), ax.c2p(x, 2.9), buff=0, color=color, stroke_width=4, max_tip_length_to_length_ratio=0.35)
        g.add(a)
    for y in (0, TAU_K):
        for dx in (0.0, 0.32):
            a = Arrow(ax.c2p(1.6 + dx, y), ax.c2p(2.7 + dx, y), buff=0, color=C_FOLD, stroke_width=4,
                      max_tip_length_to_length_ratio=0.35)
            g.add(a)
    return g


class S02_Map(NScene):
    def construct(self):
        ax, bz = bz_axes(4.4, center=[-3.7, -0.3, 0])
        ticks = VGroup(*[MathTex(s, font_size=24, color=GREY_B).next_to(ax.c2p(v, 0), DOWN, buff=0.38)
                         for v, s in [(np.pi, r'\pi'), (TAU_K, r'2\pi')]])
        pts = bz_point_labels(ax)
        title = txt('the map: momentum $\\to$ state', 38, bold=True).to_edge(UP, buff=0.35)

        # ---------------- map1: the Brillouin zone is a torus
        glue = edge_arrows(ax)
        cam_t = Cam(0.6, -0.6, 0.62, center=[-3.7, 2.55, 0])
        tor = torus_wire(cam_t)
        eq_t = txt('$=$', 34).next_to(tor, LEFT, buff=0.2)
        with self.narrate('map1') as b:
            self.play(Write(title), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(bz), FadeIn(ticks), FadeIn(pts), run_time=1.5)
            b.wait_sentence(2)
            self.play(LaggedStart(*[GrowArrow(a) for a in glue], lag_ratio=0.15), run_time=1.5)
            self.play(title.animate.set_opacity(0), FadeIn(tor), FadeIn(eq_t), run_time=1.2)

        # ---------------- map2: the Bloch sphere
        sph = Sphere2D(radius=SPH_R, el=EL, az=AZ, n_merid=3).move_to(SPH_C)
        poles = sph.pole_labels(34)
        Pn = MathTex(r'P = \tfrac12(1 + \mathbf n\cdot\boldsymbol\sigma)', font_size=36).next_to(sph, UP, buff=0.55)
        with self.narrate('map2') as b:
            self.play(FadeIn(sph), FadeIn(poles), run_time=1.2)
            b.wait_sentence(1)
            self.play(Write(Pn), run_time=1.5)
            st = txt('state up to its phase $=$ a point on the sphere', 26, GREY_A).next_to(sph, DOWN, buff=0.55)
            self.play(FadeIn(st), run_time=0.8)

        # ---------------- map3: a moving momentum and its state; the model
        path_k = np.concatenate([np.stack([np.linspace(0.05, np.pi, 60), np.full(60, 0.05)], 1),
                                 np.stack([np.full(60, np.pi), np.linspace(0.05, np.pi, 60)], 1),
                                 np.stack([np.linspace(np.pi, 2 * np.pi - 0.05, 60), np.linspace(np.pi, 2 * np.pi - 0.05, 60)], 1)])
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
        model = MathTex(r'\mathbf d(\mathbf k) = (\sin k_x,\ \sin k_y,\ m - \cos k_x - \cos k_y)', font_size=32)
        model2 = MathTex(r'\mathbf n = \mathbf d/|\mathbf d|,\qquad m = 1,\qquad C = 1', font_size=32)
        mgrp = VGroup(model, model2).arrange(DOWN, buff=0.15).to_edge(UP, buff=0.3)
        with self.narrate('map3') as b:
            self.play(FadeOut(Pn), FadeOut(st), FadeOut(tor), FadeOut(eq_t), run_time=0.6)
            self.add(ktr, strace, kdot, sdot)
            self.play(s.animate.set_value(0.55), run_time=b.until_sentence(1, 1.5), rate_func=linear)
            self.play(FadeIn(mgrp), s.animate.set_value(1.0), run_time=b.until_sentence(2, 2.0), rate_func=linear)
            self.play(Indicate(model2, color=C_FOLD), run_time=1.0)

        # ---------------- map4: paint the grid cell by cell
        cols, om_c = cell_orient(NK)
        cells = bz_cells(ax, NK, opacity=0.0, stroke=GREY_E, width=0.5)
        X, _, _ = sphere_cells(NK)
        cam = Cam(EL, AZ, SPH_R, SPH_C)
        # one polygon per cell on the sphere, ordered back-to-front once (the camera stays still while painting)
        flipped = om_c < 0
        quads = mesh(cam, X, cols, opacity=0.78, back_opacity=0.12, stroke_width=0.4, cull_center=np.zeros(3),
                     on_top=flipped)
        # map each sphere polygon back to its cell, then reveal by an updater (keeps the painter's order intact)
        A, B, Cc, D = X[:-1, :-1], X[1:, :-1], X[1:, 1:], X[:-1, 1:]
        cen = (A + B + Cc + D) / 4
        dep = cen @ cam.basis()[0] + 100.0 * (flipped & ((cen @ cam.basis()[0]) > 0))
        order = np.argsort(dep, axis=None)
        rank_q = np.array([divmod(int(idx), NK)[0] * NK + divmod(int(idx), NK)[1] for idx in order], float)
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
                        VGroup(Square(0.25, fill_color=C_FLIP, fill_opacity=1, stroke_width=0), txt('flipped', 26)).arrange(RIGHT, buff=0.15)
                        ).arrange(RIGHT, buff=0.5).next_to(bz, DOWN, buff=0.55)
        with self.narrate('map4') as b:
            self.play(FadeOut(kdot), FadeOut(ktr), FadeOut(sdot), FadeOut(strace), FadeOut(mgrp), run_time=0.6)
            self.add(cells, quads)
            self.bring_to_front(pts, glue)
            self.play(prog.animate.set_value(NK * NK + FADE), run_time=b.until_sentence(1, 3.0) + 3.5, rate_func=linear)
            quads.clear_updaters()
            cells.clear_updaters()
            self.play(FadeIn(legend[0]), run_time=0.6)
            b.wait_sentence(2)
            self.play(FadeIn(legend[1]), Indicate(pts[5], color=C_FLIP, scale_factor=1.6), run_time=1.0)

        # ---------------- map5: the fold
        fcurve = fold_curve(ax)
        fimg = VGroup(*[polyline3d(cam, np.moveaxis(qwz_n(seg[:, 0], seg[:, 1]), 0, -1) * 1.035, color=C_FOLD, width=4,
                                   back_opacity=0.25, cull_center=np.zeros(3)) for seg in fold_points()])
        fl = txt('fold', 30, C_FOLD).next_to(ax.c2p(np.pi + 1.25, np.pi + 1.25), UR, buff=0.05)
        with self.narrate('map5') as b:
            self.play(Create(fcurve), Create(fimg), run_time=1.6)
            self.play(FadeIn(fl), run_time=0.6)
            b.wait_sentence(2)
            self.play(Circumscribe(VGroup(bz, sph), color=GREY_B, buff=0.15), run_time=1.6)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
