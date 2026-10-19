# Harbour: banking at your own pace

Read this before changing the prototype. `app/tokens.css` owns visual values; `checks/tokens.cjs` guards token use, theme parity, contrast, wiring and the unmodified fixture copy.

## Purpose and priorities

Older customers moving from branch banking need to understand what happens next without losing access to familiar human support. Priorities, in order:

1. Read and operate comfortably: large type, generous controls, visible labels.
2. Understand one step at a time: one primary action, a named step and a familiar Back path.
3. Recover confidently: specific errors, preserved entries, reachable human help.
4. Stay safe: the fixture warning stays beside code entry and inside Help.
5. Recognise a welcoming bank: restrained character, no unfamiliar mechanics.

## Principles in this product

Familiar forms are the interface. No segmented code boxes, automatic submission, gesture-only navigation, or countdown pressure. A single code field supports typing, selection and paste.

Minimal never means missing. Labels stay visible, errors use words and colour, help includes a telephone number and a branch alternative.

The personal expression is the welcome: “Banking, at your own pace.” It acknowledges the change without treating older customers as children. The arched mark suggests a welcoming branch doorway and a sheltered harbour. It is inline vector artwork, with no external assets.

## Colour and type

This palette is a proposal: no bank brand guide was supplied. Warm paper recalls familiar printed banking material; harbour blue anchors actions. Dark mode uses a deep blue ground and pale teal actions, with the same semantic roles.

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| Ground | #f6f3eb | #142832 | Comfortable neutral reading surface |
| Main text | #182f3b | #f5f1e7 | Strong contrast without pure black/white glare |
| Supporting text | #50616a | #b9c8cb | Still readable, not faded out |
| Primary | #194859 | #b8dfdc | Navigation and action, never an error |
| Error text | #a32826 | #ffb4a6 | Always accompanied by a corrective sentence |
| Focus | #9c4b03 | #ffcd83 | Distinct from both errors and brand actions |

Full role values, including surfaces, borders and overlay, live in tokens.css. Guarded text pairs meet 4.5:1; meaningful input borders and focus meet 3:1. Hairline separators are decorative.

Locally bundled IBM Plex Sans gives open letterforms and clear numerals. It is a proposed product face rather than inherited branding. Type scale: 16px supporting text, 18px body, 20px labels/actions/lead, 26px wordmark/dialog title, 30px security code, 34px task title, 40px welcome title. The welcome uses 34px below 350px. All sizes use rem for text scaling; line height is 1.5 for prose and 1.12 for headings. Medium and semibold are used sparingly.

## Space, shape and layout

A 4px rhythm supports 8, 12, 16, 20, 24, 32, 40, 48 and 64px steps. The phone gutter is 24px, reduced to 20px at the smallest size. A 480px maximum column keeps longer lines readable on a laptop or TV. Both display parameters retain the same accessible task hierarchy.

Controls are at least 48px tall; primary actions and inputs are 60px. The 10px control corner is friendly without looking playful. The 18px dialog corner is reserved for an actual overlay. Surfaces group safety information; the form itself has no enclosing card. Dividers organise the welcome checklist.

Content scrolls naturally at short heights. No bottom action overlays a field or warning. The help dialog has a scrollable information region with a fixed heading and dismiss action; the close button remains visible at 320×568 and 200% text size. At large text sizes the header wraps rather than reducing type.

## Components and behavior

- Header: the bank name, simple mark, and text Help button. Help is not hidden in a menu.
- Navigation: named step count and a conventional Back button. Back keeps entered details during the current visit.
- Form: persistent labels, appropriate autofill/input modes, linked hints, linked errors, invalid state semantics. Validate on explicit submission.
- Code: one field, explicit confirmation, no visual example, no automatic advance. Wrong codes stay on the step.
- Help: native modal dialog, explicit focus loop, Escape and button dismissal, return focus to the exact trigger. Phone link delegates to the device calling app.
- Completion: confirms a practice setup, not account creation or a real verification. Finish clears entries and returns to welcome.

## Motion and writing

Only a 120ms ease-out button feedback transition. Reduced motion removes it; all information remains. No animation or delay stands between an action and its result.

Voice: plain, reassuring, adult. Error: “Enter the name on your account.” Success: “You’re all set.” Never claim a real text was sent or an account changed. Do not show the fixture code in UI copy.

## Accessibility and future checks

Native buttons, form labels, headings, landmarks and dialog semantics. Focus moves to the new heading, or first invalid field, with a visible 3px focus ring on interactive controls. A keyboard-focusable help information region allows scrolling without a pointer. The 3-step welcome list is an actual ordered list.

Before changing this UI: run both verification scripts; inspect the state contact sheet and full-size screenshots; check both themes, narrow phones, text enlargement, errors and keyboard navigation. Keep the warning verbatim from fixtures. Human testing with older customers and screen readers remains necessary before any production use.
