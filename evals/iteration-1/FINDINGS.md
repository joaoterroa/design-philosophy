# Iteration 1 findings (2026-10-18)

Three prompts, each run twice by an independent agent: once told to read this skill (`with_skill`), once not (`without_skill`). Every run produced a `DESIGN.md`, a static prototype in `outputs/app/` and screenshots in `outputs/screenshots/`. The skill was at version 0.1.0 (commit `9037897`) and was not changed during or after the runs.

| Eval | Prompt (short) | Folder |
| --- | --- | --- |
| 1 | Design a macOS menu-bar app for on-call schedules and shift handover (40 SREs, no code) | `oncall-menubar/` |
| 2 | Redesign an incident dashboard for an ops-room TV and laptops, with a brand guide | `incident-dashboard/` (inputs: `../fixtures/incident-dashboard/`) |
| 3 | Onboarding flow of a mobile banking app for older customers moving from branches | `banking-onboarding/` |

## Results

| | With skill | Without skill |
| --- | --- | --- |
| Assertions passed | 29/29 (100%) | 26/29 (91%) |
| Mean time | 1145 s | 825 s |
| Mean tokens | ~197k | ~151k |
| Screenshots per run | 20–63 | 14–29 |

Per-run grades with evidence: `<eval>/<config>/grading.json`. Aggregate: `benchmark.md`. A static review page (write-ups and grades, not images): `review.html`.

## Important caveat: two baselines were not skill-free

The runs shared a machine with the project this skill was extracted from. Asked to use "my design philosophy" without the skill, the menu-bar and banking baselines searched, found that project's `design/SYSTEM.md` (the "Recall" design system) and used it as the philosophy (each says so in its `DESIGN.md`). Those two comparisons measure the skill against a written project design system, not against nothing. Only the dashboard baseline is a clean "no philosophy" run.

Future runs must keep baselines away from any of the user's design documents (separate machine or container, or an explicit, enforced exclusion).

## What the comparison shows

- **Clean comparison (dashboard): clear difference.** All three baseline failures are here: no ordered priorities, no deliberate novelty moment, a literal colour outside the tokens and no guard test. Visually it repeats the SEV1 and "Not assigned" in a banner, the list and a card, and truncates "Not assi…". The skill's run is one calm list with no repeated facts, the missing commander in the SEV1's own row, and a single distinctive element (24-hour lanes on a shared now-axis), with measured before/after positions and four critique-and-fix rounds.
- **Against the Recall system (menu bar, banking): close.** Structures and quality are very similar. The skill's banking run avoided a real hazard the baseline has: its text-message preview shows a sample code ("482 913") an older user could type.
- **Rigour.** Wherever the skill was used, the runs recorded ordered priorities, measured layouts, more states, two to four refinement rounds and more screenshots. That is most of the extra time and tokens.
- **Identity.** No run reused the Recall palette. But two of the three with-skill runs that had no brand guide defaulted to a safe blue (the banking run called its own palette "safe rather than distinctive"). `identity.md` should push harder when no brand exists.

## Limits of this iteration

- The assertions were mostly too easy: 9 of 11 pass on both sides, so the pass rate barely separates the configurations. Harder checks are needed (facts shown twice, sample-data hazards, primary action above the fold, a blind preference judgement).
- One run per configuration; no variance.
- No side-by-side visual comparison was produced. That is the next step (see `README.md` in this folder's parent for what a comparison page should show).

## Lessons proposed by the with-skill runs (not yet applied to the skill)

The skill asks agents to propose edits at the end of a project. All seven proposals generalise beyond their project:

1. `critique.md` › States: for tools that change shared responsibility (on-call, approvals, ownership), check that no surface (menu bar, badge, notification) looks more resolved than it is. *(menu bar)*
2. `decisions.md` › Platform constraints: for wall or TV displays, size type from the viewport height so one layout serves every resolution, and set an explicit, measured row budget ("N items must fit at 1080p"). *(dashboard)*
3. `critique.md` › Restraint: check that visual weight follows importance, not quantity; a long bar for a minor item can outweigh a small mark for a critical one. *(dashboard)*
4. `method.md` › Phase 3: check that existing headline numbers agree with the detail beneath them. *(dashboard)*
5. `decisions.md` › Accessibility: test at 200% text; keep horizontal insets fixed while type and vertical rhythm scale. *(banking)*
6. `decisions.md` › Hierarchy: measure where the screen's primary action sits, not only where content starts. *(banking)*
7. `method.md` › Phase 3: with no existing product, say so and treat the first rendered build as the baseline, with numbers. *(banking)*

Plus, from reviewing the runs: strengthen the no-brand guidance in `identity.md` so "a safe blue" is treated as a default to justify, not a choice.
