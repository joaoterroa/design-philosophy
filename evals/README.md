# Evals

Prompts and results for checking that the skill changes how agents design, not just what they say.

```
evals/
├── evals.json                 # the test prompts and their assertions
├── fixtures/                  # input files a prompt refers to (e.g. the dashboard to redesign)
├── scripts/grade_auto.py      # scripted checks over a run's outputs (tokens, dark mode, screenshots…)
└── iteration-N/
    ├── FINDINGS.md            # what the iteration showed, caveats, proposed skill edits
    ├── benchmark.{json,md}    # pass rate, time, tokens per configuration
    ├── review.html            # static review page (write-ups and grades)
    └── <eval-name>/
        ├── eval_metadata.json # prompt + assertions
        ├── with_skill/        # outputs/ (DESIGN.md, app/, screenshots/…), grading.json, timing.json
        └── without_skill/     # same, from the run without the skill
```

Each `outputs/app/index.html` opens directly in a browser. Most prototypes switch states with a URL parameter or an on-page control; see each run's `DESIGN.md`.

## Comparable screenshots in iteration 1

Screenshot names differ between runs. These pairs show the same screen and state:

| Eval | Screen | with_skill | without_skill |
| --- | --- | --- | --- |
| oncall-menubar | On call, main panel | `oncall-light.png` / `-dark` | `02-on-light.png` / `-dark` |
| oncall-menubar | Composing a handover | `compose-light.png` | `03-choose-light.png` |
| oncall-menubar | Waiting for acceptance | `pending-light.png` | `04-pending-light.png` |
| oncall-menubar | Offline | `offline-light.png` | `08-offline-light.png` |
| incident-dashboard | TV, live with SEV1 | `wall-live-dark.png` | `tv-sev1-no-commander.png` |
| incident-dashboard | TV, data stale | `wall-stale-dark.png` | `tv-stale.png` |
| incident-dashboard | Laptop, live | `desk-live-light-1440.png` | `laptop-sev1-light.png` |
| incident-dashboard | Original (before) | `before/` | `original-1920.png` |
| banking-onboarding | Welcome | `390-light--welcome.png` | `01-welcome.png` |
| banking-onboarding | Account details with errors | `390-light--details-errors.png` | `04-details-errors.png` |
| banking-onboarding | Enter the texted code | `390-light--code.png` | `11-code.png` |
| banking-onboarding | Done | `390-light--done.png` | `20-done.png` |

## Side-by-side comparison

Open [`iteration-1/compare/index.html`](iteration-1/compare/index.html) directly from disk. It has matched-scale screenshots, light/dark switching, blind left/right randomisation, per-pair reveal, live prototype links, and browser-saved choices with JSON export. There are 89 screen/size combinations and 262 PNGs, including one-sided states and the shared original dashboard. The [capture inventory](iteration-1/compare/README.md) lists all mappings and limitations.

To recapture or verify from the repo root (Python 3.10+):

```sh
python3 -m venv /tmp/design-compare-venv
/tmp/design-compare-venv/bin/pip install -r evals/scripts/requirements-compare.txt
/tmp/design-compare-venv/bin/python -m playwright install chromium
/tmp/design-compare-venv/bin/python evals/scripts/capture_pairs.py
/tmp/design-compare-venv/bin/python evals/scripts/verify_compare.py
```

Capture blocks network requests and reads the original run outputs without modifying them. Phone/dashboard shots use the fixed viewport, not full-page height; popovers retain their native widths. Fonts and fixture data are preserved, so different invented content and the baseline font fallback remain comparison limits. Two baselines used the Recall design system (see `iteration-1/FINDINGS.md`).

## Running a new iteration

- Keep baseline runs away from any of the user's own design documents (iteration 1's baselines found one and used it; see its FINDINGS).
- Give both configurations identical prompts, inputs, time budget and deliverables, including a fixed list of screens and states to screenshot at fixed sizes and names, so results can be compared side by side.
- Grade with assertions that can fail for a good baseline, and add a blind preference judgement of paired screenshots.

## Experimental skill comparison

[Iteration 3](iteration-3/controlled/index.html) compares the preserved current skill with a separate experimental revision: three tasks, two runs per condition, twelve completed designs and 192 matched screenshots. The [findings](iteration-3/controlled/FINDINGS.md) recommend keeping the current baseline: menus improve consistently, dashboards favor the current skill, and banking is mixed. The canonical skill is unchanged. The earlier cross-task pilot is excluded in full.

The [shape study](iteration-2/shape-study/index.html) preserves the Adjusted Squircle preference as an optional visual treatment; the controlled revision contains that reference, but none of its final apps implements continuous corners.
