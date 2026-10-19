# Rota — a shift, with a clear owner

[Open the app](app/index.html) · [Open the review harness](review.html) · [Design system](SYSTEM.md) · [Composition comparison](research/compositions.html)

Rota is a small macOS menu-bar utility for a team of 40 SREs. Its first answer is who owns the user's shift and when it ends. The handover is a request: Jamie remains responsible until Priya explicitly accepts. This implementation covers the opening menu-bar task only. The dashboard and banking clauses describe other tasks and are outside this app's scope.

## Priorities and constraints

1. Make responsibility unmistakable, especially during a handover.
2. Make choosing, reviewing, and sending deliberate and quick.
3. Keep the other current responders visible without implying a directory of all 40 staff.
4. Keep saved information honest when offline.
5. Fit a native-feeling, keyboard-accessible 360px popover in a 400×680 scene.

There was no existing app to audit. The supplied fixture is the factual baseline. The popover's 360px width, 640px maximum height, and x20/y20 placement come from the production contract, not an inferred macOS API limit. All shared facts come from the unchanged copy of `fixtures.js` through `EVAL_FIXTURES`. The clock is the fixture's 10:00 UTC snapshot; it does not simulate a ticking live connection.

## Reference evidence and interpretation

I read the supplied skill and its philosophy, method, identity, decisions, case-recall, critique, and system/guard templates. Offline first-party screenshots were the only visual research. Source attribution and crop limits are in the supplied `reference-pack/SOURCES.md`.

- **Dia's Create a Profile frame:** a restrained sheet, a clear heading, and explicit cancel/confirm controls give the task a boundary. Rota borrows that hierarchy and restraint, but uses persistent field labels instead of relying on a placeholder. No Dia colours, branding, or components are copied.
- **Arc's routing sheet:** labels sit beside familiar native controls, and the hierarchy remains quiet despite detailed settings. Rota uses conventional radio selection, a note field, and ordinary Back/Cancel controls rather than an invented handover gesture.
- **Arc's Recovery Card:** consequential information becomes a single recognizable object with its context attached. Rota's handover summary keeps sender, recipient, rotation, and shift end together from review through pending and acceptance. It does not copy the recovery card's black styling or security framing.

These are cropped published screens, not observed end-to-end sessions. They provide evidence about composition and control relationships, not proof of animation, accessibility, or complete product behavior. There was no external research, brand guide, native implementation, or live team data available.

## Composition decision

Two meaningful alternatives were rendered at an actual 360px width before implementation. The comparison is preserved in `research/compositions.html` and `verification/screenshots/compositions.png`; each also includes the proposed after-send relationship.

**Chosen: personal shift first.** The user's ownership, rotation, time range, and handover action form one reading group. Other responders sit below in a compact list. This is useful when opening a menu-bar utility mid-task: the actionable answer appears before the roster.

**Rejected: roster first.** Four equal rows make team coverage easier to scan, but push the user's responsibility and action apart. Its compact pending annotation also gives the ownership caveat less prominence. The chosen version accepts a little repeated context to make the personal task clearer.

## Identity

The palette is a proposal for this utility, not a claim about the user's general colour preferences. Neutral, slightly green-grey surfaces suit a quiet operational tool. Deep evergreen is the action colour in light mode; a pale counterpart maintains weight and contrast in dark mode. Confirmed ownership uses green words as well as a dot. Amber describes an unresolved request or uncertain saved data, always in a sentence.

System typography makes the utility feel at home on macOS. The bundled IBM Plex Mono is reserved for aligned roster times and UTC. A 23px title makes the rotation the visual anchor; 13px body text keeps the four-person current roster and task within the compact panel. Hairlines and consistent spacing do most of the grouping. Only the personal shift and handover object receive an inset surface.

The small rotation mark uses two opposing arrow paths: responsibility moves from one person to another. The transfer object is the distinctive moment; there are no novel interaction mechanics, decorative charts, looping status animations, or notification badges.

## Implemented behavior

| URL `screen` | Behavior |
| --- | --- |
| `main` | Jamie's Platform Primary shift, time range, snapshot-based remaining time and progress, and the other three current responders. One handover action. |
| `compose` | Choose Priya using a labelled radio row; Review stays disabled until selected. Optional 500-character note. Cancel and Escape return to the schedule. |
| `review` | Additional directly addressable state. Sender, recipient, rotation, shift end, and note are shown before sending. Back preserves the selection and note; Cancel abandons the draft. Direct entry uses the fixture handover recipient. |
| `pending` | Explicit waiting state. Jamie remains responsible. Return to the schedule preserves the pending request; the schedule offers View pending handover. Cancel request ends it and returns to Jamie's schedule. No automatic acceptance. |
| `accepted` | Priya's acceptance and ownership are explicit. Back to schedule shows Priya as current owner and removes Jamie's handover action. |
| `offline` | An amber saved-at warning, past-tense personal status and timestamped roster. The progress indicator is omitted. Handover is disabled. Try again honestly remains offline. |
| `empty` | No fabricated schedule or roster. Advises confirming coverage with the rotation owner. Check again stays empty and explains the result. |

Use `app/index.html?screen=pending&theme=dark` for example. All required menu states support `theme=light|dark`; without it, the system preference is followed and changes are observed. The menu keeps its specified dimensions regardless of an unrelated `display` query. Browser Back is supported. Within an active page, cancelled or accepted requests cannot be resurrected by history navigation. Returning from accepted/pending to the schedule carries ownership/request state in the URL.

**Explicit acceptance simulation:** open `review.html`, enter pending through the app or harness, then press **Simulate Priya accepting** outside the iframe. This sends a local event to the embedded prototype. It has no effect when no request is pending. The standalone app contains no test controls or pretend incoming response. Direct `accepted` remains available for visual evaluation.

## Accessibility and interaction

The app uses a labelled main landmark, headings, actual buttons, a fieldset/legend, labelled radio input and textarea, list semantics, a labelled progressbar, and live status messages for retry/cancel feedback. Decorative SVGs and initials are hidden from assistive technology. State transitions focus the new heading; Tab then reaches the relevant action. Review Back and Escape retain the draft. Visible focus is a 2px blue outline with a 3px offset. Primary targets are 40px tall; secondary text actions have at least 32px height for pointer use in a desktop utility; the radio's entire row is a target.

No information depends on colour or animation. Reduced motion removes hover transitions. Long notes wrap and allow the popover to scroll vertically, retaining the 640px maximum. Tab/focus brings below-fold actions into view. Nothing is horizontally clipped.

## Verification actually performed

Commands, from the workspace root:

```sh
node outputs/verification/design-guard.mjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
/private/tmp/design-compare-venv/bin/python outputs/verification/edge-checks.py
/private/tmp/design-compare-venv/bin/python outputs/verification/capture_study.py
```

Chromium needed sandbox escalation to launch; the local headless browser then ran successfully. No dependencies were installed.

- Captured and visually inspected **all 7 states in both themes** at 400×680, including the additional review state: 14 app screenshots. Full-size key screens and both contact sheets were reviewed, not just code.
- All direct-state popovers sit at **x20/y20**, are **360px wide**, and range from **368.22px to 639.72px high**. No horizontal or vertical content overflow occurs in those initial fixture states. Exact measurements are in `verification/results.json`.
- Exercised selection gating, note preservation, Review Back, sending, no automatic acceptance, return to schedule with pending state, cancellation, accepted schedule ownership, explicit harness acceptance, and honest offline/empty retries.
- Completed the handover and cancellation path with the keyboard, checked the visible outline and heading focus, tested Escape, and confirmed browser Back cannot restore a cancelled request.
- Tested a 500-character note including a long unbroken string: it wraps, vertical scrolling retains actions, and Escape preserves the draft. HTML-looking notes render as text.
- Checked explicit light overriding a dark system preference and automatic dark mode with reduced motion.
- Token guard passes: theme parity, no raw component colours/type sizes/radii/shadows, token wiring, fixture identity, and **40 contrast pairs**. Normal text's lowest tested ratio is **4.86:1**; the meaningful control boundary is at least **3.32:1**. Disabled controls are intentionally exempt from active-control contrast requirements.
- No JavaScript page errors. No HTTP/HTTPS requests during the edge checks. Measured layout shift after main load: **0**.

Machine-readable records: `verification/results.json`, `verification/edge-results.json`, `verification/contrast.json`. Screenshots are in `verification/screenshots/`.

## Critique and refinements

The first render's three weakest points were form height, pending-state height, and offline crowding. Compose initially exceeded the available interior by 8px, pending by 51px, and offline by 131px. Refinement reduced form gaps, compacted the pending icon and transfer connector, and consolidated offline warnings. Labels, names, times, and responsibility text were preserved. A second pass removed live-sounding wording from the saved roster and verified all states again. The final result gives the user's rotation first visual weight, keeps the ownership warning readable, and shows all four initial responders through the hero plus three rows.

## Limits and omitted production behavior

This is an offline HTML prototype, not an NSStatusItem integration. There is no real service, authentication, notification delivery, availability/eligibility lookup, staff directory, future schedule, request expiry, real retry, or persistence across a fresh page load. The only recipient provided for this flow is Priya; the UI does not imply that the other current responders are the full eligible staff list. Notes remain local to the current page and are lost on reload. The review harness explicitly simulates acceptance. Retry actions re-evaluate the local state and do not claim a successful network refresh.

Native menu-bar attachment/dismissal, production routing and notifications, real timezone requirements, VoiceOver on a native host, and usability with the actual SRE team still need human/device validation. Automated semantic and keyboard checks are not a full screen-reader audit. There is no loading animation because the supplied facts arrive synchronously from disk.

A possible improvement to the supplied method, recorded only: for menu-bar workflows, compare both the first screen and the ownership caveat after the main action before choosing a composition. A compact pending annotation may look economical while weakening the most important guarantee. The supplied skill was not modified.
