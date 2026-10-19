# Harbour mobile setup design system

Read this before changing the prototype. Values live in `app/tokens.css`; run `node outputs/verification/design-guard.cjs` from the workspace root to guard tokens, theme parity, contrast and fixture integrity.

## Purpose and priorities

Older customers are moving a familiar branch relationship onto a phone. They may have limited confidence with forms, SMS or mobile navigation. The interface should be patient without being patronising.

1. Make the next step and its purpose clear.
2. Keep reading, tapping and correcting comfortable.
3. Protect trust: explain the security code and distinguish the preview from real banking.
4. Keep a route to a person available.
5. Make progress feel finite, with a recognisable account at the end.

## Direction: a familiar relationship, closer to home

Use ordinary labeled forms, a single primary action and two plainly numbered steps. There is no carousel, gesture requirement, countdown or split code field. Colour carries action or error; text explains both. Back stays above the form. Help stays in the header, which remains available while scrolling.

The distinctive moment is completion: the customer's account appears as a quiet statement-like object with a familiar holder, sort code, account number and balance. It explains what setup gives them. The completion view is the endpoint, with no button that restarts onboarding.

## Identity and roles

No Harbour brand guide was supplied. This is a task-specific proposed identity, not an assertion about an existing brand. Warm paper evokes a familiar statement; dark ink supports reading; deep harbour blue marks actions. Dark mode uses deep blue-grey surfaces and pale blue actions, rather than inverting the page mechanically.

| Role | Light | Dark | Use |
| --- | --- | --- | --- |
| Background | `#f8f7f2` | `#14272d` | Page and modal |
| Surface | `#ffffff` | `#1c333a` | Inputs and account |
| Main text | `#1b3038` | `#f5f5ed` | Headings, labels, values |
| Supporting text | `#52616a` | `#b8c8ca` | Guidance and metadata, never disabled-looking |
| Action | `#155361` | `#b6dedc` | Buttons, links and meaningful marks |
| Error | `#a02f28` | `#ffb3a5` | Invalid fields and corrective words |
| Error surface | `#fff0ec` | `#432d2d` | Invalid input fill |
| Focus | `#9b4d00` | `#f7c78a` | Keyboard outline only |

All other colours, including the modal scrim and decorative hairlines, are in the token file. Error words and thicker borders reinforce colour. Hairlines around the account and numbered overview are decorative; field borders and focus outlines have separately checked contrast.

## Type, spacing and shape

Bundled IBM Plex Sans gives the bank a consistent, readable voice offline. IBM Plex Mono is limited to the code field to distinguish digits. Supporting copy is 16px, body 18px, labels and actions 20px, brand 26px, headings 32px and the welcome heading 40px (34px at the narrow breakpoint). Body line height is 1.5. Account numerals are tabular.

Use the token spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48 and 64px. The normal gutter is 24px and the narrow gutter 20px. Controls have 8px corners; the account and modal have 12px corners. Only the modal casts a shadow because only the modal floats above another task.

The content column caps at 440px. At 320×568, vertical scrolling preserves text size. Short-height welcome spacing is reduced so Get started fits the initial viewport. Do not shrink controls to fit more information. Inputs and primary actions are at least 60px tall; utility controls at least 52px. The header wraps when text is enlarged. Long account-holder names wrap rather than truncate.

## Components and state

- Forms use permanent labels and associated hints; placeholders never carry required information.
- Errors sit immediately below the relevant input, use `aria-invalid`, and are announced on submit. The first invalid field receives focus.
- The security code is one editable field, supports pasting and has a numeric keyboard hint. It never contains an example code.
- Help uses a native modal dialog, a labeled heading, an ordinary telephone link and a large dismissal button. Tab and Shift+Tab remain inside; Escape dismisses; focus returns to the opener.
- Navigation focuses the new heading. Form Back preserves values in memory. Nothing is saved to storage.
- The safety notice stays in the document, before confirmation, and is repeated in shorter form inside Help.

## Motion and writing

There are no animated transitions, timers or delayed reveals. The one-pixel press treatment is immediate. Reduced motion loses no content.

Voice: direct, patient, specific. Error: “Enter the full mobile number. A number starting 07 has 11 digits.” Success: “You’re all set, Alex.” Avoid claims of account verification, a sent text or live bank access. Preview notices state those limits explicitly.

## Before changing the UI

Run token/contrast checks, render all seven routes at both mobile sizes and themes, and run the interaction suite. Check keyboard focus, Help dismissal, form corrections, long names and 200% text. Record actual results in `DESIGN.md`. Browser tests support accessibility review but do not replace testing with older customers, a physical phone and a screen reader.
