"""Nonequilibrium steady state of the dc-driven two-band model with a constant-Gamma
wide-band reservoir (Geng et al., arXiv:2607.01519, Eqs. 1-3).

Method: in the temporal gauge the kinetic momentum drifts, kappa(t) = kappa0 + E t x.
For a local wide-band bath (Sigma^R = -i Gamma, Sigma^<(w) = 2i Gamma f(w)) the
equal-time density matrix is

    n(kappa(t)) = int dw/2pi 2 Gamma f(w) eta_w(t) eta_w(t)^dagger,
    i d/dt eta_w = (H(kappa(t)) - w - i Gamma) eta_w + 1,

i.e. each bath frequency w drives a damped 2x2 amplitude eta_w. One trajectory per ky
sweeps every kx once per Bloch period 2 pi / E, so Jy = BZ-average Tr[v_y n] becomes a
time average. The propagator is exact for H frozen at the step midpoint.
At E = 0, eta_w = G^R(w) and n = int f A dw/2pi (equilibrium), which is the start state.
"""
import math
import numpy as np
from numba import njit, prange

DX, DY = 0.5, 1.0


@njit(cache=True, inline='always')
def dvec(kx, ky, Dx, Dy):
    return math.cos(kx) - Dx, math.sin(ky), math.cos(ky) - Dy


@njit(cache=True, inline='always')
def berry_upper(kx, ky, Dx, Dy):
    """Upper-band Berry curvature, sign chosen as in the paper (positive at kx<0 node)."""
    dx, dy, dz = dvec(kx, ky, Dx, Dy)
    d = math.sqrt(dx * dx + dy * dy + dz * dz)
    return -math.sin(kx) * (1.0 - Dy * math.cos(ky)) / (2.0 * d * d * d)


@njit(parallel=True, cache=True)
def run_kernel(E, Gam, Dx, Dy, kys, omegas, wts, wbin, nbins, Nkx, m_sub, dt, n_burn,
               record_maps):
    Nky = kys.shape[0]
    Nw = omegas.shape[0]
    J = np.zeros((Nky, nbins))
    BC = np.zeros((Nky, nbins))
    occ = np.zeros((nbins, Nky, Nkx if record_maps else 1))
    nup = np.zeros((nbins, Nky, Nkx if record_maps else 1))
    n_rec = Nkx * m_sub
    kx_start = -math.pi - E * dt * n_burn
    for iy in prange(Nky):
        ky = kys[iy]
        uy = math.cos(ky)
        uz = -math.sin(ky)
        for j in range(Nw):
            b = wbin[j]
            if b >= nbins:
                continue
            w = wts[j]
            z = omegas[j] + 1j * Gam
            # equilibrium start: eta = (z - H)^-1
            dx, dy, dz = dvec(kx_start, ky, Dx, Dy)
            dn = math.sqrt(dx * dx + dy * dy + dz * dz)
            gp = 1.0 / (z - dn)
            gm = 1.0 / (z + dn)
            a0 = 0.5 * (gp + gm)
            h = 0.5 * (gp - gm) / dn
            ax = h * dx
            ay = h * dy
            az = h * dz
            jacc = 0.0
            bacc = 0.0
            for n in range(n_burn + n_rec):
                kxm = kx_start + E * dt * (n + 0.5)
                dx, dy, dz = dvec(kxm, ky, Dx, Dy)
                dn = math.sqrt(dx * dx + dy * dy + dz * dz)
                mp = np.exp(-1j * (dn - z) * dt)
                mm = np.exp(-1j * (-dn - z) * dt)
                fp = (mp - 1.0) / (dn - z)
                fm = (mm - 1.0) / (-dn - z)
                M0 = 0.5 * (mp + mm)
                B0 = 0.5 * (fp + fm)
                M1 = 0.5 * (mp - mm) / dn
                B1 = 0.5 * (fp - fm) / dn
                px = M1 * dx
                py = M1 * dy
                pz = M1 * dz
                # (M0 + p.s)(a0 + a.s) = M0 a0 + p.a + (M0 a + a0 p + i p x a).s
                na0 = M0 * a0 + px * ax + py * ay + pz * az + B0
                nax = M0 * ax + a0 * px + 1j * (py * az - pz * ay) + B1 * dx
                nay = M0 * ay + a0 * py + 1j * (pz * ax - px * az) + B1 * dy
                naz = M0 * az + a0 * pz + 1j * (px * ay - py * ax) + B1 * dz
                a0, ax, ay, az = na0, nax, nay, naz
                if n + 1 > n_burn:
                    # rho = r0 + r.s  with r = 2 Re(a0 a*) + i a x a*
                    r0 = (a0 * a0.conjugate()).real + (ax * ax.conjugate()).real \
                        + (ay * ay.conjugate()).real + (az * az.conjugate()).real
                    cx = ay * az.conjugate() - az * ay.conjugate()
                    cy = az * ax.conjugate() - ax * az.conjugate()
                    cz = ax * ay.conjugate() - ay * ax.conjugate()
                    rx = 2.0 * (a0 * ax.conjugate()).real + (1j * cx).real
                    ry = 2.0 * (a0 * ay.conjugate()).real + (1j * cy).real
                    rz = 2.0 * (a0 * az.conjugate()).real + (1j * cz).real
                    jacc += 2.0 * (uy * ry + uz * rz)
                    kxe = kx_start + E * dt * (n + 1)
                    ex, ey, ez = dvec(kxe, ky, Dx, Dy)
                    en = math.sqrt(ex * ex + ey * ey + ez * ez)
                    dr = (ex * rx + ey * ry + ez * rz) / en
                    bacc += 2.0 * dr * berry_upper(kxe, ky, Dx, Dy)  # (n+ - n-) Omega+
                    if record_maps:
                        s = n + 1 - n_burn
                        if s % m_sub == 0:
                            ik = (s // m_sub) % Nkx   # s = n_rec wraps to kx = -pi
                            occ[b, iy, ik] += w * 2.0 * r0
                            nup[b, iy, ik] += w * (r0 + dr)
            J[iy, b] += w * jacc / n_rec
            BC[iy, b] += w * bacc / n_rec
    return J, BC, occ, nup


def solve(E, Gam=0.1, mus=(0.3,), Nky=256, Nkx=256, dw=None, wmin=-3.6, dt_max=0.1,
          burn=12.0, Dx=DX, Dy=DY, record_maps=False):
    """Steady state at field E. Returns dict with Jy/E, BC estimate / E and maps per mu."""
    mus = np.sort(np.asarray(mus, float))
    if dw is None:
        dw = min(0.01, Gam / 10)
    nW = int(round((mus[-1] - wmin) / dw))
    edges = mus[-1] - dw * np.arange(nW, -1, -1)
    omegas = 0.5 * (edges[1:] + edges[:-1])
    wts = np.full(omegas.shape, Gam / np.pi * dw)
    wbin = np.searchsorted(mus, omegas).astype(np.int64)
    kys = -np.pi + (np.arange(Nky) + 0.5) * 2 * np.pi / Nky
    if E > 0:
        m_sub = max(1, math.ceil(2 * np.pi / (Nkx * E * dt_max)))
        dt = 2 * np.pi / (Nkx * E * m_sub)
    else:
        raise ValueError('E must be > 0')
    n_burn = int(math.ceil(burn / Gam / dt))
    J, BC, occ, nup = run_kernel(E, Gam, Dx, Dy, kys, omegas, wts, wbin, len(mus), Nkx,
                                 m_sub, dt, n_burn, record_maps)
    Jmu = np.cumsum(J.sum(0))[: len(mus)] / Nky
    BCmu = np.cumsum(BC.sum(0))[: len(mus)] / Nky
    out = dict(E=E, Gam=Gam, mus=mus, JyE=Jmu / E, BCE=BCmu, kys=kys, dt=dt)
    if record_maps:
        kxs = -np.pi + np.arange(Nkx) * 2 * np.pi / Nkx
        KX, KY = np.meshgrid(kxs, kys)
        dx, dy, dz = np.cos(KX) - Dx, np.sin(KY), np.cos(KY) - Dy
        dn = np.sqrt(dx**2 + dy**2 + dz**2)
        tail_p = (np.arctan((wmin - dn) / Gam) + np.pi / 2) / np.pi
        tail_m = (np.arctan((wmin + dn) / Gam) + np.pi / 2) / np.pi
        out['kxs'] = kxs
        out['occ'] = np.cumsum(occ, 0) + (tail_p + tail_m)[None]
        out['nup'] = np.cumsum(nup, 0) + tail_p[None]
    return out


if __name__ == '__main__':
    import time
    for E in [0.01, 0.03, 0.05]:
        t0 = time.time()
        r = solve(E, 0.1, mus=[0.0, 0.3], Nky=128)
        print(f'E={E}: Jy/E={r["JyE"]*1e4} e-4  BC={r["BCE"]*1e4} e-4  ({time.time()-t0:.1f}s)')
