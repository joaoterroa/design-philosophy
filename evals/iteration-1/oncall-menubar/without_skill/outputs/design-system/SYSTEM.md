# Handover design system

The source of truth for how the on-call menu-bar app looks and behaves. Values live in `app/tokens.css`. `checks/tokens.test.mjs` fails when `app.css` uses a colour, type size, radius or shadow that is not a token, when light and dark disagree, or when a text colour drops below 4.5:1.

## 1. What it is for

An SRE glances up at the menu bar between other work. In priority order:

1. **Am I on call, and until when?** Answered by the menu bar without opening anything.
2. **Who do I escalate to right now?** One click: the panel opens on the list.
3. **Hand over a shift** without breaking the rule that someone is always holding the pager.
4. **Staying out of the way.** It is a menu-bar extra, not a destination. Anything bigger goes to PagerDuty.

## 2. Principles

- **Familiar, then elevated.** A macOS menu-bar panel: system font, system material, push buttons, a segmented control, a search field. No new mechanics.
- **One obvious way.** Hand over is a button on the shift it hands over, and nowhere else. Messaging a person is a button on that person's row.
- **Novelty where it pays.** The one unusual element is the shift bar: the shift as a line, with the part being handed over drawn on it (outlined while choosing, striped while waiting, solid with the person's name when accepted). Everything else is plain.
- **Minimal is not hidden.** Times, time zones, who would double up, who is away, gaps in the rota, and how stale the data is all stay visible. The less suitable people are behind one disclosure that says what is behind it.
- **Words over widgets.** "You're on call until Priya accepts" instead of a status badge. "Would be primary and secondary at once" instead of a red icon.
- **Never look more certain than you are.** A request is not a handover. Until the other person accepts, the panel says you are still on call, and the bar shows their part striped with a question mark.
- **Stable layout.** The you panel keeps its place at the top in every state; only its contents change.

## 3. Colour

Neutral greys carry everything. Each meaning has one colour:

| Token | Means | Use for | Never for |
| --- | --- | --- | --- |
| `--accent` / `--accent-text` | act or follow | Default button, the handed-over range, links, the selected person, the "needs you" dot | Decoration, headings |
| `--warn` / `--warn-line` | look twice | Would double up, overnight for them, a gap in the rota, a declined request | Anything merely important |
| `--err` on `--err-bg` | failed or missing | Can't reach PagerDuty | Anything without a sentence saying what failed |
| `--ok` | healthy | The sync dot in the footer | Anything else |

- People are told apart by initials and name on a neutral circle, never by colour.
- The menu-bar glyph is a template image (one colour, adapts to the menu bar). State is carried by shape: outline = off call, filled = on call, struck through = data stale, dot = something needs you.
- In the native build, `--accent` is the user's system accent colour and the surfaces are the system material. The hex values are the prototype's stand-ins; the prototype holds 4.5:1 for white on the accent fill.
- Dark mode is designed, not inverted: every colour token is redefined.

## 4. Type

The system face (SF Pro). Sizes in points:

| Token | Size / line | Use |
| --- | --- | --- |
| `--fs-head` | 15/20, 600 | The you-panel sentence |
| `--fs` / `--fs-strong` | 13/17 | Body, names (600) |
| `--fs-meta` | 12/16 | Rotations, times, reasons |
| `--fs-small` / `--fs-label` | 11/14 | Footer, bar labels; uppercase section labels (600, +0.02em) |

Tabular numbers everywhere, because times line up and tick.

## 5. Space and shape

- Panel 360 pt wide, at most 680 pt tall; gutter 14 pt; rows at least 34 pt.
- Radii nest: panel 14, you panel 10, rows 7, buttons and fields 5, bar 3.
- No cards. One filled block per screen: the you panel. Hairlines separate the footer.
- Elevation only for the panel itself, push buttons and the segmented thumb.

## 6. Layout

**Now** (default): you panel (your state and its one action), On call now (one row per rotation, escalation order, local time when it differs), Your next shifts (two), footer (sync state, global shortcut).
**Schedule**: rotation picker, the next seven days by day, gaps named in place, a link out to PagerDuty for anything more.
**Hand over** (replaces the panel content, back chevron, Esc returns): the shift and its bar, which part, who (free people on the rotation first, longest since their last shift first; then a disclosure for people who would double up, be up overnight or are away), handover note (open incidents pre-ticked), a fixed footer that says what will happen and the button that does it ("Ask Priya · 13 h").

## 7. Handover rules

- A handover is a request. The asker stays on call until the other person accepts; declining changes nothing.
- Accepting creates the override in PagerDuty. The app never writes an override nobody agreed to.
- Away people are shown, greyed, with the reason; they cannot be picked.
- Open incidents assigned to you are offered in the note, ticked by default.
- While PagerDuty can't be reached, handovers are paused and the button says why.

## 8. Motion

`--t-fast` 150 ms for hover and press, `--t-mid` 220 ms for the sheet sliding in and the range moving, `--t-slow` 600 ms for the range settling when accepted (the one moment that earns it). The pending dot pulses only while waiting. `prefers-reduced-motion` removes all of it.

## 9. Writing

Plain, specific, calm, in the user's terms: "You're on call until Priya accepts." "Can't reach PagerDuty since 18:31. This is the schedule as of then, and handovers are paused until it's back." No exclamation marks, no "Oops", no jargon the rota tool uses but people don't ("override" appears only once, as confirmation of what happened in PagerDuty).

## 10. Keyboard and access

- Global shortcut ⌃⌥O opens the panel (shown in the footer). Esc goes back, then closes.
- Every control is a real button or input with a visible focus ring. Row actions appear on hover and on keyboard focus.
- The menu-bar item has a spoken label ("Handover: On call, 14 hours 13 minutes left, needs you").
