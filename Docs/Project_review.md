# Project Review — Harmony Tessellations

*Status, file-by-file state, decisions, and how to resume. Written so a future
session (Claude Code or chat) can pick up cold.*

Last updated: end of the session that produced the {4,6,12} tonnetz file and
this document.

---

## 1. What this project is

Tools for the user — a music-theory enthusiast — to **trace harmonic
progressions of pieces as orbits on tessellations of "harmony space."**

Two tessellations, deliberately kept in **separate files / frameworks**:

1. **Harmonious tessellation** — the "Rest of the Shapes" / "Beyond Diatonic"
   diagram from harmoniousapp.net. A note-based voice-leading lattice of
   seven-note scales. The user's primary tool.
2. **{4,6,12} Archimedean tonnetz tessellation** — dodecagons/hexagons/squares,
   from Boland–Hughston arXiv:2505.08752 Fig 12. The genuinely
   tonnetz-derived tiling.

See `TONNETZ_AND_TESSELLATIONS.md` for the theory and how the two relate.

---

## 2. File-by-file state

All delivered files are in `/mnt/user-data/outputs/`. Working copies in
`/home/claude/`.

### Harmonious tessellation — COMPLETE

- **`harmony_tiling.py`** — geometry core. Builds the strip tiling.
  - Constants: `S=60` (edge), `STRIP=(90,-51.96)` (SE-neighbour step),
    `STACK=(30,155.88)` (strip-above step), `U=(30,51.96)` (rhombus offset).
  - `build_tiling(radius)` → `(tiles, centres)`. Tiles are dicts:
    `{type:'hex'|'rho'|'tri', pts, cx, cy, label, scale, up, rel(hex), ang(rho)}`.
  - `crop`, `normalize` (snaps vertices to the exact grid so adjacency is
    exact), `verify`.
  - VERIFIED: 0 overlaps; every interior hexagon borders
    2 hex + 2 rho + 1 up-tri + 1 down-tri.
- **`harmony_tessellation.py`** — print generator. Imports `harmony_tiling`.
  White background, translucent fills (`FILL_ALPHA=0.20`) for ink-light
  tracing. Outputs multi-page PDF + single SVG. CLI: `--radius --paper
  --cols --page-rows --out`.
- **`harmony-map.html`** — interactive widget. Medium crop (radius 6).
  Hover previews a tile's neighbours; click tiles in sequence to build a
  progression (each click must be edge-adjacent to the last); drag to pan.
- **`harmony_tessellation.pdf` / `.svg`** — generated print output.

### {4,6,12} tonnetz tessellation — COMPLETE (core)

- **`tonnetz_tessellation.py`** — standalone, self-contained (no shared
  module). Builds the truncated trihexagonal tiling directly on the dodecagon
  triangular lattice (`L = 2*A12 + S`), no BFS. Dodecagons at lattice points,
  hexagons at triangle centroids, squares at edge midpoints. Dodecagons
  labelled with triads in fifths order. White-bg PDF + SVG.
  CLI: `--rings --paper --cols --page-rows --out`.
  - VERIFIED: 0 overlaps; interior dodecagons border 6 hex + 6 sq;
    hexagons 3 dod + 3 sq; squares 2 dod + 2 hex.
- **`tonnetz_tessellation.pdf` / `.svg`** — generated print output.

### Reference

- **`TONNETZ_AND_TESSELLATIONS.md`** — the theory reference.
- **`PROJECT_REVIEW.md`** — this file.

---

## 3. Key conventions (apply to both tessellations)

- **Case = quality.** UPPER-CASE key label = major-type tile (diatonic major,
  harmonic major); lower-case = minor-type (melodic minor, harmonic minor).
- **Colour + shape = exact scale type**, so no "harm/mel" text is needed.
  Harmonious palette: hex `#cd7430` (orange, diatonic), rho `#dcb648` (yellow,
  acoustic/melodic minor), up-tri `#7c9d6a` (green, harmonic major), down-tri
  `#6b8db1` (blue, harmonic minor).
- **Hexagons** show the major key bold on top, the relative natural minor in
  parentheses below, smaller and non-bold (e.g. `C` / `(a)`).
- **Real Unicode accidentals**: `♯` U+266F, `♭` U+266D — never ASCII `#`/`b`.
- **Print**: white background, `FILL_ALPHA=0.20`, dark edges/ink — a
  light substrate that leaves room to draw an orbit by hand.

---

## 4. Decisions made (and why)

- **The rhombitrihexagonal tiling was retired.** Early in the project the
  Harmonious tiling was drawn with every hexagon ringed by 6 rhombi (0
  hexagon-neighbours). That is a valid plane tiling but corresponds to no
  tonnetz and contradicts the harmoniousapp distance-1 data (a diatonic scale
  has two diatonic neighbours a fifth away). It was replaced by the **strip
  tiling** (hexagons touch in NW–SE strips). Do not reintroduce it.
- **Two separate files, two frameworks.** Harmonious = Tymoczko second-family
  note-based lattice; {4,6,12} = Archimedean tonnetz. They are different
  mathematical objects and are kept apart deliberately.
- **Tonnetz file uses a direct lattice, not BFS.** An earlier BFS build of the
  {4,6,12} tiling ran out of memory (unbounded queue). The dodecagon centres
  lie on a known triangular lattice, so they are placed directly. Keep it that
  way.
- **Key placement is structural, not a transcription.** In the Harmonious
  tiling the exact key in a given tile follows a consistent index rule
  (`idx=(i+2r)%12` for hexagons, etc.), not a tile-for-tile copy of the
  harmoniousapp chart. The *adjacency structure* is faithful; absolute key
  placement is internally consistent but not pinned to a region of their
  diagram. State this caveat whenever it matters.

---

## 5. Known limitations / caveats

- **Flip restrictions are not yet modelled.** Per Tymoczko §3, a complex
  note-based graph has edges that are *not* single-semitone voice leadings.
  The Harmonious widget currently treats every shared edge as a legal move.
  An orbit traced on it is adjacency-correct but not yet
  voice-leading-distance-correct. (See `TONNETZ_AND_TESSELLATIONS.md` §5c.)
- **Cropped-edge tiles** show fewer neighbours than interior tiles — expected,
  not a bug. `verify()` only checks deep-interior tiles.
- **Tonnetz hexagons/squares are unlabelled.** Only dodecagons carry triads.
  The paper puts musical content on edges (shared tones); a future pass could
  label edges.

---

## 6. Environment notes

- Python: `matplotlib`, `cairosvg`, `reportlab`, `pdftoppm` all available.
- Render check loop: write SVG → `cairosvg` to PNG → view.
- Widget tile data is embedded in `harmony-map.html` between the markers
  `<script>\n` and `\n(function(){` as `const TILING={...};`.
- `harmony_tessellation.py` REQUIRES `harmony_tiling.py` in the same folder.
  `tonnetz_tessellation.py` is standalone.

---

## 7. Suggested next steps

In rough priority order:

1. **Set up the repo** (the user's stated goal). Suggested layout:
   ```
   harmony-tessellations/
     README.md
     docs/
       TONNETZ_AND_TESSELLATIONS.md
       PROJECT_REVIEW.md
     harmonious/
       harmony_tiling.py
       harmony_tessellation.py
       harmony-map.html
     tonnetz/
       tonnetz_tessellation.py
     output/            # generated PDFs/SVGs, git-ignored
   ```
   `harmony_tessellation.py` imports `harmony_tiling` — keep them together.
2. **Euclidean Tonnetz pair** — add the classical triangle tiling and its
   dual hexagon tiling to the tonnetz side. Most-classical tonnetz; currently
   missing.
3. **Flip-restriction layer** — mark genuine single-semitone edges on the
   Harmonious widget so traced orbits carry honest voice-leading distances.
4. **Orbit input** — let the scripts accept a chord/key sequence and draw the
   progression as arrows on the tessellation.
5. **Laves dual of {4,6,12}** — completes the Archimedean picture.
6. **Cube Dance / octahedral Tonnetz** — Tymoczko Fig 14b, a possible third
   tessellation.

---

## 8. One-paragraph summary for a cold start

This project builds two musical tessellations for tracing chord progressions
as orbits. The **Harmonious tessellation** (`harmonious/`) is a note-based
voice-leading lattice of seven-note scales — hexagons (diatonic) in NW–SE
strips, with rhombus (acoustic) and triangle (harmonic major/minor) bands
between; it has an interactive widget and a print PDF. The **{4,6,12} tonnetz
tessellation** (`tonnetz/`) is the Archimedean dodecagon/hexagon/square tiling
that the first Archimedean tonnetz unfolds into. Both are verified gap-free.
The geometry is settled; the open work is mostly additive — more
tessellations (Euclidean pair, Laves dual), a flip-restriction metric layer,
and an orbit-drawing input mode. Read `TONNETZ_AND_TESSELLATIONS.md` first for
the theory; it explains why these two tilings are legitimate and a third
(rhombitrihexagonal) was retired.
