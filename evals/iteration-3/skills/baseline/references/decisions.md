# Decision guides

How to decide, case by case. Each guide is a set of questions; the answers depend on the product.

## Contents
- Simplify, emphasize, remove or redesign
- Hierarchy and the first screen
- Colour roles
- Information density
- States and loading
- Layout stability
- Controls and interaction
- Motion
- Copy
- Platform constraints
- Accessibility
- Interpreting feedback

## Simplify, emphasize, remove or redesign

For every element on screen, ask in order:

1. **Does the user need it to do the job or trust the result?** If no, remove it. If yes, keep it, however plain the screen wants to be.
2. **Does something else already do this job?** Merge into the one that is easier to find. Two status displays, two ways to cancel, two labels for one thing: keep one.
3. **Is it needed always, or only in a situation?** Situational things appear in their situation (an access prompt only until access is granted; a stale-data note only while data is stale).
4. **Is its weight right for its importance?** Emphasize by position, then weight, then size, and colour last.
5. **Is the structure fighting the task?** If the user's eye or hand has to travel against the flow (the input far from the reading point, the answer below its controls), redesign the structure, not the styling.
6. **Is it explaining something conventional?** Remove the explanation; keep it for assistive technology.

## Hierarchy and the first screen

- Write down what must be visible without scrolling at the typical size, in priority order. Measure where the first useful content starts before and after.
- The user's own input often makes the best heading for the output: it reminds them what they asked and frames everything below as an answer.
- Group by meaning, separate with space and hairlines, and use one filled surface per screen at most for a grouped fact.

## Colour roles

- List the meanings the product needs. Typical: brand/act, follow/cite, caution, failure, health, data categories. Fewer is better.
- One colour per meaning, used for that meaning everywhere. When feedback changes "this link's colour", it changes the role.
- Errors are never colour alone: words plus a tinted surface, so they can't be confused with a brand colour in the same hue family.
- If many things need telling apart (sources, categories), consider shape and name before colour; a coloured category is one more meaning to learn.
- Use exact brand values for fills and marks; adjust text uses only as far as contrast requires, and document it.

## Information density

- Tools for experts: dense, aligned, tabular numbers, metadata visible, caveats written out. Make density calm with consistent rhythm and quiet secondary text, not by hiding.
- Tools for occasional users: fewer things at once, more guidance, progressive disclosure for advanced controls.
- Truncate only where the full value is reachable (tooltip, expansion), and break long identifiers at natural boundaries rather than mid-token.

## States and loading

- Enumerate every state before designing any: empty, first run, loading, streaming partial results, success, no results, partial failure, total failure, offline, permission missing, stale data.
- Show results as soon as they are usable; never make the user wait for the slowest part.
- A failure is "missing, not empty": say what failed and that its results are absent.
- Loading treatments show the shape of what is coming in the space it will occupy. Loops stop when work stops.

## Layout stability

- Reserve space for content that will certainly arrive; size the reserve from real measurements.
- Content that may or may not arrive goes at the end of the flow, where its arrival moves nothing above.
- Grow containers away from the reading point (a bottom-docked input grows upward; a top bar grows downward only if nothing is being read below it).
- Measure layout shift during real loading and compare with the baseline.

## Controls and interaction

- One control per action, in the place the user already looks.
- A primary action can change role with state (send becomes stop while working) rather than adding a second button.
- Toggles that filter keep keyboard focus when the view re-renders.
- Familiar shortcuts and patterns are adopted, not reinvented; check they don't collide with the host's own (research the host's shortcut list).
- When instructions mention a value the system controls (a shortcut binding, a limit), read the live value instead of hard-coding the text.

## Motion

- Durations short (roughly 150ms for hover and press, 200–250ms for things appearing); ease out.
- Motion explains: an item arriving, a container growing, the target of a jump flashing once.
- Reduced motion removes all of it without losing information.

## Copy

- Plain and specific: what happened, what it means, what to do. "Jira timed out. Its results are missing from this search, not empty."
- Label inferred things as inferred; never claim more certainty than the data supports.
- No exclamation marks, filler or performed personality. Personality shows in precision and in a few well-chosen words.
- Examples in empty states should be real, typed by kind, and runnable in one click.

## Platform constraints

- Find the real limits early and from sources (docs, issue trackers, testing): minimum sizes, whether the product can control them, reserved shortcuts, permission prompts, font availability.
- Design to the floor (the narrowest real size), then check the typical and widest sizes.
- When a limit can't be changed by the product, say so to the user rather than pretending a setting fixes it.

## Accessibility

- Contrast: 4.5:1 for text, 3:1 for meaningful graphics, checked automatically in both themes.
- Real controls, visible focus, focus preserved across re-renders, hints via `aria-describedby`, live regions for milestones only (not every update).
- Test the keyboard path end to end.

## Interpreting feedback

- Restate ambiguous feedback as a role change before acting ("so: link colour → red, caution colour → something that pairs with red, other red stays").
- Feedback about one screenshot usually applies everywhere that role or pattern appears; apply it consistently and say so.
- When the user supplies brand material, it overrides your earlier palette choices.
- If your earlier choice is overturned, find the reason and record it as a lesson; it is often a general rule (brand first; don't explain the familiar; dynamic over fixed when nothing moves).
