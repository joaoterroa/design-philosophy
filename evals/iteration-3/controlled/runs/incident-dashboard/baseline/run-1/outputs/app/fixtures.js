/* Fixed offline fixture for the assigned product. */
window.EVAL_FIXTURES = {
  "now": "2026-10-18T10:00:00Z",
  "dashboard": {
    "product": "Northwind Incidents",
    "openCount": 7,
    "surgeCount": 12,
    "incidents": [
      {
        "id": "INC-2291",
        "title": "Route optimiser timeouts for EU-West depots",
        "service": "Routing API",
        "severity": 1,
        "status": "Investigating",
        "opened": "09:42",
        "duration": "1h 18m",
        "commander": null
      },
      {
        "id": "INC-2290",
        "title": "Delayed tracking events from scanner fleet B",
        "service": "Tracking Ingest",
        "severity": 2,
        "status": "Mitigated",
        "opened": "08:05",
        "duration": "2h 55m",
        "commander": "Priya N."
      },
      {
        "id": "INC-2289",
        "title": "Invoice PDF generation failing for 3% of accounts",
        "service": "Billing",
        "severity": 2,
        "status": "Monitoring",
        "opened": "Yesterday 22:10",
        "duration": "12h 50m",
        "commander": "Sam Okafor"
      },
      {
        "id": "INC-2286",
        "title": "Proof-of-delivery photos delayed",
        "service": "Driver App Backend",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2285",
        "title": "ETA recalculation lagging on EU routes",
        "service": "Routing API",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2284",
        "title": "Stock counts stale for Rotterdam depot",
        "service": "Warehouse Sync",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2283",
        "title": "Fuel surcharge rounding discrepancy",
        "service": "Billing",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2282",
        "title": "Pickup requests delayed for partner fleet",
        "service": "Routing API",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2281",
        "title": "Scanner retry queue above normal",
        "service": "Tracking Ingest",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2280",
        "title": "Export manifest refresh delayed",
        "service": "Warehouse Sync",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2279",
        "title": "Driver session refresh retries",
        "service": "Driver App Backend",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      },
      {
        "id": "INC-2278",
        "title": "Invoice export queue growing",
        "service": "Billing",
        "severity": 3,
        "status": "Monitoring",
        "opened": "08:30",
        "duration": "2h 30m",
        "commander": "Aiko Kimura"
      }
    ],
    "resolved": [
      {
        "id": "INC-2288",
        "title": "Driver app login slow on Android 14",
        "service": "Driver App Backend",
        "severity": 3,
        "status": "Resolved",
        "opened": "Yesterday 15:30",
        "duration": "2h 05m"
      },
      {
        "id": "INC-2287",
        "title": "Warehouse sync duplicate SKUs",
        "service": "Warehouse Sync",
        "severity": 3,
        "status": "Resolved",
        "opened": "Yesterday 11:02",
        "duration": "45m"
      }
    ],
    "services": [
      {
        "name": "Routing API",
        "value": 14
      },
      {
        "name": "Tracking Ingest",
        "value": 9
      },
      {
        "name": "Billing",
        "value": 6
      },
      {
        "name": "Driver App Backend",
        "value": 4
      },
      {
        "name": "Warehouse Sync",
        "value": 2
      }
    ],
    "primary": "Priya N. (Platform)",
    "secondary": "Tomás R. (Routing)",
    "until": "18:00",
    "pages": 23,
    "pagesDelta": 5,
    "mttr": "48m",
    "mttrChange": "12% lower",
    "slo": "61%",
    "sloChange": "4 points lower",
    "staleAsOf": "09:42",
    "displayTime": "11:00",
    "displayDate": "18 October 2026"
  }
};
