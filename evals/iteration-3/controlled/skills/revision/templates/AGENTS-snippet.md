# Agent pointer

Add these lines to the project's agent instructions (`CLAUDE.md`, `AGENTS.md`, or both) once the project has its own design system. They make every future agent start from the project's decisions instead of rediscovering or drifting from them.

```markdown
## UI and design
- Any change to the interface follows `design/SYSTEM.md` (this project's own design system). Read it first.
- New values go in `[path/to/tokens]`, never inline. `[test command]` includes the design guard test.
- For new UI work, use the `design-philosophy` skill's method (understand → references → audit → direction → system → implement → verify → record), but this project's SYSTEM.md decides its look.
- Record verified design changes and open items in `[FOLLOWUPS.md / CHANGELOG]`.
```

For agents without skill support, replace the third line with a path to a local copy of the philosophy, for example `docs/design-philosophy/philosophy.md` and `method.md`.
