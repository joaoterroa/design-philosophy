# Northwind: the operations board

Read this before changing the interface. Values are in `app/tokens.css`; run `node verification/design-guard.cjs` after any visual change.

## Users and priorities

Engineers see this board across an ops room and while investigating on a laptop. Priority order:

1. Find the most severe open incident and its owner.
2. Distinguish current snapshots from outdated information.
3. Read every incident, including mitigated and monitoring work.
4. Keep operational context and history nearby.
5. Preserve a quiet board during long shifts.

The additional contract flows serve different moments: Rota is a compact mid-shift handover; Harbour is an occasional-use setup flow with large type and controls.

## Direction and identity

The dashboard is a flat, aligned operations board. A single metric band replaces decorative cards. The distinctive treatment is the severity-one row: incident, missing commander and status share one restrained alert ground. It connects urgency to accountability.

Northwind's exact Harbor Navy anchors the header. Fog is the light workspace; dark mode uses deep blue surfaces rather than black. IBM Plex Sans carries all prose; Plex Mono aligns durations, counts and IDs. Flat edges and four-pixel severity corners suit an operational table. Rounded floating surfaces are reserved for popovers and dialogs.

No official logo file was supplied. The small compass is a provisional vector interpretation of the guide's compass-N description, white on Harbor Navy; it needs brand-owner review before production use.

The Rota symbol is a quiet shift dial. Its handover shows the current and proposed owners together, and says who remains responsible. Harbour's proposed mark resembles a harbour entrance. Its account-shaped welcome object previews the account rather than presenting a decorative illustration. Neither Rota nor Harbour has a supplied brand guide; their identities are provisional and deliberately simple.

## Colour roles

| Role | Light | Dark | Use |
|---|---|---|---|
| Brand | #12355B | #12355B | Northwind header, white mark |
| Text | #253746 | #EAF0F5 | Primary reading |
| Secondary text | #566575 | #A7B8C7 | Metadata with full text contrast |
| Action | #12355B | #B9D8F4 | Buttons, links |
| Critical / missing owner | #B5362D | #FFADA3 | Severity-one, missing commander, errors |
| Caution | #85500C | #F0C58D | Stale data, pending responsibility, severity-two |
| Confirmed state | #216A57 | #91D3BA | Accepted handover, completion, current snapshot label |
| Service bars | #217D73 | #65C4B4 | Counts by service, always paired with values |

Signal Orange #F26B21 is only a small highlight on the Harbour account object; never body text or a large area. Exact Tide Teal is preserved as a brand token and account boundary accent. The chart shade is darker in light mode and lighter in dark mode to meet contrast. The guard checks text at 4.5:1 and chart bars at 3:1.

## Type, space and shape

The type scale is 12, 14, 16, 18, 20, 24, 32, 40, 56 and 68px. TV incident titles are 20px; metrics 56px; metadata 14px. Laptop prose is 16px with 12px metadata. Banking labels and controls are 18–20px. Large numbers use tabular Plex Mono.

Space follows 4, 8, 12, 16, 20, 24, 32, 40 and 48px. The dashboard has 40px outer gutters and 32–40px between incident and context columns. Border radii are 4px for small labels, 8px for controls, 16px for floating containers. Only floating containers have a shadow.

Layout dimensions, target minima, border widths and percentage data widths are structural values. Type sizes, radii, colours, shadows and motion values must come from tokens. The automated guard enforces those categories and theme parity.

## Layout and behaviour

At 1920×1080, the TV board stays in the frame. Seven open incidents fit in the first page; surge adds a deliberate next page for the remaining five. No automatic rotation moves content while someone reads it. The count and next-page statement prevent hidden overflow. At 1440×900 the page scrolls normally; all twelve surge incidents are in the document. Incident titles open full, keyboard-accessible details. Resolved history is compact on TV, with service and opened facts in the same details dialog.

The Rota root is 360px wide at (20,20), maximum 640px high. Longer states scroll inside that boundary. The roster explicitly says four currently on call; forty describes the team, not the roster.

Harbour is a single-column setup. At 320px, content scrolls vertically where needed; labels and targets do not shrink to force everything into one screen. The welcome action remains in the initial viewport. Help is a native modal with a telephone link and the safety warning.

## Accessibility and motion

Use semantic headings, table headers, visible form labels, native buttons, select, inputs and dialogs. Focus moves to the new screen heading or invalid field; dialog dismissal returns focus to its trigger. Focus outlines are three pixels with an offset. Banking buttons are at least 52px high and text inputs at least 56px. Menu buttons are at least 46px. Incident titles are keyboard buttons.

There are no looping animations, refresh timers or automatic transitions. Reduced motion preserves exactly the same information. Theme comes from the URL when specified and system preference otherwise; system changes are observed.

## Voice and preflight

Calm and specific: “You are still responsible.” “Data is stale.” “That code doesn’t match.” Avoid claiming an absent backend is connected.

Before changes ship: run the token guard, render the full state matrix, check both themes and sizes, walk handover and setup, dismiss Help with Escape, confirm the TV frame, and inspect the captures. Physical TV distance, assistive technology and real integration need separate production validation.
