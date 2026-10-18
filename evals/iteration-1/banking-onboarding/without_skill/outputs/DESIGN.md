# Mobile banking onboarding for branch customers

## The ask and how I read it

"Apply my design philosophy to the onboarding flow of our mobile banking app. Users are older customers switching from branches. Keep it accessible."

There was no app code, brand or written philosophy for the banking app. I couldn't ask questions, so I made the assumptions below and recorded them.

**Which "design philosophy".** The only design writing of yours I could find is the "Recall" system for Technical Memory (`/home/user/vfuk-technical-memory/design/SYSTEM.md`). I treated its principles as your philosophy and carried them over: familiar then elevated, one obvious way, novelty only where it pays, minimal is not hidden, words over widgets, stable layout, and its writing rules (plain, calm, say what failed and what to do, no exclamation marks). I left out the Crossjoin red palette and the side-panel layout because they belong to that product's brand and form. If you have a separate philosophy document, this needs checking against it. That's the biggest open assumption.

**Other assumptions**
- UK retail bank (sort code and account number, UK English, Ofcom drama-range phone numbers so nothing real gets called). "Larch" is a placeholder name. The logo is a stand-in.
- People already have an account and a mobile number on file. Opening a new account is out of scope; it gets one screen that points to a branch or phone.
- Identification is sort code + account number + date of birth, then a text code to the number already on file. A real bank's fraud and KYC rules will set the exact checks. The screens are built so a step can be swapped without changing the pattern.
- A 6-number passcode is the login, and fingerprint is optional.
- Users are mostly 65+. Common needs at that age: lower contrast sensitivity, presbyopia, tremor or less precise touch, larger OS text sizes, some screen-reader or magnifier use, less trust in apps, and real exposure to impersonation scams. Many will set up with a relative beside them or in a branch.

## Research basis

Nothing was fetched live; this comes from what I already know.
- WCAG 2.2 AA as the floor, with AAA contrast (7:1) for text. Also 2.5.8 target size, 3.3.1/3.3.3 error identification and suggestion, 2.2.1 timing adjustable, 1.4.4/1.4.10 resize and reflow, 2.4.3 focus order.
- GOV.UK Design System patterns that test well with older and less confident users: one question per page, a date of birth as three boxes, an error summary that moves focus to the field, hint text above inputs, and a yellow focus highlight.
- Known problems with older users in banking apps: they abandon at identity checks, OTP boxes split into six fields break paste and screen readers, timeouts with no warning lose their work, icon-only navigation gets missed, and they fear that a mistake moves money.
- UK scam patterns: "safe account" transfers, courier fraud, and fake bank calls asking for codes.

## Direction

**Make it feel like the branch: someone tells you what's happening, you never feel rushed, and there is always a person to ask.**

The flow, one question per screen:

1. **Welcome.** What the app does, and that the branch, card and phone banking stay as they are. For branch switchers this is the main worry, so it comes first.
2. **Before you start.** What you need, about how long it takes, that you can stop, and that branch staff can do it with you.
3. **Step 1: Your account details.** Date of birth in three boxes, sort code, account number. "Where do I find these numbers?" opens a card diagram and lists the statement, chequebook and passbook.
4. **Checking.** Three named stages with a word beside each. If it's slow: "This is taking longer than usual… keep this screen open". If it's very slow: an option to stop, with the details kept. If it fails: "Nothing has been changed on your account and no money has moved… a problem on our side". If there's no match: what to check, then a phone number.
5. **Step 2: Text code.** Says which phone it went to, shows what the text will look like (including the "we never call to ask for it" line), and uses one input with `autocomplete="one-time-code"`. A wrong code says how many tries are left. "I have not received a text" offers to send it again, to **call and read the code out** (works on landlines and helps people with poor signal or eyesight), or explains what to do if the number has changed.
6. **Step 3: Passcode.** A "Show the numbers as I type" option. Easy-to-guess codes and the user's own date of birth are refused with a reason. Then a confirm screen, then an optional fingerprint screen where "Not now" is a full-size button, not a faint link.
7. **Step 4: Three things we will never do.** A scam warning at the moment of highest attention, which takes one tap.
8. **Done.** The account balance shows straight away so the effort pays off, and it repeats that nothing else has changed.

Every screen also has **Help**: a sheet with help for that step, then a phone number with hours. There's also a **timeout warning** that offers more time, keeps what was typed, and lets people stop and finish later.

## Key decisions and why

| Decision | Reason |
| --- | --- |
| Sort code + account number, not a card number or a scanned ID | People who bank in a branch know these and have them on paper; some passbook customers have no card. One way only, so no either/or choice to work through. |
| One text-code input, not six boxes | Paste and autofill work, screen readers read it as one field, and there's no focus jumping for people with tremor. |
| "Call me and read the code out" | Covers landlines, poor signal and low vision. Many older users already know this pattern from telephone banking. |
| Back and Help as words in fixed places | Older users often miss icon-only controls. Your principle: words over widgets. |
| Primary button at the end of the content, not stuck to the bottom | A sticky bar hides fields at large text sizes and with the keyboard open. The reading order matches the visual order. |
| 19px body, 17px floor, all in rem | Readable by default, and the phone's text-size setting scales everything (tested at 200%). |
| 7:1 contrast for all text | Contrast sensitivity drops with age; AA isn't enough for this audience. |
| 56px buttons and inputs, 48px minimum for anything tappable | Less precise touch. This is above the WCAG 2.2 AA minimum (24px) and the AAA one (44px). |
| Progress in words ("Step 2 of 4: Check it's you") | A bar alone doesn't say how far there is to go or what the step is. |
| Motion only on the checking screen | Your principle: novelty where it pays. That wait is where people worry, so a calm pulse with words shows the app hasn't frozen. |
| Failure copy says that no money moved | The biggest fear for this audience. Your principle: failures are said out loud, with the fix. |
| Scam warning built into the flow | High stakes for this audience, and it costs one tap. |
| Fingerprint is optional, with equal-weight buttons | Some people share phones or fingerprints with a carer; consent should be real. |

## Files

- `app/index.html`, `app/styles.css`, `app/app.js`, `app/tokens.css`: the prototype. Open `app/index.html`; it works from `file://` with no network. At the very bottom of the page is a "Prototype only" list that jumps to every state. Each state also has a URL, e.g. `index.html#checking-slow`.
  - Test values: sort code `11-11-11` runs the live slow path (normal, then slow, then very slow, then the code screen, about 20 seconds); `00-00-00` gives "no account found"; text code `000000` is wrong; passcode `123456` or your date of birth is refused.
- `design-system/SYSTEM.md`: principles, colour meanings, type scale, components, writing rules and a pre-ship checklist, in the same shape as your Recall doc.
- `checks/tokens.test.js`: guardrails (`node --test checks/tokens.test.js`). Contrast pairs in light and dark, light/dark token parity, no raw colours or font sizes in the stylesheet, nothing under 17px.
- `checks/render.py`: renders every state to `screenshots/` and runs behaviour checks; results are in `checks/last-run.json`.
- `screenshots/`: 20 numbered states at 390×844 (@2x), 5 dark-mode screens, a 320px error screen, 200%-text screens and a live mid-check frame.

## What I verified

- **Contrast:** 46 of 46 token checks pass. Text is 7:1 or more on every surface in both modes (body text 16.7:1, secondary 9.6:1, accent 8.7:1, white on button 9.1:1, error 7.1:1 on its tint), and control edges are 4.4:1.
- **Touch targets:** every visible button, link and input in all 20 states (and in open dialogs) is at least 48×48 px. The check found the phone link and the error-summary links too small, and I fixed both.
- **Reflow:** no horizontal scrolling in any state at 320px wide, or at 390px with text at 200%.
- **Keyboard and screen reader behaviour (Chromium):**
  - An empty submit moves focus to the error summary. Enter on a summary link moves focus to the field.
  - Fields get `aria-invalid` and `aria-describedby` that point to the hint and the error.
  - A slow check is announced through a live region.
  - The help sheet opens as a modal, Escape closes it, and focus goes back to Help.
- **Happy path end to end** with real input, including the wrong-code, date-of-birth-passcode and mismatch errors. No JS or console errors in any state.
- **Visual review** of the welcome, details error, help, slow check, wrong code, timeout, done, dark-mode and 200% screenshots. This caught three problems, all fixed: a focus ring drawn around headings, a clipped card diagram, and a vague "enter a real date" message (it now says "The month should be a number from 1 to 12").

## What I could not verify

- **Testing with older users.** Nothing replaces watching five or six branch customers try this, ideally including people who use a screen magnifier, VoiceOver or TalkBack.
- **Real screen readers.** I checked roles, names, focus and live regions in Chromium. I didn't hear it in VoiceOver or TalkBack, and live-region timing varies between them.
- **Real devices.** Not tried on iOS Safari or Android Chrome: the numeric keypad, one-time-code autofill, a fingerprint prompt, or how the bottom sheet behaves with the keyboard open.
- **Automated audits.** No axe or Lighthouse run, since they weren't available offline. My checks are targeted, not exhaustive.
- **Windows High Contrast.** `forced-colors` is styled for the button edge and status marks but not inspected.
- **The bank's rules.** Real fraud rules (attempt limits, what happens when someone is locked out, whether a call-out code is allowed) and legal copy need review by risk and compliance.
- **The timeout.** The 2-minute warning and the "20 more minutes" figure are placeholders; the dialog is reached through the prototype menu, not a real timer.
- **Prototype limits.** The fingerprint screen doesn't call a real sensor, and "Go to my accounts" returns to the start.
