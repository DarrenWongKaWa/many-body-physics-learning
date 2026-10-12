import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

DATA = np.load(ROOT / 'data' / 'mds.npz')
KEEP = DATA['keep']
CLOUD_C = np.array([2.7, -0.55, 0])
SCALE = 4.4                      # scene units per unit length (sphere of radius 1/2 -> 2.2)


def snapshot(tag, s):
    """Configuration after iteration ~ 1500 s^3 (early steps are where the shape forms)."""
    it = 1500 * s ** 3
    i = int(np.searchsorted(KEEP, it, side='right') - 1)
    i = max(0, min(i, len(KEEP) - 1))
    return DATA[f'{tag}_iters'][i], int(KEEP[i])


class S04_MDS(NScene):
    def construct(self):
        tag = txt('[H1]', 26, GREY_T).to_corner(UL, buff=0.4)
        self.add(tag)

        # ---------------- mds1: a pair of momenta and the distance between their states
        ax, bz = bz_axes(3.4, center=[-4.6, 0.6, 0])
        kx, ky = DATA['chern_kx'], DATA['chern_ky']
        _, _, omk, _ = qwz_geom(kx, ky)
        dots_k = VGroup(*[Dot(ax.c2p(a, b), radius=0.025, color=C_UP if o >= 0 else C_FLIP) for a, b, o in zip(kx, ky, omk)])
        nl = txt('484 sampled momenta', 24, GREY_T).next_to(bz, DOWN, buff=0.35)
        i0, j0 = 37, 300
        pair = Line(ax.c2p(kx[i0], ky[i0]), ax.c2p(kx[j0], ky[j0]), color=YELLOW, stroke_width=3)
        pi_ = Dot(ax.c2p(kx[i0], ky[i0]), radius=0.07, color=YELLOW)
        pj_ = Dot(ax.c2p(kx[j0], ky[j0]), radius=0.07, color=YELLOW)
        li = MathTex(r'\mathbf k_i', font_size=28, color=YELLOW).next_to(pi_, UP, buff=0.08)
        lj = MathTex(r'\mathbf k_j', font_size=28, color=YELLOW).next_to(pj_, DOWN, buff=0.08)
        not_l = txt('not this length', 22, GREY_A).next_to(pair, UP, buff=0.05).shift(0.3 * RIGHT)
        msph = Sphere2D(radius=1.5, el=0.35, az=0.5, n_merid=2).move_to([0.6, 0.6, 0])
        ni, nj = qwz_n(kx[i0], ky[i0]), qwz_n(kx[j0], ky[j0])
        mi, mj = msph.dot(ni, YELLOW, 0.08), msph.dot(nj, YELLOW, 0.08)
        chord = Line(msph.p(ni), msph.p(nj), color=C_UP, stroke_width=5)
        chord_l = MathTex(r'D_{ij}', font_size=32, color=C_UP).next_to(chord.get_center(), RIGHT, buff=0.12)
        with self.narrate('mds1') as b:
            self.play(FadeIn(bz), LaggedStartMap(FadeIn, dots_k, lag_ratio=0.002), FadeIn(nl), run_time=1.6)
            self.play(FadeIn(pi_), FadeIn(pj_), FadeIn(li), FadeIn(lj), Create(pair), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(not_l), run_time=0.6)
            b.wait_sentence(2)
            self.play(FadeIn(msph), FadeIn(mi), FadeIn(mj), run_time=1.0)
            self.play(Create(chord), FadeIn(chord_l), run_time=1.0)

        # ---------------- mds1b: the whole table as an image
        D = DATA['chern_D'].astype(float)
        img = ImageMobject(mono_rgba(D, D.max(), color='#E8E8E8', gamma=0.8))
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS['nearest'])
        img.height = 3.3
        img.move_to([4.6, 0.4, 0])
        img_box = SurroundingRectangle(img, buff=0, stroke_color=GREY_C, stroke_width=1.5)
        xi = MathTex('j', font_size=30, color=GREY_B).next_to(img, UP, buff=0.12)
        yi = MathTex('i', font_size=30, color=GREY_B).next_to(img, LEFT, buff=0.12)
        n = D.shape[0]
        px = img.get_left()[0] + (j0 + 0.5) / n * img.width
        py = img.get_top()[1] - (i0 + 0.5) / n * img.height
        pix = Square(0.16, color=YELLOW, stroke_width=3).move_to([px, py, 0])
        cb = VGroup(Rectangle(width=1.6, height=0.18, stroke_width=0).set_fill(color=[BLACK, WHITE], opacity=1),
                    ).next_to(img, DOWN, buff=0.35)
        cb[0].set_sheen_direction(RIGHT)
        cbl = VGroup(MathTex('0', font_size=24).next_to(cb, LEFT, buff=0.1), MathTex('1', font_size=24).next_to(cb, RIGHT, buff=0.1))
        cbt = txt('same state \\quad\\quad orthogonal', 20, GREY_A).next_to(cb, DOWN, buff=0.08)
        tab_l = MathTex(r'D_{ij} = D_{\rm HS}\big(P(\mathbf k_i), P(\mathbf k_j)\big)', font_size=30).next_to(xi, UP, buff=0.12)
        with self.narrate('mds1b') as b:
            self.play(FadeIn(img), Create(img_box), FadeIn(xi), FadeIn(yi), FadeIn(tab_l), run_time=1.4)
            self.play(Create(pix), Indicate(chord_l, color=C_UP), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(cb), FadeIn(cbl), FadeIn(cbt), run_time=1.0)
            b.wait_sentence(2)
            diag = Line(img.get_corner(UL), img.get_corner(DR), color=C_FOLD, stroke_width=2).set_opacity(0.8)
            self.play(Create(diag), run_time=1.0)
            self.play(FadeOut(diag), run_time=0.6)

        # ---------------- mds2: multidimensional scaling
        goal = MathTex(r'\text{find } \mathbf x_i\in\mathbb R^3:\quad |\mathbf x_i - \mathbf x_j| \approx D_{ij}', font_size=36, color=C_FOLD)
        goal.move_to([2.7, 3.25, 0])
        why = txt('$D_{\\rm HS}$ is a straight-line distance between matrices', 28, GREY_A).move_to([1.6, -3.3, 0])
        blind_in = txt('input: only the table (no momenta, no states)', 24, GREY_A).move_to([2.7, 2.6, 0])
        with self.narrate('mds2') as b:
            self.play(FadeOut(VGroup(msph, mi, mj, chord, chord_l, not_l, cb, cbl, cbt, pix, xi, yi)),
                      Group(bz, dots_k, nl, pair, pi_, pj_, li, lj).animate.scale(0.7).move_to([-5.2, 1.3, 0]),
                      Group(img, img_box, tab_l).animate.scale(0.62).move_to([-5.2, -1.85, 0]), run_time=1.2)
            self.play(FadeIn(blind_in), run_time=0.8)
            b.wait_sentence(1)
            self.play(FadeIn(why), run_time=0.8)
            b.wait_sentence(2)
            self.play(Write(goal), run_time=1.8)

        # ---------------- mds3/4: SMACOF for the Chern band
        s = ValueTracker(0.0)
        az = ValueTracker(0.4)
        which = {'tag': 'chern'}
        cols_of = {'chern': [C_UP if o >= 0 else C_FLIP for o in omk]}
        _, _, omt, _ = qwz_geom(DATA['trivial_kx'], DATA['trivial_ky'], M_TRIV)
        cols_of['trivial'] = [C_UP if o >= 0 else C_FLIP for o in omt]
        cloud = VGroup(*[Dot(radius=0.035) for _ in range(len(kx))])

        def upd(grp):
            X, _ = snapshot(which['tag'], s.get_value())
            cam = Cam(0.35, az.get_value(), SCALE, CLOUD_C)
            P = cam.p(X)
            dep = cam.depth(X)
            dn = (dep - dep.min()) / max(1e-9, dep.max() - dep.min())
            for d, p, a, col in zip(grp, P, dn, cols_of[which['tag']]):
                d.move_to(p)
                d.set_fill(col, opacity=0.25 + 0.75 * a)
        cloud.add_updater(upd)
        upd(cloud)
        ghost = DashedVMobject(Circle(radius=0.5 * SCALE, stroke_color=GREY_D, stroke_width=1.5).move_to(CLOUD_C), num_dashes=60)
        step = always_redraw(lambda: txt(f'step {snapshot(which["tag"], s.get_value())[1]}', 26, GREY_T).move_to([6.2, -2.75, 0]))
        spring = txt('every pair: a spring of rest length $D_{ij}$', 26, GREY_A).move_to([2.7, -3.5, 0])
        with self.narrate('mds3') as b:
            self.play(FadeOut(why), FadeOut(blind_in), FadeIn(cloud), run_time=0.8)
            self.add(step)
            b.wait_sentence(1)
            self.play(FadeIn(spring), run_time=0.6)
            self.play(s.animate.set_value(0.45), az.animate.set_value(1.0), run_time=b.remaining(-0.1), rate_func=linear)
        sphere_l = txt('Chern band: the Bloch sphere, radius $\\tfrac12$', 30, C_UP).move_to([2.7, 2.5, 0])
        with self.narrate('mds4') as b:
            self.play(s.animate.set_value(1.0), az.animate.set_value(1.9), FadeIn(ghost), run_time=2.5, rate_func=linear)
            self.play(FadeIn(sphere_l), az.animate.set_value(2.6), run_time=b.remaining(-0.1), rate_func=linear)
        chk = txt('same shape as classical MDS (difference $<10^{-14}$)', 22, GREY_T).next_to(sphere_l, DOWN, buff=0.15)

        # ---------------- mds5: the trivial band
        with self.narrate('mds5') as b:
            self.play(FadeIn(chk), az.animate.set_value(3.1), run_time=1.2, rate_func=linear)
            which['tag'] = 'trivial'
            s.set_value(0.0)
            triv_l = txt('trivial band ($m=3.2$, all $n_z\\ge0.87$): an open cap', 30, C_FLIP).move_to(sphere_l)
            self.play(FadeOut(sphere_l), FadeOut(chk), FadeIn(triv_l), run_time=0.8)
            self.play(s.animate.set_value(1.0), az.animate.set_value(3.8), run_time=b.until_sentence(1, 2.5) + 1.2, rate_func=linear)
            no_hole = txt('fully covered, but never closes', 26, GREY_A).next_to(triv_l, DOWN, buff=0.2)
            self.play(FadeIn(no_hole), az.animate.set_value(4.3), run_time=1.5, rate_func=linear)
            b.wait_sentence(2)
            topo = txt('closed or open: a first glimpse of topology', 30, C_FOLD).move_to([2.7, -3.5, 0])
            self.play(FadeOut(spring), FadeIn(topo), az.animate.set_value(4.8), run_time=b.remaining(-0.1), rate_func=linear)

        # ---------------- mds6: the two blind spots of a distance table
        cloud.clear_updaters()
        tri = [np.array([-0.6, -0.35, 0]), np.array([0.65, -0.35, 0]), np.array([-0.25, 0.65, 0])]
        c_a, c_b = np.array([0.6, 0.3, 0]), np.array([2.6, 0.3, 0])
        t_a = Polygon(*[c_a + p for p in tri], stroke_color=C_UP, stroke_width=3, fill_color=C_UP, fill_opacity=0.3)
        t_b = Polygon(*[c_b + np.array([-p[0], p[1], 0]) for p in tri], stroke_color=C_FLIP, stroke_width=3, fill_color=C_FLIP, fill_opacity=0.3)
        mir = txt('mirror images: the same distances', 26, GREY_A).move_to([1.6, -0.8, 0])
        lay = VGroup(*[Polygon([4.4, y, 0], [6.2, y, 0], [6.6, y + 0.45, 0], [4.8, y + 0.45, 0], stroke_color=c, stroke_width=2,
                               fill_color=c, fill_opacity=0.35) for y, c in ((0.0, C_UP), (0.45, C_FLIP), (0.9, C_UP))])
        lay_l = txt('three layers look like one', 26, GREY_A).move_to([5.5, -0.8, 0])
        with self.narrate('mds6') as b:
            self.play(FadeOut(VGroup(cloud, ghost, triv_l, no_hole, topo, goal)), FadeOut(step), run_time=0.9)
            self.play(FadeIn(t_a), run_time=0.6)
            self.play(TransformFromCopy(t_a, t_b), FadeIn(mir), run_time=1.4)
            b.wait_sentence(1)
            self.play(LaggedStart(*[FadeIn(l, shift=0.2 * DOWN) for l in lay], lag_ratio=0.3), run_time=1.2)
            self.play(lay[1].animate.move_to(lay[0]), lay[2].animate.move_to(lay[0]), FadeIn(lay_l), run_time=1.4)
        chern_need = VGroup(txt('Chern number $=$ signed count of coverings', 30, C_UP),
                            txt('$\\Rightarrow$ need orientation $\\Rightarrow$ zoom in on the derivative of the map', 28, C_FOLD)
                            ).arrange(DOWN, buff=0.2).move_to([2.6, -2.6, 0])
        with self.narrate('mds6b') as b:
            self.play(FadeIn(chern_need[0]), run_time=1.0)
            b.wait_sentence(1)
            self.play(FadeIn(chern_need[1]), run_time=1.0)
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
