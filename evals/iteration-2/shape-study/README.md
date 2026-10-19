# Shape language study

Open [index.html](index.html) directly from disk. It embeds all reference images, full captures and enlarged corner details. No server or build step is needed to read it. It includes the evidence, a radius-versus-curve illustration, controlled comparisons, optional hidden-label review with JSON export, and a concrete next-iteration proposal.

The skill, its references/templates and original evaluation outputs remain unchanged. All experiments are separate copies under this directory. No new evaluation agents ran. These files remain research proposals, not a skill revision.

## Findings

Rounded geometry recurs in nine selected actual product views from six first-party publications, with two additional published component closeups. This is a targeted sample, not a product-wide adoption rate. The images show a mix of soft panels, compact rounded controls, capsules, circles and compound tab/popover outlines. The precise Dia/Arc corner formula is unconfirmed. Dia explicitly mentioned platform-specific window/menu radius refinements for Tahoe in its January 23, 2026 release notes, scheduled for the next release; accompanying demos must not be treated as proof of that final treatment.

The current skill already asks for appropriate shape/space choices. Its examples use conventional `border-radius`; the experiments distinguish corner extent from curve family. CSS `squircle` is an experimental proxy here, not a reconstruction of Apple or Dia geometry.

The stronger next step is a small process-first skill proposal: compare two distinct rendered compositions before fixing the style system, qualify the few absolute rules that obstruct choice, and keep continuous geometry as an optional visual treatment. After user agreement, test the process revision with isolated, repeated runs. The report states the bounded evaluation and decision gate. Do not treat its proposal as authorization to modify the skill or run that evaluation.

## Experiments

A 2 × 2 comparison separates original/larger corner extent and ordinary/squircle curve:

| Variant | Extent | Curve |
|---|---|---|
| Original | Existing | Conventional quarter-circle for these uniform radius corners |
| Curve only | Existing | CSS squircle |
| Radius only | Existing × 1.840896... | Conventional |
| Adjusted squircle | Existing × 1.840896... | CSS squircle |

The multiplier matches the diagonal inset of an unclamped circular corner and exponent-four corner. It does not equalize area or perceived softness, and is not a recommended design token. Small dashboard bars can constrain the radius, as documented in the report.

Ten cases × light/dark × four variants = **80 full PNGs**, plus 80 corner detail crops:

- Menu at native 340px width: on call, composing handover, pending acceptance. Only the popover silhouette changes; controls and shift strip are unchanged.
- Banking: code entry at 390 × 844 and 320 × 568, wrong code at 390 × 844, help sheet at 390 × 844. Existing button, input, panel, message and sheet corners change. The message asymmetry and square sheet bottom remain.
- Dashboard: live and busy TV at 1920 × 1080, live laptop at 1440 × 900. Only existing severity/data-end geometry changes. No new cards or row gaps.

All visible element bounding boxes, text, source logic, fonts and palettes remain identical. Normal/busy TV still shows seven/eight incidents. These interventions do not solve hierarchy, density or below-fold content. The adjusted curve is a subtle optional finish; larger conventional radii cause more obvious softening. This is an editorial visual assessment, not a measured preference win.

## Reproduce

From the repository root, use Python 3.11+ with the existing comparison requirements. If needed, install once:

```sh
python3 -m venv /tmp/design-compare-venv
/tmp/design-compare-venv/bin/pip install -r evals/scripts/requirements-compare.txt
/tmp/design-compare-venv/bin/python -m playwright install chromium
```

Then run:

```sh
/tmp/design-compare-venv/bin/python evals/iteration-2/shape-study/tools/capture.py
/tmp/design-compare-venv/bin/python evals/iteration-2/shape-study/tools/build_report.py
/tmp/design-compare-venv/bin/python evals/iteration-2/shape-study/tools/verify.py
```

Capture requires `corner-shape: squircle` support and fails if unsupported. Tested with Playwright headless Chromium 156.0.8078.4. Unsupported browsers can read the report screenshots and SVG diagram; live experiment copies degrade to ordinary rounded corners. Production curve, outline, hit-test and resizing support needs separate platform verification.

Capture and report verification block HTTP/HTTPS requests. They use frozen time, DPR 1, en-GB, Europe/London, reduced motion and identical local fonts. The report builder reuses the exact local primary images from the previous `browser-company-study/`; source hashes verify identity. No downloads are needed to reproduce once those local evidence assets and Chromium are present.

The verifier checks all 80 PNGs for dimensions and non-uniform pixels, checks hashes and copied app contents, checks unchanged protected files, exercises all full-image comparison combinations, tests random order/hide/reveal, image zoom/Escape, saved preferences and both JSON exports, and checks responsive layout in both report themes at 1440, 1280 and 390px. It saves visual QA screenshots outside the repo in `/tmp/shape-study-qa/`. Capture separately exercises menu handover, banking code/error/help and keyboard focus.

Review choices use localStorage where available. Hidden labels hide variant attribution and assessment for the current comparison, but surrounding text can prime judgment. The review tool is not an independent blind preference study.

## Evidence and sources

- [Primary research](evidence/primary-research.md): first-party findings, platform evidence, definitions and limits.
- [Image catalog](evidence/catalog.json): source URLs/dates, hashes, observations and exact detail-crop bounds. Primary full images remain in the previous study; crops are stored here.
- [Experiment manifest](experiments/manifest.json): source hashes and exact selectors/radii.
- `experiments/<eval>/<variant>/app/shape.css`: exact CSS overrides; application code/data unchanged apart from the stylesheet link.
- [Results](experiments/results.json): all box/content/target/corner measurements and image hashes.
- [Verification](verification.json): browser verification results.
- `tools/report-template.html`: editable report.

First-party product images are included for evidence and retain their owners' attribution. No Browser Company artwork, assets or source code are used in the experimental interfaces.
