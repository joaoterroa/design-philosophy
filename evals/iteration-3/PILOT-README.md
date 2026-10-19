# Iteration3: primary comparison and excluded pilot

The valid task-only comparison is in **[controlled/](controlled/README.md)**. Open **[controlled/index.html](controlled/index.html)** once built. The experimental skill snapshots are unchanged between cohorts.

The first cohort below is an **excluded pilot**, not evidence for adoption. Its contract listed requirements for allthree apps, and several generators implemented the whole suite despite a task-only sentence. We stopped and retained the whole cohort rather than select individual outcomes. See [PILOT-EXCLUSION.json](PILOT-EXCLUSION.json).

The primary cohort has12fresh jobs and a720second equal allowance. Combined with the pilot’s approximately84.5active generation minutes, its maximum144minutes stays within the original240minute generation plan. No credits were purchased or reset credits consumed.

---

# Experimental iteration 3

The current skill remains unchanged at the repository root. The experiment lives entirely here. The copies in `skills/` are frozen evaluation inputs, not newly registered or promoted skills.

- [Current skill snapshot](skills/baseline/SKILL.md)
- [Experimental revision](skills/revision/SKILL.md)
- [Exact revision diff](revision.diff)
- [Optional shape reference](skills/revision/references/shape-language.md)
- [Frozen protocol](protocol.json)
- [Infrastructure and quota recovery](INFRASTRUCTURE.md)
- [Post-freeze observations](notes/post-freeze-observations.md)
- [Offline comparison page](index.html), once built

## The intervention

The revision requires two meaningfully different rendered compositions of a critical screen before fixing a direction or style system. It qualifies fixed novelty, color and surface limits while preserving priority, accessibility, honest state, native behavior and rendered verification. It adds one optional shape reference and explanatory SVG. The user’s preference for **Adjusted Squircle** is explicit when a soft continuous treatment is appropriate. No global shape default is introduced.

This is a bundled intervention. Two conditions cannot isolate the effect of composition exploration from the relaxed principles or optional reference. The main skill and prior eval outputs are untouched.

## Evaluation design

Same three original prompts from `../evals.json`, with identical production requirements and fixtures for both conditions. Two fresh runs per task and condition, twelve design jobs total. CLI model `gpt-6.1-sol`, high reasoning, maximum three concurrent jobs, twenty minutes active time per job including research/exploration/implementation/verification. Each workspace contains only the assigned skill, shared reference pack, fixed data and relevant raw task inputs. No conversation history, host skills, plugins, MCP, web access or other generated prototypes are supplied. This is context and workspace separation, not an assertion that filesystem reads are cryptographically confined; logs receive a read-boundary audit.

The baseline is an exact copy of the root `SKILL.md`, `references/` and `templates/`. All file hashes and the originating Git commit are recorded. The experimental revision was frozen before the first model execution. A pre-run amendment clarified that each workspace implements only its assigned task. No feedback about design quality is sent to generators.

The shared production contract makes screenshots comparable and supplies the same invented data. It adds explicit state hooks, offline constraints, viewports and required task paths to the original prompts. This improves within-iteration control, but this iteration is not a direct reproduction of iteration1’s unconstrained runs. All runs receive the same shared primary visual references, so the comparison tests revision behavior with reference access held constant.

## Service interruption

A CLI argument conflict rejected the first invocations before any model ran. Records remain under `infrastructure-attempt-1/`.

The account quota then interrupted three in-progress design jobs, while nine jobs failed before design work. Records and partial artifacts remain under `quota-segment-1/`. After the read-only account endpoint confirmed ordinary usage available, each job continued with its remaining active-time budget and the same frozen inputs. The three ephemeral sessions restore their existing workspace and visible trace, but hidden context is unavailable. The nine unstarted designs begin fresh. This is a real limitation, especially for repeat1, and must be considered separately from design quality. No credits or banked resets were consumed. No model or credential substitution occurred. See [recovery.json](recovery.json).

## Standard captures

Four runs per task produce **192 final PNGs**:

| Task | States | Sizes | Themes | Shots/run |
|---|---|---|---|---|
| Menu | main, compose, pending, offline, empty, accepted | Native360pxpopover within400×680scene | Light/dark | 12 |
| Dashboard | live, stale, surge | TV1920×1080, laptop1440×900 | Light/dark | 12 |
| Banking | welcome, details-error, code, code-error, help, done | 390×844,320×568 | Light/dark | 24 |

All use direct `?screen=…&theme=…&display=…` hooks, DPR1, en-GB, Europe/London, fixed2026-10-18T10:00Z and reduced motion. Capture blocks network requests, records console/runtime errors, checks PNG variance/dimensions and hashes outputs before/after. No generated output is repaired by the evaluator.

Functional evidence and visual judgment are separate. Token consistency, overflow and control checks do not establish personality or composition. Scripted controls that cannot be recognized by generic selectors receive manual-review status, not an automatic design failure. Real older-user usability, assistive technology behavior and native host integration need external testing.

## Files and execution

`tools/prepare.py` and `tools/freeze.py` created the snapshots and workspaces once before execution. They refuse an already-frozen protocol. Do not run them over this study.

`tools/runner.py` starts a never-attempted preregistered job and refuses replacement attempts. `tools/recover_quota.py` is the explicit one-time quota continuation, preserving prior segments and reducing remaining time; it is not a way to replace poor results. Normal CLI rollouts are now retained so a later service interruption can resume context.

All exact commands, JSONL events, status, timing and usage remain per-run in `runs/<task>/<condition>/run-N/`. The outputs are exact copied artifacts, excluding caches and node_modules. Initial prompts are retained with hashes.

For collection and report rebuilding, use Python3.11+, the existing `../scripts/requirements-compare.txt` dependencies and Playwright Chromium installed. Validation additionally used PyYAML6.0.3 in a temporary environment. From repo root:

```sh
/tmp/design-compare-venv/bin/python evals/iteration-3/tools/capture.py --all
/tmp/design-compare-venv/bin/python evals/iteration-3/tools/grade.py
/tmp/design-compare-venv/bin/python evals/iteration-3/tools/anonymize.py
/tmp/design-compare-venv/bin/python evals/iteration-3/tools/build_report.py
```

`capture.py --replace-capture` repeats collection from unchanged output only. It never reruns or fixes a design. Benchmark job attempts are not rerun by these commands. The account-limit check used only read-only account metadata, with official documentation at https://learn.chatgpt.com/docs/app-server .

## Adoption decision

The preregistered gate requires a stable overall preference for the revision on at least two tasks across both repeats, with no new critical functional, accessibility or coverage regression. This is a directional test with two repeats, not a significance test. Any account interruption and incomplete run must remain visible. Human review of the paired interfaces remains necessary before promotion.

No promotion or changes to the canonical skill are authorized by a preference score alone. The user will review the results and direction first.
