import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *

DATA = np.load(ROOT / 'data' / 'mds.npz')
KEEP = DATA['keep']
CLOUD_C = np.array([2.7, -0.55, 0])
SCALE = 4.4                      # scene units per unit length (sphere of radius 1/2 -> 2.6)


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

        # ---------------- mds1: the distance table
        ax, bz = bz_axes(3.4, center=[-4.6, 0.2, 0])
        kx, ky = DATA['chern_kx'], DATA['chern_ky']
        _, _, omk, _ = qwz_geom(kx, ky)
        dots_k = VGroup(*[Dot(ax.c2p(a, b), radius=0.025, color=C_UP if o >= 0 else C_FLIP) for a, b, o in zip(kx, ky, omk)])
        D = DATA['chern_D'].astype(float)
        img = ImageMobject(mono_rgba(D, D.max(), color='#E8E8E8', gamma=0.8)[::-1])
        img.set_resampling_algorithm(RESAMPLING_ALGORITHMS['nearest'])
        img.height = 3.4
        img.move_to([0.2, 0.2, 0])
        img_box = SurroundingRectangle(img, buff=0, stroke_color=GREY_C, stroke_width=1.5)
        tab_l = MathTex(r'D_{ij} = D_{\rm HS}\big(P(\mathbf k_i), P(\mathbf k_j)\big)', font_size=32).next_to(img, DOWN, buff=0.3)
        nl = txt('484 sampled momenta', 24, GREY_T).next_to(bz, DOWN, buff=0.35)
        i0, j0 = 37, 300
        pair = Line(ax.c2p(kx[i0], ky[i0]), ax.c2p(kx[j0], ky[j0]), color=YELLOW, stroke_width=3)
        q = txt('rebuild the shape from the table alone?', 34).to_edge(UP, buff=0.45)
        with self.narrate('mds1') as b:
            self.play(FadeIn(bz), LaggedStartMap(FadeIn, dots_k, lag_ratio=0.002), FadeIn(nl), run_time=1.6)
            self.play(Create(pair), run_time=0.6)
            self.play(FadeIn(img), Create(img_box), FadeIn(tab_l), run_time=1.5)
            b.wait_sentence(1)
            self.play(FadeIn(q), run_time=1.0)

        # ---------------- mds2: multidimensional scaling
        goal = MathTex(r'\text{find } \mathbf x_i\in\mathbb R^3:\quad |\mathbf x_i - \mathbf x_j| \approx D_{ij}', font_size=36, color=C_FOLD)
        goal.move_to([2.7, 3.25, 0])
        why = txt('$D_{\\rm HS}$ is a straight-line distance between matrices', 28, GREY_A).move_to([0, -3.15, 0])
        with self.narrate('mds2') as b:
            self.play(FadeOut(q), FadeIn(why), run_time=1.0)
            b.wait_sentence(1)
            self.play(Group(bz, dots_k, nl, pair).animate.scale(0.7).move_to([-5.2, 1.3, 0]),
                      Group(img, img_box, tab_l).animate.scale(0.62).move_to([-5.2, -1.85, 0]), run_time=1.2)
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
            self.play(FadeOut(why), FadeIn(cloud), run_time=0.8)
            self.add(step)
            b.wait_sentence(1)
            self.play(FadeIn(spring), run_time=0.6)
            self.play(s.animate.set_value(0.45), az.animate.set_value(1.0), run_time=b.remaining(-0.1), rate_func=linear)
        sphere_l = txt('Chern band: a closed sphere', 30, C_UP).move_to([2.7, 2.5, 0])
        with self.narrate('mds4') as b:
            self.play(s.animate.set_value(1.0), az.animate.set_value(1.9), FadeIn(ghost), run_time=2.5, rate_func=linear)
            self.play(FadeIn(sphere_l), az.animate.set_value(2.6), run_time=b.remaining(-0.1), rate_func=linear)
        chk = txt('same shape as classical MDS (difference $<10^{-14}$)', 22, GREY_T).next_to(sphere_l, DOWN, buff=0.15)

        # ---------------- mds5: the trivial band
        with self.narrate('mds5') as b:
            self.play(FadeIn(chk), az.animate.set_value(3.1), run_time=1.2, rate_func=linear)
            which['tag'] = 'trivial'
            s.set_value(0.0)
            triv_l = txt('trivial band ($m=3.2$): an open cap', 30, C_FLIP).move_to(sphere_l)
            self.play(FadeOut(sphere_l), FadeOut(chk), FadeIn(triv_l), run_time=0.8)
            self.play(s.animate.set_value(1.0), az.animate.set_value(3.8), run_time=b.until_sentence(1, 2.5) + 1.2, rate_func=linear)
            no_hole = txt('fully covered, no hole, but never closes', 26, GREY_A).next_to(triv_l, DOWN, buff=0.2)
            self.play(FadeIn(no_hole), az.animate.set_value(4.3), run_time=1.5, rate_func=linear)
            b.wait_sentence(2)
            topo = txt('closes or not: a sign of topology', 30, C_FOLD).move_to([2.7, -3.5, 0])
            self.play(FadeOut(spring), FadeIn(topo), az.animate.set_value(4.8), run_time=b.remaining(-0.1), rate_func=linear)

        # ---------------- mds6: what distances cannot see
        with self.narrate('mds6') as b:
            nope = txt('distances do not see orientation or multiplicity', 30, GREY_A).move_to(topo)
            self.play(FadeOut(topo), FadeOut(step), FadeIn(nope), az.animate.set_value(5.3), run_time=1.5, rate_func=linear)
            b.wait_sentence(1)
            zoom = txt('$\\Rightarrow$ zoom in', 34, C_FOLD).move_to([6.0, -2.75, 0])
            self.play(FadeIn(zoom), az.animate.set_value(5.7), run_time=b.remaining(-0.1), rate_func=linear)
        cloud.clear_updaters()
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.8)
