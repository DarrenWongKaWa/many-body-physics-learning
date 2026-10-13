"""Narration script (English, voice af_bella). One entry per animation beat: (key, text).

Scenes sync to sentence boundaries via self.narrate(key) and Beat.wait_sentence(i).
Sentences are split at . ! ? ; followed by a space, so avoid those inside a sentence.
Pronunciation overrides: [word](/phonemes/) (misaki IPA); stripped from subtitles.

Conventions (guide p. 18): standard metric g = (1/2) tr(dP dP), Bloch sphere of radius 1/2 and
Gaussian curvature 4. The video follows the QWZ band whose Bloch vector is n = d/|d| (Chern number +1 at m = 1).
"""

HUANG = '[Huang](/hwˈɑŋ/)'
QWZ = '[Qi](/ʧˈi/) [Wu](/wˈu/) [Zhang](/ʤˈɑŋ/)'
BZ = '[Brillouin](/bɹilwˈæn/) zone'
GB = '[Gauss](/ɡˈWs/) [Bonnet](/bɔnˈA/)'
FS = '[Fubini](/fubˈini/) [Study](/ʃtˈudi/)'
KAHLER = '[Kähler](/kˈAləɹ/)'
EULER = '[Euler](/ˈYləɹ/)'
BARGMANN = '[Bargmann](/bˈɑɹɡmən/)'

SCRIPT = {
    "S01_ColdOpen": [
        ("open1", "Take a flat sheet of paper. You can roll it into a cylinder without stretching it, and without a single crease."),
        ("open2", "Now bend the cylinder around, and glue its two ends together. You get a torus, the surface of a donut."),
        ("open3", "Here is a harder question. Can you lay a torus-shaped membrane smoothly over a sphere, without any creases? You cannot. Somewhere, the membrane has to fold back on itself."),
        ("open4", "Electrons in a crystal do exactly this. In a two-band crystal, every band presses a torus onto a sphere, and hidden in the folds is a topological number, the Chern number."),
        ("open5", f"This video follows three papers by Shin-Ming {HUANG}, which read all of this from a single object, the projector onto the occupied states, without ever fixing a phase."),
    ],
    "S02_Map": [
        ("map1", f"Here is the stage. On the left is the {BZ}, a square of crystal momenta. Opposite edges describe the same states, so they are glued together, and the square is really a torus."),
        ("map2", "On the right is the space of states. For two bands, a state up to its overall phase is fixed by one unit vector, the expectation value of the Pauli matrices. That vector is a point on the Bloch sphere."),
        ("map3", "So what is the map? A two-band Hamiltonian is a vector d of k, dotted into the Pauli matrices. Its upper band is the state whose Bloch vector points along d. So the map is simply this: k goes to n of k, the vector d divided by its length."),
        ("map3b", f"We use one model throughout, the {QWZ} model. Its vector d is sine k x, sine k y, and m minus cosine k x minus cosine k y. At Gamma, d points straight down, so Gamma lands on the south pole. At X and at M, d points straight up, so both land on the north pole."),
        ("map3c", "The mass m sets the topology. For m between zero and two, the image wraps the whole sphere, and the Chern number is one. That is the band we follow, with m equal to one. For m above two, the z component of d is always positive, every state stays near the north pole, and the Chern number is zero. Our trivial example is m equal to three point two."),
        ("map4", "Now paint the whole grid onto the sphere, cell by cell. Walk around a small cell counterclockwise. Its image is walked either the same way as most of the map, which we call face up and color blue, or the mirror way, which we call flipped and color red. The flipped cells surround the point M, where both momenta equal pi."),
        ("map5", "Where blue meets red, the map folds. Keep this picture in mind. We will come back to it again and again, adding one layer at a time."),
    ],
    "S03_Distance": [
        ("dis1", f"The first paper, by {HUANG} and [Giataganas](/jˌɑtəɡˈɑnəs/), starts with a simple question: how far apart are two states?"),
        ("dis2", "A state does not care about its overall phase, so compare projectors instead. Two states define an angle theta: its cosine is the size of their overlap."),
        ("dis3", "On the Bloch sphere, the two Bloch vectors make an angle of two theta at the center. Orthogonal states, with theta equal to ninety degrees, sit at opposite points."),
        ("dis3b", f"Measured with the quantum metric, this sphere has radius one half. So the arc between the two states has length theta: that is the {FS} distance. And the straight chord has length sine theta: that is the Hilbert Schmidt distance between the projectors. For nearby states the two agree."),
        ("dis4", "Now let two bands be occupied. At one momentum, the occupied states span a two-dimensional subspace. Think of it as a plane through the origin. At another momentum, they span another plane."),
        ("dis5", "Two planes are compared by principal angles. Picture the floor and a half-open door. Along the hinge, the planes share a direction, so that angle is zero. Across the hinge, they differ by the opening angle."),
        ("dis5b", "In general, the singular value decomposition of the overlap matrix pairs each direction u in the first plane with a direction v in the second, and the principal angles are the angles between these pairs. They do not depend on the basis chosen in either plane, and the squared Hilbert Schmidt distance is the sum of their squared sines."),
        ("dis5c", "Check it on the floor and the door. Turn the arrows in each plane to any other directions. The angles between your arrows change, but the principal angles stay at zero and fifty degrees, and the distance stays the same. The principal angles belong to the planes, not to the arrows: the first is the smallest angle that any arrow in the floor can make with any arrow in the door, here zero along the hinge, and the second is the opening across it."),
    ],
    "S04_MDS": [
        ("mds1", "Now sample the zone at four hundred and eighty four momenta, and for every pair, write down the distance between their states. Careful: this is not the length of the yellow line in momentum space. It is the chord between the two states on the sphere."),
        ("mds1b", "Here is the whole table as an image, one entry for every pair of momenta. Row i and column j show D i j, the chord between the two states: black means the same state, and white means orthogonal states. The diagonal is black, and the stripes come from the order in which the momenta are numbered."),
        ("mds2", "Can you rebuild the shape of the states from this table alone, without the momenta and without the states? Because the Hilbert Schmidt distance is a straight-line distance between matrices, the answer is yes. Multidimensional scaling looks for points in ordinary space whose distances match the table."),
        ("mds3", "Watch it work. Start from a random cloud, and let every pair of points pull or push like a spring, until its length matches the table. Each frame here is one real step of the algorithm."),
        ("mds4", "For the Chern band, the points settle onto a complete sphere of radius one half, with an empty cavity inside. It is the Bloch sphere, rebuilt from distances alone, up to a rotation."),
        ("mds5", "For the trivial band, with m equal to three point two, the z component of d is always positive, so every state stays within thirty degrees of the north pole. Its table is much darker: no two states are more than about half a unit apart. The only shape with these distances is a small cap, and that is what comes back. The cap is fully covered, but it never closes. A closed surface or an open patch: that is a first glimpse of the topology."),
        ("mds6", "But the table has two blind spots. A shape and its mirror image have exactly the same distances, so the table cannot tell face up from flipped. And three layers lying on top of each other look like one."),
        ("mds6b", "The Chern number counts how many times the sphere is covered, with signs, so we need the orientation. Orientation is local: we have to zoom in on the derivative of the map."),
    ],
    "S05_Zoom": [
        ("zoo1", "Zoom in on one momentum. A tiny circle of momenta around it lands on the sphere as a tiny ellipse."),
        ("zoo2", "That ellipse is the quantum metric. A small step delta k moves the state by a distance d s, with d s squared equal to g i j delta k i delta k j, where g is one quarter of the derivatives of n dotted together."),
        ("zoo2b", "The eigenvectors of g give the axes of the ellipse, and the square roots of its eigenvalues give their lengths. The long axis points where the state changes fastest."),
        ("zoo3", f"In the second paper, {HUANG} builds everything from the derivative of the projector. The metric is one half the trace of d P times d P, and no phase is ever chosen."),
        ("zoo4", "Now take a tiny square of momenta instead. It lands as a tiny parallelogram, whose area is the square root of det g, times delta k x delta k y. Here det g, the product of the two eigenvalues, says how much the map magnifies area."),
        ("zoo5", "Walk around the square counterclockwise. Its image is walked either the same way as most of the map, face up, or the mirror way, flipped. The Berry curvature is this signed area, times a fixed factor of two: plus where the cell lands face up, minus where it lands flipped. The two only converts units: a Berry phase is half a solid angle, and on a sphere of radius one half, the solid angle is four times the area."),
        ("zoo6", "Here is a check of this picture. The other band has the opposite Bloch vector, so it sits at the opposite point of the sphere. Its parallelogram has the same shape, so the same metric, but it is walked the mirror way, so it has the opposite Berry curvature. That is exactly the known result for two bands."),
        ("zoo7", "One warning. Both bands live on the same sphere of radius one half, whose Gaussian curvature is four everywhere: that is the shape of the surface. The Berry curvature is something else: it says how the zone is laid onto the sphere, how much area each cell covers, and which way up."),
    ],
    "S06_Transport": [
        ("tra1", "The derivative of the projector also tells you how to travel between states along the straightest path. Exponentiate it, and you get a geodesic. On the Bloch sphere, geodesics are great circles."),
        ("tra2", "Now carry an arrow around a triangle made of three geodesics, keeping it as parallel as the curved surface allows. When it comes home, it has turned."),
        ("tra3", "The turning angle is the curvature, four, times the enclosed area, which is just the solid angle of the triangle."),
        ("tra4", f"The quantum states remember the loop too. Multiply the overlaps around the triangle, one to two, two to three, three to one. The phase of this product, the {BARGMANN} invariant, gives the Berry phase of the triangle, and it is half of the solid angle."),
        ("tra5", "So the arrow turns by the full solid angle, while the state picks up half of it. They are proportional, but they are not the same thing."),
        ("tra6", "This gives a phase-free way to compute Berry phases. Replace a smooth loop by a polygon of sampled states joined by geodesics. The polygon's phase converges to the Berry phase of the loop as you add more points."),
    ],
    "S07_Fold": [
        ("fol1", "Back to the fold. At every momentum, draw the metric ellipse from before, with its axes along the eigenvectors of g and lengths given by the square roots of the eigenvalues."),
        ("fol2", "Far from the fold the ellipses are fat. Near the fold one eigenvalue shrinks, and on the fold it vanishes: det g is zero, the ellipse collapses to a segment, and one direction of motion no longer changes the state. Remember from the zoom-in: root det g is the area a cell covers, and for two bands the Berry curvature is twice that area, with a sign. On the fold the area is zero, so the Berry curvature vanishes there, and across the fold, where the cells flip, it changes sign."),
        ("fol3", "That is what a fold is. Fold a clear sheet printed with arrows, and the folded part comes down mirrored. Two different momenta land on the same state, with opposite orientations."),
        ("fol4", "In our model the fold is a closed curve around M, where the determinant of the metric vanishes. Inside it, the sheet is flipped."),
        ("fol5", "Now count how often each point of the sphere is covered. Three momenta, X, Y and M, all land on the north pole. Around each of them, a region of the zone covers the area near the north pole once."),
        ("fol5b", "Around X and around Y, the cover lands face up. Around M, inside the fold, it lands flipped. So the region bounded by the image of the fold, a star with four points, is covered three times, with orientation signs plus one, plus one, and minus one. These are orientations, not Chern numbers."),
        ("fol5c", "And the rest of the blue zone, outside the highlighted regions? It is laid down once over everything outside the star, face up. Together with the X sheet, it makes one complete sphere, face up. The Y sheet and the M sheet are an extra pair over the star, one face up and one flipped."),
        ("fol6", "Call each piece of the zone that is laid down once a sheet. Count every sheet: add up the image area of every cell, root det g times delta k x delta k y, always positive. That is the quantum volume, and it comes to one point one nine spheres."),
        ("fol7", "Now count with signs: face-up cells plus, flipped cells minus, which is the integral of the Berry curvature over two. Away from the star every point is covered once. Inside it, plus, plus, minus: again once. So the signed total is exactly one sphere, the Chern number."),
        ("fol7b", "The unsigned total is larger by twice the area of the star. That is why, in these units, the quantum volume can never be smaller than the Chern number."),
    ],
    "S08_GaussBonnet": [
        ("gab1", "The third paper asks a deeper question. What does the curvature of the metric know about topology?"),
        ("gab2", f"For a smooth closed surface, the {GB} theorem says that the total Gaussian curvature is two pi times the {EULER} characteristic. For a sphere that is four pi; for a torus it is zero."),
        ("gab3", "Away from the folds, our metric is a piece of sphere, with constant curvature four. Add it up over all the regular sheets, and you get plus two point three seven eight, times two pi. Not zero."),
        ("gab4", "The missing piece lives on the fold. Treated as a crease, the fold carries a singular curvature, and it contributes minus two point three seven eight, times two pi. The books balance, and the total is zero, as it must be for a torus."),
        ("gab5", "Now keep the signs instead. The flipped sheet subtracts, three sheets become one, and the signed total curvature is four pi times the Chern number."),
        ("gab6", f"These totals do not depend on how the metric is normalized. {HUANG}'s papers use a metric twice as large, with sphere curvature two, and find the same two point three seven eight."),
    ],
    "S09_Multiband": [
        ("mul1", "The third paper ends with an open question. What replaces this picture when there are more than two bands? What follows is our own proposal. It is not yet published, and it is marked as such."),
        ("mul2", "Count dimensions first. A state with N components, normalized and without its phase, needs two N minus two real numbers: two for two bands, the Bloch sphere, and four for three bands. The zone still maps to a two-dimensional surface, but now inside a four-dimensional space."),
        ("mul2b", "A fold needs one direction of motion in k to stop changing the state. With two extra dimensions to move into, a generic surface never has to do that. The simplest fold shows why. Here s and t go to s and t squared, so t and minus t land on the same point."),
        ("mul2c", "A third orbital gives the state a new direction to move in. Add a small component along it, epsilon times t, and the two sides no longer meet: the crease opens into a smooth bend. In our three-band model, det g stays positive everywhere we computed it."),
        ("mul3", f"Without folds there is no sign to flip. What replaces it is an angle. The Berry curvature can never exceed twice root det g, so define cos theta K as the Berry curvature divided by this largest possible value: the {KAHLER} angle. For two bands it is always plus or minus one. For three bands it varies smoothly, and the shading shows it."),
        ("mul4", "Where it reaches plus or minus one, the surface locally looks like a two-band sphere again. These are complex points. Around each one, an associated phase winds once, like a vortex, with index plus one or minus one. Topology fixes the sum of the indices to three times the size of the Chern number. Our example has five complex points, four with plus one and one with minus one, adding up to three."),
        ("mul5", f"And since this surface no longer folds, the ordinary {GB} theorem applies again. The total Gaussian curvature vanishes, and it no longer carries the Chern number."),
    ],
    "S10_Outro": [
        ("end1", "Let's put the three papers together. The first compares states at a distance, and rebuilds their shape from a table of distances."),
        ("end2", "The second differentiates the projector, giving the metric, the Berry curvature, geodesics and Berry phases. The same toolbox gives Wilson loops, winding numbers and the Z two index."),
        ("end3", "The third integrates curvature carefully, folds and signs included, and gets the Chern number back from geometry."),
        ("end4", "All of it starts from one object, the projector, with no phase to fix, and it all lives in one picture: a torus pressed onto a sphere, folding where it must. Thanks for watching."),
    ],
}
