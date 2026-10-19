# Harbour: a familiar bank, within reach

Read this before changing the prototype. Values live in `app/tokens.css`; run `node outputs/verification/design-guard.js` from the workspace root after edits.

## Purpose and priorities

Older customers who normally bank at a branch are trying a new way of banking, on a small phone, potentially with limited vision or confidence. Priorities, in order:

1. Understand what to do next, without learning a new interaction.
2. Read and operate the flow comfortably, including with keyboard or enlarged text.
3. Recover from an error and reach a person without losing progress.
4. Understand code safety and the limits of this practice setup.
5. Feel a quiet continuity with a familiar institution.

## Principles in this interface

- One question per screen, one primary action. Labels remain visible above inputs.
- Information is preserved in normal document flow. Small screens scroll rather than shrink the text.
- Help is a word at a consistent location, with an actual telephone link and a branch alternative.
- Errors explain the correction in words, use the same red role, and focus the first invalid field.
- The distinctive moment is the completion receipt: the two promised steps return as two checked statements. It makes progress tangible without introducing a new control or animation.
- No simulated service activity, message-sending spinner, or countdown. Practice status is explicit.

## Identity and colour

No brand guide was supplied. This is a proposal derived from Harbour's name and its branch customers, not an established brand claim. Warm off-white recalls printed correspondence; deep blue gives text a stable visual anchor. IBM Plex Sans has clear forms and a substantial x-height, is bundled locally, and keeps a measured tone rather than an advertising voice. A small line mark suggests harbour walls and a beacon; the wordmark carries recognition, so the mark is decorative.

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| Background | `#f7f5ef` | `#14232d` | A warm reading surface / a low-glare blue surface |
| Main text | `#182c3a` | `#f4f3ed` | Strong continuous reading contrast |
| Secondary text | `#52616a` | `#b9c5ca` | Still readable, never a disabled-looking grey |
| Action | `#194c69` | `#b5d9ed` | One action role for buttons and the phone link |
| Grouped information | `#e9efef` | `#243b48` | Only the welcome overview and completion symbol |
| Error | `#a42e26` | `#ffb4a9` | Failures, always accompanied by words |
| Focus | `#9c5100` | `#ffd28d` | Distinct from both action and error |

The remaining surface, border, error-background and overlay tokens are in the token file. Hairlines divide regions; only the floating dialog receives a shadow. Informational separators are intentionally quieter than control outlines. No decorative accent palette.

## Type, spacing and shape

- Browser base remains 100%, respecting user text preferences.
- 16px support text, 18px body, 19px labels/buttons, 26px wordmark, 28px code input, 34px titles at the default browser size. All text sizes are rem-based.
- Body line height 1.5; titles 1.16. Weight 600 distinguishes labels and actions without uppercase instructions.
- Spacing scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64px.
- Mobile gutter 24px, 20px below 350px; reading width capped at 480px.
- Controls: at least 56px high; the safety disclosure at least 48px. Actual code input grows with its larger text.
- Control radius 10px; grouped overview and modal 16px. Circular step numerals communicate sequence, not interactivity.
- Focus is a 3px outline with a 4px offset. Borders have 1px and 2px roles.
- Breakpoints describe layout, not a device identity: small phone below 350px; bounded column above 700px. `display` does not override accessible responsive layout.

## Components and behaviour

The header contains the wordmark and Help. Forms have an ordinary Back control and text progress. The code is a single labelled input, supporting paste and one-time-code autofill instead of six separate focus stops. A safety sentence stays in the code step; elsewhere a native disclosure exposes it. A native modal dialog blocks background interaction, loops Tab between its actions, supports Escape, and returns focus to its opening control. Its body scrolls on smaller screens or with enlarged text.

Normal screen changes focus the main region; validation focuses the first invalid field. Back preserves values in memory. Finish resets values. Refresh resets entered values rather than persisting personal information to disk.

## Motion and writing

The local font is preloaded and resolved before initial content is inserted, with fallback rendering on font-load failure. This prevents initial text reflow without a simulated loading state. Only a 150ms ease-out hover response; no essential motion, autoplay or loading theatre. Reduced motion removes transitions. Copy is calm, specific and brief: “Enter a UK mobile number with 11 digits, starting with 07.” No blame, timers, confetti or banking jargon.

## Change checklist

- Run the design guard and browser verification.
- Inspect both phone sizes, both themes, and every direct state.
- Keep labels, target sizes, focus and disclosure semantics intact.
- Keep the fixture byte-for-byte unchanged and never show its usable code in product copy.
- Test Back, errors, modal dismissal and focus return after changing markup.
- Preserve explicit practice status and avoid claims of real authentication or SMS delivery.
