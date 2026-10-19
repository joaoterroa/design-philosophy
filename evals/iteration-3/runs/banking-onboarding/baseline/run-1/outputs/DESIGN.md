# Harbour: accessible mobile banking setup

Open `app/index.html` directly from disk. No server, build, installation or internet connection is needed. This implements the banking task only; the Menu and Dashboard clauses describe other tasks and are outside this opening request.

## Design decisions

The intended user is an older customer bringing an existing branch relationship onto a phone. Priorities are clear progress, comfortable reading and tapping, safe correction, and access to a person. The existing recovered Harbour implementation was continued, rather than replaced with a new design.

The supplied philosophy informed familiar controls, colour with a defined purpose, plain error sentences and rendered verification. The two-step overview sets expectations; details and SMS each get their own screen. Permanent labels, a single code input and large buttons reduce precision demands. The account summary is the distinctive completion moment: recognisable banking information in a statement-like layout.

The warm paper, dark ink, blue actions, simple harbour mark and bundled IBM Plex type are a proposed Harbour identity. No banking brand guide or original banking application was supplied. The mark suggests shelter above water; it is an identity detail, not an unlabeled control. Blue means action; errors use red text, thicker borders and tinted input fills. Light and dark are separately specified.

Offline reference research used `reference-pack/dia-profile-form.png`, `dia-signup.png` and `arc-recovery.png`, with provenance in `reference-pack/SOURCES.md`. The form crops support ordinary labels and straightforward actions; the recovery image supports making security information visible and concrete. These are limited still images, not evidence of complete flows or usability with older customers. Their branding, palette and component styling were not copied. No external research or services were used.

## Routes and implemented behaviour

All routes accept `theme=light` or `theme=dark`. Without it, the operating system preference applies. The generic `display` parameter is harmless; banking layout follows viewport width.

| Route | Behaviour |
| --- | --- |
| `?screen=welcome` | Two-step explanation and Get started; starts a blank details form. |
| `?screen=details` | Additional normal form route; accepts full name and UK mobile number. |
| `?screen=details-error` | Direct invalid example with an empty name and incomplete mobile number; both can be corrected. |
| `?screen=code` | One code field, masked mobile suffix, Help and the exact fixture safety warning. |
| `?screen=code-error` | Correctable code mismatch state; wrong or incomplete input cannot advance. |
| `?screen=help` | Opens Help over the code step. Call route uses the fixture number. Button or Escape dismisses with focus return. |
| `?screen=done` | Completion and the fixture account summary. This is the endpoint of the prototype. |

Normal flow: Get started → details → code → account summary. Details accepts UK `07…` and `+447…` mobile forms, with spaces, parentheses and hyphens tolerated. A short/blank name or invalid phone receives specific correction text. Validation focuses the first invalid field. Only the fixture's test code advances, and it is never shown as guidance, a notification or a preview code. No text message is sent; the screen says so.

Back returns to the preceding setup step and preserves entered details in memory. Browser history works too. Help is available from every screen, remains reachable while scrolling, and preserves underlying input. The telephone link opens the device's calling handler; it does not place a call automatically. There is no fake resend control or backend progress simulation.

The provided `fixtures.js` was copied unchanged. Customer/account defaults, bank name, code length, safety warning and phone come from `EVAL_FIXTURES.bank`. Completion uses the entered name when the normal flow supplies one.

## Accessibility and trade-offs

Text is 18px by default, labels/actions 20px and supporting text 16px, with generous line height. Buttons and fields are at least 52px tall (primary actions and standard inputs at least 60px). Visible keyboard focus uses a 3px outline with a 4px offset. Controls have semantic labels; errors have associated descriptions and a polite announcement. Navigation focuses the destination heading. Help traps keyboard focus and restores its opener.

At 320×568, form screens and the complete account summary scroll vertically. This preserves reading size and safety information instead of squeezing everything onto one screen. The welcome action is fully visible on initial load at both sizes. The header wraps at enlarged text sizes. No content depends on motion, colour alone, hover or a gesture.

## Verification performed

Run from the workspace root:

```sh
node --check outputs/app/app.js
node outputs/verification/design-guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/render.py
/private/tmp/design-compare-venv/bin/python outputs/verification/interactions.py
```

Chromium required the standard sandbox escalation on this Mac. Tests load the app via `file://`.

- 28 state/theme/viewport renders: seven routes × light/dark × 390×844 and 320×568. Checks cover horizontal overflow, target dimensions, runtime errors and the welcome action fitting the viewport. Screenshots and contact sheets were inspected directly.
- Four end-to-end flows cover both sizes/themes, blank and malformed details, valid international mobile input, incomplete/wrong/correct codes, Back, browser history, Help from multiple steps, Tab wrapping, Escape, telephone destination and focus restoration. A separate keyboard-only main flow passed at 320px in dark mode with a visible focus outline. Long-name completion also passed without widening the page. No HTTP or HTTPS requests occurred.
- System theme selection and explicit override passed. Both system themes were checked at 200% text on welcome, errors, Help and completion, including dialog content reflow. Reduced motion preserves the same information.
- Token/theme/fixture guard and 34 contrast pairs passed. Lowest checked text contrast is 5.45:1; field boundaries and focus exceed 3:1. Results are in `verification/contrast-results.json`.
- The render observer recorded zero load-time layout shift in the checked routes. Synchronous error insertion can move subsequent form content; focus is deliberately moved to the relevant input.

Refinement corrected the previously oversized Help dialog, added reliable Tab wrapping, allowed the enlarged header/telephone text to wrap, made long names wrap, tinted invalid fields, shortened the welcome overview and removed the completion button that restarted onboarding. Final contact sheets are `verification/contact-sheet-320.png` and `verification/contact-sheet-390.png`; viewport screenshots show the actual small-screen fold as well as full-page content.

## Limits and omitted behaviour

This is a local, in-memory prototype. Refreshing restores route-specific fixture defaults; no personal data is persisted. There is no real identity/account matching, SMS delivery, resend service, bank connection, PIN/biometric enrolment, live balance, branch locator or wider account navigation. No physical call was made. A production authentication and customer-support service must supply those behaviours and approved wording.

Screen-reader speech, physical-device keyboard/zoom behaviour and usability with older customers were not tested. Semantic labels, roles and keyboard behaviour were checked in Chromium, not certified against every assistive technology. No claim of full WCAG conformance is made.

The supplied skill was not changed. A useful task-specific lesson is to check the whole header and telephone link at enlarged text sizes early: large body text alone does not guarantee accessible reflow. No visual preference was written outside this workspace.
