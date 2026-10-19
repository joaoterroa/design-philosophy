# Northwind incident dashboard

Open `app/index.html` directly from disk. No build, server, dependency installation or network is required.

Direct route format: `app/index.html?screen=live&theme=dark&display=tv`. Screen supports `live`, `stale`, `surge`; theme supports `light`, `dark`; display supports `tv`, `laptop`. Missing theme follows the system preference, including preference changes. Defaults are live and laptop. There are no state selectors inside the product.

## Direction and evidence

The ordered priorities are severity and ownership, freshness, exact incident detail, then on-call and historical context. Brand guidance determined navy, Fog, restrained orange and IBM Plex typography. The visual preference for this task is a precise operations ledger with a fixed context rail; it suits cross-row comparison and the room display rather than suggesting a universal dashboard style.

Read the supplied skill and its philosophy, method, identity, decisions, critique, case-recall and system templates. Offline research examined `reference-pack/dia-profile-form.png` and `arc-recovery.png` with the supplied source manifest. The profile frame makes the current task clearly dominant; the recovery card gives critical information a stable, recognizable object. Borrowed hierarchy and careful grouping, not their palettes, rounded surfaces or branding. These are cropped official frames, not evidence of complete flows or transitions. No external research was performed.

Rendered two comparable critical-screen compositions before implementing: `exploration/compare.html?table` and `?board`, with saved PNGs. The table keeps status and ownership comparable; the split board makes the monitoring column overflow at 1080px while leaving its other column underused. Chose the table and accepted a deliberate TV pagination trade-off.

The original rendered TV table began at y=678px, after two rows of secondary cards; it used 14px incident text, lacked commanders and displayed only three open fixture records. The redesign places the incident panel at y=321px on TV and 325px on laptop, with all seven initial incidents. Strong summary figures remain, but the incident record owns most of the screen. Teal is historical data, rose means critical attention and orange marks warnings. All semantic colours are accompanied by text.

## Implemented

- All three direct states in both themes and display sizes; light/dark system fallback.
- First seven fixture incidents for live/stale; all twelve for surge. Monitoring and mitigated count as open. Exact fixture facts, services, metrics and resolved records are retained. The original open-count comparison of +2 is retained for the seven-record view; no comparison is invented for surge.
- Missing incident commander is explicitly Unassigned, with an attention marker. On-call cover and the separately unassigned overall commander remain visible.
- Stale warning says last snapshot 09:42 and warns that counts, statuses and durations may have changed. No live dot in stale. Nothing ticks or refreshes. All screens explicitly identify offline snapshot data.
- Laptop: all rows on a normally scrolling page, plus search. TV: seven visible rows; surge shows 1–7 of 12 with Next/Previous and explicit page count. The final five are on page two; no timer rotates records out of view. This preserves legibility instead of squeezing twelve records onto a wall screen. An unattended TV only shows its selected page.
- Incident and resolved-history detail dialogs expose the full supplied record. Resolved titles, IDs and durations are visible in the rail; service, severity, opening time and status are available in their dialogs.
- Semantic table headings, labeled search and navigation, native dialog, skip link, visible focus, keyboard actions, Escape dismissal and focus return. Search keeps input focus. Buttons are at least 44px high. No motion is required to convey information.

## Rendered critique and refinement

First pass overflowed the TV frame. Reduced vertical spacing and adjusted TV row height while retaining the full information. Second pass showed the additional stale banner would push the footer out; placed that warning in the title row, keeping the records stationary. Final TV footer bottom is 1031px in all states and themes; no horizontal overflow. Laptop vertical scrolling is intentional (surge footer around 1466px). A dark-mode compass cutout was corrected so the N remains legible.

The weakest remaining points are physical viewing distance, the cost of manually paging an unattended surge screen, and a locally interpreted compass rather than the official asset. These are recorded trade-offs and evidence limits, not hidden working behavior.

## Verification

Run from the workspace root:

```sh
node outputs/verification/guard.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

Both pass. Browser launch needed normal sandbox escalation because macOS denied Chromium's local Mach service inside the sandbox.

`verification/results.json` records all 12 combinations at laptop 1440×900 and TV 1920×1080. Checked route rendering, fixture counts, stale visibility, missing commander, five services, two resolved records, zero page errors, zero network requests, horizontal overflow, TV frame fit, modal/Escape/focus return, keyboard pagination, search/no-results and focus retention. System dark/light changes were also checked. Tests use reduced motion. Extended checks (`extended.py`, results in `extended-results.json`) verified every laptop surge record against its fixture, resolved detail facts, 44px minimum visible control heights, modal Tab containment and absence of TV document overflow. Measured CLS was 0 for the TV and laptop surge loads in that run; this is not a claim about future live updates. `verification/contrast.json` records tested pairs: normal and semantic text exceeds 4.5:1 and chart fills exceed 3:1 against the canvas. Guard checks token use, light/dark parity and exact copied-fixture identity.

Captured all 12 state screenshots; retained the contact sheet and a representative set of full-size screens, TV surge page two, a baseline and composition studies. Personally inspected the rendered alternatives, live laptop light, surge laptop dark, live TV light, and stale TV dark; the contact sheet covers the remaining route renders. Screenshots include focus outlines deliberately exercised by keyboard tests.

No live backend, automatic refresh, incident editing, assignment, acknowledgement, authentication or fabricated production links. No loading, empty-source, backend-failure or permission flows are invented; search has a real no-results state. No real screen reader or physical TV was available. The prototype does not claim those checks or reconciliation of inconsistent supplied clock/duration values. The fixture's duration strings are preserved verbatim.

Suggested method lesson, not an edit to the frozen skill: for wall dashboards, compare compositions with the overflow state before freezing row density; seven useful records and explicit paging can be safer than shrinking every row to fit an exceptional surge.
