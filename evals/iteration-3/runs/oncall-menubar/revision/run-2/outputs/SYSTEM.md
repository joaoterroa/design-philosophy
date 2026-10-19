# Interface system

Read this before changing the prototype. Visual roles live in `app/tokens.css`; `verification/tokens.cjs` checks their use and contrast. This is a proposed identity because no product brand material was supplied.

## Rota: responsibility first

Rota is a small macOS utility for roughly 40 SREs checking ownership mid-task. The four supplied people are the current roster, not a directory of the whole team.

Priorities, in order:
1. Know who is responsible now, and until when.
2. Transfer responsibility only after explicit acceptance.
3. Scan the current rotations without opening another view.
4. Trust the distinction between saved and current information.
5. Complete the task with a keyboard in a small popover.

Native mechanics carry the task: system type, a conventional recipient select, explicit review, ordinary buttons, Back and Cancel. The own-shift object gets the strongest position and one primary action. The rest is an aligned list, not a collection of cards. The three-bar mark depicts parallel shifts with one active shift; it remains recognizable at menu-bar scale. It is a proposal, not supplied brand artwork.

The 360px container starts at (20,20) in a 400×680 scene and grows to a maximum of 640px. Long notes can scroll the popover. Main and offline fit without scrolling. Insets are 20px, inner shift inset 16px, roster rows use a 12px vertical rhythm. Rounded outer corners (14px) match the role of a floating macOS utility; inner objects use 9px and buttons 6px. Elevation belongs to the popover, not every row.

Use 14px body, 12px metadata, 11px secondary footer/eyebrow, 22px shift title and 26px task headings. These compact sizes are for a pointer-and-keyboard desktop utility. Bank and wall display deliberately do not inherit this density.

Blue means an available action or shift progress; it does not mean healthy. Amber means responsibility needs attention or information is uncertain. Green only accompanies accepted completion. Offline wording says “last known” and “you were on call”; it cannot establish present ownership. Error and caution always have words.

## Northwind: an incident-room reading surface

IBM Plex Sans supports the operational density; Plex Mono aligns identifiers, times and metrics. Data is a table with a persistent column header, because experts need comparison rather than a set of expanded cards. First column severity and last column commander make the dangerous missing owner visible. Color is restrained to severity, missing ownership and freshness.

TV uses 24px incident text, 16px supporting status/metadata and 32px major headings. Laptop uses 14px incidents with a 26px heading. The large center is the incident list; the right rail groups metrics, duty and services. Light uses cool gray paper; dark uses a deep blue-gray background with separately tuned text, borders and signals. This is a proposal: `dashboard/index.html` and `brand/guide.md` were not present, so no claim of brand fidelity is possible.

Live and stale include seven open records; surge includes twelve. Every non-resolved status counts as open. Resolved history is a separate section and never adds to the count. No inferred aggregation replaces supplied service values. TV keeps the seven-row live/stale set visible; surge has a fixed-height scroll region and an explicit overflow sentence. Laptop supports scrolling both the list and the document. No automatic paging moves a row while someone reads it.

## Harbour: a short, legible setup

Harbour is a distinct consumer surface with a warm neutral ground and deep green action color. These are proposed, task-specific choices, not an inferred user-wide palette preference. Plex Sans uses 18px body and input text, 16px hints/errors and 32px headings (26px at 320px). Buttons are at least 54px high; Help and Back are at least 48px. The header stays familiar while each step asks for one kind of information. The simple harbour mark depicts a sheltered basin and a central mooring.

Welcome → details → code → completion. Name and mobile are labeled; examples never expose a usable code. A single code input supports paste and OS one-time-code completion. Bad input explains a repair next to the field. The safety warning remains in the page, reachable by scroll at the small size. Help is a native modal dialog with a telephone link, close button, Escape support, focus containment and return to its trigger.

## Shared roles and rules

All palettes have explicit light/dark counterparts. `--fg` is primary text; `--muted` remains readable, not faint. `--line` separates groups; `--control-line` is the stronger boundary of editable fields. Action fills have their own foreground tokens. Brand/identity colors never replace error wording. Check concrete values in the token file rather than copying them into components.

The spacing scale is 4, 8, 12, 16, 20, 24, 32, 40, 48px. Radius roles are 6/9/14px and circular avatars. Layout widths and column dimensions are structural CSS constraints. Font sizes, colors, radii, shadows and transitions must use tokens. There is one short hover transition (140ms); reduced motion removes it. No motion carries unique information. There are no delayed content insertions or loading simulations.

Use semantic forms, labels and real buttons. All controls have a 3px visible keyboard focus ring. A state transition moves focus to its heading; validation moves it to the first failed field; dialog dismissal returns it. Native Tab, Enter, Space, select keys and Escape are sufficient; no invented global shortcuts conflict with macOS.

Copy should describe ownership, certainty and the next action. Examples: “You’re still on call”; “No schedule yet”; “Priya is now responsible.” Avoid a reassuring color without the qualifying sentence.

## Before changing this UI

- Run the token guard and browser verification scripts.
- Inspect the real dimensions, both themes, all states and the narrow bank layout.
- Keep the fixture copy unchanged; take shared facts from EVAL_FIXTURES.
- Check Back, cancellation, failed validation, modal focus and explicit acceptance.
- Preserve every incident and its metadata, including the missing commander.
- Do not add live-looking claims or simulated backend results.
