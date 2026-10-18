# Northwind Incident Board design system: "What's open, who has it"

This is the source of truth for how the incident board looks and behaves. Read it before changing the UI. Values live in `app/tokens.css`. `tests/design.test.js` (`node --test tests/*.test.js`) fails when code uses a value that is not a token, when light and dark disagree, when a brand value drifts, or when text drops below contrast.

## 1. What it is for

Two audiences, one page:

- **The ops-room TV** (`app/index.html?display=wall`): read from about 3 m, in passing, with no mouse. The question is "is anything on fire, and is someone on it?"
- **Laptops** (`app/index.html`): engineers and incident leads checking in, at arm's length, able to click through to an incident.

In priority order:

1. **What is open now**, most severe first, with how long each has been running.
2. **Who owns it**: the incident commander per incident, and the on-call rota. A missing owner must be impossible to miss.
3. **Whether the numbers can be trusted**: when the data last arrived; stale or missing data says so in a sentence.
4. **Is it getting better or worse**: pages today, MTTR, error budget.
5. **History**: resolved in the last 24 hours, incidents by service over 30 days.

## 2. Principles

**The list is the dashboard.** Open incidents take the largest column and the top of the page. Everything else is context and sits to the right or below. The count of open incidents is the heading of the list, not a separate tile.

**Colour only for trouble.** A calm board is almost monochrome navy/fog. Red appears only when something is SEV1 or broken; orange only when something needs attention. If the board is colourful, something is wrong, and that is the point.

**Words over badges.** "No incident commander", "5 more than all of yesterday", "12% faster than last week", "No new data since 10:54". No arrows that need a legend, no emoji, no "LIVE" pill that stays on when the feed is dead.

**Honest and stable.** Space for every region is reserved before data arrives (zero shift above the list between loading and loaded, measured). Stale data is labelled, not dimmed into illegibility. A source that fails is "missing, not empty".

**One page, two distances.** The same layout serves the TV and the laptop because every size is in `rem` and the wall display sets the root size from the screen height (§6). No second design to drift.

**Novelty where it pays: the 24-hour lane.** Each incident row carries a thin bar on a shared 24-hour axis that ends at "now". Every open bar grows towards the same now-edge as time passes, so from across the room you see at once what just started (a dot), what has been running all night (a long bar) and which incidents overlap. Resolved incidents keep their bar, ended before now, in a quiet grey. Everything else on the page is plain.

## 3. Colour

Neutrals come from the brand (Fog, Slate, Harbor Navy). Dark is its own navy-derived palette, not an inversion. Each remaining colour has one job:

| Token | Light / dark | Means | Use for | Never for |
| --- | --- | --- | --- | --- |
| `--bg` | `#EEF1F4` Fog / `#0A1828` | page | ground | |
| `--surface` | `#FFFFFF` / `#11253C` | grouped fact | the on-call band, tooltip, controls | cards around every block |
| `--fg` / `--fg-strong` | Slate `#3D4852`, Navy `#12355B` / `#D9E1E9`, `#FFFFFF` | text | body / titles and numbers | |
| `--muted` | `#56626E` / `#9AACBF` | secondary text | meta, labels, axis | anything the user must act on |
| `--brand` | `#12355B` both | Northwind | the mark only (white-on-navy tile in dark, per brand rule) | UI chrome, data |
| `--critical` / `--critical-text` | `#CC2F36` / `#B42318`, `#FF8A80` | SEV1, broken | SEV1 tag and bar; failed source title | SEV2, decoration |
| `--attention` / `--attention-text` | Signal Orange `#F26B21` / `#A6410C`, `#FF9A5C` | needs attention | SEV2 tag and bar; missing owner; stale-data sentence | large areas, body text (brand rule) |
| `--data` | Tide Teal `#2A9D8F` both | the measured series | chart marks, meter fill, today's column | status, text |
| `--data-quiet` | `#BFCAD5` / `#34506E` | context data | earlier days, meter track, resolved bars | |
| `--minor` | `#9AA7B4` / `#4F6884` | SEV3 | SEV3 timeline bars | — deliberately quiet so a long SEV3 never outweighs a new SEV1 |
| `--focus` | `#12355B` / `#8FB8E8` | keyboard focus | focus ring | |

Rules:
- Brand values are used exactly as fills and marks; the guard test pins Harbor Navy, Signal Orange, Tide Teal, Fog and Slate.
- Signal Orange is 2.9:1 as text on white, so orange **words** use `--attention-text` (`#A6410C`, 5.3:1 on Fog). Ink, not white, sits on orange fills (white on orange is 2.9:1).
- The brand has no red. `#CC2F36` was chosen to sit beside Navy and carry white text at 5.2:1.
- Tide Teal on Fog is 2.93:1, just under 3:1 for graphics. It stays exact because the brand names it for charts; the relief is that every chart value is also printed as text. The guard test records this as the one exception.
- SEV3 has no colour: its tag is plain text. Colour is not a severity scale here, it is an alarm.
- Errors are words plus a tinted band, never colour alone.

## 4. Type

IBM Plex Sans and Plex Mono, per the brand guide, shipped locally in `app/fonts/` (latin subset, OFL) so the TV doesn't depend on the network. Fallback is the system sans.

| Token | Size | Use |
| --- | --- | --- |
| `--fs-hero` | 3rem | the open-incident count, one per view |
| `--fs-xl` | 1.75rem | stat values, clock |
| `--fs-lg` | 1.25rem | incident titles, open durations |
| `--fs-md` | 1rem | body, on-call names |
| `--fs-sm` | 0.875rem | meta lines, labels |
| `--fs-xs` | 0.8125rem | axis, "since 09:42", captions |

- Plex Mono for incident IDs and durations, so durations align in their column (brand: "Mono for IDs and tabular figures").
- Big standalone numbers (count, stat values) use proportional Plex Sans. The clock uses Sans with `tabular-nums` so it doesn't jitter as minutes change.
- Hierarchy by weight (400/500/600) before size. Labels are sentence case, never uppercase.

## 5. Space and shape

- One gutter (`--gutter`, 2rem); spacing steps `--sp-1`…`--sp-6`.
- Nearly square: `--radius-sm` 2px for tags, bars and meter; `--radius-md` 4px for the focus ring and tooltip. Freight-precise, not friendly-soft.
- Hairlines separate rows and stats. One filled band per page (on call). Only the tooltip floats and has a shadow.

## 6. Layout

```
header:   mark · Northwind | Incidents   freshness sentence                    11:00 Sun, 18 Oct
on call:  Primary … · Secondary … · Incident commander … · Handover 18:00 to …        (one line)
board:    [ N open incidents · counts · 24h axis · Running ]   [ Pages today        ]
          [ incident rows, SEV1 → SEV3, newest first in band ]   [ MTTR, 7 days       ]
          [ Resolved in the last 24 hours                    ]   [ Error budget       ]
                                                                 [ By service, 30 d   ]
```

- Columns 2.4 : 1. Row columns are tokens (`--col-sev`, `--col-lane`, `--col-dur`) shared by the list head so the axis lines up with the bars.
- **Desk** root is 16px. Typical 1440×900: all seven open incidents are above the fold (first row at 185px; was 707px). The page may scroll.
- **Wall** root is `100vh / 48` (22.5px at 1080p, 45px at 4K), so the board is the same proportion on any TV. Dark by default. Never scrolls, no cursor, no controls. If rows don't fit, history goes first, then the least severe open rows, and a sentence lists the IDs not shown.
- **Narrow** (< 60rem): one column; the on-call band stacks; the lane is hidden and the duration becomes a line under the title.

## 7. Components

- **Incident row.** Severity tag · title (2 lines max, full title on hover) · meta (`ID · service · status · IC name` or "No incident commander") · 24h lane · duration with "since". Whole row is one link to the incident. Screen readers get one sentence per row via `aria-label`.
- **Severity tag.** SEV1 red fill, white text; SEV2 orange fill, ink text; SEV3 plain muted text. Resolved rows lose their fill.
- **24-hour lane.** Hairline track, one gridline at midnight, bar from opened to now (or to resolved). A bar that began before the window has a square left end. Open bars end in a dot at the now-edge.
- **On-call band.** One line. If every shift ends at the same time, the handover is said once. Unassigned is orange words. Failure turns the band red-tinted with a sentence.
- **Stat.** Label, value, delta in words, one small chart. Pages: 14 columns, today in teal, the rest quiet (emphasis, not categorical). MTTR: 8-week line, 2px, end dot. Error budget: meter, teal fill on a quiet track; orange below 25%.
- **By-service bars.** One series, one colour, value at the tip, square at the baseline, 2px-rounded data end.
- **Freshness.** "Updated 11:00:00 · 12 s ago" in muted text; when stale the whole header tints orange and the sentence says since when and what happens next.

## 8. Motion

One easing (`--ease`), 150ms for hover, 250ms for a bar growing. A newly arrived incident may flash once (`.arrived`, 1.2s). Nothing loops. `prefers-reduced-motion` removes all transitions and animation.

## 9. Writing

Direct, calm, competent (brand voice). Examples:
- Stale: "No new data since 10:54 (6 min). Figures may be out of date; retrying every 60 s."
- Failure: "The rota didn't load. The paging service timed out at 10:59:58. It is missing, not empty: check the paging tool for who is on call."
- Empty: "Nothing open. The last incident closed at 07:48, 3 hours 12 minutes ago: INC-2291 Route optimiser timeouts for EU-West depots."
No exclamation marks, no emoji, no hype.

## 10. Brand

The "compass N" symbol beside the wordmark is a **placeholder** drawn in `index.html` (a north-pointing needle, filled north half). Replace it with the official asset. Per the guide, the symbol is never recoloured except to white on Harbor Navy, which is what the dark theme does.

## 11. Keyboard and accessibility

- Tab order: incident rows (most severe first), resolved rows, chart columns (desk only), prototype controls.
- Focus ring 2px `--focus`, kept on the same incident across re-renders.
- Tooltips enhance, never gate: every chart value is in `aria-label`s and in text.
- `role="status"` on freshness; the board does not announce every refresh.

## 12. Before you ship a UI change

- [ ] Tokens only; `node --test tests/*.test.js` passes.
- [ ] Looked at wall 1920×1080 (dark), desk 1440×900 (light and dark), 390px, in live, loading, all clear, stale, partial and surge.
- [ ] Nothing above the list moves between loading and loaded.
- [ ] No new colour meaning, card, or badge where a word would do.
- [ ] Seven open incidents still fit on the wall at 1080p.
- [ ] Copy says what is stale, what failed and what to do.
