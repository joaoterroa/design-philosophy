# Iteration 1 comparison captures

Open [index.html](index.html) from disk; no server or build step is needed. Blind mode starts enabled. Reveal a pair to see its caption, identities, source links and full-size PNG links. Use the Show filter for matched or one-sided states. Votes are independent for each viewport and theme, saved in localStorage when available, and exported with the original left/right assignment plus the chosen design identity. When storage is unavailable, voting and export still work in memory.

## Reproduce

From the repository root, with Python 3.10+:

```sh
python3 -m venv /tmp/design-compare-venv
/tmp/design-compare-venv/bin/pip install -r evals/scripts/requirements-compare.txt
/tmp/design-compare-venv/bin/python -m playwright install chromium
/tmp/design-compare-venv/bin/python evals/scripts/capture_pairs.py
/tmp/design-compare-venv/bin/python evals/scripts/verify_compare.py
```

Both scripts accept `--browser /path/to/chromium`. Capture also accepts `--repo-root` to read sources from another clean checkout and `--output` for a separate destination. The page expects to remain under `evals/iteration-1/compare/` for its relative live-prototype links to resolve. Verification accepts `--screenshots /tmp/compare-qa` for page renders. Dependencies and browser installation require a network once; capture and page operation do not. Browser/system font differences can change pixels across machines.

`comparison_pairs.py` is the state-mapping source of truth. Capture writes the PNGs, `manifest.json`, `capture-report.json`, and the same manifest inline in `index.html` to avoid file-URL fetch restrictions. It checks every expected filename, dimensions, non-uniform pixels, theme, console errors and unexpected network access. UI verification checks disk opening, scale equality, all light-image loads and live links, blind shuffle/reveal, theme-specific persistence, JSON download, storage-disabled fallback, and no horizontal scroll at 1440, 1280 and 390 px.

## Coverage

262 PNGs across 89 screen/size combinations: 42 matched design pairs, 45 one-sided states, and two shared-original pairs. All design screens have both light and dark captures. The unchanged original dashboard has light only. Every row from the starting table in `evals/README.md` is included.

- Menu bar: 13 states, cropped native panels (340 px with, 360 px without), loaded at the same 1100 × 800 viewport. Eight matched; five one-sided.
- Dashboard: ten states at each of TV 1920 × 1080 and laptop 1440 × 900. Four matched design states, five one-sided states and one shared original at each size.
- Banking: 28 states at each of 390 × 844 and 320 × 568. Thirteen matched and fifteen one-sided at each size.

The inventory below lists semantic states once; dashboard and banking rows repeat at both sizes. “Only” describes a distinct screen/state at that point in the flow, not absence of all related behaviour elsewhere. For example, the banking baseline always uses account numbers, while the skill version exposes that route through an explicit no-card alternative.

## oncall-menubar

| Screen | Matching | Concrete difference / reason for no match |
| --- | --- | --- |
| On call · main panel | Matched | With: a shift strip above the rotation list. Without: a Now/Schedule tab bar and a next-shifts section. |
| Composing a handover | Matched | With: an eight-hour range and availability on each candidate. Without: a thirteen-hour range and a disclosure for less suitable candidates. |
| Waiting for acceptance | Matched | With: an outlined, hatched segment marked PR?. Without: a striped segment labelled Priya?. Both say the shift remains yours. |
| Offline · cached schedule | Matched | With: cached-data age sits in the footer, with a connection explanation below Hand over. Without: an offline notice follows the next-shifts section. Both disable handover. |
| Not on call | Matched | With: the next shift appears in the main answer. Without: a separate next-shifts section follows the rotation list. |
| Handover accepted | Matched | With: the accepted interval remains on the multi-day strip. Without: the remainder is labelled with Priya's name on the shift bar. |
| Handover declined | Matched | With: the reply appears below the shift strip as plain text. Without: the reply has a tinted notice inside the current-shift panel. |
| Incoming handover request | Matched | With: the request appears before your own shift. Without: the request replaces the main you-panel and includes a rota check. |
| Handover could not be sent | Only in with | Only in with: an in-place send failure keeps the handover form and states that nothing changed. |
| Coverage gap · main panel | Only in with | Only in with: a gap warning appears in the main panel. Without has gap information in its separate Schedule view. |
| First sync | Only in with | Only in with: a first-sync spinner and a connecting message in an otherwise empty panel. |
| Not connected · first run | Only in with | Only in with: a first-run sign-in state before a schedule is connected. |
| Weekly schedule | Only in without | Only in without: a dedicated Schedule tab with a seven-day rotation view and a named gap. |

## incident-dashboard

| Screen | Matching | Concrete difference / reason for no match |
| --- | --- | --- |
| Live · SEV1, no commander | Matched | With: the missing commander sits in the SEV1 row and the on-call band. Without: it is called out in a banner and an on-call card; the SEV1 is repeated in the list. |
| Data stale | Matched | With: an amber freshness header retains the incident list. Without: an inverse warning replaces the status banner and dims the data. Fixture ages differ (about six versus seven minutes). |
| All clear | Matched | With: zero-open wording leads into resolved history. Without: an all-clear banner includes days since the last SEV1. The runs invented different history and budget values. |
| Loading | Matched | With: row-shaped placeholders reserve the list and chart areas. Without: loading messages occupy the dashboard's existing panels. |
| Rota source failed | Only in with | Only in with: the rota source fails while incident and metric data remain live; this is not the whole-feed failure on the other run. |
| Surge · twelve open incidents | Only in with | Only in with: twelve open incidents; TV names the rows that cannot fit, while laptop can scroll. |
| SEV1 · commander assigned | Only in without | Only in without: Ana L. is assigned as incident commander in the live SEV1 state. |
| SEV2 only | Only in without | Only in without: the SEV1 has resolved and the headline changes to the remaining SEV2 incidents. |
| Entire feed down | Only in without | Only in without: the entire incident feed is unavailable; this differs from losing just the rota source. |
| original (before) | Shared original | Both: the same unmodified original dashboard. This is shared context, not a with/without design result. The original has no dark theme. |

## banking-onboarding

| Screen | Matching | Concrete difference / reason for no match |
| --- | --- | --- |
| Welcome | Matched | With: setup requirements and a Start button share the welcome screen. Without: two account-status choices lead to a separate preparation screen. |
| Account details · errors | Matched | With: errors concern the long card number and date of birth. Without: errors concern date of birth, sort code and account number. Both use a summary plus field errors. |
| Enter the texted code | Matched | With: the code input and Continue come before a preview with blank code digits. Without: a preview containing 482 913 comes before the input. |
| Done | Matched | With: balance and last money in follow the setup confirmation. Without: a balance panel precedes reminders that card and branch banking remain available. |
| Account details | Matched | With: long card number and date of birth, plus an alternate account-number route. Without: date of birth, sort code and account number are the default route. |
| Account not found | Matched | With: the no-match message stays on the details form. Without: no match has its own result screen. Both represent the same failed account lookup. |
| Text code · wrong | Matched | With: an inline wrong-code message leaves the field high on the page. Without: a summary precedes the preview and code field. Both name the remaining tries. |
| Text code · delivery help | Matched | With: delivery help expands within the code screen, with a new-code notice. Without: a separate help screen offers resend, a voice call and changed-number guidance. |
| Choose a passcode | Matched | With: passcode and confirmation are on one screen. Without: confirmation is a separate step. |
| Passcode · easy to guess | Matched | With: the two-field form rejects a sequential passcode. Without: an error summary and message appear on the first passcode screen. |
| Optional biometrics | Matched | With: face or fingerprint includes a warning about other people enrolled on the phone. Without: fingerprint is offered alongside a full-size passcode-only option. |
| Account details · help sheet | Matched | With: help explains the card-number route and its alternative. Without: help explains where to find sort code and account number, with a card illustration. |
| Alternative · no card | Only in with | Only in with: an explicit alternate identification route. Without already uses sort code and account number by default (see Account details). |
| Text code expired | Only in with | Only in with: an expired-code message and a new-code action; this differs from the other run's session-timeout dialog. |
| Text code · attempt limit | Only in with | Only in with: a dedicated attempt-limit state replaces the code form. |
| Final setup · working | Only in with | Only in with: named connection tasks after biometrics. Without's checking states happen earlier, before text-code verification. |
| Final setup · slow | Only in with | Only in with: a delayed final-setup state keeps the connection tasks and adds reassurance. |
| Final setup · failed | Only in with | Only in with: a final-setup failure explains that the account has not changed and offers retry. |
| Before you start | Only in without | Only in without: a dedicated preparation screen. With puts requirements on its welcome screen. |
| New customer guidance | Only in without | Only in without: people without an existing account are directed to assisted account opening. |
| Identity check · working | Only in without | Only in without: named identity-check tasks before the text-code step; with moves directly from valid details to code. |
| Identity check · slow | Only in without | Only in without: the identity check explains a longer-than-usual wait. |
| Identity check · very slow | Only in without | Only in without: an extended identity-check delay offers a way to stop and keep the entered details. |
| Identity check · failed | Only in without | Only in without: a failure before text verification says no money moved and offers retry. |
| Session timeout warning | Only in without | Only in without: a modal offers more time or stopping. With deliberately has no screen timeout. |
| Confirm passcode · separate step | Only in without | Only in without: passcode confirmation has its own screen. With combines both fields (see Choose a passcode). |
| Confirm passcode · mismatch | Matched | Without: mismatch is on the separate confirmation step. With also validates mismatches, on its combined form; captured via that form here. |
| Standalone safety advice | Only in without | Only in without: a separate scam-advice acknowledgement. With places scam advice alongside text-code verification. |

## Limits and visual verification

- The runs used different fixture dates, names, shift lengths, lower-severity incidents, banking balances and identification methods. States are semantically matched, not rewritten to force identical data. Stale data is about six versus seven minutes old; final setup and the earlier identity check are separate one-sided states.
- Menu-bar and banking baselines used the Recall design system. Only the dashboard baseline is a clean no-philosophy run. There is one run per configuration, so this is a visual preference exercise, not a causal or statistical estimate of skill quality.
- Captures keep each prototype's original fonts. Dashboard with-skill bundles Plex Sans; without-skill falls back to a system sans. macOS material, device text sizing and native controls are simulated by Chromium. Reproducing on another OS or browser build may change line breaks.
- Phone and dashboard images capture the initial viewport at scroll position zero. Content and actions below that fold remain absent, particularly at 320 × 568. Cropped native menu panels keep their internal scroll limits and first scroll position. They are padded on the page and never stretched to match the other panel. Native rounded corners and shadows are cropped at the panel bounds; desktop/menu-bar context is deliberately excluded.
- The banking baseline's prototype-only footer is hidden during capture, as in its original capture script. Product styling/content is unchanged. The dashboard baseline uses its kiosk option to hide demo controls; the skill dashboard's laptop footer stays as authored.
- The controlled clock advances 1.5 seconds, enough for the skill banking SMS preview and slow-setup note to appear, before a normal identity check leaves its initial state. Dashboard clocks retain their own fixture dates; the skill version additionally uses its `frozen` option. Animations and the caret are suppressed in PNGs. Fresh browser storage prevents resume state or theme from leaking between captures.
- Blind mode hides visible attribution, difference captions and live links until reveal; styling and missing-state silhouettes can still identify a run. The source files, manifest and exports necessarily contain identities. Votes store whether attribution was visible at voting time. Re-enabling blind mode reshuffles; existing choices remain attached to design identity. File-URL localStorage persistence is browser-dependent and moving the page can change its storage scope.
- All 262 expected PNGs were checked for dimensions/non-uniform pixels and all pair sheets were visually reviewed in both themes. The page was rendered at 1280/1440 and phone widths, and the dashboard and banking code pair were inspected at presentation scale. Existing long-title truncation on the dashboard and below-fold phone content are preserved as evaluation evidence.
- Capture and UI verification were repeated successfully from a clean local git clone with Playwright's default headless Chromium. The final PNGs come from that run. No prototype console errors, page console errors or network dependencies were encountered.
