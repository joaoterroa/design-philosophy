# Incident board redesign

The original is untouched at `dashboard/index.html`. The redesign is in `app/`: open `app/index.html` for laptops, or `app/index.html?display=wall` for the ops-room TV. The design system is in `design/SYSTEM.md`, the tokens in `app/tokens.css`, and the guard test in `tests/design.test.js`. Screenshots are in `screenshots/` (before: `screenshots/before/`).

## 1. How I approached it

I followed the method in the design-philosophy skill. First I worked out who reads the board and when. Then I rendered and measured the original, chose a structure before any styling, wrote the tokens and system, built the page with every state, and then checked it in headless Chromium at real sizes. I did four rounds of looking at screenshots and fixing what I saw (§6). I also followed the dataviz skill for the small charts: the form for each, a single series in one colour, value labels, and a validator run on the chart colour.

### Users, moment, priorities

- **TV in the ops room:** people glance at it from 2–4 m while doing something else. It has no mouse, runs all day, and the room is often dim. The question it answers: *is anything on fire, and is someone on it?*
- **Laptops:** engineers and incident leads check in up close. They can click through to an incident and may want history.

Priorities in order: (1) what is open now and how severe; (2) who owns it, and especially when nobody does; (3) whether the data is fresh; (4) direction of travel (pages, MTTR, error budget); (5) history.

### Constraints kept

- The data model and the 60 s refresh from `/api/metrics` (noted in the original's script). Fixtures in `app/data.js` mirror the original's values, and `#open` still holds the open count.
- Brand guide v3: Harbor Navy, Signal Orange used sparingly and never for body text or large areas, Tide Teal for charts, Fog and Slate, IBM Plex Sans and Mono, a calm voice, and the symbol only white-on-navy when recoloured.
- No dependence on the network: Plex is bundled locally (OFL, latin subset), with no CDNs.

### Assumptions (I couldn't ask)

| Assumption | Why | Easy to change |
| --- | --- | --- |
| The TV is a 1080p or 4K landscape screen, opened with `?display=wall` | You set up a wall display once, as a bookmark. Detecting it from the screen size would also catch large desktop monitors | The wall root size scales to any height |
| The TV runs dark; laptops follow the system theme | A dim ops room means glare and burn-in concerns. Laptops sit in lit offices | `?theme=light` |
| "Open" = Investigating, Identified, Mitigated or Monitoring | Usual incident lifecycle | `data.js` |
| The original's "7 open" was correct and its table showed only part of the list | The table was "recent incidents" and only 3 of its rows were unresolved. I added 4 realistic SEV3s so the headline and the list agree | `data.js` |
| "Incident commander: unassigned" belongs to INC-2291 (the SEV1) and to the rota slot | It was the only unowned item, and a SEV1 without an IC is the one thing the room must notice | `lead` per incident |
| Error budget = a 99.9% availability SLO over 30 days | The original didn't say which SLO | `budgetSlo` |
| "▲ 5" pages = 5 more than all of yesterday (18) | The original didn't say what the delta compared against. I chose a reading and wrote it out in words | `pagesYesterday` |
| Next on-call names (Amara O., Jonas K.), per-incident ICs, 14-day and 8-week history | Needed so the board shows handover and trend. Values are realistic but invented | `data.js` |
| Incident links go to `#INC-xxxx` | The incident tool's URL is unknown | `incidentRow()` in `app.js` |

### References

The brief named no product to emulate, so I worked from the skill's own philosophy, which comes from The Browser Company's reasoning: familiar but elevated, novelty only at the differentiator, minimal but never hiding information. I did no web research for this run. For an ops board, the familiar pattern is the departures board or flight-information display: one row per item, the status in words, times aligned, and colour only for exceptions. I borrowed that reasoning. I did not copy its look (no split-flap, no yellow-on-black).

## 2. Audit of the existing dashboard

Rendered at 1920×1080 (TV), 1440×900 and 1280×720 (laptops). See `screenshots/before/`.

**Measured problems**
- On a 1280×720 laptop, the SEV1 incident row starts **707 px** down, below the fold. The page is 948 px tall. The most important fact on the board is in the fifth block.
- The text is far too small for a TV: table text is **14 px** and labels **14 px uppercase grey**. Viewed from 3 m on a 1080p panel, that is unreadable. Only the four KPI numbers (42 px) can be read from across the room.
- Contrast failures (WCAG text minimum 4.5:1): labels `#888` on white **3.54:1**; trend text `#2ed573` **1.93:1**; white on the SEV2 pill **1.97:1**, on SEV3 **3.24:1**, on SEV1 and the LIVE badge **3.34:1**.
- 30% of the 1080p TV screen (the bottom band) is empty purple gradient, while the incident list is squeezed into 14 px text.
- The page doesn't support dark mode.

**Hierarchy problems**
- The eye lands first on four equally weighted KPI cards with emoji. The open incidents (what's broken) come last.
- "Incident commander: unassigned" for a running SEV1 is plain body text inside the "On call" card, in the same weight as the names around it.
- "Open incidents 7" contradicts the table, which shows 3 unresolved incidents among 5 "recent" ones.

**Noise**
- Purple-to-blue gradient background, 20 px radius cards with heavy shadows, an emoji per card and in the title, gradient bars, and pills for every severity.
- Every trend is green regardless of direction. "▲ 2" more open incidents and "▼ 4 pts" of error budget are both bad, yet both are green, so the colour carries no meaning.
- A permanent "LIVE" badge that stays red even if the feed is dead.

**Missing information**
- When the data last updated, and whether it is stale.
- Severity counts. Durations that tick. Which incidents are still open versus resolved, without reading every Status cell.
- What "▲ 5" compares against, which SLO the budget belongs to, and when the on-call handover is.
- States: empty, loading, error and stale are not designed at all.

**Ranked weaknesses:** (1) the open SEV1 and its missing IC are not what the eye finds first; (2) the board is unreadable at TV distance; (3) the board makes no freshness or failure claim at all, so it can't be trusted; (4) colour carries no meaning (green for everything, purple decoration); (5) the headline count contradicts the list.

## 3. Direction: "What's open, who has it"

> The list of open incidents *is* the dashboard. It takes the largest column and the top of the page, sorted SEV1 first, with the count as its heading. Ownership sits on one line directly under the header, where the room's eye starts. Everything else is quiet context on the right. Colour appears only when something is wrong, so a calm board looks calm and a bad day is visible from the door.

**The novelty moment: the 24-hour lane.** Each row has a thin bar on a shared axis that ends at "now". Open bars all reach the same now-edge and grow as time passes. A new incident is a dot, an overnight one is a long bar, and you can see the overlaps. Resolved incidents keep their bar, ending before now, in grey. It carries information: it answers "how long, since when, alongside what" without reading numbers. I chose this spot because time is the thing that matters most in incident response, and the original showed it only as static text.

**Identity, each with a reason specific to this product**
- *Palette:* the brand's own navy, fog and slate carry the page. Dark mode is a navy-derived palette because the TV lives in a dim room and the brand is navy. Signal Orange (the brand's "use sparingly" accent) becomes *needs attention*, which keeps it sparing by construction. Red, which the brand lacks, is reserved for SEV1 and broken sources. Tide Teal is used only for chart marks, as the brand guide says.
- *Type:* IBM Plex because the brand mandates it. Plex Mono for IDs and durations so the durations column aligns. Proportional Plex Sans for big numbers.
- *Shape:* 2–4 px radii and hairlines instead of cards, to look precise and freight-like rather than soft.
- *Layout:* rows like a departures board, because that is the familiar pattern for "what's happening, how long, status".
- *Mark:* the brand's compass-N (placeholder drawn; the official asset should replace it).

## 4. Key decisions and why

| Decision | Reason |
| --- | --- |
| Removed the 4-card KPI row; the open count became the list heading with "1 SEV1 · 2 SEV2 · 4 SEV3" | One obvious place for "what's open". The count and the list can no longer disagree |
| Sort by severity, then **newest first** within a severity | A fresh incident appears at the top of its band, where the eye already is. Long-running SEV3s sink |
| "No incident commander" in the SEV1's own row, in orange words | The missing owner is shown where the incident is. Words, not an icon |
| On call moved from a card to a one-line band under the header | It's the second priority and it's short. A band makes it visible in every state and frees the right column for the charts. When all shifts end together, the handover is said once ("Handover 18:00 to Amara O. and Jonas K.") |
| Freshness sentence in the header replaces the "LIVE" badge. In the stale state the header tints orange and says since when and what happens next | Trust needs a claim that can be false. A permanent badge can't be |
| SEV3 has no colour and a pale bar | Colour is an alarm here, not a scale. A 2-day SEV3 bar must not outweigh a new SEV1 dot (I fixed this in round 2, §6) |
| Trends written in words ("12% faster than last week", "5 more than all of yesterday") and drawn without colour | The original's green arrows were wrong half the time. Words carry the direction and whether it's good |
| Pages: 14-day columns with today in teal; MTTR: 8-week line; budget: a meter | The dataviz form rules: emphasis for "today against context", a line for a trend, a meter for a ratio against a limit |
| By-service bars: one colour, value at the tip | One series needs no legend and no colour per bar (the original's gradient implied a scale) |
| One page for TV and laptop, with the wall root size = `100vh/48` | The same proportions on any TV resolution, and one design to maintain. Verified at 1366×768, 1920×1080 and 3840×2160 |
| On the wall, overflowing rows are hidden with a sentence ("5 more not shown: INC-2297 (SEV3), …") | The TV can't scroll. It drops history first, then the least severe rows, and says which are hidden |
| Plex bundled locally | The TV must not depend on Google Fonts. Network was available here; I downloaded the official Google Fonts files once |
| Missing owner and rota gap both orange; red only for SEV1 and failure | Fixed in round 4: one meaning had two colours (§6) |

**Trade-offs made on your behalf**
- Signal Orange is 2.9:1 as text, so orange *words* use a deeper `#A6410C` (light) or `#FF9A5C` (dark). Fills stay exact brand orange, with ink text (white on orange is 2.9:1).
- Tide Teal on Fog is 2.93:1, just under the 3:1 graphics guideline. I kept the exact brand value because every chart value is also printed as text. The guard test records this as a documented exception.
- Wall text is 22.5 px at 1080p (meta lines about 20 px). That is the size at which seven open incidents fit without scrolling. It needs checking on the real TV (§7).
- On the wall, incident titles are clamped to 2 lines (only the longest one truncates in the demo data). The full title is on the laptop view and in the incident tool.

## 5. States implemented

Use the switcher in the laptop footer, or `?state=` in the URL. Add `&display=wall` for the TV and `&frozen` to stop the clock for screenshots.

| State | What it shows |
| --- | --- |
| `live` | 7 open (1 SEV1 without IC, 2 SEV2, 4 SEV3), 2 resolved in 24 h. The clock and durations tick; the simulated refresh runs every 60 s |
| `loading` | Static placeholders in the exact shape of rows and stats, plus "Connecting to the incident feed…" and "Loading the rota…". No shimmer. **0 px shift** above the list when data arrives (first row at 236 px wall / 185 px desk in both states) |
| `allclear` | "0 open incidents" and "Nothing open. The last incident closed at 07:48, 3 hours 12 minutes ago: INC-2291 …", with resolved history and its bars |
| `stale` | Header tinted orange: "No new data since 10:54 (6 min). Figures may be out of date; retrying every 60 s." The last data is still shown |
| `partial` | The on-call source failed: a red-tinted band says "The rota didn't load … It is missing, not empty: check the paging tool …". Everything else stays live |
| `surge` | 12 open, 41 pages. The wall shows 7 and "5 more not shown: …"; the laptop shows all 12 |

## 6. Verification

**How:** Playwright with headless Chromium (`tools/shoot.py`, `tools/interact.py`, `tools/shoot_before.py`). I took 19 screenshots: every state on the wall at 1920×1080 dark; live wall in light, at 4K and at 1366×768; every state on the laptop at 1440×900 light; live at 1440×900 dark and 1280×720; and 390 px light and dark. Each run measured horizontal overflow, elements off-screen, wall overflow, first-row position, whether the font loaded, and console errors.

**Results**
- 0 console errors, 0 horizontal scroll, 0 elements off-screen, in all 19 captures. IBM Plex loaded from the local files in every capture.
- First incident row: **185 px** on a 1440×900 laptop (was 707 px at 1280×720 and 1440×900). All 7 open incidents are above the fold at 1440×900, and the wall fits all 7 at 1366×768, 1080p and 4K.
- Layout shift from loading to loaded: 0 px above the list (measured).
- Guard test: `node --test tests/*.test.js` → 7 pass. A mutation check (appending `.x{color:#fff;font-size:13px}` to `app.css`) made it fail, as intended.
- Contrast: every text token holds 4.5:1 on every surface and tint it sits on, in both themes (20 pairs × 2 themes, in the test).
- dataviz validator on Tide Teal: passes the lightness band and chroma checks in both modes. Contrast is a WARN in light (2.93:1 on Fog); value labels provide the relief.
- Keyboard: Tab goes through the incident rows SEV1 first, then the resolved rows, the chart columns and the controls. The focus ring is 2px Navy. Focus stays on the same incident after a re-render (checked by re-rendering with INC-2290 focused). Focusing a chart column shows the tooltip ("11 pages Mon, 5 Oct"). The state switch updates the URL. Reduced motion sets transition durations to 0s.

**Refinement rounds (what looking found)**
1. Wall showed only 4 of 7 incidents, and axis labels collided ("06:00now"). "since yesterday 22:10" wrapped. Long SEV3 bars in dark slate outweighed the SEV1. → I widened the list column, moved to weekday times ("since Sat 22:10"), cut the axis to "24 h ago · 00:00 · now", lightened `--minor`, and sorted newest first within each severity.
2. Still 5 of 7 shown, and the side column overflowed (meter cut off). → I moved on call to a one-line band, merged the list head into the count row, and shortened the copy.
3. The on-call band stretched to fill spare height in "all clear" (a grid-row bug), and the loading band was 6 px shorter than the loaded one, causing a shift. → I fixed the grid rows and reserved the band height. I lowered the wall root from /44 to /48 so stale/partial/1366×768 also fit 7 rows.
4. Critique pass: the same fact (no IC) was red in the row and orange in the rota. → One colour: orange = needs attention. At 390 px the mark was squeezed to a sliver and the clock overlapped "Incidents". → The mark no longer shrinks, and the date is hidden on phones.

**Critique verdict, the three weakest things left**
- On the wall, the 2-line titles make rows uneven in height. A product decision on title length (or a short-title field) would tidy it.
- With the demo data, the 24-hour lane mostly shows dots and full-width bars. It is most useful on busy days, and that only shows with real history.
- The right column on the TV is information-light. A future "deploys today" or "customer-impacting" line could earn that space if the team wants it. I didn't invent one.

## 7. What I could not verify

- **The real TV:** legibility at the room's actual distance, overscan/safe area, panel brightness, and burn-in behaviour of the static header. View `?display=wall` on the TV and read the meta line from the back of the room. If it's too small, raise `--root-wall` to `100vh/44`; seven rows will then need single-line titles.
- **Live data:** refresh, new incidents arriving (the `.arrived` flash exists but the demo doesn't trigger it), and real SLO and pager numbers. `app.js` marks where the `/api/metrics` fetch goes.
- **The official compass-N symbol:** the mark is a placeholder.
- **Brand-owner approval** of the added red (`#CC2F36`) and the deepened orange text.
- **Screen readers:** I checked labels in the DOM. I did not test with VoiceOver or NVDA.
- **Browsers other than Chromium,** and fonts on a machine without the bundled files (fallback is system sans).

## 8. Proposed skill improvements (not applied)

From this project, for `design-philosophy`:
1. In `decisions.md` › Platform constraints, add: *"For wall or TV displays, size type from the viewport height (root = vh/N) so one layout serves every resolution, and set a row budget ('N open items must fit at 1080p') as an explicit, measured exit criterion."* That budget drove three of the four refinement rounds here.
2. In `critique.md` › Restraint, add: *"Check that visual weight follows importance, not quantity: a long bar or large area for a minor item can outweigh a small mark for a critical one."* I found this only by looking.
3. In `method.md` › Phase 3, add: *"Check that the existing headline numbers agree with the detail beneath them."* The original's "7 open" didn't match its own table.
