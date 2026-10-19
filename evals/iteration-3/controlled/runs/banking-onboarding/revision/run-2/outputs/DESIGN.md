# Harbour mobile onboarding

## Direction
A familiar bank, at the customer’s pace. This prototype is for older customers starting to use mobile banking after relying on their branch. The priorities are readability and comfortable touch targets, a clear next action, recovery without losing work, code safety, and continuity with human support—in that order.

The proposed Harbour identity uses warm paper, maritime blue and the supplied local IBM Plex Sans. No Harbour brand guide was provided. The open harbour mark is original inline SVG: two protective posts above water. Familiar forms and explicit words carry the interaction; personality comes from the composition, reassuring voice and coherent palette rather than unfamiliar gestures. Error red means only an error. Dark mode has its own ink surfaces and pale blue actions.

## Evidence and alternatives
Read the supplied `skill/SKILL.md` and its philosophy, method, identity, decisions, critique and case-recall references. No installed skills, external services, other workspaces or agents were used.

Inspected the offline `dia-profile-form.png` and `arc-recovery.png` references. The Dia crop places a plainly named task above a familiar input and separates cancellation from commitment: borrowed clear hierarchy and conventional form mechanics, not its compact desktop proportions. Arc’s recovery object separates sensitive information from surrounding explanation: borrowed a distinct, readable safety region beside code entry, not its dark card branding or recovery interaction. These are cropped official product/help images, not evidence of a complete onboarding transition or usability research with older customers. Sources and provenance remain in `reference-pack/SOURCES.md`.

There was no existing app to audit. Two actual-size compositions were rendered before implementation and retained in `research/`:

- **A, introduction first:** explains the two steps, offers branch reassurance, then enters the form. Selected because it establishes expectations before asking for personal details.
- **B, form first:** combines the welcome with both fields. Saves one tap but presents data entry before the customer has understood the process. Rejected against the confidence priority.

The comparison harness also opens the screen following each main action; `research/comparison.json` and the `*-next.png` images record those transitions. These are composition studies, not alternate production flows. The finished version further shortens the journey copy and puts the CTA before branch reassurance to fit the short phone.

## Running and direct states
Open `app/index.html` directly from disk. No server, build, dependencies or network is needed. Assets are packaged locally. `#app` is the document root container.

Example: `app/index.html?screen=code&theme=dark&display=laptop`.

| State | Behaviour |
| --- | --- |
| `welcome` | Two-step explanation; Set up the app opens details |
| `details` | Name and UK mobile fields; Continue validates |
| `details-error` | Direct error state with actionable inline messages |
| `code` | One labeled numeric-friendly code field, mobile ending, safety warning |
| `code-error` | Wrong-code explanation; never advances without the fixture code |
| `help` | Help modal immediately opens over the code step |
| `done` | Personalized, explicitly practice-only completion; Finish practice clears entries |

`theme=light` and `theme=dark` override the OS. With neither supplied, the system preference applies and responds to changes. `display=tv|laptop` is accepted in every URL; the app remains a centered mobile-width task on wide screens. There is no product-canvas review switcher.

## Implemented interactions and accessibility
The real path is welcome → details → SMS-code entry → completion. Name validation accepts Unicode letters, including a one-character name; empty or numeric-only names fail. UK mobiles accept 07 plus nine digits or +44 7 plus nine digits, with ordinary spaces and punctuation. These checks validate format, not account ownership. Fields retain entries when using Back or Help; sensitive values are kept only in page memory.

Wrong, incomplete and non-numeric codes show a repair instruction. Only `EVAL_FIXTURES.bank.testCode` completes setup. No test code or usable example is displayed. The unchanged fixture file is copied into `app/`; shared facts, warning, code length, code check, customer fallback and support telephone come from it. A practice notice makes clear that no SMS is sent or bank account changed.

Help offers the fixture telephone number as a `tel:` link and a branch alternative. It dismisses by Back to setup or Escape, traps Tab/Shift+Tab, restores focus to the actual opener, and preserves the underlying form. “I haven’t received a code” opens the same human-support route rather than claiming a resend occurred. The complete fixture safety warning remains reachable beside the code field after Help closes.

Semantic forms, buttons, headings and labeled inputs support keyboard operation. Each error is connected to its field and politely announced when changed. Invalid submission focuses the first invalid field; step navigation focuses the new heading. Focus uses a 3px contrasting outline with a 4px gap. Body text is 18px, labels 19px, supporting copy at least 16px. Controls are 52–60px tall; all tested interactive targets exceed 44×44px. No countdown, auto-advance or motion-dependent information. Reduced motion removes transitions. Text can enlarge to 200% without horizontal document overflow; long content and short screens scroll naturally.

## Verification and refinement
Commands from the workspace root:

```sh
node outputs/verification/design-guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
/private/tmp/design-compare-venv/bin/python outputs/verification/edge-checks.py
/private/tmp/design-compare-venv/bin/python outputs/verification/render-audit.py
/private/tmp/design-compare-venv/bin/python outputs/verification/research-check.py
```

Headless Chromium required normal sandbox escalation, which was approved. No packages were installed.

Completed automated checks and personally inspected screenshots/contact sheets:

- All seven states (including normal details) at 390×844 and 320×568 in light and dark: 28 combinations, no horizontal document overflow or JavaScript errors; no HTTP(S) requests.
- Full interaction path and a separate keyboard-only path; invalid details; wrong/correct codes; Back data retention; international-format phone; Unicode and long names.
- Help direct entry, Tab containment, Escape and button dismissal, opener focus restoration, correct telephone URI, and dismissal at 200% text. No actual telephone call was placed.
- URL and system themes, system-theme changes, reduced motion, enlarged text, wide laptop/TV query entry, target dimensions and semantic accessibility snapshot. These are browser checks, not a screen-reader speech test.
- Design guard: token wiring and references, matching theme colour sets, no literal component colours or off-token font sizes/radii/shadows/durations, fixture integrity, and 34 contrast pairs. Minimum tested text contrast is **5.83:1**; meaningful input borders/focus indicators meet 3:1. Results are in `verification/contrast.json`.
- Welcome initial-load CLS measured **0** in this local Chromium run. This is not a production performance claim.

Three rendered weaknesses were corrected: (1) the original Help content required scrolling to reach dismissal at 320×568; the compact sheet now fits at default text size, (2) the narrow welcome CTA ended at 639.6px, below the viewport; shorter list copy and reordered reassurance moved it to **500.6–560.6px**, fully within 568px, and (3) an unusually long unbroken name could overflow completion; headings now wrap safely. The keyboard check also led to explicit modal focus cycling. The final critique found the heading/action hierarchy clear in both themes and no overlapping elements. Short-phone forms intentionally scroll rather than reduce type size.

Individual screenshots show welcome, details errors, code, Help, completion, dark code errors, keyboard focus and enlarged text. The two `states-*-contact.png` sheets preserve viewport captures of every state/theme at both sizes. `verification/results.json` records the matrix; `edge-results.json` records additional checks.

## Deliberate omissions and evidence limits
No real account lookup, authentication, SMS sending/resending, delivery failure handling, rate limiting, account dashboard, banking transaction or server persistence. Reload discards typed data and opens the requested fixture state. No invented support hours or security certification. The support number is supplied test content; its real operation was not verified. The prototype does not claim an account was opened.

Physical device keyboards, VoiceOver/TalkBack speech, real bank identity/security policy, real SMS delivery, production timeout/lockout behaviour and usability with older customers remain unverified. The offline references cannot establish these. Brand and accessibility review with customers should precede production use.

## Handover
`SYSTEM.md` records the design decisions and tokens; `AGENTS.md` points future editors to it. Source inputs were not edited, and nothing was committed or pushed. A proposed lesson for the supplied method, left unapplied: on short-height mobile tasks, measure the primary action’s bottom edge as well as page overflow; a page can have no horizontal overflow while its first action still needs unnecessary scrolling.
