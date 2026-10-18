/* Sample data. Invented. "Now" is Sunday 18 October 2026, 18:47 in London.
   Hours in shift bars count from the shift's start. */
window.DATA = {
  now: { label: "Sun 18 Oct 18:47", clock: "Sun 18 Oct  18:47" },
  source: "PagerDuty",

  // The shift you are on in the on-call states.
  myShift: {
    rotation: "Core platform · primary",
    start: "Fri 17 Oct, 09:00",
    end: "Mon 20 Oct, 09:00",
    startShort: "Fri 09:00",
    endShort: "Mon 09:00",
    hours: 72,
    nowAt: 57.8, // Sun 18:47
    left: "14 h 13 m",
  },

  // The part you are handing over in the sample handover.
  handover: {
    to: "Priya Nair",
    toFirst: "Priya",
    from: "Sun 20:00",
    until: "Mon 09:00",
    fromAt: 59,
    length: "13 h",
    askedAgo: "3 min ago",
    declineNote: "Flying back from Porto tonight, sorry. Marta said she's around.",
  },

  // Who is on call right now, one row per rotation (escalation order).
  nowOn: [
    { rotation: "Core platform · primary", name: "You", initials: "JT", you: true, until: "Mon 09:00" },
    { rotation: "Core platform · secondary", name: "Rui Almeida", initials: "RA", until: "Mon 09:00", tz: "Lisbon" },
    { rotation: "Network & edge", name: "Tom Becker", initials: "TB", until: "Tue 09:00" },
    { rotation: "Databases", name: "Ananya Rao", initials: "AR", until: "Mon 09:00", tz: "Bengaluru 23:17" },
    { rotation: "Incident commander", name: "Helen Okafor", initials: "HO", until: "Mon 09:00" },
  ],
  nowOnWhenOff: { rotation: "Core platform · primary", name: "Daniel Whitfield", initials: "DW", until: "Mon 09:00" },

  myNext: [
    { rotation: "Databases · secondary", when: "Wed 22 Oct 18:00 → Thu 09:00", length: "15 h", inDays: "in 3 days" },
    { rotation: "Core platform · primary", when: "Fri 7 Nov 09:00 → Mon 09:00", length: "3 days", inDays: "in 20 days" },
    { rotation: "Incident commander", when: "Mon 24 Nov 09:00 → Tue 09:00", length: "24 h", inDays: "in 37 days" },
  ],

  // People who could take the shift, already ordered: free people on this
  // rotation first, longest since their last shift first; then people who
  // would double up or be up overnight; then people who are away.
  candidates: [
    { name: "Priya Nair", initials: "PN", tz: "London", why: "Free then · last on call 12 days ago" },
    { name: "Marta Sousa", initials: "MS", tz: "Lisbon", why: "Free then · last on call 9 days ago" },
    { name: "James Doyle", initials: "JD", tz: "London", why: "Free then · last on call 6 days ago" },
    { name: "Callum Reid", initials: "CR", tz: "London", why: "Free then · has covered 3 shifts this month" },
    { name: "Rui Almeida", initials: "RA", tz: "Lisbon", why: "On call as secondary then, so he would be primary and secondary at once", warn: true },
    { name: "Arjun Mehta", initials: "AM", tz: "Bengaluru", why: "00:30 → 13:30 his time, overnight", warn: true },
    { name: "Ananya Rao", initials: "AR", tz: "Bengaluru", why: "On call for Databases then, and overnight for her", warn: true },
    { name: "Sofia Marques", initials: "SM", tz: "Lisbon", why: "Away until Wed 22 Oct", away: true },
  ],
  rotationSize: 9,
  teamSize: 40,

  openIncident: { id: "INC-4821", title: "checkout-api elevated 5xx", detail: "SEV3, mitigated by rollback" },

  incoming: {
    from: "Tom Becker",
    first: "Tom",
    rotation: "Network & edge",
    when: "Tue 21 Oct 18:00 → Wed 09:00",
    length: "15 h",
    note: "Kid's school play. Nothing open on edge; INC-4790 closed Friday.",
    fit: "You're free then. Your next shift starts Wed 22 Oct 18:00, 9 h after this ends.",
  },

  schedule: [
    { day: "Today · Sun 18 Oct", rows: [
      { name: "You", initials: "JT", you: true, sub: "Fri 09:00 → Mon 09:00", right: "now" } ] },
    { day: "Mon 20 Oct", rows: [
      { name: "Daniel Whitfield", initials: "DW", sub: "09:00 → Tue 09:00" } ] },
    { day: "Tue 21 Oct", rows: [
      { name: "Marta Sousa", initials: "MS", sub: "09:00 → Wed 09:00" } ] },
    { day: "Wed 22 Oct", rows: [
      { name: "Callum Reid", initials: "CR", sub: "09:00 → Thu 09:00 · covering for Sofia Marques" } ] },
    { day: "Thu 23 Oct", rows: [
      { name: "James Doyle", initials: "JD", sub: "09:00 → Fri 09:00" } ] },
    { day: "Fri 24 Oct", rows: [
      { name: "Priya Nair", initials: "PN", sub: "09:00 → Sat 09:00" } ],
      gap: "Sat 25 Oct 09:00 → Sun 09:00. Nobody is scheduled, so pages go straight to the secondary." },
  ],
};
