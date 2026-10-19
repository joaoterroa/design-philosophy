# Northwind incident overview

An offline redesign of the supplied internal dashboard. Open `app/index.html` directly in a browser; no build, server, dependencies or network connection is required. The original dashboard, brand guide, skill, fixtures and reference pack remain unchanged.

## Scope and priorities

This task is the dashboard named in the opening request. The unrelated menu and banking exercises are not implemented.

Ops engineers need to recognize severity, affected service and missing ownership while standing in the room, then inspect precise incident facts on their laptops. Priorities:

1. Expose open incidents and missing command ownership.
2. Make snapshot freshness explicit, especially when updates fail.
3. Keep all incident facts and operating metrics available.
4. Support a readable wall display and keyboard operation on laptops.
5. Retain Northwind's calm, practical identity.

## Direction and research

The supplied considered-design skill was used. Research was limited to `reference-pack/`; no external services were contacted. `arc-routing.png` shows aligned labels and familiar controls in a bounded sheet: borrowed the alignment and standard dismiss mechanics for incident details, not Arc's styling. `dia-profile-form.png` separates the active object from subdued context and keeps Cancel visible: borrowed that clear foreground relationship for the dialog. These are cropped official screenshots, not evidence of complete task flows or dashboard behavior. `reference-pack/SOURCES.md` retains their first-party attribution. No transition footage was available.

Two compositions were rendered at 1920×1080 before the current implementation (`research/compositions.html`, `research/incident-tv.png`, `research/metrics-tv.png`). The metrics-first alternative enlarged aggregate numbers and placed support information below the list. It pushed actionable incidents downward and made ownership harder to find. The selected composition uses a compact metrics band, a wide severity-ordered table and a stable side column for on-call coverage and service history. This retains familiar scanning behavior; its character comes from Northwind's navy, freight-operations precision and aligned Plex numerals.

The original table began approximately 678px down the TV screen and used 14px row text. The new TV table's first incident begins at approximately 356px (409px in stale). Its titles use 20px text, supporting fields 16–18px. Laptop layouts retain more comfortable scrolling rather than shrinking the data to fit.

## Implemented states and behavior

Direct URLs share the form `app/index.html?screen=live&theme=light&display=tv`.

| Parameter | Values | Behavior |
| --- | --- | --- |
| `screen` | `live`, `stale`, `surge` | First 7 incidents; last-known 7 with a prominent warning; all 12 incidents respectively |
| `theme` | `light`, `dark` | Explicit override; absent or invalid follows system preference and subsequent changes |
| `display` | `tv`, `laptop` | 1920×1080 wall composition or 1440×900 scrolling composition; laptop is the default |

- All fixture statuses in the incident array count as open, including Mitigated and Monitoring. The two resolved incidents appear separately and do not enter the open count.
- Fixture titles, IDs, severity, services, status, opened times, durations, commanders, on-call contacts, service history and metric values are preserved. The original +2 versus yesterday open-count comparison is retained. Surge comparison is derived from the fixture counts. Durations are recorded values, not recalculated timers.
- Missing commander is explicitly “Unassigned” in the incident row, detail sheet and on-call coverage panel. It is never inferred from the primary contact.
- Every title is a keyboard-accessible button opening a native modal with the full facts. Close and Escape dismiss it and return focus. Tab and Shift+Tab stay on its sole control.
- TV surge shows seven incidents on its first page and five on the second, with a visible range, total and Previous/Next controls. The open-count metric remains 12. The table reserves seven rows of space so pagination does not move the resolved history. There is no automatic rotation: critical incidents remain visible until an operator deliberately changes page. A passive TV will therefore show the first seven; the remaining five are explicitly counted and accessible with Next or on a laptop.
- Laptops render every applicable incident in one continuous scrolling page; the final surge incident can be focused and opened by keyboard. No title truncation is used.
- Stale replaces the freshness label with “Data is stale,” adds a persistent last-known warning, labels coverage by its snapshot time, and repeats the caveat in details. It never shows a LIVE badge or a simulated refresh.
- The footer states that this is a local snapshot with no live monitoring connection. No test codes or backend claims appear in the UI.
- Semantic headings, table headers, labeled buttons, a skip link, visible focus, 44px minimum control heights, high-contrast text and reduced-motion support are implemented.

## Visual system and trade-offs

`app/SYSTEM.md` records the system; `app/tokens.css` owns its values. Exact Harbor Navy is used for the header; Fog is the light canvas. Signal Orange is limited to a narrow warning edge. Teal is darkened from brand Tide Teal for readable text and service bars on light surfaces, and lightened in dark mode. Critical red is separate from the brand accent and always accompanied by severity or ownership text. No gradients, emoji or decorative stat icons compete with incidents.

Small 4px control corners and 8px panel corners organize a dense operational tool. A compact horizontal metrics band gives incidents more room without discarding comparisons. Dark mode uses navy surfaces with warm critical and caution tints rather than a literal inversion.

No official logo artwork was supplied. The white compass-style mark in the navy header is an inline prototype interpretation, paired with the specified Plex Sans SemiBold wordmark. Production should replace it with the approved Northwind vector.

## Verification actually performed

Run from the workspace root:

```sh
node outputs/scripts/guard.mjs
/private/tmp/design-compare-venv/bin/python outputs/scripts/verify.py
```

The browser script uses installed Chrome at its macOS path. `DASHBOARD_CHROMIUM` can override the executable path. Headless Chromium required sandbox escalation in this environment. No dependencies were installed.

- All 12 combinations of three states, two themes and two displays were opened from `file://`, measured and captured. Additional captures cover TV surge page two and detail dialogs.
- No horizontal document or table overflow, clipped tested cells, console errors or external page requests. Every TV state fits within 1080px; laptop vertical scrolling is intentional.
- Fixture row contents, open totals and resolved history checked against `EVAL_FIXTURES`; the fixture copy checked byte-for-byte.
- Incident opening by Enter, modal Tab containment, Escape, Close, focus restoration, TV pagination and its stable vertical position, final laptop incident reachability, skip-link navigation, explicit and automatic themes, and reduced motion checked.
- 50 actual text/surface and meaningful-graphic contrast combinations meet 4.5:1 for text and 3:1 for graphics. Token guard checks color literals, typography/radius/shadow/duration use, theme parity and stylesheet wiring.
- Font-loading layout shift is measured with a budget below 0.01. One intermediate run measured 0.0017; the final full run's exact results are in `verification/layout-results.json`. This is a local-load check, not a claim about production loading performance.
- Screenshots were inspected and refined. First pass: TV exceeded its screen. Reduced stacked whitespace and made the metric band horizontal. Second pass: stale warning still pushed the footer below the TV; tightened spacing while preserving all seven rows. Keyboard checks found Tab leaving the one-control modal; added containment. Incident buttons were enlarged to include metadata so their targets reach 44px without bloating rows.

Evidence: `verification/layout-results.json`, `verification/interaction-results.json`, `verification/contrast-results.json` and PNGs in the same folder. `scripts/research.py` can regenerate the original and alternative composition captures.

## Limits and omissions

No real monitoring backend, refreshing, mutation, assignment, search, filtering, authentication or persistence was added; these did not exist in the supplied dashboard. Direct URL states and normal detail/pagination interactions are implemented. Page selection resets on reload. No loading/empty/error state beyond the requested stale snapshot is invented. Mobile, menu and banking flows are outside this task.

Physical TV legibility at the actual viewing distance, color rendering on the room display, screen-reader announcements with a real assistive technology, other browser engines, and 200% zoom have not been verified. The automated checks do not establish a full accessibility audit. Production freshness timing and reconciliation require the real data source. The provisional compass mark needs approved artwork.

## Final critique and proposed lesson

The three weakest points were TV overflow, small incident hit targets and ambiguous stale coverage. All were corrected without removing fixture facts. The main remaining trade-off is manual pagination on the TV during surge; laptops offer the complete list. Review the physical TV's viewing distance before shipping.

Proposed skill note: “For a wall dashboard, assert the document height against the display height for both the normal and failure states. A full-page screenshot can conceal content that falls outside the physical TV.” This is a proposed lesson only; the supplied skill was not modified. No global visual preference is inferred from this single operational task.
