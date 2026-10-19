# Harbour mobile setup: a familiar way in

Read this before changing the prototype. The source of truth for values is `app/tokens.css`; run `node outputs/verification/design-guard.js` from the workspace to guard token use, theme parity, text contrast and fixture integrity.

## Purpose and priorities

Older customers moving from branch banking need confidence before speed. In order:

1. Understand what to do next, without learning a new interaction.
2. Read and operate the interface comfortably, including with enlarged text and a keyboard.
3. Recover from mistakes without losing entered details.
4. Reach a person and see the security warning without navigating away.
5. Recognise the bank throughout the transition.

## Principles in this product

One labeled primary action per step. Familiar forms, one text-message code field and an ordinary Back button. Do not split the code across six boxes. Keep Help in the same place. Explain an invalid entry in words adjacent to the field, linked with `aria-describedby`. Do not add timers, urgency, decorative badges or animated progress.

The distinctive moment is the completion summary: a quiet, passbook-like account slip gives the digital transition a familiar banking object. The welcome page is restrained so this moment has meaning. The mark is a simple arched entrance: an invitation into the same bank, rather than a technology emblem.

## Colour and identity

This is a proposed identity, not supplied brand guidance. Warm paper and ink recall printed bank correspondence without imitating a particular bank. Navy carries action and links; rust carries errors; green is reserved for completion. Dark mode uses blue-black surfaces, pale ink and lighter action fills rather than mechanically inverting colours.

| Role | Light | Dark | Use |
| --- | --- | --- | --- |
| Background | `#f7f5ef` | `#15232c` | Main canvas |
| Surface | `#fffefa` | `#1d303c` | Inputs, account slip, phone group |
| Text | `#202d39` | `#f3f3eb` | Main content |
| Supporting text | `#52606a` | `#b9c7cd` | Guidance, never disabled-looking |
| Action | `#173e56` | `#bdd7e6` | Buttons and links |
| Error | `#a42d25` | `#ffb2a4` | Error words, icon and input border |
| Success | `#256149` | `#b2d4b9` | Completion check |

Errors also have a tinted background and a specific corrective sentence. Status never relies on colour. Every text role is checked at 4.5:1 or more against its used backgrounds; input outlines and focus at 3:1 or more. Detailed measured ratios are in `verification/contrast.json`.

## Typography, rhythm and shape

Locally bundled IBM Plex Sans provides open letterforms and a clear reading rhythm. Georgia is used only for the Harbour wordmark, for continuity with established banking. Local Plex Mono keeps the code easy to count. Body and labels are 19px at the default browser size, supporting copy 16px and nonessential metadata 14px. Titles are 34px, welcome 40px; narrow welcome titles use 34px. Weights: 400, 500, 600. No light type.

Spacing follows 4, 8, 12, 16, 20, 24, 32, 40, 48px. Mobile gutters are 24px, 20px below 350px. Controls are at least 52px high, primary actions and inputs 60px. Corners are 6px for inputs, 10px for actions, 20px for the floating help sheet. Hairlines separate the overview; avoid turning each step into a card. The account slip has one strong top rule. Shadows belong only to the modal.

All physical sizes, colours, radii, durations and shadow live in tokens. CSS media thresholds at 350px and 700px are structural constants; percentages, unitless ratios and SVG drawing coordinates are intrinsic geometry. Browser forced-colour keywords intentionally delegate to the OS.

## Layout and interaction

A single column, maximum width 512px; wider windows retain the mobile sequence. `display=tv` and `display=laptop` use the same accessible mobile composition. At 390×844 the hierarchy reads as bank, purpose, next action, overview. At 320×568 the first action remains in the initial viewport; supporting content scrolls naturally. At enlarged text the masthead wraps and account columns stack.

Help is a native modal dialog. Its content scrolls when needed, while the dismiss action stays visible. Focus goes to the heading on opening, stays within the dialog, and returns to Help on button dismissal or Escape. Form errors focus the first invalid field; advancing and going Back focus the new heading. Headings receive programmatic focus without a decorative ring; interactive controls have a 3px visible focus outline. No keyboard shortcuts beyond normal Tab, Shift+Tab, Enter and Escape.

No movement carries information. Optional 160ms ease-out colour/focus transitions are removed under reduced motion. State changes are synchronous and contain no loading layout shift; user-triggered errors add necessary corrective text below their field.

## Voice and truthfulness

Calm, concrete, respectful. “Enter a valid UK mobile number, including all digits.” “That code is not right. Check your text message and try again.” “Your branch is still here for you.” Do not patronise customers or imply a real SMS, account match or bank activation happened. Practice status remains visible in the footer and on the code/completion steps.

## Before changing the UI

Run the guard and interaction scripts. Inspect both themes at both required sizes. Check focus return, code rejection, typed-data retention and 200% text reflow. Keep fixtures unchanged and do not print the test code. Test with older customers and real assistive technology before drawing production conclusions.
