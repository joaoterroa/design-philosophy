# Northwind Ops screens: design system (v0.1)

The rules behind `app/`. Tokens live in `app/tokens.css`; `app/styles.css` must not contain raw colour values (checked with `grep -E "#[0-9a-fA-F]{3,6}" app/styles.css`, which returns nothing).

## Where the brand guide stops
The brand guide (v3) was written for marketing and product UI. An ops screen needs a few things it doesn't cover. Each addition is marked `[ext]` in `tokens.css`.

| Need | Decision | Why |
|---|---|---|
| Severity colours | SEV1 red, SEV2 amber, SEV3 neutral slate. Light `#C0262D / #9E7A00 / #5E6A76`, dark `#F25757 / #E0A228 / #8A9AAB` | The brand has no red. An ops team reads red as "worst" before it reads anything else. SEV3 is grey on purpose because a low-severity incident shouldn't pull the eye. |
| Signal Orange | **Not used on this screen** | The guide reserves it for calls to action and highlights. On an incident screen any orange would read as a severity, and it would be too close to the SEV2 amber. |
| Tide Teal | The only data colour (bars, sparkline end, meter) and the "live / all clear" signal | The guide names it for charts. There is one series per chart, so one colour is enough. |
| Dark theme | Deep navy surfaces taken from Harbor Navy (`#0A1A2E` page, `#10263F` panel) | Ops rooms are dim, and a white 55" panel glares. These are new steps, not an inverted light theme. |
| Good/bad deltas | Teal-dark for better, red for worse. The arrow still shows up or down. | Colour carries the meaning (good or bad); the arrow carries the direction. "MTTR ▼" is good and "budget ▼" is bad. |

## Validation (dataviz palette checker, OKLab ΔE×100)
- Light SEV1/SEV2 on white: deutan ΔE 7.0, normal-vision 18.7, contrast ≥ 3:1. ΔE 7.0 is in the 6–8 band, which is only legal with secondary encoding. We always have it: the text label `SEV1` plus a shape (◆ SEV1, ▲ SEV2, ○ SEV3).
- Dark SEV1/SEV2 on `#10263F`: deutan ΔE 10.0, normal-vision 18.3, contrast ≥ 4.5:1. SEV2 sits above the checker's dark lightness band (L 0.75). This is accepted on purpose: it's a status signal that has to carry across a room, not one of several categorical series.
- The checker flags SEV3 for its low chroma. That is the intent: SEV3 is neutral.
- Text contrast (computed): ink on panel 9.3:1 light and 13:1 dark; muted ink 5.5:1 light and 7.4:1 dark.

## Rules
1. **One headline per view.** That's the status banner. If the feed is stale or down, the feed bar replaces it.
2. **Severity is never colour alone.** Every place it appears has the label, the shape and the colour, and in lists also the edge.
3. **Text wears ink tokens.** Severity and data colours are for marks (edges, shapes, bars). The only coloured text is a delta or an alert ("Not assigned", "No owner"), and those use the text-safe `--delta-*` tokens.
4. **A feed problem is not an incident.** Stale or down data uses the neutral inverse bar and greys the content out. It never uses a severity colour.
5. **TV never scrolls.** The page is built on a 1920×1080 canvas with root size `100vw/96`. A 4K panel gets the same physical sizes. Lists trim their least severe rows and say what they trimmed ("+ 2 more SEV3 · INC-…").
6. **Type floor.** On TV, 20px is the minimum for any text people need to read. Body text is 27px and the headline is 36px. On a laptop the minimum is 12.8px (0.8rem).
7. **Numbers.** IDs use IBM Plex Mono (bundled, OFL). Columns of times and durations use tabular figures. The large figures stay proportional.
8. **Marks.** Bars are 24px or less with a 4px rounded end and a square base. Lines are 2px. Grids and dividers are 1px solid hairlines. No gradients, shadows on data, or emoji.
