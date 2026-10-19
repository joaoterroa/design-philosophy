# Rota design system — clear responsibility

Read this before changing the prototype. `app/tokens.css` is the value source; `verification/tokens_guard.js` guards token use, theme parity, contrast, stylesheet order and an exact fixture copy.

## Purpose and priorities

A small macOS menu-bar companion for a team of about 40 SREs. It is opened briefly, often while another task has the user's attention. Priorities, in order:

1. Know who owns the current shift and when it ends.
2. Hand over deliberately; sending is never acceptance.
3. Keep the other current assignments visible without implying a full staff directory.
4. Be clear about stale or missing information.
5. Fit the menu-bar context and work with keyboard and assistive technology.

## Composition and character

One inset shift object, followed by a plain roster. Personal responsibility leads; people and roles remain together. This is a quiet operational utility, with system typography and compact rows rather than dashboard tiles. The handover is the distinctive moment: a two-person object keeps the current and requested owner visibly separate. Do not replace it with an ambiguous success toast.

The proposed pine palette suits a calm duty tool; it is not an existing brand claim. Green identifies the shift and its primary action. It never means a request has been accepted without explicit words. Amber marks uncertainty or continuing responsibility. There is no red alarm state in these fixtures.

## Tokens and roles

| Role | Light | Dark | Reason |
| --- | --- | --- | --- |
| Background | `#fafbf9` | `#262d29` | Near-neutral, opaque popover; readable without wallpaper dependence |
| Main text | `#242d29` | `#edf1eb` | Native-like clarity on every content surface |
| Secondary text | `#59675e` | `#b3beb5` | Roles, timestamps, metadata; still above 4.5:1 |
| Shift surface | `#e8f0e9` | `#303f34` | Groups the assignment and action without boxing the roster |
| Action / assignment | `#285b46` | `#b6d7be` | Pine by day, light sage in dark mode; dark mode has its own luminance hierarchy |
| Caution text / ground | `#77521a` / `#f6eedf` | `#ebc78c` / `#403829` | Words about pending responsibility and stale data |
| Focus | `#286ba6` | `#8ec5f5` | Distinguishable keyboard focus, separate from shift status |
| Control boundary | `#819083` | `#829886` | At least 3:1 against adjacent button/input surfaces |

All remaining values are named in the token file. Pale separators communicate grouping, not control affordances. Decorative avatars are initials with accessible names provided in adjacent text. Never encode an engineer's role solely by colour.

## Typography, spacing and shape

Use `-apple-system`, then platform sans-serif fallbacks. Native macOS text is the starting point, not the supplied Plex fonts. Scale: 11px timestamps and initials, 12px metadata, 13px body and controls, 14px app name, 16px small glyph, 19px shift time, 23px screen title. Weight 400 for reading, 500 for names, 600–650 for hierarchy. Times use tabular figures. Body line height is 1.45; titles 1.2.

The 4px rhythm has 8/12/16/20/24/28/32px steps. Popover inset is 20px; shift inset 16px. Corners: 14px popover, 10px grouped objects, 6px controls, circles only for initials. One shadow grounds the popover. No gradients, transparency or looping effects. These ordinary corner radii do not claim to be continuous squircles.

## Layout and components

Contract: 400×680 scene, #app at x20/y20, width 360px, maximum height 640px. Both `display=laptop` and `display=tv` retain this fixed menu-bar composition; TV is not interpreted as a different wall dashboard. These constraints come from the supplied brief, not inferred macOS API limits.

Header: app identity and fixture date. Footer: explicit UTC plus the fixture snapshot time. The personal shift includes a static elapsed rail: 06:00–18:00, one-third complete at fixture time 10:00. Its fraction is calculated from EVAL_FIXTURES and set as a runtime data variable; it is not a live timer. The offline variant removes the rail and reduces the summary so the uncertainty notice and all current names fit.

The native select has only the known handover contact. Do not populate it with the supplied on-call roster: on-call status is not evidence that someone can accept this shift. Review is a separate composition within `compose`, before sending. Pending has a cancellation action and one return route; accepted states transfer ownership explicitly. Empty keeps its explanation and a repeatable check.

Controls have a minimum 36px height, with ample width. This is a mouse/keyboard macOS surface; no claim of touch-first ergonomics. Browser zoom remains available. The root can scroll if larger system text requires it, though no assigned default-size state scrolls.

## Motion and writing

Only background feedback uses 120ms ease-out. There are no entrance animations or state delays. Reduced motion removes transitions, preserving all content.

Voice: precise, calm, accountable. Examples: “Showing the last-known schedule … Assignments may have changed.” / “No schedule yet.” / “Priya has the shift.” Responsibility is stated in words even when the surface also uses colour.

## Keyboard and semantics

Real buttons and a labeled native select. Tab and Shift+Tab follow document order; Enter/Space activate buttons; the select retains native keyboard operation. On a view change, focus moves to its h1, so the next Tab reaches the next relevant control. The current recipient stays selected when returning from review. Escape steps back from review, or cancels the chooser. No invented global shortcut or simulated macOS window buttons.

Milestones use a polite live region. Repeated offline checks announce continuing failure. Empty checks use a status region. Decorative marks, avatars and timeline are hidden from assistive technology; equivalent names and time text remain visible.

## Guardrails before changing

- Run `node outputs/verification/tokens_guard.js` from the workspace root.
- Run `outputs/verification/check_ui.py` with the supplied Python/Playwright environment.
- Inspect both themes at 400×680, including review and the responsibility transition.
- Preserve the exact supplied fixtures; no backend, availability or acceptance claims without evidence.
- Check keyboard focus, no overflow, contrast and honest retry behavior.
