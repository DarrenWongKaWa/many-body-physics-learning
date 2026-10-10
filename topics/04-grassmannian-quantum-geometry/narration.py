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
        ("map2", "On the right is the space of states. For two bands, a state up to its overall phase is a point on the Bloch sphere."),
        ("map3", f"As the momentum moves, the state moves. We use one model throughout, the {QWZ} model with mass one, the same band as in our earlier video. Its Chern number is one."),
        ("map4", "Now paint the whole grid onto the sphere, cell by cell. Most of the zone lands one way up, and we color those cells blue. But around the point M, where both momenta equal pi, the sheet lands flipped over, and those cells are red."),
        ("map5", "Where blue meets red, the map folds. Keep this picture in mind. We will come back to it again and again, adding one layer at a time."),
    ],
    "S03_Distance": [
        ("dis1", f"The first paper, by {HUANG} and [Giataganas](/jˌɑtəɡˈɑnəs/), starts with a simple question: how far apart are two states?"),
        ("dis2", "A state does not care about its overall phase, so compare projectors instead. For one band, two states make an angle theta, whose cosine is the size of their overlap."),
        ("dis3", f"On this Bloch sphere of radius one half, the angle has a picture. The straight chord between the two points has length sine theta, the Hilbert Schmidt distance between the projectors. The arc along the sphere has length theta, the {FS} distance. For nearby states the two agree."),
        ("dis4", "With several occupied bands, the occupied states form a plane rather than a line. Two planes are separated by a set of angles, the principal angles, one for each pair of matching directions."),
        ("dis5", "They come from the singular values of the overlap matrix, so they do not change when you rotate the basis inside either plane. The Hilbert Schmidt distance is the square root of the sum of their squared sines."),
    ],
    "S04_MDS": [
        ("mds1", "Now suppose all you are given is a table: the distance between every pair of sampled momenta. Can you rebuild the shape of the states from the table alone?"),
        ("mds2", "Because the Hilbert Schmidt distance is a straight-line distance between matrices, the answer is yes. Multidimensional scaling looks for points in ordinary space whose distances match the table."),
        ("mds3", "Watch it work. Start from a random cloud, and let every pair of points pull or push like a spring, until its length matches the table. Each frame here is one real step of the algorithm."),
        ("mds4", "For the Chern band, the cloud closes into a complete sphere, with an empty cavity inside."),
        ("mds5", "For a trivial band, with mass three point two, it builds only a small cap around the north pole. The cap is fully covered, with no hole in it, but it never closes. Whether the shape closes up is a sign of the topology."),
        ("mds6", "But distances alone cannot tell you how often each piece is covered, or which way up. For that, we need to zoom in."),
    ],
    "S05_Zoom": [
        ("zoo1", "Zoom in on one momentum. A tiny circle of momenta around it lands on the sphere as a tiny ellipse."),
        ("zoo2", "That ellipse is the quantum metric. It says how far the state moves for each direction of step in momentum. The long axis points where the state changes fastest."),
        ("zoo3", f"In the second paper, {HUANG} builds everything from the derivative of the projector. The metric is one half the trace of d P times d P, and no phase is ever chosen."),
        ("zoo4", "Now take a tiny square of momenta instead. It lands as a tiny parallelogram. Its area is the quantum area, and it has an orientation: it can land face up, or flipped."),
        ("zoo5", "The Berry curvature is exactly this signed area. It is positive where the cell lands face up, negative where it lands flipped, and in our units it is twice the signed area per unit area in momentum."),
        ("zoo6", "Here is a check that this is the right picture. The other band sits at the opposite point of the sphere. Its parallelogram has the same shape, so the same metric, but it is flipped, so the opposite Berry curvature."),
        ("zoo7", "Yet the metric of both bands is that of a sphere of radius one half, with Gaussian curvature four. So the Berry curvature is not the curvature of the metric. Keep the two apart."),
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
        ("fol1", "Back to the fold. Draw the metric ellipse at every momentum, like the little circles that show the distortion of a map projection."),
        ("fol2", "Far from the fold the ellipses are fat. Near the fold they flatten, and on the fold itself they collapse into line segments: one direction of motion no longer moves the state at all."),
        ("fol3", "That is what a fold is. Fold a clear sheet printed with arrows, and the folded part comes down mirrored. Two different momenta land on the same state, with opposite orientations."),
        ("fol4", "In our model the fold is a closed curve around M, where the determinant of the metric vanishes. Inside it, the sheet is flipped."),
        ("fol5", "Now look at the polar cap. It is covered three times: two sheets face up, and one flipped."),
        ("fol6", "So there are two ways to add up area. Count every sheet, and you get the quantum volume: one point one nine spheres."),
        ("fol7", "Count with signs, and the flipped sheet cancels one of the others: exactly one sphere. That signed count is the Chern number. The difference is the extra area tucked into the folds, which is why, in these units, the quantum volume can never be smaller than the Chern number."),
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
        ("mul2", "With a third band, the space of states has four real dimensions instead of two, and a fold has room to escape. Take the simplest fold, where s and t go to s and t squared. Push it gently into a new direction, epsilon times t, and the crease opens into a smooth bend."),
        ("mul3", f"Then what replaces the plus or minus sign? An angle, the {KAHLER} angle. The Berry curvature is twice its cosine times the quantum area density. For two bands the cosine can only be plus or minus one, and it jumps across the fold. For three bands it varies smoothly."),
        ("mul4", "Points where its size reaches one are special: there the tangent plane is a complex line. In our three-band example there are five such complex points, four with index plus one and one with index minus one. Their signed count is three, three times the size of the Chern number, exactly as a topological argument predicts."),
        ("mul5", f"And since this surface no longer folds, the ordinary {GB} theorem applies again. The total Gaussian curvature vanishes, and it no longer carries the Chern number."),
    ],
    "S10_Outro": [
        ("end1", "Let's put the three papers together. The first compares states at a distance, and rebuilds their shape from a table of distances."),
        ("end2", "The second differentiates the projector, giving the metric, the Berry curvature, geodesics and Berry phases. The same toolbox gives Wilson loops, winding numbers and the Z two index."),
        ("end3", "The third integrates curvature carefully, folds and signs included, and gets the Chern number back from geometry."),
        ("end4", "All of it starts from one object, the projector, with no phase to fix, and it all lives in one picture: a torus pressed onto a sphere, folding where it must. Thanks for watching."),
    ],
}
