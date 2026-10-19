# Rota design system — clear custody

Rota is a small macOS menu-bar companion for about 40 SREs, opened briefly while working elsewhere. Read this before changing the UI. `app/tokens.css` contains visual values; `node outputs/verification/design-guard.cjs` checks their use, theme parity, fixture integrity and contrast.

## Priorities

1. Identify who owns the current shift, its rotation, and when it ends.
2. Make a handover intentional: choose, review, request, await acceptance.
3. Preserve trust: pending does not change ownership; stale data is explicitly stale.
4. Keep the current roster visible without mistaking four on-call people for all 40 staff.
5. Fit a familiar, keyboard-operable menu-bar surface.

## Identity and composition

This is a proposal; no brand guide was supplied. Cool neutral surfaces and a restrained macOS-like blue distinguish interaction from amber responsibility warnings and green acceptance. System type belongs in a utility opened alongside native apps. There is no downloaded font or imagery. The mark’s two returning arrows describe a rotation, and remain clear at 22px; it is an inline vector, not a brand copied from the references.

The own-shift block precedes the roster because an incorrect assumption about responsibility is more costly than an extra glance at colleagues. The distinctive object is the handover itself: named sender and recipient, then explicit custody language. Rounded 14px shell, 9px grouped objects and 6px controls distinguish host, content and action; the remaining roster uses simple rows and hairlines. There is no decorative motion or ornamental background.

## Tokens and roles

Colors are paired explicitly for light and dark in `app/tokens.css`.

| Role | Light | Dark | Use |
| --- | --- | --- | --- |
| Primary text | #24272d | #f0f1f4 | Names, headings, controls |
| Secondary text | #616672 | #b3b8c3 | Time, role, context; never invisible metadata |
| Action | #2459bd | #a6c4ff | One primary action, focus, rotation mark |
| Current-shift surface | #edf2fc | #2d3850 | Current ownership group |
| Caution text / ground | #805100 / #fff3d9 | #f2cd83 / #3d3423 | Responsibility until acceptance |
| Acceptance text / ground | #236440 / #e9f4ed | #9bdbb1 / #293e32 | Completed handover check |

The accent is proposed from the platform, not an asserted company brand. Color is reinforced by words. Hairlines group content; interactive borders use a stronger token. Disabled controls are exempt from contrast; their labels remain readable in context and the native required field conveys how to enable the action.

## Type, shape and rhythm

System font at 13px body / 1.45 line height; 23px headings / 1.2, 14px product name, 12px metadata and 11px footer or timeline. Only the small footer and redundant timeline labels use 11px. Names use medium weight; headings semibold. Numeric time uses tabular figures. A 4px base rhythm extends through 8, 12, 16, 20, 24 and 32px gaps. The shell uses a 20px content inset. Actions are at least 36px high: appropriate for a pointer-driven desktop tool, without squeezing text or making false touch-device claims.

## Layout and behavior

The body places a 360px popover at x20/y20. The shell never exceeds 640px. The scene is 400×680. `display=tv` retains these dimensions because the explicit scene contract takes precedence over inventing a wallboard; this is not validated for viewing at distance.

Main: title/date → own shift with elapsed-time rail → handover action → other current on-call engineers → footer. The timeline uses the fixture clock and UTC, not the viewer’s timezone or real machine time. Offline uses a simpler saved schedule instead of a live-looking progress graphic.

Compose uses a real select, optional note and review step. Review exposes recipient, rotation, cover period and retained responsibility before Send. Pending and accepted use stable named objects and explicit text. No automatic acceptance, pulsing activity or false sync indicator. The footer identifies the local preview. Retry and refresh never manufacture successful connectivity or a schedule.

## Writing and accessibility

Plain, calm and exact. “You’re still responsible.” “Current coverage may have changed.” “Priya accepted your request.” No jargon badges or unexplained status dots.

Controls use native semantics and visible 3px focus with 2px separation. Each view change focuses its heading; edit returns to the select; refresh/retry retains focus on the initiating button. Optional notes are safely escaped. Escape goes back from subviews and leaves Offline intact. No global macOS shortcut is claimed. Only milestones use a polite live region. A 140ms hover transition provides feedback; reduced motion removes it without removing information.

## Before changing the interface

Run the guard and browser verification. Inspect both themes at the actual scene size. Preserve pending custody, literal UTC times, current-roster scope and the explicit acceptance boundary. Keep prototype simulation controls in the separate harness. Record actual evidence and unverified native integration in DESIGN.md.
