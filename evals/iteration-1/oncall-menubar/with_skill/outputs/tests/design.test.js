// Rota design guardrails. Run from outputs/: node --test tests/
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const dir = path.join(__dirname, "..", "app");
const tokens = fs.readFileSync(path.join(dir, "tokens.css"), "utf8");
const css = fs.readFileSync(path.join(dir, "app.css"), "utf8").replace(/\/\*[\s\S]*?\*\//g, "");
const html = fs.readFileSync(path.join(dir, "index.html"), "utf8");
const js = fs.readFileSync(path.join(dir, "app.js"), "utf8");

const vars = (s) => Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
const block = (start) => { const i = tokens.indexOf(start); const open = tokens.indexOf("{", tokens.indexOf("{", i) + (start.startsWith("@media") ? 1 : 0)); let d = 0, j = open; for (; j < tokens.length; j++) { if (tokens[j] === "{") d++; if (tokens[j] === "}" && --d === 0) break; } return tokens.slice(open, j); };
const light = vars(tokens.slice(0, tokens.indexOf("@media")));
const darkMedia = vars(block("@media (prefers-color-scheme: dark)"));
const darkAttr = vars(block(':root[data-theme="dark"]'));
const dark = { ...light, ...darkAttr };

const hex = (v) => { const m = /^#([0-9a-f]{6})([0-9a-f]{2})?$/i.exec(v); return m ? m[1] : null; };
const lum = (h) => [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255)
  .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4))
  .reduce((a, c, i) => a + c * [0.2126, 0.7152, 0.0722][i], 0);
const ratio = (a, b) => { const [x, y] = [lum(hex(a)), lum(hex(b))].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

test("app.css uses tokens only: no literal colours, sizes, radii or durations", () => {
  assert.deepEqual(css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(|\b(white|black)\b(?!-)/gi) || [], [], "literal colour");
  const bad = (re, ok) => [...css.matchAll(re)].map((m) => m[1].trim()).filter((v) => !ok.test(v));
  assert.deepEqual(bad(/font-size:\s*([^;}]+)/g, /^var\(--fs-/), [], "font-size");
  assert.deepEqual(bad(/font-weight:\s*([^;}]+)/g, /^var\(--fw-/), [], "font-weight");
  assert.deepEqual(bad(/border-radius:\s*([^;}]+)/g, /^var\(--r-/), [], "border-radius");
  assert.deepEqual(css.match(/\b\d+(\.\d+)?m?s\b(?![^;]*var\()/g)?.filter((v) => !/^0m?s$/.test(v)) || [], [], "literal duration");
  assert.deepEqual(css.match(/box-shadow:[^;]*\d+px[^;]*#/g) || [], [], "shadow colour");
});

test("scripts and markup carry no inline colours or styles beyond geometry", () => {
  assert.deepEqual(js.match(/#[0-9a-f]{6}\b/gi) || [], []);
  assert.deepEqual([...js.matchAll(/style="([^"]+)"/g)].map((m) => m[1]).filter((s) => !/^(left|width):\$\{[^}]+\}%(;width:\$\{[^}]+\}%)?$/.test(s)), []);
  assert.equal(/style=/.test(html), false);
});

test("dark mode redefines every colour, in both the media query and the manual theme", () => {
  const colours = Object.keys(light).filter((k) => /^#/.test(light[k]));
  assert.deepEqual(colours.filter((k) => !(k in darkMedia)), [], "missing in prefers-color-scheme block");
  assert.deepEqual(colours.filter((k) => !(k in darkAttr)), [], "missing in [data-theme=dark]");
  assert.deepEqual(colours.filter((k) => darkMedia[k] !== darkAttr[k]), [], "the two dark blocks disagree");
});

test("tokens.css loads before app.css", () => {
  assert.ok(html.indexOf("tokens.css") > -1 && html.indexOf("tokens.css") < html.indexOf("app.css"));
});

const TEXT = [ // [foreground, background, minimum]
  ["fg", "window", 4.5], ["fg-2", "window", 4.5], ["fg", "fill-hover", 4.5], ["fg-2", "fill-hover", 4.5],
  ["fg", "fill-quiet", 4.5], ["on-you", "fill-you", 4.5], ["on-accent", "accent", 4.5], ["accent-text", "window", 4.5],
  ["fg", "accent-soft", 4.5], ["fg-2", "accent-soft", 4.5], ["pending", "pending-soft", 4.5], ["pending", "window", 4.5],
  ["fg", "pending-soft", 4.5], ["accent-text", "pending-soft", 4.5], ["danger", "danger-soft", 4.5], ["danger", "window", 4.5],
  ["fg", "danger-soft", 4.5],
  // meaningful graphics at 3:1. (--accent as a button fill is identified by its white label, like the native
  // macOS push button, so the fill-vs-window boundary is not checked; see SYSTEM.md §3.)
  ["fill-you", "window", 3], ["accent-line", "window", 3], ["accent-line", "fill-quiet", 3], ["pending", "pending-soft", 3], ["fg-3", "window", 1.9],
];
for (const [name, t] of [["light", light], ["dark", dark]]) {
  test(`contrast holds in ${name}`, () => {
    const fails = TEXT.filter(([f, b, min]) => ratio(t[f], t[b]) < min).map(([f, b, min]) => `--${f} on --${b}: ${ratio(t[f], t[b]).toFixed(2)} < ${min}`);
    assert.deepEqual(fails, []);
  });
}
