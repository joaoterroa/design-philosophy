# Rota design system: "Still yours until it isn't"

This is the source of truth for how Rota looks and behaves. Read it before changing the UI. Values live in `app/tokens.css`. `tests/design.test.js` (`node --test tests/*.test.js`) fails when `app.css` uses a literal colour, size, weight, radius or duration, when the light and dark token sets disagree, or when a text pair drops below contrast.

The prototype is HTML; the shipping app would be SwiftUI/AppKit. Map each token to its native counterpart (column "Native" below). Where a native semantic colour exists, the native app uses it and these values are only its stand-in.

## 1. What it is for

Rota is a macOS menu-bar app for a team of about 40 SREs. It is opened for a few seconds at a time, usually while doing something else (in a terminal, in a meeting, on a Saturday). In priority order:

1. **Am I on call, and until when.** Answered by the menu bar itself, without a click.
2. **Who is on call right now, per rotation, and how to reach them.** One click.
3. **Hand over all or part of my shift, safely.** Never leave a gap; never imply someone has it before they accept.
4. **What needs me.** A request from a teammate, or a hole in coverage, appears first and in a sentence.
5. **Trust.** Where the data came from, how fresh it is, and in whose time zone a time is.

## 2. Principles

**The menu bar is the answer.** The status item shows a dial and, while you're on call, the time left (`1d 19h`). Most glances end there. Nothing else in the bar: no colour, no counts beyond a single dot for "a request is waiting".

**Native first.** System font, macOS push buttons, radio groups, popup buttons, a search field and menu rows. The popover is a standard menu-bar-extra window. Craft goes into wording, alignment and the strip, not into new controls.

**Still yours until it isn't.** A handover is a request, not a fact. Until the other person accepts, every surface (strip, sentence, menu-bar title) still says you're on call. The orange "waiting" state and the sentence "You're still on call until Priya accepts" exist to stop someone switching off early.

**Novelty where it pays: the shift strip.** The one distinctive element is the strip that shows who holds each hour of your shift. In the handover sheet it previews the result: the chosen hours change from your dark fill to the recipient's quiet fill and their initials slide in (220ms). It is the only animation in the product besides the popover appearing, and it explains the outcome before you commit.

**Words over badges.** Availability is a sentence ("Out of office until Wed 22 Oct, per Google Calendar"), not an icon. People are not colour-coded. Only three colours carry meaning (section 3).

**What needs you goes first.** Requests and coverage gaps sit at the top of the popover, each with one action. Healthy state is silent.

## 3. Colour

Neutrals carry the interface; the window ground follows the system popover material. Colour is kept for meaning, and each meaning has one colour:

| Token | Light / dark | Native | Means | Use for | Never for |
| --- | --- | --- | --- | --- | --- |
| `--fill-you` / `--on-you` | `#3a3a3f` / `#e6e6eb` | labelColor at strip opacity | Your time | Your segments on the strip; your avatar | Anything that isn't you |
| `--fill-quiet` | `#e0e0e5` / `#45454b` | quaternarySystemFill | Someone else's time | Others' segments, avatars | Disabled controls |
| `--accent` / `--accent-line` / `--accent-text` / `--accent-soft` | `#0068d6` / `#0a6bd4` (fill) | controlAccentColor | Act and selection | The committing button, the selected person, the previewed range, links, focus | Status of any kind |
| `--pending` / `--pending-soft` | `#a85300` / `#ffad5c` | systemOrange (darkened for text) | Waiting for a reply: still yours | Pending segment (hatched), the "Waiting for…" note, caution text on a person | Errors; decoration |
| `--danger` / `--danger-soft` | `#c0001a` / `#ff7b80` | systemRed (darkened for text) | Nobody covering, or something failed | Coverage gap, send failure, invalid range | Declines (a decline is a normal answer, in plain text) |

Rules:
- No brand guide was supplied, so the palette is derived from the platform: the system accent for acting, the system orange/red families for waiting and failure. **This is a proposal**; if the team has brand colours, they would go on the mark and app icon, not on these roles.
- The real app uses the user's System Settings accent colour. The prototype shows a slightly deepened default blue so white button text holds 4.5:1 (`#007AFF` is 4.0:1). The accent fill against the window is not checked at 3:1 in dark mode: like the native push button, the button is identified by its label.
- System orange and red fail as text on light grounds; text uses darker members of the same hue family (`#a85300`, `#c0001a`). Dark mode uses lighter ones.
- Errors are words plus a tinted surface, never colour alone. Green is not used: healthy is silent.
- Text tokens hold 4.5:1 on every surface they sit on, in both themes; the strip fills and accent outline hold 3:1. The guard test lists every pair.

## 4. Type

System font (SF Pro on macOS; Inter stands in on Linux renders), because a menu-bar utility should feel like part of the OS. One scale:

| Token | Size / line, weight | Use |
| --- | --- | --- |
| `--fs-emph` | 15/20, 600 | The one answer: "1 day 19 hours left", "You're not on call" |
| `--fs-body` | 13/16, 400 or 600 | Names, sentences, controls (macOS body) |
| `--fs-caption` | 11/14, 400 or 600 | Rotation names, times, handles, reasons, section labels |
| `--fs-mini` | 10/14 | Strip day labels and avatar initials only |

Weight before size. Times use tabular numerals. Section labels are 11pt semibold secondary, not uppercase.

## 5. Space and shape

- 12pt gutter inside the popover; spacing steps 4 / 8 / 12 / 16.
- Radii: window 12, controls and rows 6, strip segments 3, avatars round. Nested shapes take smaller radii than their containers.
- Hairlines separate groups. One tinted surface at most per state, and only for a fact that needs you (pending note, gap, failure).
- Only the popover (and its overflow menu) is elevated.

## 6. Layout

Popover width 340pt (fixed); height fits content, capped at 640pt with the handover body scrolling between a fixed header and footer. Status item: 16pt dial within the 22pt menu-bar working area of a 24pt bar (source: Bjango, "Designing macOS menu bar extras"; Apple's HIG page did not load here).

Main view, top to bottom: anything that needs you → your shift (eyebrow, answer, until/then, strip, any handover note, Hand over…) → On call now (one row per rotation layer) → footer (sync source and age, ⋯ menu).

Handover view: back + title + shift → large strip preview → Which part (rest / part, with From/Until) → Who covers (search + rotation members, free first, blocked last) → Note + link open incidents → fixed footer with the outcome in one sentence and Cancel / Ask {name}.

## 7. Components

- **Status item.** Template-style dial; filled wedge = share of your shift still to run. Title `1d 19h` / `4h 12m` while on call, none otherwise. Dot cut into the ring when a request is waiting. Dial at 50% when offline. Accessible label says all of this in words.
- **Shift strip.** Now → Tue 00:00. Segments: you (dark), other (quiet), pending (orange outline + hatch, label `PR?`), preview (quiet + accent outline). Labels: "You", first name when ≥64pt wide, initials when ≥26pt, nothing below that; full text in `title` and in the strip's `aria-label`.
- **Person row (handover).** Avatar, name, one wrapping line: availability sentence, then the range in their own time when their zone differs. Blocked people are listed but disabled with the reason; people with a caution can still be chosen, and the caution is repeated in the summary.
- **On-call row.** Avatar, name, "Rotation Layer · @handle", "until …" right-aligned. The row opens a Slack DM.
- **Needs-you block.** Title sentence, one-line reason, one action. Tinted only for danger.

## 8. Motion

Ease-out (`--ease`), 120ms for hover/press, 220ms for the popover appearing and a segment changing hands. Nothing loops except the first-sync spinner, which stops when data arrives. `prefers-reduced-motion` sets both durations to 0 and slows the spinner; the strip still shows the result.

## 9. Writing

Plain, exact, calm. Times are absolute ("Sun 10:00–18:00"), with the zone named only when it differs from yours. Ranges never break across lines.
- Error: "Couldn't send the request. PagerDuty didn't answer within 10 seconds. Nothing changed: you're still on call. Your note is kept."
- Empty / first run: "Rota reads your team's schedules from PagerDuty. It only changes them when you hand over or cover a shift."
- Success: "Priya Raman covers Sun 10:00–18:00. It's in PagerDuty as an override."
- No exclamation marks, no "Oops", no emoji.

## 10. Brand

Name: **Rota** (the British word for the thing it shows). Mark: a dial whose filled wedge is the part of your shift still to run; it is the status-item icon, drawn on a 16pt grid with a 1.5pt ring so it survives at 1x. The empty version (ring + tick at 12 o'clock) is used when you're not on call.

## 11. Keyboard and accessibility

- No global shortcut by default (the menu-bar space is crowded and ⌥⌘ combos collide with many SRE tools); users can set one in Settings, and any text showing it must read the live binding.
- In the popover: Tab order follows reading order; Esc backs out of the handover sheet, then closes the popover and returns focus to the status item; ⌘↩ sends; arrow keys move within radio groups; the ⋯ menu has ⌘, and ⌘Q.
- Focus is restored to the same control after every re-render, and moved deliberately after navigation (to the first choice when the sheet opens, to "Hand over…" after cancelling).
- Status changes use `role="status"`; failures use `role="alert"`.

## 12. Before you ship a UI change

- [ ] Tokens only; `node --test tests/*.test.js` passes.
- [ ] Looked at in both themes, at 340pt, in all 12 states (`tools/shoot.py`), with long names and far-away time zones.
- [ ] `tools/interact.py` passes: keyboard path, focus, no shift above the reading point.
- [ ] No new colour meaning, card, or badge where a sentence would do.
- [ ] Nothing reads as covered before it is accepted.
- [ ] Copy says what failed, what it means for coverage, and what to do.
