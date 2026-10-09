"""Narration script (Mandarin). One entry per animation beat: (key, text).

Keys are referenced from scenes.py via self.narrate(key). Numbers and symbols are
written out in Chinese so the TTS reads them correctly.
"""

SCRIPT = {
    "S01_Hook": [
        ("hook1", "沿着一个方向推动电子，电流却拐了个弯，流向了侧面。而且，这里没有任何磁场。"),
        ("hook2", "这就是非线性霍尔效应。在弱电场下，它是一个二阶效应：横向电流正比于电场的平方。"),
        ("hook3", "可是，如果电场很强呢？今天要讲的这篇论文，研究的正是强电场驱动下，非平衡稳态中的非线性霍尔效应。"),
    ],
    "S02_Berry": [
        ("hall1", "先回忆一下普通的霍尔效应。在磁场中运动的电子受到洛伦兹力，向侧面偏转，于是产生横向电流。"),
        ("hall2", "但在一些材料里，即使没有磁场，也会出现横向电流。原因藏在动量空间里：布洛赫电子的波函数带有一种几何性质，叫做贝里曲率。它就像动量空间里的一个等效磁场。"),
        ("hall3", "在电场中，电子会获得一个反常速度。它垂直于电场，大小正比于贝里曲率。"),
        ("hall4", "把所有被占据态的反常速度加起来，就得到了霍尔电流。"),
        ("hall5", "但是，如果材料具有时间反演对称性，贝里曲率在动量 k 和负 k 处大小相等、符号相反。正负相消，积分为零，线性霍尔效应就消失了。"),
    ],
    "S03_Dipole": [
        ("bcd1", "转机出现在二阶。电场会推动整片费米海，在动量空间里平移。"),
        ("bcd2", "平移之后，费米海覆盖的正负贝里曲率不再平衡，于是出现了净的反常速度。平移量正比于电场，反常速度又正比于电场，所以横向电流正比于电场的平方。"),
        ("bcd3", "这就是贝里曲率偶极子的图像。它成功解释了在双层二碲化钨等材料中观测到的二阶霍尔信号。"),
        ("bcd4", "然而，在外尔近藤半金属中，实验观测到了巨大的霍尔响应，而且明显偏离了偶极子图像预言的平方律。"),
        ("bcd5", "问题在于，偶极子图像本质上是微扰论，它假设平移非常小。当电场强到把费米海推到贝里曲率集中的热点附近，或者让电子在两条能带之间跃迁时，微扰展开就失效了。我们需要一个非微扰的理论。"),
    ],
    "S04_Model": [
        ("mod1", "作者用一个最简单的两能带晶格模型来研究这个问题。"),
        ("mod2", "三个泡利矩阵作用在轨道空间上。取 D x 等于零点五，D y 等于一，两条能带在两个点上相交，形成两个类似外尔锥的节点。"),
        ("mod3", "贝里曲率高度集中在这两个节点附近，而且两个节点的符号相反。我们把这些区域叫做贝里曲率热点。"),
        ("mod4", "这个模型保持时间反演对称，却破坏了空间反演对称。所以，它没有线性霍尔效应，但可以有非线性霍尔效应。"),
        ("mod5", "当化学势取零点三时，费米面是围绕两个节点的两个小口袋。"),
    ],
    "S05_Method": [
        ("met1", "那么，如何在不做微扰展开的前提下，描述一个被恒定电场驱动的晶格呢？"),
        ("met2", "第一个困难是：直流电场会不断地加速电子。在晶格里，电子的动量一次又一次地扫过布里渊区。如果没有耗散，电场做的功无处释放，系统也就到达不了一个稳态。"),
        ("met3", "所以作者把每个格点都耦合到一个费米子热库上。热库以速率伽马交换粒子和能量。电场的注入与热库的耗散相互平衡，系统就进入了一个非平衡稳态。"),
        ("met4", "在这个稳态里，电子的动量以速率 E 沿电场方向漂移，平均寿命大约是一除以伽马。所以，占据分布大约会平移 E 除以伽马。"),
        ("met5", "为了精确地处理这一切，作者使用非平衡格林函数。电场通过维格纳表象中的莫亚尔星积进入理论，自然的动量变量是规范协变动量卡帕。整个过程不需要按电场的幂次展开。"),
        ("met6", "得到稳态的密度矩阵之后，霍尔电流就是速度算符与密度矩阵乘积的迹，在布里渊区上积分。"),
        ("met7", "和半经典的玻尔兹曼方程相比，这个方法保留了能带之间的量子相干，不依赖准粒子近似，并且可以通过自能，把相互作用和电声耦合都包含进来。"),
    ],
    "S06_Results": [
        ("res1", "来看结果。这是横向电流除以电场，随电场强度的变化。不同的曲线对应不同的化学势，阻尼伽马固定为零点一。"),
        ("res2", "在弱场区，曲线近似是直线，也就是说横向电流正比于电场的平方，这正是贝里曲率偶极子的预言。"),
        ("res3", "但是在电场约为零点零三的地方，较大化学势的曲线出现了明显的弯折。"),
        ("res4", "再往上，当电场与阻尼伽马相当时，出现了一个鼓包。到了更强的电场，霍尔信号甚至会随着电场的增大而减小。"),
        ("res5", "曲线上那些细小的振荡，来自上下两条能带相干振幅之间的朗道、齐纳、斯图克尔贝格干涉。"),
    ],
    "S07_Crossover": [
        ("cro1", "弯折是从哪里来的？我们回到动量空间。化学势为零点三时，左边口袋的费米面边缘与节点之间，相距零点三二二二。"),
        ("cro2", "现在打开电场。这是非平衡格林函数算出的稳态占据分布。随着电场增强，整个占据分布向右漂移，漂移量大约是 E 除以伽马。"),
        ("cro3", "当漂移量等于这段距离，费米面的边缘就碰到了贝里曲率热点。从这里开始，偶极子展开不再成立。于是，临界电场大约等于伽马乘以这段距离。"),
        ("cro4", "换不同的伽马来检验：每一条曲线的弯折点，都恰好落在 E 除以伽马等于零点三二二二的位置附近。"),
    ],
    "S08_Interband": [
        ("int1", "如果化学势正好位于节点处，根本没有费米面，横向电流又从哪里来呢？"),
        ("int2", "答案是带间跃迁。电场在锥附近把电子从下能带推到上能带，在同一个动量上留下一个空穴。由于漂移和耗散，这些电子空穴对被沿着电场的方向拖离节点。电场越强，拖得越远。"),
        ("int3", "这时，还能用贝里曲率加权的占据公式来计算霍尔电流吗？作者做了直接的比较。"),
        ("int4", "化学势为零点三、电场较弱时，三种算法吻合得很好。但是一旦带间过程变得重要，贝里曲率公式就明显偏离了完整的计算。"),
        ("int5", "化学势为零时更加明显：刚性平移的平衡分布给出的霍尔电流始终为零，而真实的电流并不为零。"),
        ("int6", "还有一个微妙之处。常数弛豫时间近似给出的临界电场，是热库模型的两倍。热点判据本身是普适的，但具体的临界电场，取决于耗散的机制。"),
    ],
    "S09_Spectral": [
        ("spe1", "这个框架还能给出频率分辨的信息，比如有效分布函数。在平衡态，它就是一个费米台阶。"),
        ("spe2", "电场较弱时，台阶只是变得平滑。电场很强时，分布函数出现了明显的摆动和左右不对称。这标志着微扰区域的彻底失效，系统进入了一个强驱动的非平衡稳态。"),
    ],
    "S10_Interactions": [
        ("ia1", "最后，真实材料里还有电声耦合和电子关联。作者在动力学平均场理论中，加入了声子和哈伯德相互作用。"),
        ("ia2", "霍尔信号随电场变化的整体形状没有改变，说明前面发现的非微扰机制是稳健的。但信号的大小被显著增强了。"),
        ("ia3", "增强主要来自自能的实部，而不是额外的阻尼。自能的实部重整化了能带，并在节点处打开了一个小能隙。"),
        ("ia4", "能隙虽小，却让贝里曲率热点变得更强、更集中。"),
        ("ia5", "事实上，只要把 D y 换成一个有效值，一个无相互作用的模型，就能在百分之几的精度内重现完整的电声计算。"),
    ],
    "S11_Summary": [
        ("sum1", "总结一下。"),
        ("sum2", "第一，贝里曲率偶极子图像，只在掺杂足够大、电场足够弱时才是可控的。"),
        ("sum3", "第二，当被驱动的费米面边缘到达节点附近的贝里曲率热点，或者带间电荷转移变得重要时，它就会失效。这时，贝里曲率加权的占据公式也不再可靠。"),
        ("sum4", "第三，非平衡稳态格林函数方法，可以非微扰地计算完整的霍尔电流，并且自然地包含耗散、相互作用和电声耦合。它们不只是带来阻尼，还会通过能带重整化，改变贝里曲率热点。"),
        ("sum5", "这为强场输运和光谱实验，提供了一个定量的理论工具。感谢观看。"),
    ],
}

SCENES = list(SCRIPT.keys())


# English narration. Same keys and the same number of sentences per beat as SCRIPT, so the
# sentence-level sync points in the scenes line up. [word](/phonemes/) overrides TTS pronunciation
# (stripped for subtitles).
SCRIPT_EN = {
    "S01_Hook": [
        ("hook1", "Push electrons along one direction, and the current bends, flowing off to the side. And there is no magnetic field anywhere."),
        ("hook2", "This is the nonlinear Hall effect. At weak fields it is a second-order effect: the transverse current grows as the square of the electric field."),
        ("hook3", "But what happens when the field is strong? The paper we look at today studies exactly this: the nonlinear Hall effect in nonequilibrium steady states driven by strong fields."),
    ],
    "S02_Berry": [
        ("hall1", "First, recall the ordinary Hall effect. An electron moving through a magnetic field feels the Lorentz force, gets deflected sideways, and a transverse current appears."),
        ("hall2", "But in some materials, a transverse current appears even without a magnetic field. The reason is hidden in momentum space: the wavefunctions of Bloch electrons carry a geometric property called the Berry curvature. It acts like an effective magnetic field in momentum space."),
        ("hall3", "In an electric field, an electron picks up an anomalous velocity. It points perpendicular to the field, with a size proportional to the Berry curvature."),
        ("hall4", "Add up the anomalous velocities of all the occupied states, and you get the Hall current."),
        ("hall5", "But if the material has time-reversal symmetry, the Berry curvature at k and at minus k is equal in size and opposite in sign. Positive and negative cancel, the integral vanishes, and the linear Hall effect is gone."),
    ],
    "S03_Dipole": [
        ("bcd1", "The way out appears at second order. The electric field pushes the whole Fermi sea, shifting it through momentum space."),
        ("bcd2", "After the shift, the positive and negative Berry curvature covered by the Fermi sea no longer balance, so a net anomalous velocity appears. The shift is proportional to the field, and the anomalous velocity is proportional to the field again, so the transverse current scales as the field squared."),
        ("bcd3", "This is the Berry curvature dipole picture. It successfully explains the second-order Hall signals seen in materials such as bilayer tungsten ditelluride."),
        ("bcd4", "However, in a [Weyl](/vˈIl/) Kondo semimetal, experiments found a giant Hall response that clearly departs from the square law predicted by the dipole picture."),
        ("bcd5", "The issue is that the dipole picture is fundamentally perturbative: it assumes the shift is tiny. Once the field is strong enough to push the Fermi sea toward the hot spots where the Berry curvature is concentrated, or to drive electrons between the two bands, the perturbative expansion breaks down. We need a nonperturbative theory."),
    ],
    "S04_Model": [
        ("mod1", "The authors study this with the simplest possible two-band lattice model."),
        ("mod2", "The three Pauli matrices act on an orbital degree of freedom. With D x equal to one half and D y equal to one, the two bands touch at two points, forming two [Weyl](/vˈIl/)-like nodes."),
        ("mod3", "The Berry curvature is strongly concentrated near these two nodes, with opposite signs at the two of them. We call these regions Berry curvature hot spots."),
        ("mod4", "The model keeps time-reversal symmetry but breaks inversion symmetry. So it has no linear Hall effect, but it can have a nonlinear one."),
        ("mod5", "At a chemical potential of zero point three, the Fermi surface consists of two small pockets around the nodes."),
    ],
    "S05_Method": [
        ("met1", "So how do we describe a lattice driven by a constant electric field, without expanding in the field?"),
        ("met2", "Here is the first difficulty: a DC field keeps accelerating the electrons. On a lattice, their momentum sweeps through the Brillouin zone again and again. Without dissipation, the work done by the field has nowhere to go, and the system never settles into a steady state."),
        ("met3", "So the authors couple every lattice site to a fermionic reservoir. The reservoir exchanges particles and energy at a rate Gamma. Energy pumped in by the field balances energy drained by the reservoirs, and the system reaches a nonequilibrium steady state."),
        ("met4", "In this steady state, the electron momentum drifts along the field at rate E, and survives for a time of roughly one over Gamma. So the occupation ends up shifted by roughly E over Gamma."),
        ("met5", "To handle all of this exactly, the authors use nonequilibrium Green's functions. The field enters through the [Moyal](/mˈYəl/) star product in the Wigner representation, and the natural momentum variable is the gauge-covariant momentum, kappa. Nowhere does the calculation expand in powers of the field."),
        ("met6", "Once you have the steady-state density matrix, the Hall current is the trace of the velocity operator times the density matrix, integrated over the Brillouin zone."),
        ("met7", "Compared with the semiclassical Boltzmann equation, this approach keeps the quantum coherence between bands, does not rely on a quasiparticle picture, and can include interactions and electron-phonon coupling through self-energies."),
    ],
    "S06_Results": [
        ("res1", "Let's look at the results. This is the transverse current divided by the field, as a function of field strength. Each curve is a different chemical potential, with the damping Gamma fixed at zero point one."),
        ("res2", "At weak fields the curves are nearly straight lines, meaning the transverse current goes as the field squared, exactly as the Berry curvature dipole predicts."),
        ("res3", "But near a field of about zero point zero three, the curves for larger chemical potentials bend noticeably."),
        ("res4", "Further up, when the field becomes comparable to the damping Gamma, a bump appears. At even stronger fields, the Hall signal can actually decrease as the field grows."),
        ("res5", "The small wiggles on the curves come from Landau, Zener, [Stueckelberg](/stˈʊkəlbɜɹɡ/) interference between the coherent amplitudes of the upper and lower bands."),
    ],
    "S07_Crossover": [
        ("cro1", "Where does the bend come from? Let's go back to momentum space. At a chemical potential of zero point three, the edge of the left pocket sits a distance of zero point three two two two from its node."),
        ("cro2", "Now turn on the field. This is the steady-state occupation, computed with nonequilibrium Green's functions. As the field grows, the whole occupation drifts to the right, by roughly E over Gamma."),
        ("cro3", "When the drift equals that distance, the edge of the Fermi surface runs into the Berry curvature hot spot. From here on, the dipole expansion no longer holds. So the critical field is roughly Gamma times this distance."),
        ("cro4", "Check this with different values of Gamma: for every curve, the bend lands right near the point where E over Gamma equals zero point three two two two."),
    ],
    "S08_Interband": [
        ("int1", "But if the chemical potential sits exactly at the nodes, there is no Fermi surface at all, so where does the transverse current come from?"),
        ("int2", "The answer is interband transitions. Near the cones, the field pushes electrons from the lower band into the upper band, leaving a hole behind at the same momentum. Drift and dissipation drag these electron-hole pairs away from the nodes, along the field. The stronger the field, the farther they are dragged."),
        ("int3", "In this regime, can we still compute the Hall current from the Berry-curvature-weighted occupation formula? The authors compared the two directly."),
        ("int4", "At a chemical potential of zero point three and weak fields, all three methods agree well. But once interband processes matter, the Berry curvature formula departs clearly from the full calculation."),
        ("int5", "At zero chemical potential it is even starker: a rigidly shifted equilibrium distribution gives exactly zero Hall current, while the true current is not zero."),
        ("int6", "There is one more subtlety. The constant relaxation time approximation predicts a critical field twice as large as the reservoir model. The hot-spot criterion itself is universal, but the actual critical field depends on how the system dissipates."),
    ],
    "S09_Spectral": [
        ("spe1", "The framework also gives frequency-resolved information, such as the effective distribution function. In equilibrium, it is simply a Fermi step."),
        ("spe2", "At weak fields, the step just gets smoother. At strong fields, the distribution develops clear wiggles and a left-right asymmetry. This marks the complete breakdown of the perturbative regime, as the system enters a strongly driven nonequilibrium steady state."),
    ],
    "S10_Interactions": [
        ("ia1", "Finally, real materials also have electron-phonon coupling and electron correlations. Within dynamical mean-field theory, the authors add phonons and a Hubbard interaction."),
        ("ia2", "The overall shape of the Hall signal versus field does not change, so the nonperturbative mechanisms found earlier are robust. But the size of the signal is substantially enhanced."),
        ("ia3", "The enhancement comes mainly from the real part of the self-energy, not from extra damping. The real part renormalizes the bands, and opens a small gap at the nodes."),
        ("ia4", "The gap is small, yet it makes the Berry curvature hot spots stronger and more concentrated."),
        ("ia5", "In fact, simply replacing D y with an effective value lets a noninteracting model reproduce the full electron-phonon result to within a few percent."),
    ],
    "S11_Summary": [
        ("sum1", "To sum up."),
        ("sum2", "First, the Berry curvature dipole picture is only controlled at large enough doping and weak enough fields."),
        ("sum3", "Second, it breaks down when the driven Fermi-surface edge reaches the Berry curvature hot spots near the nodes, or when interband charge transfer becomes important. In those regimes, the Berry-curvature-weighted occupation formula is no longer reliable either."),
        ("sum4", "Third, the nonequilibrium steady-state Green's function method computes the full Hall current nonperturbatively, and naturally includes dissipation, interactions, and electron-phonon coupling. These do more than add damping, because through band renormalization they reshape the Berry curvature hot spots."),
        ("sum5", "This gives a quantitative theoretical tool for strong-field transport and spectroscopy experiments. Thanks for watching."),
    ],
}
