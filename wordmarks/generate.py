#!/usr/bin/env python3
"""Generate the family wordmarks as SVG, one per project, light and dark.

Geometry mirrors components/Plate.astro exactly. Change the component and this
together, or the assets drift from what the sites render.

    python3 wordmarks/generate.py

The type is emitted as outlines, not as <text>. The plate geometry is computed
from JetBrains Mono's 600-unit advance, so a viewer without that font used to
get a fallback mono whose advance did not match a divider that does not move.
Outlines make the SVG self-contained: it renders identically everywhere, with
no font dependency and nothing to install.

GLYPHS below is the consequence -- the 21 characters the nine names need, in
JetBrains Mono Bold, as path data in font units. Outlining freezes the type
into the asset: a JetBrains Mono release no longer reflows the marks. That is
deliberate for a wordmark. To take a new version, re-extract with:

    from fontTools.ttLib import TTFont
    from fontTools.pens.svgPathPen import SVGPathPen
    f = TTFont("JetBrainsMono-Bold.ttf"); gs = f.getGlyphSet()
    pen = SVGPathPen(gs, ntos=lambda v: str(int(round(v))))
    gs[f.getBestCmap()[ord(ch)]].draw(pen); pen.getCommands()

fontTools is needed for that one-off step only. This script is stdlib.
"""
import pathlib

PROJECTS = {
    "code": "#792b0b", "emu": "#0d4a7d", "asm": "#0f5631",
    "cat": "#562a8d", "build": "#60410c", "debug": "#85112d",
    "isa": "#0f5158", "forge": "#721a6e", "play": "#424e0c",
}

UPEM = 1000          # JetBrains Mono units per em
ADV_UNITS = 600      # its advance, the 0.6em the geometry above assumes

# JetBrains Mono Bold, path data in font units. See the module docstring.
GLYPHS = {
    '1': "M84 0V113H274V609L83 469V609L251 730H399V113H552V0Z",
    '8': "M300 -10Q227 -10 171 18Q115 45 84 94Q53 142 53 206Q53 273 92 323Q130 373 192 386V388Q139 399 106 442Q74 485 74 544Q74 602 102 646Q131 690 182 715Q233 740 300 740Q367 740 418 715Q470 690 498 646Q527 602 527 544Q527 485 494 442Q461 399 408 388V386Q470 373 508 323Q547 273 547 206Q547 142 516 94Q485 45 429 18Q373 -10 300 -10ZM300 431Q347 431 376 460Q405 488 405 533Q405 579 376 608Q347 636 300 636Q253 636 224 608Q195 579 195 533Q195 488 224 460Q253 431 300 431ZM300 96Q355 96 390 128Q425 160 425 212Q425 265 390 298Q355 330 300 330Q245 330 210 298Q175 265 175 212Q175 160 210 128Q245 96 300 96Z",
    '9': "M175 0 346 295Q334 286 318 280Q302 273 270 273Q210 273 160 302Q111 331 82 382Q53 434 53 502Q53 574 84 628Q114 681 170 710Q225 740 300 740Q375 740 430 710Q486 680 516 626Q547 571 547 498Q547 455 528 400Q510 344 478 287L320 0ZM300 373Q356 373 390 408Q424 444 424 504Q424 563 390 598Q356 634 300 634Q244 634 210 598Q176 563 176 504Q176 444 210 408Q244 373 300 373Z",
    'A': "M35 0 219 730H380L565 0H437L397 177H203L163 0ZM226 279H374L330 475Q319 524 311 564Q303 603 300 621Q297 603 289 564Q281 524 270 476Z",
    'B': "M77 0V730H301Q406 730 468 679Q531 628 531 542Q531 482 496 439Q462 396 407 387V385Q448 380 480 356Q512 331 530 292Q548 254 548 208Q548 145 519 98Q490 51 437 26Q384 0 312 0ZM199 429H299Q348 429 377 456Q406 482 406 528Q406 573 378 600Q349 626 299 626H199ZM199 104H305Q360 104 392 134Q423 163 423 214Q423 265 392 296Q360 328 305 328H199Z",
    'C': "M308 -10Q237 -10 185 16Q133 43 104 92Q76 140 76 206V524Q76 590 104 638Q133 687 185 714Q237 740 308 740Q378 740 430 714Q482 687 511 638Q540 590 540 524H414Q414 575 386 602Q359 630 308 630Q257 630 229 602Q201 575 201 524V206Q201 155 229 128Q257 100 308 100Q359 100 386 128Q414 155 414 206H540Q540 140 511 92Q482 43 430 16Q378 -10 308 -10Z",
    'D': "M75 0V730H292Q366 730 420 702Q475 673 505 622Q535 571 535 502V229Q535 160 505 108Q475 57 420 28Q366 0 292 0ZM200 112H292Q346 112 378 144Q410 175 410 229V502Q410 555 378 586Q346 618 292 618H200Z",
    'E': "M88 0V730H526V620H211V430H491V324H211V110H526V0Z",
    'F': "M80 0V730H534V614H203V419H508V303H205V0Z",
    'G': "M304 -10Q233 -10 181 16Q129 43 100 92Q72 140 72 206V524Q72 590 100 638Q129 687 181 714Q233 740 304 740Q374 740 426 714Q478 687 507 638Q536 590 536 524H410Q410 575 382 602Q355 630 304 630Q253 630 225 603Q197 576 197 525V206Q197 155 225 127Q253 99 304 99Q355 99 382 127Q410 155 410 206V287H286V395H536V206Q536 140 507 92Q478 43 426 16Q374 -10 304 -10Z",
    'I': "M90 0V113H237V617H90V730H510V617H363V113H510V0Z",
    'L': "M121 0V730H246V113H556V0Z",
    'M': "M54 0V730H217L299 416L382 730H546V0H429V307Q429 370 432 438Q436 505 441 568Q446 632 452 684L349 317H246L147 675Q156 606 164 510Q171 415 171 307V0Z",
    'O': "M300 -10Q195 -10 134 50Q72 110 72 216V514Q72 620 134 680Q195 740 300 740Q405 740 466 680Q528 620 528 515V216Q528 110 466 50Q405 -10 300 -10ZM300 100Q351 100 377 128Q403 155 403 206V524Q403 575 377 602Q351 630 300 630Q249 630 223 602Q197 575 197 524V206Q197 155 223 128Q249 100 300 100Z",
    'P': "M77 0V730H320Q393 730 448 702Q502 674 532 624Q562 573 562 505Q562 437 532 386Q502 336 448 308Q393 280 320 280H202V0ZM202 390H320Q373 390 404 422Q435 454 435 505Q435 556 404 588Q373 620 320 620H202Z",
    'R': "M77 0V730H307Q380 730 434 703Q487 676 517 628Q547 579 547 513Q547 440 511 386Q475 331 414 308L557 0H420L292 290H201V0ZM201 400H307Q360 400 390 429Q420 458 420 509Q420 560 390 590Q359 620 307 620H201Z",
    'S': "M303 -10Q229 -10 174 16Q118 42 88 90Q57 139 57 206H180Q180 157 214 128Q247 99 303 99Q357 99 388 128Q420 156 420 204Q420 240 400 268Q379 295 341 305L243 330Q164 350 118 405Q72 460 72 536Q72 629 133 684Q194 740 296 740Q365 740 416 715Q468 690 496 644Q524 599 524 538H402Q402 580 373 606Q344 632 296 632Q249 632 222 606Q194 581 194 540Q194 506 214 484Q233 462 268 452L369 427Q450 407 496 347Q543 287 543 204Q543 139 514 91Q484 43 430 16Q376 -10 303 -10Z",
    'T': "M237 0V617H46V730H554V617H363V0Z",
    'U': "M300 -10Q193 -10 132 48Q72 107 72 208V730H198V209Q198 157 224 128Q250 99 300 99Q349 99 376 128Q402 157 402 209V730H528V208Q528 107 468 48Q408 -10 300 -10Z",
    'Y': "M237 0V265L23 730H155L268 477Q281 447 290 418Q299 389 302 373Q306 389 314 418Q323 447 336 477L447 730H577L363 265V0Z",
    'x': "M36 0 228 284 49 550H190L275 415Q283 403 290 388Q297 373 300 364Q304 373 310 388Q317 403 325 415L410 550H552L373 284L564 0H422L327 151Q319 163 312 178Q304 194 300 203Q296 194 289 178Q282 163 274 151L178 0Z",
}

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
