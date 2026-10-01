# Fonts — the House198x roster, self-hosted

The three faces §4 of `family-visual-identity.md` names, served from this repo
rather than a CDN.

| Family | Role | Licence |
|---|---|---|
| Nebula Sans | interface, headings, the slogan | SIL OFL 1.1 |
| Fira Sans Condensed (Heavy Italic, 900) | the magazine voice: masthead, pull quote, stat box, teaser | SIL OFL 1.1 |
| JetBrains Mono | code, data, plates | SIL OFL 1.1 |

All three permit redistribution, so these files are committed. The OFL asks only
that the licence travels with the fonts — that is what the `.txt` files are for
— and requires no visible credit.

## Why they moved here

The consuming sites each carried a Google Fonts `<link>` for Archivo, Literata
and JetBrains Mono. When Archivo was retired for having no Cyrillic, its
replacement broke that arrangement: **Nebula Sans is not on Google Fonts**, so
the CDN link could no longer deliver the interface face at all.

Rather than have five sites each solve that differently, the roster lives where
the decision lives. One copy, one place to change it, and no third-party request
from any site — which also removes the CDN the family had been quietly relying
on for a set of faces it self-hosts everywhere else.

## Use

```astro
import '@198x-ui/tokens.css';
import '@198x-ui/fonts.css';
```

The URLs are absolute (`/fonts/…`), so the directory has to be served at
`/fonts/`. In Astro, copy it into `public/` at build time, or symlink it. A host
that mounts it elsewhere should override the `src` URLs rather than edit
`fonts.css`.

## Coverage

| Family | Latin | Latin Ext | Greek | Cyrillic | CJK |
|---|---|---|---|---|---|
| Nebula Sans | full | full | 88/144 (the italic lacks Δ, U+0394) | 156/256 | — |
| Fira Sans Condensed (Heavy Italic) | full | full | 121/144 | 100/256 | — |
| JetBrains Mono | full | full | 79/144 | 122/256 | — |

All three cover the scripts the family's scope needs, which is the point: a
heading naming a Soviet or Bulgarian machine sets in the house face rather than
the viewer's. **None covers CJK.** If the curriculum reaches the Japanese MSX
scene or Sharp's machines, that is a further decision and a much larger
download.

Fira counts are glyphs in the kit's subsets inside U+0370-03FF and U+0400-04FF:
`python3 -c "from fontTools.ttLib import TTFont; c=TTFont('fonts/fira-sans-condensed-900-italic-greek.woff2').getBestCmap(); print(sum(0x370<=x<=0x3ff for x in c))"`
(Cyrillic file, `0x400<=x<=0x4ff`). The Nebula italic Δ gap is recorded in
`KNOWN_GAPS` in `scripts/check_fonts.py`.

Split by `unicode-range`, so a Latin page fetches only the Latin cuts and other
scripts arrive only when a page uses them.

## Regenerating

Subsets of upstream releases, taken from the designers' own repositories:

- Nebula Sans — <https://www.nebulasans.com> (1.010)
- Fira Sans Condensed Heavy Italic — <https://github.com/bBoxType/FiraSans> (release 4.3, pinned at commit `f54eeb3124c63fe9b5bcd36d09d1cd46788cd15e`; `Fira_Sans_4_3/Fonts/Fira_Sans_TTF_4301/Condensed/Italic/FiraSansCondensed-HeavyItalic.ttf`, licence `OFL.txt` at the same commit). The font declares usWeightClass 900; `fonts.css` declares weight 900 italic. Subset with `python3 scripts/subset_font.py SRC fira-sans-condensed 900 italic`; `python3 scripts/check_fonts.py` verifies every face
- JetBrains Mono — <https://github.com/JetBrains/JetBrainsMono> (2.304)

Subsetting for web use is permitted under the OFL and does not trigger the
Reserved Font Name rename requirement.
