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
A proportional face makes nine plates look like nine unrelated marks.

**The frame is constant.** House brown `#3a2c1f` on light, paper `#efe7d6` on
dark — never the project colour. It is what makes nine fills of differing
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

## Colours

The fill is the project's, at `oklch(0.40 <chroma> <hue>)` — equal lightness is
the cohering rule, chroma runs to the sRGB gamut edge per hue.

| Project | Fill | Project | Fill |
|---|---|---|---|
| Code198x | `#792b0b` | Debug198x | `#85112d` |
| Emu198x | `#0d4a7d` | Isa198x | `#0f5158` |
| Asm198x | `#0f5631` | Forge198x | `#721a6e` |
| Cat198x | `#562a8d` | Play198x | `#424e0c` |
| Build198x | `#60410c` | | |

Prefix text is `#faf8f2` on the fill. The `198x` cell is `#fdfcf7` with
`#3a2c1f` text on light, `#242019` with `#efe7d6` on dark.

**Shadow on light grounds only**: `0 1px 2px rgba(58,44,31,0.20), 0 3px 8px
rgba(58,44,31,0.10)`. On a dark ground a drop shadow reads as dirt, not lift.

## Ready-made assets

`wordmarks/` carries all nine, light and dark, as SVG and PNG:

```
wordmarks/asm198x-light.svg   wordmarks/asm198x-light.png
wordmarks/asm198x-dark.svg    wordmarks/asm198x-dark.png
```

**Prefer the PNG where you do not control the fonts.** The SVG sets its type in
JetBrains Mono; a viewer without it gets a fallback mono and the geometry no
longer matches. GitHub READMEs are the common case.

Regenerate with `python3 wordmarks/generate.py`. The geometry there mirrors
`Plate.astro` — change both together or the assets drift from what the sites
render.

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
- **Give a new sibling a colour outside `oklch(0.40 … …)`** because the set
  needs something brighter. Add a hue; keep the lightness.
- **Link a site to itself** in the family strip. It takes its list as a prop.
