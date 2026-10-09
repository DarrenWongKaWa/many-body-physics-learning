"""Shared style, narration sync and physics helpers for the scenes."""
import json, os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *
import matplotlib
from matplotlib import cm as mpl_cm

ROOT = Path(__file__).resolve().parent
LANG = os.environ.get('NLHE_LANG', 'zh')
VOICE = os.environ.get('NLHE_VOICE', 'zm_010' if LANG == 'zh' else 'af_bella')
AUDIO = ROOT / 'audio' / VOICE
MANIFEST = json.loads((AUDIO / 'manifest.json').read_text()) if (AUDIO / 'manifest.json').exists() else {}
SUBLOG = ROOT / 'media' / ('sublog' if LANG == 'zh' else f'sublog_{LANG}')

# ---------------------------------------------------------------- style
BG = '#0b0d12'
CJK = 'PingFang SC'
C_E = YELLOW            # electric field
C_J = '#7CFC9A'         # Hall current
C_ELEC = BLUE_C         # electrons
C_POS = '#FF6B5B'       # Berry curvature > 0
C_NEG = '#4FA3FF'       # Berry curvature < 0
C_HOT = '#FFB347'
C_BOX1 = '#FF9F43'      # orange box (crossover)
C_BOX2 = '#C56CF0'      # purple box (bump)
GREY_T = '#9aa0a6'

config.background_color = BG
Tex.set_default(tex_template=TexTemplateLibrary.default)
MathTex.set_default(font_size=40)


def zh(text, size=36, color=WHITE, weight=NORMAL, **kw):
    """On-screen label. Written in Chinese; with NLHE_LANG=en the English entry of
    i18n_en.EN is typeset with LaTeX instead."""
    if LANG == 'en' and text:
        from i18n_en import EN
        s = EN[text]
        if weight == BOLD:
            s = r'\textbf{' + s + '}'
        return Tex(s, font_size=size * 1.12, color=color)
    return Text(text, font=CJK, font_size=size, color=color, weight=weight, **kw)


def caption(text, size=30, color=GREY_T):
    return zh(text, size=size, color=color)


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
        """Wait until t seconds after the beat started."""
        dt = t - self.elapsed()
        if dt > 0.02:
            self.scene.wait(dt)

    def wait_sentence(self, i):
        self.wait_until(self.sentence_start(i))

    def frac(self, f):
        """Duration corresponding to fraction f of the beat."""
        return self.dur * f


class Narrated:
    """Mixin: `with self.narrate('key') as b:` plays the audio and pads time."""

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


class NScene(Narrated, Scene):
    pass


class N3DScene(Narrated, ThreeDScene):
    pass


# ---------------------------------------------------------------- physics
DX, DY = 0.5, 1.0
NODE = np.arccos(DX)            # nodal kx = +-pi/3
DKX = np.arccos(0.2) - NODE     # 0.3218: outer Fermi edge to node at mu=0.3


def dvec(kx, ky, Dx=DX, Dy=DY):
    return np.cos(kx) - Dx, np.sin(ky), np.cos(ky) - Dy


def eps(kx, ky, Dx=DX, Dy=DY):
    dx, dy, dz = dvec(kx, ky, Dx, Dy)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def berry(kx, ky, Dx=DX, Dy=DY):
    """Upper-band Berry curvature, paper sign convention (positive at the kx<0 node)."""
    e = eps(kx, ky, Dx, Dy)
    return -np.sin(kx) * (1 - Dy * np.cos(ky)) / (2 * np.maximum(e, 1e-9) ** 3)


def n_eq(kx, ky, mu, Gam=0.1, Dx=DX, Dy=DY):
    """Equilibrium (T=0, Lorentzian-broadened) band occupations n+, n-."""
    e = eps(kx, ky, Dx, Dy)
    f = lambda x: 0.5 + np.arctan((mu - x) / Gam) / np.pi
    return f(e), f(-e)


def grid(n=256, lo=-np.pi, hi=np.pi):
    k = lo + (np.arange(n) + 0.5) * (hi - lo) / n
    return np.meshgrid(k, k)


# ---------------------------------------------------------------- images
def rgba_from(values, cmap, vmin, vmax, alpha=None):
    norm = np.clip((values - vmin) / (vmax - vmin), 0, 1)
    rgba = (cmap(norm) * 255).astype(np.uint8)
    if alpha is not None:
        rgba[..., 3] = (np.clip(alpha, 0, 1) * 255).astype(np.uint8)
    return rgba


def signed_rgba(values, vmax, pos=C_POS, neg=C_NEG, bg=BG, gamma=0.6):
    """Diverging map on a dark background: 0 -> background, +/- -> red/blue glow."""
    x = np.clip(values / vmax, -1, 1)
    a = np.abs(x) ** gamma
    cp, cn, cb = (np.array(color_to_rgb(c)) for c in (pos, neg, bg))
    rgb = np.where(x[..., None] >= 0, cb + (cp - cb) * a[..., None], cb + (cn - cb) * a[..., None])
    out = np.concatenate([rgb, np.ones(x.shape + (1,))], -1)
    return (out * 255).astype(np.uint8)


def image_on_axes(rgba, axes, x_range, y_range):
    """ImageMobject stretched over the data rectangle x_range x y_range of `axes`.
    rgba rows are y (from low to high), columns x."""
    img = ImageMobject(rgba[::-1])
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS['bilinear'])
    ll = axes.c2p(x_range[0], y_range[0])
    ur = axes.c2p(x_range[1], y_range[1])
    img.stretch_to_fit_width(ur[0] - ll[0])
    img.stretch_to_fit_height(ur[1] - ll[1])
    img.move_to((ll + ur) / 2)
    return img


def contour_paths(Z, xs, ys, level):
    """Contour lines of Z (rows=y, cols=x) at `level` as lists of (x, y) points."""
    import contourpy
    gen = contourpy.contour_generator(xs, ys, Z)
    return gen.lines(level)


def contour_mobject(axes, Z, xs, ys, level, color=WHITE, width=3, **kw):
    g = VGroup()
    for seg in contour_paths(Z, xs, ys, level):
        if len(seg) < 3:
            continue
        pts = [axes.c2p(x, y) for x, y in seg]
        m = VMobject(stroke_color=color, stroke_width=width, **kw)
        m.set_points_smoothly(pts)
        g.add(m)
    return g


def kspace_axes(width=6.0, height=None, xr=(-np.pi, np.pi), yr=(-np.pi, np.pi), labels=True,
                tick=None):
    height = height or width * (yr[1] - yr[0]) / (xr[1] - xr[0])
    ax = Axes(x_range=[xr[0], xr[1], tick or np.pi / 2], y_range=[yr[0], yr[1], tick or np.pi / 2],
              x_length=width, y_length=height, tips=False,
              axis_config=dict(stroke_color=GREY_B, stroke_width=1.5, include_ticks=False))
    if labels:
        lx = MathTex(r'k_x', font_size=30, color=GREY_B).next_to(ax.x_axis, RIGHT, buff=0.12)
        ly = MathTex(r'k_y', font_size=30, color=GREY_B).next_to(ax.y_axis, UP, buff=0.12)
        ax.add(lx, ly)
    return ax


def frame_box(axes, xr, yr, color=GREY_D, width=1.5):
    return Polygon(axes.c2p(xr[0], yr[0]), axes.c2p(xr[1], yr[0]), axes.c2p(xr[1], yr[1]),
                   axes.c2p(xr[0], yr[1]), stroke_color=color, stroke_width=width)


def node_marks(axes, size=0.09, color=WHITE):
    g = VGroup()
    for s in (-1, 1):
        p = axes.c2p(s * NODE, 0)
        g.add(VGroup(Line(p + size * (UL), p + size * DR), Line(p + size * UR, p + size * DL))
              .set_stroke(color, 3))
    return g


def load(name):
    return np.load(ROOT / 'data' / name, allow_pickle=True)
