# Northwind incident dashboard redesign

Open `app/index.html` directly from disk. No build, server, package install or network is required. `review.html` links to all twelve combinations of state, theme and display.

Direct URL example: `app/index.html?screen=surge&theme=dark&display=tv`.

## Direction and priorities

The incident comes first: make severity, current ownership and freshness obvious, then support the response with metrics and operational context. This is for operators glancing across a room and engineers reading on laptops. The hierarchy is:

1. Critical incident and missing commander.
2. Whether the snapshot is current or stale.
3. The full open register, including monitoring and mitigated incidents.
4. Response metrics, on-call cover and thirty-day service concentration.
5. Separately identified resolved history.

The familiar table is retained, with aligned fields and a broad title column. The distinctive treatment is concentrated on the SEV1 row: a severity spine, a quiet red ground and explicit “Unassigned.” A navy identity bar, brand typography, neutral page and restrained teal service bars establish Northwind's identity without decorative cards, emoji or gradients.

The unchanged brand guide is authoritative. IBM Plex Sans and Mono ship locally. The compass N is a simple white SVG interpretation because no official logo asset was supplied; its fidelity has not been approved by a brand owner. Signal Orange is not spent on large areas or body text. Tide Teal is adjusted to contrast-safe service-bar tones. See `SYSTEM.md` and `app/tokens.css` for roles and values.

## Research and baseline

Read the existing `dashboard/index.html` and brand guide first, then the supplied skill and its philosophy, method, identity, decisions, critique, worked example and system/guard templates. No installed skills, network sources, other projects or agents were used.

Offline references: `reference-pack/SOURCES.md`, visually inspected `dia-profile-form.png` and `arc-recovery.png`. The former supports familiar form controls with deliberate hierarchy; the latter makes a consequential state a concrete, labeled object. Borrowed reasoning: preserve ordinary mechanics and reserve special treatment for consequential information. This dashboard does not copy their palette, rounded forms, typography or recovery-card metaphor. These are cropped published frames, not evidence about whole workflows or unseen interactions. No additional product behavior is inferred from them.

Baseline at 1440×900: the incident table began at y=678; document height was 956 px. The original displayed five incident rows even though the open metric was seven, mixed resolved work into recent incidents and omitted commander data in the table. Gradients, emoji, broad purple fills and repeated rounded cards competed with the incident list. Only one freshness badge and one theme existed.

Final table starts at y≈392 on laptop, about 286 px earlier. At the TV target it starts at y≈405. The redesign exposes all seven live incidents and the fixture's commander values, without reclassifying monitoring or mitigated work as resolved.

## Implemented behavior

- `screen=live`: first seven fixture incidents, open count seven.
- `screen=stale`: same seven incidents, amber header treatment, “Updates paused,” last-received time 09:42, and a plain warning that status, counts and durations may have changed. No live freshness label or fabricated retry.
- `screen=surge`: all twelve fixture incidents, open count twelve.
- All non-resolved statuses count as open. The separate two-item resolved history does not contribute to open counts.
- Original incident facts, titles, services, statuses, severities, opened times, durations and commander names are preserved. Missing commander is explicitly “Unassigned.” Opened time is visible beneath duration. Resolved opened times remain available in incident details.
- Fixture metrics, service totals, on-call names and handover time are retained. The original open-count change of +2 versus yesterday is retained for the seven-incident snapshots; no unsupported comparison is calculated for surge. The pages delta is displayed without inventing its comparison period.
- Search by title, ID, service or commander; severity filtering; explicit no-match state. Summary metrics remain the overall snapshot when the table is filtered.
- Incident and resolved-history details open in a native modal. Close and Escape dismiss; focus returns to the opener.
- Light/dark via URL or system preference. With no explicit theme, changes to the system preference are followed. The theme control updates the current URL without resetting filters. Display preference preserves screen/theme and clears the skip-link fragment to reopen at the top.
- Native, labeled controls; skip link; scoped table headings; named regions and dialog; visible focus, including white focus on navy. Search and select retain focus when results change. TV pager focuses the available page control. Control targets are at least 44 px; incident hit regions cover the title cell, and resolved hit regions cover their item.
- No animation, flashing, automatic page rotation or running clocks. Reduced motion retains all information.

## TV overflow and laptop reachability

At 1920×1080, all states fit vertically and horizontally, including operational context, resolved history and paging controls. TV type increases to 22 px incident titles, 20 px body and 15–17 px metadata. Seven incident rows are shown per page. Surge explicitly says “Showing 1–7 of 12” with a two-page control; the second page contains incidents 8–12. Nothing is silently dropped. No auto-rotation removes an incident while someone reads it. The missing-commander warning remains visible on both pages.

At 1440×900, the page uses normal document scrolling. All twelve surge incidents exist in the single table, with no inner vertical scroll region or pagination. The last incident and resolved history are reachable by scrolling and keyboard focus. Document heights are approximately 1023 px for live/stale and 1363 px for surge. At narrower widths the context flows below the register, and the table can scroll horizontally; narrow mobile use is a fallback, not an evaluated primary layout.

## Verification actually performed

Run from this workspace:

```sh
node outputs/verification/design-guard.mjs
/private/tmp/design-compare-venv/bin/python outputs/verification/verify.py
```

Chromium needed the normal sandbox escalation because macOS process registration was blocked in the sandbox. No dependencies were installed.

- All 12 combinations: live/stale/surge × light/dark × laptop 1440×900 / TV 1920×1080, loaded using `file://` with reduced motion enabled.
- Screenshots taken for every combination and assembled into `verification/state-matrix.png`. Full-size examples retained for live light TV, stale dark TV, surge dark laptop and surge TV page two, plus the original baseline.
- Inspected the contact sheet and full-size TV light, TV stale dark, surge page two and laptop dark renders. Initial TV clipping and excessive sidebar/header spacing were corrected, then rerendered. Opened times were restored to the table, and stale information was moved into a prominent reserved header region.
- TV document height ≤1080, no horizontal overflow at either target size, no JavaScript page errors, local font loading succeeds, no HTTP(S) requests. Observed initial layout shift was zero across the measured matrix.
- Search, no-match state, severity filter, details, Escape, focus return, both TV pages, theme URL updates and system preference changes.
- Keyboard-only path: skip link → search → severity select → incident → modal → Escape; focus and open the last surge incident and a resolved incident; activate display change by keyboard.
- Design guard: fixture copy byte identity; color and font-size tokens; radius rules; theme color parity; 34 text/background contrast pairs at ≥4.5:1; service graphics, control boundaries and focus at ≥3:1 for their tested surfaces. `verification/contrast.json` and `verification/results.json` contain measurements.

## Critique and remaining limits

Three weaknesses found in the first renders were excessive TV vertical extent, repeated sidebar spacing, and opened times only accessible in details. All three were corrected. A severity strip was removed because the explicit severity counts and critical row already carry that information. High-contrast control boundaries and header focus were added during the accessibility pass.

Not implemented: real refresh/polling, incident mutation, commander assignment, notifications, authentication, export, historical trend charts or automatic TV rotation. The prototype is an honest fixed snapshot driven by the provided `EVAL_FIXTURES`, not a simulated backend. Fixture dates and durations are preserved literally; no attempt is made to recalculate them from the host clock or infer a timezone.

Not verified: physical TV legibility at room distance or with overscan, a screen reader session, other browser engines, real live-data failure/recovery, OS high-contrast mode, browser zoom extremes or official logo fidelity. Automated contrast and semantics checks are not a complete accessibility audit.

No durable aesthetic preference was recorded: the flat operational register, navy identity and larger TV type are choices for this task. A possible lesson for the supplied skill is to require wall-display overflow and paging controls to be verified together; a fit check of incident rows alone misses controls below them. The frozen skill was not edited.
