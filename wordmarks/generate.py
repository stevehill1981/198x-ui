#!/usr/bin/env python3
"""Generate the family wordmarks as SVG, one per project, light and dark.

Geometry mirrors components/Plate.astro exactly. Change the component and this
together, or the assets drift from what the sites render.

    python3 wordmarks/generate.py
"""
import pathlib

PROJECTS = {
    "code": "#792b0b", "emu": "#0d4a7d", "asm": "#0f5631",
    "cat": "#562a8d", "build": "#60410c", "debug": "#85112d",
    "isa": "#0f5158", "forge": "#721a6e", "play": "#424e0c",
}

F = 48.0            # cell type size
ADV = 0.6 * F       # JetBrains Mono advance width
PAD_X = 0.6 * F     # matches padding: … 0.6em
PAD_Y = 0.34 * F    # matches padding: 0.34em …
STROKE = 2.0 / 14.0 * F   # the component's 2px border at font-size 14
RADIUS = 3.0 / 14.0 * F

THEMES = {
    "light": {"frame": "#3a2c1f", "cell": "#fdfcf7", "ink": "#3a2c1f", "fill_ink": "#faf8f2"},
    "dark":  {"frame": "#efe7d6", "cell": "#242019", "ink": "#efe7d6", "fill_ink": "#faf8f2"},
}


def plate(prefix: str, fill: str, theme: dict) -> str:
    left, right = prefix.upper(), "198x"
    w_l = len(left) * ADV + 2 * PAD_X
    w_r = len(right) * ADV + 2 * PAD_X
    h = F + 2 * PAD_Y
    w = w_l + w_r + STROKE          # one shared divider line
    ow, oh = w + STROKE, h + STROKE  # room for the outer stroke
    o = STROKE / 2
    baseline = o + PAD_Y + F * 0.74  # cap height sits ~0.74em below the top
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
    <g font-family="JetBrains Mono, ui-monospace, monospace" font-size="{F:.1f}" font-weight="700"
       letter-spacing="{-0.01 * F:.2f}">
      <text x="{o + PAD_X:.1f}" y="{baseline:.1f}" fill="{theme['fill_ink']}">{left}</text>
      <text x="{o + w_l + STROKE + PAD_X:.1f}" y="{baseline:.1f}" fill="{theme['ink']}">{right}</text>
    </g>
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
            # PNG as well: the SVG sets the type in JetBrains Mono, which a
            # viewer may not have. A raster always looks right.
            if rsvg:
                subprocess.run(
                    [rsvg, "-w", "600", str(svg), "-o", str(svg.with_suffix(".png"))],
                    check=True,
                )
    print(f"{n} wordmarks written to {out}" + ("" if rsvg else " (no rsvg-convert: SVG only)"))
