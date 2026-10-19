# Northwind incident operations

Open `app/index.html` directly from disk. It needs no server, build, package installation or network. Default view is live/laptop with the system theme.

Examples:

- `app/index.html?screen=live&theme=dark&display=tv`
- `app/index.html?screen=stale&theme=light&display=tv`
- `app/index.html?screen=surge&theme=light&display=laptop`

All combinations of `screen=live|stale|surge`, `theme=light|dark` and `display=tv|laptop` are implemented. Omit `theme` to follow the system, including changes while open. `review.html` provides links outside the product canvas.

## Direction and evidence

The design follows the supplied considered-design skill. Priorities are urgency, missing ownership, data freshness, complete incident access, then historic context. The distinctive treatment is a single SEV1 exception row: severity, affected operation and unassigned commander can be read together. Other rows use familiar table mechanics. Northwind's navy, Fog and Plex type establish the identity; quiet hairlines replace cards, gradients and emoji. The exact brand orange is not needed for this read-only surface.

The original live dashboard was rendered at 1440×900. Its table began at y=678px; it displayed three open incidents despite reporting seven, mixed resolved history into that list, and did not show commanders. Its permanent LIVE badge supplied no stale-data treatment. The new table starts at approximately y=371px on laptop and y=355px on TV, with all fixture incidents available. The screenshot of the original is retained as `verification/before-laptop.png`. The source had no alternate states to baseline; those were implemented from the supplied contract.

Offline reference study used the six supplied product crops and `reference-pack/SOURCES.md`. Dia's profile/signup controls informed familiar labelled fields and disciplined grouping. Its icon-picker crop informed restrained, local interactions rather than a decorative navigation system. Arc's recovery card demonstrates giving an exceptional condition a concrete object; here the exception is the SEV1 row, not a copied card. The strategy composer crop supports putting context next to the task; here ownership and status remain in the ledger. These are limited still-image observations, not evidence of complete flows, timing or accessibility. No network research or external services were used. Reference palettes, shapes and browser-specific UI were not copied.

## Implemented

- Exact copied `fixtures.js`, consumed through `EVAL_FIXTURES`; no simulated requests or backend.
- Live/stale: first seven incidents. Surge: all twelve, preserving fixture order and facts. All supplied non-resolved statuses count as open.
- Four metrics, all five 30-day service counts, both on-call names and 18:00 handover, original open-count comparison for the seven-incident snapshot, and both resolved records.
- Missing SEV1 commander explicitly marked Unassigned in its row, contextual warning and details.
- Laptop search across ID, title, service, status and commander; severity filter; no-results and clear action. The KPI count stays the total, while the result count describes the filter.
- Read-only incident dialogs for open and resolved records, full facts, native modal focus handling, Escape/Close, outside-click dismissal and focus restoration.
- TV pagination with visible total and remaining count; laptop full-list document scrolling.
- URL themes and system preference; labelled native controls, scoped table headings, skip link, visible keyboard focus and live result counts. No animation or information lost with reduced motion.
- Token file, written system and guard script for visual values, theme parity, actual text/graphic contrast pairs and unchanged fixture copy.

## TV overflow decision

Readable rows take priority over fitting twelve incidents into 1080px. TV shows seven per page. Surge initially says “Showing 1–7 of 12 · 5 more open incidents”; Next reaches the other five, and Previous returns to the initial urgent incidents. It does not auto-rotate: the board never changes while an operator is reading. Space is reserved for seven rows on page two so context and resolved history stay in place. On an unattended TV, the initial seven stay visible until someone changes pages. All twelve remain reachable with search, filtering and normal scrolling on a laptop. The two resolved incidents stay separate on both displays.

## Fidelity and omissions

Fixture display time/date and duration strings are shown verbatim. They are not recalculated from the differently represented `now` timestamp. Staleness is 09:42 to the fixture's 11:00 display time, explicitly 1h 18m; the banner and footer warn that values may have changed. “Current snapshot” describes the assigned live/surge snapshot; the footer always identifies the app as an offline snapshot. The source's +2 open-incident comparison is retained for live/stale, but not projected onto the twelve-incident surge. The pages delta has no comparison period in the fixture, so its delta is shown as “↑ 5” without a comparison period.

No retry, polling, acknowledgements, commander assignment, incident editing, authentication, real backend, history beyond the two supplied resolved records, or saved filters are implemented. Those would imply unsupported capabilities or new facts. There are no demo state controls in the product. A compass logo asset was not supplied; the prototype uses the text wordmark without inventing a symbol. Actual TV distance/overscan, assistive-technology announcements and production connectivity require human/device checks.

## Verification

Run from the workspace root:

```
node outputs/verification/guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

The browser script also checks exact row facts, 44px incident targets, keyboard pagination and stable TV page geometry. It uses installed Playwright and Chromium, opens `file://`, checks all twelve combinations at their assigned viewport sizes, counts and source facts, missing ownership, resolved/service counts, TV pagination, laptop search/filter/empty results, dialogs, keyboard dismissal and focus restoration, system theme, skip link, and overflow. It records page errors and non-file network requests. See `verification/results.json` and `verification/contrast.json` for actual numbers. A small selection of full-resolution screenshots and a review contact sheet are retained.

Final recorded run: all 12 combinations passed. No horizontal overflow, page-script errors or non-file requests were observed. TV content ends at y=1062.3px within 1080px; laptop document heights are 1180px (seven incidents) and 1560px (twelve incidents), intentionally scrollable. The initial layout-shift observer recorded at most 0.000217. During the full scripted interaction sequence it recorded up to 0.025173; those runs include deliberate list filtering and document scrolling, so that total is not a passive-load measurement. TV pagination kept the resolved section within 1px of its initial position.

The token guard checks 40 text/graphic pairs. Minimum text contrast is 5.21:1; minimum tested graphic/focus contrast is 3.56:1. Native browser styling and every possible antialiased pixel are not assessed by that token calculation.

Rendered refinements: the initial TV render exceeded 1080px; TV spacing and row-height tokens were corrected. A flex rule exposed hidden pagination; an explicit hidden rule fixed it. Incident hit areas now include title plus metadata, giving 44px minimum targets without shrinking rows. Light teal was darkened for chart contrast. Browser tests exposed an asynchronous system-theme test assertion; that check now waits for the media-change event. These are recorded as verification corrections, not backend behavior.

Only the original live source could be baselined. The app's assigned states are checked; actual refresh/loading/failure transitions are outside this static prototype. Automated keyboard checks are not a screen-reader audit. Physical TV viewing and the approved compass mark remain production validation tasks.

Proposed lesson from this task, without editing the frozen skill: for a passive operations board, decide and document overflow behavior before selecting a row size; test the surge state at the physical display's resolution before polishing the normal state.
