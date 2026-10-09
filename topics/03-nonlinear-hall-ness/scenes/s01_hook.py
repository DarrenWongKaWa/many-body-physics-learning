import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


class ElectronFlow(VGroup):
    """Dots streaming through a rectangle with velocity (vx, vy), wrapping at the edges."""

    def __init__(self, rect, n=70, vx=0.2, seed=1, **kw):
        super().__init__(**kw)
        rng = np.random.default_rng(seed)
        self.rect = rect
        self.w0 = rect.width
        self.uv = np.c_[rng.uniform(0, 1, n), rng.uniform(0, 1, n)]   # coordinates inside rect
        self.jit = rng.uniform(0.8, 1.2, n)
        self.vx = ValueTracker(vx)       # in units of rect widths / heights per second
        self.vy = ValueTracker(0.0)
        for _ in self.uv:
            self.add(Dot(radius=0.045, color=C_ELEC).set_opacity(0.9))
        self.r_now = 0.045
        self.add_updater(lambda m, dt: m.step(dt))
        self.step(0)

    def step(self, dt):
        v = np.array([self.vx.get_value(), self.vy.get_value()])
        self.uv = (self.uv + dt * v[None] * self.jit[:, None]) % 1.0
        ll = self.rect.get_corner(DL)
        w, h = self.rect.width, self.rect.height
        m = 0.04
        s = w / self.w0
        for d, (u, vv) in zip(self.submobjects, self.uv):
            d.move_to([ll[0] + w * (m + (1 - 2 * m) * u), ll[1] + h * (m + (1 - 2 * m) * vv), 0])
            if abs(max(0.032, 0.045 * s) - d.width / 2) > 1e-3:
                d.scale_to_fit_width(2 * max(0.032, 0.045 * s))


class S01_Hook(NScene):
    def construct(self):
        sample = RoundedRectangle(corner_radius=0.15, width=7.2, height=3.2,
                                  fill_color='#161c2a', fill_opacity=1, stroke_color=GREY_C,
                                  stroke_width=2).shift(0.3 * DOWN)
        lat = VGroup(*[Dot([x, y, 0], radius=0.012, color=GREY_D)
                       for x in np.arange(-3.3, 3.31, 0.3) for y in np.arange(-1.5, 1.51, 0.3)]
                     ).move_to(sample)
        elL = Rectangle(width=0.35, height=3.2, fill_color='#b8932f', fill_opacity=1,
                        stroke_width=0).next_to(sample, LEFT, buff=0)
        elR = elL.copy().next_to(sample, RIGHT, buff=0)
        flow = ElectronFlow(sample)
        Earrow = Arrow(sample.get_left() + 1.0 * LEFT + 2.3 * UP, sample.get_right() + 1.0 * RIGHT + 2.3 * UP,
                       color=C_E, stroke_width=6, buff=0)
        Elab = MathTex(r'\mathbf{E}', color=C_E).next_to(Earrow, UP, buff=0.1)
        Bzero = VGroup(MathTex(r'\mathbf{B}=0', color=WHITE, font_size=40))
        Bzero.add(SurroundingRectangle(Bzero[0], color=GREY_B, buff=0.15, corner_radius=0.1))
        Bzero.to_corner(UR, buff=0.5)

        with self.narrate('hook1') as b:
            self.play(FadeIn(sample), FadeIn(lat), FadeIn(elL), FadeIn(elR), run_time=1.0)
            self.add(flow)
            self.play(GrowArrow(Earrow), Write(Elab), run_time=1.0)
            self.wait(1.2)
            Jarrow = Arrow(sample.get_bottom() + 0.2 * DOWN + 4.5 * RIGHT, sample.get_top() + 0.2 * UP + 4.5 * RIGHT,
                           color=C_J, stroke_width=7, buff=0)
            Jlab = MathTex(r'J_y', color=C_J).next_to(Jarrow, RIGHT, buff=0.1)
            self.play(flow.vy.animate.set_value(0.25), GrowArrow(Jarrow), Write(Jlab), run_time=2.0)
            b.wait_sentence(1)
            self.play(FadeIn(Bzero, shift=0.2 * DOWN), run_time=0.8)

        title = zh('非线性霍尔效应', 44).to_edge(UP, buff=0.35)
        grp = VGroup(sample, lat, elL, elR, Earrow, Elab, Jarrow, Jlab)
        with self.narrate('hook2') as b:
            self.play(FadeOut(Bzero), FadeIn(title, shift=0.2 * DOWN), run_time=1.0)
            self.play(grp.animate.scale(0.55).to_edge(LEFT, buff=0.5).shift(0.3 * DOWN), run_time=1.5)
            ax =Axes(x_range=[0, 1.6, 0.4], y_range=[0, 1.6, 0.4], x_length=5, y_length=3.6, tips=False,
                      axis_config=dict(include_ticks=False, stroke_color=GREY_B)).to_edge(RIGHT, buff=0.8).shift(0.4 * DOWN)
            xl = MathTex(r'E', font_size=36).next_to(ax.x_axis, RIGHT, buff=0.1)
            yl = MathTex(r'J_y', font_size=36, color=C_J).next_to(ax.y_axis, UP, buff=0.1)
            par = ax.plot(lambda x: 0.55 * x**2, x_range=[0, 1.0], color=C_J, stroke_width=5)
            law = MathTex(r'J_y = \chi\, E^2', font_size=44).next_to(ax, UP, buff=0.3)
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), run_time=1.0)
            b.wait_sentence(1)
            self.play(Create(par), Write(law), run_time=2.0)

        with self.narrate('hook3') as b:
            ext = DashedVMobject(ax.plot(lambda x: 0.55 * x**2, x_range=[1.0, 1.55], color=C_J), num_dashes=10)
            alt1 = ax.plot(lambda x: 0.55 + 0.6 * (x - 1.0) - 0.4 * (x - 1.0)**2, x_range=[1.0, 1.55],
                           color=C_BOX1, stroke_width=4)
            alt2 = ax.plot(lambda x: 0.55 + 1.1 * (x - 1.0) - 1.5 * (x - 1.0)**2, x_range=[1.0, 1.55],
                           color=C_BOX2, stroke_width=4)
            q = Text('?', font_size=72, color=WHITE).move_to(ax.c2p(1.35, 1.3))
            strong = zh('强电场', 28, C_E).next_to(ax.c2p(1.3, 0), DOWN, buff=0.2)
            self.play(Create(ext), FadeIn(strong), run_time=1.5)
            self.play(Create(alt1), Create(alt2), FadeIn(q, scale=1.5), run_time=1.5)
            b.wait_sentence(1)
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
            self.remove(flow)
            t1 = zh('非平衡稳态中的非微扰非线性霍尔效应', 46, weight=BOLD)
            t2 = Text('Nonperturbative Nonlinear Hall Effect in Nonequilibrium Steady States',
                      font_size=26, color=BLUE_B)
            t3 = Text('L. Geng, M. Eckstein, L. Chen, S. Sur, S. Paschen, Q. Si, P. Werner',
                      font_size=22, color=GREY_B)
            t4 = Text('arXiv:2607.01519', font_size=22, color=GREY_C)
            if LANG == 'en':     # t1 already is the English title
                card = VGroup(t1, t3, t4).arrange(DOWN, buff=0.32)
                t4.shift(0.1 * DOWN)
                line = Line(LEFT * 5.5, RIGHT * 5.5, stroke_width=1.5, color=GREY_D).next_to(t1, DOWN, buff=0.16)
                self.play(Write(t1), run_time=1.6)
                self.play(Create(line), run_time=0.8)
            else:
                card = VGroup(t1, t2, t3, t4).arrange(DOWN, buff=0.32)
                line = Line(LEFT * 5.5, RIGHT * 5.5, stroke_width=1.5, color=GREY_D).next_to(t2, DOWN, buff=0.16)
                self.play(Write(t1), run_time=1.6)
                self.play(FadeIn(t2, shift=0.2 * UP), Create(line), run_time=1.0)
            self.play(FadeIn(t3), FadeIn(t4), run_time=0.8)
        self.wait(1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
