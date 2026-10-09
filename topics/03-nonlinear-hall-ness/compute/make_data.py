"""Produce all datasets used by the animation (writes data/*.npz)."""
import sys, time, numpy as np
sys.path.insert(0, 'compute')
from negf import solve

def fig1b():
    mus = [0.0, 0.06, 0.12, 0.18, 0.24, 0.30, 0.36, 0.42]
    Es = np.round(np.arange(0.0025, 0.3501, 0.0025), 5)
    J = []
    for E in Es:
        r = solve(E, 0.1, mus=mus, Nky=256); J.append(r['JyE'])
    np.savez('data/fig1b.npz', E=Es, mus=mus, JyE=np.array(J))

def fig1c():
    Gs = [0.05, 0.075, 0.1, 0.125, 0.15]
    Es = np.round(np.arange(0.001, 0.0801, 0.001), 5)
    J = np.zeros((len(Gs), len(Es)))
    for i, G in enumerate(Gs):
        for k, E in enumerate(Es):
            J[i, k] = solve(E, G, mus=[0.3], Nky=256)['JyE'][0]
    np.savez('data/fig1c.npz', E=Es, Gam=Gs, JyE=J)

def maps():
    Es = np.round(np.arange(0.0025, 0.1501, 0.0025), 5)
    occ, nup, J = [], [], []
    for E in Es:
        r = solve(E, 0.1, mus=[0.0, 0.3], Nky=256, Nkx=256, record_maps=True)
        occ.append(r['occ'].astype(np.float32)); nup.append(r['nup'].astype(np.float32)); J.append(r['JyE'])
    np.savez_compressed('data/maps.npz', E=Es, mus=[0.0, 0.3], kxs=r['kxs'], kys=r['kys'],
                        occ=np.array(occ), nup=np.array(nup), JyE=np.array(J))

if __name__ == '__main__':
    for name in sys.argv[1:]:
        t0 = time.time(); globals()[name](); print(name, f'{time.time()-t0:.0f}s', flush=True)
