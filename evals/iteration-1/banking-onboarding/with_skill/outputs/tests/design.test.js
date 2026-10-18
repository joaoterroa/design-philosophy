// Design guardrails for the Harbour onboarding prototype. Run: node --test tests/
// Fails when styles or scripts use values that are not tokens, when dark mode misses a colour,
// when text falls below this product's contrast bar (7:1 for text, see design/SYSTEM.md),
// or when the page blocks the user's own zoom.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const root = path.join(__dirname, "..", "app");
const read = (f) => fs.readFileSync(path.join(root, f), "utf8");
const stripComments = (s) => s.replace(/\/\*[\s\S]*?\*\//g, "");

const tokens = read("tokens.css");
const styles = stripComments(read("styles.css"));
const script = read("app.js");
const html = read("index.html");

const vars = (css) => Object.fromEntries([...css.matchAll(/--([\w-]+):\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
const lightBlock = stripComments(tokens.slice(0, tokens.indexOf("@media")));
const mediaDark = stripComments(tokens.slice(tokens.indexOf("@media"), tokens.indexOf(':root[data-theme="dark"]')));
const attrDark = stripComments(tokens.slice(tokens.indexOf(':root[data-theme="dark"]')));
const light = vars(lightBlock);
const dark = { ...light, ...vars(attrDark) };

const hex = (v) => v.slice(0, 7);
const lum = (h) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a, b) => { const [x, y] = [lum(hex(a)), lum(hex(b))].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

test("styles.css uses tokens only (no literal colours, sizes, radii, durations)", () => {
  assert.deepEqual(styles.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi) || [], [], "literal colour in styles.css");
  const sizes = [...styles.matchAll(/font-size:\s*([^;}]+)/g)].map((m) => m[1].trim()).filter((v) => !/^var\(--fs-/.test(v));
  assert.deepEqual(sizes, [], "font-size must use --fs-* tokens");
  const radii = [...styles.matchAll(/border-radius:\s*([^;}]+)/g)].map((m) => m[1].trim()).filter((v) => !v.split(/\s+/).every((part) => /^(var\(--r-[\w-]+\)|50%|0)$/.test(part)));
  assert.deepEqual(radii, [], "border-radius must use --r-* tokens");
  const durations = styles.match(/\b\d+m?s\b/g) || [];
  assert.deepEqual(durations, [], "durations must use --dur-* tokens");
  const shadows = [...styles.matchAll(/box-shadow:\s*([^;}]+)/g)].map((m) => m[1].trim()).filter((v) => !/^(var\(--shadow-[\w-]+\)|none)$/.test(v));
  assert.deepEqual(shadows, [], "box-shadow must use --shadow-* tokens");
});

test("app.js and index.html set no inline colours or sizes", () => {
  for (const [name, src] of [["app.js", script], ["index.html", html]]) {
    assert.deepEqual(src.match(/#[0-9a-f]{6}\b|rgba?\(|hsla?\(/gi) || [], [], `literal colour in ${name}`);
    assert.deepEqual(src.match(/style\s*=\s*["'][^"']*(font-size|color|background)/gi) || [], [], `inline style in ${name}`);
  }
});

test("dark mode redefines every colour, identically in both dark blocks", () => {
  const colours = Object.keys(light).filter((k) => /^#/.test(light[k]) || /^0 /.test(light[k]));
  const m = vars(mediaDark), a = vars(attrDark);
  assert.deepEqual(colours.filter((k) => !(k in m)), [], "missing in prefers-color-scheme block");
  assert.deepEqual(colours.filter((k) => !(k in a)), [], "missing in [data-theme=dark] block");
  assert.deepEqual(colours.filter((k) => m[k] !== a[k]), [], "dark blocks disagree");
});

test("no type size below 17px (1.0625rem)", () => {
  for (const [k, v] of Object.entries(light).filter(([k]) => k.startsWith("fs-"))) {
    assert.ok(parseFloat(v) >= 1.0625, `--${k} is ${v}`);
  }
});

test("contrast holds in both themes", () => {
  const pairs = [
    // [fg, bg, minimum, why]
    ...["ink", "ink-muted", "act"].flatMap((fg) => ["paper", "surface", "sunk"].map((bg) => [fg, bg, 7, "text"])),
    ["act-on", "act", 7, "button label"],
    ["act-on", "act-press", 7, "pressed button label"],
    ["danger", "danger-tint", 7, "error text on its tint"],
    ["danger", "paper", 7, "inline error text"],
    ["caution", "caution-tint", 7, "safety advice"],
    ["caution", "sunk", 7, "safety line inside the message preview"],
    ["ok", "ok-tint", 7, "confirmation"],
    ["ok", "paper", 4.5, "done tick text"],
    ["ink", "caution-tint", 7, "body text inside safety panel"],
    ["ink", "danger-tint", 7, "body text inside error panel"],
    ["ink", "ok-tint", 7, "body text inside ok panel"],
    ["line", "paper", 3, "field border"],
    ["line", "surface", 3, "field border"],
    ["caution-edge", "paper", 3, "safety panel edge"],
    ["danger", "surface", 3, "error field border"],
    ["focus", "paper", 3, "focus ring"],
    ["paper", "act", 3, "focus-ring gap against a button fill"],
  ];
  const fails = [];
  for (const [name, t] of [["light", light], ["dark", dark]]) {
    for (const [fg, bg, min, why] of pairs) {
      const r = ratio(t[fg], t[bg]);
      if (r < min) fails.push(`${name}: --${fg} on --${bg} (${why}) ${r.toFixed(2)} < ${min}`);
    }
  }
  assert.deepEqual(fails, []);
});

test("page lets the user zoom and loads tokens before styles", () => {
  const vp = html.match(/<meta name="viewport" content="([^"]+)"/);
  assert.ok(vp, "viewport meta present");
  assert.ok(!/maximum-scale|user-scalable\s*=\s*no/.test(vp[1]), "viewport must not block zoom");
  assert.ok(html.indexOf("tokens.css") > -1 && html.indexOf("tokens.css") < html.indexOf("styles.css"), "tokens.css before styles.css");
});
