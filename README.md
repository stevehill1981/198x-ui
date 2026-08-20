# 198x-ui

Shared design tokens and Astro components for the 198x family sites — Asm198x,
Emu198x and Code198x.

One canonical copy, consumed by checkout, no registry. Same posture as
[`house-style`](https://github.com/stevehill1981/house-style), which does the
same job for prose.

## What is here

| | |
|---|---|
| `tokens.css` | Palette, dark tokens, the type roster, the nine project colours |
| `components/Plate.astro` | The family wordmark — `[ ASM \| 198x ]` |
| `components/SiteNav.astro` | Top-level navigation |
| `components/FamilyStrip.astro` | The footer family strip |
| `machines.json` | Machine → colour, for all 156 systems |

**Components, not layouts.** Shared components survive three sites diverging.
Shared layouts are how you end up unable to change one site without negotiating
with two others.

## Use it in a site

The consuming site checks this repo out during its build and imports from the
checkout, pinned to a tag:

```yaml
- name: Check out house-ui
  uses: actions/checkout@v7
  with:
    repository: stevehill1981/198x-ui
    ref: v0.1.0
    path: _198x-ui
```

```astro
---
import SiteNav from '../../_198x-ui/components/SiteNav.astro';
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

Pin to a tag rather than tracking `main`. Without that, a change here can break
three sites at once with nothing in between to catch it.

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
