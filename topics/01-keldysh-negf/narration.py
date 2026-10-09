"""Narration for the Keldysh NEGF explainer (after A.-P. Jauho's lecture notes).

SCRIPT (Mandarin) and SCRIPT_EN (English) have the same keys and the same number of
sentences per beat, so sentence-level sync points in the scenes work for both.
[word](/phonemes/) overrides English TTS pronunciation (stripped for subtitles).
"""

SCRIPT = {
    "S01_Intro": [
        ("in1", "一个量子点夹在两个电极之间。在电极上加一个偏压，电子就会一个接一个地隧穿过去，形成电流。"),
        ("in2", "偏压一大，系统就远离了平衡，平衡态的格林函数不再够用。我们需要另一套工具：凯尔迪什非平衡格林函数。"),
        ("in3", "这个视频跟随一份经典的讲义，从平衡态微扰论出发，一步步走到回路格林函数、朗格雷斯规则和凯尔迪什方程，最后算出共振隧穿的电流。"),
    ],
    "S02_Equilibrium": [
        ("eq1", "先回顾平衡态。零温单粒子格林函数，是精确基态中两个场算符的时间排序关联函数。"),
        ("eq2", "麻烦在于，它需要精确的基态，而这恰恰是我们求不出来的。"),
        ("eq3", "办法是在相互作用绘景中引入 S 矩阵，它满足群性质。然后从无穷远的过去，缓慢地打开相互作用。根据盖尔曼–洛定理，无相互作用的基态会绝热地演化成真正的基态。"),
        ("eq4", "关键的一步在后面。在平衡态中，如果在无穷远的将来再把相互作用缓慢关掉，系统会回到原来的基态，最多差一个相位。于是左矢也可以用 S 矩阵，从无穷远的将来得到。"),
        ("eq5", "这样，格林函数就变成了无相互作用基态上的期望值。把 S 矩阵展开，用威克定理做两两收缩，就得到费曼图，而不连通的图被分母精确抵消。"),
    ],
    "S03_Contour": [
        ("co1", "可是在非平衡情况下，这个关键的假设失效了。系统在无穷远的将来，并不一定回到初始状态。"),
        ("co2", "比如一个原子撞向表面，和表面交换了电荷，离开时的状态和到来时完全不同。"),
        ("co3", "出路是：干脆不去碰无穷远的将来。我们从已知的初始状态出发，沿时间向前演化到关心的时刻，然后再沿时间倒退回去。"),
        ("co4", "这样，所有期望值都相对于一个明确的初始态来定义。代价是，两条时间分支必须被同等对待。这就是凯尔迪什回路。"),
        ("co5", "初始时刻系统处于热平衡，而热平衡的密度矩阵本身可以写成沿虚时间的演化，所以完整的回路还挂着一段虚时间。如果把初始时刻推到无穷远的过去，并且绝热地打开相互作用，这一段就可以去掉。代价是丢掉了初始关联，对稳态问题这通常没有关系。"),
    ],
    "S04_Components": [
        ("cm1", "在回路上，我们用回路排序算符代替时间排序，定义回路格林函数。"),
        ("cm2", "神奇的是，微扰论的拓扑结构和平衡态完全一样。回路格林函数满足形式相同的戴森方程，只是所有的时间积分都沿着回路进行。"),
        ("cm3", "两个时间宗量可以分别落在前向或后向分支上，所以回路格林函数包含四个实时间函数：时间排序、反时间排序、大于和小于格林函数。"),
        ("cm4", "它们满足一个恒等式，所以只有三个是线性独立的。最方便的选择是小于、大于格林函数，再加上推迟和超前格林函数。"),
        ("cm5", "推迟减去超前，等于大于减去小于。直观地说，小于格林函数描述被占据的态，大于格林函数描述空态，而推迟与超前之差给出谱函数，也就是态密度。"),
    ],
    "S05_Langreth": [
        ("la1", "但戴森方程写在回路上，而我们最终要的是实时间的量。这一步的关键工具是朗格雷斯定理。"),
        ("la2", "考虑回路上两个函数的卷积。设第一个时间在前向分支，第二个时间在后向分支，我们要的就是它的小于分量。"),
        ("la3", "把积分回路变形成两段：一段绕过第一个时间，另一段绕过第二个时间。"),
        ("la4", "在第一段上，积分变量在回路意义下总是早于第二个时间，所以 B 变成小于分量，而 A 的两部分合起来恰好是推迟函数。第二段同理，给出超前函数。"),
        ("la5", "结果非常整齐：C 小于，等于 A 推迟乘 B 小于，加上 A 小于乘 B 超前。三个函数相乘也一样：小于标记在乘积中滑动，它左边全是推迟，右边全是超前。推迟分量更简单，就是推迟函数的乘积。"),
        ("la6", "这些规则可以整理成一张表。作为演示，用它推导电子–声子自能的推迟分量，只需要几行。"),
    ],
    "S06_Keldysh": [
        ("ke1", "现在把朗格雷斯规则用到回路上的戴森方程，就得到小于格林函数满足的方程。"),
        ("ke2", "反复迭代下去，得到凯尔迪什方程：第一项依赖于初始状态，第二项是推迟格林函数、小于自能和超前格林函数的乘积。"),
        ("ke3", "对于稳态，如果系统在无穷远的过去处于无相互作用的状态，第一项就消失了，只剩第二项。注意它仍然是一个积分方程，因为小于自能通常依赖于小于格林函数本身。"),
    ],
    "S07_Model": [
        ("mo1", "现在来看应用：介观隧穿结构。左右两个电极之间，夹着一个中心区域。"),
        ("mo2", "在遥远的过去，三部分互不耦合，各自处于热平衡，有各自的化学势。两个化学势可以相差很大，并不要求接近平衡。"),
        ("mo3", "然后打开它们之间的隧穿耦合，在双分支回路上用微扰论处理。耦合不一定很弱，通常要求和到所有阶。"),
        ("mo4", "哈密顿量分成三部分：电极、隧穿和中心区域。电极是无相互作用的电子气。中心区域可以是简单的能级，也可以包含电声耦合，或者安德森型的库仑排斥。"),
    ],
    "S08_Current": [
        ("cu1", "电流由左电极中电子数的变化率给出。算出对易子之后，它可以写成电极与中心区域之间混合格林函数的小于分量。"),
        ("cu2", "由于非平衡理论和平衡理论结构等价，只需写出零温的运动方程，再用朗格雷斯规则延拓到回路，就能把电极的自由度积掉，让电流只依赖中心区域的格林函数和能级宽度函数伽马。"),
        ("cu3", "如果左右两侧的耦合成比例，电流公式就化成一个非常简洁的形式：两侧费米函数之差，乘以一个有效透射函数，再对能量积分。"),
        ("cu4", "只有在偏压窗口里，也就是两个费米函数不同的地方，才有电流流过。而透射函数由推迟与超前格林函数之差决定，本质上就是态密度。"),
        ("cu5", "这个公式对相互作用系统也成立。但它到底有多有用，取决于我们能否算出中心区域的格林函数。"),
    ],
    "S09_Resonant": [
        ("re1", "最简单的例子是无相互作用的单能级。推迟自能的虚部是能级宽度的一半，于是谱函数是一个洛伦兹峰。"),
        ("re2", "耦合越强，峰越宽：电子在点上停留的时间越短，它的能量就越不确定。"),
        ("re3", "小于自能是左右两侧费米函数按耦合强度的加权。于是点上的占据，就像处在一个由两个费米函数混合而成的伪平衡分布里。"),
        ("re4", "电流等于透射系数乘以两侧费米函数之差，再对能量积分。这里的透射系数正是布赖特–维格纳形式的洛伦兹峰。"),
        ("re5", "现在逐渐增大偏压。当能级进入偏压窗口，电流迅速上升，然后饱和成一个平台。台阶的宽度由温度和能级宽度共同决定。"),
    ],
    "S10_Master": [
        ("ma1", "同一个问题，也可以用主方程来处理。点只有两种状态：空着，或者被一个电子占据。"),
        ("ma2", "电子以一定的速率从电极跳进来，又以一定的速率跳出去。速率由费米黄金规则给出，正比于电极里有电子或者有空位的概率。"),
        ("ma3", "在稳态，占据概率等于左右费米函数的加权平均，电流也有一个简单的形式。"),
        ("ma4", "在弱耦合极限下，洛伦兹峰缩成一个德尔塔函数，格林函数的结果和主方程完全一致。但当能级宽度和温度可比时，主方程就不再准确，而格林函数的结果依然精确。"),
        ("ma5", "讲义最后还勾勒了一条从运动方程出发、在宽带极限下推出主方程的路线，并提醒读者留意其中几处可疑的近似。"),
    ],
    "S11_Summary": [
        ("su1", "总结一下。"),
        ("su2", "非平衡时，系统不会回到初始状态，所以我们沿凯尔迪什回路先向前、再向后演化。"),
        ("su3", "回路格林函数满足和平衡态结构相同的戴森方程，而朗格雷斯规则把它翻译成实时间的推迟、超前和小于分量。"),
        ("su4", "凯尔迪什方程给出小于格林函数，由此得到穿过相互作用区域的电流公式。对于共振能级，它给出布赖特–维格纳透射，并在弱耦合下回到主方程。"),
        ("su5", "掌握了这几步，就掌握了非平衡格林函数方法的骨架。感谢观看。"),
    ],
}

SCRIPT_EN = {
    "S01_Intro": [
        ("in1", "A quantum dot sits between two electrodes. Apply a bias across them, and electrons tunnel through one after another, carrying a current."),
        ("in2", "At large bias the system is far from equilibrium, and equilibrium Green's functions are no longer enough. We need a different tool: the [Keldysh](/kˈɛldɪʃ/) nonequilibrium Green's function."),
        ("in3", "This video follows a classic set of lecture notes, starting from equilibrium perturbation theory, then building up contour Green's functions, the Langreth rules and the [Keldysh](/kˈɛldɪʃ/) equation, and finally computing the current through a resonant level."),
    ],
    "S02_Equilibrium": [
        ("eq1", "Let's start with equilibrium. The zero-temperature single-particle Green's function is a time-ordered correlation of two field operators in the exact ground state."),
        ("eq2", "The trouble is that it requires the exact ground state, which is precisely what we cannot compute."),
        ("eq3", "The fix is to work in the interaction picture with an S-matrix, which obeys a group property. Then we switch the interaction on slowly, starting in the infinite past. By the Gell-Mann and Low theorem, the noninteracting ground state evolves adiabatically into the true ground state."),
        ("eq4", "The crucial step comes next. In equilibrium, if we slowly switch the interaction off again in the infinite future, the system returns to its original ground state, up to a phase. So the bra can also be obtained with the S-matrix, coming back from the infinite future."),
        ("eq5", "Now the Green's function is an expectation value in the noninteracting ground state. Expand the S-matrix, contract the operators pairwise with Wick's theorem, and you get Feynman diagrams, with the disconnected ones cancelled exactly by the denominator."),
    ],
    "S03_Contour": [
        ("co1", "Out of equilibrium, though, this crucial assumption fails. Nothing forces the system back to where it started, not even in the infinite future."),
        ("co2", "Think of an atom hitting a surface and exchanging charge with it: the state it leaves in is completely different from the state it arrived in."),
        ("co3", "The way out is to never refer to the infinite future at all. Start from the known initial state, evolve forward in time to the moment we care about, and then evolve back again."),
        ("co4", "Every expectation value is then defined with respect to a well-defined initial state. The price is that the two time branches must be treated on an equal footing. This is the [Keldysh](/kˈɛldɪʃ/) contour."),
        ("co4b", "This closed loop also buys us something for free. Going forward and then back again is the identity, so the evolution around the whole contour multiplies to one. The awkward denominator of the equilibrium theory, and with it all the vacuum bubbles, simply disappears."),
        ("co5", "At the initial time the system is in thermal equilibrium, and the thermal density matrix itself is an evolution in imaginary time, so the full contour also carries an imaginary-time leg. If we push the initial time to the infinite past and switch the interactions on adiabatically, this leg can be dropped. The price is losing initial correlations, which usually does not matter for steady states."),
    ],
    "S04_Components": [
        ("cm1", "On the contour, we replace time ordering by contour ordering, and define the contour-ordered Green's function."),
        ("cm2", "Remarkably, the topological structure of perturbation theory is exactly the same as in equilibrium. The contour Green's function obeys a Dyson equation of the same form, except that every time integral now runs along the contour."),
        ("cm3", "Each of the two time arguments can sit on either the forward or the backward branch, so the contour function contains four real-time functions: the time-ordered, the anti-time-ordered, the greater and the lesser Green's functions."),
        ("cm4", "They obey one identity, so only three are linearly independent. The most convenient choice is the lesser and greater functions, together with the retarded and advanced ones."),
        ("cm5", "Retarded minus advanced equals greater minus lesser. Intuitively, the lesser function describes occupied states, the greater function describes empty states, and the difference between retarded and advanced gives the spectral function, the density of states."),
        ("cm6", "Here is the deeper reason we need this extra function. The retarded function tells us which states exist and how long they live: the spectrum. The lesser function tells us how full those states are: the occupation."),
        ("cm7", "In equilibrium, the two are locked together by the fluctuation-dissipation theorem: the lesser function is just the Fermi function times the spectrum. Out of equilibrium that lock breaks. The same spectrum can be filled in a completely different way, set by kinetics instead of temperature, and that is exactly the information the lesser function carries."),
    ],
    "S05_Langreth": [
        ("la1", "But the Dyson equation lives on the contour, while in the end we want real-time quantities. The key tool for this step is the Langreth theorem."),
        ("la2", "Take a convolution of two functions on the contour. Put the first time on the forward branch and the second time on the backward branch, so what we want is its lesser component."),
        ("la3", "Now deform the integration contour into two pieces: one looping around the first time, and one looping around the second."),
        ("la4", "On the first piece, the integration variable always comes earlier on the contour than the second time, so B becomes a lesser function, while the two parts of A combine into exactly the retarded function. The second piece gives an advanced function in the same way."),
        ("la5", "The result is beautifully tidy: C lesser equals A retarded times B lesser, plus A lesser times B advanced. Products of three functions work the same way: the lesser label slides along the chain, with retarded functions to its left and advanced functions to its right. The retarded component is even simpler, just the product of the retarded functions."),
        ("la5b", "There is a simple picture behind this rule. Think of the product as a path that starts on the forward branch, the history of the ket, and ends on the backward branch, the history of the bra. It has to switch branches exactly once: links before the switch are retarded, the link that switches is lesser, and links after it are advanced. Summing over where the switch happens gives the three terms."),
        ("la6", "These rules fit into a single table. As a demonstration, deriving the retarded electron-phonon self-energy with them takes just a few lines."),
    ],
    "S06_Keldysh": [
        ("ke1", "Now apply the Langreth rules to the Dyson equation on the contour, and we get an equation for the lesser Green's function."),
        ("ke2", "Iterating it to all orders gives the [Keldysh](/kˈɛldɪʃ/) equation: a first term that depends on the initial state, and a second term that is the retarded Green's function times the lesser self-energy times the advanced Green's function."),
        ("ke3", "For a steady state, if the system was noninteracting in the infinite past, the first term vanishes and only the second survives. Note that this is still an integral equation, because the lesser self-energy usually depends on the lesser Green's function itself."),
        ("ke4", "This equation has a transparent meaning. The lesser self-energy is the rate at which the leads inject electrons at each energy. The retarded and advanced functions then carry each injected electron along until it leaks away again, so the occupation is simply the injection rate times the time an electron dwells on the dot."),
        ("ke5", "And the first term, the memory of the initial state, fades away. Start the dot with any occupation you like: it relaxes, on the time scale h-bar over Gamma, to the steady value fixed by the leads. After a few lifetimes the initial state is forgotten, which is why only the second term survives."),
    ],
    "S07_Model": [
        ("mo1", "Now for the application: mesoscopic tunneling structures. A central region sits between a left and a right electrode."),
        ("mo2", "In the remote past, the three parts are decoupled, each in thermal equilibrium with its own chemical potential. The two chemical potentials can differ by a lot, with no need to be close to equilibrium."),
        ("mo3", "Then the tunneling couplings between them are switched on, and handled by perturbation theory on the two-branch contour. The couplings need not be weak, and typically must be summed to all orders."),
        ("mo4", "The Hamiltonian splits into three parts: the contacts, the tunneling, and the central region. The contacts are noninteracting electron gases. The central region can be a set of simple levels, or include electron-phonon coupling, or an Anderson-type Coulomb repulsion."),
    ],
    "S08_Current": [
        ("cu1", "The current is the rate of change of the electron number in the left electrode. After working out the commutator, it can be written as the lesser component of a mixed Green's function between the electrode and the central region."),
        ("cu2", "Because the nonequilibrium theory is structurally equivalent to the equilibrium one, we only need the zero-temperature equation of motion, continued onto the contour with the Langreth rules, to integrate out the electrodes and leave a current that depends only on the central-region Green's functions and the level-width functions, Gamma."),
        ("cu2b", "For a single level, this formula reads like a ledger. Electrons flow in from the left at rate Gamma L whenever the lead state is filled and the dot state is empty, and flow back out whenever the dot state is filled and the lead state is empty. Subtract the two, the Pauli blocking factors cancel, and what remains is exactly this expression. These are the same rates that will reappear in the master equation."),
        ("cu3", "If the left and right couplings are proportional to each other, the current formula collapses into a strikingly simple form: the difference of the two Fermi functions, times an effective transmission function, integrated over energy."),
        ("cu4", "Current flows only inside the bias window, where the two Fermi functions differ. And the transmission is set by the difference between the retarded and advanced Green's functions, which is essentially the density of states."),
        ("cu4b", "Picture two streams at every energy: electrons coming from the left with weight f L, and from the right with weight f R, each getting through with probability T. Deep below both chemical potentials the two streams cancel exactly. Only inside the window does a net flow survive."),
        ("cu5", "This formula holds for interacting systems too. But how useful it is depends on whether we can actually compute the central-region Green's functions."),
    ],
    "S09_Resonant": [
        ("re1", "The simplest example is a single noninteracting level. The imaginary part of the retarded self-energy is half the level width, so the spectral function is a Lorentzian peak."),
        ("re2", "The stronger the coupling, the broader the peak: the shorter the electron stays on the dot, the less certain its energy."),
        ("re2b", "Here is why. Put an electron on the dot at time zero: its amplitude oscillates at the level energy while leaking into the leads, so the probability of still finding it decays as e to the minus Gamma t over h-bar. The Fourier transform of that decaying oscillation is exactly a Lorentzian of width Gamma: a short life means a broad line."),
        ("re3", "The lesser self-energy is a weighted mix of the left and right Fermi functions, weighted by the coupling strengths. So the dot is occupied as if it sat in a pseudo-equilibrium distribution, blended from the two Fermi functions."),
        ("re3b", "There is a neat way to see this blend. Each lead keeps resetting the dot: lead alpha does so at rate Gamma alpha, and leaves the state filled with probability f alpha. So the dot simply copies the Fermi function of whichever lead touched it last, and lead alpha was the last one with probability Gamma alpha over Gamma."),
        ("re4", "The current is the transmission times the difference of the Fermi functions, integrated over energy. And here the transmission is exactly a [Breit](/bɹˈIt/)-Wigner Lorentzian."),
        ("re4b", "Two facts hide inside this Lorentzian. At resonance, with symmetric barriers, the transmission reaches one: two barriers that are each nearly opaque become perfectly transparent together, just like a [Fabry](/fɑbɹˈi/)-[Perot](/pəɹˈO/) cavity. And the plateau current scales as Gamma L times Gamma R over their sum, like two resistors in series, so the weaker barrier is the bottleneck."),
        ("re5", "Now slowly raise the bias. As the level enters the bias window, the current rises quickly, then saturates into a plateau. The width of the step is set by both the temperature and the level width."),
    ],
    "S10_Master": [
        ("ma1", "The same problem can also be handled with a master equation. The dot has only two states: empty, or occupied by one electron."),
        ("ma2", "Electrons hop in from the electrodes at some rate, and hop back out at another. The rates come from Fermi's golden rule, proportional to the probability of finding an electron, or a hole, in the electrode."),
        ("ma3", "In the steady state, the occupation probability is a weighted average of the two Fermi functions, and the current takes a simple form too."),
        ("ma4", "In the weak-coupling limit, the Lorentzian shrinks into a delta function, and the Green's function result agrees exactly with the master equation. But once the level width is comparable to the temperature, the master equation is no longer accurate, while the Green's function result remains exact."),
        ("ma4b", "The difference is sharpest when the level sits outside the bias window. The master equation then only allows thermally activated current, which dies off exponentially with the distance to the window. The Green's function keeps the Lorentzian tails of the level, so current still leaks through by quantum tunneling, falling off only as a power law."),
        ("ma5", "The notes close by sketching how the master equation could be derived from the equations of motion in the wide-band limit, and invite the reader to spot a few suspicious approximations along the way."),
    ],
    "S11_Summary": [
        ("su1", "To sum up."),
        ("su2", "Out of equilibrium, the system does not return to its initial state, so we evolve forward and then backward along the [Keldysh](/kˈɛldɪʃ/) contour."),
        ("su3", "Contour Green's functions obey a Dyson equation with the same structure as in equilibrium, and the Langreth rules translate it into retarded, advanced and lesser real-time components."),
        ("su4", "The [Keldysh](/kˈɛldɪʃ/) equation gives the lesser Green's function, and from it the current through an interacting region. For a resonant level it yields [Breit](/bɹˈIt/)-Wigner transmission, and reduces to the master equation at weak coupling."),
        ("su4b", "Behind every formula sits one physical picture: the leads inject electrons, the electrons propagate with a finite lifetime, and the occupation that results is set by kinetics, not by temperature alone."),
        ("su5", "Master these few steps, and you have the skeleton of the nonequilibrium Green's function method. Thanks for watching."),
    ],
}

SCENES = list(SCRIPT.keys())
