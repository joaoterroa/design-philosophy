# Rota design system — responsibility first

Read this before changing the UI. Values live in `app/tokens.css`; run `node verification/tokens.test.cjs` from this directory to check usage, theme parity and contrast.

## Purpose and priorities

A small macOS menu-bar utility for about 40 SREs, opened briefly while working elsewhere. The four fixture roster members are the current duty roster, not a directory of all staff.

1. Identify the responsible person and shift end at a glance.
2. Transfer responsibility safely: a request does not end Jamie’s duty.
3. Keep schedule context and last-known timestamps visible.
4. Make the complete task work with ordinary controls and a keyboard.

## Principles and identity

Native mechanics take precedence over a custom visual language: system typography, a real select, text area, ordinary buttons and back navigation. A cool graphite neutral ground suits a utility that sits beside incident tools. Blue denotes the active part of the workflow: primary actions and the current responsible owner. Amber means caution, including pending responsibility and offline uncertainty. Names and words carry meaning independently of color.

The one distinctive moment is the responsibility connection. A filled node names the current owner; the outlined node names the intended recipient. On acceptance the fill moves to Priya. This is a static, readable explanation of an asynchronous handover, not a decorative progress animation.

The proposed palette is platform-led; no company brand guide was supplied. The two opposing arrows in the Rota mark describe a shift exchange and remain legible at menu utility sizes. No background illustration, decorative gradient or category-colored avatar is needed.

## Tokens

| Role | Light | Dark | Purpose |
| --- | --- | --- | --- |
| Background | `#fafafa` | `#292a2e` | Popover body |
| Surface | `#f0f1f3` | `#333439` | Current shift, or an optional note |
| Text | `#202124` | `#f2f2f4` | Names, headings, controls |
| Secondary text | `#60636b` | `#b3b5bd` | Roles, date, time context |
| Active | `#135fc5` | `#8dbaff` | Actions, responsible node, focus |
| Caution | `#845100` | `#f1c681` | Pending responsibility and stale status |
| Control boundary | `#858994` | `#818590` | Locate fields and secondary buttons |

All text pairs used by the app are checked at 4.5:1 or better. Control boundaries are checked at 3:1. Separators are deliberately quiet and do not carry information on their own. Dark mode uses a lighter blue with dark button text rather than inverting the light palette.

System font: `-apple-system`, BlinkMacSystemFont, Helvetica Neue, Arial, sans-serif. The macOS choice is deliberate; the provided Plex fonts are not used. Scale: 11px footnotes, 12px metadata, 13px body, 14px controls, 22px task heading, 25px current owner. Line-height 1.45; compact headings 1.2. Weight 600 carries most hierarchy; dates and shift times use tabular numerals where aligned.

Spacing follows 4/8/12/16/20/24/28/32/40px. Gutter 20px. Shape: 6px small notes, 8px controls, 10px current-shift surface, 14px floating shell. Only the popover has a shadow, because it floats above the scene. Initials are uncolored identification aids, not status badges.

## Layout and components

The task contract fixes a 360px popover at x20/y20 in a 400×680 scene, maximum height 640px. Both display parameters retain this compact menu-bar layout; a television dashboard is outside this product. Header identifies the utility and fixture date. Current owner comes first, then the single handover action, then the other three currently on-call people. Footer names the snapshot time and current roster count.

Compose keeps the rotation and shift visible. Only Priya is offered: the fixture establishes her as the handover contact; it does not establish eligibility for the other 39 staff. A review step shows both people and the responsibility rule before sending. Pending has a view/return route and cancellation. Accepted returns to a schedule with Priya as the primary owner. Offline deliberately shows only the last-known primary shift, rather than presenting the rest of the roster as current.

## Motion and writing

120ms ease-out hover changes only. No loop, simulated latency or automatic acceptance. Reduced motion removes transitions without removing any status.

Voice: calm, exact, brief. Pending: “You’re still on call.” Offline: “We can’t confirm who’s on call now.” Empty: “No schedule available.” Accepted: “Priya has taken over your shift.” All timestamps come from the fixture and are explicitly UTC.

## Accessibility and keyboard

Native buttons, select, labeled text area, form validation and disabled review before selection. Interactive targets are at least 36px high; primary actions 38px, select at least 40px. A 3px outline with 3px offset identifies keyboard focus. Rendering moves focus to the new task heading; editing returns to the composer heading with the draft intact. Tab/Shift-Tab move through controls; native type-ahead selects Priya; Enter activates buttons; Escape cancels composition. Status milestones have a polite live region. No global shortcut is invented without the actual host integration.

## Pre-ship checks

- All six direct states in both themes and both display parameters.
- Keyboard select → note → review → send; cancel and pending return routes.
- Explicit harness acceptance; no acceptance timer.
- Contrast, theme parity, fixture integrity, geometry and reduced motion.
- Real macOS menu-bar host, VoiceOver and live backend require later validation.
