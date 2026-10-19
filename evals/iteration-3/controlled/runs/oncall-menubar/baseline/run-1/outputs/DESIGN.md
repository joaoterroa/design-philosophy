# Rota — on-call handover prototype

Open **`app/index.html`** directly from disk. No build, server, dependencies, network requests or remote assets are required. Open **`review.html`** to exercise a separate, explicit acceptance event.

## Design rationale

The app serves roughly 40 SREs who need an answer in a brief glance: who is responsible, until when, and how to hand over safely. Responsibility comes first, followed by shift timing, the handover action, and the other currently on-call people. The four supplied roster entries are the current roster; they are not presented as a directory of all 40 staff. Priya is the only supplied handover candidate, and no other staff, availability, shifts or future schedule have been invented.

The direction follows the supplied philosophy: familiar controls, one clear action per stage, restrained colour, and explicit information rather than hidden details. The primary shift is grouped in one surface; the rest is a compact list. System typography, small corners and a floating shell suit a macOS menu-bar utility. A green responsibility label in the Jamie → Priya diagram is the single distinctive treatment: responsibility visibly stays on Jamie’s side while pending, then moves to Priya on acceptance. Text describes the same change for users who cannot see colour.

Trade-off: a radio choice makes the supplied recipient explicit and keyboard reliable; a searchable 40-person directory would imply data this fixture does not contain. Trade-off: both `display` values retain the required 360px utility layout; TV does not turn this menu-bar prototype into an unrelated wall dashboard.

## Reference evidence

Read the supplied skill and its philosophy, method, identity, decisions, worked example, critique and system/guard templates. Visually inspected all six local images in `reference-pack/` in a contact sheet. The Dia form/profile examples support conventional controls and restrained hierarchy; Arc routing supports compact, understandable settings; Arc recovery shows why a consequential object deserves a clear grouped treatment. Dia’s context example supports keeping decision context next to an action. This prototype borrows those principles, not the screenshots’ palette, branding, exact components, or signature layouts.

Evidence is limited to the frozen crops and `reference-pack/SOURCES.md`. The crops cannot establish full interaction flows, macOS API behavior, or a company brand. No external services, installed skills or other projects were consulted.

## Entry points

Append `?screen=<state>&theme=light|dark&display=tv|laptop` to `app/index.html`.

| State | Behavior |
| --- | --- |
| `main` | Jamie’s primary shift, 06:00–18:00 UTC, fixture time 10:00, and the other three current roster members. Opens compose. An in-session request changes the action to “View pending handover”; an accepted request names Priya as primary. |
| `compose` | Choose Priya with a labeled radio, optionally enter a note, then review. The review shows recipient, rotation, date, coverage and retained responsibility. Edit and Cancel remain available. Sending goes to pending. |
| `pending` | Jamie is still responsible. Return to the schedule without withdrawing, or explicitly cancel the request. No automatic acceptance. |
| `offline` | Last-known fixture snapshot saved at 10:00 UTC on 18 Oct, with a saved roster. No live progress indicator or handover action. Retry remains offline and announces the failure honestly. |
| `empty` | No schedule, no roster and no assertion that Jamie is off call. Refresh remains empty; return route is available. |
| `accepted` | Priya is responsible; Jamie is off call. Return to the schedule updates the primary owner. |

If no theme is supplied, appearance follows the system preference. Explicit light/dark overrides the system. Invalid state values fall back to main. The fixed fixture clock is used instead of the actual date/time. `fixtures.js` is copied unchanged and loaded as `EVAL_FIXTURES`.

## Acceptance and state

The separate review harness embeds the app. Open pending there, then press **Simulate Priya accepting**. That explicit parent-window message changes a pending request to accepted. The product itself has no test buttons or demo controls. Sending merely records a request in local prototype memory/session storage and never contacts a real person or backend.

Request status and note are stored in session storage where file-browser permissions permit, so a sent request survives reload in the same tab. The current screen is also written into the URL. Local storage failures are handled without blocking use. Direct pending/accepted URLs seed those states for review; the compose review substep is reached by normal interaction. Back from an empty fixture returns to the populated main fixture; it is a navigation demonstration, not a successful data refresh.

## Implemented and omitted

Implemented: all six direct entry states; normal choose/review/send/edit/cancel flow; pending ownership; separate acceptance; session recovery; safely rendered optional note; main owner update; offline and empty retries; explicit themes and system appearance; reduced motion; semantic labels and controls; keyboard operation, visible focus, focus management and polite milestone announcements.

Omitted: a native NSStatusItem/NSPopover host, actual menu-bar dismissal/reopen, global shortcuts, real schedule service, network reconnection, notifications, delivery timestamps/receipts, identity/authentication, Priya’s separate device, persistent multi-user synchronization, schedule editing, team directory/search, recipient availability/conflict checks and future rotations. There is no implied integration. A production handover would require atomic responsibility transfer, server confirmation and authenticated acceptance; those are outside this offline prototype.

## Verification

Run from the workspace root:

```sh
node outputs/verification/design-guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

Chromium required sandbox escalation in this environment because its macOS process rendezvous was blocked under the initial sandbox. The approved local headless run succeeded.

The browser suite checks 24 combinations: all six direct states × light/dark × laptop/TV in a 400×680 viewport. It checks the 360px document root at x20/y20, the 640px maximum, no horizontal overflow, headings and controls, and zero page errors or HTTP(S) requests. All six supplied states fit without vertical scrolling: main 626px, compose 569px, pending 572px, offline 636px, empty 462px, accepted 539px. The suite also checks minimum 36px button heights and zero settled heading movement over a 50ms observation. Long user-entered notes may scroll within the capped popover. Screenshots and two contact sheets are saved under `verification/`. See `results.json` for measured heights and `contrast.json` for all contrast ratios.

Interaction checks cover the keyboard path through recipient choice, note, review, edit and send; focus on changed headings; pending remaining pending; reload; return without withdrawal; cancellation; Escape; offline retry retaining saved data; empty refresh; separate harness acceptance and updated main ownership; system dark appearance and explicit light override. A 300-character note is checked for safe text rendering, wrapping and reachable actions. The interaction run uses reduced motion.

The token guard passes for both themes, including 30 contrast pairings. It checks declared foreground/surface relationships, not an exhaustive pixel-level accessibility audit. Real VoiceOver, native macOS integration, a physical TV, real backend behavior and user testing with SREs remain unverified.

## Rendered critique and refinements

1. The first main render was 34px taller than the popover’s content area. Reduced row padding and vertical spacing; all current roster entries and the footer now fit without scrolling.
2. The first offline version retained a progress marker and used a current-roster label. Removed present-tense progress, changed the section to Saved roster, and compacted the saved shift. Retry never implies a successful connection.
3. Native select keyboard handling was inconsistent in this headless macOS environment. Replaced the one-candidate dropdown with a standard explicit radio choice; Space now completes the tested keyboard path. Added a deliberately contrasted placeholder in both themes.

See `SYSTEM.md` for design tokens, rationale and future-change rules. Proposed lesson for the supplied skill: when an action changes operational responsibility, require a rendered pending-state check that verifies both the visible owner and the owner after returning to the main view. No skill files were modified.
