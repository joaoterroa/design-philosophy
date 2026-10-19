# Worked example: "Recall", a browser side panel for technical knowledge

This shows the method applied end to end, including the mistakes and the corrections that improved the rules. **It is an illustration of reasoning, not a template.** Its palette, layout, components and mark belong to that product; reusing them elsewhere defeats the point of `identity.md`.

## The product

A browser side panel (Chrome, and a docked window in Dia) that searches a team's reports, tracker, Jira and mail for what is already known about a SQL ID, API, error or question. Users are engineers in the middle of an investigation. Priorities, as the user stated them: speed, technical accuracy and clear presentation, compliance and trust, staying out of the way. Inspiration requested: The Browser Company and Dia, without copying them.

## 1–2. Understanding and references

- Read the panel's HTML, CSS and JS, the backend's event stream, and a long follow-ups file of measured fixes (layout shift budgets, focus retention, accessible tabs, context-tab behaviour). These became constraints to preserve.
- The Dia sites were blocked by the environment's network; research went through search summaries of the team's design essay and release notes, and this was stated to the user.
- Borrowed: "familiar, but elevated"; minimalism in the core UI; novelty reserved for the differentiator; craft in small details. Not copied: Dia's visuals, branding, components.
- Translation: Dia's differentiator is AI chat over your browsing; this product's is *the answer arriving with its evidence*. So that moment got the distinctive treatment.

## 3. Baseline audit

A stand-in backend ran the real search engine with realistic fake sources, so every state (streaming, partial failure, AI unavailable, offline) could be rendered. Measured weaknesses at 380px:
- first passage started 608px down, under a box-in-a-box composer, permanent status dots, three lines of brief metadata, tabs and two filter rows;
- saturated source pills competed with the content;
- the empty state was a wall of text;
- a pre-existing bug printed a literal "null" in the Coverage tab.

## 4. Direction

- **Structure:** composer docked at the bottom (where the hand already is, as in chat sidebars); the user's question becomes the heading of the results so the answer reads like a reply; a pinned segmented control for the three views; source health in a faint line under the composer, speaking up only when something is wrong.
- **Novelty moment:** while sources run, a rail of source glyphs lights up with counts, and a skeleton of the brief and its status steps fills in place.
- **Restraint:** status found became four labelled steps (deterministic, labelled "inferred from wording, not AI"); citations became small chips matching labels on the cited passages; sources told apart by glyph shape and name instead of colour.
- First passage moved to 510px; layout shift stayed under the earlier budget.

## 5–7. System, implementation, verification

- Tokens extracted into one file; a written `SYSTEM.md`; a test failing on literal colours, off-scale sizes, mismatched dark tokens and contrast below 4.5:1. The contrast test immediately caught a pre-existing grey at 4.49:1.
- Verified at 320, 380 and 440px, both themes, every state; interaction checks for dismiss/reattach, stop, focus after filter toggles, citation jumps, keyboard tabs, restore after reload.

## Corrections from the user, and the lessons they became

| What happened | Lesson now in the skill |
| --- | --- |
| I invented an indigo accent, then teal. The user wanted their company's colours; their brand guide supplied red and maroon. | Ask for brand material first; a brand guide beats invented taste (`identity.md`). |
| The user said "use the red instead of the blue, and change the yellow" about a screenshot of one line; I first changed the wrong roles. | Map feedback to roles explicitly before acting, then apply it everywhere the role appears (`decisions.md`, Interpreting feedback). |
| I kept a "Type @ to add a tab" hint. The user: `@` is familiar, don't explain it. | Explain the unusual, trust the conventional; keep hints for assistive tech (principle 6). |
| I used a fixed-height attachment slot to avoid layout shift; the user wanted the input to grow only when a tab is attached. | Stability without dead space: grow away from the reading point (principle 7). |
| Filter chips could need a third row. The user asked for a minimum width; research showed the browser sets the side panel's minimum and extensions can't change it. | Verify platform limits before promising a fix; design to the real floor and move late-arriving items to the end of the list (`decisions.md`, Platform constraints and Layout stability). |
| The old shortcut ⌘⇧K closes all tabs in Dia. | Research the host's shortcut space; display the live binding instead of hard-coded text. |
| Exact brand red was 4.43:1 as small text. | Exact brand value for fills; minimal adjustment for text; say so. |
| The first logo was a generic monogram. | A mark should show what the product does (here, one highlighted line in a passage), with a pixel-fitted 16px version. |

## What made it work

Restraint was argued from the product's priorities rather than applied as a style; every state was rendered and measured, not imagined; the system was written down and guarded by tests; and each correction from the user was generalised into a rule rather than patched locally.
