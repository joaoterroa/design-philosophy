# Tokens and the guardrail test

The written system says what to do; the guard test makes drift visible the moment it happens. Adapt this to the project's stack and test runner. The checks matter more than the code.

## Token file

One file (or one module) defines every colour for both themes, the type scale, radii, shadows and durations. Comments say what each token is for. Everything else references tokens.

- CSS: custom properties in `tokens.css`, dark values under `@media (prefers-color-scheme: dark)` (and a manual theme attribute if the product has a toggle).
- Tailwind or similar: the theme config is the token file; forbid arbitrary values in lint.
- Native/desktop: a theme/constants module per platform, generated from one source if there are several platforms.

## Checks the guard test should make

1. **No literal values outside the token file**: no hex/rgb/hsl colours, font sizes, radii or shadow colours in component styles.
2. **Theme parity**: every colour token defined for light is redefined for dark.
3. **Contrast**: each text token against each surface token, in both themes, at 4.5:1; meaningful graphics at 3:1; text on filled primary at 4.5:1.
4. **Wiring**: the token file is loaded before the styles that use it, and is included in the build or package.

## Example (Node, CSS custom properties)

```js
// tests/design.test.js
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");

const tokens = fs.readFileSync("src/tokens.css", "utf8");
const styles = fs.readFileSync("src/app.css", "utf8").replace(/\/\*[\s\S]*?\*\//g, "");

const vars = (css) => Object.fromEntries([...css.matchAll(/--([\w-]+):\s*([^;]+);/g)].map((m) => [m[1], m[2].trim()]));
const darkBlock = tokens.slice(tokens.indexOf("prefers-color-scheme: dark"));
const light = vars(tokens.slice(0, tokens.indexOf("@media")));
const dark = { ...light, ...vars(darkBlock) };

const lum = (hex) => {
  const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
    .map((c) => (c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
};
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };

test("styles use tokens only", () => {
  assert.deepEqual(styles.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi) || [], []);
  const sizes = [...styles.matchAll(/font-size:\s*([^;}]+)/g)].map((m) => m[1].trim()).filter((v) => !/^var\(--fs/.test(v));
  assert.deepEqual(sizes, []);
});

test("dark mode redefines every colour", () => {
  const colours = Object.keys(light).filter((k) => /^#/.test(light[k]));
  assert.deepEqual(colours.filter((k) => !(k in vars(darkBlock))), []);
});

test("text contrast holds in both themes", () => {
  for (const t of [light, dark]) for (const fg of ["fg", "muted"]) for (const bg of ["bg", "surface"]) {
    assert.ok(ratio(t[fg], t[bg]) >= 4.5, `--${fg} on --${bg}: ${ratio(t[fg], t[bg]).toFixed(2)}`);
  }
});
```

Rename the token names to the project's. Add the project's own pairs (accent text on its tinted ground, error on its tint, glyphs at 3:1).
