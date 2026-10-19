# Northwind: an operations ledger

Read this before changing the interface. Values live in app/tokens.css. Run `node outputs/verification/tokens.cjs` and the Playwright verification script after changes.

## Purpose and priorities
Operations staff need to identify impact from across a room, then find responsibility and timing on a laptop.
1. Surface the most severe incident and missing commander.
2. Preserve every incident, status, service and original metric.
3. Distinguish current snapshots from unavailable updates.
4. Use the same recognizable hierarchy on TV and laptop.
5. Support keyboard and both themes without relying on color.

## Direction
A calm operations ledger, derived from Northwind's freight business: straight rules, aligned columns, restrained Harbor Navy. The distinctive moment is the attention rail: a small Signal Orange rule alongside the unresolved SEV1 incident and the commander gap. No gradients, decorative emoji, or card grid. Ordinary controls everywhere else.

## Color and type
IBM Plex Sans carries all language; Mono aligns IDs, dates and metrics. Harbor Navy is the exact primary fill and brand color. Fog is the light canvas; Slate is body copy. Tide Teal carries service-volume bars; darker teal text passes contrast. Signal Orange is used only as an attention edge, never body copy or a large fill. Neutral secondary text is tuned separately for dark mode. Warning and error states use explicit sentences and separate accessible text colors. The unavailable commander is written out.

Type tokens: 12, 13, 14, 15, 16, 18, 20, 22, 24, 28, 32, 40, 48, 64px. TV scales row text to 20px and metrics to 64px. Banking uses 18px labels and minimum 48px controls. Space uses a 4px base with 6px and 10px optical subdivisions. Corners are 4px for tools, 12px for the floating menu, 8px for banking controls. Shadows only on the popover and dialog.

## Layout and behavior
Dashboard header, metrics, then incident ledger with an on-call/service sidebar. Laptop pages scroll vertically; all open records remain in the document. TV shows seven incidents per page with an explicit count and manual paging during surge; it never silently rotates. Resolved history stays separate and never counts as open. The local snapshot label avoids suggesting a real connection.

Menu is a 360px popover at 20px, with 640px maximum height. Handover shows responsibility as a two-person transfer; pending never transfers ownership. Banking is a narrow, single-column setup with one labeled code field and an always-reachable safety warning. Each additional product uses its own quiet contextual treatment rather than imitating a dashboard.

## Motion, writing and accessibility
No timed transitions or rotating data. Reduced motion preserves the full presentation. Voice is direct, calm and specific. Native buttons, forms and dialogs; focus rings on all interactive elements; focus moves to the new heading after a step; dialog traps focus, supports Escape and returns focus to its opener. No keyboard shortcuts beyond native behavior. No color-only information.

## Guardrails
All component colors, font sizes, radii and shadows must reference tokens. Verify theme parity and contrast for actual text/background pairs. Never hide fixture details through truncation. Verify the 320px banking floor, 400px menu scene, 1440px laptop and 1920px TV. Physical TV legibility and assistive-technology announcements still need real-device review.
