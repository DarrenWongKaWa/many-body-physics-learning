"""Shared style, narration sync, physics helpers and drawing helpers for the scenes."""
import json, os
from contextlib import contextmanager
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent
VOICE = os.environ.get('QG_VOICE', 'af_bella')
AUDIO = ROOT / 'audio' / VOICE
MANIFEST = json.loads((AUDIO / 'manifest.json').read_text()) if (AUDIO / 'manifest.json').exists() else {}
SUBLOG = ROOT / 'media' / 'sublog'

# ---------------------------------------------------------------- style
BG = '#0b0d12'
C_G = '#B98CFF'         # quantum metric (purple, as in the review's figures)
C_POS = '#FF6B5B'       # Berry curvature > 0
C_NEG = '#4FA3FF'       # Berry curvature < 0
C_E = YELLOW            # electric field
C_J = '#7CFC9A'         # Hall current
C_A = '#FFB347'         # orbital alpha
C_B = '#5ED6E8'         # orbital beta
C_ELEC = BLUE_C
GREY_T = '#9aa0a6'
C_PANEL = '#161c2a'

config.background_color = BG
Tex.set_default(tex_template=TexTemplateLibrary.default)
MathTex.set_default(font_size=40)


def txt(s, size=36, color=WHITE, bold=False):
    """On-screen English text, typeset with LaTeX (text mode)."""
    if bold:
        s = r'\textbf{' + s + '}'
    return Tex(s, font_size=size, color=color)


def caption(s, size=28, color=GREY_T):
    return txt(s, size, color)


def panel(mob, buff=0.25, color=GREY_D, fill=C_PANEL, opacity=0.85, radius=0.12):
    return SurroundingRectangle(mob, buff=buff, corner_radius=radius, stroke_color=color, stroke_width=1.5,
                                fill_color=fill, fill_opacity=opacity)


def boxed(mob, color=YELLOW, buff=0.15):
    return SurroundingRectangle(mob, buff=buff, color=color, stroke_width=2.5, corner_radius=0.08)


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

    def sentence_end(self, i):
        s = self.seg['sentences']
        return s[i]['end'] if i < len(s) else self.dur

    def wait_until(self, t):
        """Wait until t seconds after the beat started."""
        dt = t - self.elapsed()
        if dt > 0.02:
            self.scene.wait(dt)

    def wait_sentence(self, i):
        self.wait_until(self.sentence_start(i))

    def until_sentence(self, i, minimum=0.3):
        """Time left until sentence i starts (for run_time of a slow animation)."""
        return max(minimum, self.sentence_start(i) - self.elapsed())

    def frac(self, f):
        return self.dur * f


class Narrated:
    """Mixin: `with self.narrate('key') as b:` plays the audio and pads the beat to its length."""

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


# ---------------------------------------------------------------- two-band physics
def qwz_d(kx, ky, m):
    """Qi-Wu-Zhang Chern-insulator model d(k) = (sin kx, sin ky, m - cos kx - cos ky).
    m > 2: trivial (C = 0, states near the north pole); 0 < m < 2: |C| = 1."""
    return np.sin(kx), np.sin(ky), m - np.cos(kx) - np.cos(ky)


def unit(d):
    dx, dy, dz = d
    r = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
    return dx / r, dy / r, dz / r


def geometry(nfun, kx, ky, h=1e-4):
    """Quantum metric g_ij and Berry curvature Omega of the upper band of h.sigma, n = nfun(kx, ky) = h/|h|:
    G = Tr[P d_i P d_j P] with P = (1 + n.sigma)/2 gives g_ij = (1/4) d_i n . d_j n and
    Omega = -2 Im G_xy = -(1/2) n . (d_x n x d_y n)."""
    n = np.array(nfun(kx, ky))
    nx = (np.array(nfun(kx + h, ky)) - np.array(nfun(kx - h, ky))) / (2 * h)
    ny = (np.array(nfun(kx, ky + h)) - np.array(nfun(kx, ky - h))) / (2 * h)
    gxx = 0.25 * (nx * nx).sum(0)
    gyy = 0.25 * (ny * ny).sum(0)
    gxy = 0.25 * (nx * ny).sum(0)
    om = -0.5 * (n * np.cross(nx, ny, axis=0)).sum(0)
    return gxx, gyy, gxy, om


def grid(n=256, lo=-np.pi, hi=np.pi):
    k = lo + (np.arange(n) + 0.5) * (hi - lo) / n
    return np.meshgrid(k, k)


# ---------------------------------------------------------------- images
def signed_rgba(values, vmax, pos=C_POS, neg=C_NEG, bg=BG, gamma=0.6):
    """Diverging map on a dark background: 0 -> background, +/- -> red/blue glow."""
    x = np.clip(values / vmax, -1, 1)
    a = np.abs(x) ** gamma
    cp, cn, cb = (np.array(color_to_rgb(c)) for c in (pos, neg, bg))
    rgb = np.where(x[..., None] >= 0, cb + (cp - cb) * a[..., None], cb + (cn - cb) * a[..., None])
    out = np.concatenate([rgb, np.ones(x.shape + (1,))], -1)
    return (out * 255).astype(np.uint8)


def mono_rgba(values, vmax, color=C_G, bg=BG, gamma=0.6):
    """Sequential map on a dark background (for the quantum metric, which is >= 0)."""
    a = np.clip(values / vmax, 0, 1) ** gamma
    c, cb = np.array(color_to_rgb(color)), np.array(color_to_rgb(bg))
    rgb = cb + (c - cb) * a[..., None]
    out = np.concatenate([rgb, np.ones(values.shape + (1,))], -1)
    return (out * 255).astype(np.uint8)


def image_on_axes(rgba, axes, x_range, y_range):
    """ImageMobject stretched over the data rectangle of `axes`. rgba rows are y (low to high)."""
    img = ImageMobject(rgba[::-1])
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS['bilinear'])
    ll = axes.c2p(x_range[0], y_range[0])
    ur = axes.c2p(x_range[1], y_range[1])
    img.stretch_to_fit_width(ur[0] - ll[0])
    img.stretch_to_fit_height(ur[1] - ll[1])
    img.move_to((ll + ur) / 2)
    return img


def contour_mobject(axes, Z, xs, ys, level, color=WHITE, width=3, **kw):
    import contourpy
    g = VGroup()
    for seg in contourpy.contour_generator(xs, ys, Z).lines(level):
        if len(seg) < 3:
            continue
        m = VMobject(stroke_color=color, stroke_width=width, **kw)
        m.set_points_smoothly([axes.c2p(x, y) for x, y in seg])
        g.add(m)
    return g


def kspace_axes(width=5.0, xr=(-np.pi, np.pi), yr=(-np.pi, np.pi), labels=True, color=GREY_B):
    height = width * (yr[1] - yr[0]) / (xr[1] - xr[0])
    ax = Axes(x_range=[xr[0], xr[1], np.pi], y_range=[yr[0], yr[1], np.pi], x_length=width, y_length=height,
              tips=False, axis_config=dict(stroke_color=color, stroke_width=1.5, include_ticks=False))
    if labels:
        ax.add(MathTex(r'k_x', font_size=30, color=color).next_to(ax.x_axis, RIGHT, buff=0.12),
               MathTex(r'k_y', font_size=30, color=color).next_to(ax.y_axis, UP, buff=0.12))
    return ax


def frame_box(axes, xr, yr, color=GREY_D, width=1.5):
    return Polygon(axes.c2p(xr[0], yr[0]), axes.c2p(xr[1], yr[0]), axes.c2p(xr[1], yr[1]),
                   axes.c2p(xr[0], yr[1]), stroke_color=color, stroke_width=width)


# ---------------------------------------------------------------- Bloch sphere (orthographic 2D drawing)
class Sphere2D(VGroup):
    """Orthographic drawing of a sphere seen from elevation `el` and azimuth `az` (radians).
    Everything is 2D, so it composes freely with other panels. Use .p(n) for the screen
    position of a unit vector n and .curve(points) for a path on the sphere whose hidden
    (back) part is drawn faint."""

    def __init__(self, radius=1.6, el=0.38, az=0.5, color=GREY_B, n_merid=0, **kw):
        super().__init__(**kw)
        self.R, self.el, self.az, self.col = radius, el, az, color
        self.center_pt = ORIGIN.copy()
        self.disk = Circle(radius=radius, stroke_width=0, fill_color='#1b2436', fill_opacity=1)
        self.disk.set_sheen(-0.45, UL)
        self.outline = Circle(radius=radius, stroke_color=color, stroke_width=2)
        lat = [np.array([np.cos(t), np.sin(t), 0 * t]) for t in np.linspace(0, TAU, 121)]
        self.equator = self.curve(lat, color=color, width=1.3, back_opacity=0.25)
        self.merids = VGroup()
        for j in range(n_merid):
            ph = PI * j / n_merid
            pts = [np.array([np.sin(t) * np.cos(ph), np.sin(t) * np.sin(ph), np.cos(t)])
                   for t in np.linspace(0, TAU, 121)]
            self.merids.add(self.curve(pts, color=color, width=1.0, back_opacity=0.12, front_opacity=0.35))
        self.zaxis = self.curve([np.array([0, 0, z]) for z in np.linspace(-1.12, 1.12, 30)],
                                color=GREY_D, width=1.3, back_opacity=0.6)
        self.add(self.disk, self.equator, self.merids, self.zaxis, self.outline)

    # camera basis
    def basis(self):
        el, az = self.el, self.az
        c = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
        e1 = np.array([-np.sin(az), np.cos(az), 0.0])
        e2 = np.array([-np.sin(el) * np.cos(az), -np.sin(el) * np.sin(az), np.cos(el)])
        return c, e1, e2

    def p(self, n, r=1.0):
        c, e1, e2 = self.basis()
        n = np.asarray(n, float)
        return self.get_center() + self.R * r * (np.dot(n, e1) * RIGHT + np.dot(n, e2) * UP)

    def depth(self, n):
        return float(np.dot(np.asarray(n, float), self.basis()[0]))

    def curve(self, pts3d, color=WHITE, width=3, back_opacity=0.25, front_opacity=1.0, r=1.0, smooth=True):
        """Path on (or near) the sphere: front runs solid, back runs faint."""
        g = VGroup()
        if len(pts3d) < 2:
            return g
        c = self.basis()[0]
        front = [np.dot(np.asarray(q), c) >= 0 for q in pts3d]
        run = [pts3d[0]]
        for a, b, fa, fb in zip(pts3d[:-1], pts3d[1:], front[:-1], front[1:]):
            if fa == fb:
                run.append(b)
            else:
                g.add(self._seg(run + [b], color, width, front_opacity if fa else back_opacity, r, smooth))
                run = [a, b]
        g.add(self._seg(run, color, width, front_opacity if front[-1] else back_opacity, r, smooth))
        return g

    def _seg(self, pts, color, width, op, r, smooth):
        m = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=op)
        q = [self.p(x, r) for x in pts]
        if 3 <= len(q) <= 90 and smooth:
            m.set_points_smoothly(q)
        else:
            m.set_points_as_corners(q)
        return m

    def pole_labels(self, size=34):
        a = MathTex(r'|\alpha\rangle', font_size=size, color=C_A).next_to(self.p([0, 0, 1], 1.12), UP, buff=0.05)
        b = MathTex(r'|\beta\rangle', font_size=size, color=C_B).next_to(self.p([0, 0, -1], 1.12), DOWN, buff=0.05)
        return VGroup(a, b)

    def arrow(self, n, color=WHITE, width=5):
        return Arrow(self.get_center(), self.p(n), buff=0, color=color, stroke_width=width,
                     max_tip_length_to_length_ratio=0.12, max_stroke_width_to_length_ratio=10)

    def dot(self, n, color=WHITE, radius=0.07):
        d = Dot(self.p(n), radius=radius, color=color)
        if self.depth(n) < 0:
            d.set_opacity(0.45)
        return d


def bloch_vec(theta, phi):
    return np.array([np.sin(theta) * np.cos(phi), np.sin(theta) * np.sin(phi), np.cos(theta)])


def slerp_path(n1, n2, num=40):
    n1, n2 = np.asarray(n1, float), np.asarray(n2, float)
    om = np.arccos(np.clip(np.dot(n1, n2), -1, 1))
    if om < 1e-6:
        return [n1, n2]
    return [(np.sin((1 - t) * om) * n1 + np.sin(t * om) * n2) / np.sin(om) for t in np.linspace(0, 1, num)]


# =============================================================================================
# Topic 04 additions: one band of the QWZ model on the Brillouin torus [0, 2pi]^2 (M at the centre),
# orientation colours, an orthographic camera with painter's-algorithm meshes, and BZ panels.
# =============================================================================================
C_UP = '#4FA3FF'        # sheet lands face up   (Omega > 0 for the band followed in the video, C = +1)
C_FLIP = '#FF6B5B'      # sheet lands flipped   (Omega < 0)
C_FOLD = '#FFD166'      # fold curve (det g = 0)
C_PROP = '#5FD38D'      # proposal (unpublished extension) -- green, as in the study guide
C_GEO = '#F2F2F2'       # geodesics
M_CHERN, M_TRIV = 1.0, 3.2
TAU_K = 2 * np.pi


def qwz_geom(kx, ky, m=M_CHERN):
    """Band with Bloch vector n = d/|d|, d = (sin kx, sin ky, m - cos kx - cos ky).
    Returns n (3,...), metric g (2,2,...) = (1/4) dn.dn, Berry curvature Om = -(1/2) n.(dx n x dy n), det g."""
    kx, ky = np.asarray(kx, float), np.asarray(ky, float)
    d = np.stack([np.sin(kx), np.sin(ky), m - np.cos(kx) - np.cos(ky)])
    z = np.zeros_like(kx)
    dx = np.stack([np.cos(kx), z, np.sin(kx)])
    dy = np.stack([z, np.cos(ky), np.sin(ky)])
    r = np.linalg.norm(d, axis=0)
    n = d / r
    nx = (dx - n * (n * dx).sum(0)) / r
    ny = (dy - n * (n * dy).sum(0)) / r
    g = 0.25 * np.array([[(nx * nx).sum(0), (nx * ny).sum(0)], [(nx * ny).sum(0), (ny * ny).sum(0)]])
    om = -0.5 * (n * np.cross(nx, ny, axis=0)).sum(0)
    detg = g[0, 0] * g[1, 1] - g[0, 1] ** 2
    return n, g, om, detg


def qwz_n(kx, ky, m=M_CHERN):
    d = np.stack([np.sin(kx), np.sin(ky), m - np.cos(kx) - np.cos(ky)])
    return d / np.linalg.norm(d, axis=0)


def orient_color(om):
    return C_UP if om >= 0 else C_FLIP


# ---------------------------------------------------------------- orthographic camera
class Cam:
    """Orthographic view from elevation `el` and azimuth `az` (radians); `scale` scene units per unit length."""

    def __init__(self, el=0.38, az=0.5, scale=1.0, center=ORIGIN):
        self.el, self.az, self.scale = el, az, scale
        self.center = np.array(center, float)

    def basis(self):
        el, az = self.el, self.az
        c = np.array([np.cos(el) * np.cos(az), np.cos(el) * np.sin(az), np.sin(el)])
        e1 = np.array([-np.sin(az), np.cos(az), 0.0])
        e2 = np.array([-np.sin(el) * np.cos(az), -np.sin(el) * np.sin(az), np.cos(el)])
        return c, e1, e2

    def p(self, X):
        """Screen point(s) of 3D point(s) X (last axis = 3)."""
        c, e1, e2 = self.basis()
        X = np.asarray(X, float)
        sx, sy = X @ e1, X @ e2
        out = np.stack([sx, sy, np.zeros_like(sx)], -1) * self.scale
        return out + self.center

    def depth(self, X):
        return np.asarray(X, float) @ self.basis()[0]


def shade(color, factor):
    rgb = np.clip(np.array(color_to_rgb(color)) * factor, 0, 1)
    return rgb_to_color(rgb)


def mesh(cam, X, colors, opacity=0.9, back_opacity=None, stroke_width=0.6, light=(0.4, 0.3, 1.0),
         ambient=0.55, cull_center=None, on_top=None):
    """Painter's-algorithm quad mesh. X: (nu+1, nv+1, 3) points; colors: (nu, nv) list of colors.
    Two-sided Lambert shading. If back_opacity is given, quads facing away from the viewer
    (outward normal relative to cull_center) get that opacity instead. `on_top` (nu, nv bool) marks quads
    that are drawn after all others when they face the viewer (sheets lying on top of coincident sheets)."""
    X = np.asarray(X, float)
    nu, nv = X.shape[0] - 1, X.shape[1] - 1
    c, _, _ = cam.basis()
    L = np.array(light, float)
    L /= np.linalg.norm(L)
    A, B, Cc, D = X[:-1, :-1], X[1:, :-1], X[1:, 1:], X[:-1, 1:]
    cen = (A + B + Cc + D) / 4
    nrm = np.cross(Cc - A, D - B)
    nn = np.linalg.norm(nrm, axis=-1, keepdims=True)
    nrm = np.where(nn > 1e-12, nrm / np.maximum(nn, 1e-12), 0)
    bright = ambient + (1 - ambient) * np.abs(nrm @ L)
    dep = cen @ c
    if cull_center is not None:
        facing = ((cen - np.asarray(cull_center)) @ c) > 0
    else:
        facing = np.ones(dep.shape, bool)
    key = dep.copy()
    if on_top is not None:
        key = key + 100.0 * (np.asarray(on_top) & facing)
    order = np.argsort(key, axis=None)
    S = cam.p(X)
    g = VGroup()
    for idx in order:
        i, j = divmod(int(idx), nv)
        col = shade(colors[i][j], bright[i, j])
        op = opacity if (back_opacity is None or facing[i, j]) else back_opacity
        if op <= 0.005:
            continue
        poly = Polygon(S[i, j], S[i + 1, j], S[i + 1, j + 1], S[i, j + 1], fill_color=col, fill_opacity=op,
                       stroke_color=col, stroke_width=stroke_width, stroke_opacity=min(1.0, op * 1.1))
        g.add(poly)
    return g


def polyline3d(cam, X, color=WHITE, width=3, back_opacity=None, cull_center=None, opacity=1.0):
    """3D polyline; runs on the far side of cull_center are drawn with back_opacity."""
    X = np.asarray(X, float)
    S = cam.p(X)
    if back_opacity is None or cull_center is None:
        return VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity).set_points_as_corners(S)
    c = cam.basis()[0]
    front = ((X - np.asarray(cull_center)) @ c) >= 0
    g = VGroup()
    start = 0
    for i in range(1, len(X) + 1):
        if i == len(X) or front[i] != front[start]:
            seg = S[max(start - 1, 0):i]
            if len(seg) >= 2:
                g.add(VMobject(stroke_color=color, stroke_width=width,
                               stroke_opacity=opacity if front[start] else back_opacity).set_points_as_corners(seg))
            start = i
    return g


# ---------------------------------------------------------------- Brillouin-zone panel on [0, 2pi]^2
def bz_axes(width=4.0, center=ORIGIN, labels=True, color=GREY_B):
    ax = Axes(x_range=[0, TAU_K, np.pi], y_range=[0, TAU_K, np.pi], x_length=width, y_length=width, tips=False,
              axis_config=dict(stroke_color=color, stroke_width=1.2, include_ticks=False)).move_to(center)
    box = frame_box(ax, (0, TAU_K), (0, TAU_K), color=GREY_C)
    g = VGroup(box)
    if labels:
        g.add(MathTex('k_x', font_size=28, color=color).next_to(box.get_corner(DR), RIGHT, buff=0.12),
              MathTex('k_y', font_size=28, color=color).next_to(box.get_corner(UL), UP, buff=0.12))
    ax.set_opacity(0)          # the box replaces the axes lines
    return ax, g


def bz_point_labels(ax, size=26):
    pts = {r'\Gamma': (0, 0), 'X': (np.pi, 0), 'M': (np.pi, np.pi)}
    g = VGroup()
    for s, (x, y) in pts.items():
        d = Dot(ax.c2p(x, y), radius=0.04, color=GREY_A)
        lab = MathTex(s, font_size=size, color=GREY_A).next_to(d, DR if s != r'\Gamma' else UR, buff=0.05)
        g.add(d, lab)
    return g


def bz_cells(ax, nk, colors=None, opacity=0.85, stroke=GREY_E, width=0.6):
    """Squares of an nk x nk grid on [0, 2pi]^2; cell (i, j) covers kx in [i h, (i+1) h], ky in [j h, (j+1) h]."""
    h = TAU_K / nk
    g = VGroup()
    for i in range(nk):
        for j in range(nk):
            col = colors[i][j] if colors is not None else GREY_D
            g.add(Polygon(ax.c2p(i * h, j * h), ax.c2p((i + 1) * h, j * h), ax.c2p((i + 1) * h, (j + 1) * h),
                          ax.c2p(i * h, (j + 1) * h), fill_color=col, fill_opacity=opacity, stroke_color=stroke,
                          stroke_width=width))
    return g


def cell_orient(nk, m=M_CHERN):
    """Orientation colour of each cell, from the sign of the Berry curvature at its centre."""
    h = TAU_K / nk
    c = (np.arange(nk) + 0.5) * h
    KX, KY = np.meshgrid(c, c, indexing='ij')
    _, _, om, _ = qwz_geom(KX, KY, m)
    return [[orient_color(om[i, j]) for j in range(nk)] for i in range(nk)], om


def fold_curve(ax, m=M_CHERN, n=400, color=C_FOLD, width=4):
    ks = np.linspace(0, TAU_K, n)
    KX, KY = np.meshgrid(ks, ks, indexing='xy')
    _, _, om, _ = qwz_geom(KX, KY, m)
    return contour_mobject(ax, om, ks, ks, 0.0, color=color, width=width)


def fold_points(m=M_CHERN, n=600):
    """Points of the fold curve Omega = 0 (kx, ky) for mapping onto the sphere."""
    import contourpy
    ks = np.linspace(0, TAU_K, n)
    KX, KY = np.meshgrid(ks, ks, indexing='xy')
    _, _, om, _ = qwz_geom(KX, KY, m)
    return [np.asarray(s) for s in contourpy.contour_generator(ks, ks, om).lines(0.0) if len(s) > 3]


def lift_factor(om, amount=0.03):
    """Radial lift of flipped cells, so that coincident sheets on the polar cap do not z-fight."""
    return 1 + amount / (1 + np.exp(np.asarray(om) / 0.008))


def sphere_cells(nk, m=M_CHERN, lift=0.03):
    """Corner points (nk+1, nk+1, 3) on the unit sphere of the band map, lifted on flipped cells,
    plus per-cell colours and Berry curvature at the cell centres."""
    ks = np.linspace(0, TAU_K, nk + 1)
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    n, _, om_v, _ = qwz_geom(KX, KY, m)
    cols, om_c = cell_orient(nk, m)
    X = np.moveaxis(n, 0, -1)
    if lift:
        X = X * lift_factor(om_v, lift)[..., None]
    return X, cols, om_c


def torus_wire(cam, R=1.0, r=0.42, nu=10, nv=8, color=GREY_B, width=1.5):
    g = VGroup()
    t = np.linspace(0, TAU, 80)
    for a in np.linspace(0, TAU, nu, endpoint=False):
        P = np.stack([(R + r * np.cos(t)) * np.cos(a), (R + r * np.cos(t)) * np.sin(a), r * np.sin(t)], -1)
        g.add(polyline3d(cam, P, color=color, width=width))
    for b in np.linspace(0, TAU, nv, endpoint=False):
        P = np.stack([(R + r * np.cos(b)) * np.cos(t), (R + r * np.cos(b)) * np.sin(t), r * np.sin(b) + 0 * t], -1)
        g.add(polyline3d(cam, P, color=color, width=width))
    return g
