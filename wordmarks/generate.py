#!/usr/bin/env python3
"""Generate the family wordmarks as SVG, one per project, light and dark.

Geometry mirrors components/Plate.astro exactly, and both read their outlines
from wordmarks/glyphs.json. Change the component and this together, or the
assets drift from what the sites render.

    python3 wordmarks/generate.py

It also writes each project's stacked tile -- the plate turned on its side,
for app icons and avatars -- and the compact tile that replaces it below
about 24px (family-visual-identity.md section 1).

The type is emitted as outlines, not as <text>. The plate geometry is computed
from JetBrains Mono's 600-unit advance, so a viewer without that font used to
get a fallback mono whose advance did not match a divider that does not move.
Outlines make the SVG self-contained: it renders identically everywhere, with
no font dependency and nothing to install.

wordmarks/glyphs.json is the consequence -- A-Z, 0-9 and x in JetBrains Mono
Bold, as path data in font units. components/Plate.astro reads the same file,
so the component and these assets cannot drift apart. Outlining freezes the
type: a JetBrains Mono release no longer reflows the marks. That is deliberate
for a wordmark. To take a new version, re-extract with:

    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    f = TTFont("JetBrainsMono-Bold.ttf"); gs = f.getGlyphSet()
    pen = SVGPathPen(gs, ntos=lambda v: str(int(round(v))))
    gs[f.getBestCmap()[ord(ch)]].draw(pen); pen.getCommands()

fontTools is needed for that one-off step only. This script is stdlib.
"""
import json
import pathlib

PROJECTS = {
    "code": "#a93800", "emu": "#0066af", "asm": "#007742",
    "cat": "#8000e0", "build": "#865900", "debug": "#b9003c",
    "isa": "#00717b", "forge": "#a4009e", "play": "#5b6c00",
    "format": "#007465", "studio": "#482aff",
}

_DATA = json.loads((pathlib.Path(__file__).parent / "glyphs.json").read_text())
UPEM = _DATA["upem"]          # JetBrains Mono units per em
ADV_UNITS = _DATA["advance"]  # its advance, the 0.6em the geometry above assumes
GLYPHS = _DATA["glyphs"]
CAP = _DATA["capHeight"] / UPEM   # 0.73 em — what the type is centred on

F = 48.0            # cell type size
ADV = 0.6 * F       # JetBrains Mono advance width
PAD_X = 0.6 * F     # matches padding: … 0.6em
PAD_Y = 0.34 * F    # matches padding: 0.34em …
STROKE = 2.0 / 14.0 * F   # the component's 2px border at font-size 14
LETTER_SPACING_UNITS = -10   # the component's -0.01em, in font units
RADIUS = 3.0 / 14.0 * F

THEMES = {
    "light": {"frame": "#3a2c1f", "cell": "#fdfcf7", "ink": "#3a2c1f", "fill_ink": "#faf8f2"},
    "dark":  {"frame": "#efe7d6", "cell": "#242019", "ink": "#efe7d6", "fill_ink": "#faf8f2"},
}


def run(text: str, x: float, y: float, fill: str) -> str:
    """One text run as outlines: a scaled group, one path per glyph.

    scale(s, -s) flips the y axis, so path data stays in readable font units
    and the baseline lands on y exactly where the <text> version put it.
    """
    s = F / UPEM
    step = ADV_UNITS + LETTER_SPACING_UNITS
    paths = []
    for i, ch in enumerate(text):
        dx = f' transform="translate({i * step} 0)"' if i else ""
        paths.append(f'<path d="{GLYPHS[ch]}"{dx}/>')
    inner = "".join(paths)
    return (f'<g fill="{fill}" transform="translate({x:.1f} {y:.1f}) '
            f'scale({s:.3f} -{s:.3f})">{inner}</g>')


def plate(prefix: str, fill: str, theme: dict) -> str:
    left, right = prefix.upper(), "198x"
    w_l = len(left) * ADV + 2 * PAD_X
    w_r = len(right) * ADV + 2 * PAD_X
    h = F + 2 * PAD_Y
    w = w_l + w_r + STROKE          # one shared divider line
    ow, oh = w + STROKE, h + STROKE  # room for the outer stroke
    o = STROKE / 2
    # Centre the cap-height band in the cell, rather than sitting the type on a
    # text baseline. The names are uppercase with no descenders, so a text
    # baseline leaves 0.34em above the caps and 0.59em below them -- a 0.125em
    # list that reads as the type riding high. Centring on cap height rather
    # than on each string's ink keeps all nine plates on one baseline.
    baseline = o + (h + CAP * F) / 2
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{ow:.1f}" height="{oh:.1f}"
     viewBox="0 0 {ow:.1f} {oh:.1f}" role="img" aria-label="{prefix.capitalize()}198x">
  <title>{prefix.capitalize()}198x</title>
  <g>
    <clipPath id="r"><rect x="{o:.1f}" y="{o:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{RADIUS:.1f}"/></clipPath>
    <g clip-path="url(#r)">
      <rect x="{o:.1f}" y="{o:.1f}" width="{w_l:.1f}" height="{h:.1f}" fill="{fill}"/>
      <rect x="{o + w_l:.1f}" y="{o:.1f}" width="{w_r + STROKE:.1f}" height="{h:.1f}" fill="{theme['cell']}"/>
    </g>
    <rect x="{o:.1f}" y="{o:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{RADIUS:.1f}"
          fill="none" stroke="{theme['frame']}" stroke-width="{STROKE:.1f}"/>
    <line x1="{o + w_l + STROKE/2:.1f}" y1="{o:.1f}" x2="{o + w_l + STROKE/2:.1f}" y2="{o + h:.1f}"
          stroke="{theme['frame']}" stroke-width="{STROKE:.1f}"/>
    {run(left, o + PAD_X, baseline, theme['fill_ink'])}
    {run(right, o + w_l + STROKE + PAD_X, baseline, theme['ink'])}
  </g>
</svg>
'''


def centred_run(text: str, cx: float, cy: float, size: float, fill: str) -> str:
    """A text run of cap height centred on (cx, cy), at type size `size`."""
    s = size / UPEM
    step = ADV_UNITS + LETTER_SPACING_UNITS
    width = (len(text) * step - LETTER_SPACING_UNITS) * s
    x, y = cx - width / 2, cy + CAP * size / 2
    paths = "".join(
        f'<path d="{GLYPHS[ch]}"' + (f' transform="translate({i * step} 0)"' if i else "") + "/>"
        for i, ch in enumerate(text)
    )
    return (f'<g fill="{fill}" transform="translate({x:.2f} {y:.2f}) '
            f'scale({s:.4f} -{s:.4f})">{paths}</g>')


def stacked(prefix: str, fill: str, theme: dict, size: float = 1024.0,
            compact: bool = False, margin: float = 0.0) -> str:
    """The stacked tile: the project fill carrying 19 over the constant cell
    carrying 8x, divided and framed in the frame colour. `compact` is the
    small-size form, the wildcard x alone on the fill. `margin` insets the
    tile within a transparent canvas, as fraction of the side, for icon grids
    that expect one (Apple's is 100/1024)."""
    name = f"{prefix.capitalize()}198x"
    o = size * margin
    side = size - 2 * o
    stroke = side / 26          # proportionally heavier than the plate's F/7,
    radius = side * 0.11        # so the frame survives at 32px
    inner = side - stroke
    x0 = y0 = o + stroke / 2
    frame = (f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{inner:.2f}" height="{inner:.2f}" '
             f'rx="{radius:.2f}" fill="none" stroke="{theme['frame']}" stroke-width="{stroke:.2f}"/>')
    if compact:
        body = (f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{inner:.2f}" height="{inner:.2f}" '
                f'rx="{radius:.2f}" fill="{fill}"/>' + frame
                + centred_run("x", size / 2, size / 2 - side * 0.04, side * 0.95, theme["fill_ink"]))
    else:
        half = inner / 2
        type_size = half * 0.62
        body = (f'<clipPath id="t"><rect x="{x0:.2f}" y="{y0:.2f}" width="{inner:.2f}" '
                f'height="{inner:.2f}" rx="{radius:.2f}"/></clipPath>'
                f'<g clip-path="url(#t)">'
                f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{inner:.2f}" height="{half:.2f}" fill="{fill}"/>'
                f'<rect x="{x0:.2f}" y="{y0 + half:.2f}" width="{inner:.2f}" height="{half:.2f}" fill="{theme['cell']}"/>'
                f'</g>{frame}'
                f'<line x1="{x0:.2f}" y1="{y0 + half:.2f}" x2="{x0 + inner:.2f}" y2="{y0 + half:.2f}" '
                f'stroke="{theme['frame']}" stroke-width="{stroke:.2f}"/>'
                + centred_run("19", size / 2, y0 + half / 2, type_size, theme["fill_ink"])
                + centred_run("8x", size / 2, y0 + half * 1.5, type_size, theme["ink"]))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size:g}" height="{size:g}" '
            f'viewBox="0 0 {size:g} {size:g}" role="img" aria-label="{name}">'
            f'<title>{name}</title>{body}</svg>\n')


if __name__ == "__main__":
    import shutil
    import subprocess

    out = pathlib.Path(__file__).parent
    rsvg = shutil.which("rsvg-convert")
    n = 0
    for name, fill in PROJECTS.items():
        for theme_name, theme in THEMES.items():
            svg = out / f"{name}198x-{theme_name}.svg"
            svg.write_text(plate(name, fill, theme))
            n += 1
            # PNG as well, for the places that cannot take an SVG at all --
            # some mail clients, some social card scrapers. Not a font
            # workaround any more: the SVG carries its own outlines.
            if rsvg:
                subprocess.run(
                    [rsvg, "-w", "600", str(svg), "-o", str(svg.with_suffix(".png"))],
                    check=True,
                )
            for suffix, compact, width in (("stacked", False, 512), ("stacked-compact", True, 64)):
                tile = out / f"{name}198x-{suffix}-{theme_name}.svg"
                tile.write_text(stacked(name, fill, theme, compact=compact))
                n += 1
                if rsvg:
                    subprocess.run(
                        [rsvg, "-w", str(width), str(tile), "-o", str(tile.with_suffix(".png"))],
                        check=True,
                    )
    print(f"{n} wordmarks written to {out}" + ("" if rsvg else " (no rsvg-convert: SVG only)"))
