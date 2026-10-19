# Critique

Run this on rendered screenshots of every state, as if someone else made them. The questions are about judgement; the automated checks (contrast, tokens, overflow, layout shift) should already pass before you start.

## First look (five seconds per screen)

- What does the eye land on first? Is that the thing the user needs first?
- Can you tell what this screen is for without reading the small text?
- Is anything shouting that shouldn't be: a colour, a badge, a border, a shadow?
- Does it look like it belongs on its platform, or like a miniature web dashboard pasted in?

## Purpose and priorities

- Walk the top priority task. How many glances, clicks or keystrokes? Can any be removed?
- Is every element there because the user needs it to act or trust the result?
- Is anything the user needs hidden, truncated without recourse, or behind a click it shouldn't be?

## Restraint

- Count the colours. Name the meaning of each. Any without a meaning, or any meaning with two colours?
- Count the surfaces (cards, panels, filled boxes). Could a hairline or space do the job?
- Count the different sizes, weights and radii on screen. Could fewer do the job?
- Is there decoration that contributes nothing: gradients, icons beside every label, pills for plain values?

## Novelty and personality

- Where is the one distinctive moment? Is it at the product's differentiator, and does it explain something?
- Is the personality quiet (mark, a phrase, a motion) and never at usability's expense?
- Swap test: could this stylesheet be dropped onto the last project without anyone noticing? If so, revisit `identity.md`.

## Craft

- Alignment: do edges, baselines and icon centres line up? Is text optically centred in its container?
- Rhythm: is spacing consistent between like things and different between unlike things?
- Proportion: are touch targets and click areas comfortable at the real size? Are small elements legible?
- Long and awkward content: longest title, longest identifier, many items, zero items, huge numbers. Nothing clipped, nothing overlapping, wrapping at sensible boundaries.
- Both themes: is dark mode designed (contrast, elevation, saturation) or merely inverted?
- Motion: does it explain, is it quick, does reduced motion still convey everything?

## States

- Empty, loading, streaming, success, partial failure, total failure, offline, no results, permission missing: each one designed, each one honest.
- Does anything above the reading point move while content arrives?
- Do failures say what failed and what it means for the results?

## Copy

- Read every string aloud. Is it plain, specific, calm? Does it explain the unusual and stay silent on the conventional?
- Are inferred or uncertain things labelled as such?

## Interaction

- Keyboard path for the main task, focus visible and preserved after every re-render.
- Every instruction in the UI matches reality (shortcuts read live, limits real).
- Undo or dismiss paths exist where the user can make a mistake.

## Verdict

Write down: the three weakest things you found, what you changed, and what still needs a human eye or the real environment. Then fix and look again.
