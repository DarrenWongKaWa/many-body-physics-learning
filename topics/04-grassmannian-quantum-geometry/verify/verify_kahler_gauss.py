"""
Numerical check of two claims about the Riemannian geometry of the
quantum-state (projector) manifold of Bloch bands:

 (1) Kähler angle:  Omega_xy = 2 cos(theta_K) sqrt(det g)   (standard convention
     Q_{mu nu} = tr(P dP_mu dP_nu) = g - (i/2) Omega ), with |cos theta_K| <= 1.
     Two-band models: cos theta_K = +-1 and sign flips across fold curves (det g = 0).
     N >= 3 bands: det g > 0 (immersion) and theta_K varies continuously.

 (2) Gauss equation on the Grassmannian  Gr(k,N) ⊂ Herm(N):
        K_G = K_Gr(sigma) + K_II ,
        K_Gr(sigma) = ||[X_1,X_2]||^2 / det g_H = (||F_occ||_F^2 + ||F_unocc||_F^2)/det g_H
     (Huang's metric convention g_H = tr(dP dP) = 2 g),
     and for rank-1 projectors  K_Gr = (1 + 3 cos^2 theta_K)/2  (Huang convention).
     K_G is checked independently with the intrinsic Brioschi formula.
     For N >= 3 (immersed torus) Gauss-Bonnet gives  ∫ K_G dA = 0.

All projector derivatives are exact (first-order perturbation theory for dP,
Sylvester equation + idempotency for d^2 P); no gauge choice is ever made.
"""
import os
import numpy as np

sx = np.array([[0, 1], [1, 0]], complex)
sy = np.array([[0, -1j], [1j, 0]], complex)
sz = np.array([[1, 0], [0, -1]], complex)
PAULI = np.stack([sx, sy, sz])


# ----------------------------------------------------------------------------
# models: return H, dH (2,...), d2H (2,2,...) on a k-grid, shapes (n,n,N,N)
# ----------------------------------------------------------------------------
def qwz_blocks(kx, ky, m0, scale=1.0):
    s, c, z = np.sin, np.cos, np.zeros_like(kx)
    d = np.stack([s(kx), s(ky), m0 - c(kx) - c(ky)], -1) * scale
    dx = np.stack([c(kx), z, s(kx)], -1) * scale
    dy = np.stack([z, c(ky), s(ky)], -1) * scale
    dxx = np.stack([-s(kx), z, c(kx)], -1) * scale
    dyy = np.stack([z, -s(ky), c(ky)], -1) * scale
    dxy = np.zeros_like(d)
    mat = lambda v: np.einsum('...i,ijk->...jk', v, PAULI)
    H = mat(d)
    dH = np.stack([mat(dx), mat(dy)])
    d2H = np.stack([[mat(dxx), mat(dxy)], [mat(dxy), mat(dyy)]])
    return H, dH, d2H


def model2(kx, ky, m0=1.0):
    return qwz_blocks(kx, ky, m0)


def model3(kx, ky, m0=1.0, a1=0.8, a2=0.6, b1=0.3, b2=0.2j, e0=4.5, e1=0.5):
    """QWZ Chern block coupled to a third orbital (generic, no symmetry)."""
    H2, dH2, d2H2 = qwz_blocks(kx, ky, m0)
    n = kx.shape
    H = np.zeros(n + (3, 3), complex)
    dH = np.zeros((2,) + n + (3, 3), complex)
    d2H = np.zeros((2, 2) + n + (3, 3), complex)
    H[..., :2, :2] = H2
    dH[..., :2, :2] = dH2
    d2H[..., :2, :2] = d2H2
    ex, ey, z = np.exp(1j * kx), np.exp(1j * ky), np.zeros_like(kx, dtype=complex)
    c = np.stack([a1 * ex + b1, a2 * ey + b2], -1)
    cx = np.stack([1j * a1 * ex, z], -1)
    cy = np.stack([z, 1j * a2 * ey], -1)
    cxx = np.stack([-a1 * ex, z], -1)
    cyy = np.stack([z, -a2 * ey], -1)
    cxy = np.zeros_like(c)
    eps, epsd, epsdd = e0 + e1 * np.cos(kx + ky), -e1 * np.sin(kx + ky), -e1 * np.cos(kx + ky)

    def put(Hm, cv, e):
        Hm[..., :2, 2] = cv
        Hm[..., 2, :2] = np.conj(cv)
        Hm[..., 2, 2] = e

    put(H, c, eps)
    put(dH[0], cx, epsd)
    put(dH[1], cy, epsd)
    put(d2H[0, 0], cxx, epsdd)
    put(d2H[1, 1], cyy, epsdd)
    put(d2H[0, 1], cxy, epsdd)
    put(d2H[1, 0], cxy, epsdd)
    return H, dH, d2H


def model4(kx, ky):
    """Two QWZ blocks (C=1 each) + generic k-dependent coupling; occupied rank 2."""
    HA, dHA, d2HA = qwz_blocks(kx, ky, 1.0)
    HB, dHB, d2HB = qwz_blocks(kx, ky, 0.5, scale=0.8)
    n = kx.shape
    V0 = 0.15 * np.array([[1, 0.5j], [0.3, -0.7]])
    V1 = 0.12 * np.array([[0.4, 1], [-0.6j, 0.2]])
    V2 = 0.10 * np.array([[0.9j, -0.3], [0.5, 0.8]])
    ex, ey = np.exp(1j * kx)[..., None, None], np.exp(1j * ky)[..., None, None]
    V = V0 + V1 * ex + V2 * ey
    Vx, Vy = 1j * V1 * ex, 1j * V2 * ey
    Vxx, Vyy, Vxy = -V1 * ex, -V2 * ey, np.zeros_like(V)

    def assemble(A, B, C):
        M = np.zeros(n + (4, 4), complex)
        M[..., :2, :2] = A
        M[..., 2:, 2:] = B
        M[..., :2, 2:] = C
        M[..., 2:, :2] = np.conj(np.swapaxes(C, -1, -2))
        return M

    H = assemble(HA, HB, V)
    dH = np.stack([assemble(dHA[0], dHB[0], Vx), assemble(dHA[1], dHB[1], Vy)])
    d2H = np.stack([[assemble(d2HA[0, 0], d2HB[0, 0], Vxx), assemble(d2HA[0, 1], d2HB[0, 1], Vxy)],
                    [assemble(d2HA[1, 0], d2HB[1, 0], Vxy), assemble(d2HA[1, 1], d2HB[1, 1], Vyy)]])
    return H, dH, d2H


# ----------------------------------------------------------------------------
# gauge-free projector geometry
# ----------------------------------------------------------------------------
def tr(A):
    return np.trace(A, axis1=-2, axis2=-1)


def dag(A):
    return np.conj(np.swapaxes(A, -1, -2))


def comm(A, B):
    return A @ B - B @ A


def acomm(A, B):
    return A @ B + B @ A


def projector_geometry(H, dH, d2H, k):
    """Everything is computed in the eigenbasis of H(k) (all outputs are unitary
    invariants, so this is legitimate); P = diag(1_k, 0)."""
    np.seterr(divide='ignore', invalid='ignore')
    E, U = np.linalg.eigh(H)
    N = E.shape[-1]
    Ud = dag(U)
    Ht = np.einsum('...ij,m...jk,...kl->m...il', Ud, dH, U)
    Htt = np.einsum('...ij,mn...jk,...kl->mn...il', Ud, d2H, U)
    shape = E.shape[:-1]
    P = np.zeros(shape + (N, N), complex)
    P[..., :k, :k] = np.eye(k)
    Q = np.eye(N) - P
    gap = (E[..., k] - E[..., k - 1]).min()

    # first derivatives: (b,a) block = <b|dH|a>/(E_a-E_b), b unocc, a occ
    den1 = E[..., None, :k] - E[..., k:, None]           # E_a - E_b
    T = np.zeros((2,) + shape + (N, N), complex)
    for m in range(2):
        blk = Ht[m][..., k:, :k] / den1
        T[m][..., k:, :k] = blk
        T[m][..., :k, k:] = dag(blk)

    # second derivatives: Sylvester for off-diagonal blocks, idempotency for diagonal
    den2 = E[..., k:, None] - E[..., None, :k]           # E_b - E_a
    TT = np.zeros((2, 2) + shape + (N, N), complex)
    resid_un, resid_occ = 0.0, 0.0
    for m in range(2):
        for n in range(2):
            R = -comm(Htt[m, n], P) - comm(Ht[n], T[m]) - comm(Ht[m], T[n])
            M = np.zeros(shape + (N, N), complex)
            blk = R[..., k:, :k] / den2
            M[..., k:, :k] = blk
            M[..., :k, k:] = dag(blk)
            AC = acomm(T[m], T[n])
            M[..., :k, :k] = -AC[..., :k, :k]
            M[..., k:, k:] = AC[..., k:, k:]
            TT[m, n] = M
            # consistency: (E_b-E_b') M_bb' = R_bb' on unocc block, and
            # (E_a-E_a') M_aa' = R_aa' on occ block (both must hold automatically)
            dEu = E[..., k:, None] - E[..., None, k:]
            dEo = E[..., :k, None] - E[..., None, :k]
            resid_un = max(resid_un, np.abs(dEu * M[..., k:, k:] - R[..., k:, k:]).max())
            resid_occ = max(resid_occ, np.abs(dEo * M[..., :k, :k] - R[..., :k, :k]).max())

    out = dict(E=E, gap=gap, resid_un=resid_un, resid_occ=resid_occ)

    # metrics (Huang: g_H = tr(T T); standard: g = Re tr(P T T))
    gH = np.real(np.array([[tr(T[m] @ T[n]) for n in range(2)] for m in range(2)]))
    Qgt = np.array([[tr(P @ T[m] @ T[n]) for n in range(2)] for m in range(2)])
    g = np.real(Qgt)
    Om = -2 * np.imag(Qgt[0, 1])
    detg = g[0, 0] * g[1, 1] - g[0, 1] ** 2
    detgH = gH[0, 0] * gH[1, 1] - gH[0, 1] ** 2
    cos_th = Om / (2 * np.sqrt(detg))
    out.update(g=g, gH=gH, Om=Om, detg=detg, detgH=detgH, cos_th=cos_th)

    # Kähler form from the complex structure J T = i[P,T]  (independent route)
    JT1 = 1j * comm(P, T[0])
    omega_H = np.real(tr(JT1 @ T[1]))
    out['omega_H_minus_Om'] = np.abs(omega_H - Om).max()

    # horizontal generators and Grassmannian sectional curvature
    X = [comm(T[m], P) for m in range(2)]
    C12 = comm(X[0], X[1])
    normC = np.real(-tr(C12 @ C12))
    B = [T[m][..., k:, :k] for m in range(2)]
    Focc = dag(B[0]) @ B[1] - dag(B[1]) @ B[0]
    Fun = B[0] @ dag(B[1]) - B[1] @ dag(B[0])
    normF = np.real(tr(Focc @ dag(Focc)) + tr(Fun @ dag(Fun)))
    out['K_Gr_H'] = normC / detgH
    out['normC_minus_normF'] = np.abs(normC - normF).max()
    if k == 1:
        out['K_Gr_H_kahler'] = (1 + 3 * cos_th ** 2) / 2

    # second fundamental forms (Gauss equation) -------------------------------
    gHm = np.moveaxis(gH, (0, 1), (-2, -1))
    ginvH = np.linalg.pinv(gHm)                                   # (...,2,2), robust near folds

    def tangential(M):
        c = [np.real(tr(M @ T[b])) for b in range(2)]
        coef = [ginvH[..., a, 0] * c[0] + ginvH[..., a, 1] * c[1] for a in range(2)]
        return coef[0][..., None, None] * T[0] + coef[1][..., None, None] * T[1]

    IIf = [[TT[m, n] - tangential(TT[m, n]) for n in range(2)] for m in range(2)]
    Ad = [[P @ TT[m, n] @ P + Q @ TT[m, n] @ Q for n in range(2)] for m in range(2)]
    IIin = [[(P @ TT[m, n] @ Q + Q @ TT[m, n] @ P) - tangential(TT[m, n]) for n in range(2)]
            for m in range(2)]
    gauss = lambda II: np.real(tr(II[0][0] @ II[1][1]) - tr(II[0][1] @ II[0][1])) / detgH
    out['K_G_H'] = gauss(IIf)
    out['K_GrGauss_H'] = gauss(Ad)
    out['K_II_H'] = gauss(IIin)
    return out


def brioschi(g, h):
    """Intrinsic Gauss curvature of a 2x2 metric field g[a,b](kx,ky) on a periodic grid."""
    E, F, G = g[0, 0], g[0, 1], g[1, 1]
    d = lambda f, ax: (np.roll(f, -1, axis=ax) - np.roll(f, 1, axis=ax)) / (2 * h)
    d2 = lambda f, ax: (np.roll(f, -1, axis=ax) - 2 * f + np.roll(f, 1, axis=ax)) / h ** 2
    Eu, Ev, Gu, Gv, Fu, Fv = d(E, 0), d(E, 1), d(G, 0), d(G, 1), d(F, 0), d(F, 1)
    Evv, Guu, Fuv = d2(E, 1), d2(G, 0), d(d(F, 0), 1)
    M1 = np.array([[-Evv / 2 + Fuv - Guu / 2, Eu / 2, Fu - Ev / 2],
                   [Fv - Gu / 2, E, F],
                   [Gv / 2, F, G]])
    M2 = np.array([[0 * E, Ev / 2, Gu / 2],
                   [Ev / 2, E, F],
                   [Gu / 2, F, G]])
    det = lambda M: np.linalg.det(np.moveaxis(M, (0, 1), (-2, -1)))
    return (det(M1) - det(M2)) / (E * G - F ** 2) ** 2


def fd_check(model, kx0=0.37, ky0=-1.1, h=1e-4):
    """finite-difference check of the analytic dH, d2H of a model at one k point"""
    f = lambda a, b: model(np.array([[a]]), np.array([[b]]))[0][0, 0]
    H, dH, d2H = model(np.array([[kx0]]), np.array([[ky0]]))
    dHx = (f(kx0 + h, ky0) - f(kx0 - h, ky0)) / (2 * h)
    dHy = (f(kx0, ky0 + h) - f(kx0, ky0 - h)) / (2 * h)
    dxx = (f(kx0 + h, ky0) - 2 * f(kx0, ky0) + f(kx0 - h, ky0)) / h ** 2
    dyy = (f(kx0, ky0 + h) - 2 * f(kx0, ky0) + f(kx0, ky0 - h)) / h ** 2
    dxy = (f(kx0 + h, ky0 + h) - f(kx0 + h, ky0 - h) - f(kx0 - h, ky0 + h) + f(kx0 - h, ky0 - h)) / (4 * h ** 2)
    return max(np.abs(dH[0][0, 0] - dHx).max(), np.abs(dH[1][0, 0] - dHy).max(),
               np.abs(d2H[0, 0][0, 0] - dxx).max(), np.abs(d2H[1, 1][0, 0] - dyy).max(),
               np.abs(d2H[0, 1][0, 0] - dxy).max())


# ----------------------------------------------------------------------------
def run(model, k, n, label):
    ks = (np.arange(n) + 0.5) * (2 * np.pi / n)   # half-step offset avoids exact fold/cusp points
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    h = 2 * np.pi / n
    H, dH, d2H = model(KX, KY)
    o = projector_geometry(H, dH, d2H, k)
    dk2 = h ** 2
    N = H.shape[-1]
    print(f"\n==== {label}: N={N}, occupied rank k={k}, grid {n}x{n} ====")
    print(f"model dH/d2H vs finite differences : {fd_check(model):.1e}")
    print(f"min gap between band {k} and {k+1}  : {o['gap']:.4f}")
    print(f"d^2P Sylvester consistency (unocc,occ blocks): {o['resid_un']:.1e}, {o['resid_occ']:.1e}")
    C = o['Om'].sum() * dk2 / (2 * np.pi)
    vol = np.sqrt(o['detg']).sum() * dk2
    print(f"Chern number  (1/2pi)∫Ω           : {C:+.6f}")
    print(f"min det g (standard conv.)        : {o['detg'].min():.3e}   max: {o['detg'].max():.3e}")
    print(f"cos theta_K  range                 : [{o['cos_th'].min():+.4f}, {o['cos_th'].max():+.4f}]")
    print(f"max |cos theta_K| - 1              : {np.abs(o['cos_th']).max()-1:+.2e}")
    print(f"Kähler form via J=i[P,·] vs Ω      : {o['omega_H_minus_Om']:.1e}")
    print(f"quantum volume ∫√det g             : {vol:.6f}  (π|C| = {np.pi*abs(C):.6f}),"
          f"  ∫(1-cosθ)dA = {((1-np.sign(C)*o['cos_th'])*np.sqrt(o['detg'])).sum()*dk2:.6f}")
    print(f"||[X1,X2]||² vs ||F_occ||²+||F_un||² : {o['normC_minus_normF']:.1e}")
    print(f"K_Gr (‖[X1,X2]‖²/det g) vs Gauss eq. of Gr⊂Herm : {np.abs(o['K_Gr_H']-o['K_GrGauss_H']).max():.1e}")
    if k == 1:
        print(f"K_Gr vs (1+3cos²θ)/2               : {np.abs(o['K_Gr_H']-o['K_Gr_H_kahler']).max():.1e}")
    KB = brioschi(o['gH'], h)                       # intrinsic, Huang convention
    good = o['detg'] > 1e-3 * o['detg'].max()      # mask near-degenerate points (2-band folds)
    err_gauss = np.abs(o['K_G_H'] - o['K_Gr_H'] - o['K_II_H'])[good].max()
    err_brio = np.abs(o['K_G_H'] - KB)[good].max() / np.abs(KB[good]).max()
    print(f"K_G (Gauss eq. in Herm) vs K_Gr + K_II : {err_gauss:.1e}")
    print(f"K_G vs intrinsic Brioschi (rel.)   : {err_brio:.1e}   [masked {100*(~good).mean():.1f}% of BZ]")
    print(f"K_G  range (Huang conv.)           : [{o['K_G_H'][good].min():.4f}, {o['K_G_H'][good].max():.4f}]")
    print(f"K_Gr range (Huang conv.)           : [{o['K_Gr_H'][good].min():.4f}, {o['K_Gr_H'][good].max():.4f}]")
    print(f"K_II range (Huang conv.)           : [{o['K_II_H'][good].min():.4f}, {o['K_II_H'][good].max():.4f}]")
    dA_H = np.sqrt(o['detgH']) * dk2
    if o['detg'].min() > 0:
        print(f"Gauss-Bonnet ∫K_G dA /2π           : {(o['K_G_H']*dA_H).sum()/(2*np.pi):+.6f}  (χ(T²)=0)")
        print(f"           ∫K_Gr dA /2π, ∫K_II dA /2π : {(o['K_Gr_H']*dA_H).sum()/(2*np.pi):+.4f}, "
              f"{(o['K_II_H']*dA_H).sum()/(2*np.pi):+.4f}")
    o.update(KX=KX, KY=KY, C=C, good=good, KB=KB, label=label, N=N, k=k)
    return o



# ----------------------------------------------------------------------------
# complex points of a rank-1 band in a 3-band model: zeros of w = B_x ∧ B_y
# (there |cos theta_K| = 1).  det g = Ω²/4 + |w|²  (Lagrange identity).
# Signed count of zeros = degree of Λ²(L^⊥) ⊗ L^{-2} = -3C.
# ----------------------------------------------------------------------------
def wedge_field(model, n):
    ks = (np.arange(n) + 0.5) * (2 * np.pi / n)
    KX, KY = np.meshgrid(ks, ks, indexing='ij')
    H, dH, _ = model(KX, KY)
    E, U = np.linalg.eigh(H)
    Ht = np.einsum('...ij,m...jk,...kl->m...il', dag(U), dH, U)
    Bx = Ht[0][..., 1:, 0] / (E[..., None, 0] - E[..., 1:])
    By = Ht[1][..., 1:, 0] / (E[..., None, 0] - E[..., 1:])
    w = Bx[..., 0] * By[..., 1] - Bx[..., 1] * By[..., 0]
    wn = np.abs(w) / (np.linalg.norm(Bx, axis=-1) * np.linalg.norm(By, axis=-1))
    return KX, KY, w, wn


def winding(model, kx0, ky0, r=0.05, M=800):
    """winding of arg w around a small loop, in a parallel-transport gauge (Berry-phase corrected)"""
    t = np.linspace(0, 2 * np.pi, M, endpoint=False)
    lx, ly = kx0 + r * np.cos(t), ky0 + r * np.sin(t)
    Hl, dHl, _ = model(lx[:, None], ly[:, None])
    Hl, dHl = Hl[:, 0], dHl[:, :, 0]
    El, Ul = np.linalg.eigh(Hl)
    for j in range(1, M):
        ov = np.einsum('ia,ia->a', np.conj(Ul[j - 1]), Ul[j])
        Ul[j] *= np.exp(-1j * np.angle(ov))
    gamma = -np.angle(np.einsum('ia,ia->a', np.conj(Ul[-1]), Ul[0]))
    Hlt = np.einsum('mij,nmjk,mkl->nmil', dag(Ul), dHl, Ul)
    bx = Hlt[0][:, 1:, 0] / (El[:, None, 0] - El[:, 1:])
    by = Hlt[1][:, 1:, 0] / (El[:, None, 0] - El[:, 1:])
    wl = bx[:, 0] * by[:, 1] - bx[:, 1] * by[:, 0]
    dphi = np.angle(wl[1:] / wl[:-1]).sum() + np.angle(wl[0] / wl[-1])
    return (dphi - (2 * gamma[0] - gamma[1] - gamma[2])) / (2 * np.pi)


def complex_points(model, n=600):
    from scipy import ndimage
    KX, KY, w, wn = wedge_field(model, n)
    mn = ndimage.minimum_filter(wn, size=9, mode='wrap')
    pts = []
    for i, j in np.argwhere((wn == mn) & (wn < 0.3)):
        wd = winding(model, KX[i, j], KY[i, j])
        if abs(wd) > 0.5:
            pts.append((KX[i, j], KY[i, j], int(round(wd))))
    return pts


if __name__ == '__main__':
    n = 240
    r2 = run(model2, 1, n, "two-band QWZ (m0=1)")
    r3 = run(model3, 1, n, "three-band: QWZ ⊕ orbital, coupled")
    r4 = run(model4, 2, n, "four-band, two occupied (rank-2 projector)")

    # ------------------------------------------------------------------ figure
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.colors import SymLogNorm

    cp = complex_points(model3)
    print("complex points of the 3-band model (k_x, k_y, winding):", cp,
          "  signed total =", sum(p[2] for p in cp), " (theory: -3C =", -3 * round(r3['C']), ")")

    fig, ax = plt.subplots(2, 3, figsize=(15.5, 9.2))
    ext = [0, 2 * np.pi, 0, 2 * np.pi]

    def show(a, F, title, cmap='viridis', **kw):
        im = a.imshow(F.T, origin='lower', extent=ext, cmap=cmap, aspect='equal', **kw)
        a.set_title(title, fontsize=10.5)
        a.set_xlabel(r'$k_x$'); a.set_ylabel(r'$k_y$')
        a.set_xticks([0, np.pi, 2 * np.pi]); a.set_xticklabels(['0', r'$\pi$', r'$2\pi$'])
        a.set_yticks([0, np.pi, 2 * np.pi]); a.set_yticklabels(['0', r'$\pi$', r'$2\pi$'])
        plt.colorbar(im, ax=a, fraction=0.046, pad=0.04)

    # row 1: two-band
    show(ax[0, 0], r2['cos_th'], r'2-band QWZ: $\cos\theta_K=\Omega/(2\sqrt{\det g})=\pm1$; black: fold ($\det g=0$)',
         cmap='RdBu', vmin=-1, vmax=1)
    ax[0, 0].contour(r2['KX'], r2['KY'], r2['Om'], levels=[0], colors='k', linewidths=1.2)
    show(ax[0, 1], np.log10(r2['detg'] + 1e-12), r'2-band: $\log_{10}\det g$ (fold curve where $\det g\to0$)')
    ax[0, 1].contour(r2['KX'], r2['KY'], r2['Om'], levels=[0], colors='k', linewidths=1.2)
    KG2 = np.where(r2['good'], 2 * r2['K_G_H'], np.nan)
    show(ax[0, 2], KG2, r'2-band: $K_G=4$ (std. conv.) off the fold;  $\int K_G d\bar A=4\pi C$', vmin=3.9, vmax=4.1)

    # row 2: three-band
    show(ax[1, 0], r3['cos_th'], r'3-band: $\cos\theta_K$ continuous; black: $\Omega=0$ ($\theta_K=\pi/2$); '
         '\n' r'markers: complex points $|\cos\theta_K|=1$ (+: winding +1, x: -1), signed count $=3|C|$',
         cmap='RdBu', vmin=-1, vmax=1)
    ax[1, 0].contour(r3['KX'], r3['KY'], r3['Om'], levels=[0], colors='k', linewidths=1.2)
    for kx0, ky0, wd in cp:
        ax[1, 0].plot(kx0, ky0, 'k+' if wd > 0 else 'kx', ms=12, mew=2.5)
        ax[1, 0].plot(kx0, ky0, 'w+' if wd > 0 else 'wx', ms=10, mew=1.2)
    K3 = 2 * r3['K_G_H']; K3II = 2 * r3['K_II_H']
    show(ax[1, 1], K3, r'3-band: $K_G$ (std. conv., symlog scale);  $\int K_G dA=0$',
         cmap='coolwarm', norm=SymLogNorm(linthresh=5, vmin=-np.abs(K3).max(), vmax=np.abs(K3).max()))
    show(ax[1, 2], K3II, r'3-band: extrinsic part $K_{II}=K_G-(1+3\cos^2\theta_K)$ (symlog)',
         cmap='coolwarm', norm=SymLogNorm(linthresh=5, vmin=-np.abs(K3II).max(), vmax=np.abs(K3II).max()))
    fig.suptitle('Kähler angle and Gauss-equation decomposition of the quantum-state manifold '
                 '(2-band QWZ vs. coupled 3-band model, lowest band, C=-1)', fontsize=12.5)
    plt.tight_layout()
    plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'kahler_gauss_check.png'), dpi=140, bbox_inches='tight')
    print("\nfigure saved")
