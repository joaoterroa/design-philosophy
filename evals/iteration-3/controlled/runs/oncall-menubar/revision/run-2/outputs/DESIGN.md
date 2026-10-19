# Rota — on-call, with clear responsibility

Open `app/index.html` directly from disk. No build, server, dependencies, account or network is needed. `review.html` is a separate review harness with an explicit “Simulate Priya accepting” action. The app itself contains no simulation controls.

## Product and priorities

For about 40 SREs checking a shift mid-task, the ordered priorities are: identify current responsibility and end time; make handover deliberate; keep pending and offline truthful; show the current roster; fit the macOS menu-bar context. Four people in the supplied roster are currently on call, not the whole team. Priya is the only supplied handover candidate; the prototype does not invent the remaining staff or anyone’s availability.

The fixture clock is Sunday 18 October 2026 at 10:00 UTC. Jamie’s Platform Primary rotation runs 06:00–18:00. There are eight hours left. All dates, the elapsed rail, times, roster and recipient derive from the unmodified copied `EVAL_FIXTURES`. Nothing uses the real machine clock to reinterpret this sample.

## Direction and evidence

The supplied “Considered design” skill guided this work. Offline reference evidence was limited to the provided PNGs and their source notes; no external research was performed. I inspected Dia’s profile form, Dia’s context composer and Arc’s routing sheet. Dia’s profile form groups a single decision above a clear action pair; Arc’s routing sheet demonstrates ordinary labeled native controls in a dense utility; Dia’s composer makes the context being acted on a visible object. Rota borrows those relationships: an explicit shift object, a native recipient select, and named sender/recipient continuity. It does not copy their branding, colors, chat interface or signature shapes. These are crops and static frames, not evidence of a complete transition or macOS menu-bar integration.

Two meaningful compositions were rendered at 360px before implementing the final design. `exploration/compositions.html` and `verification/compositions.png` preserve them, including their after-send treatments:

- A: own-shift object and handover action first, colleagues below, explicit custody after sending.
- B: all four people in an equal-weight roster, with the action following the list and pending marked within Jamie’s row.

A wins because ownership and the action appear before reading the roster. B gives more immediate row-to-row comparison but pushes the handover action below every person and makes pending easier to overlook. The chosen layout accepts some extra height for the ownership object. There was no pre-existing interface or code to audit; these studies are the initial baseline, not a claimed before/after improvement in an existing product.

The proposed visual identity is a cool neutral native-style utility with a modest blue action color, amber responsibility messages and green acceptance. System type fits macOS; a compact rotation mark and a proportional time rail give the product character without adding a new interaction. Dark mode uses independent surface, border and text values. The complete rationale and tokens are in `SYSTEM.md` and `app/tokens.css`.

## Implemented behavior

Every required state opens directly with `?screen=main|compose|pending|offline|empty|accepted`. `theme=light|dark` overrides the system preference; omitting it follows the system, including live preference changes. `display=laptop|tv` is recognized, with the same mandated popover dimensions in either mode. The app is rooted at `#app`, 360px wide, positioned at 20/20 in a 400×680 scene, with a 640px height limit.

Main → Hand over shift → choose Priya → optional note → Review handover → Send request → Pending. Review shows sender, recipient, rotation, cover period and the fact that Jamie stays responsible. Edit preserves the draft. A 240-character note is safely rendered in a keyboard-focusable, bounded scrolling note region if needed; the primary action remains visible. Back and Escape provide return routes, and cancel request restores Jamie’s unchanged responsibility.

Pending remains pending indefinitely until a separate action in the review harness simulates Priya’s acceptance. This is local state only. Acceptance shows Priya as responsible, then Back to schedule shows her cover from 10:00 to 18:00. Pending/accepted schedule status survives a reload through URL state; browser storage and a real backend are not used. An unsent note is held only for the current page lifetime.

Offline shows when the snapshot was saved, labels coverage as last known, provides no handover control, and retries without inventing connectivity. Retry feedback replaces text in reserved space. Escape does not convert Offline into a live-looking schedule. Empty shows no roster, provides an administrator next step and an honest refresh result. Its Back route returns to the prototype’s seeded main screen.

Controls are semantic and labeled. Native select supports keyboard type-ahead; Tab and Enter operate the flow. Visible focus, heading focus on view changes, focus retained after retry/refresh, a polite milestone live region and reduced motion are implemented. No macOS-wide shortcut is asserted.

## Rendered critique and refinements

The first render revealed Compose overflowing by 3px. Removing its duplicate bottom cancel route fixed it. An ornamental clock pushed Pending too tall; the heading already carried its meaning, so it was removed. The original Offline composition reused a live-looking timeline and was too tall; its replacement is an explicitly saved coverage summary. The “now” label was initially centered despite one-third elapsed time; it now aligns with the actual elapsed position. A later long-note test exposed review scrolling, and retry feedback initially added height: denser review details, a bounded note region and replacement feedback fixed both. Redundant top Back controls were removed from Pending and Accepted.

I inspected both theme contact sheets and representative individual renders, then the corrected long-note review. Ownership is first, names and times are aligned, amber is confined to responsibility, and all six direct states fit without clipping or internal popover scroll. The longest allowed note also fits the shell; its own region can scroll. Small metadata is an intentional desktop density trade-off, not a claim of readability on a distant TV.

## Verification performed

Run from the workspace root:

```sh
node outputs/verification/design-guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
/private/tmp/design-compare-venv/bin/python outputs/verification/visual_audit.py
```

The browser scripts need permission to launch local Chromium in this environment. No packages were installed.

- 24 direct renders: six states × two themes × two display values, checked for x/y, width, height and horizontal/vertical overflow.
- Keyboard-only recipient selection, note, review, edit and send, with visible 3px focus verified; edit retains the note; cancellation restores ownership; pending does not accept on a timer; main/reload retains pending.
- Explicit acceptance through the separate harness, accepted return/reload, and correct 10:00–18:00 cover.
- Offline retry, empty refresh, Escape return, focus retention, system theme, explicit theme override and reduced-motion behavior.
- No JavaScript/console errors and no network requests in the tested app paths.
- Token guard: no literal component colors, pixel dimensions or durations; all referenced tokens defined; dark color parity; CSS wiring; original and copied fixture byte equality. All 32 contrast pairs pass; minimum tested text contrast is 5.09:1. Focus and meaningful control/rail graphics are checked at 3:1.
- Semantic accessibility snapshot saved; final contact sheets include all 12 state/theme combinations. Short post-render geometry observations were stable and PerformanceObserver reported cumulative layout shift of 0 across the 12 state/theme captures; this does not measure real async data loading.
- Long-note review: 603px shell including borders, no popover overflow. Offline after retry: 638px including borders, no overflow. Raw measurements and results are saved alongside the scripts.

## Omitted and unverified

This is an offline browser prototype, not a native app bundle. Actual menu-bar anchoring, outside-click dismissal, system permissions, VoiceOver announcements, notifications, authentication, paging integration, network recovery, concurrent requests, server acknowledgment, real acceptance and persistence across separate app launches are not implemented or verified. There is no complete 40-person directory, future schedule, availability logic, administrative editor or unsupported “send” integration. The simulated acceptance time uses the fixed fixture clock. Real deployment would need server-authoritative custody and conflict handling before these actions could affect a shift.

The native macOS font and native select are used, but no claim is made that Chromium’s controls match every macOS release. TV distance reading, zoom/large text and a real screen-reader session remain unverified.

A possible method lesson from this exercise: a successful handover review should be verified with the maximum note length as well as the default form. This is a proposed lesson only; the frozen skill was not modified.
