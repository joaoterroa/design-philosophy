# Deriving a project's own identity

The philosophy is shared; the identity is not. Every project should look like it was designed for its own users, by people who care. If two projects designed with this skill could swap stylesheets without anyone noticing, the identity step was skipped.

## Where identity comes from, in order

1. **The brand, if one exists.** Ask for brand guidelines, logo files, the company's palette and typefaces. Use the brand's values exactly where they are used as brand (marks, primary fills); assign the rest of the palette to roles. A brand guide is evidence; your taste is an opinion.
2. **The platform and host.** A browser side panel should feel native to the browser; a desktop app to its OS; a wall dashboard to a room viewed from three metres; a terminal UI to a terminal. The host decides type choice (system font vs. brand font), density, motion and what "familiar" means.
3. **The users and their moment.** Engineers mid-incident want density and precision; occasional users want guidance; executives at a glance want one number and its direction. This decides scale, density and how much the UI may explain.
4. **The product's character.** What does the product do that nothing else does, and what tone suits it: calm and exact, warm and encouraging, fast and terse? This decides the novelty moment, the mark, the voice of the copy.

Only after these four, apply taste.

## Deciding each element

**Palette.** Start neutral, then add colour only for roles the product needs (act, follow/cite, caution, failure, health, data categories). Take each colour from the brand when it fits the role; if the brand lacks a role, choose a colour that sits naturally with the brand (often a related hue at a different lightness, or the brand's own secondary), not a fashionable accent. Design dark mode as its own palette with the same roles. Check contrast for every text use.

**Type.** System fonts when the product should feel native to its host or when speed and rendering matter; a brand or characterful face when the product is a destination or a brand surface. One scale, few sizes, weight before size for hierarchy, tabular numerals where numbers align.

**Shape and space.** Pick a corner and spacing language that suits the character (tight and precise, soft and friendly) and apply it consistently: nested shapes take smaller radii than their containers; one gutter; a short spacing scale.

**Elevation and surfaces.** Flat by default; elevation only for what floats over content (popovers, a docked input, a dragged item). Hairlines before cards; a filled panel only for a genuinely grouped fact.

**Motion.** Decide one easing and two or three durations. Motion explains change (arrival, growth, focus moving); loops only while work is happening.

**The mark.** A mark that shows what the product does, drawn simply enough to survive 16px, with a separate pixel-fitted small version. It should be explainable in one sentence.

**Voice.** Write a few sample messages (an error, an empty state, a success) and check they sound like the product's character.

## Avoiding sameness

Defaults pull every project toward the last one. Watch for these and only use them when this product's context independently justifies them:

- the previous project's palette, accent or neutral temperature;
- a docked bottom input, a segmented control, a skeleton/sheen loading treatment, citation chips, a status "ladder", or other patterns from a recent case study;
- system font by habit (choose it for nativeness, not by default);
- the same radius scale and spacing numbers;
- the same mark structure (a tile with a glyph inside).

Before finalising, write one sentence per major choice (palette, type, layout structure, novelty moment, mark) saying why it fits *this* product. If the sentence would be equally true of the last project, reconsider the choice.

Also avoid the generic look that comes from no decisions at all: gradient washes, every block in a card, gratuitous rounded corners, badges and pills for everything, oversized spacing, decorative icons, emoji, a purple-to-blue accent chosen because it is safe.
