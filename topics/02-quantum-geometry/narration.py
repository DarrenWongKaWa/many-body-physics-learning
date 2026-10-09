"""Narration script (English, voice af_bella). One entry per animation beat: (key, text).

Scenes sync to sentence boundaries via self.narrate(key) and Beat.wait_sentence(i).
Sentences are split at . ! ? ; followed by a space, so avoid those inside a sentence.
Pronunciation overrides: [word](/phonemes/) (misaki IPA); stripped from subtitles.
"""

WANNIER = '[Wannier](/vˈɑnjA/)'
BZ = '[Brillouin](/bɹilwˈæn/) zone'

SCRIPT = {
    "S01_Intro": [
        ("intro1", "In a crystal, every electron state carries a momentum, k, and an energy. Plot one against the other and you get the band structure, the picture we usually draw."),
        ("intro2", "But each of those states is also a quantum wavefunction. As k moves, the energy changes, and so does the wavefunction itself. Here, the arrow on the sphere tracks how the state is built from two orbitals."),
        ("intro3", "So we can ask: how fast does the wavefunction change, and how does it twist? The answer is a geometry that lives in momentum space. It is called quantum geometry."),
        ("intro4", "All of it is packed into one object, the quantum geometric tensor. Its real part is the quantum metric, which measures distance between states. Its imaginary part is the Berry curvature, which measures twisting."),
        ("intro5", "Berry curvature became famous long ago, through Hall effects and topology. The quantum metric was largely ignored until recently, when it turned up in nonlinear transport, flat-band superconductivity, and nonlinear optics."),
        ("intro6", "This video follows a review by [Gao](/ɡˈW/), [Nagaosa](/nˌɑɡɑˈOsə/), [Ni](/nˈi/), and [Xu](/ʃˈu/), in Reviews of Modern Physics. Let's build the geometry from scratch."),
    ],
    "S02_Distance": [
        ("dist1", "Start with a simple question: how far apart are two quantum states? The obvious guess is the length of their difference. But that fails."),
        ("dist2", "Multiply a state by a phase, and nothing physical changes. Yet the length of the difference changes a lot. A state is really a ray: a whole circle of phases that all describe the same physics."),
        ("dist3", "So take a small change of the state, and split it in two. One part points along the state itself, and is just a change of phase. The other part is perpendicular to it, and is a genuine change."),
        ("dist4", "The length of the perpendicular part is the true distance, and it defines the quantum metric, g. Equivalently, one minus the squared overlap of two neighbouring states equals g times the squared step."),
        ("dist5", "The phase part has meaning too. It defines the Berry connection. The connection depends on the choice of phase, but its curl, the Berry curvature, does not."),
        ("dist6", "Both pieces combine into the quantum geometric tensor: the overlap of derivatives, with the part along the state projected out. Its real, symmetric part is the metric. Its imaginary, antisymmetric part is minus one half of the Berry curvature."),
    ],
    "S03_Bloch": [
        ("blo1", "To see this concretely, take the simplest case: two orbitals, alpha and beta. Any state is a superposition of the two, so it is a point on a sphere, the Bloch sphere. Pure alpha sits at the north pole, and pure beta at the south pole."),
        ("blo2", "A two-band Hamiltonian is a vector h dotted into the Pauli matrices. Each band's state is just the direction of h, a unit vector n on the sphere."),
        ("blo3", "Then the quantum geometric tensor becomes ordinary geometry on the sphere. The metric is one quarter of the squared distance between nearby points. The Berry curvature is one half of the solid angle that they sweep out."),
        ("blo4", "Take a trivial atomic insulator first, where the whole conduction band is made of the alpha orbital. Every momentum maps to the north pole. Neighbouring states do not move apart, so the metric is zero. A loop of momenta encloses no area, so the Berry curvature is zero too."),
        ("blo5", "Now invert the bands. Near the inversion, the orbital character changes quickly with momentum. Two nearby momenta land far apart on the sphere, so the metric is large. And a small loop in momentum space sweeps out a large patch of the sphere, so the Berry curvature is large too."),
    ],
    "S04_Wrap": [
        ("wrap1", f"Now do this for the whole {BZ}. Take a simple lattice model with a mass parameter, m. Here is a grid of momenta, and here is where each one lands on the sphere."),
        ("wrap2", "With a large mass the band is trivial. The image of the grid stays crumpled near the north pole, the map barely stretches, and the quantum metric is small everywhere."),
        ("wrap3", "Now lower the mass through a band inversion. The grid spreads out, and wraps the entire sphere exactly once. The total Berry curvature, divided by two pi, counts the wrappings. This is the Chern number."),
        ("wrap4", "So the Berry curvature, integrated over the zone, gives topology: a global, quantized number. The quantum metric, by contrast, is a local quantity, and it is never negative."),
        ("wrap5", "Because the quantum geometric tensor is positive semidefinite, the metric is bounded from below by the curvature. Its trace is at least the size of the Berry curvature. So a band with a nonzero Chern number is forced to have a nonzero quantum metric."),
    ],
    "S05_Info": [
        ("info1", "The quantum metric also has a meaning in quantum information. Suppose a state depends on a parameter, lambda, and you want to estimate lambda by measuring the state."),
        ("info2", "If neighbouring states are almost identical, no measurement can tell them apart. If they are far apart, lambda is easy to read out. In fact, the quantum Fisher information, which sets the best possible precision through the [Cramér-Rao](/kɹɑmˈAɹ ɹˈW/) bound, is exactly four times the quantum metric."),
        ("info3", "This also tells us how to measure the metric directly. Prepare a qubit in its ground state, suddenly kick the parameter by a small amount, and measure how likely it is to end up excited. That probability equals the metric times the square of the kick."),
        ("info4", "This is how the quantum metric was first mapped out: in superconducting qubits, and in microcavities of exciton [polaritons](/pəlˈɛɹɪtˌɑnz/), where it was seen to blow up at [Dirac](/dɪɹˈæk/) points."),
    ],
    "S06_Berry": [
        ("ber1", f"Now to electrons in solids. The parameter is the crystal momentum, k, and each band carries its own quantum geometry over the {BZ}."),
        ("ber2", "Build a wave packet from one band, and push it with an electric field. Its momentum changes at a steady rate. But its velocity has two parts: the ordinary group velocity, and an anomalous velocity, perpendicular to the field and proportional to the Berry curvature."),
        ("ber3", "Add up the anomalous velocity of every occupied state, and you get the intrinsic anomalous Hall effect: a Hall current with no magnetic field and no scattering. If the band is a filled Chern band, the Hall conductance is exactly quantized."),
        ("ber4", "This quantum anomalous Hall effect has been seen in magnetic topological insulators, and its fractional cousin in twisted molybdenum [ditelluride](/dˌItˈɛljəɹˌId/) and in rhombohedral graphene."),
        ("ber5", "Symmetry decides what survives. Time reversal makes the curvature odd in k, while inversion makes it even. With both symmetries, it vanishes everywhere."),
        ("ber6", "Break time reversal with magnetism, and you get the anomalous Hall effect. Keep time reversal but break inversion, and the curvature becomes locked to valleys, spins, or layers, giving valley, spin, and layer Hall effects."),
        ("ber7", "Even when every linear Hall effect vanishes, a Berry curvature dipole can survive. The field shifts the Fermi sea, the shifted sea sees uncompensated curvature, and a Hall current appears at second order in the field. This was first seen in few-layer tungsten [ditelluride](/dˌItˈɛljəɹˌId/)."),
    ],
    "S07_Metric": [
        ("met1", "So where does the quantum metric enter the motion of electrons? Through the other bands. An electric field mixes a little of the neighbouring band into each state."),
        ("met2", "That mixing shifts where the electron sits inside the unit cell. This positional shift is a field-induced Berry connection, equal to the field times a tensor called the Berry connection polarizability."),
        ("met3", "For two bands, the polarizability is just the quantum metric divided by half the band gap. The faster the wavefunction changes with k, and the smaller the gap, the bigger the shift."),
        ("met4", f"Here is the catch. This geometric motion is usually tiny compared with ordinary [Drude](/dɹˈudə/) transport, where electrons simply accelerate until they scatter. To see the metric, the [Drude](/dɹˈudə/) part has to be suppressed."),
        ("met5", "There are two ways to do that. One is to make the band flat, so that the electrons have no group velocity at all."),
        ("met6", "The other is to go to higher order, and separate the pieces by symmetry and by how they scale with the scattering time, tau. The nonlinear [Drude](/dɹˈudə/) term grows as tau squared, the Berry curvature dipole as tau, and the quantum metric dipole does not depend on tau at all."),
    ],
    "S08_NLHE": [
        ("nl1", "Follow the second route, and you reach the intrinsic nonlinear Hall effect. Its source is the quantum metric dipole: an uneven distribution of the metric around the Fermi surface, larger on one side than on the other."),
        ("nl2", "Symmetry tells us where to look. The metric dipole is odd under time reversal, and odd under inversion, but even under their combination, P T. The Berry curvature dipole behaves differently: it is even under time reversal. So the metric dipole lives in P T symmetric antiferromagnets."),
        ("nl3", "Here is the picture. In a P T symmetric antiferromagnet, the Berry curvature vanishes at every k, so there is no anomalous Hall effect at all."),
        ("nl4", "Apply an electric field, and it induces a Berry curvature, proportional to the metric dipole times the field. The driven system now has a Hall conductivity. Acting a second time, the field drives a Hall current that grows as E squared."),
        ("nl5", "This was observed in twenty twenty-three, in even-layer manganese bismuth telluride, an antiferromagnetic topological insulator. Interfacing it with black phosphorus breaks its threefold rotation symmetry, which would otherwise forbid the effect."),
        ("nl6", f"The evidence is convincing. The signal flips sign when the antiferromagnetic order is reversed, so it is odd under time reversal, which rules out a Berry curvature dipole. It vanishes above the [Néel](/nAˈɛl/) temperature. It does not depend on the scattering time. It is antisymmetric, as a true Hall response must be. And its doping dependence follows the calculated metric dipole."),
        ("nl7", "The effect can even rectify wireless microwave signals into direct current, and in films of manganese tin it survives up to room temperature. One order higher, a quantum metric quadrupole produces a third-order Hall effect, which needs no symmetry breaking at all."),
    ],
    "S09_FlatBand": [
        ("fb1", "Now the first route: flat bands. Think about superconductivity in a band with no dispersion at all. Conventional theory runs into a paradox."),
        ("fb2", "The superfluid stiffness measures how easily the condensate carries a supercurrent. It goes as the density of pairs divided by the effective mass. In a flat band the mass is infinite, so the stiffness should vanish, and superconductivity with it."),
        ("fb3", "The way out is geometry. Expand the energy of the condensate in the gradient of its phase, and a second term appears. It is set not by the band dispersion, but by the quantum metric. The stiffness is a conventional part plus a geometric part."),
        ("fb4", f"Picture it in real space. If the flat band is built from compact, isolated orbitals, the pairs are stuck. But a nontrivial quantum metric forces the {WANNIER} orbitals to spread out and overlap, so pairs can hop. For a Chern band this spread is bounded from below by the Chern number. Topology guarantees a minimum stiffness."),
        ("fb5", "Magic-angle twisted bilayer graphene is the prime test case. Its electrons move about a thousand times slower than in ordinary graphene. Yet the measured superfluid stiffness is far larger than the conventional estimate, which is consistent with a large quantum metric contribution. A fully quantitative account is still being worked out."),
    ],
    "S10_Measure": [
        ("mea1", "Can we see the quantum geometry of a crystal directly? Optics gives one handle. Integrate the absorption spectrum, weighted by one over frequency, and you get the quantum metric integrated over the zone. This is the Souza Wilkens Martin sum rule."),
        ("mea2", "Since every absorbed photon must at least cross the gap, the same sum rule puts an upper bound on the optical gap, set by the electron density and the integrated metric."),
        ("mea3", f"And recently, photoemission has gone further, mapping a quasi quantum geometric tensor point by point in momentum space. In the [kagome](/kəɡˈOmi/) metal cobalt tin, the metric extracted from the measured bands agrees well with theory."),
    ],
    "S11_Outlook": [
        ("out1", "To sum up. The quantum geometric tensor packs two kinds of geometry into one object."),
        ("out2", f"Its imaginary part, the Berry curvature, drives the anomalous, quantum anomalous, valley, spin and layer Hall effects, and the Berry curvature dipole. Its real part, the quantum metric, sets the size of {WANNIER} orbitals, optical sum rules, the stiffness of flat-band superconductors, and the intrinsic nonlinear Hall effect."),
        ("out3", "Where next? Near topological band crossings the geometry diverges, which could drive strong, nonperturbative high-harmonic generation even at weak fields. In fractional Chern insulators, band geometry guides where these exotic states appear, and fluctuations of the metric show up as chiral graviton modes."),
        ("out4", "Geometry can also live in real space, as in [skyrmion](/skˈɜɹmiˌɑn/) spin textures. And it connects to quantum information, where the quantum Fisher information becomes a witness of entanglement."),
        ("out5", "The quantum metric, especially, has only just begun to be explored. Thanks for watching."),
    ],
}
