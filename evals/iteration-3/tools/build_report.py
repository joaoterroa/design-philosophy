#!/usr/bin/env python3
"""Embed collected evidence and main-agent assessments into an offline report.

No grading or output repairs occur here. It also builds a useful pending report
while generation/capture is in progress. Re-run after assessment.json changes.
"""
from __future__ import annotations

import argparse
import base64
from datetime import datetime, timezone
import json
import os
from pathlib import Path
from study_paths import artifact_path

STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[1]


def read_json(path, fallback):
    return json.loads(path.read_text()) if path.exists() else fallback


def relative(path, output):
    return Path(os.path.relpath(path, output.parent)).as_posix()


def build(study, output, assessment_path):
    protocol = json.loads((study / "protocol.json").read_text())
    prompts = {e["name"]: e["prompt"] for e in json.loads((REPO / "evals/evals.json").read_text())["evals"]}
    tasks = []
    for task in dict.fromkeys(r["task"] for r in protocol["runs"]):
        tasks.append({"id": task, "prompt": prompts.get(task, task)})
    pairs = {}
    all_shots = 0
    for record in protocol["runs"]:
        artifact = artifact_path(record, study)
        key = f"{record['task']}__{record['repeat']}"
        pair = pairs.setdefault(key, {"id": key, "task": record["task"], "repeat": record["repeat"], "runs": {}})
        capture = read_json(artifact / "capture.json", {})
        status = read_json(artifact / "status.json", {"state": "not started"})
        shots = {}
        for shot in capture.get("shots", []):
            image = artifact / shot["path"]
            row = {k: v for k, v in shot.items() if k not in ("metrics", "url")}
            metrics = shot.get("metrics", {})
            row["metrics"] = {k: metrics.get(k) for k in (
                "horizontalOverflow", "viewport", "app", "visibleItemCount", "fullyVisibleItemCount",
                "smallTargets", "fonts", "cornerShapes", "headings",
            )}
            if image.is_file():
                row["image"] = "data:image/png;base64," + base64.b64encode(image.read_bytes()).decode()
                all_shots += 1
            shots[shot["id"]] = row
        run = {
            "id": record["id"], "condition": record["condition"], "status": status,
            "shots": shots, "capture": {k: v for k, v in capture.items() if k != "shots"},
            "links": {
                "prototype": relative(artifact / "outputs/app/index.html", output),
                "design": relative(artifact / "outputs/DESIGN.md", output),
                "status": relative(artifact / "status.json", output),
                "capture": relative(artifact / "capture.json", output),
                "functional": relative(artifact / "functional.json", output),
                "events": relative(artifact / "events.jsonl", output),
            },
            "functional": read_json(artifact / "functional.json", {}),
            "hasPrototype": (artifact / "outputs/app/index.html").is_file(),
            "infrastructureAttempts": len(list(artifact.glob("infrastructure-attempt-*"))),
        }
        # Source status retains logs and hashes. Report needs audit summaries,
        # not duplicate every initial file hash and multi-kilobyte command.
        run["status"] = {k: v for k, v in status.items() if k not in ("initialFiles", "command")}
        pair["runs"][record["condition"]] = run
    assessment = read_json(assessment_path, {
        "headline": "Assessment pending", "summary": "The report will show the recorded assessment after capture and review.",
        "recommendation": "No adoption recommendation has been made.", "taskResults": [], "limitations": [],
    })
    data = {
        "studyId": "design-philosophy-iteration-3-controlled" if study.name == "controlled" else "design-philosophy-iteration-3-pilot",
        "generatedAt": datetime.now(timezone.utc).isoformat(), "tasks": tasks,
        "pairs": sorted(pairs.values(), key=lambda p: ([t["id"] for t in tasks].index(p["task"]), p["repeat"])),
        "assessment": assessment, "protocol": protocol, "recovery": read_json(study / "recovery.json", None),
        "capturedShots": all_shots, "expectedShots": protocol.get("design", {}).get("finalScreenshotsExpected", 192),
        "links": {
            "protocol": relative(study / "protocol.json", output),
            "baseline": relative(study / "skills/baseline/SKILL.md", output),
            "revision": relative(study / "skills/revision/SKILL.md", output),
            "diff": relative(study / "revision.diff", output),
            "shape": relative(study / "skills/revision/references/shape-language.md", output),
            "references": relative(study / "inputs/common/reference-pack/SOURCES.md", output),
            "assessment": relative(assessment_path, output),
            "findings": relative(study / "FINDINGS.md", output),
        },
    }
    template = (Path(__file__).parent / "report-template.html").read_text()
    encoded = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    if template.count("__REPORT_DATA__") != 1:
        raise ValueError("Expected exactly one report data placeholder")
    output.write_text(template.replace("__REPORT_DATA__", encoded))
    print(f"Built {output}: {len(pairs)} pairs, {all_shots}/{data['expectedShots']} embedded PNGs, {output.stat().st_size:,} bytes")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--study", type=Path, default=STUDY)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--assessment", type=Path)
    args = parser.parse_args()
    study = args.study.resolve()
    build(study, args.output.resolve() if args.output else study / "index.html",
          args.assessment.resolve() if args.assessment else study / "assessment.json")


if __name__ == "__main__":
    main()
