# Harbour mobile banking onboarding

Open `app/index.html` directly from disk. No build, server, installation or network connection is needed. The supplied fixture is copied unchanged to `app/fixtures.js`; the interface and verification read shared banking facts from `EVAL_FIXTURES`.

## Direction

Apply the supplied considered-design philosophy to a customer who trusts their branch but may not yet trust their own ability to use an app. Familiar labelled forms, a stable Help location, readable text, and a single primary action take priority over visual novelty. The identity is a proposal: paper-like neutrals, deep harbour blue and a locally bundled, legible sans serif. No banking brand assets, customer research or live banking system were supplied.

The one distinctive moment is the completion receipt. Two checked statements echo the two steps promised on arrival. This gives the user evidence of progress without a new interaction or an animation to interpret. See `SYSTEM.md` for values and rationale.

## Offline reference research

I read the supplied skill, philosophy, method, identity, decisions, critique and worked example, and inspected these frozen first-party images:

- `dia-signup.png`: borrow clear labels and a single decisive action. Do not copy its low-contrast placeholder treatment or compact form scale.
- `dia-profile-form.png`: borrow the tight relationship between a task title and ordinary form controls. Do not copy desktop dialog density or the surrounding browser aesthetic.
- `arc-recovery.png`: borrow making an important security/progress concept into a readable object. Harbour's completion receipt uses that reasoning; no recovery-card styling, secret preview or card controls are copied.

`reference-pack/SOURCES.md` provides provenance. These are crops and still frames, so they do not establish full flows, accessibility performance or interaction behaviour. No external research or other projects were consulted. There was no pre-existing app implementation to audit.

## Implemented

| Direct URL state | Behaviour |
| --- | --- |
| `?screen=welcome` | Context, start action, a two-step overview, Help, expandable safety warning |
| `?screen=details` | Additional normal state; labelled full-name and UK-mobile inputs |
| `?screen=details-error` | Explicit errors for both fields and a summary; values can be corrected |
| `?screen=code` | One six-digit input, mobile ending, full safety warning and help for a missing code |
| `?screen=code-error` | Wrong-code explanation; incorrect and incomplete codes cannot advance |
| `?screen=help` | Opens Help over the code step; telephone link, branch option, button and Escape dismissal |
| `?screen=done` | Personalised practice completion, a two-item receipt and Finish reset |

All states accept `&theme=light` or `&theme=dark`, and `&display=tv` or `&display=laptop`. The display parameter intentionally uses the same responsive app: there is no separate kiosk mode. With no theme parameter, the interface follows the system preference and updates if it changes.

The normal path is Welcome → account details → mobile code → completion. Name validation allows different writing systems and names without requiring an artificial two-word format. Mobile validation accepts UK `07` numbers and the equivalent `+44` form, with spaces, parentheses or hyphens. Only the fixture's exact test code completes the practice flow; it is never displayed or previewed. Back retains typed values during the session. Browser history and direct entry work. Help returns focus to the exact opening button and preserves values; direct Help returns to code. The telephone link uses the fixture's supplied number.

This is explicitly a practice setup. It sends no messages, authenticates no identity, changes no account, and shows no invented banking balance. No test-code hint, backend simulation, countdown or fake resend status appears.

## Accessibility decisions

- 18px body text, 19px labels/actions, 16px supporting text; all sizes respect browser text enlargement.
- Primary controls and inputs at least 56px high; safety disclosure at least 48px.
- Real buttons, forms, labels, inputs, a telephone link, native disclosure and modal dialog.
- Visible keyboard focus; error text is programmatically associated with inputs. Errors focus the first invalid input. Main regions receive focus after navigation.
- Help is labelled, modal, keyboard-contained and dismissible without a pointer. It scrolls when needed.
- A single code field supports paste and platform autofill, avoiding six tiny targets.
- Safety remains visible on the code screen and reachable in a disclosure elsewhere.
- No information depends on motion or colour alone. Reduced-motion mode removes transitions.
- At 320×568, longer forms and errors deliberately scroll instead of reducing type, compressing targets or fixing a footer over content.

## Verification and refinement

Run from the workspace root:

```sh
node outputs/verification/design-guard.js
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
/private/tmp/design-compare-venv/bin/python outputs/verification/extra-checks.py
```

Chromium required normal sandbox escalation in this environment. The first attempt was blocked when automatic approval review exhausted account usage; after the session resumed, approval succeeded and the checks ran.

The browser script opens the app through `file://`, captures all six assigned states at 390×844 and 320×568 in both themes, checks horizontal overflow, target heights, labels and dialog state, and exercises the complete flow. `verification/results.json` records the state matrix and main flow; `verification/extra-results.json` records the full 320px flow, Unicode names, `+44` input, incomplete-code rejection, visible focus, safety disclosure, 200% text at both sizes and long-name reflow. `verification/contrast-results.json` records 30 checked foreground/background pairs. The design guard also checks theme-token parity, token use for colour/type/radius/shadow/tracking, stylesheet wiring and fixture identity.

Screenshots are in `screenshots/`: four state contact sheets plus representative full-size captures. Contact sheets intentionally show the viewport, not the scrolled remainder of a long form.

Refinements from inspecting the rendered screens:

1. The first welcome heading occupied four lines at 320px and placed the start action too far down. It became a two-line heading, the overview now matches the two actual steps, and Get started precedes the overview. Its final bounds at 320px are y=307.9px to 364.4px, fully within the 568px viewport.
2. Native modal tabbing briefly put focus on the document body at the edge of the loop. An explicit Tab/Shift+Tab wrap now keeps focus between the phone link and dismissal button.
3. The first header had a fixed height. It now has a minimum height and can wrap under enlarged text. Error pages keep ordinary vertical scrolling instead of clipping actions. Long first names now wrap instead of widening the completion page.
4. A sequential-load check measured an initial code-screen layout shift of 0.066. Preloading and loading the bundled font before the first form render removed that movement; the final welcome, code and Help observations are all 0.

Completed checks include light/dark state matrices, wrong/incomplete input rejection, successful fixture-code submission, Back retention, both Help dismissal methods and focus return, direct Help, keyboard form entry, system-theme changes, reduced motion, text enlargement, and absence of network requests or console errors. Measured results and any additional checks are recorded by the script, rather than inferred from screenshots.

## Limits and omitted behaviour

No real SMS, resend, authentication, account matching, session expiry, secure credential storage, app dashboard, or bank-account change is implemented. Entered values are in memory only; refreshing loses them. Missing-code assistance leads to a person rather than pretending to resend a message. The telephone destination is supplied fixture data; service availability, opening hours and actual call routing are unverified. No real call was placed.

Automated Chromium checks and visual inspection do not replace VoiceOver/TalkBack testing, an actual phone keyboard/autofill test, or usability sessions with older branch customers. Initial layout-shift observations for local welcome, code and Help loads are recorded in `extra-results.json`; they cover this browser run, not real-device font loading. No formal WCAG conformance claim is made. A bank would need to establish the real identity/security flow and approved wording before production.

Suggested skill lesson from this exercise: on very short phone screens, check the first actionable control's position before spending vertical space on an onboarding overview. This is recorded as a proposal only; the supplied skill was not changed.
