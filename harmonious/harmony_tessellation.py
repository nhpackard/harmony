#!/usr/bin/env python3
"""
harmony_tessellation.py
=======================

Renders the voice-leading tessellation of "harmony space" -- the diagram in the
"Rest of the Shapes" section of https://harmoniousapp.net/p/0c/Beyond-Diatonic --
as print-ready output.

The tiling is the rhombitrihexagonal tessellation: a genuine, gap-free,
overlap-free tiling in which

    hexagon   -> diatonic / major scale
    rhombus   -> acoustic / melodic-minor scale
    triangle  -> harmonic major (apex up) / harmonic minor (apex down)

Every shared edge is a single-semitone voice-leading step, so a chord or scale
progression is a walk from polygon to polygon across the plane.

Outputs
-------
1. harmony_tessellation.pdf  -- multi-page; each page is one printable sheet.
                                The tiling runs continuously across page breaks,
                                so trimmed sheets tape into one large wall chart.
2. harmony_tessellation.svg  -- the whole tiling as a single vector file.

Usage
-----
    python harmony_tessellation.py
    python harmony_tessellation.py --radius 11 --cols 4 --page-rows 3
    python harmony_tessellation.py --paper a4 --cols 3 --page-rows 2

Dependencies: matplotlib, and the companion module harmony_tiling.py
(kept in the same folder).
"""

from __future__ import annotations

import argparse

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Polygon as MplPolygon

import harmony_tiling as ht


# --------------------------------------------------------------------------
# Appearance
# --------------------------------------------------------------------------

COLORS = {
    "hex": "#cd7430",      # diatonic / major
    "rho": "#dcb648",      # acoustic / melodic minor
    "tri_maj": "#7c9d6a",  # harmonic major  (apex up)
    "tri_min": "#6b8db1",  # harmonic minor  (apex down)
}
# Print appearance: white paper, light translucent fills so the chart can be
# used as an analysis substrate -- a harmonic progression can be traced over
# it as an orbit without the printed colour competing with the pen.
BG = "#ffffff"          # paper white
EDGE = "#3a342a"        # polygon outline -- dark enough to read on white
INK = "#1a150d"         # label text
FILL_ALPHA = 0.20       # translucency of every polygon fill

PAPER = {  # portrait dimensions in inches
    "letter": (8.5, 11.0),
    "legal": (8.5, 14.0),
    "a4": (8.27, 11.69),
    "a3": (11.69, 16.54),
    "tabloid": (11.0, 17.0),
}


def tile_color(t: dict) -> str:
    if t["type"] == "hex":
        return COLORS["hex"]
    if t["type"] == "rho":
        return COLORS["rho"]
    return COLORS["tri_maj"] if t["up"] else COLORS["tri_min"]


# --------------------------------------------------------------------------
# Drawing
# --------------------------------------------------------------------------

def draw_tiles(ax, tiles, edge_s: float, clip=None) -> None:
    """Render every polygon and its label.

    Every tile shows its key only. Case carries the major/minor distinction
    (UPPER = major-type, lower = minor-type); the polygon's colour and shape
    carry the exact scale type, so no "harm"/"mel" text is needed.
    Hexagons additionally show their relative natural minor, parenthesised.
    Fills are translucent (FILL_ALPHA) so a progression can be traced on top.

    `clip`, if given as (x_lo, x_hi, y_lo, y_hi), suppresses labels for tiles
    whose centre lies outside that window -- used for paged PDF output so a
    tile's text never spills into a neighbouring sheet's margin.
    """
    for t in tiles:
        ax.add_patch(MplPolygon(
            t["pts"], closed=True,
            facecolor=tile_color(t), alpha=FILL_ALPHA,
            edgecolor=EDGE, linewidth=1.2, joinstyle="round",
        ))
    # outlines drawn again at full opacity so the translucent fill does not
    # wash them out
    for t in tiles:
        ax.add_patch(MplPolygon(
            t["pts"], closed=True, fill=False,
            edgecolor=EDGE, linewidth=1.2, joinstyle="round",
        ))

    def in_window(t):
        if clip is None:
            return True
        xl, xh, yl, yh = clip
        return xl <= t["cx"] <= xh and yl <= t["cy"] <= yh

    def keytext(t):
        major = (t["type"] == "hex") or (t["type"] == "tri" and t["up"])
        return t["label"].upper() if major else t["label"].lower()

    for t in tiles:
        if not in_window(t):
            continue
        cx, cy = t["cx"], t["cy"]
        if t["type"] == "hex":
            # major key sits a little above centre, relative minor well below,
            # with a clear gap so the two never touch
            ax.text(cx, cy - 0.20 * edge_s, keytext(t),
                    ha="center", va="center",
                    fontsize=0.24 * edge_s, color=INK,
                    fontweight="bold", family="monospace")
            ax.text(cx, cy + 0.22 * edge_s, f"({t['rel'].lower()})",
                    ha="center", va="center",
                    fontsize=0.13 * edge_s, color=INK, alpha=0.75,
                    family="monospace")
        elif t["type"] == "rho":
            ax.text(cx, cy, keytext(t), ha="center", va="center",
                    fontsize=0.17 * edge_s, color=INK,
                    fontweight="bold", family="monospace",
                    rotation=-t.get("ang", 0), rotation_mode="anchor")
        else:  # triangle
            oy = (0.06 if t["up"] else -0.08) * edge_s
            ax.text(cx, cy + oy, keytext(t), ha="center", va="center",
                    fontsize=0.17 * edge_s, color=INK,
                    fontweight="bold", family="monospace")


def draw_legend(ax, edge_s: float) -> None:
    """Compact legend box, bottom-left of the axis."""
    x0 = ax.get_xlim()[0]
    y_lo, y_hi = sorted(ax.get_ylim())
    w = ax.get_xlim()[1] - x0
    h = y_hi - y_lo
    lx = x0 + 0.022 * w
    ly = y_lo + 0.022 * h
    rows = [
        (COLORS["hex"], "HEX", "diatonic major  (key + relative minor)"),
        (COLORS["rho"], "rhombus", "acoustic / melodic minor"),
        (COLORS["tri_maj"], "TRIANGLE up", "harmonic major"),
        (COLORS["tri_min"], "triangle down", "harmonic minor"),
    ]
    sw = 0.5 * edge_s
    gap = 0.8 * edge_s
    pad = 0.4 * edge_s
    box_w = 12.0 * edge_s
    box_h = gap * len(rows) + 2 * pad
    ax.add_patch(MplPolygon(
        [(lx, ly), (lx + box_w, ly),
         (lx + box_w, ly + box_h), (lx, ly + box_h)],
        closed=True, facecolor="#ffffff", edgecolor=EDGE,
        linewidth=1.0, zorder=5))
    for idx, (col, name, desc) in enumerate(rows):
        ry = ly + box_h - pad - sw - idx * gap
        ax.add_patch(MplPolygon(
            [(lx + pad, ry), (lx + pad + sw, ry),
             (lx + pad + sw, ry + sw), (lx + pad, ry + sw)],
            closed=True, facecolor=col, alpha=FILL_ALPHA,
            edgecolor=EDGE, linewidth=1.0, zorder=6))
        ax.text(lx + pad + sw + 0.32 * edge_s, ry + sw * 0.5,
                f"{name}  -  {desc}", ha="left", va="center",
                fontsize=0.17 * edge_s, color=INK,
                family="monospace", zorder=6)


# --------------------------------------------------------------------------
# Output
# --------------------------------------------------------------------------

def render_svg(tiles, path: str, edge_s: float) -> None:
    xs = [p[0] for t in tiles for p in t["pts"]]
    ys = [p[1] for t in tiles for p in t["pts"]]
    w, h = max(xs) - min(xs), max(ys) - min(ys)

    fig_w = 16.0
    fig, ax = plt.subplots(figsize=(fig_w, fig_w * h / w))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)

    draw_tiles(ax, tiles, edge_s)

    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(max(ys), min(ys))          # SVG y-down
    ax.set_aspect("equal")
    ax.axis("off")
    draw_legend(ax, edge_s)
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    fig.savefig(path, format="svg", facecolor=BG)
    plt.close(fig)
    print(f"  wrote {path}")


def render_pdf(tiles, path: str, edge_s: float,
               paper: str, cols: int, page_rows: int,
               margin_in: float = 0.4) -> None:
    """Render the tiling across a (cols x page_rows) grid of printable sheets.

    Each page shows one window of the tiling. The window's aspect ratio is
    matched to the printable area of the sheet, so the equal-aspect drawing
    fills the page edge-to-edge with no blank side-bands.
    """
    xs = [p[0] for t in tiles for p in t["pts"]]
    ys = [p[1] for t in tiles for p in t["pts"]]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    total_w, total_h = maxx - minx, maxy - miny

    paper_w, paper_h = PAPER[paper]
    landscape = total_w / total_h > 1.0
    if landscape:
        paper_w, paper_h = paper_h, paper_w
    sheet_w = paper_w - 2 * margin_in
    sheet_h = paper_h - 2 * margin_in

    # One sheet covers span_x x span_y world units. To leave no blank bands,
    # span_x / span_y must equal the printable sheet aspect ratio. Start from
    # an even division, then expand whichever dimension is too small.
    span_x = total_w / cols
    span_y = total_h / page_rows
    sheet_aspect = sheet_w / sheet_h
    if span_x / span_y < sheet_aspect:
        span_x = span_y * sheet_aspect          # widen the window
    else:
        span_y = span_x / sheet_aspect          # heighten the window

    print(f"  PDF: {cols * page_rows} sheet(s)  ({cols} x {page_rows}), "
          f"{paper} {'landscape' if landscape else 'portrait'}")

    with PdfPages(path) as pdf:
        for pr in range(page_rows):
            for pc in range(cols):
                fig = plt.figure(figsize=(paper_w, paper_h))
                fig.patch.set_facecolor(BG)
                ax = fig.add_axes([margin_in / paper_w, margin_in / paper_h,
                                   sheet_w / paper_w, sheet_h / paper_h])
                ax.set_facecolor(BG)

                x0 = minx + pc * (total_w / cols)
                y0 = miny + pr * (total_h / page_rows)

                draw_tiles(ax, tiles, edge_s,
                           clip=(x0, x0 + span_x, y0, y0 + span_y))

                ax.set_xlim(x0, x0 + span_x)
                ax.set_ylim(y0 + span_y, y0)     # SVG y-down
                ax.set_aspect("equal")
                ax.axis("off")

                if pr == page_rows - 1 and pc == 0:
                    draw_legend(ax, edge_s)

                for fx in (0.0, 1.0):
                    for fy in (0.0, 1.0):
                        ax.plot([fx], [fy], marker="+", markersize=9,
                                markeredgewidth=0.8, color="#8a8275",
                                transform=ax.transAxes, clip_on=False)

                fig.text(0.5, margin_in / paper_h * 0.45,
                         f"harmony space   .   row {pr + 1} of {page_rows}"
                         f"   .   col {pc + 1} of {cols}",
                         ha="center", va="center", fontsize=7,
                         color="#8a8275", family="monospace")

                pdf.savefig(fig, facecolor=BG)
                plt.close(fig)
    print(f"  wrote {path}")


# --------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Render the harmony-space voice-leading tessellation.")
    ap.add_argument("--radius", type=int, default=10,
                    help="hexagon-ring radius to generate (default 10)")
    ap.add_argument("--paper", choices=sorted(PAPER), default="letter")
    ap.add_argument("--cols", type=int, default=3,
                    help="sheet columns in the PDF (default 3)")
    ap.add_argument("--page-rows", type=int, default=2,
                    help="sheet rows in the PDF (default 2)")
    ap.add_argument("--out", default="harmony_tessellation",
                    help="output filename stem")
    args = ap.parse_args()

    print("Building harmony-space tessellation ...")
    tiles, _ = ht.build_tiling(radius=args.radius)

    half_w = args.radius * 130.0
    half_h = args.radius * 100.0
    tiles = ht.crop(tiles, half_w, half_h)
    W, H, tiles = ht.normalize(tiles)

    n_hex = sum(t["type"] == "hex" for t in tiles)
    n_rho = sum(t["type"] == "rho" for t in tiles)
    n_tri = sum(t["type"] == "tri" for t in tiles)
    print(f"  {len(tiles)} tiles  ({n_hex} hexagons, {n_rho} rhombi, "
          f"{n_tri} triangles)")
    v = ht.verify(tiles)
    if v["edges_shared_by_more_than_2"] == 0 and v["interior_hexagons_wrong"] == 0:
        print(f"  geometry check passed: no overlaps, all "
              f"{v['interior_hexagons_correct']} interior hexagons have "
              f"2 hexagons + 2 rhombi + 2 triangles as neighbours")
    else:
        print(f"  geometry check WARNING: {v}")

    render_svg(tiles, f"{args.out}.svg", ht.S)
    render_pdf(tiles, f"{args.out}.pdf", ht.S,
               args.paper, args.cols, args.page_rows)
    print("Done.")


if __name__ == "__main__":
    main()
