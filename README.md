# 198x-ui

Shared design tokens and Astro components for the 198x family sites — Asm198x,
Build198x, Cat198x, Debug198x, Emu198x, Format198x, Play198x and Code198x.

One canonical copy, consumed by checkout, no registry. Same posture as
[`house-style`](https://github.com/stevehill1981/house-style), which does the
same job for prose. The two names differ for historical reasons and that is
deliberate — renaming `house-style` would churn nine pinned configs to fix
nothing, and the style inside it is called `House198x` either way.

## What is here

| | |
|---|---|
| `tokens.css` | Palette (dark leads, light follows), the type roster, the eleven project colours |
| `components/Plate.astro` | The family wordmark — `[ ASM \| 198x ]` |
| `components/SiteNav.astro` | Top-level navigation |
| `components/FamilyStrip.astro` | The footer family strip |
| `components/Screen.astro` | One capture, at a whole multiple of its true grid |
| `components/Button.astro` | Primary, secondary and quiet; a link or a button; the arrow in its own cell |
| `components/Eyebrow.astro` | The small boxed uppercase label |
| `components/Shell.astro` | The double bezel: `device` (an object, rounded) or interface (square) |
| `components/ThemeToggle.astro` | Auto / Light / Dark, with `ThemeBoot.astro` for the document head |
| `components/Tabs.astro` | Accessible tabs, or a segmented control without panels |
| `components/Listing.astro` | Program listings: syntax colour, line numbers, keyboard-reachable scrolling |
| `components/Kbd.astro` | A keycap, or a combination as separate caps |
| `components/Tile.astro` | A door into a site: the site's glyph, a name, one line, the arrow in its cell |
| `components/Figure.astro` | A capture (through Screen) or a photograph, with a Literata italic caption |
| `components/Breadcrumbs.astro` | The trail above a page, the current page marked for screen readers |
| `components/Chip.astro` | A square label, link, or filter toggle (`aria-pressed`, inverse when on) |
| `components/SearchField.astro` | A labelled search landmark with an optional key hint; the site does the searching |
| `components/Loading.astro` | What each machine showed while it loaded, from `loading-looks.ts`, every value sourced |
| `catalogue/` | Every component in its variants, for a site to mount in development |
| `machines.json` | Machine → colour, for all 156 systems |
| `wordmarks/` | The eleven plates as SVG and PNG, light and dark |
| `wordmarks/glyphs.json` | JetBrains Mono outlines, shared by `Plate.astro` and the generator |
| `fonts.css`, `fonts/` | The three house faces, self-hosted and range-split |
| [`WORDMARK.md`](WORDMARK.md) | Wordmark spec — geometry, colours, and what not to do |
| [`AGENTS.md`](AGENTS.md) | How to work on the kit — verification, governance, release |

**Components, not layouts.** Shared components survive sites diverging. Shared
layouts are how you end up unable to change one site without negotiating with
every other.

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
every site at once with nothing in between to catch it.

## Screen

A capture, shown as the machine showed it (`family-visual-identity.md` §7):

```astro
---
import Screen from '@198x-ui/components/Screen.astro';
---
<Screen src="/images/…/step-02.png" alt="The Spectrum after RUN: Hello, then 0 OK." width={352} height={296} />
<Screen src="/images/…/signal.png" alt="Signal on an Amiga 500." width={640} height={512} grid={{ w: 320, h: 256 }} />
<Screen src="/images/…/dash.png" alt="Dash on an NTSC NES." width={256} height={240} maxScale={2} />
```

It renders at a whole multiple of the true grid, never a fraction, and only a
cell narrower than the grid at 1x (a phone) scales it down. A capture stored
with every column or row doubled is detected and halved. The Amiga cannot be
detected, because its pixels do not always pair up, so it declares its grid.
With `crt` on (the default) there is one scanline per source line, drawn in
whole device pixels, a gentle falloff and a faint bloom. A line has to cover at
least two device pixels to hold a dark band, so scanlines are off at 1x on a 1x
display and at a fractional fallback scale; they follow page zoom. The bloom is a separate blurred copy
of the capture, so the capture itself is never filtered or tinted. `crt={false}`
leaves the capture in its bezel and nothing else.

`alt` is required. An empty one throws unless you also pass `decorative`,
because a capture is evidence and usually needs describing. The component file
header documents every prop.

The fitting runs in the browser, once per page however many screens it holds.
Detection reads the pixels, so a capture has to be same-origin. A site that adds
screens after load calls `window.fitScreens()`.

## Loading

A loading state shows what *that* machine showed while it was busy, quoted from
a source, never borrowed from another machine (`family-visual-identity.md` §7):

```astro
---
import Loading from '@198x-ui/components/Loading.astro';
---
<Loading machine="sinclair-zx-spectrum" />
<Loading machine="commodore-64" media="disk" label="Loading Bricks…" />
<Loading machine="commodore-amiga" />
<Loading machine="nintendo-entertainment-system" />   <!-- renders nothing: a cartridge never loaded -->
```

Each machine's look is data in `components/loading-looks.ts`, with the source
of every colour, band height and message beside it. A machine with no entry
fails the build: there is no default look, because a default would be another
machine's. To add one, find what its stock loader put on screen in a primary
source or an Emu198x capture of an official ROM, and cite it there.

Whatever the machine printed is a real Emu198x capture in
`components/loading-captures/`, shown at whole multiples of its grid by the same
rule as `Screen`; never text set in a font. What changed too fast to capture
(the Spectrum's border stripes, the C64's blanked screen, the Amiga's greys) is
drawn in the same box. Every capture is of a program called `GAME`, so there is
no `name` prop: passing one fails the build. Say what is really loading in
`label`. The scripts and media that make the captures are in
`loading-captures/source/`, and `loading-looks.ts` says how each was made.

The root is `role="status"`; the picture is aria-hidden. Sequences play once
and hold the busy state; under `prefers-reduced-motion: reduce` that state is
one still frame. The Spectrum's stripes drift slower than the machine's, so no
point flashes more than twice a second (WCAG 2.3.1); the file says why.

## The catalogue

`catalogue/Catalogue.astro` shows every component in its variants, each with
the call that produces it and the rule it embodies. It has a Light/Dark switch
and width presets of 390, 768, 1280 and full. Each entry sits in a resizable
frame, which is an `<iframe>` so that a 390-pixel frame really is a 390-pixel
viewport and the components' media queries fire.

The kit cannot run it, so a site mounts it on a route that exists only in
development:

```astro
---
// src/pages/catalogue/[...slug].astro
import '@198x-ui/tokens.css';
import '@198x-ui/fonts.css';
import Catalogue from '@198x-ui/catalogue/Catalogue.astro';
import { catalogueEntries } from '@198x-ui/catalogue/entries';

export function getStaticPaths() {
  if (import.meta.env.PROD) return [];   // nothing reaches dist/
  return [{ params: { slug: undefined } },
          ...catalogueEntries.map((e) => ({ params: { slug: e.slug } }))];
}
const { slug } = Astro.params;
---
<html lang="en-GB">
  <head><meta charset="UTF-8" /><meta name="robots" content="noindex" /><title>198x-ui catalogue</title></head>
  <body><Catalogue base="/catalogue" entry={slug} /></body>
</html>
```

The kit ships no images. The Screen entry shows captures by URL, and the
defaults in `catalogue/samples.ts` are files `code198x.com` serves: a Spectrum
screen, the column-doubled BBC Micro poster, an Amiga screen stored at 640x512
and an NES screen. Any other site passes its own set as `samples`, with the same
shapes, because each one is there to prove one of Screen's rules.

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
  eleven fills of differing strength read as one set.
- **`--h-ink-faint` is decorative, never small informational text.** It measures
  2.31:1 on the light page, and darkening it far enough to carry copy turns it
  into `--h-ink-muted` — the tone that already does that job. The two cannot
  both be text colours.
- **Set text in `--h-accent-ink`, never `--h-accent`.** The plain accent is the
  fill: as small text it measures 4.30:1 on the light page. `--h-accent-ink` is
  the accent at ink strength in each theme, and it is the only one to put words
  in. Text *on* the fill is `--h-ink-on-accent`.
- **Dark leads.** Dark is the default; light follows `prefers-color-scheme` or
  an explicit `data-theme="light"`, and `data-theme="dark"` forces dark (§7).
  The Auto/Light/Dark toggle is the site's: it sets or clears `data-theme`.
- **Three faces, three jobs.** Nebula Sans for interface, Literata for reading and
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

## Licence

MIT — see [`LICENSE`](LICENSE). That is the content side of
`198x/decisions/how-198x-licenses-its-own-work.md`: this is a presentation kit
for the family's own sites, not a shipped tool, and nothing in it derives from a
GPL source.

Two carve-outs, both in `LICENSE`. **`fonts/` is not ours** — Nebula Sans,
Literata and JetBrains Mono are redistributed under the SIL OFL 1.1, and the
licence has to travel with them if you redistribute them further. And MIT grants
copyright, not trade marks: use the plate to say *this is a 198x site*, not to
badge something unaffiliated.

The capture PNGs in `components/loading-captures/` are screenshots of the
machines, made in Emu198x, not code of ours, and MIT does not cover them. They
stand where the lesson screenshots on the family sites stand: output, not ROMs
(`198x/decisions/system-rom-sourcing.md`). No ROM, character set or font is in
this repo.
