# Northwind incident dashboard redesign

The chosen direction is a calm operational ledger. It puts severity and missing ownership ahead of historical metrics, keeps all shared facts intact, and uses Northwind's navy and Plex typography rather than the original decorative gradient and emoji.

Open `app/index.html` directly from disk. There is no build, server, dependency installation or network request. The URL contract is:

`index.html?screen=live|stale|surge&theme=light|dark&display=tv|laptop`

Use one value per parameter. Missing theme follows the system preference and responds to later system changes. Missing screen defaults to live; missing display defaults to laptop. A separate review page at `review/index.html` links to all twelve combinations.

## Product priorities and evidence

1. Spot severity and unassigned command immediately.
2. Know whether the snapshot can be trusted as current.
3. Read incident facts without opening details.
4. Reach all open incidents and resolved history, then inspect supporting metrics.

Read the original dashboard and unchanged brand guide first. Read the supplied skill, its philosophy, method, identity, decisions, case recall, critique and token guard guidance. Used only the workspace's offline references. The reference contact sheet is `review/references.jpg`.

The Dia profile form and Arc routing sheet show familiar controls grouped by task, with a clear primary reading order. Borrowed the reasoning: use a familiar incident table and native controls, with small refinements in alignment. Arc's recovery card gives important information a coherent object; here, the critical incident receives a single tinted row and an explicit ownership label. Dia's context-in-composer closeup places relevant metadata beside its object; incident IDs and service names sit directly below each title. Did not copy those products' palettes, shapes, typography or signature browser components. These images are published crops and demo frames, not an observed end-to-end workflow; no transition timing or usability claims are inferred.

## Composition comparison

Two compositions were implemented and rendered at 1920px wide before choosing the final structure. Source: `review/alternatives.html` (incident-first by default; `?metrics` for metrics-first). Screenshots are preserved beside it.

| Composition | First incident top | Trade-off |
| --- | ---: | --- |
| Original dashboard | 678px | Charts and on-call context precede incidents; count and visible open list disagree. |
| Incident-first experiment | 419px | Earlier incidents and adjacent ownership; initial spacing still overflowed. |
| Metrics-first experiment | 567px | Strong metric overview, but incidents begin later and context is separated. |
| Final TV live / surge | 424px | Seven readable rows and context fit 1080p. |
| Final laptop live | 424px | Seven rows in the initial reading region; context continues below the fold. |

Selected incident-first. The final layout improves density without removing metadata. Its critical row is part of the table, not a repeated alert card. Header, metrics, ledger and side rail form a clear operational hierarchy. See `SYSTEM.md` for token choices and reasons.

## Implemented behaviour

- `live`: the first seven fixture incidents; all seven count as open, including Mitigated and Monitoring.
- `surge`: all twelve fixture incidents count as open. Laptop renders all twelve in document flow, searchable and filterable.
- `stale`: the same seven last-known incidents; a prominent warning and 09:42 last-received timestamp replace the live dot and label. Counts, durations and on-call information are explicitly last known.
- All original service counts, on-call people, shift end, MTTR, pages, SLO and resolved records remain. The original dashboard's +2 open comparison is retained in live/stale; it is omitted during surge because no surge-specific comparison was supplied. MTTR and page comparison periods follow the original dashboard. SLO has no invented comparison period.
- Exact fixture IDs, titles, services, severities, statuses, commanders, opened text and durations are preserved. Missing commander is visibly Unassigned. No commander is invented for the resolved history, which has no commander field.
- Open / Resolved view buttons, search by incident text/ID/service/status/commander, severity filter, clear filters, incident detail dialogs, Escape, focus return and TV page controls work.
- Light/dark URL overrides and responsive system-preference fallback; local bundled Plex Sans and Mono.
- Semantic landmarks, labelled controls, column headers, skip link, 44px minimum controls and 3px visible keyboard focus. No animation is required to understand any state.

### TV overflow policy

All assigned TV states fit within 1920×1080 without document scrolling. Seven incidents are shown per page to preserve reading size. Surge states show “Showing 1–7 of 12 · 5 more on the next page”; Next exposes incidents 8–12 and Previous returns. Paging is manual, not timed, so a critical row does not disappear while it is being read. The missing SEV1 commander remains visible in the side rail on page two. This accepts that a wall viewer sees the first seven by default; the other five require a keyboard or pointer. Laptop uses ordinary document scrolling and keeps all twelve reachable without pagination.

## Verification and refinements

Scripts run with installed tools only:

```sh
node outputs/verification/design-guard.mjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
/private/tmp/design-compare-venv/bin/python outputs/verification/accessibility.py
```

Chromium needed normal sandbox escalation because the macOS process could not register its Mach port inside the sandbox. Rendering succeeded after approval. No external service was used.

`verification/results.json` records all twelve required URL combinations at 1920×1080 and 1440×900. Each passed open-count and row assertions, no horizontal page overflow, theme selection, all-file requests, no JavaScript page errors, view switching, details and focus return. TV combinations additionally passed 1080p document-height checks and surge paging. Laptop combinations passed search, no results, clear filters, severity filtering and focus retention. System preference fallback and preference changes were tested separately.

`verification/accessibility.json` records a real Tab/Enter/Escape path, 3px focus styling, modal containment and return focus, reduced motion, 44px minimum target height, and a separate assertion of every shared fact for all 12 open and 2 resolved incidents. Measured initial cumulative layout shift was below 0.001 in this local Chromium run; this is not a guarantee for other hardware.

`verification/contrast.json` contains the checked text pairs. The guard passes theme token parity, no component colour literals, token-based font sizes/radii/shadows, token references, stylesheet order, text contrast ≥4.5:1, chart/control contrast ≥3:1, and byte equality of the fixture copy. Light teal text is darkened for contrast; the exact chart teal is retained on a white track.

Rendered refinement fixed: TV sidebar overflow; stale-state height; duplicate explanatory copy above and below the table; unnecessarily tall laptop chrome; low chart-track contrast; low control-boundary contrast; modal Tab focus containment. Two test harness issues were also corrected: programmatic select changes do not focus the control automatically, and system media changes require waiting for the change event.

## Limits and omitted behaviour

No backend, automatic refresh, live clock, acknowledgement, incident editing, commander assignment, escalation, alert sound or production connection is implemented or implied. The live state is labelled a snapshot. Search, filters and pagination reset on reload. There is no separate loading, permission, or total-failure screen because these states were not assigned.

Fixture opened times and durations do not always reconcile with its `now`; preserved them verbatim rather than deriving replacement values. No timezone was supplied for display fields, so no timezone label or conversion was invented. The compass-N is a locally drawn approximation because the guide supplied no official logo artwork. The frozen guide and source fixture are unchanged.

Screenshots and DOM checks cannot establish readability at the real TV viewing distance, TV colour calibration, assistive-software announcements or browser compatibility beyond installed Chromium. No screen reader, Safari/Firefox, real ops TV, touch hardware or backend was tested. The narrower-width fallback is implemented but not part of the required visual matrix.

Proposed skill lesson, not applied to the frozen skill: for wall dashboards, reserve the worst-case warning height before choosing row density, and test the stale state before polishing the live state.

## Final visual critique

Reviewed the full state contact sheet plus full-size live TV, stale TV, surge laptop, TV surge page two and incident detail captures. The three weakest remaining points are physical TV readability (not testable here), manual access to the second surge page (an explicit stability trade-off), and the laptop's historical service panel extending below the initial viewport (ordinary scrolling keeps it reachable). The first TV overflow, low-contrast tracks and laptop chrome density were corrected before this final inspection. No clipped incident titles or overlapping controls were observed at the assigned sizes.

A compact screenshot set is in `screenshots/`: `live-light-tv.png`, `stale-dark-tv.png`, `surge-light-laptop.png`, `surge-dark-tv-page-2.png`, `incident-details.png`, plus `state-matrix.jpg` covering all twelve initial states. The scripts reproduce these and their machine-readable results. `verification/input-hashes.json` records delivered source/copy hashes; the copied fixture matches byte-for-byte.
