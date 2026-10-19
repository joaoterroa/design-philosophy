# Browser Company sensibility study

Open **[index.html](index.html)** directly from disk. Images and three short official demo excerpts are embedded, so the report works offline. Live experiments link to separate local app copies. No original eval output, skill, reference or template is modified.

The report contains direct visual comparisons, a gap analysis separated into philosophy/translation/execution, counterevidence, four controlled CSS probes, measurements and prioritized proposals. It distinguishes actual help screenshots, sampled product demonstrations, isolated component presentations and staged product-output imagery. It does not claim an authenticated inspection of current Dia or a user preference study.

## Principal finding

The skill specifies how to avoid many mistakes more concretely than it specifies how to choose a strong visual direction. Some conditional source ideas became universal restraint rules; reference study can pass with verbal principles; a first defensible composition can become a guarded system before a rendered alternative tests it. This plausibly narrows character, but these runs cannot isolate the causal contribution of individual instructions.

There is successful product judgment to preserve: responsibility remains honest until a handover is accepted, banking's message preview avoids a usable example code, and the dashboard's hierarchy follows operational priorities. The task is to improve visual calibration and exploration, not to add a Dia skin.

## Experiment results

All changes use separate copies of the **with-skill** prototypes. Application logic, data, words, fonts and palettes are unchanged. CSS overrides are intentionally small and are not production-ready token-system patches.

| Probe | Result | Limit |
| --- | --- | --- |
| Menu type | Main duty answer changes from 15 to 22 px; normal panel 388 → 396 px. All four tested states fit. | Clearer focal hierarchy is an editorial judgment; no independent preference or speed result. |
| Menu object | Adds an inset responsibility surface on top of the same type change; normal panel 388 → 405 px. | Does not establish a stronger identity. The type-only control prevents crediting the card for every difference. |
| Banking message | Removes the preview's outer wrapper. At 390 px, safety headline top 817.2 → 789.2 px and bottom 874.2 → 817.7 px; Continue remains at the same position. | Only the full headline enters the 844 px viewport. The full warning still scrolls. At 320 × 568 it remains below the fold; error/help states do not get the same above-fold result. |
| Dashboard separation | Normal TV still fits seven incidents; busy TV visibility changes eight → seven. Laptop retains all twelve surge incidents in its scrollable page. | A coverage trade-off, not evidence that all cards are bad. Reject this as a universal transfer. |

These validate narrow mechanisms and trade-offs, not Browser Company likeness or a revised skill. See [all measurements](experiments/results.json). There are 40 controlled pairs / 80 PNGs, including light and dark, both phone sizes, and both dashboard sizes. A later skill evaluation would need fresh runs and independent preference/task judgments after the proposed edits are reviewed.

## Evidence and editable sources

- [study.json](study.json): findings, confidence, local evidence links and recommendations.
- [Independent primary research](evidence/primary-research.md): dated sources, observed details, descriptions versus interpretations and counterexamples.
- [Image catalog](evidence/catalog.json): exact source URLs, provenance, dimensions and SHA-256 hashes for the 21 selected reference images.
- `evidence/assets/`: published images, short demo excerpts and sampled frames. The downloaded article's non-product artwork was excluded.
- `evidence/research-assets/`: additional first-party images and timed frames used in the independent research.
- [Experiment manifest](experiments/manifest.json): hypothesis, exact intervention and hashes of the copied original files.
- `experiments/<probe>/app/experiment.css`: exact override. Other app files remain identical to the source, except the stylesheet link in `index.html`.
- `tools/report-template.html` and `tools/build_report.py`: editable report source and offline embedding step.

The first-party material remains attributable to its respective owners and is included as evidence for this comparison, not as reusable design assets. The experimental apps do not use Browser Company artwork, branding or code.

## Reproduce from the repository root

Use Python 3.11+ with the iteration-1 comparison dependencies and Playwright Chromium installed (Pillow 13 requires Python 3.11):

```sh
python3 -m venv /tmp/design-compare-venv
/tmp/design-compare-venv/bin/pip install -r evals/scripts/requirements-compare.txt
/tmp/design-compare-venv/bin/python -m playwright install chromium
/tmp/design-compare-venv/bin/python evals/iteration-2/browser-company-study/tools/build_experiments.py
/tmp/design-compare-venv/bin/python evals/iteration-2/browser-company-study/tools/capture_experiments.py
/tmp/design-compare-venv/bin/python evals/iteration-2/browser-company-study/tools/build_report.py
/tmp/design-compare-venv/bin/python evals/iteration-2/browser-company-study/tools/verify_report.py
```

Dependency installation needs the network once. All capture, report-building and verification steps use the local evidence and prototypes. Capture blocks HTTP/HTTPS requests. The included first-party assets are already downloaded; source dates and URLs are recorded so they can be checked independently. The video excerpts were fetched from the public Mux playback IDs linked in the official release pages, downscaled to 1280 px, without audio; screenshots retain their source crops. Exact local video provenance is in [video-provenance.json](evidence/video-provenance.json).

For page QA, add `--screenshots /tmp/browser-study-qa` to `verify_report.py`. Browser/platform rasterization can change pixels; before/after claims must use the same environment. The earlier dashboard DESIGN.md's surge row count differs from this machine's contemporaneous original capture, so the experiment uses the same-run comparison rather than repeating that historic count.

The report's optional visual preferences are stored locally where the browser permits it and exported as JSON. Hidden labels conceal original/revision attribution and the experiment assessment in that panel; reading the surrounding report can still prime judgment. These controls are for review, not a claim of an unbiased study.
