"""Scripted checks for the design-philosophy evals. Prints JSON facts per run; judgement checks are graded by reading."""
import json
import re
import sys
from pathlib import Path

ITER = Path(sys.argv[1])
RECALL = re.compile(r"#(e61d30|d0192b|fbfbfa|891924)\b", re.I)


def texts(out: Path, exts):
    files = [p for p in (out / "app").rglob("*") if p.suffix in exts] if (out / "app").exists() else []
    return files, "\n".join(p.read_text(errors="ignore") for p in files)


def css_of(out: Path):
    files, blob = texts(out, {".css", ".html"})
    css = "\n".join(re.findall(r"<style[^>]*>(.*?)</style>", blob, re.S)) + "\n" + "\n".join(
        p.read_text(errors="ignore") for p in files if p.suffix == ".css")
    return css


def strip_token_blocks(css: str) -> str:
    """Remove :root / theme blocks (where tokens live) and media wrappers around them, then return the rest."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    out, i = [], 0
    pattern = re.compile(r"(:root|\[data-theme[^\]]*\]|\.theme-[\w-]+|html\[[^\]]*\]|html\.[\w-]+|body\.[\w-]+)\s*[^{]*\{")
    while True:
        m = pattern.search(css, i)
        if not m:
            out.append(css[i:]); break
        out.append(css[i:m.start()])
        depth, j = 1, m.end()
        while depth and j < len(css):
            depth += {"{": 1, "}": -1}.get(css[j], 0); j += 1
        i = j
    return "".join(out)


results = {}
for eval_dir in sorted(p for p in ITER.iterdir() if p.is_dir()):
    for cfg in ("with_skill", "without_skill"):
        out = eval_dir / cfg / "outputs"
        if not out.exists():
            continue
        css = css_of(out)
        _, js = texts(out, {".js", ".html"})
        rest = strip_token_blocks(css)
        literal = re.findall(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^)]*\d|hsla?\(", rest)
        all_files = [str(p.relative_to(out)) for p in out.rglob("*") if p.is_file()
                     and not str(p.relative_to(out)).startswith(("dashboard/", "brand/"))]
        everything = "\n".join((out / f).read_text(errors="ignore") for f in all_files
                               if Path(f).suffix in {".css", ".html", ".js", ".md", ".json"})
        results[f"{eval_dir.name}/{cfg}"] = {
            "design_md": (out / "DESIGN.md").exists(),
            "design_md_words": len((out / "DESIGN.md").read_text().split()) if (out / "DESIGN.md").exists() else 0,
            "screenshots": len(list((out / "screenshots").glob("*.png"))) if (out / "screenshots").exists() else 0,
            "dark_mode": bool(re.search(r"prefers-color-scheme:\s*dark|data-theme=.?dark|\[data-theme=\"?dark|\.dark\b|theme-dark", css + js)),
            "custom_properties": len(set(re.findall(r"--[\w-]+(?=\s*:)", css))),
            "literal_colours_outside_tokens": len(literal),
            "recall_palette_reused": sorted(set(m.lower() for m in RECALL.findall(everything))),
            "system_doc": [f for f in all_files if re.search(r"system|tokens", f, re.I) and f.endswith((".md", ".css", ".json"))],
            "guard_test": [f for f in all_files if re.search(r"test|guard|check", f, re.I) and f.endswith((".js", ".mjs", ".py"))],
            "brand_hex_used": sorted(set(h.lower() for h in re.findall(r"#(12355b|f26b21|2a9d8f|eef1f4|3d4852)\b", css, re.I))),
            "emoji_in_app": len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", js)),
            "gradient_count": len(re.findall(r"gradient\(", rest)),
            "files": len(all_files),
        }
print(json.dumps(results, indent=1))
