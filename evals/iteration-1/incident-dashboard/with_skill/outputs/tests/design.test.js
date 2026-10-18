// Design guardrails for the Northwind Incident Board. Run: node --test tests/*.test.js
// Fails when code drifts from app/tokens.css, when light and dark disagree, or when text loses contrast.
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");

const APP = path.join(__dirname, "..", "app");
const read = (f) => fs.readFileSync(path.join(APP, f), "utf8");
const stripComments = (s) => s.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, "");

const tokens = stripComments(read("tokens.css"));
const css = stripComments(read("app.css"));
const js = stripComments(read("app.js"));
const html = read("index.html");

const vars = (block) => Object.fromEntries([...block.matchAll(/--([\w-]+):\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
const blockAfter = (src, marker) => {
  const i = src.indexOf(marker);
  assert.ok(i >= 0, "missing block: " + marker);
  const open = src.indexOf("{", i + marker.length - 1);
  let depth = 0;
  for (let j = open; j < src.length; j++) {
    if (src[j] === "{") depth++;
    if (src[j] === "}" && --depth === 0) return src.slice(open + 1, j);
  }
  throw new Error("unclosed block: " + marker);
};
const light = vars(blockAfter(tokens, ":root {"));
const darkMedia = vars(blockAfter(blockAfter(tokens, "@media (prefers-color-scheme: dark)"), ':root:not([data-theme="light"])'));
const darkAttr = vars(blockAfter(tokens, ':root[data-theme="dark"]'));
const dark = { ...light, ...darkAttr };

const isColour = (v) => /^#[0-9a-f]{6}([0-9a-f]{2})?$/i.test(v);
const lum = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

test("app.css uses tokens only: no literal colours, font sizes, radii or font families", () => {
  assert.deepEqual(css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi) || [], [], "literal colour in app.css");
  const sizes = [...css.matchAll(/font-size:\s*([^;}]+)/g)].map((m) => m[1].trim()).filter((v) => !/^var\(--(fs|root)-[\w-]+\)$/.test(v));
  assert.deepEqual(sizes, [], "font-size outside the type scale");
  const radii = [...css.matchAll(/border(?:-[a-z]+)*-radius:\s*([^;}]+)/g)].map((m) => m[1].trim())
    .filter((v) => !v.split(/\s+/).every((p) => /^var\(--radius-[\w]+\)$/.test(p) || p === "0" || p === "50%"));
  assert.deepEqual(radii, [], "radius outside the token scale");
  const families = [...css.matchAll(/font-family:\s*([^;}]+)/g)].map((m) => m[1].trim()).filter((v) => !/^var\(--font-(sans|mono)\)$/.test(v));
  assert.deepEqual(families, [], "font-family outside tokens");
  const durations = [...css.matchAll(/\b\d+m?s\b/g)].map((m) => m[0]);
  assert.deepEqual(durations, [], "literal duration in app.css");
});

test("app.js and index.html carry no styling of their own", () => {
  assert.deepEqual(js.match(/#[0-9a-f]{6}\b|rgba?\(|hsla?\(/gi) || [], [], "literal colour in app.js");
  const styleWrites = [...js.matchAll(/\.style\.(\w+)/g)].map((m) => m[1]).filter((p) => !["setProperty", "left", "top"].includes(p));
  assert.deepEqual(styleWrites, [], "app.js may only set custom properties (and tooltip position)");
  assert.ok(!/<style[\s>]/i.test(html) && !/\sstyle="/i.test(html), "no inline styles in index.html");
});

test("every colour token is defined for light and redefined, identically, in both dark blocks", () => {
  const colours = Object.keys(light).filter((k) => isColour(light[k]));
  assert.ok(colours.length >= 15, "expected the full colour set in :root");
  assert.deepEqual(colours.filter((k) => !(k in darkMedia)), [], "missing from @media dark");
  assert.deepEqual(colours.filter((k) => !(k in darkAttr)), [], "missing from [data-theme=dark]");
  assert.deepEqual(darkMedia, darkAttr, "the two dark blocks must match");
});

test("brand values are used exactly where they are used as brand", () => {
  for (const t of [light, dark]) {
    assert.equal(t.brand.toUpperCase(), "#12355B", "Harbor Navy");
    assert.equal(t.attention.toUpperCase(), "#F26B21", "Signal Orange");
    assert.equal(t.data.toUpperCase(), "#2A9D8F", "Tide Teal");
  }
  assert.equal(light.bg.toUpperCase(), "#EEF1F4", "Fog");
  assert.equal(light.fg.toUpperCase(), "#3D4852", "Slate");
});

test("text contrast holds at 4.5:1 in both themes", () => {
  const pairs = [
    ["fg", "bg"], ["fg", "surface"], ["fg-strong", "bg"], ["fg-strong", "surface"],
    ["muted", "bg"], ["muted", "surface"],
    ["critical-text", "bg"], ["critical-text", "surface"], ["critical-text", "critical-tint"],
    ["attention-text", "bg"], ["attention-text", "surface"], ["attention-text", "attention-tint"],
    ["fg", "attention-tint"], ["fg-strong", "attention-tint"], ["muted", "attention-tint"],
    ["fg", "critical-tint"], ["muted", "critical-tint"],
    ["on-critical", "critical"], ["on-attention", "attention"], ["on-brand", "brand"],
  ];
  const fails = [];
  for (const [name, t] of [["light", light], ["dark", dark]]) {
    for (const [fg, bg] of pairs) {
      const r = ratio(t[fg], t[bg]);
      if (r < 4.5) fails.push(`${name}: --${fg} on --${bg} = ${r.toFixed(2)}`);
    }
  }
  assert.deepEqual(fails, []);
});

test("meaningful graphics hold 3:1 against the page", () => {
  // --minor and --data-quiet are deliberately quiet: their values are always also given as text.
  // Documented exception: exact Tide Teal on Fog is 2.93:1. Kept exact (brand chart colour); the relief is that
  // every chart value is also printed as text (bar values, stat values, meter %), as SYSTEM.md section 3 requires.
  const EXCEPTIONS = { "light:data": 2.9 };
  const fails = [];
  for (const [name, t] of [["light", light], ["dark", dark]]) {
    for (const g of ["data", "critical", "focus"]) {
      const r = ratio(t[g], t.bg);
      const floor = EXCEPTIONS[name + ":" + g] || 3;
      if (r < floor) fails.push(`${name}: --${g} on --bg = ${r.toFixed(2)}`);
    }
  }
  // Signal Orange is exact brand; on Fog it is a fill that always carries the words "SEV2" in ink.
  const orangeDark = ratio(dark.attention, dark.bg);
  if (orangeDark < 3) fails.push(`dark: --attention on --bg = ${orangeDark.toFixed(2)}`);
  assert.deepEqual(fails, []);
});

test("wiring: tokens load before styles, fonts ship locally", () => {
  assert.ok(html.indexOf("tokens.css") > 0 && html.indexOf("tokens.css") < html.indexOf("app.css"));
  for (const m of tokens.matchAll(/url\("([^"]+)"\)/g)) assert.ok(fs.existsSync(path.join(APP, m[1])), "missing font " + m[1]);
  assert.ok(!/https?:\/\//.test(read("tokens.css") + css + html.replace(/<!--[\s\S]*?-->/g, "")), "no network dependencies");
});
