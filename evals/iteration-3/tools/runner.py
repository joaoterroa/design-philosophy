#!/usr/bin/env python3
"""Run each preregistered design once, in a fresh isolated Codex session.

No evaluation runs occur without --run ID or --all. --dry-run validates inputs
and prints the exact command. Failed or interrupted runs are never replaced.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import shutil
import signal
import subprocess
import threading
import time

STUDY = Path(__file__).resolve().parents[1]
REPO = STUDY.parents[1]
CODEX = "/Users/joao.terroa/.local/bin/codex"
PYTHON = "/private/tmp/design-compare-venv/bin/python"
PRINT_LOCK = threading.Lock()
DISABLED = (
    "plugins", "apps", "multi_agent", "multi_agent_v2", "memories",
    "hooks", "skill_search", "skill_mcp_dependency_install",
    "browser_use", "browser_use_external", "computer_use", "in_app_browser",
    "image_generation", "workspace_dependencies", "remote_plugin",
    "external_agent_memory_import", "agent_message_board", "chronicle",
)


def now():
    return datetime.now(timezone.utc).isoformat()


def say(message):
    with PRINT_LOCK:
        print(message, flush=True)


def write_json(path, data):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, indent=2) + "\n")
    temporary.replace(path)


def tree_hash(path):
    """Hash names + exact bytes; this definition is recorded alongside each run."""
    digest = hashlib.sha256()
    for file in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(file.relative_to(path).as_posix().encode() + b"\0")
        digest.update(file.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_path(value, protocol):
    path = Path(value)
    if path.is_absolute():
        return path
    # Repo-relative paths begin evals/; other paths are protocol-relative.
    return (REPO if path.parts and path.parts[0] == "evals" else protocol.parent) / path


def command_for(workspace, artifact, codex=CODEX):
    command = [codex, "exec", "--ignore-user-config",
               "--skip-git-repo-check", "--json", "--color", "never",
               "--model", "gpt-6.1-sol",
               "--approve-for-me", "--cd", str(workspace),
               "--output-last-message", str(artifact / "final.md"),
               "--enable", "skip_host_skill_discovery"]
    for feature in DISABLED:
        command += ["--disable", feature]
    # Ignore host hooks, skills, apps and MCP configuration. Preserve safety
    # execpolicy rules and automatic approval review. Shell tools
    # inherit no secrets. Authentication is handled by Codex, never copied here.
    config = [
        'model_reasoning_effort="high"', 'web_search="disabled"',
        'mcp_servers={}', 'sandbox_workspace_write.network_access=false',
        'shell_environment_policy.inherit="none"',
        'shell_environment_policy.set={PATH="/private/tmp/design-compare-venv/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"}',
        'shell_environment_policy.experimental_use_profile=false',
        'project_doc_max_bytes=0',
    ]
    for value in config:
        command += ["-c", value]
    return command + ["-"]


def validate(record, protocol):
    specification = json.loads(protocol.read_text())
    executor = specification.get("executor", {})
    for key, required in (("model", "gpt-6.1-sol"), ("reasoningEffort", "high"),
                          ("network", False), ("hostSkills", False)):
        if key in executor and executor[key] != required:
            raise ValueError(f"Frozen executor {key} is not the required {required!r}")
    workspace = resolve_path(record["workspace"], protocol).resolve()
    artifact = resolve_path(record["artifactDir"], protocol).resolve()
    if not (workspace / "PROMPT.md").is_file():
        raise ValueError(f"{record['id']}: missing PROMPT.md")
    skill = workspace / "skill"
    if not (skill / "SKILL.md").is_file():
        raise ValueError(f"{record['id']}: missing skill/SKILL.md")
    if any(p.is_symlink() for p in workspace.rglob("*")):
        raise ValueError(f"{record['id']}: workspace contains symlinks")
    initial_files = {
        p.relative_to(workspace).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in sorted(workspace.rglob("*")) if p.is_file()
    }
    expected_files = record.get("initialFiles")
    if expected_files is not None and ((not record.get("quotaRecovery") and initial_files != expected_files) or any(initial_files.get(name) != value for name,value in expected_files.items())):
        differing = sorted(set(initial_files) ^ set(expected_files) | {
            name for name in set(initial_files) & set(expected_files)
            if initial_files[name] != expected_files[name]})
        raise ValueError(f"{record['id']}: initial files differ from frozen protocol: {differing}")
    if record.get("quotaRecovery"):
        initial_files = {name:initial_files[name] for name in expected_files}
    prompt_hash = initial_files["PROMPT.md"]
    if record.get("promptSha256", prompt_hash) != prompt_hash:
        raise ValueError(f"{record['id']}: prompt differs from frozen protocol")
    expected_skill_files = specification.get("skillHashes", {}).get(record["condition"])
    if expected_skill_files is not None:
        actual_skill_files = {name.removeprefix("skill/"): value for name, value in initial_files.items()
                              if name.startswith("skill/")}
        if actual_skill_files != expected_skill_files:
            raise ValueError(f"{record['id']}: skill files differ from frozen condition hashes")
    actual_hash = tree_hash(skill)
    expected_hash = record.get("skillTreeSha256")
    if expected_hash and actual_hash != expected_hash:
        raise ValueError(f"{record['id']}: skill tree differs from protocol")
    return workspace, artifact, actual_hash, initial_files


def boundary_audit(event, workspace):
    """Flag apparent external file references for human audit; never block tools.

    This scans logged shell commands, not the agent's actual filesystem reads.
    Runtime libraries/browser caches are allowed. A path in a script string can
    be a false positive; no finding here is proof of a read or contamination.
    """
    commands = []

    def collect(value):
        if isinstance(value, dict):
            for key, child in value.items():
                if key in ("command", "cmd") and isinstance(child, str):
                    commands.append(child)
                elif key not in ("aggregated_output", "output", "text"):
                    collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(event)
    allowed = (str(workspace) + "/", "/private/tmp/design-compare-venv/", "/tmp/design-compare-venv/",
               "/Users/joao.terroa/Library/Caches/ms-playwright/", "/opt/homebrew/", "/usr/",
               "/bin/", "/sbin/", "/System/", "/Library/Frameworks/", "/dev/", "/Applications/Google Chrome.app/",
               "/private/var/folders/", "/var/folders/")
    pattern = r"(?:~/(?:[^\s'\"`;),<>]+)|/(?:Users|private|tmp|var|home)/[^\s'\"`;),<>]+|\$\{?HOME\}?(?:/[^\s'\"`;),<>]+)?)"
    found = []
    for command in commands:
        for match in re.finditer(pattern, command):
            path = match.group().rstrip(".:]}")
            if path != str(workspace) and not path.startswith(allowed):
                found.append({"pathReference": path[:220], "eventType": event.get("type")})
        if re.search(r"(?:^|[\s'\"])(?:\.\./){2,}", command):
            found.append({"pathReference": "two-or-more parent-directory traversal segments", "eventType": event.get("type")})
    return found


def run_one(record, protocol, args):
    workspace, artifact, skill_hash, initial_files = validate(record, protocol)
    command = command_for(workspace, artifact, args.codex)
    if record.get("resumeThreadId"):
        command = command[:-1] + ["resume", record["resumeThreadId"], "-"]
    if args.dry_run:
        say(json.dumps({"id": record["id"], "command": command,
                        "stdin": str(workspace / "PROMPT.md"), "skillTreeSha256": skill_hash}))
        return True
    artifact.mkdir(parents=True, exist_ok=True)
    # O_EXCL is also an inter-process lock. A partial launch is an attempt.
    try:
        lock = os.open(artifact / "attempt.lock", os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    except FileExistsError:
        raise RuntimeError(f"{record['id']}: an attempt already exists; refusing replacement")
    with os.fdopen(lock, "w") as handle:
        handle.write(now() + "\n")
    prompt = (workspace / "PROMPT.md").read_bytes()
    if record.get("quotaRecoveryPrompt"):
        prompt = (record["quotaRecoveryPrompt"].encode() if record.get("resumeThreadId")
                  else prompt + ("\n\n" + record["quotaRecoveryPrompt"]).encode())
    status = {
        "id": record["id"], "task": record["task"], "condition": record["condition"],
        "repeat": record["repeat"], "startedAt": now(), "state": "running",
        "model": "gpt-6.1-sol", "reasoningEffort": "high", "command": command,
        "workspace": str(workspace), "promptSha256": hashlib.sha256(prompt).hexdigest(),
        "initialFiles": initial_files,
        "skillTreeSha256": skill_hash,
        "skillHashDefinition": "sha256(sorted relative UTF-8 path + NUL + file bytes + NUL)",
        "timeoutSeconds": args.timeout_seconds,
        "quotaRecovery": record.get("quotaRecovery",False),
        "priorElapsedSeconds": record.get("priorElapsedSeconds",0),
        "contextRecovery": record.get("contextRecovery","fresh"),
    }
    write_json(artifact / "status.json", status)
    (artifact / "command.json").write_text(json.dumps(command, indent=2) + "\n")
    (artifact / "command.txt").write_text(shlex.join(command) + " < PROMPT.md\n")
    shutil.copyfile(workspace / "PROMPT.md", artifact / "prompt.md")
    started = time.monotonic()
    say(f"START {record['id']}")
    process = None
    try:
        with (artifact / "events.jsonl").open("wb") as out, (artifact / "stderr.log").open("wb") as err:
            process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err,
                                       cwd=workspace, start_new_session=True)
            process.stdin.write(prompt)
            process.stdin.close()
            next_progress = started + 30
            while process.poll() is None:
                elapsed = time.monotonic() - started
                if elapsed > args.timeout_seconds:
                    status["state"] = "timeout"
                    os.killpg(process.pid, signal.SIGTERM)
                    try:
                        process.wait(timeout=10)
                    except subprocess.TimeoutExpired:
                        os.killpg(process.pid, signal.SIGKILL)
                        process.wait()
                    break
                if time.monotonic() >= next_progress:
                    say(f"RUNNING {record['id']} {int(elapsed)}s")
                    next_progress = time.monotonic() + 30
                time.sleep(1)
            status["exitCode"] = process.returncode
            if status["state"] == "running":
                status["state"] = "completed" if process.returncode == 0 else "failed"
    except BaseException as error:
        status["state"] = "interrupted" if isinstance(error, KeyboardInterrupt) else "failed"
        status["runnerError"] = str(error)
        if process and process.poll() is None:
            os.killpg(process.pid, signal.SIGTERM)
            process.wait(timeout=10)
    finally:
        status["finishedAt"] = now()
        status["segmentElapsedSeconds"] = round(time.monotonic() - started,3)
        status["elapsedSeconds"] = round(status["segmentElapsedSeconds"]+record.get("priorElapsedSeconds",0),3)
        status["skillTreeSha256After"] = tree_hash(workspace / "skill")
        status["inputSkillUnchanged"] = status["skillTreeSha256After"] == skill_hash
        changed_inputs = []
        for name, expected in initial_files.items():
            path = workspace / name
            actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
            if actual != expected:
                changed_inputs.append({"path": name, "before": expected, "after": actual})
        status["originalInputsModified"] = bool(changed_inputs)
        status["changedOriginalInputs"] = changed_inputs
        output = workspace / "outputs"
        if output.is_dir():
            shutil.copytree(output, artifact / "outputs", ignore=shutil.ignore_patterns(
                "__pycache__", ".pytest_cache", "node_modules", ".DS_Store", "*.pyc"))
        status["hasApp"] = (artifact / "outputs/app/index.html").is_file()
        status["hasDesign"] = (artifact / "outputs/DESIGN.md").is_file()
        status["usage"] = []
        status["logReadBoundaryAudit"] = {
            "method": "Informational shell-command path scan; not proof of actual reads; runtime paths excluded",
            "findings": [],
        }
        event_path = artifact / "events.jsonl"
        if event_path.exists():
            for line in event_path.read_text(errors="replace").splitlines():
                try:
                    event = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if event.get("usage"):
                    status["usage"].append(event["usage"])
                status["logReadBoundaryAudit"]["findings"].extend(boundary_audit(event, workspace))
                if event.get("type") in ("error", "turn.failed"):
                    status.setdefault("agentErrors", []).append(event)
        status["completeArtifact"] = (status["state"] == "completed" and status["hasApp"]
                                      and status["hasDesign"] and status["inputSkillUnchanged"])
        write_json(artifact / "status.json", status)
    say(f"END {record['id']} {status['state']} {status['elapsedSeconds']}s app={status['hasApp']}")
    return status["completeArtifact"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--protocol", type=Path, default=STUDY / "protocol.json")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--run", action="append", help="Run ID; repeat to select several")
    group.add_argument("--all", action="store_true")
    parser.add_argument("--jobs", type=int, choices=(1, 2, 3), default=3)
    parser.add_argument("--timeout-seconds", type=int, default=1200)
    parser.add_argument("--codex", default=CODEX)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    args.protocol = args.protocol.resolve()
    protocol = json.loads(args.protocol.read_text())
    if args.timeout_seconds != protocol.get("executor", {}).get("timeoutSeconds", 1200):
        parser.error("The timeout must equal the frozen protocol's 1200-second budget")
    if args.jobs > protocol.get("executor", {}).get("maxConcurrent", 3):
        parser.error("Concurrency exceeds the frozen protocol")
    records = protocol["runs"]
    if not args.all:
        unknown = set(args.run) - {r["id"] for r in records}
        if unknown:
            parser.error(f"Unknown IDs: {sorted(unknown)}")
        records = [r for r in records if r["id"] in args.run]
    # Validate the entire selected set before starting any fresh sessions.
    for record in records:
        validate(record, args.protocol)
    good = True
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = {executor.submit(run_one, r, args.protocol, args): r["id"] for r in records}
        for future in as_completed(futures):
            try:
                good = future.result() and good
            except Exception as error:
                say(f"ERROR {futures[future]}: {error}")
                good = False
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
