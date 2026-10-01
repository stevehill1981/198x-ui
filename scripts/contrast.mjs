// WCAG 2.x relative luminance and contrast, and a reader for the kit's tokens.
// The kit measures its own colours here instead of quoting ratios measured elsewhere.

export function luminance(hex) {
  const n = hex.replace('#', '');
  const [r, g, b] = [0, 2, 4].map((i) => {
    const c = parseInt(n.slice(i, i + 2), 16) / 255;
    return c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

export function contrastRatio(a, b) {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi + 0.05) / (lo + 0.05);
}

export function parseTokens(css) {
  // Strip CSS comments before matching
  const stripped = css.replace(/\/\*[\s\S]*?\*\//g, '');
  const tokens = {};
  for (const m of stripped.matchAll(/(--h-[\w-]+)\s*:\s*([^;]+);/g)) {
    if (!(m[1] in tokens)) tokens[m[1]] = m[2].trim();
  }
  return tokens;
}

const HEX = /^#[0-9a-f]{6}$/i;

export function resolveColour(tokens, nameOrHex, seen = new Set()) {
  if (HEX.test(nameOrHex)) return nameOrHex.toLowerCase();
  if (!(nameOrHex in tokens)) throw new Error(`unknown token ${nameOrHex}`);
  if (seen.has(nameOrHex)) throw new Error(`loop resolving ${nameOrHex}`);
  seen.add(nameOrHex);
  const value = tokens[nameOrHex];
  if (HEX.test(value)) return value.toLowerCase();
  const ref = value.match(/^var\((--h-[\w-]+)\)$/);
  if (ref) return resolveColour(tokens, ref[1], seen);
  throw new Error(`${nameOrHex} is not a plain colour: ${value}`);
}
