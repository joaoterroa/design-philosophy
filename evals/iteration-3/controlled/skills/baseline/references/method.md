# Method

Eight phases. They overlap in practice, but don't move to the next until the current one's exit criteria hold. The criteria are what keeps this from becoming a checklist of generic UI advice: each asks for something specific to this product.

## Contents
1. Understand the product
2. Study references for their thinking
3. See the current state honestly
4. Choose a direction and the place for novelty
5. Write the system down
6. Implement
7. Verify and refine
8. Record and hand over

---

## 1. Understand the product

Read before you draw. For an existing product: the code paths of the UI, how data flows into it, the docs, the changelog or follow-up notes, the tests, the issues. For a new product: the brief, the users, the platform, the data it will show.

Find out:
- **Who** uses it and **in what moment** (mid-task in another tab? on a wall display? once a month?). The moment decides density, speed and how much attention the UI may ask for.
- **The first thing they need**, and the second. This becomes the visual hierarchy.
- **What must not break**: earlier fixes, accessibility work, measured performance, workflow guarantees. List them; they are constraints, not suggestions.
- **The platform's hard limits**: minimum and maximum sizes, permission models, shortcut space already taken, available fonts, offline behaviour. Verify each by documentation or test.

**Exit:** a short written statement of users, moment, 3–5 ordered priorities, constraints to preserve, platform limits (with the source of each).

## 2. Study references for their thinking

If the user names an inspiration, research the team's reasoning (essays, interviews, release notes, the real product and its interactions), not only its marketing site. If you have no inspiration, find two or three products that do the core task exceptionally well and study those.

For each reference, write:
- the principles it embodies, in your own words;
- what you will borrow (a reasoning pattern, an interaction idea, a level of craft);
- what you will deliberately not copy (branding, signature components, its palette and type).

If a source can't be reached, say so plainly and note what your conclusions rest on.

**Exit:** a list of borrowed principles, each tied to a concrete implication for this product ("their novelty goes into the differentiator, so ours goes into the answer arriving").

## 3. See the current state honestly

Get the real interface rendering with realistic data. If the backend or data source isn't available, build the smallest faithful stand-in: the real logic fed by realistic fixtures beats a static mockup, because states (streaming, partial failure, empty) are where design breaks.

Capture every state at the real sizes (narrowest supported, typical, widest), light and dark. Then write the audit:
- **Measured problems:** where the first useful content starts, how much the layout shifts while loading, what clips or overflows, contrast failures.
- **Hierarchy problems:** what draws the eye first versus what should.
- **Noise:** duplicated controls, decoration, badges, colours without meaning, instructions for familiar things.
- **Missing information:** what users need that is hidden or absent.
- **Pre-existing bugs** you notice; fix them in passing if small, and say so.

**Exit:** a baseline (screenshots and numbers) and a ranked list of the biggest weaknesses.

## 4. Choose a direction and the place for novelty

Decide structure before style. Ask: if this product were designed by a team that cared about every detail, where would each thing live? Challenge the existing layout where a different structure serves the priorities better (for example, moving input to where the hand already is, or turning a heading into the user's own question so the answer reads like a reply).

Then decide:
- **The novelty moment:** the one place that gets distinctive treatment, and why that place.
- **The identity** (read `identity.md`): derived palette, type, shape language, mark; each choice with a product-specific reason.
- **What to remove, merge, move, or keep** (read `decisions.md`).

State the direction in a few sentences someone else could check work against. Give it a short name if that helps the team talk about it.

**Exit:** a direction statement, the novelty moment, the identity with reasons, and the list of structural changes.

## 5. Write the system down

Before or alongside implementation, create the project's own design system (use `templates/SYSTEM.md` and `templates/tokens-guard.md`):

- **Tokens** for every colour (both themes), type size, radius, shadow and duration. Code uses tokens only.
- **SYSTEM.md** stating the product's purpose and priorities, its principles (adapted, not copied, from `philosophy.md`), each colour's meaning and where it must not be used, the type scale and its uses, spacing and shape rules, layout, components, motion, writing, keyboard, and a pre-ship checklist.
- **A guardrail test** that fails on literal values outside the token file, mismatched light/dark token sets, and text colours below contrast. It should run in the project's normal test command.
- **An agent pointer** (`templates/AGENTS-snippet.md`) in the project's agent instructions so future agents read the system first.

**Exit:** tokens, SYSTEM.md, guardrail test and pointer exist, and the test passes on the new code.

## 6. Implement

- Implement the actual redesign. A mockup alone leaves the hardest decisions (states, data, edge cases) unmade.
- Preserve behaviour and identifiers other code or tests rely on; keep earlier fixes and requirements intact.
- Keep architecture changes to what the design needs.
- Use real controls (`button`, `a`, `input`), keep keyboard focus across re-renders, expose hints to assistive tech, respect reduced motion.
- When content arrives over time, reserve space for it or add it below the reading point.

**Exit:** the redesign runs, existing tests pass, nothing previously working is lost.

## 7. Verify and refine

Look at the real thing again, systematically:
- Every state from phase 3, at every size, both themes.
- Numbers: layout shift during loading, first useful content position, overflow, contrast (automated), errors in the console.
- Interactions: the main keyboard path, focus after every action that re-renders, dismiss and restore, cancel, reload and restore state, the shortcut.
- Then run `critique.md` on the screenshots as if someone else had made them.

Fix, re-render, re-look. Expect at least two refinement rounds; most of the quality arrives here. Note each bug found and fixed.

**Exit:** the critique passes, the numbers are at least as good as the baseline, and the main paths work by keyboard.

## 8. Record and hand over

- Update the project's SYSTEM.md with anything decided during refinement.
- Write what was verified, how, and what still needs a human: live data, the real device or host, a brand owner's approval.
- If the project has a follow-ups or changelog file, record the change there.
- Propose any lesson that should improve this skill (see Maintenance in `SKILL.md`).

**Exit:** the next person (or agent) can continue without asking you anything.
