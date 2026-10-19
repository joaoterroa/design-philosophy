# Philosophy

These principles are the stable core. They say how to think; they deliberately say nothing about which colours, fonts or components to use. Each one comes with the reason it exists and the way it goes wrong, because a principle applied without its reason turns into a style.

## Where it comes from

The starting influence is The Browser Company, particularly Dia. Its reasoning informs the core; visual treatments remain choices for each project:

- **"Familiar, but elevated."** Dia was designed so anyone could switch to it on an ordinary Tuesday morning without learning anything. Core mechanics stay where people expect them; the craft goes into how well they are made. Arc, the company's earlier browser, reinvented the core and paid for it in adoption.
- **Minimalism in the core UI, even when it is hard.** No duplicate controls, no update banners; secondary things appear when they are relevant.
- **Novelty placed where it adds value.** The unusual parts are reserved for what genuinely differentiates the product.
- **Craft as care.** Colour that extends naturally from the content, fluid but purposeful motion, tidy spacing; release notes that celebrate making things "tidier, quieter, more considered".

What this skill adds on top: a working tool's needs (density, accuracy, trust), a method that verifies everything in the rendered product, and a written system per project so quality doesn't drift.

## The principles

### 1. Familiar first, then elevated
Use the patterns people already know for the job: a search box where search boxes go, links that look like links, a segmented control for a few peer views, a standard shortcut idiom. Earn delight through execution (alignment, timing, the exact wording) rather than new mechanics.
*Why:* every unfamiliar mechanic is a cost the user pays before getting value. Familiarity is what lets craft be noticed instead of puzzled over.
*Goes wrong when:* "familiar" becomes "generic". The pattern is familiar; the execution must not be.

### 2. One obvious way
Each task has one control in one place. When something is hard to find, make the existing way more findable instead of adding a second way. Status that is fine stays quiet; status that needs the user speaks in a sentence with a fix.
*Why:* duplicate paths split attention and make every screen busier for everyone.
*Goes wrong when:* "one way" becomes hiding the way. One control, clearly visible.

### 3. Spend novelty where it pays
Put unfamiliar mechanics where they earn their learning cost. Distinctive composition, typography, shape and expression can work together across a product without requiring new mechanics. Decide how much expression the task and context can support.
*Why:* people need a clear path to value and a coherent product character. A fixed count of distinctive moments measures neither.
*Goes wrong when:* novelty obstructs the task, or a novelty quota turns useful familiarity into generic execution.

### 4. Minimal is not hidden
Remove decoration, never information. For a tool, density, discoverability and precise detail (dates, sources, states, counts, caveats) are features. Hierarchy, not deletion, is how you make dense information calm.
*Why:* restraint is for the user's attention, not for the screenshot. A technical user forced to hunt for a detail will stop trusting the tool.
*Goes wrong when:* a clean screen is achieved by pushing needed information behind clicks.

### 5. Colour is meaning
Keep operational meanings consistent and distinguishable. Colour can also support identity, context or atmosphere when it strengthens the product without confusing status or weakening contrast. Derive brand uses from the brand and judge their combined visual weight.
*Why:* stable signals help scanning; considered expression can help orientation and attachment. Both must serve this product.
*Goes wrong when:* colour alone carries a meaning (an error must also be words), or when a brand colour is used for a job it fails at (contrast, confusion with errors).

### 6. Words over widgets
Prefer a clear sentence ("Copy of Jira text, so not independent confirmation") to a badge, icon or colour code the user has to learn. Copy is plain, specific and calm: what happened, what it means, what to do.
*Why:* words are the most precise interface. Badges and icons multiply the vocabulary the user must learn.
*Goes wrong when:* words become instructions for familiar things ("Type @ to…"). Explain what is unusual; trust what is conventional.

### 7. Stable, honest layout
Things fill in place and never push what the user is reading. Reserve space before content arrives; add late arrivals at the end, not the middle; let containers grow in the direction that moves nothing (a docked composer grows upward). Never make something look more certain, complete or resolved than it is.
*Why:* a jumping layout breaks reading and erodes trust; so does an interface that overstates certainty.
*Goes wrong when:* stability is bought with dead space. Look for the layout that gives both.

### 8. Native to its platform
Respect the host: system type where native feel matters, the platform's conventions, its constraints (minimum sizes, shortcuts already taken, permission models). Research the constraints instead of assuming them, and design to the real limits.
*Why:* an interface that fights its host feels like a guest. Constraints discovered late cause the ugliest compromises.
*Goes wrong when:* "native" becomes "default". Native is the starting point for craft.

### 9. Craft is verified, not imagined
Every claim of quality is checked in the rendered product: real sizes, both themes, every state, keyboard path, screen reader text, reduced motion, layout shift. Fix what you find, then look again.
*Why:* the difference between a prototype and a finished product lives in states and details you only see by looking.
*Goes wrong when:* screenshots of the happy path stand in for verification.

### 10. Write the system down and guard it
Each project gets its own tokens, its own written rationale and an automated check that the code keeps to them. The written system is the memory that stops later changes from drifting back to generic.
*Why:* taste decays under deadline pressure unless it is cheap to follow and visible when broken.
*Goes wrong when:* the system documents values without reasons. Values without reasons get changed casually.

### 11. Personality in proportion
Let personality come from the whole composition and the task: its rhythm, proportions, words, objects and transitions. Quiet precision can suit an operational tool; a consumer destination can support more expression. Preserve usability and judge the complete result.
*Why:* a coherent character feels cared for. Isolated flourishes cannot rescue a weak composition.

## Tensions and how to resolve them

| Tension | Resolve by |
| --- | --- |
| Simplicity vs. density | Keep the information; simplify the hierarchy. Weight, size and position before deletion. |
| Stability vs. no wasted space | Reserve only what will certainly arrive; put uncertain arrivals at the end; grow containers away from the reading point. |
| Brand fidelity vs. accessibility | Use the exact brand value for fills and marks; adjust the minimum needed for text contrast and say so. |
| Polish vs. speed | Motion and animation never delay the user; content first, choreography second. |
| Familiar vs. distinctive | Familiar mechanics where useful; distinctive execution with a justified learning cost. |
| Explaining vs. trusting | Explain the unusual and the risky; trust the conventional; always expose hints to assistive tech. |
| User's literal request vs. its intent | Map the request to the role it touches; confirm the mapping when ambiguous; then apply it consistently everywhere that role appears. |
