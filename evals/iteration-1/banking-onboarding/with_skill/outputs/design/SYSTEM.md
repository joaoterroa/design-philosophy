# Harbour app onboarding design system: "Counter Service"

This is the source of truth for how the Harbour onboarding flow looks and behaves. Read it before changing the UI. Values live in `app/tokens.css`. `tests/design.test.js` (`node --test tests/*.test.js`) fails when code uses a value that is not a token, when light and dark disagree, when text drops below this product's contrast bar, or when the page blocks zoom.

"Harbour" is a placeholder name. The palette is a proposal, not a brand. When the bank's brand guide arrives it replaces the act colour and the wordmark (see section 3).

**Direction in one sentence:** the app should feel like being served at the counter by someone patient: one question at a time, in plain words, with the thing you already hold (your card) as the way in, and a person always one tap away.

## 1. What it is for

Existing customers, mostly 65 and over, who have banked in a branch for decades and are setting up the app for the first time, often because their branch has reduced hours or closed. They do it once, at home, sometimes with a relative beside them, often with the phone's text size turned up. Many are wary of scams, and have reason to be.

In priority order (these break ties):

1. **Never lost.** Each screen asks one thing, says which step it is in words, and has the same Back and Help in the same places.
2. **Readable and reachable.** Large type that follows the phone's text setting; 7:1 text contrast; 56px targets; visible edges on every control.
3. **Safe, and seen to be safe.** Scam advice appears at the moment it matters (the code), not as a wall of warnings up front. Nothing is said that is not true.
4. **A person is one tap away.** Phone and branch help on every screen, never hidden behind a menu.
5. **Mistakes cost nothing.** Errors say what to change; entered details survive Back, errors and stopping; no screen times out.

## 2. Principles

**Familiar first.** Standard mobile form patterns: labelled fields, a full-width primary button, a Back button top left, Help top right. No gestures, no carousels, no icon-only buttons, no split one-digit-per-box code inputs (they break paste, autofill and screen readers).

**One question per screen.** The title is the question ("Tell us who you are", "Enter the code we've texted you"). Detail lives beneath it in sentences.

**Words over widgets.** "Step 2 of 4: Check it's you" is the progress indicator; the bar is a second signal. Errors say what is wrong and what to do ("The card number is 16 numbers. You've entered 12."). Ticks in the setup list also say "done" to screen readers.

**Explain the unusual, not the conventional.** A typed field needs no instruction. A one-time code, biometrics and "your branch hasn't gone anywhere" are new ideas for these users and get one or two plain sentences each.

**Stable, honest layout.** The message status line reserves its height before the text is sent. Setup steps fill in place. A slow setup says it is slow; a failed one says nothing changed on the account. Primary buttons follow the content instead of being docked to the bottom: at 200% text a docked bar would cover a third of the screen.

**Novelty where it pays: the text message, shown before it arrives.** On the code step, the app shows exactly what the text from Harbour will look like (sender, wording, where the code sits) with a status line that changes from "Sending your text…" to "Sent at 2:14pm" as the bubble arrives. It is the only animated, illustrated moment in the flow. It explains what is happening (a text is on its way, and this is how to recognise it) and puts the one scam rule that matters next to the code it protects: never read it out to anyone.

## 3. Colour

Warm paper and ink neutrals carry everything. White is kept for things you write in (fields, the message bubble, the help sheet), so "white box = type here" holds on every screen. Each other colour has one meaning:

| Token | Light / dark | Means | Use for | Never for |
| --- | --- | --- | --- | --- |
| `--paper` | `#faf7f2` / `#151412` | ground | page | fields |
| `--surface` | `#ffffff` / `#1f1d1a` | write here / overlay | inputs, message bubble, help sheet, secondary buttons | page background |
| `--sunk` | `#efe9df` / `#2a2723` | one grouped fact | the message preview, the account summary, the slow-setup note | decoration, more than one per screen in the normal state |
| `--ink`, `--ink-muted` | `#1b1a17`, `#47433c` / `#f4f0e9`, `#cfc8bc` | text | all text | — |
| `--line` | `#6f695f` / `#8f887d` | an edge you can act on | field borders, Back/Help borders, progress track | decorative rules |
| `--hairline` | `#d9d1c4` / `#3a3631` | separation only | list dividers, the help sheet rule | the only edge of a control |
| `--act` | `#1d3d6e` / `#a9c4f0` | act / go | primary buttons, links, progress fill, card highlight | errors, status |
| `--danger` + `--danger-tint` | `#8c1f15` + `#fbe8e4` / `#ffaa9e` + `#3b1d18` | needs you to change something | error text, error panels, error field edges | branding, emphasis |
| `--caution` + `--caution-edge` | `#6e4300` + `#a8690a` / `#f3c873` + `#c8902a` | safety advice | the scam line on the code step | errors, general tips |
| `--ok` + `--ok-tint` | `#175a2e` + `#e3f1e6` / `#96d8aa` + `#16301f` | done, confirmed | completed setup steps, "we sent a new code" | the primary action |
| `--focus` | ink / light ink | keyboard focus | 3px ring with a paper gap | anything else |

Rules:
- The palette is a reasoned proposal; no brand guide was available. Deep ink blue was chosen for act because it gives 10.8:1 with white labels and is far in hue and lightness from the red, amber and green meanings. With age the eye's lens yellows and blue/violet and blue/green distinctions weaken, so no meaning depends on telling two blues or a blue and a green apart, and nothing blue sits on yellow.
- When the bank's colour arrives: use it exactly for the wordmark and primary button fill if white text on it holds 7:1; otherwise keep it for the mark and use a deepened shade for text and buttons, and record the adjustment here.
- Text holds **7:1** (WCAG AAA) on every surface it appears on, in both themes, not just 4.5:1. Control edges and focus hold 3:1. The guard test checks every pair.
- Errors are words plus a tinted surface plus a thicker edge, never colour alone.
- Dark mode is its own palette: warm near-black rather than pure black (less halation for older eyes), lighter act colour with dark labels, tints dark enough that light text holds 7:1.

## 4. Type

System faces (SF Pro on iOS, Roboto on Android). They follow the phone's own text-size setting, render best, and are what these users read every day in Messages and Settings; a brand face would add nothing they need. Sizes are rem so the OS setting scales everything. Nothing is smaller than 17px at default size.

| Token | Size / line, weight | Use |
| --- | --- | --- |
| `--fs-title` | 28px / 1.2, 700 | the screen's question; the balance |
| `--fs-code` | 30px, tabular, 0.3em tracking | the code and passcode fields |
| `--fs-body` | 19px / 1.5, 400 (600 for labels and buttons) | body, labels, buttons, section heads |
| `--fs-small` | 17px / 1.5 | hints, step counter, asides |

Hierarchy is position and weight before size. Three sizes for reading, one for digits. Numbers that compare (balance, sort code) use tabular numerals.

## 5. Space and shape

- 4px base, steps 4, 8, 12, 16, 24, 32, 48 (rem, so vertical rhythm grows with text).
- **Horizontal insets are px** (`--gutter` 20px, `--inset` 16px). At 200% text, rem gutters doubled too and squeezed a 390px screen to a 240px column; px insets give enlarged text the width. Measured: the balance overflowed its panel at 200% before this change and fits after.
- Radii: fields 10px, buttons 12px, panels 16px, the sheet 20px. Nested shapes take smaller radii.
- Every control has a 2px visible edge (3px when in error). Hairlines are for separation only.
- One filled surface per screen in the normal state. Error panels and the "new code sent" note are situational and disappear when resolved.
- No shadows except the help sheet, which genuinely floats.

## 6. Layout

Single column, phone first: designed at 320px (iPhone SE at Zoomed display, small Androids), typical 390px, checked at 430px; max text column 34rem on larger screens.

Top to bottom on every step: bar (Back left, Help right; on the welcome, setup and done screens the wordmark replaces Back and Help stays put) → "Step N of 4: name" and bar → the question → its explanation → fields → primary button → secondary routes (a link such as "I haven't had a text").

Four numbered steps: Your details, Check it's you, Your passcode, How you log in. Welcome, setting up and done are not counted as steps, so the count never lies.

## 7. Components

- **Primary button.** Full width, 56px, act fill, verb-led label ("Start setting up", "Continue", "Yes, use fingerprint or face"). One per screen.
- **Secondary button.** Same size, surface fill, act edge and label. Used for real alternatives of equal standing ("No, I'll use my passcode"), never for a downgraded version of the primary.
- **Bar buttons (Back, Help, Close).** Bordered, 48px, words not icons. Older users miss borderless text buttons; the border says "press me" without relying on colour.
- **Text field.** Label above, hint below it, error above the field, then the field. 56px, white, 2px edge. Numeric keyboards for numbers. Card number groups itself in fours as typed and accepts pasted spaces and dashes.
- **Date of birth.** Day, Month, Year fields, labelled, because a date picker wheel spanning 1925–2005 is slow and error-prone.
- **Code field.** One field with `autocomplete="one-time-code"` (iOS and Android offer the code from the text), tabular large digits.
- **Passcode fields.** Masked by default (platform convention, and people set up with others nearby), one "Show numbers" toggle below both fields controls both.
- **Error summary.** On a submit with errors, a danger panel at the top lists each problem as a link to its field and takes focus, so a screen-reader or zoomed user lands on what to fix.
- **Message preview.** The novelty component (section 2). Sunk panel, white bubble with the sender line and the code as blanks, status line with reserved height, then the safety line with a caution edge.
- **Setup list.** Three named steps that tick in place. The active step's ring turns only while work is happening; with reduced motion it becomes a static dotted ring and the words "in progress" remain for screen readers.
- **Help sheet.** Bottom sheet, modal, focus moves to its title and returns to Help on close; Escape and the scrim close it. Content: help for this step first, then "Talk to a person" with a call button and branch option.

## 8. Motion

One easing (`--ease`), 150ms for presses, 220ms for arrivals. Motion explains three things only: the text message arriving, the help sheet rising from where it lives, setup steps progressing. Reduced motion removes all animation; every state is still conveyed in words.

## 9. Writing

Patient, plain, specific. Second person, contractions, short sentences, no jargon ("passcode", not "credentials"; "the long number on your card", not "PAN"), no exclamation marks.

- Error: "The card number is 16 numbers. You've entered 12."
- Slow: "This is taking longer than usual. You don't need to do anything."
- Failure: "We couldn't finish setting up. Nothing has changed on your account, and your details are saved on this phone."
- Success: "You're set up, Margaret."
- Limits are stated before they bite: "You can try 2 more times."

## 10. Brand

No mark yet: the wordmark is the placeholder name set in the system face. When the bank's logo arrives it goes in the bar's left slot on welcome, setup and done screens only.

## 11. Keyboard and accessibility

- On every screen change focus moves to the new question (h1) and the title updates.
- Errors: inline text prefixed "Error:" for screen readers, `aria-invalid` on the field, `aria-describedby` linking hint and error, focus to the summary or the field.
- Live region announces milestones only (setup slow, setup finished), not every tick.
- Help sheet: `role="dialog"`, `aria-modal`, the app behind is `inert`, Tab is trapped, Escape closes, focus returns.
- Zoom is never blocked. Hash routes in the prototype must not reuse element ids (a `#code` route once focused the input with `id="code"`).

## 12. Before you ship a UI change

- [ ] Tokens only; `node --test tests/*.test.js` passes.
- [ ] Looked at in both themes, at 320, 390 and 430px, and at 200% text, in every state (`python tools/verify.py`).
- [ ] No horizontal overflow, nothing clipped, every target at least 48px (the verifier checks these).
- [ ] The keyboard walkthrough in the verifier completes.
- [ ] Nothing above the reading point moves while content arrives.
- [ ] No new colour meaning, card or badge where a sentence would do.
- [ ] Every new message says what happened, what it means for the account, and what to do.
