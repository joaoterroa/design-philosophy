## UI and design
- Any change to the onboarding interface follows `design/SYSTEM.md` (this project's own design system, "Counter Service"). Read it first.
- New values go in `app/tokens.css`, never inline. `node --test tests/*.test.js` runs the design guard test.
- `python tools/verify.py` renders every state (320/390/430px, light/dark, 200% text, help sheet) into `screenshots/` and runs overflow, target-size and keyboard checks.
- For new UI work, use the `design-philosophy` skill's method (understand, references, audit, direction, system, implement, verify, record), but this project's SYSTEM.md decides its look.
- Record verified design changes and open items in `DESIGN.md` (section "Open items").
