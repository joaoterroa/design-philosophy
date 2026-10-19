# Rota: responsibility stays visible

Open `app/index.html` directly from disk. No server, build, dependencies or network are needed. `review.html` is a separate reviewer harness with an explicit **Simulate Priya accepting** action. Send a request inside its Rota preview before using that action. No simulation controls appear in the product.

## Priorities and direction

Rota serves approximately 40 SREs who need to glance at the current rotation while working elsewhere. The fixture contains four people currently on call; it is not the full staff directory.

1. State who is responsible and when their shift ends.
2. Make the current on-call roster quick to scan.
3. Let Jamie choose Priya, review, and send without accidentally transferring responsibility.
4. Distinguish pending, accepted, offline and absent schedules in words.
5. Keep the utility familiar to macOS and usable by keyboard.

The direction is a quiet, native-feeling utility: system typography, one compact popover, restrained surfaces, a blue action, and hairlines between roster entries. The distinctive moment is the two-person responsibility diagram. A solid outline belongs to the person responsible now; a dashed outline belongs to the intended recipient. Text explains both, so neither colour nor outline is required to understand the handover. Acceptance reverses the responsibility labels and outlines.

There are no decorative charts, staffing totals masquerading as a roster, or invented shift owners. The small opposing-arrow mark expresses a handover. The horizontal shift track represents 06:00–18:00, with one third elapsed at the fixture's 10:00 UTC reference time.

## Evidence and research limits

The supplied `skill/SKILL.md` and its philosophy, method, identity, decisions, case recall, critique and system/guard templates informed the work. The local reference pack was reviewed as frozen product screenshots; `reference-pack/SOURCES.md` supplies their provenance. No external services or other projects were consulted.

- Arc's routing sheet supports conventional select, Cancel and action controls. Rota borrows that familiarity, not Arc's styling.
- Dia's profile and signup crops support direct labels and quiet surrounding UI. They do not prove the behaviour of a complete onboarding flow.
- Arc's recovery card makes a consequential state into a legible object. Rota uses that reasoning for the responsibility diagram, without copying the card, palette or typography.
- Dia's composer crop puts relevant context beside an action. Rota shows the rotation and responsibility beside Review and Send.

The requested `dashboard/index.html` and `brand/guide.md` are absent from the supplied workspace, including the recovered session's initial inventory. No existing dashboard or authoritative brand could be examined. No supplied inputs were changed. Northwind's neutral presentation and Harbour's green action colour are proposals for these fixtures, not claims of brand fidelity. IBM Plex Sans and Mono are bundled locally.

## Implemented routes and behaviour

Append `?screen=<state>&theme=light|dark&display=tv|laptop` to `app/index.html`. Omitting theme follows the system and responds to preference changes. Omitting screen opens Rota. `display` affects the dashboard; menu and bank use their own size rules.

| Family | Direct states | Behaviour |
| --- | --- | --- |
| Rota | `main`, `compose`, `pending`, `offline`, `empty`, `accepted` | Select Priya, optional note, Review, Edit, Cancel, Send, pending schedule, cancel request, acceptance and updated roster |
| Northwind | `live`, `stale`, `surge` | First seven incidents in live/stale, all twelve in surge, metrics, all five service values, on-call people and complete resolved history |
| Harbour | `welcome`, `details-error`, `code`, `code-error`, `help`, `done` | Start, name/mobile validation, SMS code validation, Back, Help, support phone, completion and account details |
| Extra normal step | `details` | Error-free account details form, reached from welcome |

**Rota.** Choosing Priya does not send. Review shows the recipient, rotation, shift end and any note. Sending enters pending. Jamie remains responsible until the separate harness explicitly accepts. Returning to the schedule keeps a pending notice and a route back to the request. Cancelling keeps Jamie responsible. Acceptance updates the schedule to Priya. Offline uses “last known” wording, shows a last-sync time and offers no handover action. Empty says no schedule exists and provides Back. Popovers sit at x20/y20, are 360px wide and never taller than 640px. Long content, including the offline footer or long review notes, scrolls inside the popover.

**Northwind.** Every incident outside the separate resolved history counts as open, including Mitigated and Monitoring. The missing commander reads “Unassigned.” Durations, opening times, metrics and service values remain exactly as supplied; the fixtures' reference clock and displayed incident clock are not silently reconciled. Stale removes the live indicator, shows “Data delayed,” names the last successful update, and labels the information last known. The laptop uses normal page scrolling to keep all twelve incidents and resolved history reachable. After refinement, all TV states fit 1920×1080 without vertical overflow; no pagination hides incidents. TV spacing is tighter while incident titles remain 18px. Secondary metadata is smaller and needs closer viewing; room-distance readability still requires a real display check.

**Harbour.** Name and UK mobile fields have explicit labels, autocomplete, descriptive hints and inline errors. Blank/invalid input keeps the details step open and focuses the first error. The SMS field has a numeric keyboard hint and one-time-code autocomplete. A wrong code retains the input, explains the problem and never advances. Only the fixture's code completes the local flow. The usable code is never displayed or supplied as a placeholder. The safety warning remains in the code step and Help. Help is a native modal dialog with a telephone link to a person, focus containment, a close button, Escape dismissal and focus return to Help. The direct `help` route opens it over the code step. At 320×568, forms scroll rather than compressing text or hiding warnings. Banking text is 18px, labels 18px, hints/errors 16px, inputs and primary actions 56px tall; Help and Back are at least 48px tall.

## Accessibility and theme decisions

Real buttons, selects, forms, headings, labels, descriptions, a dialog, and an ARIA incident table provide structure. Re-rendered steps focus their main heading; validation focuses the invalid field. Focus rings are explicit. Handover review has Edit and Cancel; pending has Cancel and Back. Help restores the invoking control's focus. Status is always written as text. Light and dark palettes are designed separately, including native control colour schemes. Reduced motion removes transitions without removing information. No animation, timer or background event accepts a shift.

## Verification performed

The completed Chromium suite in `verification/check_all.py` opens the application using `file://` and checks **52 direct state/size/theme combinations**: six menu states at 400×680; three dashboard states at 1920×1080 and 1440×900; and seven bank states at 390×844 and 320×568, all in both themes.

It checks horizontal overflow, clipped text, popover geometry, incident counts, direct Help, no displayed fixture code, TV height, JavaScript errors and external requests. Interaction checks cover keyboard entry into handover, review/edit/send, pending responsibility, return/cancel, explicit acceptance, updated roster, invalid details, valid details, wrong/right SMS codes, Help button/Escape/focus return, direct Help dismissal, system theme, URL override, reduced motion and the actual separate review harness. **All passed; zero JavaScript errors and zero external requests.**

`verification/tokens_guard.cjs` verifies token use for colours/type sizes/radii/shadows, theme colour parity, stylesheet order, exact fixture copy, meaningful activity-bar contrast and 88 text contrast pairs. Lowest checked text contrast: **5.58:1**. Reports are `verification/results.json` and `verification/contrast-results.json`.

`verification/keyboard_checks.py` separately passes the handover and banking flows with keyboard input alone, verifies the visible focus ring and modal Tab wrap, and reaches the last laptop incident using End. Its result is `verification/keyboard-results.json`.

`verification/render_screens.py` captures all 52 combinations and the reachable review step. `screenshots/` contains selected full-size PNGs and contact sheets of every direct state. Rendered inspection covered both menu themes, TV and laptop dashboards, both bank sizes/themes, and the handover review. The saved files are actual Chromium renders.

Refinements found and verified during review:

1. The menu Back button was centred like a primary action; it now sits at the leading edge with a comfortable desktop hit area.
2. The offline roster heading still said “On call now”; it now says “Last known on call,” consistent with its warning.
3. Stale/surge TV views extended 34–45px below 1080; compact row padding and sidebar spacing retain every fact within the screen.
4. Native dialog tabbing could reach browser chrome, and an extra delayed focus restoration could interrupt fast typing after dismissal. Help now explicitly wraps Tab, uses native focus return for ordinary opens, and supplies focus return for the direct Help route.

Two browser assertions initially sampled asynchronous dialog/message events too early. They now wait for the resulting route or heading, and pass. The recovered session's failed Python launch and quota interruption are not counted as completed checks. Native select arrow events were not reliable in headless macOS; the keyboard-only test uses native type-ahead to choose Priya.

Run again from the workspace root:

```sh
node outputs/verification/tokens_guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/check_all.py
/private/tmp/design-compare-venv/bin/python outputs/verification/keyboard_checks.py
/private/tmp/design-compare-venv/bin/python outputs/verification/render_screens.py
```

Chromium may require permission to launch outside the filesystem sandbox. No dependency installation is needed.

## Omitted and unverified

This is a local UI prototype. It does not connect to scheduling, paging, SMS, banking or incident services; no requests or messages are sent. The displayed completion and accepted states represent local fixture transitions. There is no persistence across reloads, account provisioning, authenticated recipient, real SMS generation/resend, background sync, notification delivery, directory of all 40 staff, menu-bar installation, native popover dismissal, or real connectivity detection. Offline and stale are explicit fixture states. The harness's message listener is a local simulation, not a production acceptance mechanism.

Automated browser checks do not establish VoiceOver announcement quality, physical phone/SMS behaviour, real macOS menu-bar integration, screen magnification, or TV readability at room distance. These need real devices and people. No claim is made of a complete accessibility audit. No authoritative brand review was possible because the referenced brand file was not supplied.

A potential skill lesson from this task: for mixed-size state contracts, assert the physical TV height separately from horizontal overflow; a page can have no clipped text while still requiring an unseen final row to be scrolled. This is a proposed lesson only; the supplied skill was not modified.
