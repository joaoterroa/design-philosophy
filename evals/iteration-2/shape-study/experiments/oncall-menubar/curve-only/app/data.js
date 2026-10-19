// Sample data. Invented; stands in for the PagerDuty schedules API + Google Calendar OOO.
// Times are hours from Sat 18 Oct 2026 00:00 Europe/London (BST). "Now" is 13:48.
window.ROTA_DATA = {
  now: 13.8,
  me: "je",
  tzName: "BST",
  people: {
    je: { name: "Jordan Ellis", initials: "JE", handle: "jordan.ellis", city: "London", tz: 0 },
    so: { name: "Sam Okafor", initials: "SO", handle: "sam.okafor", city: "London", tz: 0 },
    to: { name: "Tomás Ortega", initials: "TO", handle: "tomas", city: "Madrid", tz: 1 },
    ak: { name: "Aiko Kimura", initials: "AK", handle: "aiko.k", city: "London", tz: 0 },
    pr: { name: "Priya Raman", initials: "PR", handle: "priya", city: "London", tz: 0 },
    mf: { name: "Marcus Feld", initials: "MF", handle: "mfeld", city: "Berlin", tz: 1 },
    ln: { name: "Lena Novak", initials: "LN", handle: "lena.novak", city: "Amsterdam", tz: 1 },
    dp: { name: "Dev Patel", initials: "DP", handle: "devp", city: "New York", tz: -5 },
    as: { name: "Ana Souza", initials: "AS", handle: "ana.souza", city: "Lisbon", tz: 0 },
    ob: { name: "Owen Byrne", initials: "OB", handle: "owen", city: "Dublin", tz: 0 },
    cm: { name: "Chloe Martin", initials: "CM", handle: "chloe.m", city: "San Francisco", tz: -8 },
    ka: { name: "Kwame Asante", initials: "KA", handle: "kwame", city: "London", tz: 0 },
    ht: { name: "Hiro Tanaka", initials: "HT", handle: "hiro", city: "London", tz: 0 },
    rl: { name: "Rosa Lindqvist", initials: "RL", handle: "rosa.l", city: "Stockholm", tz: 1 },
  },
  // Who is on call right now, per rotation layer (the 40 SREs are split across these).
  onCallNow: [
    { rotation: "Platform", layer: "Primary", who: "je", until: 57 },
    { rotation: "Platform", layer: "Secondary", who: "so", until: 57 },
    { rotation: "Data", layer: "Primary", who: "to", until: 81 },
    { rotation: "Edge", layer: "Primary", who: "ak", until: 105 },
  ],
  myShift: { rotation: "Platform", layer: "Primary", from: -45, to: 57, next: "ob" },
  myNextShift: { rotation: "Platform", layer: "Primary", from: 129, to: 297 }, // Thu 23 Oct 09:00 -> Thu 30 Oct 09:00
  // Platform rotation members eligible to take a Platform Primary handover.
  platformMembers: ["pr", "mf", "ln", "as", "ka", "rl", "dp", "cm", "ob", "ht", "so"],
  // Availability for any range inside this weekend. Derived from schedules + calendar.
  availability: {
    so: { kind: "blocked", text: "Already Platform Secondary then. One person can’t hold both layers." },
    ht: { kind: "caution", text: "Out of office until Wed 22 Oct, per Google Calendar" },
    ob: { kind: "free", text: "Free · takes over from you Mon 09:00 anyway" },
    pr: { kind: "free", text: "Free · last on call 3 weeks ago" },
    mf: { kind: "free", text: "Free · last on call 9 days ago" },
    ln: { kind: "free", text: "Free · last on call 2 weeks ago" },
    as: { kind: "free", text: "Free · last on call 5 weeks ago" },
    ka: { kind: "free", text: "Free · last on call 4 weeks ago" },
    rl: { kind: "free", text: "Free · last on call 6 days ago" },
    dp: { kind: "free", text: "Free · last on call 2 weeks ago" },
    cm: { kind: "free", text: "Free · last on call 3 weeks ago" },
  },
  openIncidents: [{ id: "INC-4821", title: "Checkout p99 latency", sev: "SEV3", status: "mitigated" }],
  incoming: {
    from: "to", rotation: "Data", layer: "Primary", start: 90, end: 105,
    note: "Flying to Lisbon Tuesday evening, back online Wednesday morning.",
    fit: "You’re free then. It doesn’t overlap your Platform shift.",
  },
  gap: { rotation: "Edge", layer: "Primary", start: 26, end: 30, reason: "Aiko’s override for those hours was declined and nobody replaced it." },
};
