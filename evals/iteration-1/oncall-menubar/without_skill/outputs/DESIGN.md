# On-call menu-bar app: design

A macOS menu-bar app ("Handover", a working name) for a team of about 40 SREs: it shows who is on call, tells you when you are, and lets you hand over all or part of a shift.

Deliverables, all in this folder:

- `app/index.html`: the prototype. Open it in a browser. The panel is drawn at real size (1 CSS px = 1 pt) under a mock menu bar. The column on the right is prototype chrome: it switches between 9 states and between light and dark.
- `app/tokens.css`, `design-system/SYSTEM.md`: the design system (tokens, rules).
- `checks/tokens.test.mjs`: design guardrails (`node --test checks/tokens.test.mjs`).
- `checks/flow.py`, `checks/shoot.py`: an interaction check and the screenshot script.
- `screenshots/`: every state in light and dark at 2x (Retina), plus a hover state and the full page.

## 1. How I approached it

**Finding "my design philosophy".** I could not use a dedicated design-philosophy document for this run. The best written evidence of your design thinking that I had was the design system you wrote for the Technical Memory side panel (`vfuk-technical-memory/design/SYSTEM.md`, "Recall"), plus its directions README. I read both and treated their principles as your philosophy. I did not copy that product's look (red brand, side-panel layout): I carried over the principles and the way they're enforced. **This is the biggest assumption in the work. If you have a separate philosophy document, check the result against it.**

What I took from it, and where it shows up here:

| Your principle | How it shaped this app |
| --- | --- |
| Familiar, then elevated | A standard macOS menu-bar panel: system font and material, push buttons, segmented control, search field, Esc to close. |
| One obvious way | "Hand over…" lives on the shift it hands over. "Message" lives on the person's row. Nothing is duplicated in a menu or toolbar. |
| Novelty where it pays | One novel element only: the **shift bar**, which draws the part being handed over on the shift itself, through each stage of the handover. |
| Minimal is not hidden | Time zones, "would double up", "overnight for her", "away until Wed", rota gaps and data age stay visible. Less suitable people sit behind a disclosure that names them: "4 more: would double up, be up overnight, or away". |
| Words over widgets | Status is a sentence, not a badge: "You're on call until Priya accepts." |
| Never look more certain than it is ("missing, not empty") | A requested handover is not shown as done. When offline, the schedule stays on screen marked "as of 18:31", and handovers are paused. |
| Status that is fine stays quiet; status that needs you speaks up | The menu bar shows a glyph, plus hours left only while you're on call. A dot appears only when you need to act (someone asked you, or your request was declined). The footer's sync line is faint. |
| Colour is for meaning, one colour per meaning | Neutral greys. The accent means act or follow. Amber means look twice. Red means failed, and always comes with a sentence. Green is only the sync dot. People never get colours. |
| Designed dark mode, tokens only, contrast enforced by a test | `tokens.css` and `checks/tokens.test.mjs` work the same way as your `tokens.css` and `design.test.js`. |
| Plain, calm writing | No exclamation marks, no "Oops". Each message says what happened and what to do. |

**Research** (from what I know; I did no live web research and had no access to your rota tool):

- **Rota tools.** PagerDuty and Opsgenie both model a schedule as layers plus *overrides*. An override is created instantly, and nobody has to accept it. That is the gap this app fills. Most teams swap shifts in Slack and someone then edits the rota by hand, so the rota and the agreement can drift apart.
- **Menu-bar extras.** Apple's guidance is to keep the menu-bar item small and template-tinted (one colour that adapts to the menu bar), and to avoid text unless it is essential. Recent macOS uses panel-style windows without an arrow (Control Center) for menu-bar extras.
- **What on-call engineers want at a glance.** Am I on call and until when? Who do I escalate to? What's open that I'm inheriting or handing on? Time zones matter for a team split across countries.

## 2. Assumptions (where I would have asked)

1. **Your philosophy** is the one in the Technical Memory design system (see above).
2. **The schedule source is PagerDuty.** The app reads schedules and writes overrides. Opsgenie would work the same way.
3. **The team** is about 40 SREs across London, Lisbon and Bengaluru. They're split into five rotations (Core platform primary and secondary, Network & edge, Databases, Incident commander), about 9 people per rotation. Shifts change at 09:00 London time.
4. **A handover needs the other person to agree.** The app sends a request (Slack message plus a notification). The override is written only when they accept, and until then the asker stays on call. This is the most important product decision. It is an assumption about your team's norms, and I chose it because silently moving a pager onto someone is the failure that matters most.
5. **You can hand over part of a shift** (for example one evening), not just whole shifts.
6. **Who should take a shift** is a suggestion, not a rule. The app sorts and labels people, but lets you pick anyone on the team except people who are away. Order: free people on the rotation first, longest since their last shift first (a simple fairness signal). Then people who would double up or be up overnight. Then people who are away.
7. **The user** is "JT" in the sample data. All people, incidents and times are invented. "Now" is Sunday 18 October 2026, 18:47 London.
8. **Global shortcut ⌃⌥O.** I have not checked it against your team's other tools.
9. **Panel size** is 360 × at most 680 pt, which fits a 13" MacBook Air screen under the menu bar.

## 3. Direction and key decisions

**One panel, two tabs, one sheet.**

- **Now** (default) answers the three glance questions in order. First the *you panel*: your state, the shift bar, and the one action. Then *On call now*: one row per rotation in escalation order, with the person's local time when it differs from yours. Then *Your next shifts*.
- **Schedule** shows the next seven days for a rotation, with gaps named in place ("Gap. Sat 25 Oct 09:00 → Sun 09:00. Nobody is scheduled, so pages go straight to the secondary."). It links out to PagerDuty instead of rebuilding a calendar. A menu-bar app is the wrong place for a full rota editor.
- **Hand over** replaces the panel content (back chevron, Esc). It is one screen, not a wizard: which part → who → note → a footer that says what will happen and a button that names it ("Ask Priya · 13 h").

Key decisions and why:

1. **The menu bar carries the most-asked answer.** Off call: outline glyph only. On call: filled glyph and hours left ("14h"). Needs you: a dot. Data stale: struck-through glyph. State is carried by shape as well as colour, so it survives the template tinting the menu bar applies.
2. **The shift bar is the one novel element.** A handover is about *which part of the shift*, and dates in text are easy to misread at 2 a.m. The same bar appears in every stage. While choosing, the range is outlined. While waiting it is striped and labelled "Priya?". Once accepted it is solid and labelled "Priya". It settles in over 600 ms, the only slow motion in the app.
3. **The request is not shown as done.** While waiting, the headline still reads "You're on call for Core platform · primary", and the line under it says "You're on call until Priya accepts." Declined says so in amber, quotes her note, and offers "Ask someone else…" as the default button.
4. **Suitability is said in words next to each person,** not as icons or colours: "Free then · last on call 12 days ago", "00:30 → 13:30 his time, overnight", "On call as secondary then, so he would be primary and secondary at once", "Away until Wed 22 Oct" (greyed, can't be picked).
5. **Incoming requests take over the you panel,** because they need you. Tom's request shows his note and a check against your rota ("You're free then. Your next shift starts Wed 22 Oct 18:00, 9 h after this ends."). The buttons are Decline… and Accept, with the default on the right as macOS does.
6. **The handover note pre-ticks your open incidents** (INC-4821). Losing context on open incidents is the classic handover failure, and here it costs one checkbox to avoid.
7. **Offline is missing, not empty.** The schedule stays visible, "Last synced 18:31". An error sentence says what is affected. "Hand over…" is disabled with the reason next to it, not just greyed.
8. **The accent follows the system.** I didn't bring the Technical Memory red across. In a native macOS app the accent belongs to the user's System Settings, and red in a pager app reads as "incident". The prototype uses a blue stand-in (`#0071E3`), deep enough for white button text to hold 4.5:1.

## 4. What I verified

- **Guardrails** (`node --test checks/tokens.test.mjs`): 6/6 pass. In both modes, every text token holds ≥ 4.5:1 on the panel, the you panel and the controls, and white on the accent fill holds ≥ 4.5:1. Glyphs hold ≥ 3:1. The two dark-mode blocks agree. `app.css` has no raw colours, font sizes, radii or shadows. Two problems the test caught and I fixed: muted text on dark controls was 4.22:1, and white on the stock macOS blue is about 4.0:1 in light mode and 3.65:1 in dark.
- **Interaction** (`checks/flow.py`, Playwright/Chromium): 17/17 checks pass.
  - Hand over… opens the sheet. Search filters people. The disclosure reveals all 8 candidates. An away person can't be picked.
  - The send button names the person and the length.
  - Pending and accepted name whoever was actually picked. Handing over the rest of the shift makes you off call and drops the hours from the menu bar.
  - Esc goes back, then closes. "Try again" clears the offline notice. Row actions show on keyboard focus.
  - Reduced motion stops the pulse. No page errors.
- **Layout:** in every state the panel is 360 pt wide with no horizontal overflow. Main-view states fit without scrolling (545–666 pt tall). The handover sheet scrolls inside a 680 pt panel, with its footer and button fixed.
- **Bugs found and fixed while checking:**
  - The "now" label collided with the end label.
  - The avatar class clashed with the you-panel class.
  - Date pickers wrapped.
  - The panel body didn't scroll, so content was clipped.
  - `[hidden]` didn't hide the panel.
  - Row actions were `display:none`, so the keyboard couldn't reach them.
  - Pending text said "Priya" even when you picked someone else.
- **Screenshots:** all 9 states in light and dark, plus hover, at 2x.

## 5. What I could not verify

- **It isn't a Mac.** Screenshots come from Chromium on Linux. SF Pro isn't available, so Inter stands in, and real SF metrics will set slightly narrower. The panel's blur approximates the system material. Real menu-bar spacing, the notch on newer MacBooks (which can hide menu-bar items when the bar is crowded) and the current macOS panel radius should be checked on a device.
- **No real users.** I don't know whether your team accepts the request → accept model (assumption 4), or whether "hours left" in the menu bar is wanted or is noise. Both are cheap to test with three or four SREs using the prototype.
- **Things I haven't designed:**
  - PagerDuty sign-in and first-run.
  - The settings menu (the gear).
  - Notification content (incoming request, accepted, "your shift starts in 1 h").
  - The rotation picker's menu.
  - A handover started from a future shift: the sheet always shows the current shift.
  - Request expiry (what happens if nobody answers before the shift starts; I would suggest the app reminds the asker 1 h before and never auto-hands-over).
  - VoiceOver. The labels are written but I haven't tested them with a screen reader.
- **The guardrail test** reads `app.css`, but not the few inline styles in `app.js`. Those use tokens only, which I checked by eye.
