# Incident dashboard redesign

Open `app/index.html` directly; it has no build step and no network dependencies. The original is unchanged at `dashboard/index.html`, and `screenshots/original-1920.png` shows it.

URL parameters: `?state=major|major-ic|elevated|clear|stale|error|loading`, `&display=tv|laptop`, `&theme=dark|light`, and `&kiosk` to hide the demo switcher. You can also press **D** or use the "Demo states" button.

## 0. The assumption everything rests on
You asked me to use "my design philosophy", but I don't have it in this workspace and couldn't ask you. So I worked from the principles below, which I took from the brand voice ("direct, calm, competent… we don't do hype") and from what an ops room needs. **If your philosophy says something different, this is the part to check first.**

1. **Lead with the decision, not the data.** The screen should answer "is anything on fire, and is someone on it?" before anything else.
2. **Calm until it matters.** When nothing is wrong the screen should be quiet, so that alarm stays meaningful when something is.
3. **Every element earns its place for a named reader.** That reader is the ops room at 3–4 m and the engineer at a laptop.
4. **Honest states.** If the data is old or missing, the screen says so before it shows any numbers.
5. **System over one-offs.** Tokens and rules, not hand-tuned values.

Other assumptions I made:
- The TV is a 55" 1080p panel viewed from about 3 m.
- Times are UK.
- The "SLO budget" is an aggregate 28-day error budget.
- Below 25% budget the team freezes risky changes. I invented this threshold to give the meter meaning.
- I added 4 open incidents and 1 resolved incident. They make the list agree with the original's headline of "7 open", which the original table contradicted.
- I added an 8-week MTTR history and a 7-day pages average.

Every invented value is marked `added` in `app/data.js`.

## 1. Audit of the existing dashboard
| # | Problem | Why it matters |
|---|---|---|
| 1 | **The most urgent fact is buried.** A SEV1 has been open 1h 18m with *no incident commander*. That shows up only as table row 1 and a plain line of text in another card. | This is the one thing the room must act on, and nothing points to it. |
| 2 | **Trend colours are wrong.** Every trend is green: "▲ 2" more open incidents, "▲ 5" pages, and "▼ 4 pts" of budget. | Three of the four "good" signals are actually bad news. |
| 3 | **The data contradicts itself.** "Open incidents 7", but the table shows 5 *recent* incidents, 2 of them resolved. | Nobody can see which 7 are open. |
| 4 | **No freshness signal.** "LIVE" is a static red badge. There's no timestamp and nothing for stale or failed data. | A frozen TV looks exactly like a quiet day. |
| 5 | **Not readable from a distance.** Table text is 14px, pills 12px, labels `#888` on white (3.5:1). | At 3 m, most of the content is decoration. |
| 6 | **Off-brand.** Purple gradient, Arial, emoji icons, and a red "LIVE" badge in the same red as SEV1. | Nothing comes from the Northwind guide, and the badge competes with real severity. |
| 7 | **Severity is colour-only pills** (red, orange, blue). | Fails colour-vision accessibility, and blue suggests "info", not SEV3. |
| 8 | **No hierarchy.** Four equal KPI cards, each with an emoji, sit above everything else. | The page leads with averages instead of what's happening now. |
| 9 | **Fixed 4-column grid, no responsive layout, one display mode.** | It doesn't fit a TV without scrolling and breaks on narrow screens. |
| 10 | **Bar chart is decorative.** Gradient bars with labels detached above them. | The chart is harder to read than the numbers alone. |

## 2. Direction
**"Calm control room."** Deep Harbor Navy for the TV and Fog/white for laptops, in IBM Plex. One colour does all the data work (Tide Teal). Severity colours appear only where there's severity. The structure from top to bottom:

1. **Top bar.** Who we are, a freshness indicator that changes when data stops ("Live · updated 10:59:59 · every 60 s"), and the clock. The clock matters because the wall clock tells you how old "1h 18m" is.
2. **Status banner, the one headline.** It changes shape with the situation:
   - SEV1: the incident title, its age, and an "Incident commander: Not assigned" callout.
   - SEV2 only: the count and the longest-running incident.
   - All clear: a teal check, "last resolved 1h 12m ago", and "9 days since last SEV1".
3. **Open incidents.** Every open incident, most severe first, then oldest first. Each row shows ID, service, status, owner, live age and start time. "No owner" is flagged.
4. **Health.** MTTR with an 8-week sparkline, pages today against the 7-day average, and error budget as a meter. Deltas are coloured by **good or bad**, not by direction.
5. **On call.** Primary, secondary and incident commander. The commander row turns into an alert when a SEV1 is open with nobody in command.
6. **Incidents by service (30 days).** Thin single-colour bars with values at the tips. It sits lowest because it's a review metric, not a "now" one.
7. **Recently resolved** (laptop only).

## 3. Key decisions and reasons
- **I removed the "Open incidents" KPI tile.** The count now heads the incident list ("7 open · 1 SEV1, 2 SEV2, 4 SEV3 · ▲ 2 more than yesterday"). That way the number and the list can't disagree, which fixes audit item 3.
- **The commander gap is called out twice.** It appears in the banner and in the on-call panel. It's the most actionable fact on the screen, and the two panels are read by different people for different reasons.
- **Severity uses label, shape and colour.** ◆ SEV1, ▲ SEV2, ○ SEV3, plus a coloured row edge. The light-theme red/amber pair only reaches ΔE 7.0 for deuteranopes, so the shape and label are required, not decoration. The validator numbers are in `design-system/README.md`.
- **SEV3 is grey.** Low severity shouldn't compete for attention. Most of the time this keeps the screen calm.
- **Signal Orange is absent.** The brand reserves it for calls to action, and on this screen it would be mistaken for a severity. I'd rather follow the guide's "use sparingly" than invent a meaning for it.
- **Stale or down data is neutral, not red.** A feed problem gets an inverse bar ("Data is 7 minutes old… check the paging tool before acting on it"). The content below is greyed out and ages stop ticking. On TV this bar replaces the status banner, so it becomes the one headline.
- **Two display modes, one codebase.**
  - TV is dark, a fixed 16:9 layout that never scrolls, scaled to the viewport (`font-size: 100vw/96`, so 4K is the same physical size), with no tooltips or demo chrome. The incident list trims its least severe rows and names them if it runs out of room.
  - Laptop follows the OS theme (light by default), scrolls, adds the resolved table, and has hover and keyboard tooltips on the sparkline points and service bars.
  - Auto-detection picks TV at ≥1800×900; the URL can override it.
- **Type sizes from viewing distance.** At 3 m on a 55" 1080p panel, 27px body text gives roughly 13 arcminutes of x-height, which is comfortable reading. 20px is the floor for anything that must be read. Hence a 20px minimum and 27px body on TV.
- **Fonts are self-contained.** IBM Plex Mono is bundled (OFL licence included) for IDs. IBM Plex Sans isn't available offline here, so the stack falls back to the system sans. The screenshots show Inter. On the real TV box, install Plex Sans or self-host its woff2 in `app/fonts/`.
- **The logo is a placeholder.** The "compass N" is a stand-in drawn in SVG. Swap in the official asset; the guide's minimum height is 16px, and the mark here renders at 32px or more.

## 4. What I verified
- **Rendering.** I rendered all states in headless Chromium (`screenshots/`):
  - TV 1920×1080: SEV1 with no commander, SEV1 with a commander, SEV2 only, all clear, stale, feed down.
  - TV 3840×2160.
  - Laptop 1440×900, light and dark.
  - Loading state.
  - Demo panel open.
  - 390px narrow.
  - Hover tooltip.
- **Layout checks (scripted).** I scripted checks on every shot. No horizontal page scroll. On TV, no panel content is clipped (`scrollHeight ≤ clientHeight` on every panel) and the page is exactly one screen. No JS errors or console errors.
- **Interaction (scripted).** Hovering a service bar shows "Tracking Ingest: 9 incidents in 30 days (26% of 35)". Keyboard focus on a sparkline point shows the same tooltip as hover. Clicking a demo state updates the page and the URL.
- **Colour.**
  - I ran the severity palette through the dataviz validator for both themes (results in `design-system/README.md`).
  - I computed WCAG contrast for all text tokens. Muted ink is ≥ 4.9:1 on Fog and ≥ 7.4:1 on the dark panel.
  - `styles.css` contains no raw colour values; all come from `tokens.css`.
- **Data consistency.** The original's numbers are preserved: 7 open, MTTR 48m (−12%; shown as −13%, because 48 vs 55 rounds that way), 23 pages, 61% budget, the 30-day service counts and on-call. Ages reconcile with the original's opened times and durations at a snapshot of 11:00.

## 5. What I could not verify
- **Not tested on a real TV, at real viewing distance, or with the real font.** The type sizes come from arithmetic, not from standing in the ops room. That's the first thing to test.
- **No real feed.** Refresh, stale detection (I'd suggest a threshold of more than 3 missed 60-second polls) and retry are simulated. The stale and down states are shapes of the payload, not tested failure handling.
- **No screen-reader or forced-colours test.** I added `role=status` / `alert`, aria labels on the charts, and hidden "(better/worse)" text on deltas, but didn't test them with assistive technology.
- **Burn-in on an always-on panel.** Not handled. If the TV is OLED, add a slow pixel shift.
- **The thresholds and process are my guesses.** The 25% budget freeze, "SEV2s run by on-call", and the incident-commander rule all need confirming with the ops team.
