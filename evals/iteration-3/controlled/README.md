# Controlled comparison: current and experimental skill

**Complete: twelve runs, 192 matched PNGs.** The [findings](FINDINGS.md) recommend keeping the current baseline: the revision wins both menu comparisons, the current skill wins both dashboard comparisons, and banking is mixed. The experimental revision remains separate.

Open [index.html](index.html) from disk. It embeds the matched screenshots and needs no server or network. Conditions and the assessment start hidden. Left/right order is randomized per pair and stored in this browser. Click **Reveal**, select a state and size, switch screenshot themes, or click an image to inspect it larger. Choices persist locally and export as JSON.

The canonical skill is unchanged. [skills/baseline/](skills/baseline/) preserves the current version; [skills/revision/](skills/revision/) is the separate experimental revision. [revision.diff](revision.diff) records the intervention. The optional shape reference retains the user's preference for Adjusted Squircle when the product benefits from softer continuous corners. It is not a universal treatment.

## Design and scope

The same three original prompts each receive two runs per condition: twelve independent design jobs. Each gets only its assigned task's requirements and data, the same raw first-party visual references, offline fonts and one frozen skill version. The executor is Codex CLI 0.163.0, `gpt-6.1-sol`, high reasoning, with at most three simultaneous jobs. Each run has twelve minutes of cumulative active process time, including exploration, implementation and verification. Extra exploration competes with implementation under the same allowance.

The shared requirements add deterministic state hooks, data and capture sizes to make the conditions comparable. They therefore test these skill versions under a controlled contract, rather than reproduce iteration 1's unconstrained runs. Hosts' skills, prior prototypes, conversation history, web, plugins and MCP are excluded from the generators. Workspace separation and a logged read-boundary audit are controls, not proof of filesystem confinement.

[protocol.json](protocol.json) froze inputs before generation. Skill and input hashes are checked at launch and after each run. Outputs are copied without evaluator repair. Any failed or unfinished design remains a result; poor outputs are never replaced.

An earlier cohort under the parent directory is **excluded in full**: its shared contract listed requirements for all three apps and caused unequal workloads. The primary cohort uses task-specific contracts and the same frozen skill versions. This exclusion was made for a harness defect, before adopting a preferred design. See [../PILOT-EXCLUSION.json](../PILOT-EXCLUSION.json).

## Service interruption

All twelve attempts encountered a service usage limit. After a read-only account check confirmed ordinary usage available again, they resumed their exact saved sessions and existing workspaces. Interrupted segments remain in each run's `quota-segment-N/` folder. Only the original remaining time is available; no extra design allowance, quality feedback, replacement model, credentials or reset credits are supplied. [recovery.json](recovery.json) records these continuations. The frozen protocol is not rewritten to hide the interruption.

## Captures and review

| Task | States | Sizes | Themes | PNGs per run |
|---|---|---|---|---:|
| On-call menu | main, compose, pending, offline, empty, accepted | Native 360px popover in a 400×680 scene | Light/dark | 12 |
| Incident dashboard | live, stale, surge | 1920×1080 TV; 1440×900 laptop | Light/dark | 12 |
| Banking onboarding | welcome, details-error, code, code-error, help, done | 390×844; 320×568 | Light/dark | 24 |

Four runs per task produce **192 expected final PNGs**. Collection uses DPR 1, en-GB, Europe/London, a fixed clock and reduced motion. Network access is blocked. Captures record dimensions, non-uniform pixels, hashes, console errors and source integrity.

Functional checks and visual judgment are separate. Anonymous reviewers inspect equal-scale images before seeing the condition key or design rationale. The [rubric](reviews/RUBRIC.md) covers composition, hierarchy, task fit, personality, craftsmanship and overall quality. Generic selectors that cannot follow a prototype receive manual review rather than an automatic design failure. Real user performance, assistive technology and native host integration remain untested.

The adoption gate requires a stable preference for the revision on at least two tasks across both repeats, with no new critical functional, accessibility or coverage regression. Two repeats, one model and a bundled intervention support a directional judgment; they cannot prove statistical significance or isolate which instruction caused a difference. Promotion still requires the user's review.

## Recollect or rebuild

From the repository root, use Python with `evals/scripts/requirements-compare.txt` installed and Playwright Chromium available:

```sh
python evals/iteration-3/tools/capture.py --protocol evals/iteration-3/controlled/protocol.json --all
python evals/iteration-3/tools/grade.py --study evals/iteration-3/controlled
python evals/iteration-3/tools/anonymize.py --study evals/iteration-3/controlled
python evals/iteration-3/tools/build_report.py --study evals/iteration-3/controlled
python evals/iteration-3/tools/verify_report.py --study evals/iteration-3/controlled
```

Use `capture.py --replace-capture` only to recollect from unchanged app outputs. These commands do not rerun designs. Preparation scripts and the generation runner preserve a once-only attempt lock; do not regenerate frozen inputs. `resume_controlled.py` is only for service-quota continuation after confirming a reset, with archived segments and the original cumulative time budget.
