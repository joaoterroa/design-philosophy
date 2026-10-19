---
name: design-philosophy
description: The user's own design philosophy and method ("considered design") for designing or redesigning any product interface — web app, browser extension, desktop app, dashboard, CLI/TUI, mobile, internal tool. Use it whenever the user says "use my design philosophy", "design this the way we do", "make it feel considered/crafted/like The Browser Company", asks to design, redesign, restyle or polish an application's UI, or starts a new product and needs its visual and interaction direction, even if they don't name the skill. It drives research, intentional decisions, implementation, rendered verification and refinement, and gives each project its own identity instead of a house style. Not for one-off charts, slide decks or documents; use the matching skill for those.
---

# Considered design

A way of designing, not a look. Every project that uses this skill should end up with its own identity, derived from its users, its brand and its platform, and the same quality of thinking behind it.

The short version of the philosophy: **familiar patterns made exceptionally well; colour and novelty chosen for the product’s task and character; nothing hidden that the user needs; every detail checked in the real thing, not imagined.** The rest of this skill is how to do that on purpose.

## How to use this skill

Work through the method below. Read the reference files when a step points to them, not all at once:

| File | Read when |
| --- | --- |
| `references/philosophy.md` | Before forming a direction. The principles, the reasoning behind each, and the tensions between them. |
| `references/method.md` | At the start, for the full phase-by-phase method with exit criteria. |
| `references/identity.md` | Before choosing colour, type, shape or a mark. How to derive a project's own identity, and how to avoid every project looking alike. |
| `references/shape-language.md` | When a soft, continuous-corner treatment fits the project. Optional visual reference, including the user’s preferred Adjusted Squircle. |
| `references/decisions.md` | Whenever you are deciding what to simplify, emphasize, remove, or redesign, or picking colour roles, type, layout, motion, copy. |
| `references/critique.md` | When reviewing your own rendered work, before calling it done. |
| `references/case-recall.md` | Once, to see the method applied end to end, including the mistakes. It is an illustration, never a template: do not reuse its palette, layout or components. |
| `templates/` | When creating the project's own design system and guardrails (Phase 5). |

## The method in brief

1. **Understand the product before designing it.** Read the code, the docs, the open issues, the constraints that earlier work fixed. Find out who uses it, in what moment, and what they need first. Write the 3–5 priorities in order. If the brief names priorities, they are the tie-breakers for every later decision.
2. **Study reasoning and real interfaces together.** Examine actual product screens and, where available, a short transition. Connect a visible relationship (composition, proportions, type, shape or state continuity) to this product’s needs. Separate shipped UI from marketing staging. Borrow the judgment, with attribution, rather than its branding. If access is blocked, record the evidence limit.
3. **See the current state honestly.** Get the real thing rendering at realistic sizes with realistic data, in every state (empty, loading, streaming, success, partial failure, offline, no results), light and dark. Name its weaknesses in measurable terms ("the first result starts 608px down"), not adjectives.
4. **Compare compositions, then choose a direction.** Render at least two meaningfully different compositions of a critical screen before committing the structure or tokens. Vary hierarchy, layout, grouping or interaction approach; colour and radius variants alone do not count. Compare at the real size against the ordered priorities, then recommend one and record its trade-off. Keep familiar mechanics where they help; give distinctive treatment as much room as the task and learning cost justify.
5. **Write the system down, then build to it.** Tokens for every colour, size, radius, shadow and duration; a project `SYSTEM.md` that records the principles and the reason behind each value; a guardrail test that fails when code drifts from the tokens. Use `templates/`.
6. **Implement the redesign, not a mockup.** Preserve existing behaviour and earlier fixes; restructure where it helps; keep every interaction keyboard- and screen-reader-sound.
7. **Verify in the rendered product and refine.** Screenshot every state at the real sizes in both themes; measure layout shift, overflow, focus retention, contrast; click through the main paths. Fix what you see, then look again. Run `references/critique.md` before calling it done.
8. **Record and hand over.** Update the project's `SYSTEM.md`, note what was verified and what still needs a human (live data, the real device), and propose any lesson that should improve this skill (see Maintenance).

Each phase has exit criteria in `references/method.md`. Skipping verification is the most common way to ship something that only looked right in your head.

## Working with the user

- **Ask early for what you cannot derive:** brand guidelines or assets, the platform it runs on (and its quirks), real or realistic data. A brand guide beats any palette you could invent. If none exists, propose a palette and say it is a proposal.
- **When feedback references a screenshot, map it explicitly** ("you mean: the link colour becomes red, and the flag colour changes") before acting. Feedback about one element is often about the role that element plays everywhere.
- **Don't explain familiar interactions in the UI.** If a pattern is conventional (`@` to mention, ⌘K, drag to reorder), trust it; put the hint where assistive tech can find it instead.
- **State trade-offs you made on their behalf** in one line each (for example, "the exact brand red is 4.43:1 as small text, so text uses a slightly deeper red").
- **Give a recommendation, not a menu.** Present one direction with its reasoning; mention a road not taken only when the user would plausibly prefer it.

## Working with other skills

This skill decides what to build and why, and how to judge it. It is meant to sit above medium-specific skills, not to replace them:

- If a skill exists for the medium (an artifact or page contract, charts and data visualisation, slide decks, a final polish pass, a multi-critic design loop, a frontend framework), follow it for that medium's mechanics and technical rules, and keep this skill's process, priorities and critique.
- If two instructions conflict on a technical contract of the medium, the medium's skill wins. If they conflict on taste or intent, this skill and the project's own `SYSTEM.md` win, in that order of specificity: project system first, then this philosophy.
- Don't re-derive what a specialised skill already provides (a validated chart palette, a page template). Adopt it, then apply identity and restraint on top.

## What "done" means

- The interface reads correctly at a glance at its real size, in both themes, in every state, with nothing clipped, overlapping or jumping.
- Every colour, size and motion comes from the project's tokens, and the guardrail test passes.
- A stranger could explain why each visual choice is there, in terms of this product's users and purpose.
- The project's design system is written down, so the next change starts from it instead of drifting.
- What could not be verified here is listed plainly.

## Maintenance

This skill improves through use. At the end of a project, if something you learned would have changed a decision earlier, write it as a proposed edit (a short diff or paragraph, with the project it came from) and offer it to the user. Don't edit the skill silently. Add new worked examples as additional `references/case-*.md` files from different kinds of products, so the examples never converge on one look.
