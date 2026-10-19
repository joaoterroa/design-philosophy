#!/usr/bin/env python3
"""Rebuild isolated visual experiments; never changes the source eval outputs.

These are controlled probes, not proposed production designs. All data, copy,
semantic controls and application logic are copied unchanged. The only added
behaviour is an experiment stylesheet loaded after the original styles.
"""

from hashlib import sha256
import json
from pathlib import Path
import shutil

STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[2]

EXPERIMENTS = {
    "menu-type": dict(
        evaluation="oncall-menubar",
        hypothesis="A stronger type hierarchy can give duty status a focal point without new mechanics or branding.",
        change="Only the answer's type size, line height and tracking change. Same text, color, panel width and controls.",
        css="""/* A: type hierarchy alone. Keep the operating-system font and original palette. */
.you .answer { font-size: 22px; line-height: 28px; letter-spacing: -.45px; font-weight: 600; }
""",
    ),
    "menu-object": dict(
        evaluation="oncall-menubar",
        hypothesis="A persistent responsibility object can distinguish personal duty from the roster without tinting every person or weakening pending status.",
        change="The same type intervention as menu-type, plus a neutral inset surface grouping existing shift information; no content or controls added or removed.",
        css="""/* B: add a responsibility object to A. No people-by-color encoding. */
.you .answer { font-size: 22px; line-height: 28px; letter-spacing: -.45px; font-weight: 600; }
.you { margin: 10px 10px 8px; padding: 12px; border-radius: 12px;
  background: var(--window); box-shadow: 0 1px 3px #00000012, inset 0 0 0 1px var(--separator); }
.you + .now-list { border-top: 0; padding-top: 4px; }
.you .strip-track { border-radius: 6px; }
""",
    ),
    "bank-message": dict(
        evaluation="banking-onboarding",
        hypothesis="Removing the redundant wrapper around an already useful message object can improve rhythm and expose safety advice sooner without shrinking type or removing help.",
        change="Remove the outer filled preview panel and its padding; retain the actual SMS bubble, all words, controls, field order and type sizes. Tighten only preview spacing and widen its existing message object.",
        css="""/* C: the SMS is the object. It does not need another card around it. */
.preview { background: transparent; border-radius: 0; padding: 0; margin-top: 20px; }
.preview-title { margin-bottom: 12px; }
.message { margin-right: 0; }
.message-status { margin-bottom: 12px; }
""",
    ),
    "dashboard-separation": dict(
        evaluation="incident-dashboard",
        hypothesis="Giving incident rows more independent object-like separation may improve perceived grouping, but must not cost TV coverage.",
        change="Add rounded surfaces, horizontal inset and 12px inter-row gaps to the existing incident rows. Brand colors, fonts, information, row sorting and overflow logic are unchanged. Deliberately tests the cost of exporting object treatment to a dense wall board.",
        css="""/* D: separation probe. Reject if it reduces the wall's seven-row budget. */
#open-list > li { margin-bottom: 12px; }
#open-list .row { background: var(--surface); border-radius: 12px; padding-left: 12px; padding-right: 12px; }
""",
    ),
}


def build():
    records = []
    for name, experiment in EXPERIMENTS.items():
        source = REPO / "evals/iteration-1" / experiment["evaluation"] / "with_skill/outputs/app"
        target = STUDY / "experiments" / name / "app"
        target.mkdir(parents=True, exist_ok=True)
        hashes = {}
        for path in source.rglob("*"):
            if not path.is_file():
                continue
            relative = path.relative_to(source)
            destination = target / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, destination)
            hashes[relative.as_posix()] = sha256(path.read_bytes()).hexdigest()
        index = target / "index.html"
        index.write_text(index.read_text().replace("</head>", '<link rel="stylesheet" href="experiment.css">\n</head>'))
        (target / "experiment.css").write_text(experiment["css"])
        records.append(dict(id=name, **{k:v for k,v in experiment.items() if k != "css"},
                            source=source.relative_to(REPO).as_posix(), sourceHashes=hashes))
    (STUDY / "experiments/manifest.json").write_text(json.dumps(records, indent=2) + "\n")
    print(f"Built {len(records)} experiments from unchanged source apps.")


if __name__ == "__main__":
    build()
