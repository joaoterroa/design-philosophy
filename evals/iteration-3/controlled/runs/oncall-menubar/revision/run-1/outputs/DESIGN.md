# Rota — a clear handover

Open [the app](app/index.html) directly from disk. Use [the separate review harness](review.html) to complete the flow with an explicit simulated acceptance. No server, build, dependencies or network are needed.

## What the design serves

This is a brief visit to a menu-bar utility, often in the middle of other SRE work. The order of priorities is: current responsibility and shift end; a deliberate handover; the other current assignments; honest uncertainty; a small, familiar macOS surface. The team has about 40 SREs, but the four fixture entries are the current roster, not a staff directory. Priya is a known handover contact, not an invented fifth on-call assignment.

There was no existing application to audit. The first functional render became the baseline; its offline state overflowed and its secondary avatar text failed contrast. Both were corrected before delivery.

## Research and choice

Only the supplied offline reference pack and design skill were used. I inspected `dia-profile-form.png`, `arc-routing.png` and `dia-strategy-05.png`.

- **Dia profile form:** title, field and actions form one readable sequence; the cancel action stays visible. Applied here as choose → review → send, with a retained recipient and clear return route. The image is a cropped demo frame, so it does not establish the full interaction.
- **Arc routing sheet:** compact native controls retain explicit labels and values. Applied as a real native select, visible rotation and exact shift times. Its large sheet layout and toolbar are not suited to this tiny popover and were not copied.
- **Dia strategy closeup:** task context is kept with the action in one object. Applied as a shift object that keeps responsibility beside the handover button, then a two-person review object. It is published component art, not evidence of a full shipped flow.

No reference transition or live native app was available. No external research, services, installed design skills or other projects were accessed.

Two compositions were rendered at their actual 360px widths before implementing the final system. They are preserved in [the study](research/compositions.html) and [its screenshot](research/compositions.png):

| Composition | Benefit | Trade-off |
| --- | --- | --- |
| A: personal shift first — selected | Makes Jamie's responsibility and action the first useful content; accommodates explicit pending ownership | The wider team roster starts lower |
| B: team roster first | Fastest comparison of all four current assignments | Jamie's handover action follows the full roster and carries less context |

A better serves the opening task. The final version refines it with exact UTC times, a static elapsed rail and aligned name/role rows. It does not copy the study's illustrative “After sending” section into the product.

## Identity and visual decisions

The identity is quiet and operational: a proposed pine/sage palette, system typography, a single inset shift object and an otherwise flat roster. Native system type is chosen for a macOS utility, rather than importing the supplied Plex fonts. A two-stroke mark suggests one duty passing to the next; it is drawn in CSS and remains offline. There is no claimed existing brand.

Green identifies the assignment and primary action; words establish whether it is current, pending or accepted. Amber is reserved for continuing responsibility and stale data. Dark mode has a separate palette and light action fill. The meaningful novelty is the handover object: Jamie and Priya stay visibly separate until acceptance. There are no unfamiliar interaction mechanics.

The 360px width and x20/y20 placement are fixed by the contract. Main is about 613px high; offline about 613px. Everything fits under 640px at the assigned text size. `display=tv` accepts the same menu-bar geometry, rather than changing the app into a wall dashboard. The full design system, component rules and token rationale are in [SYSTEM.md](SYSTEM.md).

## Implemented behavior

| URL state | Behavior |
| --- | --- |
| `main` | Jamie's Platform Primary shift, 06:00–18:00 UTC; other three current assignments; handover action |
| `compose` | Native recipient choice, initially unselected; review disabled until Priya is selected; separate review step; Back preserves choice; Cancel returns; Escape backs out |
| `pending` | Priya has not accepted; Jamie remains responsible; cancellation and return to schedule; returning retains pending status during the loaded session |
| `offline` | Explicit last-known snapshot and warning that assignments may have changed; handover unavailable; retry remains offline and announces that fact |
| `empty` | No assignments; a useful next step and repeatable check that remains empty; return route |
| `accepted` | Explicit transfer to Priya until 18:00; Jamie released; return schedule reflects Priya as owner |

All support `?screen=<state>&theme=light|dark&display=tv|laptop`. Without a theme parameter, the system preference is used and changes are followed. All six direct URLs are deterministic starting scenarios. The review step is part of `compose`, not an additional required URL state.

In normal use: Hand over shift → choose Priya → Review handover → Send handover request. Nothing automatically accepts. In `review.html`, “Simulate Priya accepting” sends a local message that only applies to a pending request; the app then opens accepted. These simulation controls stay outside the product canvas. Cancellation releases no responsibility and sends no real notification.

The fixture timestamp, 18 October 2026 at 10:00 UTC, is the snapshot time everywhere, including the last-known offline snapshot. It is not the machine clock or evidence of a live sync. The elapsed rail is static at one third of the fixture shift. The original fixture file was copied unchanged to `app/fixtures.js`; shared facts come from `EVAL_FIXTURES`.

## Verification performed

The supplied Python environment with Playwright and local headless Chromium was used. Chromium needed normal sandbox escalation to launch. Browser contexts were explicitly offline in the final checks. No external requests or JavaScript/console errors were observed.

- **24 direct-state cases:** all six states × both themes × both display parameters, in a 400×680 viewport. Each root measured x20/y20, width 360px, height ≤640px, with no horizontal or vertical content overflow.
- **Keyboard:** Tab through the main flow, disabled review before choosing, native selection using P type-ahead, Enter to review/send, visible focus, Escape cancellation, review Back retaining the recipient and focus. Milestones have a polite live region; the native select has a visible label and description.
- **Responsibility:** pending does not automatically accept; return preserves pending status; cancel restores handover availability; separate explicit harness acceptance changes ownership, including on the return schedule.
- **Failure states:** offline retry retains the warning and unavailable handover; empty retry remains empty.
- **Theme and motion:** explicit light/dark, system dark preference, reduced-motion transition removal.
- **Contrast and size:** 30 checked text pairs are ≥4.73:1; four control-boundary pairs are ≥3.24:1. Every rendered button/select is at least 36px tall. Disabled controls are exempt from boundary contrast. Decorative separators are not used as sole affordances.
- **Layout:** measured initial layout-shift score was zero in the 12 audited theme/state views. There is no asynchronous loading; intended whole-view navigation changes the popover height. This does not claim stable layout during real network traffic.

Evidence: [state results](verification/results.json), [focus/layout audit](verification/audit.json), [contrast pairs](verification/contrast.json), [contact sheet](screenshots/contact-sheet.png), and individual screenshots in `screenshots/` (six states plus review in both themes).

Re-run from the workspace root:

```sh
node outputs/verification/tokens_guard.js
/private/tmp/design-compare-venv/bin/python outputs/verification/check_ui.py
/private/tmp/design-compare-venv/bin/python outputs/verification/final_audit.py
```

## Critique and refinements

The three weakest points in the first render were the oversized offline state, faint avatar initials and redundant return controls. Offline now omits the elapsed rail and uses a compact assignment; secondary text was darkened from `#5f6c64` to `#59675e`; compose/pending/accepted use one return path each instead of duplicating it in the header. A browser interaction test also caught malformed recipient-option markup, which was fixed and the flow rerun. The last pass strengthened control outlines to exceed 3:1. The final screenshots were inspected in both themes, including review, pending, empty, offline and accepted.

## Scope and evidence limits

This is a runnable UI prototype, not a native application or backend. It has no authentication, notification delivery, real roster lookup, live sync, permission checks, conflict handling, server cancellation or durable persistence. Priya is the only supplied handover contact; no availability claim or invented 40-person directory is made. Requests and changes live only in memory; reload uses the scenario in the URL. In particular, reloading `main` resets to the original fixture, while reloading `pending` or `accepted` restores that scenario.

The empty and offline retries re-evaluate the local scenario; they do not contact a backend or simulate a successful recovery. No artificial loading state is added for synchronous disk fixtures. Native menu-bar attachment, dismissal/reopening, VoiceOver announcements on macOS, larger accessibility text, actual network failure and production concurrency still need native/device and backend verification. Semantic structure and keyboard behavior were checked in Chromium; a real screen reader was not run. Native select type-ahead with P passed. Arrow-key popup selection did not commit in the headless test, so that specific native popup interaction remains a device check.

A future design-skill lesson from this exercise: for small popovers, compare the degraded state alongside the main composition early. A stale-data explanation can consume more height than the entire normal action area. This is a proposal only; the supplied skill remains unchanged.
