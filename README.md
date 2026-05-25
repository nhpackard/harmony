# harmony-tessellations

Tools for tracing harmonic progressions of musical pieces as **orbits on
tessellations of harmony space**.

Two tessellations, each with a genuine music-theory basis, kept in separate
modules:

- **`harmonious/`** — the *Harmonious tessellation* (harmoniousapp.net's
  "Beyond Diatonic" diagram): a note-based voice-leading lattice of seven-note
  scales. Hexagons are diatonic/major scales; rhombi are acoustic/melodic
  minor; triangles are harmonic major (apex up) and harmonic minor (apex
  down). Hexagons join into NW–SE strips along the circle of fifths.
- **`tonnetz/`** — the *{4,6,12} Archimedean tonnetz tessellation*
  (dodecagons, hexagons, squares), the tiling that the first Archimedean
  tonnetz of Boland & Hughston (arXiv:2505.08752) unfolds into.

See **`docs/TONNETZ_AND_TESSELLATIONS.md`** for the theory — what a tonnetz
is, how tonnetze relate to tessellations, and why these two tilings are
legitimate. See **`docs/PROJECT_REVIEW.md`** for project status, file-by-file
state, decisions, and next steps.

## Layout

```
harmony-tessellations/
  README.md
  docs/
    TONNETZ_AND_TESSELLATIONS.md   theory reference
    PROJECT_REVIEW.md              status + how to resume
  harmonious/
    harmony_tiling.py              geometry core (verified strip tiling)
    harmony_tessellation.py        print generator (PDF + SVG); imports the core
    harmony-map.html               interactive widget
  tonnetz/
    tonnetz_tessellation.py        standalone {4,6,12} generator (PDF + SVG)
  output/                          generated files (git-ignored)
```

## Usage

```sh
# Harmonious tessellation — print PDF + SVG
cd harmonious
python3 harmony_tessellation.py --out ../output/harmony_tessellation
# (harmony_tessellation.py requires harmony_tiling.py in the same folder)

# Open harmonious/harmony-map.html in a browser for the interactive widget.

# {4,6,12} tonnetz tessellation — print PDF + SVG
cd tonnetz
python3 tonnetz_tessellation.py --out ../output/tonnetz_tessellation
```

Both generators verify their geometry on each run (gap-free, overlap-free,
correct interior adjacency) and print the result.

## Requirements

Python 3 with `matplotlib`, `reportlab`, and `cairosvg`.

## Conventions

- UPPER-CASE key label = major-type scale; lower-case = minor-type.
- Colour + shape encode the exact scale type.
- Real Unicode accidentals (♯ U+266F, ♭ U+266D).
- Print output is white-background with light translucent fills, so a
  progression can be traced over it by hand.

## Sources

- D. Tymoczko, "The Generalized Tonnetz," *Journal of Music Theory* 56:1 (2012).
- J. R. Boland & L. P. Hughston, "Configurations, Tessellations and Tone
  Networks," arXiv:2505.08752.
- harmoniousapp.net — "Beyond Diatonic" and "Orbifold Voice Leading".
