// Every component and catalogue style block sits in the `kit-components`
// cascade layer (AGENTS.md, "Component styles live in @layer
// kit-components"). An unlayered block would outrank every layered rule on
// every site that pins the kit.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const root = new URL('..', import.meta.url).pathname;
const astroFiles = dir => readdirSync(join(root, dir), { recursive: true })
  .filter(name => name.endsWith('.astro'))
  .map(name => join(dir, name));

// Blocks Astro passes through untouched, such as Tabs' <noscript> fallback,
// stay unlayered on purpose.
const STYLE = /<style(?![^>]*\bis:inline)[^>]*>([\s\S]*?)<\/style>/g;

export function unlayeredBlocks(source) {
  return [...source.matchAll(STYLE)].filter(([, css]) => !/^\s*@layer kit-components\s*\{[\s\S]*\}\s*$/.test(css)).length;
}

test('a layered block passes and an unlayered one is counted', () => {
  assert.equal(unlayeredBlocks('<style>\n@layer kit-components {\n  .a { color: red; }\n}\n</style>'), 0);
  assert.equal(unlayeredBlocks('<style>\n  .a { color: red; }\n</style>'), 1);
  assert.equal(unlayeredBlocks('<style is:global>\n.a {}\n@layer kit-components {\n}\n</style>'), 1);
  assert.equal(unlayeredBlocks('<noscript><style is:inline>.a {}</style></noscript>'), 0);
});

for (const file of [...astroFiles('components'), ...astroFiles('catalogue')]) {
  test(`${file} keeps its styles in @layer kit-components`, () => {
    assert.equal(unlayeredBlocks(readFileSync(join(root, file), 'utf8')), 0);
  });
}
