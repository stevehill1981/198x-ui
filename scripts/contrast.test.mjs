import { test } from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { luminance, contrastRatio, parseTokens, resolveColour } from './contrast.mjs';

test('luminance spans 0 to 1', () => {
  assert.equal(luminance('#000000'), 0);
  assert.equal(luminance('#ffffff'), 1);
});

test('contrast ratio matches WCAG examples', () => {
  assert.equal(Math.round(contrastRatio('#000000', '#ffffff') * 100) / 100, 21);
  assert.equal(Math.round(contrastRatio('#1b1a17', '#f6f4ee') * 100) / 100, 15.82);
  assert.equal(Math.round(contrastRatio('#7a7468', '#f6f4ee') * 100) / 100, 4.22);
});

test('first declaration of a token wins', () => {
  const t = parseTokens(':root { --h-a: #111111; } :root[x] { --h-a: #222222; }');
  assert.equal(t['--h-a'], '#111111');
});

test('ignores declarations inside comments', () => {
  const t = parseTokens('/* --h-a: #000000; */ :root { --h-a: #111111; }');
  assert.equal(t['--h-a'], '#111111');
});

test('resolves var() chains and literal hex', () => {
  const t = parseTokens(':root { --h-a: var(--h-b); --h-b: #ABCDEF; }');
  assert.equal(resolveColour(t, '--h-a'), '#abcdef');
  assert.equal(resolveColour(t, '#FFFFFF'), '#ffffff');
});

test('refuses tokens that are not plain colours', () => {
  const t = parseTokens(':root { --h-a: color-mix(in srgb, red 10%, blue); --h-loop: var(--h-loop); }');
  assert.throws(() => resolveColour(t, '--h-a'), /not a plain colour/);
  assert.throws(() => resolveColour(t, '--h-loop'), /loop/);
  assert.throws(() => resolveColour(t, '--h-missing'), /unknown token/);
});

test('CLI exits 1 when a pair is below its floor', () => {
  const r = spawnSync(process.execPath, [
    'scripts/check-contrast.mjs',
    'scripts/fixtures/tokens-failing.css',
    'scripts/fixtures/pairs-failing.json',
  ], { encoding: 'utf8' });
  assert.equal(r.status, 1);
  assert.match(r.stdout, /FAIL/);
});
