# The 198x wordmark

**If you are building a page, use the component** — `components/Plate.astro`.
Everything below is for cases it cannot serve: a raster for a README, an icon,
a social card, a slide, something not built in Astro.

Governed by `198x/decisions/family-visual-identity.md`. That record is the
authority; this file is how to apply it.

## The construction

Two cells with a full-height rule between them. The prefix varies; `198x` never
does.

```
[ ASM | 198x ]      [ DEBUG | 198x ]      [ CAT | 198x ]
```

Set in **JetBrains Mono, weight 700**. The monospace is load-bearing rather
than stylistic: it puts every cell on the same rhythm, so a three-character
prefix and a five-character one differ in width without looking inconsistent.
A proportional face makes eleven plates look like eleven unrelated marks.

Load-bearing in a literal sense too: the plate geometry is computed from the
face's 600-unit advance, and the divider is placed at a fixed offset. That is
why the ready-made assets carry the type as **outlines rather than live text** —
a substituted mono has a different advance, and the divider does not move to
meet it.

**The frame is constant.** House brown `#3a2c1f` on light, paper `#efe7d6` on
dark — never the project colour. It is what makes eleven fills of differing
strength read as one set, and it does more work than the fill does.

## Geometry

Proportional to the cell type size `F`. At `F = 14px` these are the component's
literal values.

| | |
|---|---|
| Horizontal padding | `0.6em` each side of each cell |
| Vertical padding | `0.34em` |
| Frame and divider | `2px` at `F = 14`, i.e. `F / 7` |
| Corner radius | `3px` at `F = 14` |
| Letter-spacing | `-0.01em` |
| Vertical alignment | cap-height band centred in the cell |

**The type is centred on cap height, not sat on a text baseline.** The names are
uppercase and the suffix is digits, so nothing descends. A text baseline leaves
`0.34em` above the caps and `0.59em` below them — the type rides high by
`0.125em`, which is 6px on a 48px plate. Centring the cap band puts `0.475em`
on both sides.

Centred on cap height rather than on each name's own ink, so all eleven sit on
one baseline: `Q`'s tail or a round glyph's overshoot must not shift a plate
relative to its siblings.

## Colours

The fill is the project's, at `oklch(0.50 <chroma> <hue>)` — equal lightness is
the cohering rule, chroma runs to the sRGB gamut edge per hue.

| Project | Fill | Project | Fill |
|---|---|---|---|
| Code198x | `#a93800` | Debug198x | `#b9003c` |
| Emu198x | `#0066af` | Isa198x | `#00717b` |
| Asm198x | `#007742` | Forge198x | `#a4009e` |
| Cat198x | `#8000e0` | Play198x | `#5b6c00` |
| Build198x | `#865900` | Format198x | `#007465` |
| | | Studio198x | `#482aff` |

Prefix text is `#faf8f2` on the fill, where it measures 5.3–6.6:1. The `198x`
cell is `#fdfcf7` with `#3a2c1f` text on light, `#242019` with `#efe7d6` on
dark.

**Shadow on light grounds only**: `0 1px 2px rgba(58,44,31,0.20), 0 3px 8px
rgba(58,44,31,0.10)`. On a dark ground a drop shadow reads as dirt, not lift.

## Ready-made assets

`wordmarks/` carries all eleven, light and dark, as SVG and PNG:

```
wordmarks/asm198x-light.svg   wordmarks/asm198x-light.png
wordmarks/asm198x-dark.svg    wordmarks/asm198x-dark.png
```

**Use the SVG anywhere.** It carries its own outlines, so it needs no font
installed and renders identically everywhere — GitHub READMEs included, which
used to be the case that forced the PNG. The PNG remains for the places that
cannot take an SVG at all: some mail clients, some social-card scrapers.

The type is not selectable in the SVG, which for a wordmark is the intent
rather than a cost — `ASM198x` should not land in someone's copy of the page.
`role="img"` and the `<title>` carry the name to a screen reader either way.

Regenerate with `python3 wordmarks/generate.py`. The geometry there mirrors
`Plate.astro` — change both together or the assets drift from what the sites
render. Both read their outlines from `wordmarks/glyphs.json`, so the glyphs
themselves cannot drift; it is the geometry constants that need keeping in step.

## Four renderings

| Rendering | Use |
|---|---|
| **Outlined** | Site headers, and anywhere over an unknown background. The default. |
| **Filled** | Where the plate must hold alone; the divider reverses to paper so it survives inside the fill. |
| **Stacked** — `19` over `8x` | Near-square. App icons, avatars, favicons. |
| **Typed** — `[ asm \| 198x ]` | READMEs, commit bodies, terminal banners. The mark degrades to plain text without becoming a different thing. |

Compact use: the stacked cell holds to about 36px, closes up by 24px, and drops
to the wildcard `x` alone at 16px.

## Do not

- **Put the project colour anywhere but a plate cell.** Not a border, a
  heading, a link, a rule, or a card accent. Colour on these sites already
  means *machine*; a second meaning for the same signal is what the rule exists
  to prevent, and a reader cannot tell two colours apart by looking.
- **Colour the frame.** It is constant by design.
- **Colour the `198x` cell**, or let it vary between siblings in any way.
- **Set it in a proportional face** because it looks tidier.
- **Give a new sibling a colour outside `oklch(0.50 … …)`** because the set
  needs something brighter. Add a hue; keep the lightness. `0.50` is a ceiling,
  not a preference — above it the cell's paper ink stops clearing 4.5:1 on the
  worst hue of the set.
- **Link a site to itself** in the family strip. It takes its list as a prop.
