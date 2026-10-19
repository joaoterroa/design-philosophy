# Infrastructure corrections

The first launch used mutually exclusive CLI flags `--sandbox workspace-write` and `--approve-for-me`. The CLI rejected all twelve invocations at argument parsing, with zero JSONL events and no model execution or generated artifacts. Records remain in each run’s `infrastructure-attempt-1/`. Removed the redundant `--sandbox` flag; `--approve-for-me` itself selects workspace-write with automatic approval review. The frozen model, prompts, skill files, conditions and design budget are unchanged. This is a launch correction, not replacement of a design outcome.

## Service quota interruption and continuation

At17:22–17:23UTC the service stopped three in-progress sessions on the account usage limit. Nine further sessions failed before design work. Those records are retained as `quota-segment-1/`, including the three partial output trees. No design was evaluated or selected for replacement.

At19:06UTC the read-only `account/rateLimits/read` endpoint reported `ordinaryUsageAllowed=true`, with no reached-limit type. No credits or banked resets were consumed and no model or credential substitution occurred. Continuation uses each same workspace and only the remaining part of its1200second active allowance. Three earlier sessions were ephemeral, so hidden context is unavailable; their own visible trace is supplied alongside the retained work. The other nine begin their design work fresh. This is an evaluation limitation, disclosed separately from design quality.

Recovery now persists normal CLI session rollouts to allow exact continuation if needed. Host skills, plugins, MCP, web and memories remain disabled; approval review and safety rules remain enabled. `protocol.json` and both skill/input snapshots are unchanged. `recovery.json` records per-run budget and context recovery.
