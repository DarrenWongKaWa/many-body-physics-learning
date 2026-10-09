"""Shared style, narration sync, i18n and resonant-level physics for the Keldysh scenes."""
import json, os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent
LANG = os.environ.get('NLHE_LANG', 'zh')
VOICE = os.environ.get('NLHE_VOICE', 'zm_010' if LANG == 'zh' else 'af_bella')
AUDIO = ROOT / 'audio' / VOICE
MANIFEST = json.loads((AUDIO / 'manifest.json').read_text()) if (AUDIO / 'manifest.json').exists() else {}
SUBLOG = ROOT / 'media' / ('sublog' if LANG == 'zh' else f'sublog_{LANG}')

# ---------------------------------------------------------------- style
BG = '#0b0d12'
CJK = 'PingFang SC'
C_FWD = '#58C4DD'       # forward branch / retarded
C_BWD = '#FF8A5B'       # backward branch / advanced
C_LESS = '#7CFC9A'      # lesser
C_GTR = '#C56CF0'       # greater
C_IM = '#B0B0B0'        # imaginary-time leg
C_L = '#4FA3FF'         # left lead
C_R = '#FF6B5B'         # right lead
C_DOT = YELLOW
C_HI = '#FFB347'
GREY_T = '#9aa0a6'

config.background_color = BG
MathTex.set_default(font_size=40)


def zh(text, size=36, color=WHITE, weight=NORMAL, **kw):
    """On-screen label written in Chinese; with NLHE_LANG=en the entry of i18n_en.EN is
    typeset with LaTeX instead."""
    if LANG == 'en' and text:
        from i18n_en import EN
        s = EN[text]
        if weight == BOLD:
            s = r'\textbf{' + s + '}'
        return Tex(s, font_size=size * 1.12, color=color)
    return Text(text, font=CJK, font_size=size, color=color, weight=weight, **kw)


# ---------------------------------------------------------------- narration
class Beat:
    def __init__(self, scene, key):
        self.scene, self.key = scene, key
        self.seg = MANIFEST.get(key, dict(dur=3.0, sentences=[]))
        self.t0 = scene.renderer.time
        self.dur = self.seg['dur']

    def elapsed(self):
        return self.scene.renderer.time - self.t0

    def remaining(self, pad=0.0):
        return max(0.0, self.dur - self.elapsed() + pad)

    def sentence_start(self, i):
        s = self.seg['sentences']
        return s[i]['start'] if i < len(s) else self.dur

    def wait_until(self, t):
        dt = t - self.elapsed()
        if dt > 0.02:
            self.scene.wait(dt)

    def wait_sentence(self, i):
        self.wait_until(self.sentence_start(i))

    def rest(self, minimum=0.5, minus=0.0):
        """A run_time that fills what is left of the beat (never shorter than `minimum`)."""
        return max(minimum, self.remaining() - minus)


class Narrated:
    def setup(self):
        super().setup()
        self._sublog = []

    @contextmanager
    def narrate(self, key, pad=0.35):
        b = Beat(self, key)
        wav = AUDIO / f'{key}.wav'
        if wav.exists():
            self.add_sound(str(wav))
        self._sublog.append(dict(key=key, t0=round(b.t0, 3)))
        yield b
        rem = b.remaining(pad)
        if rem > 0.02:
            self.wait(rem)

    def tear_down(self):
        SUBLOG.mkdir(parents=True, exist_ok=True)
        (SUBLOG / f'{type(self).__name__}.json').write_text(
            json.dumps(dict(beats=self._sublog, total=round(self.renderer.time, 3))))
        super().tear_down()

    def clear(self, run_time=0.7):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)


class NScene(Narrated, Scene):
    pass


# ---------------------------------------------------------------- Keldysh contour drawing
def contour_path(x0=-5.5, x1=4.5, y=0.0, gap=0.5, r=None):
    """Forward branch at y+gap/2 (left->right), half-circle turn, backward branch at y-gap/2."""
    r = r or gap / 2
    top, bot = y + gap / 2, y - gap / 2
    fwd = Line([x0, top, 0], [x1, top, 0])
    turn = ArcBetweenPoints([x1, top, 0], [x1, bot, 0], angle=-PI)
    bwd = Line([x1, bot, 0], [x0, bot, 0])
    return fwd, turn, bwd


def keldysh_contour(x0=-5.5, x1=4.5, y=0.0, gap=0.5, width=4, tips=True):
    fwd, turn, bwd = contour_path(x0, x1, y, gap)
    g = VGroup(fwd.set_stroke(C_FWD, width), turn.set_stroke(GREY_B, width), bwd.set_stroke(C_BWD, width))
    if tips:
        for line, c in ((fwd, C_FWD), (bwd, C_BWD)):
            mid = line.point_from_proportion(0.5)
            d = line.get_unit_vector()
            g.add(Triangle(fill_color=c, fill_opacity=1, stroke_width=0).scale(0.09)
                  .rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(mid))
    return g


# ---------------------------------------------------------------- resonant level (wide-band limit)
def fermi(e, mu, kT):
    return 0.5 * (1 - np.tanh((e - mu) / (2 * kT)))


def lorentz_A(e, e0, G):
    return G / ((e - e0) ** 2 + (G / 2) ** 2)


def transmission(e, e0, GL, GR):
    return GL * GR / ((e - e0) ** 2 + ((GL + GR) / 2) ** 2)


def current_gf(V, e0, GL, GR, kT, n=6001):
    """J = int de/2pi T(e)[fL - fR] with muL = +V/2, muR = -V/2 (units e/hbar)."""
    G = GL + GR
    lo, hi = min(-V / 2, e0) - 40 * (G + kT), max(V / 2, e0) + 40 * (G + kT)
    e = np.linspace(lo, hi, n)
    integrand = transmission(e, e0, GL, GR) * (fermi(e, V / 2, kT) - fermi(e, -V / 2, kT))
    return np.trapezoid(integrand, e) / (2 * np.pi)


def current_me(V, e0, GL, GR, kT):
    return GL * GR / (GL + GR) * (fermi(e0, V / 2, kT) - fermi(e0, -V / 2, kT))


def en(text, size=30, color=WHITE):
    """English label typeset with LaTeX (used by the physical-picture beats)."""
    return Tex(text, font_size=size * 1.12, color=color)


def occupation_relax(ts, n0, e0, GL, GR, muL, muR, kT=0.005):
    """Exact n(t) of a single level (wide-band leads switched on at t = 0, initial occupation n0):
    n(t) = n0 e^{-Gt} + int de/2pi [GL fL + GR fR] |1 - e^{(i(e-e0) - G/2)t}|^2 / ((e-e0)^2 + G^2/4)."""
    G = GL + GR
    e = np.linspace(e0 - 60 * G, e0 + 60 * G, 24001)
    gin = GL * fermi(e, muL, kT) + GR * fermi(e, muR, kT)
    z = 1j * (e - e0) - G / 2
    out = []
    for t in ts:
        integrand = gin * np.abs(1 - np.exp(z * t)) ** 2 / ((e - e0) ** 2 + G ** 2 / 4)
        out.append(n0 * np.exp(-G * t) + np.trapezoid(integrand, e) / (2 * np.pi))
    return np.array(out)
