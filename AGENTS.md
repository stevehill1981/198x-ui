# 198x-ui — agent context

Shared design tokens and Astro components for the 198x family sites. Human
documentation is [`README.md`](README.md) and [`WORDMARK.md`](WORDMARK.md);
this file is the operational context for working *on* the kit.

This repo sits beside the family umbrella rather than inside it — it is
`stevehill1981/198x-ui`, not a `*198x` org repo, the same posture as
[`house-style`](https://github.com/stevehill1981/house-style). It is still bound
by the umbrella's decisions, which live in `~/Projects/198x/decisions/`.

## The one thing to understand first

**Nothing in this repo builds, runs, or tests.** There is no `package.json`, no
CI, no test suite. It is consumed by *checkout*: each site clones this repo into
a gitignored `_198x-ui/` at a pinned tag and imports from it.

Two consequences, and they are the whole shape of working here:

- **A change is unverified until a consuming site builds against it.** "It looks
  right" is the entire feedback loop this repo offers on its own. Use the recipe
  below instead.
- **A change moves every site at once, on their next pin bump.** There is no
  intermediate place for a mistake to be caught. That is why sites pin tags
  rather than tracking `main`.

## Verifying a change

Build a real consuming site against your working copy. `play198x.github.io` is
the cheapest — one route, and it carries the family's accessibility gate:

```bash
SITE=~/Projects/198x/Play198x/play198x.github.io
WORK=$(mktemp -d)
rsync -a --exclude node_modules --exclude dist --exclude _198x-ui --exclude .git "$SITE/" "$WORK/"
ln -s "$SITE/node_modules" "$WORK/node_modules"
rsync -a --exclude .git ~/Projects/198x-ui/ "$WORK/_198x-ui/"   # your working copy

cd "$WORK"
npx astro build            # not `npm run build` — its prebuild would overwrite _198x-ui
node scripts/a11y-sweep.mjs
```

`a11y-sweep.mjs` runs axe over every built route in **both themes** and exits
non-zero on anything serious or critical. Half this family's contrast defects
exist in only one theme, which is why it sweeps both. It needs Chromium:
`npx playwright install chromium` once.

**Reproduce the defect before fixing it.** Point `_198x-ui/` at the pre-fix
component, confirm the sweep fails, then swap in the fix and confirm it passes.
A gate that was never seen red has measured nothing.

### The catalogue is the other half of the recipe

The sweep proves a change breaks nothing; it does not show you the change.
`catalogue/` does. Mount it in a site worktree (see README, "The catalogue";
Code198x/website carries the route at `src/pages/catalogue/[...slug].astro`),
point that site's `_198x-ui` at your working copy with a symlink, and run
`npx astro dev`, not `npm run dev`: `predev` runs `ui:fetch`, which replaces a
symlink with a fresh clone at the pinned tag. Copy `fonts/` into the site's
`public/fonts` yourself, since `ui:fetch` is what normally does it.

A new component gets an entry in the same change: a file in
`catalogue/entries/`, a line in `catalogue/entries.ts` and one in the map in
`Catalogue.astro`. Show every variant the props allow, and say in each note
which section of the record it embodies.

The route is development-only, so check it stays that way: `astro build` should
leave no `catalogue/` in `dist/`.

## Governance — the record comes first

Everything here is the concrete form of
`~/Projects/198x/decisions/family-visual-identity.md`. **Change the record
first, then this repo.**

The rule has been kept: on 2026-08-27 the palette moved to `L 0.50` and grew to
eleven colours in the record at 15:53 and 16:33, and in this repo at 15:53 and
16:34 — record first, kit within the minute, both times.

**But check which branch you are reading it on.** Those four record commits
landed on a local branch in the umbrella repo, not on `main`, and were never
merged or pushed. `main`'s copy of the record is four commits stale and still
describes the `L 0.40`, nine-colour palette. Read from `main` alone and this kit
looks like it went rogue; it did not. Verify a claim *about* the record against
the record, and verify the record against the branch that actually carries it:

```bash
git -C ~/Projects/198x log --all --oneline -- decisions/family-visual-identity.md
```

`--all` is the load-bearing flag. Without it the four newest commits are
invisible.

### The palette lives in four places

A project colour has to be changed in all of them together, or they drift:

| Where | What it holds |
|---|---|
| `decisions/family-visual-identity.md` §2 (umbrella) | **The binding values.** Hex plus `oklch()`. |
| `tokens.css` | `--h-project-*`, and a `[data-tint="…"]` rule per project |
| `wordmarks/generate.py` | `PROJECTS`, for the rendered assets |
| `WORDMARK.md` | The table humans read |

Plus two TypeScript unions that must list the same names —
`Project` in `components/Plate.astro` and `project?` in
`components/SiteNav.astro`. A name missing from the latter is a nav a sibling
cannot colour; that is exactly how Format198x and Studio198x were half-added.

After changing a colour, re-render: `python3 wordmarks/generate.py` (PNGs need
`rsvg-convert`; without it you get SVG only, silently).

### The rules that bite

Digested from the record and `README.md`; the record is the authority.

- **Project colour appears in a plate cell and nowhere else** — not a border,
  heading, link, rule or card accent. Colour on these sites already means
  *machine*. The one exception is the ambient ground tint, which works precisely
  because it is under everything equally and so labels nothing.
- **The plate frame is constant house brown**, never the project colour. It is
  what makes fills of very different strength read as one set.
- **`--h-ink-faint` is decorative.** 2.27:1 on `--h-ground`; never small text.
- **Set text in `--h-accent-ink`, never `--h-accent`.** The plain accent is the
  fill and fails AA as small text on the family's own grounds.
- **Three faces, three jobs.** A fourth face is a drift trigger, not a decision.
- **Tint ceilings are derived, not chosen** — 5% light, 20% dark. They are
  resolved inside `tokens.css` so a host cannot exceed them. Re-derive both if
  the palette lightness moves again.

## Screen measures itself

`components/Screen.astro` is the one component with a script, because the true
grid and the space a screen has are only known in the browser. The rules it
holds (§7) are easy to break by accident while tidying its CSS:

- **Width comes from the script, never from the stylesheet.** Anything that
  sizes `.h-screen` to its container (`width: 100%`, `flex: 1`, a grid track that
  stretches it) makes the scale fractional. Resize the box around it, not the
  screen.
- **Nothing goes on the capture.** Scanlines and falloff are pseudo-elements and
  the bloom is a second `<img>` with `alt=""` and `aria-hidden`. A `filter`, blend
  mode or opacity on `.h-screen-img` is a breach of §7, whatever it looks like.
- **The bezel is dark in both themes.** It is hardware; its colours are the
  `--h-screen-*` tokens, single values rather than `light-dark()` pairs.

Verify a Screen change by measuring, not looking: in the catalogue each screen's
rendered size must be the grid times a whole k, and its `::before`
`background-size` must be `100% kpx`. The Screen entry prints the grid, k and
rendered size under each screen; read the scanline size from devtools.

## Plate geometry is mirrored, not shared

`components/Plate.astro` and `wordmarks/generate.py` compute the same plate
independently — one in TypeScript for the sites, one in Python for the assets.
Both read their outlines from `wordmarks/glyphs.json`, so the *glyphs* cannot
drift; the geometry constants can. **Change both together.**

The type is emitted as outlines rather than live text on purpose: the geometry
is computed from JetBrains Mono's 600-unit advance and the divider sits at a
fixed offset, so a fallback mono would put the type and the divider in different
places.

## Accessibility

The gate is downstream, so defects here surface as failures on somebody else's
site — and get worked around there rather than fixed here. Both halves of that
are worth watching for.

The instructive case: an unlinked `Plate` rendered a bare `<span>` carrying
`aria-label`. `aria-label` only names elements whose role supports naming, so
the wordmark was not mislabelled — it was **absent from the accessibility tree**,
with both inner runs `aria-hidden`. Three sites had independently passed
`href="/"` to dodge it, turning a wordmark into a self-link to satisfy a gate.
Fixed by giving the unlinked case `role="img"`.

When a site works around a kit defect, fix the kit and revert the workaround.

## Releasing

1. Commit here.
2. Annotated tag, `vMAJOR.MINOR.PATCH`, subject in the house form —
   `v0.5.0 — the roster, self-hosted`.
3. Push the tag.
4. Bump `UI_REF` in each consuming site's `scripts/fetch-ui.sh`, one site at a
   time, building each. Sites are deliberately free to sit on older tags.

Current pins drift by design — check them before assuming a site has your change:

```bash
grep -rn 'REF:-' ~/Projects/198x/*/*198x.github.io/scripts/fetch-ui.sh
```

## About `machines.json`

Generated from `Code198x/website/src/content/systems/*.yaml`, which remains the
source — regenerate rather than hand-edit. Colour is **not** a key: 156 machines
carry 139 distinct colours. The values are *declared* brand colours, not what
renders; rendered inks are derived against a contrast floor. Never write a
derived value back into this file.
