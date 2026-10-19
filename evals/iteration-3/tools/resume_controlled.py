#!/usr/bin/env python3
"""Resume quota-interrupted primary attempts, retaining sessions and cumulative budget.

Run only after a read-only rate-limit check confirms ordinary usage is available.
Completed, timed-out, and design-failed attempts are never retried.
"""
import argparse
import json
import math
import shutil
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
from types import SimpleNamespace
import runner

STUDY = Path(__file__).resolve().parents[1] / 'controlled'

def prepare(record, budget):
    artifact = Path(record['artifactDir'])
    status = json.loads((artifact / 'status.json').read_text())
    if status.get('completeArtifact'):
        return None
    if status['state'] != 'failed' or not any('usage limit' in json.dumps(e).lower() for e in status.get('agentErrors', [])):
        return None
    assert not status.get('originalInputsModified'), record['id']
    remaining = math.floor(budget - status['elapsedSeconds'])
    assert remaining > 0, record['id']
    events = [json.loads(line) for line in (artifact / 'events.jsonl').read_text().splitlines() if line.strip()]
    thread = next(e['thread_id'] for e in events if e.get('type') == 'thread.started')
    segment_number = 1
    while (artifact / f'quota-segment-{segment_number}').exists():
        segment_number += 1
    segment = artifact / f'quota-segment-{segment_number}'
    segment.mkdir()
    for name in ('attempt.lock', 'status.json', 'command.json', 'command.txt', 'events.jsonl', 'stderr.log', 'final.md', 'prompt.md', 'outputs', 'shots', 'capture.json', 'functional.json'):
        if (artifact / name).exists():
            shutil.move(artifact / name, segment / name)
    result = dict(record, quotaRecovery=True, priorElapsedSeconds=status['elapsedSeconds'], resumeThreadId=thread,
                  contextRecovery='exact saved session plus unchanged workspace; service quota interruption')
    result['quotaRecoveryPrompt'] = f'''Continue the same task from your saved context and existing files. The service interrupted the attempt because account usage was exhausted; ordinary usage is available again. No design feedback or new requirements have been supplied. Preserve the frozen skill, fixtures and original request. You have {remaining} seconds remaining from the original {budget}-second allowance. Finish the implementation, design rationale and checks; report unfinished checks honestly. Use normal approval review for sandbox escalations. Do not begin a new design or change supplied inputs.'''
    return result, remaining

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--confirmed-reset', action='store_true', required=True)
    args = parser.parse_args()
    protocol = STUDY / 'protocol.json'
    spec = json.loads(protocol.read_text())
    budget = spec['executor']['timeoutSeconds']
    # Preparation is just-in-time: unlaunched attempts retain their original records.
    queue = iter(spec['runs'])
    journal = {'reason': 'Service quota; ordinaryUsageAllowed=true confirmed before launch',
               'budget': f'{budget} seconds cumulative active process time per run',
               'preservedFrozenInputs': True, 'runs': []}
    if (STUDY / 'recovery.json').exists():
        journal = json.loads((STUDY / 'recovery.json').read_text())
    good = True
    stop = False
    with ThreadPoolExecutor(max_workers=3) as pool:
        active = {}
        while True:
            while not stop and len(active) < 3:
                try:
                    original = next(queue)
                except StopIteration:
                    break
                plan = prepare(original, budget)
                if plan is None:
                    continue
                record, remaining = plan
                journal['runs'].append({'id': record['id'], 'remainingSeconds': remaining,
                                        'threadId': record['resumeThreadId'], 'resumedAt': runner.now()})
                runner.write_json(STUDY / 'recovery.json', journal)
                future = pool.submit(runner.run_one, record, protocol,
                                     SimpleNamespace(codex=runner.CODEX, dry_run=False, timeout_seconds=remaining))
                active[future] = record
            if not active:
                break
            finished, _ = wait(active, return_when=FIRST_COMPLETED)
            for future in finished:
                record = active.pop(future)
                try:
                    good = future.result() and good
                except Exception as error:
                    runner.say(f"RECOVERY ERROR {record['id']}: {error}")
                    good = False
                status_path = Path(record['artifactDir']) / 'status.json'
                if status_path.exists():
                    status = json.loads(status_path.read_text())
                    if any('usage limit' in json.dumps(e).lower() for e in status.get('agentErrors', [])):
                        stop = True
                        runner.say('Service limit reached; no further queued jobs will start.')
    return 0 if good and not stop else 1

if __name__ == '__main__':
    raise SystemExit(main())
