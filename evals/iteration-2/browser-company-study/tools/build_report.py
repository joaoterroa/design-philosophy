#!/usr/bin/env python3
"""Embed the study, original reference media and controlled captures in one HTML."""
import base64
import json
import mimetypes
from pathlib import Path

STUDY = Path(__file__).resolve().parents[1]


def main():
    study = json.loads((STUDY / "study.json").read_text())
    catalog = json.loads((STUDY / "evidence/catalog.json").read_text())
    results = json.loads((STUDY / "experiments/results.json").read_text())
    experiments = json.loads((STUDY / "experiments/manifest.json").read_text())
    videos = [
        dict(file="evidence/assets/dia-profiles-demo.mp4",title="Profile settings and creation",
             note="First 12 seconds; 23 January 2026. Source zoom and desktop backdrop retained.",
             source="https://www.diabrowser.com/release-notes/1-15-1-polish-galore"),
        dict(file="evidence/assets/dia-group-chat-demo.mp4",title="A work group becomes chat context",
             note="Official short demo; 15 January 2026. Original content/actions, downscaled to 1280 px.",
             source="https://www.diabrowser.com/release-notes/1-14-0-meeting-tab-groups"),
        dict(file="evidence/assets/dia-meeting-end-demo.mp4",title="A meeting group after the call",
             note="Official short demo; 15 January 2026. Captured sequence is not a timing measurement.",
             source="https://www.diabrowser.com/release-notes/1-14-0-meeting-tab-groups"),
    ]
    files = {"evidence/" + item["file"] for item in catalog}
    files.update(record["src"] for pair in results for record in pair["records"])
    files.update(video["file"] for video in videos)
    images = {}
    for file in sorted(files):
        mime = mimetypes.guess_type(file)[0]
        images[file] = f"data:{mime};base64," + base64.b64encode((STUDY / file).read_bytes()).decode()
    data = dict(study=study,catalog=catalog,results=results,experiments=experiments,videos=videos,images=images)
    payload = json.dumps(data,ensure_ascii=False,separators=(",",":")).replace("<", "\\u003c")
    template = (STUDY / "tools/report-template.html").read_text()
    assert template.count("__STUDY_DATA__") == 1
    (STUDY / "index.html").write_text(template.replace("__STUDY_DATA__",payload))
    print(f"Built offline report with {len(catalog)} reference images, {len(results)*2} captures and {len(videos)} demo excerpts.")


if __name__ == "__main__":
    main()
