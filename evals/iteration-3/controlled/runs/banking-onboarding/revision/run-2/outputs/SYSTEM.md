# Harbour — a familiar way in

Read this system before changing the interface. Values live in `app/tokens.css`; run `node outputs/verification/design-guard.cjs` from the workspace root after changes.

## Purpose and priorities
Older customers moving some banking from a branch to a mobile app need confidence before speed.

1. Read and operate without precision: 18px body text, persistent labels, 52–60px controls.
2. Understand one next step: introduction, details, code, completion; no auto-advance or countdown.
3. Recover independently: plain field errors, retained entries on Back, consistent Help.
4. Stay safe: the fixture warning is beside the code; no usable example code appears.
5. Keep continuity with the branch: human telephone support and branch reassurance.

## Identity and roles
This is a proposed identity; only the name Harbour and fixture facts were supplied. Warm paper suggests the familiar correspondence a branch customer already reads; maritime blue gives action a steady, distinct role. Dark mode uses ink-blue surfaces and pale blue actions, rather than reversing every colour. The open harbour mark shows two protective posts over water. It is a simple inline SVG, with decorative status hidden from assistive technology.

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| Background | `#f8f7f2` | `#101f29` | Quiet reading surface |
| Main text | `#172f40` | `#f5f5ed` | Strong readable hierarchy |
| Secondary text | `#495e69` | `#bdcbd0` | Secondary does not mean faint |
| Action | `#19475c` | `#b5dce6` | One consistent next-step colour |
| Safety surface | `#e8efee` | `#203b47` | Separates the security instruction without alarm |
| Error | `#a12b26` | `#ffb5aa` | Failure only, accompanied by a repair sentence |
| Focus | `#9a5100` | `#ffd18a` | Clearly distinct keyboard outline |

No gradients, promotional imagery or ornamental cards. Space and fine separators group the short task. Error tint is reserved as a future token; current errors use text and input borders. No operational meaning depends on colour alone.

## Typography, space and shape
The supplied local IBM Plex Sans has open forms and a friendly, practical tone. It loads from disk; Arial is the fallback. Body 18px / 1.5; field labels 19px; secondary copy 16px; headings 32px / 1.15; the welcome heading is 40px on the wider phone and 32px on narrow screens. Semibold establishes labels and action; normal weight keeps paragraphs readable. User text enlargement remains possible.

Spacing follows the 4/8/12/16/20/24/32/40/48px token scale. Page gutters are 24px, reduced to 20px at 350px and below. Controls have 8px corners; the true overlay alone has 16px corners and a shadow. Number markers are circles, a familiar ordered sequence. The frame caps at 460px; it is a mobile task even on a laptop or TV URL.

## Layout and behaviour
Header: bank mark/name left, Help right. Then task heading, short explanation, fields or journey, and one primary action. Back remains above the step caption on details/code. The welcome CTA precedes branch reassurance so it is visible at the 320px floor. Long forms and errors scroll naturally rather than compressing text or pinning controls over content. Footer honestly identifies the practice environment.

Help is a native modal with a real telephone link, branch alternative, and a clearly labeled dismissal. It traps focus, closes with Escape, and returns focus to its opener. The compact copy keeps the whole modal within 320×568 at default text size; at enlarged text it can scroll. Page headings receive focus after a step change; invalid submission focuses the first invalid field. Inputs have explicit labels and error/hint descriptions; changed errors are politely announced.

## Motion and writing
120ms ease-out only for control colour changes. No motion conveys essential information. Reduced motion removes transitions. No time pressure, animated progress, or disappearing errors.

Voice: direct, warm, adult. “Let’s start with you.” “Enter an 11-digit mobile number starting with 07, or use +44.” “You’re ready, Alex.” Avoid infantilizing praise or unverified security claims.

## Guardrails and shipping checks
The guard script rejects literal component colours, off-token font sizes/radii/shadows/durations, missing token references, mismatched theme colour sets, altered fixtures and failing contrast pairs. Structural percentages, SVG geometry and breakpoint sizes are intentional exceptions to token-only styling.

Before a change is complete: check both phone sizes and themes, all URL states, keyboard flow, Back, modal dismissal/restoration, wrong and correct codes, 200% text, reduced motion, console errors and network requests. Real-device keyboard behaviour, screen-reader speech and bank brand approval require human validation.
