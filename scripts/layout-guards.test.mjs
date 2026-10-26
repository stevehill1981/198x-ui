// The layout primitives' build-time guards (components/layout/). Node runs
// the TypeScript directly, so these need no build step.
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { refuseCaptures } from '../components/layout/frame.ts';
import { refuseSameKindChild, topLevelClasses } from '../components/layout/nesting.ts';

test('Frame lets an illustration through', () => {
  assert.doesNotThrow(() => refuseCaptures('<img class="h-figure-img" src="/images/photo.webp" alt="">'));
  assert.doesNotThrow(() => refuseCaptures('<figure class="h-figure h-figure-photo"><img alt=""></figure>'));
});

for (const html of [
  '<div class="h-screen h-screen--crt"><img class="h-screen-img" alt=""></div>',
  "<figure class='h-figure h-figure-capture'><img alt=\"\"></figure>",
  '<figure class="native-image" data-capture><img alt=""></figure>',
  '<div data-capture="true"><img alt=""></div>',
]) {
  test(`Frame refuses a capture: ${html.slice(0, 40)}`, () => {
    assert.throws(() => refuseCaptures(html), /cannot hold a capture/);
  });
}

test('Frame ignores the words outside a class or attribute', () => {
  assert.doesNotThrow(() => refuseCaptures('<p>An h-screen with data-capture is decoded at build time.</p>'));
  assert.doesNotThrow(() => refuseCaptures('<div class="h-screens-list"></div>'));
});

test('topLevelClasses lists only the outermost elements', () => {
  assert.deepEqual(topLevelClasses('<div class="a b"><p class="inner">x</p></div><aside class=\'c\'></aside>'), [['a', 'b'], ['c']]);
});

test('topLevelClasses is not thrown off by void elements, comments, raw text or > in attributes', () => {
  const html = '<!-- <div class="x"> --><img class="pic" alt="a > b"><br><script>if (a<b) document.write("<div class=\\"l-reel\\">")</script><div data-json=\'{"a":">"}\' class="last"><span></span></div>';
  assert.deepEqual(topLevelClasses(html), [['pic'], [], [], ['last']]);
});

test('a primitive refuses a direct child of its own kind', () => {
  assert.throws(() => refuseSameKindChild('<div class="l-with-sidebar" data-side="left"><div></div><div></div></div>', 'l-with-sidebar', 'Sidebar'), /direct child of another Sidebar/);
});

test('a primitive allows one wrapped in another element', () => {
  assert.doesNotThrow(() => refuseSameKindChild('<div class="wrap"><div class="l-with-sidebar"></div></div>', 'l-with-sidebar', 'Sidebar'));
});

test('a primitive allows a different primitive as a direct child', () => {
  assert.doesNotThrow(() => refuseSameKindChild('<div class="l-switcher"></div><div class="l-reel"></div>', 'l-with-sidebar', 'Sidebar'));
});
