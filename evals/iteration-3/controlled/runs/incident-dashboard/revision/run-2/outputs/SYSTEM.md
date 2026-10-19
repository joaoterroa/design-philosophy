# Northwind incident overview: operations ledger

Read this before changing the interface. Values live in `app/tokens.css`; run `node outputs/verification/guard.cjs` from the workspace root.

## Purpose and priorities

For operators triaging on a laptop and teams glancing at a wall display:
1. Identify severity and missing ownership.
2. Know whether the information can be trusted as current.
3. Read exact incident status, service, opening time and duration.
4. See on-call cover and longer-term service context.

## Principles

Use a familiar severity-ordered table, not a new workflow. Keep unresolved statuses open. Make missing ownership a word and an exclamation mark as well as a colour. Keep time values exactly as supplied. Do not suggest that this offline snapshot connects to production.

The distinctive treatment is a freight-operations ledger: strong numeric summary, aligned records, and a narrow operational-context rail. Expression comes from proportion and typography rather than decoration.

## Colour and identity

Harbor Navy `#12355B` anchors the wordmark. Fog `#EEF1F4` is the light canvas. Signal Orange `#F26B21` is only a small warning rule, never body text or a large surface. Tide Teal `#2A9D8F` informs the chart palette: the light chart uses deeper `#247F75` for contrast and dark uses `#56B9A9`. Main light text is a navy-derived `#172F46`; muted text is `#526371`, selected for at least 4.5:1 on used surfaces. Critical rose is separate from the brand orange. Severity always has an explicit text label. Dark mode uses independent navy surfaces and lighter semantic text.

`contrast.json` records the tested foreground/background pairs. The guard checks theme colour parity, token wiring, component colour/type/radius/shadow tokens, used text pairs, graphics and fixture identity. Layout percentages, responsive breakpoints and structural geometry are not forbidden by the guard.

## Type, shape and spacing

Bundled IBM Plex Sans for the brand and interface, IBM Plex Mono for IDs, times and metrics. Laptop scale: 12, 14, 16, 18, 20, 24, 28, 34, 48px. TV raises supporting text to 14–18px and headline figures to 56px. Base spacing uses 4px multiples with 32px laptop / 40px TV gutters. Small 4px controls and 8px panel corners support dense reading. Hairlines group data; only the modal has a shadow. Native dialog and standard buttons avoid custom interaction learning.

## Layout and behavior

At 1440×900, the page scrolls normally; all seven or twelve incidents remain in the DOM, searchable by title, ID, service, status or commander. At 1920×1080, seven readable records fit with all context. Surge has two manually selected pages, seven then five records. No automatic cycling interrupts reading; the cost is that the remaining five incidents require the next-page action. Page count and total remain visible.

Stale warning replaces the ordinary snapshot indicator in the title row, preserving the table position. All values remain frozen. Snapshot date and supplied display time are not inferred time-zone conversions.

Incident titles and resolved entries open a native detail dialog. Escape and Close return focus to the opener. Pagination moves focus to the usable reverse control. Search leaves focus in the input. Controls have at least 44px height, a visible focus outline and accessible names; native Tab order is retained. The skip link goes to the incident region. No app-specific keyboard shortcuts.

## Motion, voice and brand limits

No animation or automatic refresh; reduced motion preserves all information. Copy is direct, calm and specific: “Data is stale”; “No open incidents match…”. No success toast is needed for read-only browsing.

No production logo asset was provided. The compass N is a local SVG interpretation, navy on light and white on a navy backing in dark mode, rather than a claim to reproduce an approved master asset. Replace with the official mark when supplied.

## Change checklist

Run the token guard and browser script; inspect both themes at both assigned viewports. Verify all three states, missing commander, full surge access, modal focus return and stale wording. Keep fixture data immutable and all assets local. Review physical TV distance and actual assistive technology separately.
