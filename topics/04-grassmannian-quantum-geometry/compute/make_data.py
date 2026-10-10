"""Precompute the data the scenes read (nothing heavy is recomputed while rendering).

    python compute/make_data.py            # writes data/mds.npz, data/bargmann.npz, data/kahler.npz

All two-band quantities use the band whose Bloch vector is n = d/|d| of the QWZ model
d(k) = (sin kx, sin ky, m - cos kx - cos ky): standard metric g = (1/4) dn.dn (sphere of radius 1/2),
Berry curvature Omega = -(1/2) n.(dx n x dy n), Chern number +1 at m = 1.

  mds.npz      SMACOF iterations (metric MDS) of the Hilbert-Schmidt distance table of sampled states,
               for m = 1 (Chern band) and m = 3.2 (trivial band), plus classical MDS for comparison   [H1]
  bargmann.npz Bargmann phases of geodesic polygons inscribed in a smooth loop on the Bloch sphere     [H2]
  kahler.npz   cos(theta_K) maps of the lowest band of the two-band QWZ model and of the coupled
               three-band model of verify/, the Berry-zero set, and the complex points               [proposal]
"""
import sys
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'verify'))
DATA = ROOT / 'data'
DATA.mkdir(exist_ok=True)


def nvec(kx, ky, m):
    d = np.stack([np.sin(kx), np.sin(ky), m - np.cos(kx) - np.cos(ky)])
    return d / np.linalg.norm(d, axis=0)


# --------------------------------------------------------------------------- [H1] MDS
def hs_distance_table(n):
    """Hilbert-Schmidt distance D = sqrt(tr(P1-P2)^2 / 2) = |n1 - n2| / 2 between rank-one projectors."""
    diff = n[:, :, None] - n[:, None, :]
    return 0.5 * np.sqrt((diff ** 2).sum(0))


def smacof(D, X0, iters):
    """Unweighted SMACOF (Guttman transform). Returns all iterates and the raw stress."""
    N = len(D)
    X = X0.copy()
    out, stress = [X.copy()], []
    for _ in range(iters):
        dist = np.sqrt(((X[:, None, :] - X[None, :, :]) ** 2).sum(-1))
        with np.errstate(divide='ignore', invalid='ignore'):
            ratio = np.where(dist > 1e-12, D / dist, 0.0)
        B = -ratio
        B[np.diag_indices(N)] = 0.0
        B[np.diag_indices(N)] = -B.sum(1)
        X = B @ X / N
        out.append(X.copy())
        stress.append(0.5 * ((dist - D) ** 2).sum())
    return np.array(out), np.array(stress)


def classical_mds(D, dim=3):
    N = len(D)
    J = np.eye(N) - np.ones((N, N)) / N
    Bm = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(Bm)
    idx = np.argsort(w)[::-1][:dim]
    return V[:, idx] * np.sqrt(np.clip(w[idx], 0, None)), w[np.argsort(w)[::-1]][:6]


def procrustes(X, Y):
    """Rotation/reflection R and shift minimising |X R - Y| (both centred inside)."""
    Xc, Yc = X - X.mean(0), Y - Y.mean(0)
    U, _, Vt = np.linalg.svd(Xc.T @ Yc)
    return U @ Vt, X.mean(0), Y.mean(0)


def make_mds():
    res = {}
    # snapshots kept for the animation: every early step, then sparser (the shape settles quickly)
    keep = np.unique(np.concatenate([np.arange(0, 80), np.arange(80, 400, 4), np.arange(400, 1501, 25)]))
    res['keep'] = keep
    for tag, m, seed in (('chern', 1.0, 7), ('trivial', 3.2, 1)):
        rng = np.random.default_rng(seed)
        nk = 22
        ks = (np.arange(nk) + 0.5) * 2 * np.pi / nk
        KX, KY = np.meshgrid(ks, ks, indexing='ij')
        n = nvec(KX.ravel(), KY.ravel(), m)
        target = 0.5 * n.T                                   # true positions on the radius-1/2 sphere
        D = hs_distance_table(n)
        X0 = rng.normal(scale=0.35, size=(len(D), 3))
        its, stress = smacof(D, X0, 1500)
        R, mx, my = procrustes(its[-1], target)              # orient the final shape like the true sphere
        its = (its - mx) @ R + my
        Xc, ev = classical_mds(D)
        Rc, cx, cy = procrustes(Xc, target)
        Xc = (Xc - cx) @ Rc + cy
        res[f'{tag}_iters'] = its[keep].astype(np.float32)
        res[f'{tag}_stress'] = stress
        res[f'{tag}_classical'] = Xc
        res[f'{tag}_kx'], res[f'{tag}_ky'] = KX.ravel(), KY.ravel()
        res[f'{tag}_D'] = D.astype(np.float32)
        err_s = np.abs(its[-1] - target).max()
        err_c = np.abs(Xc - target).max()
        print(f"MDS {tag:8s} m={m}: N={len(D)}  stress {stress[0]:.3e} -> {stress[-1]:.3e}  "
              f"max|SMACOF - true| = {err_s:.2e}  max|classical - true| = {err_c:.2e}  "
              f"top eigenvalues {np.round(ev, 4)}  nz range [{n[2].min():.3f}, {n[2].max():.3f}]")
    np.savez_compressed(DATA / 'mds.npz', **res)


# --------------------------------------------------------------------------- [H2] Bargmann
def spinor(n):
    th = np.arccos(np.clip(n[2], -1, 1))
    ph = np.arctan2(n[1], n[0])
    return np.array([np.cos(th / 2), np.exp(1j * ph) * np.sin(th / 2)])


def loop(t):
    """A smooth loop around the north pole: polar angle 0.95 + 0.28 cos 3t."""
    th = 0.95 + 0.28 * np.cos(3 * t)
    return np.stack([np.sin(th) * np.cos(t), np.sin(th) * np.sin(t), np.cos(th)])


def make_bargmann():
    t = np.linspace(0, 2 * np.pi, 20001)
    th = 0.95 + 0.28 * np.cos(3 * t)
    S = np.trapezoid(1 - np.cos(th), t)                     # solid angle enclosed (around +z, counter-clockwise)
    Ns = np.array([3, 4, 5, 6, 8, 12, 24, 48, 96])
    phases = []
    for N in Ns:
        tt = 2 * np.pi * np.arange(N) / N
        u = [spinor(v) for v in loop(tt).T]
        B = np.prod([np.vdot(u[i], u[(i + 1) % N]) for i in range(N)])
        phases.append(-np.angle(B))                         # Berry phase of the geodesic polygon
    phases = np.array(phases)
    print(f"Bargmann: smooth loop solid angle S = {S:.5f}, -S/2 = {-S / 2:.5f}; polygon Berry phases:",
          dict(zip(Ns.tolist(), np.round(phases, 5).tolist())))
    np.savez(DATA / 'bargmann.npz', Ns=Ns, phases=phases, S=S)


# --------------------------------------------------------------------------- proposal: Kahler angle
def make_kahler():
    from verify_kahler_gauss import model2, model3, projector_geometry, complex_points
    n = 200
    ks = (np.arange(n) + 0.5) * (2 * np.pi / n)
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    out = dict(ks=ks)
    for tag, model in (('two', model2), ('three', model3)):
        H, dH, d2H = model(KX, KY)
        o = projector_geometry(H, dH, d2H, 1)              # lowest band, rank-one projector
        C = o['Om'].sum() * (2 * np.pi / n) ** 2 / (2 * np.pi)
        sgn = np.sign(C)
        out[f'{tag}_cos'] = sgn * o['cos_th']               # normalised: +1 where the sheet agrees with C
        out[f'{tag}_Om'] = sgn * o['Om']
        out[f'{tag}_C'] = C
        print(f"Kahler {tag}-band: C = {C:+.4f}, sign(C) cos(theta_K) in [{out[tag + '_cos'].min():+.3f}, "
              f"{out[tag + '_cos'].max():+.3f}]")
    cp = complex_points(model3)
    out['cp'] = np.array(cp, float)
    print("complex points (kx, ky, index):", [(round(a, 3), round(b, 3), int(w)) for a, b, w in cp],
          " signed sum =", int(sum(w for *_, w in cp)))
    np.savez_compressed(DATA / 'kahler.npz', **out)


if __name__ == '__main__':
    make_mds()
    make_bargmann()
    make_kahler()
