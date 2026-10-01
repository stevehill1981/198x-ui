#!/usr/bin/env node
// Measures every pair in contrast-pairs.json against tokens.css and fails below the floor.
import { readFileSync } from 'node:fs';
import { parseTokens, resolveColour, contrastRatio } from './contrast.mjs';

const [tokensPath = 'tokens.css', pairsPath = 'contrast-pairs.json'] = process.argv.slice(2);
const tokens = parseTokens(readFileSync(tokensPath, 'utf8'));
const pairs = JSON.parse(readFileSync(pairsPath, 'utf8'));

let failed = 0;
for (const { fg, bg, min, note } of pairs) {
  const ratio = contrastRatio(resolveColour(tokens, fg), resolveColour(tokens, bg));
  const ok = ratio >= min;
  if (!ok) failed++;
  console.log(`${ok ? 'pass' : 'FAIL'}  ${ratio.toFixed(2)}:1 (min ${min})  ${fg} on ${bg}  ${note}`);
}
process.exit(failed ? 1 : 0);
