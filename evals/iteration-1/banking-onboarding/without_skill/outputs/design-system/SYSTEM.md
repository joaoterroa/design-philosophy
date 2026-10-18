# Larch onboarding: design system

The source of truth for how the onboarding flow looks and behaves. Values live in `../app/tokens.css`. `../checks/tokens.test.js` fails if `styles.css` uses a raw colour or font size, if light and dark disagree, or if a text pair drops below its contrast floor. "Larch" is a placeholder bank name.

## 1. What onboarding is for

An existing customer, usually 65 or older, who has banked in a branch for decades, wants to use the app. Often a family member suggested it, or their branch is closing. In priority order:

1. **Confidence.** They should never wonder whether they did something wrong, or whether money has moved.
2. **Finishing.** As few steps as the bank's checks allow, one question per screen.
3. **Safety.** Teach the one habit that protects them most (we never ask for codes) at the moment they are most attentive.
4. **A person is always one tap away.** Help is on every screen, with a phone number and the branch.

## 2. Principles

Adapted from the user's own system ("Recall", `design/SYSTEM.md` in the Technical Memory repo).

- **Familiar, then elevated.** Use what branch customers already know: sort code and account number (on their card, statement, chequebook, passbook), a text message code, a numbered passcode. Make them easier through layout and wording, not new mechanics. No swipe-to-continue, no hidden gestures, no carousels.
- **One obvious way.** One way to identify yourself (sort code, account, date of birth). One primary button per screen, at the end of the content. Back and Help are always in the same place, always as words.
- **Novelty where it pays.** The only moving element is the checking screen, because waiting on a bank is where people worry. Everywhere else is still.
- **Minimal is not hidden.** Say how long it takes, which phone the text goes to (ending 0471), how many tries are left, and that nothing has changed on the account when something fails.
- **Words over widgets.** "Step 2 of 4: Check it's you" rather than dots alone. "Done", "Checking", "Waiting" beside every status mark. Errors are sentences that say what to do.
- **Stable layout.** Space for the "taking longer" note is reserved, so nothing jumps under a reader's finger.

## 3. Colour

Warm neutral greys carry everything. Each meaning has one colour:

| Token | Means | Use for | Never for |
| --- | --- | --- | --- |
| `--accent` (deep blue / light blue in dark) | act, follow | Buttons, links, progress, the current check | Headings, decoration |
| `--err` on `--err-bg` | something needs fixing | Error summary, field errors, a failed check | Anything without a sentence saying what to do |
| `--ok` on `--ok-bg` | finished | A completed check, the "set up" mark | Anything still in progress |
| `--focus`, `--focus-fill` | keyboard focus | A 3px ring outside every control; yellow behind focused links | Anything else |

Contrast floors (checked): body and secondary text 7:1 (AAA) on every surface, because the audience is older and many have reduced contrast sensitivity; link/accent text 7:1; control edges 3:1. Dark mode is designed, not inverted.

## 4. Type

The phone's own font. All sizes in `rem` so the phone's text-size setting scales the whole flow (checked at 200%).

| Token | Size / line | Use |
| --- | --- | --- |
| `--fs-display` | 30/36, 700 | Screen question (h1) |
| `--fs-title` | 24/30 | Typed numbers, amounts, phone number, sheet titles |
| `--fs-body` | 19/28 | Everything else |
| `--fs-small` | 17/24 | Hints, meta. The floor: nothing smaller exists |
| `--fs-code` | 28 | Text code and passcode, widely spaced |

## 5. Space, shape, targets

- 20px side gutter. 4px spacing base.
- Buttons and inputs are 56px tall; every tappable thing is at least 48 by 48 (checked).
- Inputs have a 2px border at 4.4:1, sized to the number they hold (a day box is narrow, an account number box is wide), which tells people what to type before they read the hint.
- Hairlines separate list rows. One soft panel per screen for one grouped fact.

## 6. Components

- **Top bar.** "‹ Back" left, "(?) Help" right. Text links, 48px tall. Back is hidden where going back would be unsafe or meaningless (during a check, after finishing).
- **Step label.** "Step n of 4: name", with a four-segment bar that is decorative (`aria-hidden`).
- **Question (h1).** Phrased as the thing to do. Receives focus on every new screen so screen readers start there.
- **Field.** Label, then hint, then error, then input, in that order. Numbers use `inputmode="numeric"` (big keypad) but `type="text"` so leading zeros and spaces survive. Date of birth is three boxes (day, month, year), never a date picker.
- **Error summary.** At the top, receives focus, lists each problem as a link that moves focus to the field. The field gets a red left rule and its own message. Never colour alone.
- **Check list.** Rows with a status mark and a word. Current row pulses gently; reduced motion removes it.
- **Help sheet.** A modal bottom sheet with help for the current screen, then a person to call. Escape and Close dismiss; focus returns to Help.
- **Call box.** Phone number large and tappable, hours, "free from mobiles and landlines".
- **Text-message preview.** Shows what the real text will look like, including the warning, so people recognise it and spot fakes.

## 7. Motion

Only the checking pulse and the sheet rising (240ms ease-out). Loops run only while work is happening. `prefers-reduced-motion` removes all of it.

## 8. Writing

Plain, specific, calm. UK English. Say what happened and what to do next. Say "numbers", not "digits"; "text", not "SMS"; "code", not "OTP"; "fingerprint", not "biometrics". No exclamation marks, no jokes, no "Oops". Never blame the person: "This is a problem on our side, not with the details you entered."

## 9. Before you ship a change

- [ ] Tokens only; `node --test checks/tokens.test.js` passes.
- [ ] `python checks/render.py` reports no problems (targets, overflow at 320px and 200% text, keyboard path).
- [ ] Looked at in light and dark.
- [ ] Each new state says what happened, whether money moved, and what to do.
- [ ] Help on the new screen says something specific to it.
