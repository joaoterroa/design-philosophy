# Harbour: a familiar way in

Read this before changing the app. Values live in `app/tokens.css`; run `node outputs/verification/guard.cjs` from the workspace root to check token use, theme parity and contrast.

Harbour serves existing banking customers moving from branch visits to their first mobile setup. The identity is a proposal: no banking brand guide was supplied.

1. Make the next action clear, with a familiar linear flow and one primary button.
2. Keep reading and tapping comfortable: 18px body, 16px field hints, 56px primary buttons and fields, 48px navigation targets.
3. Make mistakes recoverable, with inline instructions, retained values, Back and Help.
4. Establish trust through precise security wording and an explicit practice-setup disclosure.
5. Preserve the route to a person and the relationship with the branch.

## Principles and character

The welcome prepares before it collects. Three ordinary steps explain the whole journey; input screens handle one topic at a time. No carousel, countdown, segmented code boxes, auto-submission or hidden gestures. The full code is one paste-friendly input. We never hide the safety warning behind Help.

Warm paper and navy recall a bank letter rather than a technical registration form. The Georgia headings give Harbour a calm, familiar voice; locally bundled IBM Plex Sans gives forms open, distinguishable letterforms. The original branch drawing makes the transition from branch to mobile feel continuous. The mark repeats its doorway at a simpler scale. Expression belongs in that welcome; form screens stay plain.

## Colour roles

| Role | Light | Dark | Use |
|---|---|---|---|
| Ground | #faf8f2 | #15242e | Warm paper / deep blue ground |
| Foreground | #172f3f | #f3f0e6 | Headings, labels, ordinary links |
| Secondary text | #4c5d67 | #c1ccd0 | Supporting text, never low-opacity |
| Primary | #193f51 | #c6dce4 | Main action; paired foreground tokens |
| Warning ground | #f2ead6 | #39372c | Security guidance, always written |
| Error text | #a12d25 | #ffb4a5 | Invalid input with a written remedy |
| Success text | #285d49 | #b2d4bc | Completion check with a text heading |
| Focus | #006c9a | #9bdbff | Keyboard outline; not an error |

Decorative gold and fine grouping rules do not communicate required information. Main text pairs exceed 6.4:1; primary text exceeds 10:1. Input boundaries and focus outlines exceed 3:1. Dark mode uses the same roles and a lighter action surface. Explicit URL theme wins over system preference.

## Type, spacing and shape

Body 18px/1.5; hints 16px/1.5; disclosure 14px/1.5; headings 36px/1.14; brand and code 28px; balance and dialog heading 32px. Text scales with rem. Weights: 400, 500, 600. No all-caps instructions. Account identifiers use tabular figures.

Spacing follows 4, 8, 12, 16, 20, 24, 28, 32, 40 and 48px. Horizontal insets are 24px, reduced to 20px at 320px. Input radius 8px; buttons 12px; grouped guidance 16px; modal 24px. The modal shadow signals a distinct interaction layer. Form fields use borders; extra cards are reserved for the account and security guidance.

The content column caps at 440px; it fills the phone at 320 and 390px. Pages scroll normally, without fixed buttons covering reading. The decorative welcome illustration is removed at viewport heights of 650px and below, bringing the action forward without shrinking text. Help fits a viewport-inset dialog and scrolls if text enlargement requires it.

## Behaviour, writing and motion

Voice: calm, direct, respectful. Error: “Enter your name as it appears on your account.” Code error: “That code doesn’t match. Check your text and try again.” Completion: “You’re all set.” No invented verification or security claims. The prototype never sends an SMS or changes an account; disclosures say so.

Input values live only in memory. Back preserves details; Help preserves partial input. The name accepts Unicode letters, mononyms, apostrophes, hyphens and spaces; mobile accepts UK 07, +44 and 0044 formats with normal separators. The fixture code alone completes the practice flow. No example or usable code appears in the interface.

Only hover opacity transitions, 140ms ease-out. No information depends on motion. Reduced-motion preference removes transitions.

## Accessibility and change checks

Native forms, labels, input purposes, error associations, invalid states, alert messages and landmarks. Screen changes focus their heading; failed submission focuses the first invalid field. Native modal dialog contains keyboard focus; Escape and “Back to setup” dismiss it and return focus to Help. The telephone action is a real `tel:` link; actual calling requires a device/phone application. Visible focus is reserved for interactive elements, not programmatically focused headings.

Before shipping a change: run both verification scripts, inspect the contact sheet and representative screenshots, recheck 320×568 and 390×844, light/dark, keyboard flow, modal dismissal and return, long content and 200% text. Human testing with older customers and VoiceOver/TalkBack is still required before any production use.
