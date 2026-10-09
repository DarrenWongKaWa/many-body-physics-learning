import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from common import *


def junction(muL=1.0, muR=-0.6, e0=0.2, y0=-2.2, scale=1.4):
    """Energy diagram: left/right Fermi seas, two barriers and one dot level."""
    def Y(e):
        return y0 + scale * (e + 1.6)
    g = VGroup()
    seaL = Rectangle(width=3.6, height=Y(muL) - y0, fill_color=C_L, fill_opacity=0.35, stroke_width=0)
    seaL.next_to([-1.4, y0, 0], UL, buff=0).shift(DOWN * 0)
    seaL.align_to([-5.0, y0, 0], LEFT).align_to([0, y0, 0], DOWN)
    seaR = Rectangle(width=3.6, height=Y(muR) - y0, fill_color=C_R, fill_opacity=0.35, stroke_width=0)
    seaR.align_to([1.4, y0, 0], LEFT).align_to([0, y0, 0], DOWN)
    bars = VGroup(*[Rectangle(width=0.22, height=4.4, fill_color=GREY_D, fill_opacity=1, stroke_width=0)
                    .move_to([x, y0 + 2.2, 0]) for x in (-1.3, 1.3)])
    level = Line([-0.55, Y(e0), 0], [0.55, Y(e0), 0], color=C_DOT, stroke_width=6)
    lmuL = DashedLine([-5.0, Y(muL), 0], [-1.42, Y(muL), 0], color=C_L)
    lmuR = DashedLine([1.42, Y(muR), 0], [5.0, Y(muR), 0], color=C_R)
    tL = MathTex(r'\mu_L', color=C_L, font_size=36).next_to(lmuL, LEFT, buff=0.1)
    tR = MathTex(r'\mu_R', color=C_R, font_size=36).next_to(lmuR, RIGHT, buff=0.1)
    te = MathTex(r'\varepsilon_0', color=C_DOT, font_size=36).next_to(level, UP, buff=0.1)
    g.add(seaL, seaR, bars, level, lmuL, lmuR, tL, tR, te)
    g.Y = Y
    return g


class S01_Intro(NScene):
    def construct(self):
        j = junction()
        Y = j.Y
        labels = VGroup(zh('左电极', 28, C_L).move_to([-3.2, 2.6, 0]), zh('量子点', 28, C_DOT).move_to([0, 2.6, 0]),
                        zh('右电极', 28, C_R).move_to([3.2, 2.6, 0]))
        with self.narrate('in1') as b:
            self.play(FadeIn(j[0]), FadeIn(j[1]), FadeIn(j[2]), FadeIn(labels), run_time=1.2)
            self.play(Create(j[3]), FadeIn(j[8]), run_time=0.8)
            b.wait_sentence(1)
            self.play(Create(j[4]), Create(j[5]), FadeIn(j[6]), FadeIn(j[7]), run_time=1.0)
            bias = DoubleArrow([-5.4, Y(-0.6), 0], [-5.4, Y(1.0), 0], buff=0, color=WHITE, stroke_width=3,
                               max_tip_length_to_length_ratio=0.12)
            bl = MathTex('eV', font_size=34).next_to(bias, LEFT, buff=0.1)
            self.play(GrowFromCenter(bias), FadeIn(bl), run_time=0.8)
            # electrons hop L -> dot -> R
            hops = []
            for k in range(6):
                d = Dot([-2.2, Y(0.85), 0], radius=0.09, color=WHITE)
                p1 = ArcBetweenPoints([-2.2, Y(0.85), 0], [0, Y(0.2), 0], angle=-PI / 4)
                p2 = ArcBetweenPoints([0, Y(0.2), 0], [2.2, Y(-0.75), 0], angle=-PI / 4)
                hops.append(Succession(FadeIn(d, run_time=0.15), MoveAlongPath(d, p1, run_time=0.8),
                                       Wait(0.25), MoveAlongPath(d, p2, run_time=0.8), FadeOut(d, run_time=0.2)))
            cur = Arrow([-1.8, 2.0, 0], [1.8, 2.0, 0], color=C_LESS, buff=0, stroke_width=5)
            cl = MathTex('I', color=C_LESS, font_size=36).next_to(cur, UP, buff=0.05)
            self.play(LaggedStart(*hops, lag_ratio=0.35), GrowArrow(cur), FadeIn(cl), run_time=b.rest(2.0))
        scene1 = VGroup(j, labels, bias, bl, cur, cl)
        with self.narrate('in2') as b:
            self.play(scene1.animate.scale(0.6).to_edge(LEFT, buff=0.4), run_time=1.2)
            far = zh('远离平衡', 34, C_HI).move_to([3.3, 1.0, 0])
            self.play(FadeIn(far, shift=0.2 * UP), run_time=0.8)
            b.wait_sentence(1)
            tool = VGroup(zh('凯尔迪什非平衡格林函数', 36, C_LESS), MathTex(r'G^<,\ G^>,\ G^r,\ G^a', font_size=40)
                          ).arrange(DOWN, buff=0.3).move_to([3.3, -0.4, 0])
            self.play(Write(tool[0]), run_time=1.5)
            self.play(FadeIn(tool[1], shift=0.2 * UP), run_time=1.0)
        self.clear()

        t1 = zh('凯尔迪什非平衡格林函数技术入门', 46, weight=BOLD)
        t2 = Text('after lecture notes by A.-P. Jauho', font_size=24, color=GREY_B) if LANG == 'en' else \
            zh('基于 A.-P. Jauho 的讲义', 26, GREY_B)
        card = VGroup(t1, t2).arrange(DOWN, buff=0.35).shift(1.4 * UP)
        steps = ['平衡态微扰论', '凯尔迪什回路', '朗格雷斯规则', '凯尔迪什方程', '电流公式', '共振能级与主方程']
        boxes = VGroup()
        for s in steps:
            t = zh(s, 22)
            boxes.add(VGroup(RoundedRectangle(corner_radius=0.1, width=max(1.9, t.width + 0.3), height=0.8,
                                              stroke_color=GREY_C, stroke_width=1.5, fill_color='#141925',
                                              fill_opacity=1), t))
        boxes.arrange(RIGHT, buff=0.32).shift(1.3 * DOWN)
        if boxes.width > 13.4:
            boxes.scale_to_fit_width(13.4)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.03, color=GREY_B,
                                stroke_width=2, max_tip_length_to_length_ratio=0.5) for i in range(len(boxes) - 1)])
        with self.narrate('in3') as b:
            self.play(Write(t1), run_time=1.6)
            self.play(FadeIn(t2), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(bx, shift=0.2 * RIGHT) for bx in boxes], lag_ratio=0.25),
                      LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.25), run_time=b.rest(3.0, 1.0))
        self.clear()
