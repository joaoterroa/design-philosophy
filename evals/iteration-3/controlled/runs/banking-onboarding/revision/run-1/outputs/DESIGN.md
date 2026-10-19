# Harbour mobile banking onboarding

The delivered direction is a single, readable column: familiar forms, a clear next action, patient wording and visible access to a person. Open `app/index.html` directly from disk; there is no build, server or network dependency.

## User priorities and evidence

The brief describes older customers moving from branches. Decisions are ordered by: comfortable reading and touch, clarity of the next step, recovery and human support, safety, then visual character. Small-phone dimensions and offline behavior come from the production contract. No existing application, bank brand guide, customer research, operating hours or real service integration was supplied. The Harbour palette and doorway mark are proposals, not claims about an existing brand. UK number validation follows the fixture’s UK banking context.

The frozen skill was read along with its philosophy, method, identity, decisions, worked example, critique and system templates. Visual research stayed within `reference-pack/`:

- **Dia signup:** visible labels, roomy fields and one obvious primary action. Borrowed that hierarchy, with larger type and touch targets appropriate here; did not copy its palette or compact control sizes.
- **Dia profile form:** one task inside a clear focus area. Applied this to Help, while retaining an explicit text dismiss action instead of relying on a shortcut.
- **Arc recovery card:** sensitive information is given its own visible object and a direct “do not share” message. Applied that reasoning to the safety warning beside code entry. No usable code preview is shown.

These are official supplied crops and still frames, not evidence of complete shipped flows, transitions, banking behavior or usability with older people. No external research was attempted.

## Composition decision

`review/compositions.html?variant=a` and `?variant=b` preserve two structural alternatives, with screenshots of welcome and the subsequent details screen.

**A, chosen:** a continuous paper-colored page with a short setup list and full-width action. Labels and fields remain on the same ground across steps. At 390px, the study action began around 575px; its corresponding details action around 511px.

**B, rejected:** dark introductory area with a separate white task sheet. This gives the welcome more ceremony, but creates a second visual region and moves the study welcome action to about 599px and details action to about 535px. The extra boundary carries little useful meaning for a customer learning mobile banking. The chosen layout trades that visual drama for continuity and room for readable text.

There was no pre-existing interface to audit. The composition studies are the initial structural baseline, not a claimed before/after redesign of a real app.

## Identity and system

Warm paper tones connect with printed banking material. Dark harbour blue gives actions a stable, restrained identity. Locally bundled Plex Sans has open forms and clear numerals. A simple arched doorway mark suggests a welcoming branch and shelter. Personality comes from the whole reading rhythm and the welcome, rather than novel controls.

The visual rules and reasons live in `SYSTEM.md`; all component visual values reference `app/tokens.css`. A 16/18/20/26/30/34/40px type scale, 48px minimum control targets, 60px main controls and a 20–24px mobile gutter support readability. Dark mode is a separate role-based palette. Explicit `theme` wins over system preference; otherwise changes to the system theme are followed.

The small-screen trade-off is deliberate: long forms and errors scroll rather than shrinking text or overlaying an action on content. Both display parameters preserve the same mobile task, centered on larger displays. There is no TV remote interface.

## Implemented behavior

| URL state | Behavior |
| --- | --- |
| `welcome` | Explains the three steps; Get started opens details. Help is visible. |
| `details` | Extra normal state for name/mobile entry. Visible labels, autofill hints and mobile input mode. |
| `details-error` | Directly opens two corrective errors. Submission validates a name and UK mobile. Errors are associated with fields; the first invalid field receives focus. |
| `code` | One labeled field for the fixture-defined code length; explicit confirmation. Mobile ending comes from entered details, or the fixture on direct entry. |
| `code-error` | Wrong or empty code cannot advance. Correcting it to the fixture’s code completes the flow. No fixture code is printed or previewed. |
| `help` | Directly opens a modal over code. Phone action uses the supplied number; branch support is an alternative. Button and Escape dismiss, with focus returned to the trigger. Tab and Shift+Tab stay within the modal. |
| `done` | Confirms practice completion honestly. Finish clears the in-memory entries and returns to welcome. |

All required states accept `?screen=<state>&theme=light|dark&display=tv|laptop`. An unknown screen falls back to welcome. Query changes are reflected in browser history. In-product Back preserves details during a visit. Help can also be opened from welcome, details, errors or done and returns to that screen when dismissed. The exact supplied warning appears beside the code and in Help, reachable through scrolling and keyboard navigation.

Personal entries are kept only in memory; reload does not restore them. The supplied fixtures were copied byte-for-byte into the app and read through `EVAL_FIXTURES`. They and the frozen skill were not modified.

## What is intentionally omitted

No SMS dispatch/resend, account lookup, identity verification, backend, account creation, balance/dashboard, password/PIN setup, branch locator or live support connection. The telephone link opens the device calling application; it does not simulate a conversation. Code help routes to a person rather than pretending to send another message. The UI explicitly identifies practice setup and says no text is sent and no account changes occur. No demo controls appear in the product.

## Verification and refinements

Commands from workspace root:

```sh
node outputs/checks/tokens.cjs
/private/tmp/design-compare-venv/bin/python outputs/checks/verify.py
/private/tmp/design-compare-venv/bin/python outputs/checks/study.py
```

The first sandboxed Chromium launch was blocked by the macOS launch-service restriction. The same local checks subsequently ran with normal approved sandbox escalation. No dependency was installed.

Completed automated checks:

- 28 direct renders: seven states × two mobile viewports (390×844 and 320×568) × light/dark. No page horizontal overflow and no visible control below 48px tall.
- Main flow with invalid details, corrected details, wrong code rejection, fixture-code success and Finish. Back preserves entries.
- Full successful journey by keyboard. Focus moves to the new heading or first invalid field.
- Help via both triggers; modal Tab containment, Escape/button dismiss, exact trigger focus return, direct-help opening over code and the fixture telephone link.
- System dark preference, explicit theme choice and reduced-motion preservation. Both display parameters accepted; readable centered layout checked at 1280×800.
- 200% root text scaling at 320×568 for welcome, details error, code error, help and done: no page overflow; Help’s dismiss action stays visible.
- Token guard, matching theme roles, token wiring, fixture integrity and 26 contrast pairs. Supporting text is at least 5.81:1 on its checked grounds; primary labels exceed 9.8:1 in both themes. Main text exceeds 10:1 on normal and safety surfaces.
- Initial-render CLS observed below 0.02 in this local run, including font swap. This is an initial-load measurement, not a network-loading benchmark. Explicit validation reflows are intentional, not asynchronous content insertion.
- Zero JavaScript page errors and zero HTTP/HTTPS requests.

`checks/results.json` and `checks/contrast.json` record actual measurements. `screenshots/all-states.png` preserves the complete mobile state matrix; five full-size representative screenshots preserve welcome, narrow details error, dark code error, narrow dark help and completion.

The rendered critique found three weaknesses. First, native dialog focus alone allowed Tab to escape in headless Chromium; an explicit focus loop fixed it. Second, long help content pushed the dismiss button below the small viewport; a scrollable body with a stable dismiss row fixed it. Third, error copy repeated too much information; shorter corrective messages reduced the reading burden. All affected states were rendered again and inspected. The two composition transitions were also rendered and inspected.

## Remaining evidence limits

Not tested with older customers, a real mobile device, a software keyboard, VoiceOver/TalkBack, a live telephone call, or Safari/Firefox. Semantic labels and keyboard operation were checked, but this is not a screen-reader audit or a claim of full WCAG conformance. The 200% check uses root text scaling rather than a physical device’s accessibility setting. Live delivery timing and real account security are outside this offline prototype.

A possible skill lesson from this task: when a modal targets a 568px-high phone and large text, test that its explicit dismiss action is visible before treating “scrollable” as sufficient. This is a proposed lesson only; the supplied skill remains frozen.
