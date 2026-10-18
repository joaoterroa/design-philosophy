# Onboarding for branch customers: design notes

Applying the user's "considered design" philosophy to the onboarding flow of a mobile banking app for older customers moving from branches. Direction name: **Counter Service**.

- Prototype: `app/index.html` (open at phone width; every state reachable by URL, listed at the end)
- Design system: `design/SYSTEM.md`, tokens in `app/tokens.css`, guard test `tests/design.test.js`
- Verification: `tools/verify.py` (screenshots, layout and keyboard checks), output in `screenshots/` (63 PNGs) and `tools/verify-report.json`
- Agent pointer: `AGENTS.md`

## 1. How I approached it

I followed the skill's eight phases: understand, study references, audit, choose a direction, write the system, implement, verify and refine, record. Two things changed the shape of the work:

- **No existing app, flow, code or brand was available, and I couldn't ask.** So phase 3 (audit the current state) could not be a measured audit of *their* flow. I audited the prototype itself across rounds instead, and recorded the numbers (section 6).
- **The network blocked every reference site** (w3.org and design-system.service.gov.uk both returned a proxy 403). Everything in section 2 comes from prior knowledge, not sources fetched in this session. A human should check it against the current documents.

### What I would have asked, and what I assumed instead

| Would have asked | Assumed | Why that assumption |
| --- | --- | --- |
| Brand guide, logo, palette, typefaces | None. Placeholder name "Harbour", proposed palette (SYSTEM.md section 3), system fonts | The skill says a brand beats invented taste. The palette is labelled a proposal, and the system says how to bring the brand colour in. |
| The existing onboarding flow and its constraints | A fresh flow for **existing** customers activating the app, not new account opening | "Switching from branches" means they already bank with you, which makes their card the natural bridge. |
| Market and regulation | UK: sort codes, £, free 0808 helpline, UK scam patterns (safe-account and code-sharing scams) | The repo context and the fraud patterns these users face. Swapping the market changes the copy and identifiers, not the structure. |
| How identity is checked | Card number + date of birth (or sort code + account number), then an SMS code to the mobile on file | The common UK pattern. Real KYC/SCA rules may add steps, which would fit the same one-question-per-screen structure. |
| Native iOS/Android or web | Native app. The prototype is HTML that simulates it at phone size | The brief says "mobile banking app". |
| How long progress is kept | 7 days on this phone, non-secret fields only | Needs a security owner's decision (see open items). |
| Helpline number | 0808 157 0192, from Ofcom's range reserved for drama and fiction | So the prototype never dials a real number. |

## 2. Understanding and research

**Users.** Existing customers, mostly 65+, who have banked at the counter for decades. They are moving because branches are cutting hours or closing, so some don't want to be here at all. They set up once, at home, sometimes with a relative, often with the phone's text size turned up. They make fewer taps and more careful reads than younger users, they are put off by gestures, hidden controls and jargon, and they are the main target of authorised push-payment and code-sharing scams.

**Moment.** A deliberate, unhurried sitting. Attention is high, confidence is low. That's the opposite of the case study's engineer mid-investigation, so density goes **down**, explanation of the *unusual* goes **up**, and targets get bigger.

**Priorities (tie-breakers, in order):** never lost; readable and reachable; safe, and seen to be safe; a person one tap away; mistakes cost nothing. The reasoning is in SYSTEM.md section 1.

**Constraints and standards I designed to** (from knowledge, not fetched):
- WCAG 2.2 AA as the floor, plus three AAA-level choices: text at **7:1** contrast, targets of **56px** for primary controls (2.5.8 asks for 24px; Apple and Google ask for 44pt and 48dp), and no timeouts.
- WCAG 2.2's newer criteria that fit this flow closely: **3.2.6 Consistent Help** (Help sits in the same place on every screen), **3.3.7 Redundant Entry** (details survive Back and errors), **3.3.8 Accessible Authentication** (the code field accepts paste and OS autofill, with no memory or puzzle test), and **2.2.1 Timing Adjustable** (no screen times out; the code's 10-minute life is stated, and a new one is one tap away).
- The OS text-size setting (iOS Dynamic Type, Android font scale) must reflow the layout up to 200% without clipping. That's why everything uses rem, and why the prototype has a `?scale=200` hook.
- Zoom is never blocked.

**References, for their thinking:**
- *The Browser Company / Dia* (the skill's root influence): "familiar, but elevated". Borrowed: no new mechanics. These users pay for every unfamiliar pattern, so the craft goes into wording, spacing and states. Not copied: any visual.
- *GOV.UK Design System* (built for everyone, including people with low digital confidence): one thing per page, the question as the heading, error summaries that link to fields, a separate day/month/year date input. Borrowed: those patterns, because they are tested on exactly this audience. Not copied: GOV.UK's typeface, colours, or its yellow focus style.
- *UK fraud-prevention messaging* (the Take Five style "we will never ask you to…"). Borrowed: one specific rule, given at the moment it applies. Not copied: blanket warning screens, which these users learn to tap past.

## 3. Direction

**Counter Service:** the app should feel like being served at the counter by someone patient. One question at a time, in plain words; the thing you already hold (your card) is the way in; a person is always one tap away.

**Structure.**
1. Welcome: what the app is for, how long setup takes (10 minutes), what you'll need, and that you can stop. Plus the offer to do it with a person.
2. Step 1, Your details: the long card number (with an illustration of where it is) and date of birth. "I don't have my card with me" switches to sort code and account number.
3. Step 2, Check it's you: the SMS code, with the message preview.
4. Step 3, Your passcode.
5. Step 4, How you log in: fingerprint or face, or passcode only.
6. Setting up: named steps that tick in place.
7. Done: their account with its balance and last payment in, and the line "Your branch is still here".

**The one novelty moment: the text message, shown before it arrives.** On the code step the app shows exactly what Harbour's text will look like: the sender, the wording, the code as blanks. The status line changes from "Sending your text…" to "Sent at 2:14pm. Check your messages." as the bubble slides in. Right under it is the single scam rule that matters at that moment: *never read this code out to anyone, even someone who says they're from Harbour*.
Why this spot: the code step is where scams actually happen (fraudsters phone and ask for exactly this code). It is also where these users leave the app for Messages and have to come back. The preview does two jobs. It tells them what to look for, and it teaches them to recognise a genuine message by showing one. Everything else in the flow is plain.

**Identity, each with a reason specific to this product:**
- *Palette:* warm paper and ink, because the reference is a bank letter, not a dashboard, and because a warm off-white glares less than pure white for older eyes. White is kept for "write here" (fields, the bubble). Deep ink blue is the single action colour: it gives 10.8:1 with white labels, and it never has to be told apart from another blue or from green, which matters because the ageing lens weakens blue/green and blue/violet discrimination.
- *Type:* system faces at 19px body and 28px titles. They follow the phone's text setting and match what users read in Messages; a brand face adds nothing they need.
- *Shape:* soft but firm (10–16px radii), with a **visible 2px edge on every control**, including Back and Help. Borderless text buttons and 1px field outlines are common in banking apps and are exactly what older users miss.
- *Layout:* buttons follow the content instead of docking to the bottom. At 200% text a docked bar would eat a third of the screen and cover fields.
- *Voice:* patient, plain, specific. "The card number is 16 numbers. You've entered 12." Limits are stated before they bite ("You can try 2 more times").

Swap test against the case study (Recall): it used a red and maroon brand on a cool UI, a docked bottom composer, chips, a skeleton sheen, dense metadata and system UI at small sizes. This flow shares none of those. Its warm paper ground, large scale, bordered bar buttons and message preview would make no sense in Recall, which is the point.

## 4. Key decisions and their reasons

| Decision | Reason | Road not taken |
| --- | --- | --- |
| The card is the way in | Users hold it already and have used it at the counter for years; "the long number on your card" plus a picture answers "which number?" | Customer ID or username, which branch customers often don't know |
| One code field with `one-time-code` autofill, not six boxes | Six boxes break paste, OS autofill and screen readers, and older users mis-tap into the wrong box | Segmented boxes, which look neat and fail this audience |
| Scam advice only at the code step, as one sentence | Advice lands when it's relevant; an up-front warnings screen gets tapped past | A safety-tips screen before setup |
| Help is a labelled, bordered button in the same place on every screen; it opens help for **this step** first, then "Talk to a person" | WCAG 3.2.6, and priority 4. Context first, because most questions are about the current screen | A help tab or menu, or a chat bot |
| A phone number and branch on the welcome screen | Some users would rather do this with a person, and should be told up front that they can | Burying assisted setup in FAQs |
| Biometrics: equal-weight yes and no, plus the honest line "anyone whose fingerprint or face is saved on this phone could also open the app" | Family members often have fingerprints on a shared phone. It's true, specific and protective | Pushing biometrics as the default |
| Passcode masked by default, one "Show numbers" toggle for both fields | Platform convention, and people set up with others nearby; the toggle reduces typing errors | Unmasked by default |
| Passcode rules explained in words, including a check against the date of birth they just entered | Specific beats "weak passcode" | A strength meter (a widget to learn) |
| Setting-up screen has named steps, and a calm, honest note when slow | No anxious spinner on its own; the user knows nothing is required of them | Spinner and "Please wait" |
| Failure says "Nothing has changed on your account" | The fear is losing money, not losing a form | Generic "Something went wrong" |
| Done shows the balance and the last money in | This is what they came for, and it looks like the statement they know | A feature tour carousel |
| "Your branch is still here" on the done screen | Quiet personality that answers the real worry ("am I losing my branch?") | A celebration animation |
| Error summary at the top **and** inline errors | A screen-reader or zoomed user lands on the summary; a sighted user sees the error at the field | Inline only, which isn't found when zoomed |

## 5. The system

`design/SYSTEM.md` records the purpose, priorities, principles, every colour's meaning and misuse, the type scale, space and shape rules, layout, components, motion, writing, accessibility and a pre-ship checklist. `app/tokens.css` holds every value. `tests/design.test.js` (6 tests) fails on:
- literal colours, font sizes, radii, durations or shadows in `styles.css`;
- inline colours or styles in `app.js` or `index.html`;
- a colour missing from, or different between, the two dark blocks;
- any type size below 17px;
- **26 contrast pairs per theme**: text at 7:1 on paper, surface and sunk; button labels; error, caution and ok text on their tints; control edges and focus at 3:1;
- a viewport that blocks zoom, or tokens loaded after styles.

## 6. Verification and refinement

**Automated, final run** (`python tools/verify.py`, Chromium headless):
- 17 states at 390px light and dark and at 320px; 3 states at 430px; 6 states at 200% text; the help sheet in light and dark.
- **No horizontal overflow, no clipped text or controls, no target under 48px** (inline links in sentences excepted, as WCAG allows), **no console errors**, in every rendering.
- The guard test passes: 6/6.
- **Keyboard-only walkthrough, completed with reduced motion on:** Start → details (focus lands on the question) → Help opens with focus on its title and the app behind inert, Escape closes it and focus returns to Help → an empty submit focuses the error summary (2 items) → the card number groups itself as "4921 3388 0154 7712" → code step (progress reads "Step 2 of 4: Check it's you") → message status updates → a wrong code gives "You can try 2 more times" with focus kept in the field → a passcode matching the birthday is rejected → a mismatch focuses the second field → "Show numbers" unmasks both fields → biometrics → setting up (Back hidden) → done, with focus on "You're set up, Margaret".

**Bugs found by looking, and fixed:**
1. **Code input below the fold.** With the preview above the field, Continue sat at y=997 on an 844px screen and y=1165 at 320px. Users would have to scroll to do the one thing the screen asks. I moved the field and Continue above the preview: Continue is now at **y=452 (390px) and y=480 (320px)**. The preview still starts on the first screen, just after the action.
2. **200% text squeezed the column to about 240px** because rem gutters and panel padding doubled too. The balance (£2,481.36) overflowed its panel, and the message bubble's text overflowed. I made horizontal insets fixed px (`--gutter` 20px, `--inset` 16px) while vertical rhythm still scales. Both overflows are gone.
3. **Masked passcode clipped at 320px:** the first dot was cut off because the Show button shared the row. I moved the toggle below both fields as one control for both. Its label was then shortened to "Show numbers" so it fits on one line at 320px.
4. **Card illustration:** the cardholder name touched the highlighted number. I re-spaced it.
5. **Prototype routing bug:** the `#code` review route matched the input `id="code"`, so the browser focused and scrolled to it. I renamed the input to `otp`, and recorded the rule in SYSTEM.md.
6. The guard test's first contrast model checked the focus ring against the button fill. The ring actually sits on a paper gap, so I corrected the pair to gap against fill. The test also caught error text (6.66:1) and confirmation text (6.31:1) under the 7:1 bar; I deepened both.

**Critique (`references/critique.md`), the three weakest things left:**
- The details screen at 390px puts Continue at y=779 (the card illustration costs about 100px). I kept it because the picture answers the most common question on this step, but it should be tested with users. An alternative is to show the picture only in Help.
- When both appear, the code step's "new code sent" note and the preview are two filled surfaces on one screen. The note is situational and temporary, but it is louder in dark mode than I'd like.
- The palette is invented. Until the brand arrives, the ink-blue action colour is safe rather than distinctive; the identity currently rests on scale, warmth, edges and the message preview.

## 7. What I could not verify

- **Real devices**, VoiceOver and TalkBack (only DOM semantics and keyboard were checked), real Dynamic Type (simulated with root font scaling), real SMS autofill, and real biometric prompts.
- **System fonts:** the screenshots render in Inter as a stand-in, because SF Pro and Roboto aren't installed here. Line breaks will differ slightly.
- **Research sources:** WCAG 2.2, GOV.UK patterns and the fraud messaging are from prior knowledge, because the network blocked them.
- **Users:** no testing with older customers. Before build, a moderated test with 5–8 branch customers (ideally including some with low vision and tremor) on the code step and the details step is the most valuable next step.
- **Compliance, fraud and legal review** of the copy, the 7-day saved-progress claim, the 3-try and 30-minute lockout, and the 10-minute code life. These are plausible values, not the bank's.

## 8. Open items

- Swap in the brand: wordmark, logo, act colour (re-run the guard test; adjust the shade for 7:1 if needed and record it in SYSTEM.md).
- Decide with security whether the "I don't have my card" route needs another factor.
- Assisted setup: if the bank offers "a colleague sets it up with you" by phone or in branch, the welcome screen should link a booking flow, not just a number.
- Native build: map the tokens to SwiftUI and Compose, and use real Dynamic Type styles rather than fixed rem steps.

## 9. Proposed lessons for the skill (not applied; offered for review)

1. **In `decisions.md`, under Accessibility:** "When users enlarge text (older users, low vision), test at 200% text. Keep horizontal insets fixed (px or pt) while type and vertical rhythm scale, or large text gets squeezed into a narrow column." *(From: banking onboarding. Rem gutters cut a 390px screen to about 240px of text at 200%.)*
2. **In `decisions.md`, under Hierarchy:** "Measure where the screen's *action* sits, not only where the first content starts. A helpful panel above the input can push the task below the fold." *(From: the code step, where Continue moved from y=997 to y=452.)*
3. **In `method.md`, phase 3:** "When there is no existing product to audit, say so, and treat the first rendered build as the baseline, with numbers." *(This brief had no flow to audit.)*

## Review states (open `app/index.html` with these)

`#welcome` `#details` `#details-errors` `#details-notfound` `#details-nocard` `#code` `#code-wrong` `#code-expired` `#code-help` `#code-locked` `#passcode` `#passcode-errors` `#biometrics` `#working` `#working-slow` `#working-failed` `#done`. Add `?help=1` for the help sheet, `?theme=dark` or `?theme=light`, and `?scale=150` or `?scale=200` for larger text, for example `index.html?scale=200#code`.

Prototype rules for the live flow: a card number ending 0000 is "not found"; code 000000 is wrong (three times locks setup); a passcode that repeats, runs in order or matches the date of birth is rejected; anything else valid continues.
