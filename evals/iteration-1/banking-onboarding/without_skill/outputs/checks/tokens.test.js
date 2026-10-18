// node --test checks/tokens.test.js
// Guardrails: styles.css uses tokens only, and text tokens hold contrast in both modes.
const test = require("node:test");
const assert = require("node:assert");
const fs = require("fs");
const path = require("path");
const app = path.join(__dirname, "..", "app");
const tokens = fs.readFileSync(path.join(app, "tokens.css"), "utf8");
const styles = fs.readFileSync(path.join(app, "styles.css"), "utf8");

function block(re) { const m = tokens.match(re); return m ? m[1] : ""; }
function vars(css) { const o = {}; for (const m of css.matchAll(/--([\w-]+):\s*(#[0-9A-Fa-f]{6})/g)) o[m[1]] = m[2]; return o; }
const light = vars(block(/^:root \{([\s\S]*?)\n\}/m));
const dark = { ...light, ...vars(block(/:root\[data-theme="dark"\] \{([\s\S]*?)\n\}/)) };
const darkMedia = { ...light, ...vars(block(/prefers-color-scheme: dark\) \{([\s\S]*?)\n  \}/)) };

function lum(hex) {
  const c = [1, 3, 5].map(i => parseInt(hex.slice(i, i + 2), 16) / 255).map(v => v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
function ratio(a, b) { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); }

// [foreground, background, minimum]. Body text aims for AAA (7:1) because the audience is older.
const pairs = [
  ["text", "bg", 7], ["text", "surface", 7], ["text", "soft", 7],
  ["text-2", "bg", 7], ["text-2", "surface", 7], ["text-2", "soft", 7],
  ["accent", "bg", 7], ["accent", "surface", 7], ["accent", "soft", 4.5],
  ["on-accent", "accent", 7], ["accent", "accent-soft", 4.5],
  ["err", "err-bg", 7], ["err", "bg", 4.5], ["err", "surface", 4.5],
  ["ok", "bg", 4.5], ["ok", "ok-bg", 4.5], ["text", "ok-bg", 7],
  ["line", "surface", 3], ["line", "bg", 3],            // control edges: WCAG 1.4.11
  ["focus", "bg", 3], ["on-focus-fill", "focus-fill", 7],
];

for (const [mode, t] of [["light", light], ["dark", dark]]) {
  for (const [fg, bg, min] of pairs) {
    test(`${mode}: --${fg} on --${bg} >= ${min}:1`, () => {
      const r = ratio(t[fg], t[bg]);
      assert.ok(r >= min, `${r.toFixed(2)}:1`);
    });
  }
}

test("dark media query and [data-theme=dark] agree", () => assert.deepStrictEqual(darkMedia, dark));

test("styles.css has no raw colours", () => {
  const bad = styles.replace(/\/\*[\s\S]*?\*\//g, "").match(/#[0-9A-Fa-f]{3,8}\b|rgba?\(/g) || [];
  assert.deepStrictEqual(bad, []);
});

test("styles.css font sizes are tokens", () => {
  const bad = [...styles.matchAll(/font-size:\s*([^;]+);/g)].map(m => m[1].trim()).filter(v => !/^var\(--fs-|^inherit$|^100%$/.test(v));
  assert.deepStrictEqual(bad, []);
});

test("no type token below 17px", () => {
  for (const m of tokens.matchAll(/--fs-[\w-]+:\s*([\d.]+)rem/g)) assert.ok(+m[1] * 16 >= 17, m[0]);
});
