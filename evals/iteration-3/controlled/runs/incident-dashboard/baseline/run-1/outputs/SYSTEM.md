# Northwind incident operations: the incident comes first

Read this before changing the dashboard. Visual values live in `app/tokens.css`; `verification/design-guard.mjs` checks color and type token use, theme parity, contrast and fixture identity.

## Purpose and priorities

Operators read this during an incident, from a laptop or across an operations room. In order:

1. Find the highest severity incident and whether someone owns it.
2. Know whether the displayed information can be trusted as current.
3. Scan every open incident, including mitigated and monitoring work.
4. See response metrics, on-call cover and service concentration.
5. Reach resolved history without mixing it into the open count.

## Principles in this product

- Familiar table, native search and select, native modal details. No custom interaction vocabulary.
- One quiet operational emphasis: the SEV1 row has a severity spine, a tinted ground and explicit missing ownership. This is the distinctive moment because it identifies the work that most needs attention.
- Color carries meaning. Harbor Navy is identity; red is critical severity or missing critical ownership; amber is caution; teal is service volume and freshness. Every state also has text.
- Keep incident titles, service, ID, severity, status, commander, duration and opened time visible. Details repeat the facts rather than conceal required fields.
- Do not call monitoring or mitigated work resolved. Do not substitute the on-call primary for a missing commander.
- Fixed snapshots have fixed dates and durations. A stale snapshot never gets a live freshness label or an invented successful retry.

## Identity and tokens

Brand source: unchanged `brand/guide.md`. The header uses exact Harbor Navy `#12355B` with white lettering. The compass N is a simple local SVG interpretation, not an official supplied logo asset. No logo artwork was supplied. IBM Plex Sans provides the brand's calm, readable type; IBM Plex Mono distinguishes IDs and durations and aligns metric figures. Both ship as local WOFF2.

Color roles in `tokens.css`:

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| Page | Fog `#EEF1F4` | `#0D1B28` | Separate the reading field from the incident register |
| Surface | White | `#132534` | A single table surface, no tile wall |
| Text | `#172D40` | `#E7EDF2` | High contrast, tied to Harbor Navy |
| Secondary | `#536574` | `#A9BAC8` | Legible metadata rather than faint gray |
| Critical | `#A52E32` | `#FFADB1` | SEV1 and missing commander |
| Caution | `#8F4C0B` | `#F4C587` | SEV2 and stale information |
| Service bars | `#257E74` | `#53B9AA` | Tide Teal adjusted for meaningful graphic contrast |
| Focus | `#155CA2` | `#8DC9FF` | Visible focus on the reading field; white on the navy header |

Exact Signal Orange and Tide Teal remain available as brand tokens; orange is intentionally not used for large surfaces or body text. Service bars use a contrast-adjusted teal. No arbitrary multicolor service palette.

Type scale (laptop / TV): metadata 12 / 15, small 14 / 17, body 16 / 20, incident title 17 / 22, section heading 20 / 24, page title 32 / 40, metrics 48 / 60 px. Sans weights 400, 500, 600; Mono 400. Metadata is subordinate but readable; severity and commander labels use words, not just color.

Spacing follows 4, 8, 12, 16, 20, 24, 32, 40, 48 px. Page gutter is 32 px on laptop and 48 px on TV. Radius is 4 px on controls/table, 8 px on the modal. Hairlines divide related facts; no decorative shadows or gradients. Data-derived bar widths are percentages, not design-token exceptions.

## Layout and interactions

Navy identity bar, page title and freshness, four metrics, then a broad incident register with a narrower context column. TV uses 22 px incident titles and seven-row pages. Laptop uses continuous document scrolling with all current incidents rendered. There is no nested vertical scroll container and no automatic page rotation that would remove the SEV1 incident while someone reads it.

Search matches title, incident ID, service and commander; severity filter combines with search. Filtering retains focus in the control. Empty matches are explained. Clicking an incident title opens a native dialog; Escape and Close dismiss it, returning focus to the opener. TV paging retains focus on the available page control. Theme and display controls are normal product preferences, reflected in the URL. System theme is followed until the URL explicitly selects a theme.

Controls have 44 px minimum targets. Incident title hit regions cover their table cell; resolved hit regions cover their item. Table headings have scope; sections and dialogs have names. A skip link goes to the incident region; focus rings remain visible. There is no motion or periodic blinking; reduced motion preserves every piece of information.

## Writing and guardrails

Voice: direct, calm, competent. Examples: “SEV1 incident commander is unassigned.” “No incidents match your filters.” “Updates paused.” No success claims about a backend.

Before shipping changes: run the design guard and browser checks, inspect light and dark at both target sizes, verify stale freshness, preserve fixture identity, and confirm the last incident and resolved history are reachable. Physical TV distance and assistive technology require human verification.
