# Harbour mobile banking onboarding

The prototype is `app/index.html`. Open it directly from disk; no build, server, install or network is required. Fonts, styles, script and the unmodified fixture copy are bundled alongside it.

## Design direction

A familiar way in: keep the clarity and human support of a branch visit while introducing a short mobile flow. Priorities are comprehension, readable and operable controls, recovery, access to a person, and continuity with the bank. A serif wordmark and warm paper-like background suggest established banking; large Plex Sans text and uncluttered forms do the practical work. Navy means action, rust means an error, and green appears only at completion. These are proposals because no brand guide was supplied.

The only distinctive treatment is the account summary at completion, modelled on the familiar clarity of a passbook or printed account slip. It uses the fixture's account facts rather than an invented balance or transaction history. The rest uses conventional controls, one action per step and visible Help.

The supplied skill and offline reference pack are the only design research. I inspected Dia's profile form and Arc's recovery card, and read the pack provenance. Borrowed: straightforward form mechanics, clear action hierarchy and treating a security-related outcome as an understandable object. Not copied: palettes, desktop window treatments, signature components or branding. These are isolated reference crops, not evidence of full flows or accessibility compliance. No interviews, analytics, banking brand materials or current app existed in the workspace; there is no prior implementation to benchmark.

## Implemented behavior

- Welcome → name and mobile → text-message code → completion. Welcome places the action before the supporting overview, so it remains immediately reachable at 320×568.
- UK mobile validation accepts 07 numbers or +447 numbers, with common spaces, parentheses and hyphens. The name requires at least two characters including a letter. These are input checks, not identity or account verification.
- Invalid fields show words, an icon, a tint and an error border. Labels stay visible; errors are programmatically associated. The first invalid input receives focus.
- Only a code equal to `EVAL_FIXTURES.bank.testCode` advances. No usable code is shown, including in Help or a preview. There is no code preview.
- Back retains name/mobile within the current page session. Code is cleared when details are resubmitted. No personal information is written to storage.
- Help is available on every screen, with the fixture's telephone link and a branch route. Escape and “Back to setup” close it and restore focus to Help. Keyboard focus is trapped while open. Its dismiss button remains visible on short screens, with content scrollable above it.
- The exact fixture safety warning is reachable on the code page and within Help.
- “Request a new code” reports a local practice request and explicitly says no text is sent. Finish resets the practice flow to welcome.
- Light/dark URL overrides and live system preference work. Both display flags retain the mobile layout. Visible focus, semantic forms, autocomplete hints, one code field, touch targets and reduced-motion handling are implemented.
- Practice status makes it clear no real account changes or SMS delivery occur.

## Direct states

Append `?screen=STATE&theme=light|dark&display=tv|laptop` to `app/index.html`.

| State | Opens |
| --- | --- |
| `welcome` | Introduction and start action |
| `details` | Empty details form, also reachable normally |
| `details-error` | Details form with actionable required-field errors |
| `code` | Empty code form; uses fixture mobile ending when no details were entered |
| `code-error` | Code form with wrong-code correction |
| `help` | Help dialog open above the code step |
| `done` | Completed practice setup and fixture account summary |

Unknown screen values fall back to welcome. Omitting theme follows the system. The URL updates to reflect normal navigation; reload opens that state but intentionally does not restore personal inputs. Direct links are independent review entry points, not secure authentication routes.

## Verification and refinement

Run from the workspace:

```
node outputs/verification/design-guard.js
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
/private/tmp/design-compare-venv/bin/python outputs/verification/visual-audit.py
```

Installed Chrome needed normal sandbox escalation to launch. Tests run against `file://`, not a development server. Results and screenshots are under `verification/`.

Verified all seven implemented states at 390×844 and 320×568, in both themes: 28 combinations, no horizontal overflow or page exceptions. The required six states are included. Verified validation, wrong-code rejection, fixture-code success, retained details on Back, telephone destination, button/Escape dismissal, focus trap/return, resend feedback and Finish. Completed the happy path with keyboard only. Checked system dark preference, explicit light override, display flag, and reduced-motion removal of transitions. All visible controls measured at least 44×44 CSS pixels; main controls are 52–60px high. Checked visible keyboard focus and 200% root-text reflow for every state in both themes.

The design guard passes theme colour parity, token use for styles, token stylesheet wiring, fixture-copy integrity and intended contrast pairs. Small text has at least 5.95:1 in light mode and 7.48:1 for the tested error pair in dark mode. Focus and input boundaries pass 3:1; exact pairs are recorded in `contrast.json`.

I inspected the individual renders and contact sheets. Refinements: fixed enlarged-text masthead overflow; moved the welcome action before the overview for short screens; kept Help dismissal visible above its scrollable content; shortened Help copy; made account columns stack when space is tight; and made programmatic heading focus quieter while preserving visible control focus. Full-page captures demonstrate reachable content below the initial viewport; short screens intentionally scroll rather than shrinking the text.

`results.json`, `layout.json`, `contrast.json`, four contact sheets and six individual screenshots document the final checks. The initial workspace had no rendered app, so no before/after layout-shift comparison is claimed. There is no delayed loading in this prototype; validation and navigation intentionally change the layout after a user action. No instrumented cumulative-layout-shift benchmark was run.

## Deliberately omitted and evidence limits

No backend, actual text delivery, code expiry, resend rate limiting, bank account lookup, live account activation, persistent login, transactions, consent workflow or identity checks. The completion page ends this onboarding exercise; it does not open a simulated banking dashboard. Browser history is not a second navigation system; use the visible Back action. Mobile keyboards and autofill are hinted, not validated on physical devices.

The tests establish prototype behavior, not production security or a WCAG audit. VoiceOver/TalkBack, real-device testing, call availability, true browser zoom, high-contrast OS behavior and usability sessions with older customers still need human verification. 200% text reflow was tested by increasing the root font size. No external accessibility library was installed.

A possible future skill lesson: for occasional users on short mobile screens, check the first action's visibility before polishing the overview; keep a modal's dismissal outside its scrolling content. This is a proposed lesson only; the frozen skill was not changed.
