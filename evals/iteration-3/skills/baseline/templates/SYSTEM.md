# [Product] design system: "[direction name]"

<!-- Template from the design-philosophy skill. Replace every bracket with this product's own answer.
     Keep the reasons: values without reasons get changed casually. Delete sections that don't apply. -->

This is the source of truth for how [product] looks and behaves. Read it before changing the UI. Values live in `[path/to/tokens]`. `[path/to/guard test]` fails when code uses a value that is not a token, when light and dark disagree, or when text drops below contrast.

## 1. What it is for

[Who uses it, in what moment, and what they need first.] In priority order:

1. **[Priority]**: [what it means here]
2. **[Priority]**: …
3. **[Priority]**: …

## 2. Principles

<!-- Adapt from the skill's philosophy.md. Write each as it applies to this product, with an example from this UI.
     Usually 4–7 principles. Include the novelty moment explicitly. -->

**[Principle].** [How it shows up in this product.]

**Novelty where it pays.** The distinctive treatment is reserved for [the moment], because [reason]. Everywhere else is plain.

## 3. Colour

[One sentence on the neutral base.] Colour is kept for meaning, and each meaning has one colour:

| Token | Light / dark | Means | Use for | Never for |
| --- | --- | --- | --- | --- |
| `[--token]` | `[#hex]` / `[#hex]` | [meaning] | [uses] | [misuses] |

Rules:
- [Where the palette comes from: brand guide, platform, or a reasoned proposal.]
- [Any brand value adjusted for contrast, and by how much.]
- Errors are words plus a tinted surface, never colour alone.
- Text tokens hold 4.5:1 on every surface in both themes; meaningful graphics hold 3:1. The guard test checks this.

## 4. Type

[Which face and why: native feel, brand, legibility at distance.] One scale:

| Token | Size / line, weight | Use |
| --- | --- | --- |
| `[--fs-…]` | [size/line, weight] | [where] |

[Rules for weight, numerals, tracking.]

## 5. Space and shape

- [Gutter, rhythm, spacing steps.]
- Radii: [scale and what each is for]. Nested shapes take smaller radii than their containers.
- [Surfaces: when hairlines, when a filled panel, when elevation.]

## 6. Layout

[The structure, top to bottom or by region, at the real sizes: narrowest [px], typical [px], widest [px]. Platform limits and their source.]

## 7. Components

- **[Component].** [What it is, its states, why it is shaped this way.]

## 8. Motion

[Easing, durations, what motion explains, what loops and when they stop. Reduced motion removes all of it.]

## 9. Writing

[Voice in three adjectives, with one example each of an error, an empty state and a success message.]

## 10. Brand

[The mark: what it shows and why; where the source files live; how to regenerate sizes.]

## 11. Keyboard and accessibility

[Shortcuts and why they don't collide with the host; in-app keys; focus rules; screen reader hints.]

## 12. Before you ship a UI change

- [ ] Tokens only; the guard test passes.
- [ ] Looked at in both themes, at [sizes], in every state, with realistic data.
- [ ] Nothing above the reading point moves while content arrives.
- [ ] No new colour meaning, card, or badge where a word would do.
- [ ] Keyboard path, screen reader text and reduced motion still work.
- [ ] Copy says what is inferred, what failed and what to do.
