# Notes for agents working on the incident board

## UI and design
- Any change to the interface follows `design/SYSTEM.md` (this project's own design system). Read it first.
- New values go in `app/tokens.css`, never inline. `node --test tests/*.test.js` runs the design guard test.
- For new UI work, use the `design-philosophy` skill's method (understand → references → audit → direction → system → implement → verify → record), but this project's SYSTEM.md decides its look.
- Record verified design changes and open items in `DESIGN.md` (section "Verification" and "Open items").
