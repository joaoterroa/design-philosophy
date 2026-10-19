# Keep the current baseline; retain the experimental revision for review

The revision improves the on-call menu consistently. It does not improve the dashboard consistently, and banking is mixed. **Do not adopt the full bundle as the new baseline.** The agreed gate required a stable preference on at least two tasks across both repeats. Only the menu meets that gate.

Open the [visual comparison](index.html) before reading further if you want to judge without knowing the results. It starts blind, randomizes the sides, supports every captured state and size, and exports your choices. The canonical `SKILL.md`, `references/` and `templates/` are unchanged.

| Task | Repeat 1 | Repeat 2 | What the evidence supports |
|---|---|---|---|
| On-call menu | Revision preferred | Revision preferred | A modest, consistent improvement in ownership grouping and pending actions |
| Incident dashboard | Current preferred | Current preferred | The extra exploration did not select a better whole |
| Banking onboarding | Tie | Revision slightly preferred | Useful improvements, with inconsistent decisions across states |

These are editorial judgments from one informed main-agent reviewer, mostly with medium-low confidence. Image order was masked and [notes were saved](reviews/main-blind.json) before opening the [identity key](review-key.json). The reviewer knew the intervention and some functional results. This is not an independent human panel or a statistical result. The [revealed judgments](reviews/revealed-results.json) preserve the mapping rather than retroactively rewriting the notes.

## What improved

In both revised menus, **Back to schedule** is the filled action while a request awaits acceptance, with cancellation secondary. Both current-skill versions give cancellation the large action and return to the schedule through a small link. The revision better distinguishes “I have sent the request and can leave this screen” from “I want to undo the request.” See [repeat 1](index.html#oncall-menubar__1) and [repeat 2](index.html#oncall-menubar__2), selecting Pending.

The first revised menu also groups the assignment, shift and handover action into one object. The second retains the three other cached responders offline, whereas its current-skill counterpart replaces that roster with a disabled handover control and reconnect action. These are concrete decisions about what remains useful through a state change. They provide stronger evidence of intentionality than a new palette or logo would.

Revised banking repeat two makes calling a person the primary Help action and keeps returning to setup secondary. It describes two actions consistently and fits its welcome button at approximately y501–561 on the 320×568 screen. Its own earlier draft placed the button below that viewport; the retained draft and final captures show a real correction. Both revised banking runs pass the scoped text, target, field-label and interaction checks.

The useful existing principles survive in both conditions: pending ownership is explicit, a missing commander is not invented, stale data is identified, wrong codes are rejected, and Help provides a human route with working Escape and focus return. All scripted menu and banking main paths pass. There is no reason here to discard those strengths.

## What did not improve

The current dashboard is preferred twice, for different concrete reasons. In [repeat one](index.html#incident-dashboard__1), it keeps both resolved summaries beside the table on TV, while the revision puts that history behind a tab. Its metrics and sidebar also form a more integrated whole. The current version is the more open composition here; relaxing a surface quota did not determine which version would achieve that.

In [repeat two](index.html#incident-dashboard__2), the current version gives resolved history a wide bottom region and makes stale data a full-width status change. The revision narrows history into its sidebar and uses a smaller warning area next to the page title. The revision does improve the separation of Opened and Duration and makes pagination more explicit. Those local improvements do not establish a better overall arrangement.

Banking repeat one is a useful counterexample to declaring the revision better because it follows the new method. Its Help call hierarchy improves, but **Get started is entirely below the initial 320×568 viewport**. The current version keeps it visible. Ordinary vertical scrolling works, so this is an observed layout trade-off rather than proof that older users cannot proceed. It still weakens the claim that the revision consistently selects the better composition.

Both conditions mostly produce familiar menus, operational tables and reassuring banking forms. The revision does not consistently create more distinctive character. A quieter dashboard can be appropriate, but this experiment does not demonstrate that the earlier personality gap has been closed. These tasks also differ substantially from a personal browser; resemblance to Dia is not the success criterion.

## Why the process change was insufficient

All six revised runs retained alternatives and rendered initial studies before final implementation. Some forks are substantial: own-shift versus roster-first menus, a table versus status board, and a separate welcome versus immediate form entry. See the [second menu study](runs/oncall-menubar/revision/run-2/outputs/verification/compositions.png), [dashboard table](runs/incident-dashboard/revision/run-2/outputs/exploration/table.png) and [board](runs/incident-dashboard/revision/run-2/outputs/exploration/board.png).

The depth varies. Banking repeat one's [A](runs/banking-onboarding/revision/run-1/outputs/review/composition-a.png) and [B](runs/banking-onboarding/revision/run-1/outputs/review/composition-b.png) retain the same reading order and similar action positions; the main difference is a dark introduction with a white task sheet. That explores grouping, but provides a weak test of alternative hierarchy. Some after-action comparisons were added later: banking repeat two's next-state captures appear in the log after final implementation had begun. Requiring two renders did not ensure a strong decision fork or that difficult states informed selection early enough.

This supports a gap in **translation and selection**, rather than proof that the revised philosophy is wrong. A count of alternatives is easy to satisfy. Judging viable alternatives against the hard state remains the important work. The bundle also changes several visual principles at once, so these outcomes cannot identify which instruction caused a preference.

There is an additional coherence limit: the frozen revised `templates/SYSTEM.md` retains legacy wording about plainness, color meaning and nested radii. This was noticed after freeze and [recorded](../notes/post-freeze-observations.md), without correcting the treatment mid-study. Some generated systems remain very restrictive, but that alone does not establish that the template caused the visual results.

## Shapes and execution

The [optional shape reference](skills/revision/references/shape-language.md) preserves the user's preference for **Adjusted Squircle** when a soft continuous-corner treatment suits the product. It covers proportions, insets, nesting, fallback and focus treatment without requiring the style universally.

No final app uses CSS `corner-shape` or a documented continuous-corner implementation. The generated systems specify ordinary radii. Therefore **this cohort does not test the visual effect of Adjusted Squircle**. It cannot establish that the shape reference improved the interfaces or that the preference should become a core rule. The reference remains separate for a future applicable use.

Two execution defects occur in the current banking condition: repeat one's local font is blocked by Chromium under `file://` and renders with a fallback; repeat two's code-screen practice footer is 14px, below the declared 16px check. These are real recorded failures, not missing generic selectors. Neither proves a wholesale philosophy failure. The revised condition has no automatic failure flags; all task-path checks pass. Automated results do not establish full accessibility or usability.

## Recommended next step

**Review these six existing pairs blind, then test a smaller process-only revision on the dashboard.** Do not add more style rules or gather another broad reference library first. The dashboard is the clearest negative case, with the current version preferred in both repeats.

For that next experiment, retain the current philosophy and change only the decision exercise: compare two viable compositions using both the normal screen and the stale/surge state at actual TV and laptop sizes before selecting one. Hold content and the action path constant; require a reason either direction could plausibly win. Use two runs per condition, four jobs total. This isolates the process change more closely and tests whether it can beat the stronger current result. A positive result would still need transfer to another task before a general adoption claim.

Keep the shape preference optional. Propose the template cleanup alongside the next candidate, without altering this frozen revision. Human choices on these existing pairs are the immediate next evidence; no additional generation or promotion is needed before that review.

## Collection and limits

- Twelve completed task-only runs; two per condition for each original task; equal cumulative twelve-minute ceilings; one fixed model and shared reference pack.
- **192/192 final PNGs**, light and dark, at native menu size, 1920×1080/1440×900 dashboards and 390×844/320×568 banking. Network requests are blocked; image hashes, dimensions, non-uniform pixels and unchanged source trees are checked.
- No horizontal overflow, menu clipping, runtime exceptions or network dependencies in the capture matrix. The one local-font console failure remains visible. [Functional evidence](functional.json) and [manual dashboard checks](reviews/manual-dashboard.json) are separate from preference.
- All four dashboards show seven open rows initially during TV surge and acknowledge five more. Paging reaches all twelve; laptop scrolling, search and resolved history are checked. This is not proof of unattended-TV suitability or viewing-distance legibility.
- The earlier cross-task pilot is excluded in full. All primary attempts encountered service usage limits and continued in their exact saved sessions, with original remaining time and unchanged inputs. Earlier segments are retained; no poor design was replaced. See [protocol](protocol.json) and [recovery](recovery.json).
- The prototypes have no live backend or native integration. Older-user comprehension, assistive technology, real mobile keyboard behavior and physical viewing distance remain untested. The static main-screen and state inspections are evidence of rendering, not measured user performance.

A [clean staged-tree export](verification-clean-checkout.json) in a different directory reproduced all 192 nonblank captures with matching dimensions, body text and unchanged source trees. 190 PNGs are byte-identical. The two current-menu repeat-two Compose captures differ only within a 12×7px native select-arrow area; the cause of that paint variation is unconfirmed. Original comparison images remain unchanged.
