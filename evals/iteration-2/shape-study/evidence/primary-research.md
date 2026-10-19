# Browser Company shape evidence

Investigated 2026-10-18. This is a targeted visual audit, not a census of all Dia releases or screens. Existing local images come from the first-party evidence collection in `../../browser-company-study/evidence/catalog.json`; its URLs, dates, dimensions, and hashes identify each image. No native application source or editable design file was available.

## Finding

Rounded geometry is a recurring part of the visible design language. The evidence supports a **family of shapes and proportions**: rounded window and sheet edges, rounded rectangular tiles and inputs, pill actions, circular controls, and compound tab silhouettes. It does not establish one universal squircle formula. Exact continuous curvature remains unconfirmed for the observed Dia and Arc components.

The strongest direct statement is Dia's January 23, 2026 release note: the company was adjusting window and menu corner radii for macOS Tahoe. This confirms deliberate work on this detail and a platform-dependent treatment; it does not disclose the curve equation or API. [Dia: Better organization, better context](https://www.diabrowser.com/release-notes/1-15-1-polish-galore).

## Terms that should stay separate

| Term | What can be said precisely |
|---|---|
| Conventional rounded rectangle | Straight sides joined by circular or elliptical corner arcs. CSS `border-radius`, with the default corner shape, describes quarter-ellipse corners. |
| CSS squircle corner | The CSS specification defines `squircle` as `superellipse(2)`, which uses exponent 4. It changes the curve within the region set by `border-radius`; it is not merely a larger radius. |
| Continuous corner | A curve whose curvature changes smoothly toward the side. Apple's SwiftUI API explicitly distinguishes its continuous style from its circular style. This is an API description, not proof that every Apple-like shape follows one mathematical superellipse. |
| Pill or capsule | A long control with fully rounded ends. Its silhouette alone does not establish a distinctive squircle treatment. |

The CSS definitions and parameters are documented in the [CSS Borders and Box Decorations Level 4 draft, sections 3.5–3.7](https://drafts.csswg.org/css-borders-4/#corner-shaping). This is a working draft, dated October 15, 2026 when inspected. Apple documents [continuous corners](https://developer.apple.com/documentation/swiftui/roundedcornerstyle/continuous) and [circular corners](https://developer.apple.com/documentation/swiftui/roundedcornerstyle/circular) separately.

Do not equate CSS `squircle`, Figma smoothing, and Apple's continuous style without a comparison. They are separate named constructions. Increasing a conventional radius can also change apparent softness much more than a small change of curve at a tiny corner.

## Direct visual examples

These seven deliberately selected UI examples span composing, browsing, profile creation, icon selection, signup, recovery, and routing. Every example contains some rounded geometry. That is an observation about this sample, not a usage percentage across either product. The sample is biased toward published closeups and excludes many invisible and transient states.

| Example and provenance | Visible evidence | What is not established |
|---|---|---|
| Dia composer, published June 17, 2025. Local `assets/dia-strategy-05.png`. [Design article](https://browsercompany.substack.com/p/the-strategy-behind-dias-design). | Rounded outer composer, inset rounded context tile, smaller rounded favicon mount, pill-shaped Chat action. Distinct levels rather than one radius everywhere. | Exact curvature. Image is an isolated component presentation. |
| Dia browser/tab closeup, same article/date. Local `assets/dia-strategy-02.png`. [Design article](https://browsercompany.substack.com/p/the-strategy-behind-dias-design). | Window corner, content edge, and a selected tab with convex upper corners and concave lower joins. Tab joins connect the tab to the page field. | A tab is not a four-corner squircle. This enlarged closeup cannot prove normal viewing-scale impact. |
| Dia Create a Profile, official demo January 23, 2026, frame 5s. Local `research-assets/dia-profile-colors-5s.png`. [Product release](https://www.diabrowser.com/release-notes/1-15-1-polish-galore). | Modestly rounded modal, field, and buttons coexist with a much rounder composer and pill Add tabs action behind it. | Rounded does not mean identical geometry; the demo includes zoom and cropping. |
| Dia icon picker, same release, frame 6s. Local `research-assets/dia-tab-icon-picker-6s.png`. [Product release](https://www.diabrowser.com/release-notes/1-15-1-polish-galore). | Rounded tab, profile control, picker edges, segmented controls, circular window controls; picker has an anchoring pointer. | The popover is a compound outline, not a pure superellipse. |
| Dia signup, undated official crop, accessed October 18, 2026. Local `research-assets/dia-onboarding.png`. [Installation page](https://www.diabrowser.com/download/thanks). | Ordinary rectangular inputs and a compact rounded Sign Up button. It remains plain despite the brand. | Only a crop is shown; no whole-window or flow inference. |
| Arc Recovery Card, historical macOS help image, article recorded as updated November 5, 2024 in the prior catalog. Local `research-assets/arc-sync-recovery.png`. [Recovery help](https://resources.arc.net/hc/en-us/articles/22370005382167-Recovery-Cards). | Rounded outer sheet and a black rounded recovery object with an inset border, alongside ordinary buttons. Visual identity comes from the recovery object as well as its corners. | No exact shape implementation. Sensitive content is obscured by the publisher. |
| Arc Air Traffic Control, historical macOS help screenshot; same recorded update date. Local `research-assets/arc-air-traffic-route.png`. [Routing help](https://resources.arc.net/hc/en-us/articles/22932014625431-Air-Traffic-Control-Automate-Your-Link-Routing). | Conventional sheet, small-radius fields, standard dropdown controls. It is a useful counterexample to large-radius styling everywhere. | Native-looking controls do not prove a specific AppKit implementation. |

## Why the geometry matters: interpretation

The visible relationships are more secure evidence than exact curve classification. A large rounded composer encloses smaller related forms. A tight field radius supports a compact settings task. A tab's concave lower joins connect it to content instead of making it a separate floating card. Circular window controls sit among rectangular structures. These differences help separate roles while keeping the overall interface coherent.

At normal scale, a curve works with its surrounding space, border, contrast, type size, and dimensions. A very soft outer corner with cramped text can look less considered than a conventional corner with a well-judged inset. This is a design hypothesis to test, not a measured preference result.

## Platform evidence and attribution limits

Apple's WWDC25 AppKit presentation explains that Tahoe window radii vary with window style. Toolbar windows use a larger radius that nests around toolbar elements; titlebar-only windows retain a smaller one. It also warns that the larger corners can clip nearby content and introduces corner-aware layout regions. This supports treating corner and spacing relationships together. It does not mean the Browser Company invented, or necessarily uses, the exact examples shown. [Build an AppKit app with the new design](https://developer.apple.com/videos/play/wwdc2025/310/).

Apple separately defines concentric nested corners as deriving the inner radius from the container radius and the distance between them. That is explicit platform guidance, not a confirmed Browser Company rule. [SwiftUI concentric corner style](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric).

Some of the softness the user recognizes can therefore be shared with native macOS design. Dia's documented Tahoe adjustments make platform and release date important controls when comparing references. A 2025 crop, a 2026 Tahoe menu, and a Windows view should not be treated as one fixed shape specification.

## What this evidence can and cannot establish

- Confirmed: rounded geometry recurs in multiple real product contexts; treatments differ by role; Dia has explicitly refined window/menu radii for Tahoe.
- Inferred visually: several outlines are compatible with smoothed or continuous corners. Compatibility is not identification.
- Unconfirmed: the proportion of components using continuous curves; precise smoothing values; universal squircle tokens; the native curve code; whether curve smoothing itself causes preference or brand recognition.
- Not established by a screenshot: whether a shape follows a component through an interaction, how hit testing follows the painted edge, or how it responds to resizing.

Compressed video frames, screenshot scaling, anti-aliasing, shadows, and unknown device pixel ratios can conceal subpixel differences. One can fit several plausible curves to a small visible corner. Do not label the entire sample as “true squircles” or claim a numeric adoption rate.

## Implications for a controlled experiment

Separate three variables: curve family, corner extent, and the relationship of nested corners to their spacing. A same-radius round-versus-squircle comparison isolates the curve but does not equalize perceived softness or enclosed area. A second comparison can compensate the corner extent explicitly; describe that as an adjusted shape treatment, not a pure curve test. Keep wording, typography, color, dimensions, task states, and layout unchanged in the first pass. Check painted borders, focus outlines, and clipping as well as screenshots.

Chrome shipped CSS corner shaping in version 139 on August 5, 2025. This enables an offline headless Chromium experiment with `corner-shape` and a conventional-radius fallback. Its availability does not prove Dia's own native chrome uses CSS. [Chrome 139 release notes](https://developer.chrome.com/release-notes/139).

The reusable principle supported here is to choose and evaluate a coherent shape family in context. The specific continuous-corner family belongs in an optional visual treatment or reference, pending a preference comparison. A mandatory “squircle all controls” rule has no support in these examples.
