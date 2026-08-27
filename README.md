# 198x-ui

Shared design tokens and Astro components for the 198x family sites — Asm198x,
Emu198x and Code198x.

One canonical copy, consumed by checkout, no registry. Same posture as
[`house-style`](https://github.com/stevehill1981/house-style), which does the
same job for prose. The two names differ for historical reasons and that is
deliberate — renaming `house-style` would churn nine pinned configs to fix
nothing, and the style inside it is called `House198x` either way.

## What is here

| | |
|---|---|
| `tokens.css` | Palette, dark tokens, the type roster, the nine project colours |
| `components/Plate.astro` | The family wordmark — `[ ASM \| 198x ]` |
| `components/SiteNav.astro` | Top-level navigation |
| `components/FamilyStrip.astro` | The footer family strip |
| `machines.json` | Machine → colour, for all 156 systems |
| `wordmarks/` | The nine plates as SVG and PNG, light and dark |
| `wordmarks/glyphs.json` | JetBrains Mono outlines, shared by `Plate.astro` and the generator |
| [`WORDMARK.md`](WORDMARK.md) | Wordmark spec — geometry, colours, and what not to do |

**Components, not layouts.** Shared components survive three sites diverging.
Shared layouts are how you end up unable to change one site without negotiating
with two others.

## Use it in a site

The consuming site fetches this repo into a gitignored `_198x-ui/` and imports
from it. One mechanism for local work and CI alike, so `npm run dev` needs no
workflow:

```jsonc
// package.json
"scripts": {
  "ui:fetch": "./scripts/fetch-ui.sh",   // clones or moves _198x-ui to the pinned tag
  "predev": "npm run ui:fetch",
  "prebuild": "npm run ui:fetch"
}
```

```jsonc
// tsconfig.json
"paths": { "@198x-ui/*": ["_198x-ui/*"] }
```

```astro
---
import '@198x-ui/tokens.css';
import SiteNav from '@198x-ui/components/SiteNav.astro';
---
<SiteNav
  prefix="asm"
  project="asm"
  version="0.0.15"
  items={[
    { label: 'Why', href: '/why' },
    { label: 'Install', href: '/install' },
    { label: 'Reference', href: '/reference', current: true },
  ]}
/>
```

`asm198x.github.io` carries a working `scripts/fetch-ui.sh` to copy.

Pin to a tag rather than tracking `main`. Without that, a change here can break
three sites at once with nothing in between to catch it.

## Ground tint

A site can carry its project colour as an ambient ground tint. Opt in from the
HTML, with the same project name the plate takes:

```astro
<html lang="en" data-tint="build">
```

That is the whole interface. The colour and both ceilings — 5% in light, 20% in
dark — resolve inside `tokens.css`, because a host that could set the strength
could exceed it, and the light ceiling is what keeps every derived ink valid on
the tinted ground. See `198x/decisions/family-visual-identity.md` §3b.

Two things it is not. It is not a licence for project colour anywhere else:
the tint works *because* it is ambient, and anything attached to an object — a
border, heading, link, rule or card accent — stays forbidden. And a fixed brand
colour is not covered by the ceiling, which protects derived ink only; check any
such colour on the tinted ground directly. That is how `--h-accent` was caught.

## Governance

Everything here is the concrete form of
`198x/decisions/family-visual-identity.md`. **Change the record first, then this
repo.** In particular:

- **Project colour appears in a plate cell and nowhere else.** Not a border, a
  heading, a link, a rule, or a card accent. Colour on these sites already means
  *machine*; a second meaning for the same signal is what the rule exists to
  prevent, and a reader cannot tell two colours apart by looking.
- **The plate frame is constant**, never the project colour. It is what makes
  nine fills of differing strength read as one set.
- **`--h-ink-faint` is decorative, never small informational text.** It measures
  2.27:1 on `--h-ground`, and darkening it far enough to carry copy turns it
  into `--h-ink-muted` — the tone that already does that job. The two cannot
  both be text colours.
- **Set text in `--h-accent-ink`, never `--h-accent`.** The plain accent is the
  fill: as small text it measures 4.07:1 on `--h-surface-light` and 4.52:1 on
  `--h-ground`. `--h-accent-ink` is whichever of the pair is readable on the
  current theme's ground, and it is the only one to put words in.
- **Three faces, three jobs.** Archivo for interface, Literata for reading and
  editorial display and all captions, JetBrains Mono for anything the machine
  said. A fourth face is a drift trigger, not a decision.

## About `machines.json`

Extracted from `Code198x/website/src/content/systems/*.yaml`, which remains the
source. Regenerate rather than hand-edit.

Two things to know before relying on it:

- **Colour is not a key.** 156 machines carry 139 distinct colours; twelve
  colours are shared by more than one machine, four machines on `#b22222` alone.
  It identifies character, not identity.
- **Some entries look like placeholders.** Several are CSS keyword colours —
  `firebrick`, `saddlebrown`, `darkred`, `royalblue` — which is unlikely to be
  anyone's considered choice of livery.

The colours here are the **declared** brand values. They are rarely what
renders: text and fills are derived from them against a contrast floor, and a
machine colour that fails AA is darkened until it passes. Never treat a value
here as the colour a reader will see, and never write a derived value down.
