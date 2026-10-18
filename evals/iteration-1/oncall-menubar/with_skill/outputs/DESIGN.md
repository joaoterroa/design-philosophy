# Rota: on-call schedule and shift handover in the macOS menu bar

**Deliverables:** `app/index.html` (open it in a browser; prototype controls on the right switch between 12 states and the light, dark and system themes) · `design/SYSTEM.md` (the design system) · `app/tokens.css` (tokens) · `tests/design.test.js` (guardrail test) · `tools/shoot.py`, `tools/interact.py` (render and interaction checks) · `screenshots/*.png` (24 renders at 2x: 12 states × 2 themes).

## 1. Approach

I followed the design-philosophy method: understand → references → baseline → direction → system → implement → verify → record. There was no existing code, so phase 3 (the baseline) became a written list of states to design. I couldn't ask questions, so the assumptions below stand in for the answers.

### Users, moment, priorities

- **Who:** about 40 SREs who share a few rotations (assumed: Platform, Data and Edge, each with Primary and Secondary layers, rotating weekly on Monday at 09:00).
- **When they look:** in passing, for a few seconds, usually while in another app, sometimes off-hours. On a Saturday, the question is "am I still on?". On a Thursday, it's "who has Data right now?".
- **Priorities, in order:** (1) am I on call and until when; (2) who's on call now and how to reach them; (3) hand over all or part of a shift safely; (4) what needs me (requests, gaps); (5) trust: the data source, its freshness and the time zone.
- **What must not break:** coverage. A handover tool that makes someone think they're off when they're not is worse than none. This became the direction.

### Assumptions (where I'd normally ask)

| Question | Assumption |
| --- | --- |
| Schedule source | PagerDuty (schedules, layers, overrides). A handover creates an override **after** the recipient accepts. Out-of-office comes from Google Calendar. |
| Brand | None supplied. The palette is derived from macOS system colours and is offered as a proposal (SYSTEM.md §3). |
| Who can take a shift | Only members of the same rotation (11 for Platform), not all 40. One person can't hold Primary and Secondary at once. |
| Acceptance | The recipient must accept, in Rota or via the macOS notification. The requester stays on call until then. |
| Time zone | The user is in London (BST). Teammates are spread across Europe, New York and San Francisco. |
| Name | "Rota". |
| macOS version | Current macOS (26 at the time of writing): 24pt menu bar, menu-bar-extra window popover. Liquid Glass material is approximated with a blur. |

### Platform research

- Apple's HIG "The menu bar" page didn't load in this environment (it renders with JavaScript), so I couldn't quote it.
- Bjango's "Designing macOS menu bar extras" (found by search) gives: a 24pt bar since Big Sur, a 22pt working area for items, about 16pt as the right visual weight for a circular item, and template (alpha-only) images so the system tints them for light and dark. I designed to those numbers.
- A developer write-up notes SwiftUI `MenuBarExtra` is limited for dynamic titles. A live countdown title probably needs `NSStatusItem`. That's an engineering note, not a design change.
- From platform knowledge (not verified here): 13pt body text, 22pt regular push buttons, system accent colour chosen by the user.

### References: what I borrowed, what I didn't

There was no named inspiration beyond the philosophy's own origin (The Browser Company / Dia), so I studied the reasoning of two kinds of product that do this job: macOS's own menu-bar extras (Battery, Wi-Fi, Calendar's popover) and paging tools' schedule views.
- **Borrowed from macOS extras:** the status item answers the question before any click; popovers built from standard controls; quiet when healthy.
- **Borrowed from paging tools:** layers and overrides as the real data model, so a "handover" is an override and stays honest about acceptance.
- **Not copied:** paging tools' colour-per-person timelines (12 people would mean 12 colours to learn), their dense week grids (wrong for a 340pt popover), and Dia's or the Recall case's visuals. There's no docked composer, no segmented control, no citation chips and no skeleton sheen.

## 2. Direction: "Still yours until it isn't"

**Structure.** The menu bar holds the first answer (a dial plus `1d 19h`). The popover reads top-down in priority order: anything that needs you, then your shift (answer, end and who's next, the strip, Hand over…), then who's on call now, then the sync source in the footer. Handover is a sheet inside the same popover (back arrow, fixed footer). It's not a separate window, because the task takes under a minute and shouldn't lose its context.

**Novelty moment: the shift strip.** It's the one distinctive element: a bar from now to Tuesday showing who holds each hour of your shift. In the handover sheet it becomes the preview. When you pick a range and a person, those hours turn from your dark fill to the quiet fill and the person's initials slide in. You see the outcome before you commit. After you send, the segment turns orange-outlined and hatched with `PR?`, still on top of your time, because it's still yours. I put the novelty here because the outcome of a handover is the thing that can go wrong, and this treatment explains it rather than decorates it.

**Identity, each with its reason:**
- *Palette:* system neutrals plus three meanings: accent = act/selection, orange = waiting (still yours), red = nobody covering or failed. Your time is the darkest fill in light mode and the lightest in dark mode, so it's never a hue. People aren't colour-coded. Each colour answers a coverage question, which is what SREs scan for.
- *Type:* the system font at macOS sizes (13/11, with one 15pt answer). A utility that lives in the OS chrome should read as part of it.
- *Layout:* 340pt, top-down by priority. It's narrow enough to feel like a system extra and wide enough for "Name · Rotation Layer · until Mon 09:00" without truncating.
- *Mark:* a dial whose wedge is the share of your shift still to run. It says "time on duty" and works as a template image at 16pt.
- *Voice:* exact and calm. "Nothing changed: you're still on call." Ranges are absolute, and the time zone is named only when it differs.

**Key decisions and why:**
1. **The handover is a request, and every surface says so.** The pending note reads "You're still on call until Priya accepts", the strip keeps your segment under the pending outline, and the menu-bar time doesn't change. This is the safety rule of the product.
2. **"Part of it" is the default, not "the rest of my shift".** The common case is covering a few hours (an evening, a Sunday). The default range is the next sensible block, editable with two popup buttons. A "rest of shift" radio sits above it.
3. **Availability is computed and written out.** "Already Platform Secondary then" (disabled), "Out of office until Wed 22 Oct, per Google Calendar" (allowed, but the caution is repeated in the summary), "last on call 3 weeks ago" (fairness, so the same people aren't always asked), and the range in their own time ("11:00–19:00 in Berlin") when it differs.
4. **The outcome is one sentence beside the commit button:** "Sun 10:00–18:00 (8 hours) moves to Priya once accepted. Until then it's still yours." The button names the person ("Ask Priya").
5. **What needs you goes first.** A teammate's request ("Cover it" / "Decline…") or a coverage gap appears at the top. The gap action is "Ask in #sre-oncall", not "Cover it myself", because the user is Platform Primary at that time and shouldn't double up.
6. **Accent fills only the committing button.** "Hand over…" is a plain push button. The accent appears when you're about to change the schedule (Ask, Cover it, Sign in).
7. **Declines aren't errors.** They're a normal answer in plain text, quoted, with "Ask someone else…", which reopens the sheet with the same range.
8. **Offline keeps the schedule, but says so** ("Showing the schedule as of 13:02; it may have changed since"), dims the dial and disables Hand over with the reason written underneath.
9. **No global shortcut by default.** The menu-bar and ⌥⌘ space is crowded on SRE machines. It's user-set, and any UI text reads the live binding.

### States designed (all in the prototype and screenshots)

On call · not on call (next shift in 4 days) · handover: choosing · handover: send failed · waiting for reply · accepted · declined · incoming request · coverage gap · offline (cached) · first sync (loading) · not connected (first run, no schedule).

## 3. Design system

- `design/SYSTEM.md`: purpose and priorities, principles, colour roles (with "never for" and the native equivalents), type scale, space and shape, layout and platform limits with sources, components, motion, writing samples, brand, keyboard and accessibility, and a pre-ship checklist.
- `app/tokens.css`: every colour (light, dark via the media query, and a manual `data-theme`), type size and weight, radius, shadow and duration, plus reduced-motion overrides. Desktop-scene colours are separated and labelled prototype-only.
- `tests/design.test.js`: fails on literal colours, font sizes, weights, radii, durations or shadow colours in `app.css`; on inline styles other than strip geometry; on missing or mismatched dark tokens; on the token file loading after the stylesheet; and on 22 text and graphic contrast pairs per theme.
- Agent pointer: not added, because there's no project repository yet and the rules forbade writing outside this folder. When the repo exists, add the `AGENTS-snippet.md` lines pointing at `design/SYSTEM.md`.

## 4. Verification

What I checked, and how:
- **Rendered every state in both themes** at 2x, with the popover at its real 340pt width under a 24pt menu bar (`tools/shoot.py`). I looked at each screenshot and fixed what I found (see below). Automated checks: no element overflows the popover, no text is truncated with an ellipsis, no console or page errors.
- **Guard test:** 6/6 pass. A mutation check (appending a literal `#ff0000`, `12px` and `4px` to `app.css`) makes it fail, as intended.
- **Keyboard and interaction path** (`tools/interact.py`, 20/20 pass):
  - Hand over… opens the sheet with focus on the first choice.
  - Arrow keys switch the range choice.
  - Send stays disabled until someone is chosen.
  - A search with no match says so.
  - Choosing a person by keyboard keeps focus.
  - The button names the person.
  - The preview segment appears.
  - Sam (already Secondary) can't be chosen.
  - ⌘↩ sends.
  - The menu-bar time is unchanged while pending.
  - Nothing above the reading point moves when the pending note appears (answer and strip at the same y before and after).
  - Cancel returns focus to Hand over….
  - Esc backs out of the sheet, then closes the popover and focuses the status item.
  - Accepting an incoming request confirms in words and clears the badge.
  - Sign-in goes from loading to the schedule.
- **Contrast:** checked automatically in both themes (see the guard test).

**Found and fixed during refinement:**
1. The strip started at Saturday noon, so the "now" line cut through the "You" label and the past (not yours to hand over) took space. It now starts at Now.
2. Day ticks drawn through the segments read as shift boundaries. They moved below the bar.
3. Person rows truncated the time-zone information. The secondary line now wraps.
4. The gap headline broke inside "02:00–06:00". Ranges now never break: non-breaking spaces, and word joiners around the dash.
5. The gap action "Cover it myself" would have put the Platform Primary on Edge as well. It became "Ask in #sre-oncall".
6. Disabled-button text was 4.3:1 on its fill. Disabled buttons now use the window ground.
7. The dark accent outline was 2.9:1 on others' segments. I added a separate `--accent-line` token (3.3:1 or better).
8. The summary repeated the name ("…moves to Priya when Priya accepts"). It's now "…once accepted".
9. The interaction script first reported a 4px shift. It came from measuring during the popover's appear animation, not from the layout. The script now waits for the animation to finish.

**Could not verify here:**
- The real macOS rendering: SF Pro (Inter stood in), the real popover material and vibrancy, the menu bar on a notched display (taller bar), a real template image, and VoiceOver. Only the ARIA structure was checked, not a screen reader.
- The real PagerDuty and Calendar data: how long override creation takes, how acceptance is delivered (notification actions), and rate limits for 40 users polling.
- Whether a live countdown in the menu bar is acceptable to users (some will want it off; this should be a setting) and how it behaves at under an hour.
- Drag-to-select on the strip: designed as a natural next step, but not built. The popup buttons are the accessible path and work by keyboard.
- Reduced motion: the tokens set durations to 0, but I didn't screenshot it separately.

### Three weakest things still (from the critique pass)
1. The handover sheet is tall (640pt, scrolling) when the person list is long. A shorter list (top 5 free people, then "Show all 11") could fit without scrolling. Test with users.
2. The "You" row in On call now repeats information from the shift section. It's kept so the per-rotation list is complete, but it's a candidate for removal.
3. The pending hatch is subtle at 1x on the 22pt strip. Check it on a real non-Retina display.

## 5. Proposed lesson for the skill

From this project: *for tools that change shared responsibility (on-call, approvals, ownership), add a "never look more resolved than it is" check to the critique, covering every surface that states the user's status (menu bar, notifications, badges), not just the screen where the action happened.* Suggested home: `references/critique.md` › States, one bullet. It isn't applied; offered for the user to accept.
