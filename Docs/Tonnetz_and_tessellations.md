# Tonnetze and Tessellations — A Reference

*A working reference for the harmony-tessellation project: what a tonnetz is,
how tonnetze relate to plane tessellations, which tessellations have a genuine
musical basis, and how many there are.*

---

## 1. Two kinds of graph

Music theory uses two different families of diagram to picture voice leading
(Tymoczko, *The Generalized Tonnetz*, 2012):

- **Note-based graphs.** Points are *notes*; a chord is an extended *shape*
  (a triangle, tetrahedron, …). The classical Tonnetz is the prototype: major
  and minor triads are triangles, and a parsimonious voice leading is a "flip"
  across a shared edge.

- **Chord-based graphs.** Each point is an entire *chord*; an edge is a
  single-step voice leading. Douthett & Steinbach's "chicken-wire torus" is
  the prototype.

The two are **geometric duals** of one another. Duality swaps dimension *k* for
dimension *(n−k)*: a face of one graph becomes a vertex of the other, and an
edge becomes an edge. So a note-based triangle-tiling and a chord-based
hexagon-tiling can carry *identical* musical information in dual dress.

This is the first thing to be clear about: **"a tonnetz" is not "a
tessellation."** A tonnetz is fundamentally a *graph*. A tessellation is one
*geometric realization* of that graph. One graph → several tessellations.

---

## 2. The Tonnetz is multivalent

A subtle point from Tymoczko that is easy to get wrong (and which I got
imprecise earlier in this project): the classical Tonnetz is not one structure
but **three structures that happen to coincide** in the three-note,
twelve-tone case:

1. **Acoustic Tonnetz** — edges are consonant intervals (perfect fifth, major
   third). This is Euler's original.
2. **Common-tone Tonnetz** — edges join chords sharing notes.
3. **Voice-leading Tonnetz** — edges are efficient (single-step) voice
   leadings.

They generalize *differently*. The acoustic one extends by adding axes for
more intervals; the common-tone one is Cohn's 1997 generalization; the
voice-leading one is the large family Tymoczko constructs. They look the same
for triads only because of a numerical coincidence. When you generalize, they
split apart. For *this* project — tracing harmonic progressions as orbits —
the **voice-leading** reading is the relevant one.

---

## 3. How a tonnetz becomes a tessellation

Tymoczko's recipe (his Section 3):

1. Start with a **chord-based lattice** — typically a chain or circle of
   *n*-dimensional cubes (hypercubes), each cube recording the ways to lower
   the notes of one chord by a step.
2. Replace every cube with its **dual cross-polytope** (square→square,
   cube→octahedron, tesseract→…). This converts the chord-based graph into a
   **note-based** graph.
3. Glue the cross-polytopes back together as the original cubes were joined.

The result is a note-based tessellation. Because step 2 is duality, the same
underlying graph yields a dual *pair* of tilings — e.g. the Euclidean Tonnetz
appears both as a triangle tiling (Fig 1a of the Boland–Hughston paper) and as
a hexagon tiling (its Fig 2). **Same tonnetz, two tessellations, related by
duality.**

A second, deeper route appears in Boland & Hughston (*Configurations,
Tessellations and Tone Networks*, arXiv:2505.08752): a tonnetz can also be
realized as a **Levi graph** and as a **points-and-lines configuration**
(their D222 for the Euclidean tonnetz). So a single tonnetz has at least four
faces: triangle tiling, hexagon tiling, Levi graph, configuration.

---

## 4. Three frameworks, kept distinct

This project touches three related but distinct mathematical settings. Keeping
them apart prevents the confusion that cost us several iterations.

| Framework | Object | Tiles are | Edges are | Source |
|---|---|---|---|---|
| **Configurations** | Levi graph / {12₃} configuration | (points & lines) | incidences | Boland–Hughston |
| **Archimedean tonnetze** | {4,6,12} tiling + Laves dual | dodecagons, hexagons, squares | shared tones | Boland–Hughston §V |
| **Generalized Tonnetz** | circle of cross-polytopes | simplexes (triangles, tetrahedra…) | single-step voice leading | Tymoczko 2012 |

The **Harmonious tessellation** of harmoniousapp.net belongs to the third
framework. It is *not* a triad tonnetz and *not* a configuration. It is the
**note-based dual of a "zigzag" chord-based lattice** — specifically
Tymoczko's Figure 11, the two-chord-type lattice of the *second family*. He
states explicitly that this schematic "can represent voice-leading relations
among … diatonic and acoustic scales." That is exactly the harmoniousapp
diagram: seven-note scales (diatonic, acoustic/melodic-minor, harmonic
major/minor) joined by single-semitone voice leading.

(Earlier in the project I called the Harmonious tiling "a 2-D slice of the 3-D
orbifold." That is loosely true — the orbifold is the ambient continuous space
— but the precise statement is better: it is a discrete note-based lattice,
the dual of a Figure-11 zigzag, *embedded in* that orbifold.)

---

## 5. How many tessellations are there?

This was your central question. The answer has two parts.

### 5a. Regular-polygon (Archimedean) tessellations — finite, eleven.

If tiles must be **regular polygons**, the count is finite and known. At any
vertex the polygon interior angles must sum to 360°. There are **21** ways to
fit regular polygons around a single vertex; of these, exactly **11** extend
to a tiling of the whole plane. These are the **11 Archimedean tilings**
(Boland–Hughston, p. 22; Grünbaum & Shephard).

The {4,6,12} tiling — dodecagons, hexagons, squares — is one of them:
(4−2)/4 + (6−2)/6 + (12−2)/12 = 1/2 + 2/3 + 5/6 = 2, i.e. 90°+120°+150°=360°.
It is the tessellation that the **first Archimedean tonnetz** unfolds into
(Boland–Hughston Fig 12). Each of the 11 has a **dual Laves tiling**, so the
tonnetz-bearing regular tessellations form a finite, enumerable set: 11 + 11
duals.

So your instinct was right: **the musical tessellations coming from tonnetze,
in the regular-polygon sense, are finite.** The appendix cycle-counts in
Boland–Hughston (62 Hamiltonian cycles in the Eulerian tonnetz, etc.) are
finite for the same root reason — these are finite graphs.

### 5b. Voice-leading lattices in general — a structured infinity.

If tiles need only be *simplexes* (Tymoczko's note-based graphs), the family
is no longer finite, but it is completely *organized* by one number: the
relationship between **chord size** *k* and **scale size** *s*.

- If *k* divides *s*: a circle of *k*-cubes joined at shared **vertices**;
  dual to a circle of cross-polytopes joined at shared **facets**. (Triads in
  the chromatic scale: "Cube Dance" → circle of octahedra.)
- If *k* and *s* are **relatively prime**: a circle of cubes joined at shared
  **facets**; dual to a circle of simplexes joined at shared facets. (Triads
  in the diatonic scale: the zigzag → the Harmonious-type strip.)

The **dimension** of the note-based graph is set by *k* (for the first family)
or by the number of chord-types represented (for the second). So the "list" is
infinite but indexed: pick a scale, pick a chord size, pick how many
chord-types — the construction is determined. The Harmonious tessellation is
the entry (second family, 7-note scales, 2 chord-types-ish) and the {4,6,12}
is the entry (first Archimedean tonnetz). They are two specified points in one
systematic catalogue.

### 5c. The catch — redundancies and flip restrictions.

Tymoczko's hard lesson (his §3): once a note-based graph is even slightly
complex, it must contain **either** "flip restrictions" (some edge-flips are
*not* single-step voice leadings, and must be disallowed) **or**
"redundancies" (the same chord drawn in several places). The classical Tonnetz
is the rare graph with *neither* — which is exactly why it became iconic and
misled theorists into thinking all note-based graphs are so clean. Any
extension (the Harmonious strip included) will have flip restrictions: not
every shared edge is a legal single-semitone move. **This matters for orbit
tracing:** an edge in the tessellation is a candidate voice leading, not a
guaranteed single-step one. The widget's adjacency captures the *graph*; the
*metric* (is this flip size-one?) is a separate, finer question.

---

## 6. Where the project's two tessellations sit

**Harmonious tessellation** (`harmony_tiling.py` + `harmony_tessellation.py` +
`harmony-map.html`).
A note-based, second-family voice-leading lattice for seven-note scales.
Hexagons = diatonic/major scales; rhombi = acoustic/melodic-minor; up-triangles
= harmonic major; down-triangles = harmonic minor. Hexagons join into NW–SE
strips (two hexagon-neighbours per hexagon — the two diatonic scales a fifth
away), with triangle/rhombus bands between strips. Verified gap-free and
overlap-free; every interior hexagon borders 2 hexagons + 2 rhombi + 1
up-triangle + 1 down-triangle, matching the harmoniousapp distance-1 data.

**{4,6,12} Archimedean tonnetz tessellation** (`tonnetz_tessellation.py`).
The truncated trihexagonal tiling — dodecagons, hexagons, squares — that the
first Archimedean tonnetz of Boland–Hughston unfolds into (their Fig 12).
Built directly on the dodecagon triangular lattice (constant L = 2·a₁₂ + s).
Dodecagons carry triads ascending in fifths, so the circle-of-fifths
Hamiltonian reads off any row. One of the 11 Archimedean tilings; has a dual
Laves tiling not yet drawn.

A third tiling — the **rhombitrihexagonal** one drawn early in the project
(every hexagon ringed by 6 rhombi) — was **retired**. It is a valid plane
tiling but corresponds to *no* tonnetz: it is neither an Archimedean
tonnetz-tiling nor a note-based dual of any chord-based lattice. It had no
musical basis and was dropped.

---

## 7. Open directions

- **Euclidean Tonnetz pair.** The triangle tiling and its dual hexagon tiling
  (Boland–Hughston Figs 1–2; Tymoczko Fig 1) are the most classical
  tonnetz-tessellations and are not yet in the project. They would round out
  the tonnetz file.
- **Laves dual of {4,6,12}.** Each Archimedean tiling has a dual Laves tiling;
  drawing it would complete the {4,6,12} picture (Boland–Hughston note it
  explicitly).
- **Flip-restriction layer.** Mark, on the Harmonious widget, which edges are
  genuine single-semitone moves and which are larger — so an orbit traced on
  the diagram carries honest voice-leading distances.
- **Orbit input.** Let the print scripts take a sequence of keys/chords and
  draw the progression as arrows on the tessellation (the "orbit" use case).
- **Cube Dance / octahedral Tonnetz.** Tymoczko's three-note voice-leading
  Tonnetz (his Fig 14b) — the circle of octahedra, including augmented triads.
  A genuine note-based graph; a possible third tessellation file.

---

## 8. Sources

- D. Tymoczko, "The Generalized Tonnetz," *Journal of Music Theory* 56:1
  (2012), 1–52.
- J. R. Boland & L. P. Hughston, "Configurations, Tessellations and Tone
  Networks," arXiv:2505.08752.
- harmoniousapp.net — "Beyond Diatonic" (/p/0c) and "Orbifold Voice Leading"
  (/p/78).
- Grünbaum & Shephard, *Tilings and Patterns* (for the 11 Archimedean tilings
  and Laves duals).
