# Northwind incident operations — operational ledger

Read this before changing the interface. `app/tokens.css` owns visual values; `app/style.css` applies them. Run `node outputs/verification/guard.cjs` from the workspace root after changes.

## Purpose and priorities

This is an incident snapshot for operators looking across a room and engineers investigating on laptops. Priorities, in order:

1. See the number and severity of open incidents, then the urgent incident.
2. See missing responsibility without opening a detail view.
3. Know whether the data is current or stale.
4. Reach every incident and retain its exact operational facts.
5. Keep historic metrics and coverage available without competing with current incidents.

## Principles and identity

The structure is an operations ledger: broad aligned incident rows with a narrower operational-context column. It is derived from a logistics team's working board, not a collection of analytics cards. A separate resolved strip prevents a resolved event being mistaken for an open one.

The single emphasized treatment is the SEV1 exception row, which visually joins severity, incident and missing commander. No decorative icon collection, card shadows, animated pulse or gradient competes with it. The layout, type alignment and short labels carry the rest of the hierarchy.

IBM Plex Sans is the supplied brand face; IBM Plex Mono makes IDs, durations and metric figures easy to compare. The text wordmark uses the brand face. No compass symbol asset was supplied; do not invent a replacement logo. A production brand owner can supply the approved symbol.

## Colour roles

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| Ground | Fog `#EEF1F4` | `#0E1C2A` | Calm continuous working surface |
| Header / controls | White | `#142637` | One clear structural header; tangible controls |
| Brand / figures / focus | Harbor Navy `#12355B` | `#C2D9EE` | Brand hierarchy; contrast in dark mode |
| Body | Slate `#3D4852` | `#E4EBF1` | Exact brand body text; pale counterpart for dark mode |
| Secondary text | `#566675` | `#A5B5C4` | Secondary facts remain readable |
| SEV1 / missing commander | `#A52D38` | `#FFABB2` | Exceptional incident / missing ownership, always labelled |
| SEV2 / stale caution | `#85440E` | `#F3BF8C` | Caution with explicit words |
| Current snapshot / MTTR improvement | `#18685F` | `#89D1C4` | Positive data context, never incident resolution by implication |
| Service history bars | `#238D81` | Tide Teal `#2A9D8F` | Brand-derived data graphic |

Light teal bars are darkened from the exact brand teal to hold at least 3:1 on Fog. Signal Orange is retained as a brand token but unused: there is no write action deserving that accent. It is never body text. Surface borders group; they do not encode incident severity. Text pairs tested hold at least 5.21:1, meaningful chart/focus pairs at least 3.56:1. Do not use muted text on arbitrary new backgrounds without checking it.

## Type, spacing, shape

Laptop: 12px metadata, 14px secondary table columns, 16px incident titles/body, 24px section heading, 54px metric figures. TV: 14px metadata, 16px secondary columns, 19px incident titles, 26px heading, 64px figures. Use regular/medium/semibold, not additional weights for emphasis. IDs and time quantities use Mono. The TV's small metadata is supporting information; critical titles, counts and responsibility use larger type.

Spacing is a 4px scale with 8, 12, 16, 20, 24, 32, 40 and 48px steps. Laptop gutter is 32px; TV gutter is 48px. Small 4px corners belong to controls and the dialog only. No dashboard-card shadows; the modal alone has elevation. Native controls and incident buttons are at least 44px high.

## Layout and behavior

Header → freshness strip → four metrics → incident ledger and context → resolved history → provenance footer. TV is tuned for 1920×1080; laptop for 1440×900. TV has 64px incident rows and seven incidents per page; table space stays reserved on its second page. Laptop uses 76px rows with ordinary document scrolling, a sticky table header, full-list search and severity filtering. No nested scrolling at the assigned sizes. Below 1000px context moves beneath the ledger; below 650px the ledger scrolls horizontally. These smaller sizes are a fallback, not assigned validation targets.

Live and stale use the first seven incident fixtures; surge uses all twelve. Monitoring and mitigated are open. Stale data retains its facts with a prominent persistent warning. Resolved history stays separate and does not change open counts. Dialogs repeat available data rather than inventing an incident timeline.

## Controls, keyboard, motion and voice

Search and severity controls have persistent accessible labels. Filtering updates rows without replacing the focused control. Empty results give one Clear filters action. Incident buttons open native modal dialogs; Escape and Close restore focus. Pagination moves focus to the available return control. Tab order follows the reading order. The skip link reaches the ledger. Focus is a 3px high-contrast outline.

No motion is necessary for a snapshot: reduced motion loses no information. A system-preference listener updates the theme unless a valid URL theme overrides it. Voice is direct, calm and factual: “Updates interrupted. Last received 09:42.” Never claim a retry worked, a commander was assigned or an incident resolved without evidence.

## Before shipping another change

- Recheck all three states × two themes × two assigned sizes.
- Run the token and fixture guard and browser checks.
- Check the longest title, unassigned commander and final surge incident.
- Keep the seven-row TV board within 1080px; disclose remaining incidents.
- Inspect focus, modal return, search, filters and stale copy.
- Live connectivity and physical TV viewing need separate production validation.
