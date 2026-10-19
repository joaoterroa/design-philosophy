const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const root = path.resolve(__dirname, '..');
const tokens = fs.readFileSync(path.join(root, 'app/tokens.css'), 'utf8');
const styles = fs.readFileSync(path.join(root, 'app/app.css'), 'utf8').replace(/\/\*[\s\S]*?\*\//g, '');
const html = fs.readFileSync(path.join(root, 'app/index.html'), 'utf8');
const vars = css => Object.fromEntries([...css.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m => [m[1], m[2].trim()]));
const light = vars(tokens.split(':root[data-theme="dark"]')[0]);
const explicitDark = vars(tokens.split(':root[data-theme="dark"]')[1].split('@media')[0]);
const systemDark = vars(tokens.split('@media (prefers-color-scheme: dark)')[1].split('@media')[0]);
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(styles), 'Literal colour outside tokens');
assert(!/\b\d*\.?\d+(px|rem|em|ms)\b/.test(styles), 'Literal design dimension outside tokens');
for (const m of styles.matchAll(/var\(--([\w-]+)/g)) assert(m[1] in light, `Unknown token: ${m[1]}`);
for (const key of Object.keys(light).filter(k => /^#/.test(light[k]))) {
  assert(key in explicitDark, `Missing explicit dark colour ${key}`);
  assert(key in systemDark, `Missing system dark colour ${key}`);
  assert.equal(explicitDark[key], systemDark[key], `Dark theme mismatch: ${key}`);
}
assert(html.indexOf('tokens.css') < html.indexOf('app.css'), 'Load tokens first');
assert.equal(fs.readFileSync(path.join(root, 'app/fixtures.js'), 'utf8'), fs.readFileSync(path.join(root, '../fixtures.js'), 'utf8'), 'Fixture copy changed');
const lum = hex => {
  const [r, g, b] = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
  return .2126 * r + .7152 * g + .0722 * b;
};
const ratio = (a, b) => { const [lo, hi] = [lum(a), lum(b)].sort((a,b) => a-b); return (hi+.05)/(lo+.05); };
const results = [];
for (const [theme, t] of [['light', light], ['dark', {...light, ...explicitDark}]]) {
  const pairs = [];
  for (const fg of ['fg', 'muted', 'action']) for (const bg of ['bg', 'surface', 'tint']) pairs.push([fg, bg, 4.5]);
  for (const bg of ['bg', 'surface', 'error-bg']) pairs.push(['error', bg, 4.5]);
  pairs.push(['fg', 'error-bg', 4.5], ['on-action', 'action', 4.5], ['input-line', 'surface', 3], ['focus', 'bg', 3], ['focus', 'surface', 3]);
  for (const [fg, bg, min] of pairs) {
    const value = ratio(t[fg], t[bg]);
    assert(value >= min, `${theme}: ${fg} on ${bg} ${value.toFixed(2)} < ${min}`);
    results.push({theme, foreground: fg, background: bg, ratio: +value.toFixed(2), minimum: min});
  }
}
fs.writeFileSync(path.join(__dirname, 'contrast-results.json'), JSON.stringify(results, null, 2)+'\n');
console.log(`Token, theme, fixture integrity and ${results.length} contrast checks passed. Minimum text ratio: ${Math.min(...results.filter(r => r.minimum === 4.5).map(r => r.ratio))}:1.`);
