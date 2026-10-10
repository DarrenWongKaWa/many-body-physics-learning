import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

NK = 24
CAP_NZ = 0.58


def ellipse_at(ax, k, scale, color, width=2):
    """Tissot-style ellipse in the zone: axes along the eigenvectors of g(k), lengths ~ sqrt(eigenvalues)."""
    _, g, om, _ = qwz_geom(*k)
    lam, V = np.linalg.eigh(g)
    lam = np.clip(lam, 0, None)
    t = np.linspace(0, TAU, 48)
    pts = [np.array(k) + scale * (np.sqrt(lam[1]) * np.cos(s) * V[:, 1] + np.sqrt(lam[0]) * np.sin(s) * V[:, 0]) for s in t]
    col = C_UP if om >= 0 else C_FLIP
    e = VMobject(stroke_color=col, stroke_width=width, fill_color=col, fill_opacity=0.35)
    e.set_points_as_corners([ax.c2p(*p) for p in pts])
    return e


def cell_areas(nk, sub=12):
    """Integrated sqrt(det g) (unsigned) and sign(Omega) sqrt(det g) (signed) on each cell, in units of pi."""
    n = nk * sub
    ks = (np.arange(n) + 0.5) * TAU_K / n
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    _, _, om, dg = qwz_geom(KX, KY)
    dA = np.sqrt(np.clip(dg, 0, None)) * (TAU_K / n) ** 2 / np.pi
    un = dA.reshape(nk, sub, nk, sub).sum((1, 3))
    sg = (np.sign(om) * dA).reshape(nk, sub, nk, sub).sum((1, 3))
    return un, sg


def paper_points(phi, pts2d, side):
    """Map printed 2D points (x, y) on the sheet to 3D; the right half (x > 0) is folded by angle phi about x = 0."""
    out = []
    for x, y in pts2d:
        if side > 0:
            out.append([x * np.cos(phi), y, x * np.sin(phi)])
        else:
            out.append([x, y, 0.0])
    return np.array(out)


class S07_Fold(NScene):
    def construct(self):
        tag = txt('[H3]', 26, GREY_T).to_corner(UL, buff=0.4)
        title = txt('Back to the fold', 40, bold=True).to_edge(UP, buff=0.35)
        ax, bz = bz_axes(5.4, center=[-3.4, -0.35, 0])
        fcurve = fold_curve(ax, width=3)

        # ---------------- fol1: Tissot ellipses over the zone
        npts = 13
        ks = (np.arange(npts) + 0.5) * TAU_K / npts
        ells = VGroup(*[ellipse_at(ax, (a, b2), 0.42, None) for a in ks for b2 in ks])
        with self.narrate('fol1') as b:
            self.play(FadeIn(tag), Write(title), Create(bz), run_time=1.2)
            b.wait_sentence(1)
            self.play(LaggedStart(*[GrowFromCenter(e) for e in ells], lag_ratio=0.01), run_time=2.5)
            self.play(Create(fcurve), run_time=1.2)

        # ---------------- fol2: crossing the fold, the ellipses collapse
        # a path from X towards M crosses the fold; find the crossing exactly
        def om_on(t):
            return qwz_geom(np.pi, t)[2]
        tl, tr = 0.3, 3.0
        for _ in range(60):
            tm = 0.5 * (tl + tr)
            if om_on(tl) * om_on(tm) <= 0:
                tr = tm
            else:
                tl = tm
        tfold = 0.5 * (tl + tr)
        row_t = tfold + np.linspace(-0.9, 0.9, 7)
        row_ax = Axes(x_range=[-1.05, 1.05, 1], y_range=[-0.43, 0.43, 1], x_length=5.6, y_length=2.3, tips=False,
                      axis_config=dict(stroke_opacity=0, include_ticks=False)).move_to([3.7, 0.7, 0])
        lam_max = max(np.sqrt(np.clip(np.linalg.eigvalsh(qwz_geom(np.pi, t)[1]), 0, None)).max() for t in row_t)
        SC = 0.13 / lam_max

        def row_ellipse(t, width=3):
            _, g, om, _ = qwz_geom(np.pi, t)
            lam, V = np.linalg.eigh(g)
            lam = np.clip(lam, 0, None)
            rotv = lambda v: np.array([v[1], -v[0]])          # display: horizontal = k_y, vertical = -k_x
            th = np.linspace(0, TAU, 60)
            pts = [np.array([t - tfold, 0.0]) + SC * (np.sqrt(lam[1]) * np.cos(s_) * rotv(V[:, 1]) + np.sqrt(lam[0]) * np.sin(s_) * rotv(V[:, 0]))
                   for s_ in th]
            col = C_UP if om >= 0 else C_FLIP
            return VMobject(stroke_color=col, stroke_width=width, fill_color=col, fill_opacity=0.35).set_points_as_corners(
                [row_ax.c2p(*p) for p in pts])
        row = VGroup(*[row_ellipse(t) for t in row_t])
        _, gf, _, _ = qwz_geom(np.pi, tfold)
        lamf, Vf = np.linalg.eigh(gf)
        vf = np.array([Vf[1, 1], -Vf[0, 1]])
        segf = Line(row_ax.c2p(*(-SC * np.sqrt(lamf[1]) * vf)), row_ax.c2p(*(SC * np.sqrt(lamf[1]) * vf)),
                    color=C_FOLD, stroke_width=5)
        row_box = SurroundingRectangle(row_ax, buff=0.1, corner_radius=0.12, stroke_color=GREY_C, stroke_width=1.5)
        row_l = txt('along the line $k_x=\\pi$, crossing the fold', 24, GREY_A).next_to(row_box, UP, buff=0.12)
        path_l = Line(ax.c2p(np.pi, row_t[0]), ax.c2p(np.pi, row_t[-1]), color=WHITE, stroke_width=3)
        seg_l = txt('on the fold: a segment', 26, C_FOLD).next_to(row_box, DOWN, buff=0.2)
        null_l = MathTex(r'\det g = 0', font_size=34, color=C_FOLD).next_to(seg_l, DOWN, buff=0.15)
        with self.narrate('fol2') as b:
            self.play(Create(path_l), FadeIn(row_box), FadeIn(row_l), LaggedStartMap(FadeIn, row, lag_ratio=0.15), run_time=1.6)
            b.wait_sentence(1)
            self.play(Create(segf), run_time=1.0)
            self.play(FadeIn(seg_l), Write(null_l), run_time=1.4)

        # ---------------- fol3: a folded sheet of clear film
        cam = Cam(0.95, -1.5708, 1.25, center=[3.7, 0.0, 0])
        W2, H2 = 2.2, 2.4

        def circ_arrow(cx, cy, r=0.42):
            t = np.linspace(0.3, 0.3 + 1.6 * PI, 40)                 # counter-clockwise arc
            arc = [(cx + r * np.cos(a), cy + r * np.sin(a)) for a in t]
            tip = np.array(arc[-1])
            d = np.array(arc[-1]) - np.array(arc[-3])
            d = d / np.linalg.norm(d)
            nrm = np.array([-d[1], d[0]])
            head = [tuple(tip - 0.2 * d + 0.12 * nrm), tuple(tip), tuple(tip - 0.2 * d - 0.12 * nrm)]
            return arc, head
        glyphs = [(circ_arrow(-1.1, -0.6), -1), (circ_arrow(1.1, 0.6), 1)]
        phi = ValueTracker(0.0)

        def film():
            g = VGroup()
            P = phi.get_value()
            L = paper_points(P, [(-W2, -H2 / 2), (0, -H2 / 2), (0, H2 / 2), (-W2, H2 / 2)], -1)
            Rr = paper_points(P, [(0, -H2 / 2), (W2, -H2 / 2), (W2, H2 / 2), (0, H2 / 2)], +1)
            g.add(Polygon(*cam.p(L), fill_color=C_UP, fill_opacity=0.3, stroke_color=C_UP, stroke_width=2))
            g.add(Polygon(*cam.p(Rr), fill_color=interpolate_color(ManimColor(C_UP), ManimColor(C_FLIP), min(1, P / PI)),
                          fill_opacity=0.3, stroke_color=WHITE, stroke_width=2))
            for (arc, head), side in glyphs:
                col = WHITE if side < 0 else interpolate_color(ManimColor(WHITE), ManimColor(C_FLIP), min(1, P / PI))
                g.add(VMobject(stroke_color=col, stroke_width=5).set_points_as_corners(cam.p(paper_points(P, arc, side))))
                g.add(VMobject(stroke_color=col, stroke_width=5).set_points_as_corners(cam.p(paper_points(P, head, side))))
            g.add(DashedLine(cam.p([0, -H2 / 2 - 0.2, 0]), cam.p([0, H2 / 2 + 0.2, 0]), color=C_FOLD, stroke_width=3))
            return g
        filmm = always_redraw(film)
        loc = MathTex(r'f(s,t) = (s,\ t^2)', font_size=36).move_to([3.7, -2.75, 0])
        loc2 = txt('$(s,t)$ and $(s,-t)$: one image, opposite orientations', 24, GREY_A).next_to(loc, DOWN, buff=0.15)
        with self.narrate('fol3') as b:
            self.play(FadeOut(VGroup(row, row_box, row_l, segf, seg_l, null_l, path_l)), run_time=0.7)
            self.play(FadeIn(filmm), run_time=0.8)
            b.wait_sentence(1)
            self.play(phi.animate.set_value(PI * 0.999), run_time=3.0, rate_func=smooth)
            b.wait_sentence(2)
            self.play(Write(loc), FadeIn(loc2), run_time=1.5)

        # ---------------- fol4: the fold curve of the model
        cols, om_c = cell_orient(NK)
        cells = bz_cells(ax, NK, cols, opacity=0.55, stroke=GREY_E, width=0.4)
        fl = MathTex(r'\det g = 0', font_size=34, color=C_FOLD).move_to(ax.c2p(np.pi + 2.2, np.pi + 2.55))
        inside = txt('flipped', 28, C_FLIP).move_to(ax.c2p(np.pi, np.pi + 0.5))
        Ml = MathTex('M', font_size=30).move_to(ax.c2p(np.pi, np.pi - 0.2))
        with self.narrate('fol4') as b:
            filmm.clear_updaters()
            self.play(FadeOut(VGroup(filmm, loc, loc2)), FadeOut(ells), FadeIn(cells), run_time=1.2)
            self.bring_to_front(fcurve)
            self.play(Write(fl), FadeIn(Ml), run_time=1.2)
            b.wait_sentence(1)
            self.play(FadeIn(inside), run_time=0.8)

        # ---------------- fol5: the polar cap is covered three times
        SPH_C, SPH_R = np.array([1.35, -0.7, 0]), 1.85
        sph = Sphere2D(radius=SPH_R, el=0.42, az=0.55, n_merid=2).move_to(SPH_C)
        scam = Cam(0.42, 0.55, SPH_R, SPH_C)
        X, colsX, omX = sphere_cells(NK)
        smesh = mesh(scam, X, colsX, opacity=0.75, back_opacity=0.1, stroke_width=0.3, cull_center=np.zeros(3), on_top=omX < 0)
        # which sheet does each cell of the cap belong to?
        h = TAU_K / NK
        cc = (np.arange(NK) + 0.5) * h
        KX, KY = np.meshgrid(cc, cc, indexing='ij')
        ncent, _, omc, _ = qwz_geom(KX, KY)
        incap = ncent[2] >= CAP_NZ
        dX = np.minimum(np.abs(KX - np.pi), TAU_K - np.abs(KX - np.pi)) ** 2 + np.minimum(KY, TAU_K - KY) ** 2
        dY = np.minimum(KX, TAU_K - KX) ** 2 + np.minimum(np.abs(KY - np.pi), TAU_K - np.abs(KY - np.pi)) ** 2
        sheet = np.where(omc < 0, 2, np.where(dX < dY, 0, 1))
        lay_cam = [Cam(0.62, 0.55, 1.45, np.array([5.6, y, 0])) for y in (-2.35, -0.75, 0.85)]
        layers = VGroup()
        for s_id, lc in zip((0, 1, 2), lay_cam):
            Xs = X.copy()
            cols_s = [[(C_FLIP if s_id == 2 else C_UP) for j in range(NK)] for i in range(NK)]
            op_mask = (sheet == s_id) & incap
            # draw only this sheet's cap cells: give other cells zero opacity
            m = mesh(lc, Xs - np.array([0, 0, 0.75]), cols_s, opacity=0.8, stroke_width=0.3)
            A, B, Cc, D = Xs[:-1, :-1], Xs[1:, :-1], Xs[1:, 1:], Xs[:-1, 1:]
            dep = (((A + B + Cc + D) / 4) - np.array([0, 0, 0.75])) @ lc.basis()[0]
            order = np.argsort(dep, axis=None)
            for poly, idx in zip(m, order):
                i, j = divmod(int(idx), NK)
                if not op_mask[i, j]:
                    poly.set_fill(opacity=0).set_stroke(opacity=0)
            layers.add(m)
        signs = VGroup(*[MathTex(s_, font_size=40, color=c_).next_to(lc.center, LEFT, buff=1.55)
                         for s_, c_, lc in zip(['+1', '+1', '-1'], [C_UP, C_UP, C_FLIP], lay_cam)])
        cap_l = txt('the polar cap, pulled apart', 24, GREY_A).move_to([5.6, 2.25, 0])
        with self.narrate('fol5') as b:
            self.play(FadeOut(title), FadeIn(sph), FadeIn(smesh), run_time=1.0)
            b.wait_sentence(1)
            self.play(LaggedStart(*[FadeIn(l, shift=0.3 * UP) for l in layers], lag_ratio=0.3), FadeIn(cap_l), run_time=1.6)
            self.play(FadeIn(signs), run_time=0.8)

        # ---------------- fol6/7: unsigned and signed area counters
        un, sg = cell_areas(NK)
        prog = ValueTracker(0.0)

        def totals():
            p = prog.get_value()
            mask = (np.arange(NK * NK) < p).reshape(NK, NK)
            return un[mask].sum(), sg[mask].sum()
        cnt_u = always_redraw(lambda: DecimalNumber(totals()[0], num_decimal_places=3, font_size=40, color=WHITE))
        cnt_s = always_redraw(lambda: DecimalNumber(totals()[1], num_decimal_places=3, font_size=40, color=C_UP))
        lu = txt('count every sheet:', 30)
        ls = txt('count with signs:', 30, C_UP)
        units = txt('(in spheres; one sphere has area $\\pi$)', 22, GREY_T)
        panel_c = VGroup(lu, ls).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([-4.6, -3.45, 0])
        cnt_u.add_updater(lambda m: m.next_to(lu, RIGHT, buff=0.3))
        cnt_s.add_updater(lambda m: m.next_to(ls, RIGHT, buff=0.3))
        units.next_to(panel_c, UP, buff=0.25, aligned_edge=LEFT)

        def sweep_hl(grp):
            p = prog.get_value()
            for r, c in enumerate(grp):
                c.set_fill(WHITE, opacity=0.35 if r < p <= r + NK else 0.0)
        with self.narrate('fol6') as b:
            self.play(Group(bz, cells, fcurve, fl, inside, Ml).animate.scale(0.82).shift(0.55 * UP + 0.2 * LEFT), run_time=0.8)
            hl = VGroup(*[c.copy().set_fill(WHITE, opacity=0).set_stroke(width=0) for c in cells])
            hl.add_updater(sweep_hl)
            self.add(hl, cnt_u, cnt_s)
            self.play(FadeIn(lu), FadeIn(ls), FadeIn(units), run_time=0.8)
            b.wait_sentence(1)
            self.play(prog.animate.set_value(NK * NK), run_time=b.remaining(-0.8), rate_func=linear)
            hl.clear_updaters()
            self.play(Indicate(cnt_u, scale_factor=1.25), run_time=0.7)
        qv = txt('quantum volume', 26, GREY_A)
        with self.narrate('fol7') as b:
            qv.next_to(cnt_u, RIGHT, buff=0.3)
            self.play(FadeIn(qv), Indicate(cnt_s, scale_factor=1.25, color=C_UP), run_time=1.2)
            b.wait_sentence(1)
            ch = txt('$=$ Chern number $C$', 28, C_UP).next_to(cnt_s, RIGHT, buff=0.3)
            self.play(FadeIn(ch), layers[2].animate.move_to(layers[1]), signs[2].animate.move_to(signs[1]), run_time=1.2)
            self.play(FadeOut(layers[2]), FadeOut(layers[1]), FadeOut(signs[1]), FadeOut(signs[2]), run_time=0.8)
            b.wait_sentence(2)
            bound = MathTex(r'\int_{\rm BZ}\sqrt{\det g}\;d^2k\ \ \ge\ \ \pi\,|C|', font_size=38, color=C_FOLD).move_to([1.5, 2.95, 0])
            mo = txt('(Mera \\& Ozawa)', 22, GREY_T).next_to(bound, RIGHT, buff=0.2)
            self.play(Write(bound), FadeIn(mo), run_time=2.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
