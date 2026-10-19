# Harbour mobile banking setup

Open `app/index.html` directly from disk. No build, server, network or dependencies are needed by the app. The supplied fixture is copied unchanged to `app/fixtures.js`; shared banking facts come from `EVAL_FIXTURES.bank`.

## Direction and priorities

For older customers moving from branch banking, the order is: understand the next step; read and tap comfortably; recover from a mistake; reach a person; feel continuity with the bank. A guided welcome introduces three steps before collecting details. This costs one tap compared with an immediate form, but provides context before a sensitive request.

The proposed identity uses paper, navy, readable Plex Sans, familiar serif headings and an original small branch drawing. Brand guidelines and an existing banking implementation were not supplied, so there is no claim of existing brand fidelity or measured improvement over a previous app. This is a complete local prototype of the requested banking task. Menu and incident-dashboard clauses concern other tasks and are intentionally not implemented.

## Offline visual research and alternatives

Studied the supplied `dia-signup.png`, `dia-profile-form.png` and `arc-recovery.png` against their source descriptions in `reference-pack/SOURCES.md`. Signup shows a clear relationship between external labels, roomy fields and a single action; the profile frame demonstrates bounded modal scope and a clear cancel route; the recovery screen gives sensitive material a distinct object with nearby safety wording. Harbour adopts those relationships as large labeled fields, a native Help modal and a persistent security panel. It does not copy branding, the desktop scale, palettes or components.

Evidence limits: these are static first-party crops, including a staged component and partial frames. No full transition, older-customer usability evidence or live banking product was available. External services were not used.

Two different welcome structures were rendered before implementation: an overview with a three-step list, and immediate collection in an inset form. See `research/compositions.html` and `research/compositions.png`. The latter asks for personal data before establishing the process and gives the form a heavier frame. The guided version won against clarity and trust, accepting the extra tap. No preference for this palette is inferred beyond this task.

## Implemented behaviour

- `?screen=welcome`: introduction → “Let’s get started” → details.
- `?screen=details`: labeled name and mobile inputs, autocomplete, UK mobile validation, retained input, Back and Help. Names allow Unicode letters and mononyms.
- `?screen=details-error`: direct invalid state with helpful inline remedies, error summary and invalid field associations. Submission focuses the first problem.
- `?screen=code`: one six-digit SMS field, numeric keyboard hint, paste/autofill support, exact fixture security warning, change-number route, Back and Help.
- `?screen=code-error`: direct mismatch state. Wrong or incomplete codes cannot advance. Only the fixture testCode completes setup; it is never displayed as a suggestion or preview.
- `?screen=help`: opens a native Help dialog over the code step. A real telephone link uses the fixture number. Button and Escape dismiss; focus returns to Help. Help also works from all other screens without losing input.
- `?screen=done`: completion with the fixture account, balance and account identifiers. Safety guidance remains reachable through a disclosure and telephone link. Back returns to code.

Every URL also accepts `&theme=light` or `&theme=dark`; without it the app follows the system preference, including preference changes. `display=tv|laptop` does not alter the banking layout. Browser history works for step navigation. Native scrolling keeps content reachable at 320×568 rather than reducing text or covering it with a fixed action bar.

## Honest limits and omissions

This is explicitly a practice setup. No SMS is sent, no account is created or modified, no authentication backend is used, and no real identity check occurs. There is no misleading resend or loading state. Calling opens the device’s phone handler; no call is simulated. The fixture help number is used without independently verifying its service or availability. Input lives only in memory and clears on reload; there is no persistence of personal data. Production onboarding would need consent/privacy, real account matching, authentication, expiry/rate limits, secure session handling and a real account destination; those are outside this prototype.

## Verification and refinements

Commands from the workspace root:

```sh
node outputs/verification/guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

The browser script uses installed Playwright/Chromium. The app itself has no such dependency. See `verification/results.json`, `verification/contrast.json`, representative PNGs and `verification/all-states-contact-sheet.jpg`.

Verified all seven rendered states (including the intermediate details step), both themes, at 390×844 and 320×568: 28 combinations. No JavaScript errors or horizontal overflow. Exercised invalid/valid details, wrong/correct code, Back, changing mobile, input retention, Help by button and Escape, focus return, complete keyboard-only setup, explicit theme override, system theme and reduced motion. Additional checks at 200% text enlargement covered welcome, details error, code error, Help and completion at 320×568; there was no horizontal overflow, the safety warning remained reachable and the Help close button remained operable. No HTTP or HTTPS requests occurred. The guard checks stylesheet wiring, token references, literal component colors/type sizes/radii/shadows, theme parity and 24 contrast pairs. Text contrast is at least 6.44:1 among the checked normal text combinations; primary actions exceed 10:1. Fields/actions are 56px high or greater; navigation and disclosure targets are at least 48px. Inline telephone text inside the optional safety paragraph is an ordinary inline link.

Rendered critique identified three weak points and informed refinements: the Help heading had an irrelevant focus rectangle (removed for the programmatically focused heading, retaining control focus rings); requiring a surname excluded mononyms (validation now accepts them); the small-screen welcome spent too much height on decoration (illustration now omitted on short displays). Error screens and the code safety content use vertical scrolling at the smaller size. No asynchronous content is injected; no loading-related layout shift is introduced. A late font swap can still depend on device font timing; fonts are bundled locally and screenshots wait for them.

Still needed before production: testing with older customers, physical-device keyboard and text-size behaviour, VoiceOver/TalkBack review, verified support details, bank brand approval and backend/security integration. Browser and contrast checks do not establish formal accessibility conformance.

Proposed skill lesson: for a first-use flow aimed at occasional users, compare an explanatory welcome against immediate collection, then assess the smallest viewport with decoration removed before reducing essential text or targets. No skill files were changed.
