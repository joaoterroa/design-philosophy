/* Demo fixtures standing in for /api/metrics (refreshed every 60 s in production).
   Base data is the original dashboard's; additions are marked "added" and listed in DESIGN.md.
   Snapshot time: the original durations all resolve to 11:00 on the day. */
(function () {
  const SNAPSHOT = "2026-10-18T11:00:00";

  const openBase = [
    { id: "INC-2291", title: "Route optimiser timeouts for EU-West depots", service: "Routing API", sev: 1, status: "Investigating", opened: "2026-10-18T09:42:00", lead: null },
    { id: "INC-2290", title: "Delayed tracking events from scanner fleet B", service: "Tracking Ingest", sev: 2, status: "Mitigated", opened: "2026-10-18T08:05:00", lead: "Wen L." },
    { id: "INC-2289", title: "Invoice PDF generation failing for 3% of accounts", service: "Billing", sev: 2, status: "Monitoring", opened: "2026-10-17T22:10:00", lead: "Marta S." },
    // added: the original headline said 7 open while its table listed only 3 unresolved
    { id: "INC-2294", title: "Proof-of-delivery photos upload slowly on 3G connections", service: "Driver App Backend", sev: 3, status: "Investigating", opened: "2026-10-18T10:48:00", lead: "Dev P." },
    { id: "INC-2293", title: "ETA recalculation lagging 4–6 minutes for UK parcels", service: "Tracking Ingest", sev: 3, status: "Identified", opened: "2026-10-18T10:21:00", lead: "Wen L." },
    { id: "INC-2286", title: "Stock counts stale for the Rotterdam distribution centre after the nightly sync job, affecting replenishment orders", service: "Warehouse Sync", sev: 3, status: "Monitoring", opened: "2026-10-17T06:40:00", lead: "Ines G." },
    { id: "INC-2285", title: "Fuel surcharge rounding differs by 1p on some invoices", service: "Billing", sev: 3, status: "Identified", opened: "2026-10-16T14:15:00", lead: "Marta S." },
  ];

  const resolvedBase = [
    { id: "INC-2288", title: "Driver app login slow on Android 14", service: "Driver App Backend", sev: 3, status: "Resolved", opened: "2026-10-17T15:30:00", resolved: "2026-10-17T17:35:00", lead: "Dev P." },
    { id: "INC-2287", title: "Warehouse sync duplicate SKUs", service: "Warehouse Sync", sev: 3, status: "Resolved", opened: "2026-10-17T11:02:00", resolved: "2026-10-17T11:47:00", lead: "Ines G." },
  ];

  const onCall = {
    rows: [
      { role: "Primary", name: "Priya N.", team: "Platform", until: "18:00", next: "Amara O." },        // next: added
      { role: "Secondary", name: "Tomás R.", team: "Routing", until: "18:00", next: "Jonas K." },       // next: added
      { role: "Incident commander", name: null, team: null, until: null, next: null },
    ],
  };

  const stats = {
    pagesToday: 23,
    pagesYesterday: 18,                                                                  // added: makes "▲ 5" explicit
    pagesByDay: [11, 9, 14, 8, 6, 5, 12, 10, 13, 17, 9, 7, 18, 23],                    // added: last 14 days, today last
    mttrMinutes: 48,
    mttrChangePct: -12,
    mttrWeekly: [71, 64, 80, 58, 66, 61, 55, 48],                                       // added: last 8 weeks
    budgetLeftPct: 61,
    budgetChangePts: -4,
    budgetSlo: "99.9% availability SLO, 30 days",                          // added (assumed SLO)
    byService: [
      { service: "Routing API", count: 14 },
      { service: "Tracking Ingest", count: 9 },
      { service: "Billing", count: 6 },
      { service: "Driver App Backend", count: 4 },
      { service: "Warehouse Sync", count: 2 },
    ],
  };

  const surgeExtra = [
    { id: "INC-2299", title: "Label printer queue backing up at Leeds hub", service: "Warehouse Sync", sev: 3, status: "Investigating", opened: "2026-10-18T10:55:00", lead: "Ines G." },
    { id: "INC-2298", title: "Geocoder returning low-confidence matches for new postcodes", service: "Routing API", sev: 2, status: "Identified", opened: "2026-10-18T10:30:00", lead: "Tomás R." },
    { id: "INC-2297", title: "Partner webhook retries exhausting rate limit", service: "Tracking Ingest", sev: 3, status: "Investigating", opened: "2026-10-18T10:12:00", lead: "Wen L." },
    { id: "INC-2296", title: "Credit note emails delayed by up to 20 minutes", service: "Billing", sev: 3, status: "Monitoring", opened: "2026-10-18T09:05:00", lead: "Marta S." },
    { id: "INC-2295", title: "Driver shift swap screen shows stale roster", service: "Driver App Backend", sev: 3, status: "Identified", opened: "2026-10-18T07:50:00", lead: "Dev P." },
  ];

  const allClearResolved = [
    { id: "INC-2291", title: "Route optimiser timeouts for EU-West depots", service: "Routing API", sev: 1, status: "Resolved", opened: "2026-10-18T05:42:00", resolved: "2026-10-18T07:48:00", lead: "Priya N." },
    { id: "INC-2290", title: "Delayed tracking events from scanner fleet B", service: "Tracking Ingest", sev: 2, status: "Resolved", opened: "2026-10-18T02:05:00", resolved: "2026-10-18T04:20:00", lead: "Wen L." },
    ...resolvedBase,
  ];

  const clone = (x) => JSON.parse(JSON.stringify(x));

  window.NW_STATES = {
    live: () => ({ status: "ok", updated: SNAPSHOT, open: clone(openBase), resolved: clone(resolvedBase), onCall: clone(onCall), stats: clone(stats) }),
    loading: () => ({ status: "loading" }),
    allclear: () => ({
      status: "ok", updated: SNAPSHOT, open: [], resolved: clone(allClearResolved),
      onCall: { rows: clone(onCall.rows).map((r) => (r.role === "Incident commander" ? { ...r, name: "Amara O.", team: "SRE", until: "18:00" } : r)) },
      stats: { ...clone(stats), pagesToday: 4, pagesByDay: [11, 9, 14, 8, 6, 5, 12, 10, 13, 17, 9, 7, 18, 4], budgetLeftPct: 64, budgetChangePts: -1 },
    }),
    stale: () => ({ status: "stale", updated: "2026-10-18T10:54:12", open: clone(openBase), resolved: clone(resolvedBase), onCall: clone(onCall), stats: clone(stats) }),
    partial: () => ({ status: "ok", updated: SNAPSHOT, open: clone(openBase), resolved: clone(resolvedBase), onCall: { error: "The paging service timed out at 10:59:58." }, stats: clone(stats) }),
    surge: () => ({ status: "ok", updated: SNAPSHOT, open: clone([...openBase, ...surgeExtra]), resolved: clone(resolvedBase), onCall: clone(onCall), stats: { ...clone(stats), pagesToday: 41, pagesByDay: [11, 9, 14, 8, 6, 5, 12, 10, 13, 17, 9, 7, 18, 41] } }),
  };
  window.NW_SNAPSHOT = SNAPSHOT;
})();
