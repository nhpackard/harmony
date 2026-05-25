"""
harmony_tiling.py -- geometry core for the Harmonious voice-leading tessellation.

This builds the tessellation shown in the "Rest of the Shapes" / "Beyond
Diatonic" pages of harmoniousapp.net. It is a 2-D slice of the 3-D voice-leading
orbifold for seven-note scales (see harmoniousapp.net/p/78/Orbifold-Voice-Leading).

    hexagon   -> diatonic / major scale
    rhombus   -> acoustic / melodic-minor scale
    triangle  -> harmonic major (apex up) / harmonic minor (apex down)

Every shared edge is a single-semitone voice-leading step. The defining
adjacency, confirmed against the harmoniousapp Voice-Leading Relationship data
(e.g. F#-Major lists D-flat Major, E-flat Harmonic Minor, F# Melodic Minor,
F# Harmonic Major as its distance-1 neighbours), is:

    a diatonic hexagon borders
        2 hexagons   (the two diatonic scales a fifth away)
        2 rhombi     (acoustic / melodic-minor scales)
        1 up-triangle   (harmonic major)
        1 down-triangle (harmonic minor)

Geometrically: hexagons join edge-to-edge into NW-SE strips; the bands between
strips are filled by one row of alternating triangles and 60-degree rhombi.
The construction is gap-free and overlap-free (see verify()).

`build_tiling()` returns a list of plain dicts:
    {type, pts, cx, cy, label, scale, up, rel(hex only), ang(rho only)}
"""

from __future__ import annotations
import math

S = 60.0                       # common edge length of every polygon
SQ3 = math.sqrt(3.0)

# Lattice vectors for the hexagon centres.
STRIP = (1.5 * S, -S * SQ3 / 2.0)      # step to the SE hexagon  (90, -51.96)
STACK = (0.5 * S, 1.5 * S * SQ3)       # step to the strip above (30, 155.88)
# Rhombus offset vector: a band rhombus is [V1, V0, V0+U, V1+U].
U = (0.5 * S, S * SQ3 / 2.0)           # (30, 51.96)

# Real Unicode accidentals: U+266F sharp, U+266D flat.
FIFTHS = ["F", "C", "G", "D", "A", "E", "B", "F\u266f",
          "D\u266d", "A\u266d", "E\u266d", "B\u266d"]

# Conventional spelling of each major key's relative natural minor.
RELATIVE_MINOR = {
    "C": "a", "G": "e", "D": "b", "A": "f\u266f", "E": "c\u266f",
    "B": "g\u266f", "F\u266f": "d\u266f", "D\u266d": "b\u266d",
    "A\u266d": "f", "E\u266d": "c", "B\u266d": "g", "F": "d",
}


def _hexv(cx, cy):
    """Flat-top hexagon vertices (maths y-up), counter-clockwise from +x."""
    return [(cx + S * math.cos(math.radians(a)),
             cy + S * math.sin(math.radians(a)))
            for a in (0, 60, 120, 180, 240, 300)]


def _centroid(pts):
    n = len(pts)
    return (sum(p[0] for p in pts) / n, sum(p[1] for p in pts) / n)


def build_tiling(radius: int = 7):
    """Build the Harmonious strip tessellation.

    `radius` controls how many hexagon rows/columns are generated.
    Returns (tiles, centres) where centres maps (row, col) -> hexagon centre.
    """
    centres = {}
    for r in range(-radius, radius + 1):
        for i in range(-radius, radius + 2):
            centres[(r, i)] = (i * STRIP[0] + r * STACK[0],
                               i * STRIP[1] + r * STACK[1])

    tiles = []

    # ---- hexagons : diatonic / major --------------------------------------
    # Key advances by a fifth along the strip (the 'i' axis); the strip-stack
    # ('r' axis) shifts by the amount that keeps the circle-of-fifths reading
    # consistent between adjacent strips.
    for (r, i), (cx, cy) in centres.items():
        idx = (i + 2 * r) % 12
        key = FIFTHS[idx]
        V = _hexv(cx, cy)
        tiles.append(dict(type="hex", pts=[list(p) for p in V],
                          cx=cx, cy=cy,
                          label=key, scale="major", up=True,
                          rel=RELATIVE_MINOR[key]))

    tri_seen = set()
    rho_seen = set()

    def key_at(c):
        return (round(c[0], 1), round(c[1], 1))

    for (r, i), (cx, cy) in centres.items():
        idx = (i + 2 * r) % 12
        V = _hexv(cx, cy)

        # N up-triangle on edge V1-V2 : harmonic major
        apex = ((V[1][0] + V[2][0]) / 2.0, V[1][1] + S * SQ3 / 2.0)
        p = [V[1], V[2], apex]
        c = _centroid(p)
        if key_at(c) not in tri_seen:
            tri_seen.add(key_at(c))
            tiles.append(dict(type="tri", pts=[list(x) for x in p],
                              cx=c[0], cy=c[1],
                              label=FIFTHS[idx], scale="harm maj", up=True))

        # S down-triangle on edge V4-V5 : harmonic minor
        apex = ((V[4][0] + V[5][0]) / 2.0, V[4][1] - S * SQ3 / 2.0)
        p = [V[4], V[5], apex]
        c = _centroid(p)
        if key_at(c) not in tri_seen:
            tri_seen.add(key_at(c))
            tiles.append(dict(type="tri", pts=[list(x) for x in p],
                              cx=c[0], cy=c[1],
                              label=FIFTHS[(idx + 3) % 12], scale="harm min",
                              up=False))

        # NE rhombus on edge V0-V1 : acoustic / melodic minor
        p = [V[1], V[0],
             (V[0][0] + U[0], V[0][1] + U[1]),
             (V[1][0] + U[0], V[1][1] + U[1])]
        c = _centroid(p)
        if key_at(c) not in rho_seen:
            rho_seen.add(key_at(c))
            tiles.append(dict(type="rho", pts=[list(x) for x in p],
                              cx=c[0], cy=c[1],
                              label=FIFTHS[(idx + 1) % 12], scale="mel min",
                              up=True))

        # SW rhombus on edge V3-V4 : acoustic / melodic minor
        p = [V[4], V[3],
             (V[3][0] - U[0], V[3][1] - U[1]),
             (V[4][0] - U[0], V[4][1] - U[1])]
        c = _centroid(p)
        if key_at(c) not in rho_seen:
            rho_seen.add(key_at(c))
            tiles.append(dict(type="rho", pts=[list(x) for x in p],
                              cx=c[0], cy=c[1],
                              label=FIFTHS[idx], scale="mel min", up=True))

    return tiles, centres


def crop(tiles, half_w, half_h):
    """Keep tiles whose centroid lies in a centred rectangle."""
    hx = [t["cx"] for t in tiles if t["type"] == "hex"]
    hy = [t["cy"] for t in tiles if t["type"] == "hex"]
    mx, my = sum(hx) / len(hx), sum(hy) / len(hy)
    return [t for t in tiles
            if mx - half_w < t["cx"] < mx + half_w
            and my - half_h < t["cy"] < my + half_h]


def normalize(tiles, pad=24):
    """Shift + flip into SVG (y-down) coordinates. Returns (W, H, tiles).

    Vertices are snapped to the exact triangular grid the tiling lives on
    (x a multiple of S/2, y a multiple of S*SQ3/2) so that shared vertices
    are bit-identical and edge-based adjacency is exact.
    """
    gx = S / 2.0
    gy = S * SQ3 / 2.0

    def snap(x, y):
        return (round(x / gx) * gx, round(y / gy) * gy)

    xs = [p[0] for t in tiles for p in t["pts"]]
    ys = [p[1] for t in tiles for p in t["pts"]]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    W, H = maxx - minx + 2 * pad, maxy - miny + 2 * pad
    out = []
    for t in tiles:
        nt = dict(t)
        snapped = []
        for x, y in t["pts"]:
            sx, sy = snap(x, y)
            snapped.append([round(sx - minx + pad, 3),
                            round(maxy - sy + pad, 3)])
        nt["pts"] = snapped
        cx, cy = _centroid(snapped)
        nt["cx"], nt["cy"] = round(cx, 2), round(cy, 2)
        if t["type"] == "rho":
            p = nt["pts"]
            d02 = math.hypot(p[0][0] - p[2][0], p[0][1] - p[2][1])
            d13 = math.hypot(p[1][0] - p[3][0], p[1][1] - p[3][1])
            a, b = (p[0], p[2]) if d02 >= d13 else (p[1], p[3])
            ang = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
            if ang > 90:
                ang -= 180
            if ang < -90:
                ang += 180
            nt["ang"] = round(ang, 1)
        out.append(nt)
    return round(W, 1), round(H, 1), out


def verify(tiles):
    """Check the tiling. Returns a dict describing interior adjacency.

    For a correct Harmonious tiling every deep-interior hexagon must border
    exactly 2 hexagons, 2 rhombi, 1 up-triangle and 1 down-triangle.
    """
    def edges(t):
        p = t["pts"]
        return [tuple(sorted([(round(p[k][0], 1), round(p[k][1], 1)),
                              (round(p[(k + 1) % len(p)][0], 1),
                               round(p[(k + 1) % len(p)][1], 1))]))
                for k in range(len(p))]

    emap = {}
    for i, t in enumerate(tiles):
        for e in edges(t):
            emap.setdefault(e, []).append(i)

    over = sum(1 for e, v in emap.items() if len(v) > 2)

    xs = [p[0] for t in tiles for p in t["pts"]]
    ys = [p[1] for t in tiles for p in t["pts"]]
    mx0, mx1 = min(xs), max(xs)
    my0, my1 = min(ys), max(ys)
    inset_x = (mx1 - mx0) * 0.25
    inset_y = (my1 - my0) * 0.25

    good = bad = 0
    for i, t in enumerate(tiles):
        if t["type"] != "hex":
            continue
        if not (mx0 + inset_x < t["cx"] < mx1 - inset_x
                and my0 + inset_y < t["cy"] < my1 - inset_y):
            continue
        kinds = {"hex": 0, "rho": 0, "tri_up": 0, "tri_dn": 0}
        for e in edges(t):
            for j in emap[e]:
                if j == i:
                    continue
                u = tiles[j]
                if u["type"] == "tri":
                    kinds["tri_up" if u["up"] else "tri_dn"] += 1
                else:
                    kinds[u["type"]] += 1
        if (kinds["hex"] == 2 and kinds["rho"] == 2
                and kinds["tri_up"] == 1 and kinds["tri_dn"] == 1):
            good += 1
        else:
            bad += 1
    return {"edges_shared_by_more_than_2": over,
            "interior_hexagons_correct": good,
            "interior_hexagons_wrong": bad}


if __name__ == "__main__":
    tiles, _ = build_tiling(radius=7)
    n = {"hex": 0, "rho": 0, "tri": 0}
    for t in tiles:
        n[t["type"]] += 1
    print(f"raw: {n['hex']} hexagons, {n['rho']} rhombi, {n['tri']} triangles")
    print("verification:", verify(tiles))
