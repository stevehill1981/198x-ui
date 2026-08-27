#!/usr/bin/env python3
"""Generate the family wordmarks as SVG, one per project, light and dark.

Geometry mirrors components/Plate.astro exactly, and both read their outlines
from wordmarks/glyphs.json. Change the component and this together, or the
assets drift from what the sites render.

    python3 wordmarks/generate.py

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
    "code": "#792b0b", "emu": "#0d4a7d", "asm": "#0f5631",
    "cat": "#562a8d", "build": "#60410c", "debug": "#85112d",
    "isa": "#0f5158", "forge": "#721a6e", "play": "#424e0c",
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
    print(f"{n} wordmarks written to {out}" + ("" if rsvg else " (no rsvg-convert: SVG only)"))
