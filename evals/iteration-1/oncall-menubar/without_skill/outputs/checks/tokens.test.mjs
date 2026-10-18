// Design guardrails for the Handover prototype. Run: node --test checks/
import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import path from "node:path";

const dir = path.dirname(fileURLToPath(import.meta.url));
const tokens = readFileSync(path.join(dir, "../app/tokens.css"), "utf8");
const css = readFileSync(path.join(dir, "../app/app.css"), "utf8");

function block(re) {
  const m = tokens.match(re);
  assert.ok(m, "token block missing: " + re);
  const out = {};
  for (const [, k, v] of m[1].matchAll(/(--[\w-]+):\s*([^;]+);/g)) out[k] = v.trim();
  return out;
}
const light = block(/^:root \{([\s\S]*?)\n\}/m);
const darkMedia = block(/:root:not\(\[data-theme="light"\]\) \{([\s\S]*?)\n  \}/);
const darkForced = block(/:root\[data-theme="dark"\] \{([\s\S]*?)\n\}/);
const dark = { ...light, ...darkForced };

const hex = (h) => { h = h.replace("#", ""); return [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255); };
const lum = (h) => { const [r, g, b] = hex(h).map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4)); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

test("dark mode redefines every colour token, the same way in both dark blocks", () => {
  const colourKeys = Object.keys(light).filter((k) => /^(#|rgba?\()/.test(light[k]) && !k.startsWith("--desk") || k.startsWith("--shadow") || k === "--focus");
  for (const k of colourKeys) assert.ok(k in darkMedia, `${k} missing in prefers-color-scheme dark`);
  assert.deepEqual(darkMedia, darkForced, "the two dark blocks disagree");
});

for (const [mode, t] of [["light", light], ["dark", dark]]) {
  test(`${mode}: text tokens hold 4.5:1 on every surface`, () => {
    for (const fg of ["--fg", "--muted", "--accent-text", "--warn"]) {
      for (const bg of ["--pop-solid", "--soft", "--raised"]) {
        const r = ratio(t[fg], t[bg]);
        assert.ok(r >= 4.5, `${mode} ${fg} on ${bg} is ${r.toFixed(2)}:1`);
      }
    }
    assert.ok(ratio(t["--err"], t["--err-bg"]) >= 4.5, `${mode} --err on --err-bg`);
    assert.ok(ratio(t["--on-accent"], t["--accent"]) >= 4.5, `${mode} --on-accent on --accent`);
  });
  test(`${mode}: glyphs hold 3:1`, () => {
    for (const bg of ["--pop-solid", "--soft"]) assert.ok(ratio(t["--glyph"], t[bg]) >= 3, `${mode} --glyph on ${bg}`);
  });
}

test("app.css uses no raw colours, type sizes, radii or shadows", () => {
  const body = css.replace(/\/\*[\s\S]*?\*\//g, "");
  assert.equal(body.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi), null, "raw colour in app.css");
  assert.equal(body.match(/font-size\s*:/g), null, "font-size outside the font tokens");
  for (const [, v] of body.matchAll(/border-radius:\s*([^;]+);/g)) {
    assert.match(v, /^(var\(--r-[a-z]+\)( 0 0 var\(--r-[a-z]+\))?|50%)$/, "raw radius: " + v);
  }
  for (const [, v] of body.matchAll(/box-shadow:\s*([^;]+);/g)) {
    assert.match(v, /^(none|var\(--[\w-]+\)|(inset )?0 0 0 [\d.]+px var\(--[\w-]+\))$/, "raw shadow: " + v);
  }
});
