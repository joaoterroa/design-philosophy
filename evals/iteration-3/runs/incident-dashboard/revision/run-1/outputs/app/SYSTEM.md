# Northwind operations design system

Read this before editing the dashboard. The source of truth for values is `tokens.css`; `../scripts/guard.mjs` checks token use, theme parity, contrast, fixture fidelity and wiring. Project rationale and evidence live in `../DESIGN.md`.

## Purpose

Ops engineers need severity, affected service, ownership and freshness first. Aggregate metrics provide context; resolved history remains visibly separate from open work. Preserve every supplied fact rather than making a cleaner screenshot by deleting data.

## Roles

- Harbor Navy `#12355B`: Northwind identity and the header, white wordmark and compass above it. Never use orange as a broad fill.
- Fog `#EEF1F4` and white: daylight canvas and working surfaces. Dark counterparts are `#0B1927` and `#102436`.
- Body `--fg`, secondary `--muted`, headings `--heading`: separate hierarchy with contrast in both themes.
- Critical `--critical` / `--critical-bg`: SEV1 and unassigned command. Always use text, never color alone.
- Caution `--warning` / `--warning-bg`: SEV2 and stale data. Signal Orange `#F26B21` is only the warning edge.
- Teal `--teal` / `--bar`: improvement text, snapshot indication and service-volume bars. The brand's `#2A9D8F` is adjusted to `#18786D` for light text and `#248779` for bars, to meet contrast. Dark counterparts are `#7BD3C5` and `#53B8A6`.
- `--quiet` / `--quiet-bg`: lower-severity labels. Severity is still written out.

## Typography

Bundled IBM Plex Sans for the interface, matching the brand; IBM Plex Mono for IDs, durations, counts and aligned statistics. Laptop scales: 13px metadata, 14px supporting fields, 16px body, 18px titles, 20px section headings, 32px page heading, 44px metrics and 56px open total. TV: 16px metadata, 18px supporting fields, 20px incident titles/body, 24px sections, 36px page heading, 52px metrics and 64px open total. Weights 400/500/600 distinguish metadata, active content and headings.

## Layout, space and shape

A navy header, compact heading and grouped metric band precede a wide table and narrower context column. TV uses 48px page gutters, 32px column gap and a 410px side column. Laptop uses 32px gutters, 24px gap and 330px context. Space tokens follow a 4px rhythm from 4 through 48px. The TV table holds seven 64px rows and uses manual pagination for surge. Laptop rows are at least 74px and remain in document flow.

Panels use 8px corners and hairline borders; controls and severity labels use 4px corners. Most separation uses alignment, space and lines. Only the modal receives a shadow, because it occupies a foreground interaction layer. Breakpoints at 1100px and 600px are literal CSS media-query thresholds (CSS custom properties cannot be used in media conditions); primary verification covers the contracted TV and laptop sizes.

## Components and behavior

- Metrics are a single band, not four competing floating cards. Open count has priority and includes severity totals.
- Table rows expose IDs, titles, service, severity, status, opened time, commander and duration. The title and its metadata share a 44px button target. No clipped title or tooltip-only fact.
- Resolved history is a separate region and excluded from open totals.
- The side column keeps named primary/secondary contacts and unassigned command visible above the service ranking. Bars use a common maximum of 14, exact counts remain adjacent.
- Stale changes wording, warning surface and coverage heading, not just a dot. Recorded facts remain visible with their limitation.
- Native modal semantics, Close and Escape, keyboard containment and focus return. One control per action.
- Page controls retain focus; unavailable directions use `aria-disabled` and ignore activation. The changing range is polite live text. No automatic page rotation.

## Motion, voice and accessibility

120ms ease-out only for hover color changes; zero under reduced motion. No pulsing live indicator, looping skeleton or timer. All data remains visible with motion disabled.

Direct, calm, competent copy: “Updates unavailable.” / “Unassigned” / “Showing 1–7 of 12.” No hype or hidden guarantees. Snapshot limitations remain explicit.

Visible 3px focus rings and 44px minimum control height. Table column headers and labeled title buttons expose the data structure. First Tab reveals a skip link to open incidents. Themes are set before styles render to avoid the wrong initial palette. Follow system theme changes only without an explicit URL override.

## Before a change is ready

Run `node outputs/scripts/guard.mjs` and the browser script from the workspace root. Inspect both themes in every contracted state, including stale and surge page two. Keep TV document height at or below 1080px, avoid horizontal overflow, preserve complete laptop reachability, test focus return and preserve the fixture inputs. Physical viewing distance and real data remain production checks.
