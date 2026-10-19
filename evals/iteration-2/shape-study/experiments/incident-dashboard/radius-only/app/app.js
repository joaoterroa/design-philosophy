/* Northwind Incident Board: rendering and the simulated feed.
   No colours or sizes here: the script sets classes and unitless positions (--x, --v) only. */
(function () {
  "use strict";

  const q = new URLSearchParams(location.search);
  const html = document.documentElement;
  const isWall = html.dataset.display === "wall";
  const frozen = q.has("frozen");
  const $ = (id) => document.getElementById(id);
  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  /* ---------- Simulated clock: starts at the fixture snapshot, then runs in real time ---------- */
  const t0 = Date.now();
  const snapshot = new Date(window.NW_SNAPSHOT).getTime();
  const now = () => snapshot + (frozen ? 0 : Date.now() - t0);

  const MIN = 60000, HOUR = 60 * MIN, DAY = 24 * HOUR;
  const WINDOW = DAY; // the timeline shows the last 24 hours

  const pad = (n) => String(n).padStart(2, "0");
  const hhmm = (ms) => { const d = new Date(ms); return pad(d.getHours()) + ":" + pad(d.getMinutes()); };
  const hhmmss = (ms) => { const d = new Date(ms); return hhmm(ms) + ":" + pad(d.getSeconds()); };
  const dayStart = (ms) => { const d = new Date(ms); d.setHours(0, 0, 0, 0); return d.getTime(); };
  const whenLabel = (ms) => {
    const diff = Math.round((dayStart(now()) - dayStart(ms)) / DAY);
    if (diff === 0) return hhmm(ms);
    // Weekday, not "yesterday": short enough for the duration column, and the clock shows today's weekday.
    if (diff < 7) return new Date(ms).toLocaleDateString("en-GB", { weekday: "short" }) + " " + hhmm(ms);
    return new Date(ms).toLocaleDateString("en-GB", { day: "numeric", month: "short" }) + " " + hhmm(ms);
  };
  // Compact durations: "45m", "1h 18m", "12h 50m", "2d 4h". Read aloud in full by screen readers via aria-label.
  const dur = (ms) => {
    const m = Math.max(0, Math.floor(ms / MIN));
    if (m < 60) return m + "m";
    const h = Math.floor(m / 60);
    if (h < 24) return h + "h " + pad(m % 60) + "m";
    return Math.floor(h / 24) + "d " + (h % 24) + "h";
  };
  const durLong = (ms) => {
    const m = Math.max(0, Math.floor(ms / MIN));
    const d = Math.floor(m / 1440), h = Math.floor((m % 1440) / 60), mm = m % 60;
    return [d && d + (d === 1 ? " day" : " days"), h && h + (h === 1 ? " hour" : " hours"), (!d && mm) && mm + " minutes"].filter(Boolean).join(" ") || "under a minute";
  };
  const ago = (ms) => {
    const s = Math.max(0, Math.round((now() - ms) / 1000));
    if (s < 60) return s + " s ago";
    return Math.floor(s / 60) + " min ago";
  };

  /* ---------- State ---------- */
  let stateName = q.get("state") in window.NW_STATES ? q.get("state") : "live";
  let data = null;
  let lastUpdate = 0;
  const live = []; // rows whose duration and bar tick with the clock

  function load(name) {
    stateName = name;
    data = window.NW_STATES[name]();
    lastUpdate = data.updated ? new Date(data.updated).getTime() : 0;
    render();
  }

  /* ---------- Header ---------- */
  function renderHeader() {
    const t = now();
    $("clock").textContent = hhmm(t);
    $("clock").dateTime = new Date(t).toISOString();
    $("date").textContent = new Date(t).toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" });
    const f = $("freshness");
    const top = $("top");
    top.classList.toggle("is-stale", data.status === "stale");
    f.replaceChildren();
    if (data.status === "loading") {
      f.textContent = "Connecting to the incident feed…";
    } else if (data.status === "stale") {
      const mins = Math.max(1, Math.floor((t - lastUpdate) / MIN));
      f.append("No new data since ", el("strong", null, hhmm(lastUpdate)), " (" + mins + " min). Figures may be out of date; retrying every 60 s.");
    } else {
      f.textContent = "Updated " + hhmmss(lastUpdate) + " · " + ago(lastUpdate);
    }
  }

  /* ---------- Open incidents ---------- */
  // Most severe first; within a severity, newest first, so a fresh incident lands at the top of its band.
  const bySeverityThenAge = (a, b) => a.sev - b.sev || new Date(b.opened) - new Date(a.opened);

  function axisTicks() {
    const axis = $("axis");
    axis.replaceChildren();
    const end = now(), start = end - WINDOW;
    // Two landmarks only: the window's start and midnight, which splits yesterday from today.
    const first = el("span", "is-start", "24 h ago");
    first.style.setProperty("--x", "0");
    axis.append(first);
    const mid = dayStart(end);
    if (mid - start > 4 * HOUR && end - mid > 4 * HOUR) {
      const s = el("span", null, "00:00");
      s.style.setProperty("--x", ((mid - start) / WINDOW).toFixed(4));
      axis.append(s);
    }
    const n = el("span", "is-now", "now");
    n.style.setProperty("--x", "1");
    axis.append(n);
  }

  function laneTicks(lane) {
    const end = now(), start = end - WINDOW;
    const mid = dayStart(end);
    if (mid - start > 4 * HOUR && end - mid > 4 * HOUR) {
      const i = el("i");
      i.style.setProperty("--x", ((mid - start) / WINDOW).toFixed(4));
      lane.append(i);
    }
  }

  function placeBar(bar, opened, closed) {
    const end = now(), start = end - WINDOW;
    const x0 = Math.max(0, (opened - start) / WINDOW);
    const x1 = Math.min(1, ((closed || end) - start) / WINDOW);
    bar.style.setProperty("--x0", x0.toFixed(4));
    bar.style.setProperty("--x1", Math.max(x0, x1).toFixed(4));
    bar.classList.toggle("is-clipped", opened < start);
  }

  function incidentRow(inc, resolved) {
    const opened = new Date(inc.opened).getTime();
    const closed = resolved ? new Date(inc.resolved).getTime() : null;
    const li = el("li", "inc sev-" + inc.sev + (resolved ? "" : " is-open"));
    const a = el("a", "row");
    a.href = "#" + inc.id; // placeholder: link to the incident in the incident tool
    a.dataset.key = inc.id;

    a.append(el("span", "sev", "SEV" + inc.sev));

    const main = el("span", "main");
    const title = el("span", "title", inc.title);
    title.title = inc.title; // full title on hover when clamped to two lines
    const meta = el("span", "meta");
    meta.append(el("span", "id", inc.id), " · " + inc.service + " · " + inc.status + " · ");
    if (inc.lead) meta.append("IC " + inc.lead);
    else meta.append(el("span", "no-ic", "No incident commander"));
    main.append(title, meta);

    const lane = el("span", "lane");
    laneTicks(lane);
    const bar = el("span", "bar");
    placeBar(bar, opened, closed);
    lane.append(bar);

    const d = el("span", "dur");
    const dv = el("span", "dur-value");
    const ds = el("span", "dur-since");
    d.append(dv, ds);

    const update = () => {
      const span = (closed || now()) - opened;
      dv.textContent = dur(span);
      ds.textContent = resolved ? "closed " + whenLabel(closed) : "since " + whenLabel(opened);
      placeBar(bar, opened, closed);
      a.setAttribute("aria-label",
        "SEV" + inc.sev + ", " + inc.id + ": " + inc.title + ". " + inc.service + ", " + inc.status + ". " +
        (inc.lead ? "Incident commander " + inc.lead + ". " : "No incident commander. ") +
        (resolved ? "Lasted " + durLong(span) + "." : "Open for " + durLong(span) + ", since " + whenLabel(opened) + "."));
    };
    update();
    live.push(update);

    a.append(main, lane, d);
    li.append(a);
    return li;
  }

  function placeholderRows(list, n) {
    for (let i = 0; i < n; i++) {
      const li = el("li");
      const r = el("div", "row");
      const m = el("span", "main");
      m.append(el("span", "ph ph-title"), el("span", "ph ph-meta"));
      r.append(el("span", "ph ph-tag"), m, el("span", "lane"), el("span", "ph ph-dur"));
      li.append(r);
      list.append(li);
    }
  }

  function renderOpen() {
    const list = $("open-list"), rlist = $("resolved-list");
    list.replaceChildren(); rlist.replaceChildren();
    live.length = 0;
    axisTicks();
    $("more").hidden = true;
    $("calm").hidden = true;
    const section = $("open-section");
    section.classList.toggle("is-loading", data.status === "loading");
    section.setAttribute("aria-busy", data.status === "loading" ? "true" : "false");

    if (data.status === "loading") {
      $("open").textContent = "–";
      $("open-label").textContent = "open incidents";
      $("sev-summary").textContent = "";
      placeholderRows(list, 4);
      placeholderRows(rlist, 2);
      $("axis").hidden = $("lh-dur").hidden = false;
      return;
    }

    const open = data.open.slice().sort(bySeverityThenAge);
    $("open").textContent = String(open.length);
    $("open-label").textContent = open.length === 1 ? "open incident" : "open incidents";
    const counts = [1, 2, 3].map((s) => open.filter((i) => i.sev === s).length);
    const sum = $("sev-summary");
    sum.replaceChildren();
    counts.forEach((c, i) => {
      if (!c) return;
      if (sum.childNodes.length) sum.append(" · ");
      sum.append(el("b", null, String(c)), " SEV" + (i + 1));
    });

    $("axis").hidden = $("lh-dur").hidden = open.length === 0;
    open.forEach((inc) => list.append(incidentRow(inc, false)));

    const resolved = data.resolved
      .filter((r) => now() - new Date(r.resolved).getTime() <= WINDOW)
      .sort((a, b) => new Date(b.resolved) - new Date(a.resolved));
    resolved.forEach((inc) => rlist.append(incidentRow(inc, true)));
    $("resolved-h").hidden = resolved.length === 0;

    if (open.length === 0) {
      const calm = $("calm");
      calm.replaceChildren();
      const last = resolved[0];
      if (last) {
        const t = new Date(last.resolved).getTime();
        calm.append("Nothing open. The last incident closed at " + hhmm(t) + ", " + durLong(now() - t) + " ago: ",
          el("span", "id", last.id), " " + last.title + ".");
      } else {
        calm.textContent = "Nothing open, and nothing closed in the last 24 hours.";
      }
      calm.hidden = false;
    }
    if (isWall) requestAnimationFrame(fitWall);
  }

  /* Wall display never scrolls. If rows don't fit, history goes first, then the least severe open rows,
     and a sentence says what is not shown. */
  function fitWall() {
    const section = $("open-section");
    const overflowing = () => section.scrollHeight > section.clientHeight + 1;
    const rrows = [...$("resolved-list").children];
    while (overflowing() && rrows.length) rrows.pop().hidden = true;
    if (overflowing() || !$("resolved-list").querySelector("li:not([hidden])")) $("resolved-h").hidden = true;
    const orows = [...$("open-list").children];
    const hiddenIds = [];
    const more = $("more");
    while (overflowing() && orows.length > 1) {
      const li = orows.pop();
      li.hidden = true;
      hiddenIds.unshift(li.querySelector("a").dataset.key + " (" + li.querySelector(".sev").textContent + ")");
      more.textContent = hiddenIds.length + " more not shown: " + hiddenIds.join(", ") + ".";
      more.hidden = false;
    }
  }

  /* ---------- On call ---------- */
  function renderOnCall() {
    const body = $("oncall-body");
    const band = $("oncall");
    body.replaceChildren();
    band.classList.toggle("is-failed", !!(data.onCall && data.onCall.error));
    if (data.status === "loading") { body.append(el("span", "oc-role", "Loading the rota…")); return; }
    if (data.onCall.error) {
      body.append(el("span", "failed-title", "The rota didn't load."),
        el("span", "failed-body", data.onCall.error + " It is missing, not empty: check the paging tool for who is on call. Retrying every 60 s."));
      return;
    }
    const rows = data.onCall.rows;
    const shifts = rows.filter((r) => r.until);
    const sameEnd = shifts.length > 1 && shifts.every((r) => r.until === shifts[0].until);
    rows.forEach((r) => {
      const item = el("span", "oc-item");
      item.append(el("span", "oc-role", r.role));
      if (r.name) {
        const name = el("span", "oc-name", r.name);
        item.append(name, el("span", "oc-team", r.team + (!sameEnd && r.until ? ", until " + r.until : "")));
      } else {
        item.append(el("span", "oc-unassigned", "Unassigned"));
      }
      body.append(item);
    });
    const nexts = shifts.filter((r) => r.next).map((r) => r.next);
    if (sameEnd && nexts.length) body.append(el("span", "oc-item oc-next", "Handover " + shifts[0].until + " to " + nexts.join(" and ")));
  }

  /* ---------- Stats ---------- */
  const SVGNS = "http://www.w3.org/2000/svg";
  const svg = (tag, attrs) => { const n = document.createElementNS(SVGNS, tag); for (const k in attrs) n.setAttribute(k, attrs[k]); return n; };

  function statBlock(id, label, value, unit, delta, chart, wide, note) {
    const box = $(id);
    box.replaceChildren();
    const left = el("div");
    const v = el("p", "stat-value", value);
    if (unit) v.append(el("span", "stat-unit", unit));
    left.append(el("p", "stat-label", label), v, el("p", "stat-delta", delta));
    box.append(left);
    if (chart) box.append(chart);
    if (wide) { wide.classList.add("stat-wide"); box.append(wide); }
    if (note) box.append(el("p", "stat-note", note));
  }

  function pagesChart(values) {
    // 14 columns, today emphasised: the story is "today against the last two weeks".
    const W = 136, H = 40, n = values.length, gap = 2, bw = (W - gap * (n - 1)) / n;
    const max = Math.max(...values);
    const s = svg("svg", { class: "stat-chart", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Pages per day, last 14 days, today last: " + values.join(", ") });
    s.setAttribute("preserveAspectRatio", "none");
    values.forEach((v, i) => {
      const h = Math.max(2, (v / max) * H);
      const x = i * (bw + gap);
      const day = new Date(dayStart(now()) - (n - 1 - i) * DAY);
      const lbl = (i === n - 1 ? "Today so far" : day.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short" })) + ": " + v + " pages";
      const hit = svg("rect", { class: "col-hit", x: x - gap / 2, y: 0, width: bw + gap, height: H, "data-tip": lbl });
      if (!isWall) { hit.setAttribute("tabindex", "0"); hit.setAttribute("aria-label", lbl); }
      s.append(hit, svg("rect", { class: "col" + (i === n - 1 ? " is-now" : ""), x, y: H - h, width: bw, height: h, rx: 1 }));
    });
    return s;
  }

  function mttrChart(values) {
    const W = 136, H = 40, n = values.length, pad = 5;
    const max = Math.max(...values), min = Math.min(...values);
    const pts = values.map((v, i) => [pad + (i * (W - 2 * pad)) / (n - 1), pad + (1 - (v - min) / (max - min || 1)) * (H - 2 * pad)]);
    const s = svg("svg", { class: "stat-chart", viewBox: `0 0 ${W} ${H}`, role: "img", "aria-label": "Weekly MTTR in minutes, last 8 weeks, latest last: " + values.join(", ") });
    s.append(svg("polyline", { class: "spark", points: pts.map((p) => p.join(",")).join(" ") }));
    const [ex, ey] = pts[n - 1];
    s.append(svg("circle", { class: "spark-end", cx: ex, cy: ey, r: 4 }));
    pts.forEach(([x], i) => {
      const lbl = (i === n - 1 ? "This week" : (n - 1 - i) + (n - 1 - i === 1 ? " week ago" : " weeks ago")) + ": " + values[i] + " min";
      const hit = svg("rect", { class: "col-hit", x: x - 8, y: 0, width: 16, height: H, "data-tip": lbl });
      if (!isWall) { hit.setAttribute("tabindex", "0"); hit.setAttribute("aria-label", lbl); }
      s.append(hit);
    });
    return s;
  }

  function renderStats() {
    if (data.status === "loading") {
      ["stat-pages", "stat-mttr", "stat-budget"].forEach((id) => { const b = $(id); b.replaceChildren(el("span", "ph ph-meta"), el("span", "ph ph-title")); });
      $("services").replaceChildren(...[0, 1, 2, 3, 4].map(() => { const li = el("li", "hbar"); li.append(el("span", "ph ph-meta"), el("span", "ph ph-title")); return li; }));
      return;
    }
    const s = data.stats;
    const diff = s.pagesToday - s.pagesYesterday;
    statBlock("stat-pages", "Pages today so far", String(s.pagesToday), "",
      diff === 0 ? "Same as all of yesterday" : Math.abs(diff) + (diff > 0 ? " more" : " fewer") + " than all of yesterday",
      pagesChart(s.pagesByDay));

    statBlock("stat-mttr", "MTTR, last 7 days", String(s.mttrMinutes), "min",
      Math.abs(s.mttrChangePct) + "% " + (s.mttrChangePct < 0 ? "faster" : "slower") + " than last week",
      mttrChart(s.mttrWeekly));

    const meter = el("div", "meter" + (s.budgetLeftPct < 25 ? " is-low" : ""));
    meter.setAttribute("role", "meter");
    meter.setAttribute("aria-valuemin", "0");
    meter.setAttribute("aria-valuemax", "100");
    meter.setAttribute("aria-valuenow", String(s.budgetLeftPct));
    meter.setAttribute("aria-label", "Error budget left");
    const fill = el("span", "meter-fill");
    fill.style.setProperty("--v", (s.budgetLeftPct / 100).toFixed(3));
    meter.append(fill);
    statBlock("stat-budget", "Error budget left", String(s.budgetLeftPct), "%",
      Math.abs(s.budgetChangePts) + (Math.abs(s.budgetChangePts) === 1 ? " pt " : " pts ") + (s.budgetChangePts <= 0 ? "used" : "regained") + " since yesterday", null, meter, s.budgetSlo);

    const max = Math.max(...s.byService.map((x) => x.count));
    $("services").replaceChildren(...s.byService.map((x) => {
      const li = el("li", "hbar");
      const name = el("span", "hbar-name", x.service);
      name.title = x.service;
      const track = el("span", "hbar-track");
      const fillb = el("span", "hbar-fill");
      fillb.style.setProperty("--v", (x.count / max).toFixed(3));
      track.append(fillb, el("span", "hbar-value", String(x.count)));
      li.append(name, track);
      li.setAttribute("aria-label", x.service + ": " + x.count + " incidents");
      return li;
    }));
  }

  /* ---------- Render, keeping focus across re-renders ---------- */
  function render() {
    const focused = document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.key : null;
    renderHeader();
    renderOpen();
    renderOnCall();
    renderStats();
    if (focused) { const again = document.querySelector('[data-key="' + focused + '"]'); if (again) again.focus(); }
  }

  /* ---------- Ticking: clock and durations every 15 s; simulated refresh every 60 s ---------- */
  let lastRefresh = Date.now();
  setInterval(() => {
    if (frozen) return;
    if (data.status !== "loading" && data.status !== "stale" && Date.now() - lastRefresh >= 60000) {
      lastRefresh = Date.now();
      lastUpdate = now(); // production: fetch /api/metrics, then render() if anything changed
    }
    renderHeader();
    live.forEach((fn) => fn());
  }, 1000);

  /* ---------- Tooltip (desk): enhances, never gates; every value is also in aria-labels ---------- */
  const tip = $("tip");
  function showTip(target, x, y) {
    const text = target.getAttribute("data-tip");
    if (!text) return;
    const [k, v] = text.split(": ");
    tip.replaceChildren(el("strong", null, v), document.createTextNode(" " + k));
    tip.hidden = false;
    const r = tip.getBoundingClientRect();
    tip.style.left = Math.min(window.innerWidth - r.width - 8, Math.max(8, x - r.width / 2)) + "px";
    tip.style.top = Math.max(8, y - r.height - 10) + "px";
  }
  if (!isWall) {
    document.addEventListener("pointermove", (e) => {
      const t = e.target.closest && e.target.closest("[data-tip]");
      if (t) showTip(t, e.clientX, e.clientY); else tip.hidden = true;
    });
    document.addEventListener("focusin", (e) => {
      const t = e.target.closest && e.target.closest("[data-tip]");
      if (t) { const r = t.getBoundingClientRect(); showTip(t, r.left + r.width / 2, r.top); } else tip.hidden = true;
    });
    document.addEventListener("focusout", () => { tip.hidden = true; });
  }

  /* ---------- Prototype controls ---------- */
  const stateSel = $("state-select");
  stateSel.value = stateName;
  stateSel.addEventListener("change", () => {
    load(stateSel.value);
    const u = new URL(location.href); u.searchParams.set("state", stateSel.value); history.replaceState(null, "", u);
  });
  const themeSel = $("theme-select");
  themeSel.value = html.dataset.theme || "system";
  themeSel.addEventListener("change", () => {
    if (themeSel.value === "system") delete html.dataset.theme; else html.dataset.theme = themeSel.value;
    try { localStorage.setItem("nw-theme", themeSel.value === "system" ? "" : themeSel.value); } catch (e) {}
  });
  $("wall-link").href = "?display=wall&state=" + stateName;
  stateSel.addEventListener("change", () => { $("wall-link").href = "?display=wall&state=" + stateSel.value; });

  load(stateName);
  window.NW_load = load; // used by the screenshot script
})();
