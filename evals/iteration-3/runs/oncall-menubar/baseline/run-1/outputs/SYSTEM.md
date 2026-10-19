# Rota and companion fixture views: design system

This system applies only to this prototype. Read `DESIGN.md` for the evidence, state contract, test results and limitations. Values are defined in `app/tokens.css`; `verification/tokens_guard.cjs` guards colour, type, shape, theme parity and contrast.

## Product principles

Rota's first job is responsibility, followed by shift time, current roster and handover. It is a menu-bar utility for roughly 40 SREs, not a full scheduling product. Keep one clear handover action. A review step must precede sending; acceptance must be separate from sending. A pending request never means Jamie has stopped being responsible. Never label the four-person on-call roster as the staff directory.

The only distinctive treatment is the responsibility diagram. Solid/dashed outlines add hierarchy; the words “Responsible now” and “After acceptance” carry the actual meaning. Conventional form controls and plain actions surround it. An offline heading must be explicitly last known. Empty means no schedule, not no incidents.

Northwind is an incident ledger for an operational room. Dense facts stay visible; severity, missing ownership and delayed data deserve attention. Harbour is a short setup flow for older users. It spends space on legibility, labels, warnings and large actions rather than decorative finance imagery.

## Identity and colour

Rota uses the macOS system stack because it belongs inside a native-feeling utility. Northwind and Harbour use locally bundled IBM Plex Sans; Mono aligns incident identifiers, durations and account numbers. Their fonts and fixture contents work offline.

| Role | Light / dark | Meaning |
| --- | --- | --- |
| `fg` | #20252c / #f2f4f7 | Main text |
| `muted` | #59616d / #b4bdca | Supporting facts, never hidden facts |
| Rota `accent` | #2157c4 / #94b8ff | Action and keyboard focus |
| Harbour `accent` | #245747 / #acd8c1 | Setup action and support link |
| `warn` | #7b4b08 / #f2c67b | Pending responsibility, offline, delayed updates |
| `danger` | #ae292b / #ffb2ae | Errors, SEV 1 and missing commander |
| `good` | #256044 / #a0d7b5 | Confirmed completion or resolved history |

Neutrals carry ordinary statuses. Do not turn every status into a colour badge. Brand colours were not supplied: these are task-specific proposals. All text combinations checked by the guard reach at least 4.5:1, with a measured minimum of 5.58:1. Outlined form controls use the supporting text colour. Activity bars clear 3:1 against their track.

## Type, space and shape

Menu body is 14px; menu headings are 20px, roster names 13px and supporting roles 12px. Dashboard body is 16px, incident titles 16px laptop / 18px TV, metrics 36px / 44px TV. Bank body and labels are 18px, hints 16px, headings 30px / 24px narrow, and code input 28px. Weight and placement establish hierarchy before extra colour. Use tabular numerals for operational values.

Spacing follows 4, 8, 12, 16, 20, 24, 32, 40, 48px; the 6px compact step is reserved for TV incident row padding. Controls have 6px corners, grouped facts 10px, popover/dialog 14px. Hairlines divide roster and incident rows. Only the floating popover and modal use shadows. Avatars identify people by initials and remain visually quiet.

Menu controls target at least 34px; banking targets at least 48px, primary controls/inputs 56px. Do not shrink banking text to force short-phone content into one screen. Scroll instead.

## Layout and states

The menu popover is exactly 360px wide at 20/20 in a 400×680 scene, capped at 640px with internal scrolling. A shift summary comes first, current roster second, handover action third. Compose uses a select and optional note; review exposes the same facts plus responsibility; pending spells out the continuing obligation.

Dashboard order is product/freshness/time, four metrics, incident ledger and an operational sidebar. The sidebar contains on-call, service values and resolved history. Laptop pages scroll naturally. TV row and sidebar spacing fit every required incident and resolved entry within 1920×1080. Do not remove data to achieve the fit. Stale must replace the live indicator and qualify the entire snapshot.

Bank is a single column with persistent Help in the header. One short introduction precedes the form. Safety text is adjacent to code confirmation; the modal repeats it. Help uses a native dialog and telephone action. All direct states are documented in `DESIGN.md`.

## Motion, words and keyboard

Only a 120ms background transition is used. Reduced motion removes transitions; it never changes information. No success timers or automatic handover acceptance.

Use specific, calm sentences: “You’re still on call.” / “No shifts to show.” / “Handover complete.” Explain uncertainty and consequence in words. Native selects, Enter/Space buttons and Tab navigation need no invented shortcuts. Heading focus follows a view transition; error focus goes to the invalid field; closing Help restores its invoking button. Wrap Tab inside Help; use native focus return for ordinary opens and explicit focus return only for the direct Help route to prevent a delayed second focus change. Focus uses a 3px accent ring with 3px offset.

## Change checks

Run the token guard and browser suite. Inspect affected states in both themes at every required size. Check long text, zero data, stale data, missing ownership, keyboard focus, cancellation and explicit acceptance. Keep all facts from `EVAL_FIXTURES` and never display the fixture SMS code. No new live-data claim is valid without an actual connection. No generic palette preference should be inferred from this task.
