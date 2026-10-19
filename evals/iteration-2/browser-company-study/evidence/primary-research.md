# Primary product research: Dia and Arc

Researched 18 October 2026. This note deliberately separates **visible evidence**, **first-party descriptions**, and **inferences**. It does not assume that adding decoration improves a design. It does not evaluate the generated prototypes; that comparison belongs in the main study.

## Scope and limits

These are official product images, help-center screenshots, and frames extracted from official short feature demonstrations. They are stronger evidence of actual controls than brand illustrations, but remain curated examples. They are not a usability study or a current authenticated product inspection. No typography family is identified from a screenshot alone. Demo frames establish states and their sequence; they cannot establish perceived motion quality, haptics, sound, timing tolerance, or accessibility. Where frames are cropped by the source, no full-window proportion is inferred.

Arc screenshots are older. Arc help JSON reports the relevant articles updated 5 November 2024. Dia evidence spans December 2025–April 2026, with separate release descriptions extending later. Avoid presenting these as a single timeless/current UI.

## A. Dia: ordinary signup and chat entry (two usable controls)

Source: [Installing Dia](https://www.diabrowser.com/download/thanks), undated page accessed 18 October 2026.

| Evidence | Local asset | Exact asset URL |
|---|---|---|
| Signup crop | [dia-onboarding.png](research-assets/dia-onboarding.png) | [750×450 PNG](https://cdn.sanity.io/images/e5fj2khm/production/3dedbdf2a554303eeee27d1257d85a5d757583f8-750x450.png) |
| Browser Chat button crop | [dia-chat-button.png](research-assets/dia-chat-button.png) | [750×450 PNG](https://cdn.sanity.io/images/e5fj2khm/production/d4bd2ab6be1b2785184a90cb6f5fcb31e823d32f-750x450.png) |

**Visible:** Signup uses plain email/password labels, white rounded inputs, and a black compact action with a Return-key hint. Chat is a dark speech icon plus a literal label in a pale rounded button. Neither control needs expressive typography or an unusual metaphor. These are enlarged presentation crops, not full onboarding/chat screens.

**Inference:** Ordinary, familiar execution is compatible with Dia. A gap analysis should not count all convention as failure. The more useful question is whether familiarity supports a larger authored interaction. Do not claim that this asset proves Dia has a distinctive full onboarding flow.

## B. Dia: tab identity, profile settings, and group closure (three demos)

Source: [Better organization, better context](https://www.diabrowser.com/release-notes/1-15-1-polish-galore), 23 January 2026. The page title's `1-15-1` slug differs from the dated [1.15.0 changelog](https://www.diabrowser.com/changelog/mac/1-15-0); preserve that distinction.

**Visible:** Tab customization changes a Google Docs favicon into a brain emoji without moving the tab. Profile settings use familiar toolbar icons, list selection, and colored chips; the creation sheet has one field and restrained actions. Closing a meeting group removes its expanded rows while a matching compact group remains in the bookmarks region. The source crop and colored desktop backdrop must not be confused with application chrome.

**Inference:** Personal character can attach to useful, persistent objects. Familiar controls coexist with expressive identity; it is not necessary to redesign every menu. The spatial relationship between expanded work and its compact resting form may matter more than a generic success toast.

Timed frames inspected (not a claim to have watched the continuous video):

| Demo | Original public video and duration from page metadata | Inspected local frames |
|---|---|---|
| Tab-icon picker | [MP4](https://stream.mux.com/JdNhe14UfVhkyudx029rQ6qe018GyMEo00RInyocRQM7PE/highest.mp4), 9.65s | [0s](research-assets/dia-tab-icon-picker-0s.png), [3s](research-assets/dia-tab-icon-picker-3s.png), [6s](research-assets/dia-tab-icon-picker-6s.png), [9s](research-assets/dia-tab-icon-picker-9s.png) |
| Profile colors | [MP4](https://stream.mux.com/kS1qBXHjLYEqMvaYU6dJbQONneVJweVbxxphjT5f4Wo/highest.mp4), 19.216667s | [0s](research-assets/dia-profile-colors-0s.png), [5s](research-assets/dia-profile-colors-5s.png), [10s](research-assets/dia-profile-colors-10s.png), [15s](research-assets/dia-profile-colors-15s.png) |
| Close groups | [MP4](https://stream.mux.com/01YUTPuLqZK00NhYiSzhKZFrlEfi8RsHftLE01UvwfVChM/highest.mp4), 3.783333s | [0s](research-assets/dia-close-groups-0s.png), [1s](research-assets/dia-close-groups-1s.png), [2s](research-assets/dia-close-groups-2s.png), [3s](research-assets/dia-close-groups-3s.png) |

The corresponding `*-poster.webp` files are first-party video posters. They are not independently timed captures.

## C. Dia: grouped work as a visual object

Source: [Organize your Tabs](https://www.diabrowser.com/release-notes/1-9-0-tab-groups), 11 December 2025.

**Visible in inspected posters:** Compact colored group labels carry small clusters of real app favicons; the selected tab joins its content area. A hover preview lists member pages immediately under the relevant group. A context menu embeds color selection and leads into an emoji/icon picker. Another view puts a closed group in the bookmark area. Native-looking grey menus coexist with pastel grouped objects.

**Described by source:** Groups expand/collapse, can be renamed/recolored, and persist in the bookmarks bar when closed. This supports the interpretation but is not a measured usability result.

**Inference:** Organization is represented as manipulable content with recognizable identity. That differs from merely adding a color accent to a conventional table. Underlying judgment to test: preserve identity across representations and expose the action at the object. Do not transplant tab groups into unrelated applications.

| Poster asset | Public original (first-party poster) |
|---|---|
| [dia-groups-create-poster.webp](research-assets/dia-groups-create-poster.webp) | [Create/hover group poster](https://image.mux.com/FAVBjAU7pSAeFlcxwuTPnXIlRmHg18XNy3mDUcS8Ryk/thumbnail.webp?width=1600&fit_mode=preserve) |
| [dia-groups-customize-poster.webp](research-assets/dia-groups-customize-poster.webp) | [Customize poster](https://image.mux.com/RlFU5ByaXbqbuJi7tDeEH02CHoABzbwFtCeV3sZnG8eM/thumbnail.webp?width=1600&fit_mode=preserve) |
| [dia-groups-storage-poster.webp](research-assets/dia-groups-storage-poster.webp) | [Stored groups poster](https://image.mux.com/PkwMO32i4Hgt3GrBXI51DJy3BD00KkNK9CmuNo01np101s/thumbnail.webp?width=1600&fit_mode=preserve) |

## D. Arc: security that becomes a specific object; routine status stays routine

Source: [Recovery Cards](https://resources.arc.net/hc/en-us/articles/22370005382167-Recovery-Cards), updated 5 November 2024 according to [public article JSON](https://resources.arc.net/api/v2/help_center/en-us/articles/22370005382167.json).

**Visible:** A recovery sheet gives the recovery phrase a large black card with an inset border, interrupted top border for a label, privacy marking, small Arc mark, and a bottom band. Its surrounding modal and Download/Copy controls remain conventional. A separate sync-status crop uses a plain row, toggle, green status dot, explanatory text and underlined links.

**Inference:** Even security can have a memorable, purposeful object without making the surrounding settings novel. The card reinforces what to save and protect. This is better evidence for concentrated expression than a claim that every TBC surface must be playful. The screenshot is a help-center example with obscured recovery text, not a current account.

Assets: [recovery sheet](research-assets/arc-sync-recovery.png), [sync-status crop](research-assets/arc-sync-settings.png). Originals: [recovery](https://resources.arc.net/hc/article_attachments/22369994728599), [status](https://resources.arc.net/hc/article_attachments/22369994734999).

## E. Arc: settings can be very conventional

Source: [Air Traffic Control](https://resources.arc.net/hc/en-us/articles/22932014625431-Air-Traffic-Control-Automate-Your-Link-Routing), updated 5 November 2024 per [public article JSON](https://resources.arc.net/api/v2/help_center/en-us/articles/22932014625431.json).

**Visible:** Routing is a regular sheet with two-line URL/destination rows, text fields, dropdowns, remove controls, and a default destination at the bottom. The surrounding Links preferences use standard toolbar navigation, checkboxes, separators, and ordinary prose. Their instructional image carries a large external red arrow, which is an annotation, not product UI. A big browser illustration belongs to this explanatory settings surface.

**Inference:** Being recognizable as TBC does not require visual tension in every widget. The naming and overall flow can carry authorship while controls preserve platform familiarity. Avoid using this example to justify a custom visual system everywhere.

Assets: [Links settings](research-assets/arc-air-traffic-control.png), [route sheet](research-assets/arc-air-traffic-route.png). Originals: [settings](https://resources.arc.net/hc/article_attachments/22932014613911), [routes](https://resources.arc.net/hc/article_attachments/22932014616343).

## F. Arc: expressive ownership lives in actual settings

Source: [How Do I Unlock Special App Icons?](https://resources.arc.net/hc/en-us/articles/21886232998807-How-Do-I-Unlock-Special-App-Icons), updated 5 November 2024 per [public article JSON](https://resources.arc.net/api/v2/help_center/en-us/articles/21886232998807.json).

**Visible:** A native-looking Icon preferences pane presents substantial icon artwork as a selectable collection: original, translucent candy treatment, hologram and neon. One includes a designer credit. List rows, radio choices, current-selection text, and explanatory referral column support that expressive content.

**Inference:** The app permits personal attachment and taste without making its control language unpredictable. This is a product feature rather than a decorative marketing backdrop. It is also a referral mechanism: do not assume pure user benefit or universal suitability.

Asset: [arc-icons-settings.png](research-assets/arc-icons-settings.png). [Exact original PNG](https://firebasestorage.googleapis.com/v0/b/bcny-arc-server.appspot.com/o/easelImages%2FB3087598-54E5-4DB2-B770-B2BE7D314293.png?alt=media&token=6db73a3a-671a-42b8-90e6-1a40b64d1389), linked in the official article. This screenshot includes a salmon presentation backdrop outside the app window.

## G. Dia: skill flow evidence is descriptive, not a visually inspected builder

[Dia 1.0.1](https://www.diabrowser.com/changelog/mac/1-0-1), 9 October 2025, describes an independently editable popup builder, distinct steps, tool/format mentions and token shimmer. [Dia 1.2.0](https://www.diabrowser.com/changelog/mac/1-2-0), 24 October 2025, describes creation from a short sentence, generated name/icon, relevant tools, follow-up questions and an approval step. These are usable primary descriptions of product decisions, not evidence of precise layout or animation.

The inspected January profile-demo 0s frame shows Skills and Learn Skills below the main input, with Skills/Personalization also near the browser top. This does **not** establish the actual builder layout. A fuller builder comparison needs more direct evidence. The main study should not invent it from the text.

## H. Dia changed: counterexamples to an immutable aesthetic

Each entry has its own source to avoid deriving the entire history from one undifferentiated changelog.

- [1.15.0, 23 January 2026](https://www.diabrowser.com/changelog/mac/1-15-0): describes a profile-colored new-tab gradient with shimmer. Expression can appear in the resting spatial field, not solely a high-importance feedback state. Exact motion was not verified here.
- [1.20.0, 26 February 2026](https://www.diabrowser.com/changelog/mac/1-20-0): describes Spotify album art on hover, pulse feedback tied to volume, separate color-tinted split panes and shimmer while naming a group. It also limits first-week suggestions to two and lets them disappear. These are task-linked behaviors; the source does not establish that they all improve usability.
- [1.23.0, 19 March 2026](https://www.diabrowser.com/changelog/mac/1-23-0): describes PR completion feedback, clearer cleanup and hover recall. This makes the end of work a designed stage rather than a bare empty state.
- [1.28.0, 23 April 2026](https://www.diabrowser.com/changelog/mac/1-28-0): describes tighter tab spacing, neutral group colors by default and more accurate page/chrome color matching. This directly counters a recommendation to maximize color or looseness everywhere.
- [Onboarding without tab overload](https://www.diabrowser.com/release-notes/1-16-0-organization-that-grows), 29 January 2026: the head of design distinguishes Dia's progressively discoverable organization from Arc's up-front complexity. Treat this as stated intent, not independent proof of user outcomes.
- [Stash your PiP out of the way](https://www.diabrowser.com/release-notes/1-36-0-pip-stash), 18 June 2026: describes a PiP moved beyond the screen edge and retrieved by click/drag; content grouping follows meeting work. It links to [Christine's own process post](https://x.com/chrstnerode/status/2065070625970946175?s=20), but that post could not be read through the research tool. Do not cite its supposed conclusions.

## Working hypotheses for the main comparison (inferences, not findings about our outputs)

1. **Expression has a job and a location.** Group identity, a recovery card, a personal icon collection, or finishing a PR can justify different treatments. A global palette change would test a weaker hypothesis.
2. **A useful object persists through the workflow.** The relevant test is whether a user's thing stays recognizable through compact, expanded, pending, complete and stored forms. Static screenshot tests under-sample this.
3. **Platform familiarity is a baseline, not a disqualification.** Plain signup and routing controls counter a blanket demand for novelty.
4. **The user supplies part of the character.** Named work, actual favicons, an emoji chosen for intent, profile colors and icon selection make an environment feel owned. A sterile fixture or decorative mascot does not test the same mechanism.
5. **Restraint and expression are jointly edited.** A later product release can reduce default color while preserving richer behavior. The transferable lesson is selection and iteration, not an always-colorful or always-minimal style.

These hypotheses should face an adverse test: retain the generated interface's functional requirements, change one mechanism, and compare states and behavior. A more charming screenshot alone cannot validate the principle.
