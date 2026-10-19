#!/usr/bin/env python3
"""Freeze baseline/revision and build independent workspaces. Run only before eval starts."""
from hashlib import sha256
from pathlib import Path
import json, shutil, subprocess, difflib, random

ROOT=Path(__file__).resolve().parents[3]
STUDY=ROOT/'evals/iteration-3'
WORK=Path('/private/tmp/design-eval-iteration-3')
FILES=['SKILL.md']+[p.relative_to(ROOT).as_posix() for folder in ('references','templates') for p in sorted((ROOT/folder).rglob('*')) if p.is_file()]

def digest(path):return sha256(path.read_bytes()).hexdigest()
def change(path,old,new):
    text=path.read_text();assert old in text,(path,old);path.write_text(text.replace(old,new))

def make_revision():
    for condition in ('baseline','revision'):
        dest=STUDY/'skills'/condition
        assert not (STUDY/'protocol.json').exists(),'Frozen protocol already exists; never silently overwrite trial inputs.'
        for file in FILES:
            (dest/file).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/file,dest/file)
    r=STUDY/'skills/revision'
    change(r/'SKILL.md','colour and novelty spent only where they carry meaning','colour and novelty chosen for the product’s task and character')
    change(r/'SKILL.md','| `references/decisions.md` |','| `references/shape-language.md` | When a soft, continuous-corner treatment fits the project. Optional visual reference, including the user’s preferred Adjusted Squircle. |\n| `references/decisions.md` |')
    change(r/'SKILL.md','2. **Study references for their thinking, not their pixels.** When the user names an inspiration, research how that team reasons (their writing, release notes, real product screenshots), then name the principles you will borrow and the surface details you will not copy. If the network blocks a source, say so and work from what you can verify.',
      '2. **Study reasoning and real interfaces together.** Examine actual product screens and, where available, a short transition. Connect a visible relationship (composition, proportions, type, shape or state continuity) to this product’s needs. Separate shipped UI from marketing staging. Borrow the judgment, with attribution, rather than its branding. If access is blocked, record the evidence limit.')
    change(r/'SKILL.md','4. **Choose a direction and the one place for novelty.** Decide the structure first (what goes where, what the user\'s eye does), then the identity. Pick the single moment that differentiates this product and spend the unusual treatment there. Everything else is familiar and plain.',
      '4. **Compare compositions, then choose a direction.** Render at least two meaningfully different compositions of a critical screen before committing the structure or tokens. Vary hierarchy, layout, grouping or interaction approach; colour and radius variants alone do not count. Compare at the real size against the ordered priorities, then recommend one and record its trade-off. Keep familiar mechanics where they help; give distinctive treatment as much room as the task and learning cost justify.')
    p=r/'references/method.md'
    change(p,'4. Choose a direction and the place for novelty','4. Compare compositions and choose a direction')
    change(p,'If the user names an inspiration, research the team\'s reasoning (essays, interviews, release notes, the real product and its interactions), not only its marketing site. If you have no inspiration, find two or three products that do the core task exceptionally well and study those.',
      'Study the team’s reasoning beside actual product screens and a short task transition where available. Identify a visible relationship among elements and explain what it achieves. Distinguish shipped UI from staged component art. If no inspiration is named, study products that do the core task well.')
    start=p.read_text().index('## 4. Compare compositions and choose a direction');end=p.read_text().index('## 5. Write the system down')
    s=p.read_text();s=s[:start]+'''## 4. Compare compositions and choose a direction

Render at least two small alternatives for a critical screen at its actual size, before fixing the style system. Make a meaningful change to hierarchy, layout, grouping or interaction; a palette or corner change alone is not an alternative. Keep the content and task comparable. For a stateful task, also inspect what happens after the main action in each alternative.

Compare where attention lands, what can be understood and done, what fits, and what gives this product its own character. Choose one against the ordered priorities. Preserve the alternatives and record the strongest reason to reject the other; an unusual alternative does not win by being unusual.

Then derive the identity (read `identity.md`) and decide what to remove, merge, move or keep (read `decisions.md`). Novelty is a learning cost, not a quota on distinctive details. Present one recommendation after exploration.

**Exit:** two rendered compositions, their comparison, a chosen direction with identity reasons, and the trade-off it accepts. Freeze tokens after this choice, then revise them when rendered evidence warrants it.

'''+s[end:];p.write_text(s)
    p=r/'references/philosophy.md'
    change(p,'Not its look, its reasoning:','Its reasoning informs the core; visual treatments remain choices for each project:')
    change(p,'Choose the single moment that differentiates the product (the answer arriving, the first result, the thing only this product does) and give it the distinctive treatment: a considered animation, a layout that fills in place, a small piece of personality. Everything else stays plain so that moment can be felt.\n*Why:* novelty is a budget. Spread everywhere it becomes noise; concentrated, it becomes the product\'s character.\n*Goes wrong when:* the "special" moment is decorative rather than informative. The novelty should explain what is happening.',
      'Put unfamiliar mechanics where they earn their learning cost. Distinctive composition, typography, shape and expression can work together across a product without requiring new mechanics. Decide how much expression the task and context can support.\n*Why:* people need a clear path to value and a coherent product character. A fixed count of distinctive moments measures neither.\n*Goes wrong when:* novelty obstructs the task, or a novelty quota turns useful familiarity into generic execution.')
    change(p,'Neutrals carry the interface. Each colour that remains has one job and keeps it everywhere (act, follow, caution, failure, health). A colour that means nothing is removed; a meaning with two colours is merged. Brand colours come from the brand, then are assigned roles.\n*Why:* when colour is reserved, the eye learns the meanings within minutes and scans faster. Decorative colour competes with meaningful colour.',
      'Keep operational meanings consistent and distinguishable. Colour can also support identity, context or atmosphere when it strengthens the product without confusing status or weakening contrast. Derive brand uses from the brand and judge their combined visual weight.\n*Why:* stable signals help scanning; considered expression can help orientation and attachment. Both must serve this product.')
    change(p,'### 11. Personality, quietly\nPersonality lives in a few considered places: a mark that says what the product does, a phrase of copy, a moment of motion, a small detail done better than necessary. It never costs usability and never shouts.\n*Why:* people warm to tools that feel cared for. They tire of tools that perform.',
      '### 11. Personality in proportion\nLet personality come from the whole composition and the task: its rhythm, proportions, words, objects and transitions. Quiet precision can suit an operational tool; a consumer destination can support more expression. Preserve usability and judge the complete result.\n*Why:* a coherent character feels cared for. Isolated flourishes cannot rescue a weak composition.')
    change(p,'Familiar mechanics, distinctive execution and one distinctive moment.','Familiar mechanics where useful; distinctive execution with a justified learning cost.')
    p=r/'references/identity.md'
    change(p,'Start neutral, then add colour only for roles the product needs (act, follow/cite, caution, failure, health, data categories).','Choose a palette for the product’s character and tasks. Keep operational signals clear; identity, context and atmosphere are also valid roles.')
    change(p,'One scale, few sizes, weight before size for hierarchy, tabular numerals where numbers align.','Choose size, weight and measure together to make the hierarchy clear; use tabular numerals where numbers align.')
    change(p,'Pick a corner and spacing language that suits the character (tight and precise, soft and friendly) and apply it consistently: nested shapes take smaller radii than their containers; one gutter; a short spacing scale.',
      'Choose a related family of shapes and insets for the component roles. Judge curve, corner extent, dimensions and padding together at actual size. Nested shapes need a convincing gap, not simply the same token or an automatic smaller radius. For a soft continuous treatment, consult the optional `shape-language.md`; it is one visual choice, not the philosophy’s default.')
    change(p,'Flat by default; elevation only for what floats over content (popovers, a docked input, a dragged item). Hairlines before cards; a filled panel only for a genuinely grouped fact.',
      'Use surfaces, borders, space and elevation to make grouping and depth clear. A flat list may fit dense data; an inset object may help a person recognize and act on a meaningful thing. Judge the hierarchy and density rather than counting cards.')
    p=r/'references/decisions.md'
    change(p,'Group by meaning, separate with space and hairlines, and use one filled surface per screen at most for a grouped fact.','Group by meaning. Compare space, hairlines and surfaces for clarity and task fit; avoid arbitrary surface quotas.')
    change(p,'One colour per meaning, used for that meaning everywhere. When feedback changes "this link\'s colour", it changes the role.','Keep semantic colour roles consistent. Allow identity, context and atmosphere where they help without obscuring operational signals. Feedback about a colour may concern a role, so check its scope.')
    change(p,'No exclamation marks, filler or performed personality. Personality shows in precision and in a few well-chosen words.','Use a voice appropriate to the product and moment. Be precise about errors and commitments; give expressive copy room where it helps without patronizing or delaying the user.')
    p=r/'references/critique.md'
    change(p,'- Count the colours. Name the meaning of each. Any without a meaning, or any meaning with two colours?\n- Count the surfaces (cards, panels, filled boxes). Could a hairline or space do the job?\n- Count the different sizes, weights and radii on screen. Could fewer do the job?',
      '- Do colour, surfaces and expression strengthen hierarchy and character without confusing operational signals?\n- Do grouping and depth make the task clearer at the required density? Compare a simpler treatment if they compete.\n- Do type, shape, proportions and insets form a convincing whole? Consistency alone does not establish that.')
    change(p,'- Where is the one distinctive moment? Is it at the product\'s differentiator, and does it explain something?\n- Is the personality quiet (mark, a phrase, a motion) and never at usability\'s expense?',
      '- What gives this product its own character? Does it emerge from the composition and task, or only a decorative flourish?\n- Is the amount of expression appropriate to its users and context, with familiar paths still easy to use?')
    change(p,'Write down: the three weakest things you found, what you changed, and what still needs a human eye or the real environment. Then fix and look again.',
      'Judge composition and character separately from functional checks. Review the whole task across its initial, active, pending, completed and return states where relevant. Write down the three weakest things, what changed, and what still needs a human eye. A consistent system can still need a better composition. Fix and look again.')
    (r/'references/shape-language.md').write_text('''# Optional soft continuous shape language

Read when a softer treatment suits this product, its platform and users. This is a visual option, not a required style. The user prefers **Adjusted Squircle** among the tested treatments: a larger corner extent with continuous-looking curves, balancing softness and structure. Preserve that preference when choosing this aesthetic; compact or conventional geometry can fit other contexts better.

## Choose relationships, not one radius

Judge curve family, corner extent, component proportions and surrounding insets together. Give outer panels, compact controls, data marks, capsules and circles roles of their own. Nested forms need a convincing, even-looking gap. An inner radius is not automatically the outer radius or a fixed percentage of it; inspect the actual silhouette and content clearance.

The accompanying `shape-comparison.svg` illustrates an ordinary corner, a same-extent exponent-four corner and an adjusted exponent-four corner. It is an explanatory drawing, not a Dia asset. In the shared reference pack, the composer shows a soft shell with smaller inset context objects; profile settings and Arc routing show useful compact counterexamples. Their exact curve implementations are unconfirmed. A capsule or compound tab outline is not a four-corner squircle.

## Adjusted Squircle as a starting treatment

In a browser with support, CSS `corner-shape: squircle` uses exponent four, whereas ordinary `border-radius` uses quarter-ellipse corners. At the same numerical radius it can look squarer. In the controlled experiment, increasing the extent by about 1.841 matched one diagonal inset to the ordinary corner. That multiplier is a comparison control, not a mandatory scale, an optical guarantee or an exact Apple/Dia formula.

Start from the intended silhouette, then tune extent for the component’s dimensions, label inset and neighboring shapes. Preserve circular avatars, semantic clipped data ends and compact platform controls where appropriate. Inspect focus rings, borders, shadows, clipping, resizing, large text and both themes. Use a normal rounded fallback when the platform cannot render the selected curve; do not clip away focus or text to simulate it.

The reusable decision is whether this shape family helps this product. Record why it fits or why a different family serves the task better. Soft curves alone do not establish hierarchy, personality or overall design quality.

Sources: [Apple continuous corners](https://developer.apple.com/documentation/swiftui/roundedcornerstyle/continuous), [CSS corner shaping](https://www.w3.org/TR/css-borders-4/#corner-shaping), [Dia’s platform-specific radius refinements](https://www.diabrowser.com/release-notes/1-15-1-polish-galore). The study does not establish Dia’s formula.
''')
    # Simple offline illustration, not a production shape specification.
    def shape(x,y,w,h,rad,n):
        import math
        pts=[]
        for q,(cx,cy) in enumerate(((w-rad,rad),(w-rad,h-rad),(rad,h-rad),(rad,rad))):
            for j in range(41):
                a=-math.pi/2+q*math.pi/2+j*math.pi/80;c=math.cos(a);s=math.sin(a)
                pts.append((x+cx+rad*math.copysign(abs(c)**(2/n),c),y+cy+rad*math.copysign(abs(s)**(2/n),s)))
        return 'M'+' L'.join(f'{a:.3f},{b:.3f}' for a,b in pts)+' Z'
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="720" height="190" viewBox="0 0 720 190"><rect width="720" height="190" fill="#f5f5f2"/>'
    for i,(label,rad,n) in enumerate((('Ordinary',24,2),('Same extent',24,4),('Adjusted Squircle',24*1.840896415,4))):
        svg+=f'<path d="{shape(20+i*240,20,200,100,rad,n)}" fill="#d8e1db" stroke="#33463a"/><text x="{120+i*240}" y="150" text-anchor="middle" font-family="sans-serif" font-size="16">{label}</text>'
    (r/'references/shape-comparison.svg').write_text(svg+'</svg>')
    diff=''
    for file in sorted(set(FILES+['references/shape-language.md','references/shape-comparison.svg'])):
        b=STUDY/'skills/baseline'/file;v=STUDY/'skills/revision'/file
        diff+=''.join(difflib.unified_diff(b.read_text().splitlines(True) if b.exists() else [],v.read_text().splitlines(True) if v.exists() else [],fromfile='baseline/'+file,tofile='revision/'+file))
    (STUDY/'revision.diff').write_text(diff)

if __name__=='__main__':make_revision()
