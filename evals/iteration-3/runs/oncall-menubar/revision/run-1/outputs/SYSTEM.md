# Rota design system — clear ownership

Read this before changing the UI. Values live in `app/tokens.css`; `verification/design-guard.mjs` checks wiring, literal colours/type sizes/radii/shadows, theme parity, used tokens, fixture integrity, and the actual text/graphic contrast pairs.

## Purpose and priorities

Rota serves SREs opening a menu-bar popover while doing other work. Priorities: (1) current responsibility, (2) deliberate handover, (3) current team coverage, (4) honest uncertainty, (5) compact native familiarity.

- The user's shift comes first. Keep ownership, rotation, time range, and action together.
- Sending is not acceptance. Pending always names Jamie as still responsible.
- A roster is not a staff directory. The hero and the three other responders represent the four current fixture entries.
- Saved data is past-tense. Never show a live progress indicator offline.
- The transfer object keeps its identity across review, pending, and accepted screens. This is the product's distinctive treatment.

## Colour and contrast

These colours are a task-specific proposal, as there is no supplied Rota brand.

| Role | Light | Dark | Use and reason |
| --- | --- | --- | --- |
| `bg` | `#fafbf9` | `#252b27` | Popover's quiet base |
| `surface` | `#f0f2ef` | `#2e3530` | Shift, transfer, and secondary grouping |
| `field` | `#ffffff` | `#202622` | Input affordance |
| `fg` | `#242c29` | `#edf0eb` | Main text; clear names and ownership |
| `muted` | `#606b65` | `#b0b9b1` | Supporting readable information, never hidden caveats |
| `accent` | `#245b46` | `#acd6b9` | Primary action; dark mode uses a lighter fill with dark text |
| `health` | `#276346` | `#b0d7bc` | Confirmed ownership, not a claim about service health |
| `health-bg` | `#eaf2eb` | `#2b3c30` | Confirmed/selected context |
| `caution` | `#775014` | `#e5c188` | Pending responsibility and uncertain saved data |
| `caution-bg` | `#f7f0df` | `#3c3425` | Same cautions, with explanatory sentences |
| `focus` | `#2967a5` | `#8fbef1` | Keyboard focus only |

`line` is structural, not an input boundary. `line-strong` supplies the accessible field boundary. The scene is a neutral host background, not product content. Shadows communicate a floating popover, never nested elevation. Text roles are checked at 4.5:1 or higher; functional boundaries/focus at 3:1 or higher. State meaning is always stated in words.

## Type

Use `--font`: macOS system typography first, with local system fallbacks. It fits a utility owned by its host rather than a branded web destination. Bundled IBM Plex Mono 400 supports aligned numeric time labels.

| Token | Size | Role |
| --- | --- | --- |
| `fs-xs` | 11px | Metadata, initials, UTC, footer |
| `fs-sm` | 12px | Secondary facts and explanatory text |
| `fs-body` | 13px | Body, names, buttons |
| `fs-md` | 14px | Reserved intermediate size |
| `fs-lg` | 16px | Product wordmark |
| `fs-title` | 23px | Current rotation and task titles |

Body line-height is 1.45; title line-height 1.2. Medium/semibold distinguish headings without adding badges. Times use tabular numerals; fixed-width roster end times align.

## Geometry and components

The 4px spacing scale runs through 56px. A 20px outer scene inset places the popover at x20/y20. The width is 360px; maximum height is 640px. Border thickness is 1px. Content generally has a 20px inset. Headers are 56px tall. Primary buttons are at least 40px; text actions at least 32px. Current responder rows are 56px, or 48px in the offline state.

The outer radius is 13px; meaningful inset objects use 9px; buttons/inputs/notices use 6px. Avatars are circles, serving as quiet person anchors rather than arbitrary colour categories. The inset spacing separates nested curves convincingly. SVG coordinates and stroke widths are drawing geometry; percentages such as shift progress are data, not visual theme values.

- **Shift:** current ownership label, rotation title, person, time range, fixture-snapshot progress, remaining time, single action.
- **Recipient:** a whole-row radio target with a persistent label; no invented presence or availability signal.
- **Transfer:** sender, recipient, rotation, remainder of shift, optional note. It survives review, waiting and acceptance without changing the information's order.
- **Caution:** words plus a tinted surface. Never replace responsibility with an icon.
- **Empty:** says the schedule is absent, not that nobody is responsible.

Initial fixture states fit without scrolling. Long notes and user-triggered feedback may scroll inside the maximum height. Never truncate names or user notes; use wrapping and keyboard-reachable actions.

## Motion and language

One 120ms ease-out hover transition. No automatic looping or time-based acceptance. Reduced motion removes transitions while keeping all content. Focus moves immediately and never waits for animation.

Voice: calm, exact, direct. Examples: “You’re still on call”; “Coverage may have changed”; “No schedule available”; “Priya is now on call.” Do not explain conventional selection mechanics. Explain responsibility and uncertainty.

## Accessibility and state

Real labelled controls, headings, fieldset/legend, list semantics, hidden decorative SVGs, status feedback, and visible focus. New screens focus their heading, with Tab continuing to the next relevant action. Back preserves form selection and note; Escape returns review to compose and compose to schedule. Keep acceptance as an explicit action outside the product, in the local harness. Production acceptance must come from the receiving user/service.

URL theme overrides system preference. Otherwise observe preference changes. Theme role names must remain identical. Fresh direct URLs load fixture states deterministically; do not persist mutations globally. Within a page, history must not undo a cancelled or accepted request.

## Before changes ship

- Run token guard and interaction verification scripts.
- Inspect every state at 400×680, both themes; root at x20/y20, width 360px, height ≤640px.
- Check a long note, cancel, Escape, keyboard focus, and explicit acceptance.
- Keep offline past-tense and pending ownership explicit.
- Preserve fixture facts and do not invent staff, presence, or network success.
- Record native host, screen reader, and live-data limits honestly.
