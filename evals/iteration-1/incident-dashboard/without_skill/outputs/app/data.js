/* Sample data. In production this is the /api/metrics payload (refreshed every
   60 s). Times are minutes relative to the snapshot ("now" = Tue 13 Oct 2026
   11:00 Europe/London), which keeps the original dashboard's numbers consistent:
   INC-2291 opened 09:42 and has run 1h 18m, etc.
   Incidents marked "added" did not exist in the original; they were invented so
   the open list matches the original headline of 7 open incidents. */

const SNAPSHOT = new Date("2026-10-13T11:00:00+01:00");
const min = (m) => new Date(SNAPSHOT.getTime() + m * 60000);

const ALL_INCIDENTS = [
  { id: "INC-2291", title: "Route optimiser timeouts for EU-West depots", service: "Routing API", sev: 1, status: "Investigating", opened: min(-78), owner: "Tomás R." },
  { id: "INC-2290", title: "Delayed tracking events from scanner fleet B", service: "Tracking Ingest", sev: 2, status: "Mitigated", opened: min(-175), owner: "Priya N." },
  { id: "INC-2289", title: "Invoice PDF generation failing for 3% of accounts", service: "Billing", sev: 2, status: "Monitoring", opened: min(-770), owner: "Billing team" },
  { id: "INC-2293", title: "Geocoding cache hit rate below 80%", service: "Routing API", sev: 3, status: "Investigating", opened: min(-12), owner: "Tomás R.", added: true },
  { id: "INC-2292", title: "Carrier rate-card import retrying", service: "Billing", sev: 3, status: "Investigating", opened: min(-29), owner: "Unassigned", added: true },
  { id: "INC-2286", title: "Label printers misaligned at Leeds depot", service: "Warehouse Sync", sev: 3, status: "Monitoring", opened: min(-1360), owner: "Warehouse IT", added: true },
  { id: "INC-2284", title: "ETA emails delayed up to 10 minutes", service: "Tracking Ingest", sev: 3, status: "Monitoring", opened: min(-2560), owner: "Priya N.", added: true },
];

const RESOLVED = [
  { id: "INC-2288", title: "Driver app login slow on Android 14", service: "Driver App Backend", sev: 3, opened: min(-1170), resolved: min(-1045) },
  { id: "INC-2287", title: "Warehouse sync duplicate SKUs", service: "Warehouse Sync", sev: 3, opened: min(-1438), resolved: min(-1393) },
  { id: "INC-2285", title: "Webhook retries saturating billing queue", service: "Billing", sev: 2, opened: min(-2010), resolved: min(-1932), added: true },
];

const BASE = {
  oncall: [
    { role: "Primary", name: "Priya N.", team: "Platform", until: "18:00" },
    { role: "Secondary", name: "Tomás R.", team: "Routing", until: "18:00" },
  ],
  kpis: {
    openYesterday: 5,
    mttr: { value: 48, prior: 55, weeks: [71, 64, 58, 66, 52, 60, 55, 48] },
    pages: { today: 23, yesterday: 18, avg7: 16 },
    budget: { left: 61, weekAgo: 65, window: "28 days" },
  },
  byService: [
    { service: "Routing API", n: 14 },
    { service: "Tracking Ingest", n: 9 },
    { service: "Billing", n: 6 },
    { service: "Driver App Backend", n: 4 },
    { service: "Warehouse Sync", n: 2 },
  ],
  daysSinceSev1: 0,
};

/* Each demo state is the payload the feed would send in that situation. */
function buildState(name) {
  const s = structuredClone(BASE);
  s.name = name;
  s.lastUpdate = SNAPSHOT;
  s.feed = "ok";
  s.incidents = ALL_INCIDENTS.map((i) => ({ ...i }));
  s.resolved = RESOLVED.map((i) => ({ ...i }));
  s.ic = null; // incident commander

  if (name === "elevated") {
    // SEV1 was resolved 20 min ago; two SEV2s remain.
    const sev1 = s.incidents.shift();
    s.resolved.unshift({ ...sev1, resolved: min(-20) });
    s.kpis.openYesterday = 5;
  }
  if (name === "clear") {
    s.resolved = [
      { id: "INC-2290", title: "Delayed tracking events from scanner fleet B", service: "Tracking Ingest", sev: 2, opened: min(-175), resolved: min(-72) },
      { id: "INC-2289", title: "Invoice PDF generation failing for 3% of accounts", service: "Billing", sev: 2, opened: min(-770), resolved: min(-120) },
      { id: "INC-2293", title: "Geocoding cache hit rate below 80%", service: "Routing API", sev: 3, opened: min(-260), resolved: min(-210) },
      ...s.resolved,
    ].slice(0, 5);
    s.incidents = [];
    s.daysSinceSev1 = 9;
    s.kpis.pages = { today: 4, yesterday: 18, avg7: 16 };
    s.kpis.budget = { left: 74, weekAgo: 71, window: "28 days" };
    s.kpis.mttr = { value: 41, prior: 55, weeks: [71, 64, 58, 66, 52, 60, 55, 41] };
  }
  if (name === "stale") {
    s.feed = "stale";
    s.lastUpdate = min(-7);
  }
  if (name === "error") {
    s.feed = "down";
    s.lastUpdate = null;
  }
  if (name === "loading") {
    s.feed = "loading";
    s.lastUpdate = null;
  }
  if (name === "major-ic") {
    // Same as major, but someone has taken command.
    s.ic = { name: "Ana L.", team: "SRE", since: min(-6) };
  }
  return s;
}

window.NW_DATA = { SNAPSHOT, buildState };
