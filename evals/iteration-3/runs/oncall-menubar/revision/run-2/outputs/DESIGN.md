# Delivered prototype

Open `app/index.html` directly from disk. It needs no server, network, build or dependency install. The default is Rota’s main popover. `review.html` is a separate review harness; it contains state navigation and the explicit simulated acceptance action, outside the product canvas.

## Direction and priorities

For the opening Rota task: ownership first, safe handover second, current roster third, honest saved status fourth, keyboard efficiency fifth. The result is a macOS-sized utility with system typography, a prominent own-shift object, one handover action and a quiet roster. It does not present four current people as all 40 SREs.

Two actual-size compositions are preserved in `explorations/compositions.html` and `verification/compositions.png`. A puts responsibility and the action above the roster. B makes a full rotation directory the first object and places the action below it. In the comparison render, A’s action begins around y282; B’s is around y655 and exceeds the requested scene. A wins for the stated priorities. Its cost is repeating Jamie’s name in the full current roster; that keeps the list complete and consistently structured. The pending variants were also compared: the chosen variant gives the continuing responsibility sentence its own visual group.

There was no existing UI or code to audit. The composition studies are the baseline, not evidence of pre-existing defects. Final main: own-shift title starts at about y142 and the action at y254, all four roster entries and the footer fit in the 640px popover.

The dashboard and bank states are implemented as required by the evaluation contract, with separate identities and densities. Their layout decisions do not imply a blanket preference for these palettes or font sizes.

## Reference evidence

Read the supplied skill and its philosophy, method, identity, decisions, critique, case-recall and system/guard templates. Inspected the provided Dia profile-form and signup images and Arc routing sheet. Dia’s profile form demonstrates a clear heading, ordinary field and explicit cancel/confirm pairing. Arc’s routing sheet demonstrates aligned native controls and quiet separation. Those relationships inform the handover form and review, without copying branding or inventing new mechanics. The signup crop reinforces large labeled fields for Harbour.

These are frozen crops and published demo frames. They do not establish timing, complete flows, real accessibility behavior or macOS API constraints. The configured popover geometry comes from the user’s contract. No external research, service or other project was accessed. The requested `dashboard/index.html` and `brand/guide.md` do not exist in the supplied tree; no guide was edited. Dashboard identity is therefore a documented proposal using the supplied fonts and fixtures.

## Direct URLs

Append these query values to `app/index.html`:

| Surface | `screen` values | Tested scene |
| --- | --- | --- |
| Rota | `main`, `compose`, `pending`, `offline`, `empty`, `accepted` | 400×680; popover 360px at (20,20), max 640px |
| Northwind | `live`, `stale`, `surge` | `display=tv` at 1920×1080; `display=laptop` at 1440×900 |
| Harbour | `welcome`, `details-error`, `code`, `code-error`, `help`, `done` | 390×844 and 320×568 |

Use `theme=light` or `theme=dark`. Omit theme to follow system preference, including changes while open. Internal `details` and `review` states also support direct URLs. Browser Back rerenders the previous step. For example: `app/index.html?screen=main&theme=dark`.

## Implemented behavior

- Rota: select Priya, add an optional note, review, send to local pending, return to the roster, revisit the request or cancel it. Jamie stays responsible while pending. Accepted makes Priya responsible and returning to the roster shows Jamie off call. Acceptance only occurs through the separate harness’s explicit button. No timer auto-accepts. Offline shows the saved timestamp and qualifying last-known language; it offers no handover. Empty invents no schedule; Check again honestly reports the local limitation.
- Dashboard: the seven original live/stale incidents, all twelve in surge, every title, ID, severity, service, status, opening time, duration and commander. Missing commander reads “Unassigned”. Both resolved records and all original metrics, duty names and service values remain. The provided service values are not recalculated to reconcile with the provided page count. Stale has an amber notice, paused status and as-of time instead of a green live signal.
- TV overflow: seven live/stale rows fit. Surge deliberately keeps full-sized text and has more rows than its 590px list can show. A visible sentence explains the overflow and points to scrolling or a laptop. No automatic carousel hides changes. The list is focusable and supports keyboard scrolling; all twelve remain in the DOM. Laptop supports list and document scrolling, so resolved history and the last incident remain reachable.
- Harbour: welcome → details → code → completion. Details validates a nonempty name with letters and a UK mobile beginning 07 or +44. Errors identify the failed field. Code input supports paste and rejects incorrect values; only the fixture test code completes the flow, and it is never printed in the UI or screenshots. Back retains typed details. Help is reachable throughout, directly opens over code at `screen=help`, has the supplied telephone link, and dismisses by button or Escape with focus return. The warning remains in the page. Completion shows original account facts.
- All surfaces: labeled controls, native keyboard operation, visible focus, both themes, system preference and reduced-motion support. Text is never truncated. Long notes and narrow phone content scroll rather than being discarded.

## Deliberate omissions and limits

This is an offline interaction prototype, not an installed macOS menu-bar app. There is no native status item, real schedule store, authentication, notification, paging integration, SMS delivery or verification service. Requests and typed details live only in memory and reset on reload. Direct URLs seed a state rather than reconstructing a backend history. The recipient chooser contains the supplied Priya option, not an invented 40-person directory. Resend describes that it cannot send a real text. Support dialing requires a phone handler on the user’s device. No real bank account is opened.

Native VoiceOver announcements, macOS popover anchoring, physical TV reading distance and the brand owner’s approval need human/device review. Screen-reader semantics and focus were checked in Chromium, not with VoiceOver. No clinical claim is made about older-user accessibility; larger type, labeled fields and comfortable targets are design provisions to validate with real people.

## Verification and corrections

Run from the workspace root:

```
node outputs/verification/tokens.cjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

Chromium needed sandbox escalation for local process startup. No network access is used by the prototype. The script checks every required direct state in both themes at every specified size (48 state/size combinations), plus interaction paths. Results and measurements are in `verification/results.json`; contrast ratios are in `verification/contrast.json`. Selected actual renders are beside the scripts.

Rendered critique and refinements:
1. TV durations initially wrapped, making the seventh row fall below the visible list. Widened the duration column, prevented line breaks and adjusted the TV row rhythm. All seven now fit; surge uses explained overflow.
2. Offline’s alert plus full shift card pushed the final roster entry below the popover edge. Replaced the progress card with a compact last-known summary and made its tense explicitly historical.
3. Input outlines were too faint to carry the field boundary. Added a dedicated control-border role with at least 3:1 contrast. Kept quiet separators separate from functional boundaries.
4. Removed a completion button that only repeated already visible account information. Made the welcome heading name the setup task directly.

The final audit covers horizontal overflow, popover bounds, page errors, actual incident counts, keyboard review/send/cancel, explicit harness acceptance, details validation, incorrect-code rejection, correct-code completion, Help Escape/button focus return, system dark preference, reduced motion and laptop surge scrolling. The token guard checks theme parity, external literal colors/type/radii/shadows, 46 text contrast pairs at 4.5:1 or better, functional field boundaries at 3:1 or better, stylesheet wiring and exact fixture-copy integrity. It does not claim automated assistive-technology certification.

A useful proposed addition to the supplied method: when a small status tool can go offline, test the tense of every ownership statement as well as its alert banner. A stale banner alone can leave a present-tense card looking more certain than the data permits. No supplied skill was modified.
