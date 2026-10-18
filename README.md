# design-philosophy

A portable design philosophy and method, packaged as an Agent Skill. It captures how to think about interface design (restraint, hierarchy, novelty, craft, verification), not a particular look. Each project still derives its own identity.

## Layout

```
design-philosophy/
├── SKILL.md                 # entry point: what it is, the method in brief, when to read what
├── references/
│   ├── philosophy.md        # principles, the reason for each, and their tensions
│   ├── method.md            # eight phases with exit criteria
│   ├── identity.md          # deriving each project's own identity; avoiding sameness
│   ├── decisions.md         # decision guides: what to simplify, colour roles, states, copy…
│   ├── critique.md          # review questions for rendered work
│   └── case-*.md            # worked examples (illustrations, never templates)
├── templates/
│   ├── SYSTEM.md            # a project's own design system, to fill in
│   ├── tokens-guard.md      # token file + guardrail test pattern
│   └── AGENTS-snippet.md    # pointer for a project's CLAUDE.md / AGENTS.md
├── evals/evals.json         # prompts for checking the skill still behaves
└── CHANGELOG.md
```

## Install

Keep this folder in its own git repository (or your dotfiles), and link it into each agent's skills directory so there is one copy to maintain.

- **Claude Code (all projects):** `ln -s ~/src/design-philosophy ~/.claude/skills/design-philosophy`
- **Claude Code (one project, shared with the team):** copy or submodule it into `.claude/skills/design-philosophy/` in that repo.
- **Claude.ai / Claude desktop:** package the folder as a `.skill` file (or zip it) and add it under your skills settings.
- **Codex and other agents that support the Agent Skills (`SKILL.md`) format:** place or link the folder in that agent's skills directory (check the agent's docs for the path).
- **Agents without skill support:** reference `references/philosophy.md` and `references/method.md` from the project's `AGENTS.md`. Everything is plain Markdown; nothing depends on Claude-specific tools.

## Use

Say it in plain words at the start of a project or a redesign:

- "Use my design philosophy to design this application."
- "Redesign the settings screen using my design philosophy. Brand guide attached."
- "Apply the considered-design method to this dashboard; the users are on-call engineers."

Give it what only you have: brand guidelines, the platform it runs on, real or realistic data, and anyone it should take inspiration from. It will produce, in the project, its own `design/SYSTEM.md`, tokens and a guard test, alongside the implemented interface.

It works with other design skills: medium-specific skills (artifacts, charts, slides, polish passes, critique loops) handle their medium's mechanics; this one handles intent, process and judgement.

## Maintain

- **Lessons:** at the end of a project, the agent proposes edits when something would have changed an earlier decision. Review and commit the ones that generalise; reject ones that are really one project's taste.
- **Examples:** add a `references/case-<product>.md` for projects of a different kind (a dashboard, a desktop app, a mobile flow). Varied examples keep the skill from converging on one look.
- **Keep SKILL.md short.** Put detail in `references/`; SKILL.md should stay a map plus the method in brief.
- **Check it:** after significant edits, run the prompts in `evals/evals.json` with and without the skill and compare (layout and past results: `evals/README.md`; latest findings: `evals/iteration-1/FINDINGS.md`). The skill-creator skill can automate this. Signs of trouble: different projects coming out looking alike, the method being skipped, or generic checklists replacing product-specific reasoning.
- **Version:** note each change in `CHANGELOG.md`; tag releases if several machines or teammates use it.
