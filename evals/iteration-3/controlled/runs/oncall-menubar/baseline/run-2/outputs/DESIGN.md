# Rota — a clear owner, a deliberate handover

Open `app/index.html` directly from disk. No server, package installation, build or network is required. Open `review.html` for the explicit acceptance simulation.

## Design rationale

The first question for an SRE is “who has this shift?” The current owner therefore has the strongest type and the only grouped surface on the schedule. The next action is directly beneath it. The other current owners remain visible in aligned rows, without inventing a 40-person directory or future rota.

Priorities: responsibility correctness; fast recognition of owner and end time; safe handover; honest freshness; keyboard access. The 360px width and 640px maximum height are assigned constraints, not claims about an actual AppKit window. The utility uses macOS system typography, native form behavior, graphite neutrals and a proposed system-like blue. Amber is reserved for situations requiring care. This treatment fits a working menu utility; it is not proposed as a general house style.

The responsibility connection is the one unusual treatment: Jamie’s node is filled until Priya accepts. Priya’s node then becomes filled, while both names and plain-language responsibility labels remain. Its purpose is to make an asynchronous ownership change understandable without making a sent request look completed.

The frozen first-party images were inspected as a local contact sheet. Dia’s profile form and ordinary signup support straightforward labeled controls and restrained hierarchy. Arc’s routing sheet supports familiar dense utility forms; the recovery card illustrates giving a consequential fact a stable visual object. Dia’s composer closeup supports keeping context beside the action. Borrowed: familiar mechanics, contextual facts, one meaningful grouped object. Not borrowed: palettes, branding, AI-chat layout, recovery-card styling or signature components. The images are crops; neither their full flows nor current native platform behavior can be established from them. No online research was used.

There was no existing application to audit. The first implementation served as the measured baseline. Main fit at about 601px high; compose initially exceeded the 640px cap with 672px of content. The first refinement reduced composer spacing and the note field to two rows. Offline was simplified to the last-known primary shift rather than an apparently current roster. The second refinement increased input/secondary-control boundary contrast, explicitly colored placeholder text, and preserved the accepted/pending overview through its URL.

## Implemented behavior

- `?screen=main|compose|pending|offline|empty|accepted` opens every assigned state directly.
- `theme=light|dark` overrides the system. Without it, system color preference applies and updates when it changes.
- `display=laptop|tv` is accepted. Both use the assigned compact geometry; this is a menu app, so it does not become a wall dashboard.
- Jamie selects Priya, optionally adds a note, reviews the two named people, then sends. Review is also directly accessible with `screen=compose&step=review`.
- The native select offers only the supplied handover contact. Other current roster members are not assumed eligible substitutes.
- Sending enters pending and keeps Jamie responsible. Returning to the schedule shows “View pending handover.” Cancel request restores Jamie’s ordinary shift and announces cancellation.
- No timer accepts the request. In `review.html`, “Simulate Priya accepting” is a separate explicit action. It sends a local message to the preview and only applies when a handover is pending. The product canvas contains no simulation controls.
- Accepted shows Priya responsible until 18:00 UTC; returning to the schedule shows Priya on call and Jamie off call.
- Back, Cancel and Escape preserve a way out of composition. Back from review preserves the selected recipient and note within the page session.
- Pending and accepted overview state is reflected in `status=pending|accepted`, so reloading that overview preserves ownership status. Direct `pending` and `accepted` URLs also restore their own scenario.
- Offline uses the fixture snapshot time as its last-saved time, warns that the current owner cannot be confirmed, and disables handover. Retry retains the saved schedule and reports that offline continues.
- Empty has no roster or shift. Refresh honestly reports that this offline prototype has no schedule available.
- Semantic controls, explicit labels, visible keyboard focus, focus to new task headings, milestone announcements, reduced motion, and HTML escaping for user-entered notes.

## Intentional limits

This is an offline interaction prototype. It has no backend, authentication, notification delivery, real acceptance, network recovery, full staff directory, future/week schedule, rota administration or macOS menu-bar integration. Fixture UTC is used rather than inferring each staff member’s timezone. The supplied roster is four currently on-call people within a team of about 40.

Draft selection and note are in memory; a full page reload discards the draft and note. URL ownership scenarios persist, but no request is durably stored. Long notes can make the capped popover scroll. Native dismissal/reopening and host shortcuts require the actual AppKit shell. No real connection or fetch is attempted by Retry or Refresh.

## Verification

Run from the workspace root:

```sh
node outputs/verification/tokens.test.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/check-ui.py
```

The browser runner uses installed Playwright/Chromium, opens local file URLs, and needs normal sandbox approval in this environment. It saves representative screenshots and `verification/results.json`. See that result file for completed checks; this document does not claim live service or native-host validation.

Rendered critique: the owner is the first useful fact, controls stay conventional, and caution remains readable without color. The three weakest early details were the over-height composer, an offline roster that could imply freshness, and faint native field boundaries; each was changed and re-rendered. System font and native select are retained deliberately despite their less distinctive appearance, because this is a macOS utility used mid-task.

Not verified: VoiceOver speech on a real device, native AppKit anchoring/dismissal, remote services, actual colleague acceptance, live schedule freshness or operational suitability in a real incident. No dependencies were installed and the supplied skill and root fixture were not modified.

Potential method lesson: an ownership-transfer prototype benefits from explicitly modeling “request sent” and “responsibility changed” as separate actions and separate facts. This is recorded here only; the frozen skill was not changed.

Final completed checks: all 24 assigned URL variants passed at a 400×680 viewport (six states × two themes × two display parameters). Every popover was x20/y20, 360px wide, at most 640px high, with no horizontal overflow or internal vertical overflow in these direct states. All rendered controls met the 36px minimum height check. Keyboard focus styling, native type-ahead, note entry, review/send, Escape, request cancellation, pending-overview reload, explicit harness acceptance, accepted overview, offline/empty feedback, system theme changes and reduced motion passed. No page errors or HTTP(S) requests occurred. The token test passed for theme parity, text and control contrast, token use, stylesheet order and exact fixture-copy integrity. Screenshots of all six states in both themes and the note-bearing review were saved; both theme contact sheets were visually inspected, as were full-size main, compose, pending, offline, empty, accepted and review captures. No automatic test establishes VoiceOver or native menu-bar behavior.
