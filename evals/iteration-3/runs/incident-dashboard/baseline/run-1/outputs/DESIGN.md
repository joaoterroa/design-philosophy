# Incident dashboard redesign

Open `app/index.html` directly from disk. It needs no server, build, package installation or network. `review.html` is a separate state/viewport harness. All product states live in the `#app` root. Shared facts come from the unchanged copy of `fixtures.js`, through `EVAL_FIXTURES`.

## Direction

A calm operations board, with urgency tied to ownership. Read in this order: open count and severity, the incident requiring attention, its commander, then operational context. History remains distinct from open work. A single metric band and aligned table replace gradient backgrounds, emoji and rounded cards.

The supplied Northwind guide governs the dashboard. Exact Harbor Navy, Fog, IBM Plex Sans and IBM Plex Mono are retained. Orange is not used for body text. Teal chart colours are adjusted for contrast, documented in `SYSTEM.md`. Dark mode has its own legible blue surfaces, warning grounds and text values.

The distinctive detail is the severity-one row: the incident and missing commander share the same alert surface. Severity labels and the word “Unassigned” carry the meaning without depending on colour.

## Evidence and research

Only this workspace and the frozen `reference-pack` were used. Dia's signup and profile crops support ordinary labelled fields and explicit cancellation. Its composer crop supports grouping task context with the action. Arc's recovery crop supports treating consequential information as a readable object; the routing sheet supports familiar controls. Borrowed principles: restrained surfaces, context beside action, familiar forms and clear recovery. Their visual branding, browser chrome and layouts were not copied.

These are still images and source crops, not complete interaction evidence. No full-flow behaviour or motion is inferred from them. The supplied skill's philosophy, method, identity, decisions, case-recall and critique references informed the implementation. No external research or service was used.

Baseline: the original laptop table began at y=678 at 1440×900, leaving little room for incidents. It showed only three open incident rows while reporting seven. The replacement renders all seven fixture incidents and separates two resolved incidents. The original had no working controls, stale state or dark theme. Its large decorative cards and gradient competed with the incident content.

## Direct URLs and implemented behaviour

Append parameters to `app/index.html`, for example `?screen=live&theme=dark&display=tv`. All listed states open independently. An omitted theme follows the system and reacts to system changes.

| Family | `screen` values | Sizes |
|---|---|---|
| Dashboard | `live`, `stale`, `surge` | `display=tv`: 1920×1080; `display=laptop`: 1440×900 |
| Rota menu | `main`, `compose`, `pending`, `offline`, `empty`, `accepted` | 400×680 scene; root at (20,20), width 360, max height 640 |
| Harbour setup | `welcome`, `details-error`, `code`, `code-error`, `help`, `done` | 390×844 and 320×568 |

`details` is an additional ordinary account-details step, reached by Get started or Back. `theme=light` and `theme=dark` work for every family. Product navigation updates the URL, and browser Back restores the corresponding screen.

### Dashboard

- Live and stale show the first seven fixture incidents. Surge uses all twelve. Mitigated and monitoring incidents count as open; the two resolved incidents do not.
- Original metrics, five service totals, on-call names and resolved history are preserved. Missing commander remains explicitly unassigned. Fixture durations remain literal, rather than being recomputed against a different clock.
- Stale mode uses a prominent warning, the supplied 09:42 timestamp and last-known wording. It says counts, durations and ownership may have changed.
- TV surge deliberately uses two manual pages, seven then five incidents. Visible counts explain the extra work; Previous and Next keep every incident reachable. There is no automatic rotation. The final TV layouts fit the 1080px frame, including stale mode.
- Laptop surge includes all twelve rows in a normal scrolling document. Titles are not truncated. Selecting an incident opens a native details dialog, dismissible by close button or Escape. The same works for resolved history; TV omits its secondary service/opened line from the board and preserves it in the details dialog.
- All data is a supplied snapshot. No refresh timer, API connection or changing production clock is implied. “Current snapshot” describes the fixture state rather than a live backend.

### Rota

- Jamie can select Priya, add an optional note, review it, edit it, and send the handover request. Returning from compose cancels composition without sending.
- Sending enters pending and continues to identify Jamie as responsible. Acceptance never happens on a timer. “Simulate Priya accepting” is a distinct explicit prototype action; the responsibility changes only after that action.
- Cancel request restores Jamie's shift. Back to on call retains a pending request with a route back to it. Accepted returns to an off-call summary with Priya responsible. Local session storage preserves handover status and recipient on reload.
- The visible roster is the supplied four current on-call people. The footer's forty people refers to the team, not an expanded roster.
- Offline labels the last-known schedule, explains uncertainty and disables sending. The longer offline state scrolls inside the popover. Empty says there is no schedule and offers a return route.

### Harbour

- Welcome leads to name and UK mobile details, then SMS code, then account completion. Labels, large targets and plain errors suit occasional and older users.
- Empty/invalid details show field-specific guidance and focus the first invalid input. Valid UK mobile numbers accept 07 or +44 formats, including common spacing. Back preserves entered details within the page session.
- An incorrect or incomplete code stays on the code step with an error. The fixture's correct code advances. No usable example or code preview is displayed.
- Help gives the supplied telephone number as a call link, repeats the safety warning, and dismisses with either button or Escape. Focus returns to Help. Direct `help` opens the dialog over the code step.
- Completion retains the fixture account, sort code, account number and balance. User-entered name is carried through.

## Verification

Run from anywhere:

```
node outputs/verification/design-guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

The browser test uses installed Playwright/Chromium and local files only. Browser launch required a sandbox escalation in this environment. No dependencies were installed.

The scripts check all 48 required state/size/theme combinations, horizontal overflow, menu bounds and TV vertical fit. They exercise handover review/send/accept/cancel, pending reload and return, keyboard-only handover, invalid details, wrong and correct codes, modal dismissal/focus return, TV pagination, incident details, laptop access to the final incident, system theme and reduced motion. They also check console errors and the smallest welcome action's initial visibility.

The design guard checks token usage for colour/type/radius/shadow/duration, dark/light colour parity, text and chart contrast, stylesheet ordering and exact fixture-copy equality. Detailed evidence is in `verification/results.json` and `verification/contrast.txt`. A small standalone screenshot set and contact sheets covering all required renders are in `verification/screenshots/`. The contact sheets and representative full-size screens were visually inspected. Final results: 48 renders passed, no console errors, no horizontal overflow, and all TV documents fit 1080px. The laptop live view’s first incident begins at y=434. Maximum recorded layout shift across the local render matrix was 0.000625; this is a local-browser measurement, not a production guarantee.

## Critique and refinements

1. **TV context extended below the frame.** Reduced secondary spacing, put on-call roles on aligned rows, and compacted resolved history while retaining complete details. Added assertions for the full TV frame.
2. **Rota's team-size footer was below the main popover's initial view.** Tightened its shift and roster rhythm; longer offline content retains internal scrolling.
3. **The small banking welcome action fell below the fold.** Removed an unnecessary welcome navigation row and resized the account preview so the action is immediately visible at 320×568. The safety text remains reachable below it.

No animation is needed to explain these state changes. Reduced motion loses no information. A proposed future skill refinement: distinguish invariant structural dimensions from visual tokens explicitly, and require a viewport-fit assertion for unattended displays before judging their screenshots.

## Limits and omitted behaviour

This is an offline prototype: no real incident updates, notifications, schedules, SMS, account opening or cross-user acceptance. Handover persistence is local to the browser session; banking inputs are in memory and reset on reload. No auto-reconnect or resend is simulated. Help's phone link requires a device with a calling handler.

Only the supplied fields and roster are available. No unavailable team directory, incident timestamps or performance history was invented. The provisional compass and the Rota/Harbour marks need brand review; the supplied Northwind guide is unchanged. Rota and Harbour had no independent brand assets.

Automated contrast, native semantics, keyboard interaction and visible focus were checked. This is not a screen-reader certification. A physical ops-room TV, real viewing distance, glare, overscan, SMS delivery, telephone routing and production integrations remain unverified. TV pagination requires an operator; it intentionally does not cycle unattended or silently hide the remaining count.
