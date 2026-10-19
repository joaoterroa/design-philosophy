# Rota design system

Read this before changing the UI. `app/tokens.css` owns visual values; run `node outputs/verification/design-guard.cjs` from the workspace root after changes.

## Purpose and priorities

A small macOS menu-bar utility for approximately 40 SREs, opened briefly while doing other work. Priorities, in order:

1. Identify the responsible engineer and the shift’s end immediately.
2. Make a handover deliberate: choose, review, request; ownership changes only on acceptance.
3. Make saved or absent data visibly different from current data.
4. Keep the supplied current roster legible within a 360px popover.
5. Support keyboard use and both appearance preferences.

## Direction: a clear chain of responsibility

The primary shift is the single grouped surface. Supporting people are compact rows divided by hairlines. The distinctive moment is the Jamie → Priya ownership diagram: the names stay in place, and “Responsible now” changes sides only after acceptance. The meaning also appears in plain text; colour never carries it alone. No animation is necessary to understand the transition.

The neutral palette is proposed, not company branding. A cool gray frame resembles a small desktop utility; green means an available action or the explicitly responsible person. Amber means uncertainty or a responsibility warning. Neither is used to categorise teams or people. The mark is two linked strokes, suggesting continuity between shifts; it is not an invented corporate logo.

## Tokens and rationale

- System typography (`-apple-system`, then local sans-serif fallbacks) fits macOS and requires no font download. Bundled Plex fonts were deliberately not used: this is a transient utility rather than a brand destination.
- Type sizes: 11px for compact dates and secondary roster roles, 12px for supporting details, 13px body/control text, 14px section names, 17px secondary emphasis, 23px page headings, 27px shift end. Tabular numerals keep times aligned.
- Base spacing is 4px, with a 20px horizontal content gutter. The main schedule fits at its real size without scrolling. The 360px document root begins at 20px/20px within the required 400×680 scene and is capped at 640px.
- Radii: 14px outer floating popover, 10px grouped shift, 6px controls; circles only for initials and small state marks. The outer popover alone casts a shadow.
- Light surfaces: background `#f8f9f9`, grouped surface `#ffffff`, soft `#eef1f1`; main text `#20292c`, supporting text `#57656a`. Action/responsibility `#166656`, on-action `#ffffff`; caution `#815414` on `#faf0de`.
- Dark surfaces: background `#252b2d`, grouped surface `#2c3335`, soft `#333c3f`; main text `#edf1f1`, supporting text `#b2bfc3`. Action/responsibility `#9cddc3`, on-action `#123c30`; caution `#f0cc8d` on `#41392b`.
- Focus uses blue, independently of ownership and caution: `#176bb0` light / `#8ac4ff` dark. Its two-pixel outline is offset three pixels.
- Border colours are quiet separators, not the sole indication of an interactive control. Primary buttons have a contrasting fill; text labels and native radio controls identify secondary affordances.
- 120ms colour transitions provide hover feedback. Reduced motion removes transitions without removing information. There are no loops, simulated progress, or timed acceptance.
- Structural percentages and SVG viewBox geometry are intrinsic layout/asset geometry. The sole dynamic visual token, `--shift-progress`, is calculated from fixture times, not the machine clock.

## Components and writing

Use one primary action per stage. The recipient is an explicit radio choice; review starts disabled. The entire recipient row is a click target. Buttons are at least 36px high, and the recipient row exceeds 48px. Optional notes are plain text, limited to 300 characters, retained through edit/review and escaped before rendering.

Use specific, calm sentences. “You’re still on call” is more useful than a warning icon. Offline copy names when the snapshot was saved, calls the roster saved, and never offers a usable handover action. Empty copy does not equate missing schedule data with being off call.

Tab follows document order. Space chooses the recipient; Enter activates buttons. Focus moves to the new screen heading after navigation, and back to the recipient after editing. Escape returns from compose/review, pending, and accepted; it never cancels a sent request. Cancelling a sent request has its own explicit button. Status announcements report sending, cancellation, acceptance and failed retry. There is no global hotkey, because no native host exists here.

## Guardrails

`verification/design-guard.cjs` checks token wiring, undefined tokens, component colour/type/radius/shadow literals, exact explicit/system dark theme parity, and 30 contrast pairings. It checks body/supporting text on their used surfaces at 4.5:1, action text on its fill at 4.5:1, caution text on its tint at 4.5:1, and focus/progress graphics at 3:1. Disabled controls are intentionally subdued and excluded from active-control contrast requirements.

Before changing the UI: rerun the guard and browser suite, inspect both themes, walk the keyboard path, ensure uncertainty is visible, and keep ownership with Jamie until an acceptance event.
