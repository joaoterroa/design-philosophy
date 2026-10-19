# Northwind Incidents — operations board

Read this before changing the prototype. Values are in `app/tokens.css`; run `node outputs/verification/design-guard.mjs` from the workspace root after a visual change.

## Purpose and priorities

Ops engineers use the board across a room and while investigating on a laptop. In order:

1. Identify the most severe open incident and missing ownership.
2. Distinguish current snapshots from stale evidence.
3. Read status, service, commander, opened time and duration without opening another tool.
4. Understand supporting metrics and reach every open or resolved incident.

## Principles

Use a familiar table; make its severity order, baselines and metadata exceptionally clear. Keep operational meaning in words as well as colour. Preserve all fixture facts; do not recompute supplied durations from the clock. Use secondary surfaces for on-call context and service history, never ahead of incidents. Novelty is confined to the composition: a single ledger with the critical row integrated into it, rather than an extra urgent card that repeats the same incident.

## Identity and colour

Harbor Navy `#12355B` anchors the header in both themes. Fog `#EEF1F4` is the light ground; the dark ground and panels are distinct navy neutrals. IBM Plex Sans provides the brand voice; Plex Mono makes IDs, durations and metrics easy to compare. The guide's Slate is superseded by a darker blue-neutral foreground for this dense operational use; the guide itself is unchanged.

Red identifies SEV1 and missing ownership. Amber identifies SEV2 and stale evidence, always with explicit labels. Teal identifies the historical service bars and lower MTTR. Exact Tide Teal `#2A9D8F` is used for light chart fills; dark mode lightens it. Teal text uses `#18786E` in light mode to pass contrast. Exact Signal Orange is reserved in the token vocabulary but intentionally unused: the read-only board has no primary call to action and orange would compete with caution.

Foregrounds pass 4.5:1 for the tested role/surface pairs. Meaningful chart bars and control boundaries pass 3:1. Light chart tracks use white to let the exact brand teal clear 3:1. Colour roles are repeated completely in dark mode.

No original logo artwork was supplied. The small white compass-N is a locally drawn approximation, not a claim of an approved brand master. It stays white on Harbor Navy and is hidden from assistive technology because the adjacent wordmark supplies the name.

## Type and geometry

Laptop scale: 13, 14, 16, 18, 20, 24, 30 and 48px. TV scale: 17, 18, 20, 22, 24, 26, 34 and 48px. The metric number is intentionally large; incident titles remain the reading focus of the ledger. Use medium titles, regular metadata and monospaced figures. All fonts are bundled WOFF2 files.

Spacing follows 4/8/12/16/20/24/32/40/48px. A 6px radius softens containers and controls without turning operational labels into pills. There are no shadows, gradients or decorative emoji. Structural percentages, grid fractions, media breakpoints and line-height ratios are layout constants; component colours, font sizes, radii and shadows must use tokens. The automated guard enforces those categories and checks undefined tokens.

## Layout

The 1920×1080 TV uses 40px side gutters, a 370px context rail and up to seven incident rows. It fits every assigned state without page overflow. Two-column on-call names and compact chart spacing preserve incident type sizes. A surge uses explicit, manual pagination, with total and continuation text. No auto-rotation removes information while someone is reading. The on-call rail still makes missing SEV1 ownership visible on page two.

At 1440×900 the table has all seven or twelve rows in document flow. Search and severity filtering sit beside the view controls. Normal page scrolling reaches the rest of the board. Both history records appear in the Resolved view. Narrower widths rearrange the sidebar and allow horizontal table scrolling; these are fallbacks, not the assigned evaluation sizes.

## Components and states

Open / Resolved are ordinary pressed-state buttons within a named group, not ARIA tabs with incomplete arrow-key semantics. Each title opens a native modal containing all incident facts. The modal has one focusable Close button, retained on Tab; Escape closes it and focus returns to the title. Search preserves input focus while results update; no results has a working Clear filters action. TV paging focuses the enabled reverse direction after the page changes.

Stale has no live dot or live label. A high-contrast sentence states the last received time and that counts, statuses and durations may have changed. The on-call heading also says last known. Frozen fixture times are not timezone conversions.

## Motion and accessibility

No automatic animation or refresh; the duration token is 0ms. Reduced motion preserves every piece of information. Controls have at least 44px height, visible 3px focus outlines, native keyboard behaviour and accessible names. The page supplies landmarks, a skip link, table headers, a caption, live announcements for view and paging changes, and a labelled dialog. No custom shortcuts intercept browser commands.

## Writing and maintenance

Direct, calm and specific. Example stale message: “Updates are unavailable. Counts, statuses and durations may have changed; confirm with the on-call team.” Example empty message: “No matching incidents. Try another search or severity.” Do not imply a backend connection, a commander assignment action or a successful refresh.

Before handing over: rerun the token/contrast guard, the twelve URL combinations and keyboard/fact checks; inspect actual screenshots; ensure fixture copy equality. Real TV viewing distance and screen-reader software still need human validation.
