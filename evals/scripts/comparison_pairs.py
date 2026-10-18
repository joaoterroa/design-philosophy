"""Semantic state mapping for iteration 1; never edits the original prototypes.

Routes come from the six DESIGN.md files and their app routers. None means the
other run has no equivalent *at that point in the flow*, not that it lacks all
related behaviour. Keep captions descriptive: these are inputs to a human vote.
"""

SIDES = ("with", "without")
EVALS = ("oncall-menubar", "incident-dashboard", "banking-onboarding")


def pairs():
    rows = []

    def add(evaluation, screen, title, size, routes, caption, **extra):
        rows.append(dict(eval=evaluation, screen=screen, title=title,
                         viewport=list(size), routes=dict(zip(SIDES, routes)),
                         caption=caption, themes=["light", "dark"], **extra))

    menu = [
        ("oncall", "On call · main panel", "oncall", "on", "With: a shift strip above the rotation list. Without: a Now/Schedule tab bar and a next-shifts section."),
        ("compose", "Composing a handover", "compose", "choose", "With: an eight-hour range and availability on each candidate. Without: a thirteen-hour range and a disclosure for less suitable candidates."),
        ("pending", "Waiting for acceptance", "pending", "pending", "With: an outlined, hatched segment marked PR?. Without: a striped segment labelled Priya?. Both say the shift remains yours."),
        ("offline", "Offline · cached schedule", "offline", "offline", "With: cached-data age sits in the footer, with a connection explanation below Hand over. Without: an offline notice follows the next-shifts section. Both disable handover."),
        ("offcall", "Not on call", "offcall", "off", "With: the next shift appears in the main answer. Without: a separate next-shifts section follows the rotation list."),
        ("accepted", "Handover accepted", "accepted", "accepted", "With: the accepted interval remains on the multi-day strip. Without: the remainder is labelled with Priya's name on the shift bar."),
        ("declined", "Handover declined", "declined", "declined", "With: the reply appears below the shift strip as plain text. Without: the reply has a tinted notice inside the current-shift panel."),
        ("incoming", "Incoming handover request", "incoming", "incoming", "With: the request appears before your own shift. Without: the request replaces the main you-panel and includes a rota check."),
        ("send-failed", "Handover could not be sent", "sendfail", None, "Only in with: an in-place send failure keeps the handover form and states that nothing changed."),
        ("coverage-gap", "Coverage gap · main panel", "gap", None, "Only in with: a gap warning appears in the main panel. Without has gap information in its separate Schedule view."),
        ("loading", "First sync", "loading", None, "Only in with: a first-sync spinner and a connecting message in an otherwise empty panel."),
        ("connect", "Not connected · first run", "connect", None, "Only in with: a first-run sign-in state before a schedule is connected."),
        ("schedule", "Weekly schedule", None, "schedule", "Only in without: a dedicated Schedule tab with a seven-day rotation view and a named gap."),
    ]
    for screen, title, with_state, without_state, caption in menu:
        routes = (f"?state={with_state}&theme={{theme}}" if with_state else None,
                  f"?theme={{theme}}#{without_state}" if without_state else None)
        add(EVALS[0], screen, title, (1100, 800), routes, caption,
            crop={"with": "#popover", "without": "#pop"})

    dashboard = [
        ("live", "Live · SEV1, no commander", "live", "major", "With: the missing commander sits in the SEV1 row and the on-call band. Without: it is called out in a banner and an on-call card; the SEV1 is repeated in the list."),
        ("stale", "Data stale", "stale", "stale", "With: an amber freshness header retains the incident list. Without: an inverse warning replaces the status banner and dims the data. Fixture ages differ (about six versus seven minutes)."),
        ("all-clear", "All clear", "allclear", "clear", "With: zero-open wording leads into resolved history. Without: an all-clear banner includes days since the last SEV1. The runs invented different history and budget values."),
        ("loading", "Loading", "loading", "loading", "With: row-shaped placeholders reserve the list and chart areas. Without: loading messages occupy the dashboard's existing panels."),
        ("rota-failed", "Rota source failed", "partial", None, "Only in with: the rota source fails while incident and metric data remain live; this is not the whole-feed failure on the other run."),
        ("surge", "Surge · twelve open incidents", "surge", None, "Only in with: twelve open incidents; TV names the rows that cannot fit, while laptop can scroll."),
        ("commander-set", "SEV1 · commander assigned", None, "major-ic", "Only in without: Ana L. is assigned as incident commander in the live SEV1 state."),
        ("sev2-only", "SEV2 only", None, "elevated", "Only in without: the SEV1 has resolved and the headline changes to the remaining SEV2 incidents."),
        ("feed-down", "Entire feed down", None, "error", "Only in without: the entire incident feed is unavailable; this differs from losing just the rota source."),
    ]
    for display, size in (("tv", (1920, 1080)), ("laptop", (1440, 900))):
        for screen, title, with_state, without_state, caption in dashboard:
            routes = (f"?display={'wall' if display == 'tv' else 'desk'}&state={with_state}&theme={{theme}}&frozen" if with_state else None,
                      f"?display={display}&state={without_state}&theme={{theme}}&kiosk" if without_state else None)
            add(EVALS[1], f"{display}-{screen}", f"{display.upper() if display == 'tv' else 'Laptop'} · {title}", size, routes, caption)
        add(EVALS[1], f"{display}-original", f"{display.upper() if display == 'tv' else 'Laptop'} · original (before)", size,
            ("", ""), "Both: the same unmodified original dashboard. This is shared context, not a with/without design result. The original has no dark theme.",
            source="dashboard/index.html", themes_override=["light"], reference=True)

    banking = [
        ("welcome", "Welcome", "welcome", "welcome", "With: setup requirements and a Start button share the welcome screen. Without: two account-status choices lead to a separate preparation screen."),
        ("details-errors", "Account details · errors", "details-errors", "details-errors", "With: errors concern the long card number and date of birth. Without: errors concern date of birth, sort code and account number. Both use a summary plus field errors."),
        ("code", "Enter the texted code", "code", "code", "With: the code input and Continue come before a preview with blank code digits. Without: a preview containing 482 913 comes before the input."),
        ("done", "Done", "done", "done", "With: balance and last money in follow the setup confirmation. Without: a balance panel precedes reminders that card and branch banking remain available."),
        ("details", "Account details", "details", "details", "With: long card number and date of birth, plus an alternate account-number route. Without: date of birth, sort code and account number are the default route."),
        ("not-found", "Account not found", "details-notfound", "checking-nomatch", "With: the no-match message stays on the details form. Without: no match has its own result screen. Both represent the same failed account lookup."),
        ("code-wrong", "Text code · wrong", "code-wrong", "code-wrong", "With: an inline wrong-code message leaves the field high on the page. Without: a summary precedes the preview and code field. Both name the remaining tries."),
        ("code-help", "Text code · delivery help", "code-help", "code-help", "With: delivery help expands within the code screen, with a new-code notice. Without: a separate help screen offers resend, a voice call and changed-number guidance."),
        ("passcode", "Choose a passcode", "passcode", "passcode", "With: passcode and confirmation are on one screen. Without: confirmation is a separate step."),
        ("passcode-errors", "Passcode · easy to guess", "passcode-errors", "passcode-easy", "With: the two-field form rejects a sequential passcode. Without: an error summary and message appear on the first passcode screen."),
        ("biometrics", "Optional biometrics", "biometrics", "fingerprint", "With: face or fingerprint includes a warning about other people enrolled on the phone. Without: fingerprint is offered alongside a full-size passcode-only option."),
        ("help", "Account details · help sheet", "?help=1#details", "help", "With: help explains the card-number route and its alternative. Without: help explains where to find sort code and account number, with a card illustration."),
        ("details-nocard", "Alternative · no card", "details-nocard", None, "Only in with: an explicit alternate identification route. Without already uses sort code and account number by default (see Account details)."),
        ("code-expired", "Text code expired", "code-expired", None, "Only in with: an expired-code message and a new-code action; this differs from the other run's session-timeout dialog."),
        ("code-locked", "Text code · attempt limit", "code-locked", None, "Only in with: a dedicated attempt-limit state replaces the code form."),
        ("working", "Final setup · working", "working", None, "Only in with: named connection tasks after biometrics. Without's checking states happen earlier, before text-code verification."),
        ("working-slow", "Final setup · slow", "working-slow", None, "Only in with: a delayed final-setup state keeps the connection tasks and adds reassurance."),
        ("working-failed", "Final setup · failed", "working-failed", None, "Only in with: a final-setup failure explains that the account has not changed and offers retry."),
        ("prepare", "Before you start", None, "prepare", "Only in without: a dedicated preparation screen. With puts requirements on its welcome screen."),
        ("new", "New customer guidance", None, "new", "Only in without: people without an existing account are directed to assisted account opening."),
        ("checking", "Identity check · working", None, "checking", "Only in without: named identity-check tasks before the text-code step; with moves directly from valid details to code."),
        ("checking-slow", "Identity check · slow", None, "checking-slow", "Only in without: the identity check explains a longer-than-usual wait."),
        ("checking-veryslow", "Identity check · very slow", None, "checking-veryslow", "Only in without: an extended identity-check delay offers a way to stop and keep the entered details."),
        ("checking-failed", "Identity check · failed", None, "checking-failed", "Only in without: a failure before text verification says no money moved and offers retry."),
        ("timeout", "Session timeout warning", None, "timeout", "Only in without: a modal offers more time or stopping. With deliberately has no screen timeout."),
        ("passcode-confirm", "Confirm passcode · separate step", None, "passcode-confirm", "Only in without: passcode confirmation has its own screen. With combines both fields (see Choose a passcode)."),
        ("passcode-mismatch", "Confirm passcode · mismatch", None, "passcode-mismatch", "Without: mismatch is on the separate confirmation step. With also validates mismatches, on its combined form; captured via that form here."),
        ("safety", "Standalone safety advice", None, "safety", "Only in without: a separate scam-advice acknowledgement. With places scam advice alongside text-code verification."),
    ]
    for width, height in ((390, 844), (320, 568)):
        for screen, title, with_state, without_state, caption in banking:
            def route(state):
                if state is None:
                    return None
                if state.startswith("?"):
                    return state.replace("?", "?theme={theme}&", 1)
                return f"?theme={{theme}}#{state}"
            routes = (route(with_state), route(without_state))
            if screen == "passcode-mismatch":
                routes = ("?theme={theme}#passcode", routes[1])
            add(EVALS[2], f"{width}-{screen}", f"{title} · {width} px", (width, height), routes, caption,
                action="passcode-mismatch" if screen == "passcode-mismatch" else None)
    for row in rows:
        row["themes"] = row.pop("themes_override", row["themes"])
    return rows
