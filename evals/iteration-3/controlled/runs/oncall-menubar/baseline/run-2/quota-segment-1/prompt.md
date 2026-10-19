Use my design philosophy to design the UI for a small macOS menu-bar app that shows our team's on-call schedule and lets me hand over a shift. There's no existing code yet; it's for about 40 SREs.

# Production contract for this evaluation

This workspace is one task: implement only the task in the opening user request. Task-specific clauses below apply only to that task.

Work only in this workspace. Read `skill/SKILL.md` and follow that supplied skill. It is the only design skill for this run. Other agents work elsewhere; edit only this workspace. Use `reference-pack/` for available offline visual research. Do not search other projects, home directories, earlier evaluations or other runs. Do not use installed skills, subagents, connectors or external services. All assets and code must work offline from disk. State any evidence limits instead of requesting clarification.

Deliver `outputs/app/index.html`, supporting static files, `outputs/DESIGN.md` and your verification scripts/screenshots. The prototype must run from file:// without a build or network. Copy the provided fixtures.js into the app and use EVAL_FIXTURES for shared facts. You may choose your copy and composition. Do not display test codes or pretend to use a real backend.

Provide a document root container `#app`. URL `?screen=<state>&theme=light|dark&display=tv|laptop` must directly open the states below. Normal interactions must work too. Record implemented and omitted behavior in DESIGN.md; no demo controls inside the product canvas. You may put a review harness in a separate HTML file.

## Assigned product requirements

Menu: `main`, `compose`, `pending`, `offline`, `empty`, `accepted`. #app is a 360px-wide popover with maximum height640px, at x20/y20 in a 400×680 scene. The main flow lets Jamie choose Priya, review and send a handover. Sending enters pending, with Jamie responsible until acceptance. A simulated acceptance is a separate explicit action, not automatic. Offline shows last-known status honestly. Empty has no schedule. Preserve a return/cancel route. The supplied roster is the current roster, not all40staff.

Implement light and dark themes via the URL and system preference. Provide semantic, labeled controls, keyboard operation and visible focus. Preserve information in reduced motion. Target sizes and contrast must suit the task. Every state must be accessible through its direct URL.

You have the same12minute wall-clock allowance as every run, including research, exploration, implementation and verification. Use this whole allowance wisely, but finish when the implementation and checks are ready. Prioritize a runnable complete result. Do not install dependencies. Available tools: Node, Python `/private/tmp/design-compare-venv/bin/python` with Playwright and Pillow, and installed Chromium. Headless launch can require sandbox escalation; request that through the approval tool if needed. Inspect rendered screens yourself, fix issues, and record what you actually tested. Save a small set of your own screenshots; a separate evaluator will capture the full standardized set.

Do not commit, push, modify the supplied skill or fixtures, or edit global configuration. Record a preference for a visual treatment only if it fits this task. These are prototype exercises, not deployments.
