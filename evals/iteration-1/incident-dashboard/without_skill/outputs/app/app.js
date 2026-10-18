/* Incident status dashboard: rendering + demo state switcher. No dependencies. */
(function () {
  const { SNAPSHOT, buildState } = window.NW_DATA;
  const $ = (id) => document.getElementById(id);
  const root = document.documentElement;
  const params = new URLSearchParams(location.search);

  const STATES = [
    ["major", "SEV1, no commander"],
    ["major-ic", "SEV1, commander set"],
    ["elevated", "SEV2 only"],
    ["clear", "All clear"],
    ["stale", "Stale data"],
    ["error", "Feed down"],
    ["loading", "Loading"],
  ];
  const DISPLAYS = [["tv", "TV"], ["laptop", "Laptop"]];
  const THEMES = [["dark", "Dark"], ["light", "Light"]];

  // ---- Settings: URL first, then sensible defaults -------------------------
  const autoDisplay = () => (window.innerWidth >= 1800 && window.innerHeight >= 900 ? "tv" : "laptop");
  const prefersDark = () => window.matchMedia && matchMedia("(prefers-color-scheme: dark)").matches;
  const settings = {
    state: params.get("state") || "major",
    display: params.get("display") || autoDisplay(),
    theme: params.get("theme") || null,
  };
  const themeFor = (display) => settings.theme || (display === "tv" ? "dark" : prefersDark() ? "dark" : "light");
  if (params.has("kiosk")) document.body.classList.add("kiosk");

  // ---- Simulated clock: starts at the snapshot and runs in real time --------
  const t0 = Date.now();
  const now = () => new Date(SNAPSHOT.getTime() + (Date.now() - t0));

  // ---- Formatting -----------------------------------------------------------
  const tz = "Europe/London";
  const hhmm = (d) => d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: tz });
  const hhmmss = (d) => d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit", second: "2-digit", timeZone: tz });
  const dayLabel = (d) => d.toLocaleDateString("en-GB", { weekday: "short", day: "numeric", month: "short", timeZone: tz });
  function dur(ms) {
    const m = Math.max(0, Math.floor(ms / 60000));
    if (m < 60) return `${m}m`;
    const h = Math.floor(m / 60);
    if (h < 24) return `${h}h ${String(m % 60).padStart(2, "0")}m`;
    return `${Math.floor(h / 24)}d ${h % 24}h`;
  }
  function openedLabel(d, ref) {
    const sameDay = dayLabel(d) === dayLabel(ref);
    const wd = d.toLocaleDateString("en-GB", { weekday: "short", timeZone: tz });
    return sameDay ? `since ${hhmm(d)}` : `since ${wd} ${hhmm(d)}`;
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;

  // Shapes are the second severity channel (with the text label) so colour is never alone.
  const SHAPES = {
    1: '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M5 0 10 5 5 10 0 5z" fill="currentColor"/></svg>',
    2: '<svg viewBox="0 0 10 10" aria-hidden="true"><path d="M5 .5 9.8 9.5H.2z" fill="currentColor"/></svg>',
    3: '<svg viewBox="0 0 10 10" aria-hidden="true"><circle cx="5" cy="5" r="3.6" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  };
  const sevChip = (n) => `<span class="sev" data-sev="${n}">${SHAPES[n]}SEV${n}</span>`;
  const ICON_OK = '<svg class="banner-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="m7.5 12.5 3 3 6-7" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>';
  const ICON_WARN = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v6M12 16.5v.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>';

  let S; // current state payload

  // ---- Header ---------------------------------------------------------------
  function renderHeader() {
    const n = now();
    $("clock").innerHTML = `${hhmm(n)} <small>${dayLabel(n)} · UK time</small>`;
    const f = $("freshness");
    f.dataset.feed = S.feed;
    if (S.feed === "ok") f.innerHTML = `<span class="dot"></span>Live · updated <span class="num">${hhmmss(new Date(n.getTime() - ((Date.now() - t0) % 60000)))}</span> · every 60 s`;
    else if (S.feed === "stale") f.innerHTML = `<span class="dot"></span>Not updating · last update ${hhmm(S.lastUpdate)}`;
    else if (S.feed === "down") f.innerHTML = `<span class="dot"></span>No connection to feed`;
    else f.innerHTML = `<span class="dot"></span>Connecting…`;
  }

  // ---- Feed bar (stale / down / loading) -------------------------------------
  function renderFeedbar() {
    const fb = $("feedbar");
    $("screen").dataset.feed = S.feed;
    if (S.feed === "stale") {
      const age = Math.round((now() - S.lastUpdate) / 60000);
      fb.hidden = false;
      fb.innerHTML = `${ICON_WARN}<div><strong>Data is ${age} minutes old</strong><br><span>The incident feed stopped updating at ${hhmm(S.lastUpdate)}. Everything below is frozen at that time. Check the paging tool before acting on it.</span></div>`;
    } else if (S.feed === "down") {
      fb.hidden = false;
      fb.innerHTML = `${ICON_WARN}<div><strong>Can’t reach the incident feed</strong><br><span>No data since this screen started. Retrying every 30 s. Use the paging tool directly for current incidents.</span></div>`;
    } else fb.hidden = true;
  }

  const hasData = () => S.feed === "ok" || S.feed === "stale";

  // ---- Status banner ----------------------------------------------------------
  function renderBanner() {
    const b = $("banner");
    const n = S.feed === "stale" ? S.lastUpdate : now();
    if (!hasData()) {
      b.dataset.level = "none";
      b.innerHTML = `<div></div><div><p class="banner-title placeholder">${S.feed === "loading" ? "Loading incident status…" : "Incident status unavailable"}</p><p class="banner-sub">${S.feed === "loading" ? "Connecting to the incident feed" : "Nothing below is current"}</p></div><div></div>`;
      return;
    }
    const open = S.incidents;
    const s1 = open.filter((i) => i.sev === 1);
    const s2 = open.filter((i) => i.sev === 2);
    if (s1.length) {
      const top = s1[0];
      b.dataset.level = "1";
      const ic = S.ic
        ? `<div class="callout"><span class="callout-label">Incident commander</span><span class="callout-value">${esc(S.ic.name)} <span class="muted">· since ${hhmm(S.ic.since)}</span></span></div>`
        : `<div class="callout" data-alert><span class="callout-label">Incident commander</span><span class="callout-value">Not assigned</span></div>`;
      b.innerHTML = `<div>${sevChip(1).replace('class="sev"', 'class="sev" style="font-size:var(--text-title)"')}</div>
        <div><p class="banner-title">${esc(top.title)}</p>
        <p class="banner-sub"><span class="mono">${top.id}</span> · ${esc(top.service)} · <b>${top.status}</b> · open <b class="num">${dur(n - top.opened)}</b>${s1.length > 1 ? ` · +${s1.length - 1} more SEV1` : ""}</p></div>${ic}`;
    } else if (s2.length) {
      const oldest = [...s2].sort((a, b) => a.opened - b.opened)[0];
      b.dataset.level = "2";
      b.innerHTML = `<div class="banner-count">${s2.length}</div>
        <div><p class="banner-title">${s2.length === 1 ? "SEV2 incident" : "SEV2 incidents"} open · no SEV1</p>
        <p class="banner-sub">Longest running: <b>${esc(oldest.title)}</b> · <b class="num">${dur(n - oldest.opened)}</b></p></div>
        <div class="callout"><span class="callout-label">Last SEV1 resolved</span><span class="callout-value">${lastSev1Label(n)}</span></div>`;
    } else {
      const last = [...S.resolved].sort((a, b) => b.resolved - a.resolved)[0];
      b.dataset.level = "clear";
      b.innerHTML = `<div>${ICON_OK}</div>
        <div><p class="banner-title">${open.length ? `No SEV1 or SEV2 open · ${plural(open.length, "minor incident")}` : "All clear · no open incidents"}</p>
        <p class="banner-sub">${last ? `Last resolved <b class="num">${dur(n - last.resolved)}</b> ago (<span class="mono">${last.id}</span>)` : ""}</p></div>
        <div class="callout"><span class="callout-label">Since last SEV1</span><span class="callout-value">${plural(S.daysSinceSev1, "day")}</span></div>`;
    }
  }
  function lastSev1Label(n) {
    const r = S.resolved.find((i) => i.sev === 1);
    return r ? `${dur(n - r.resolved)} ago` : plural(S.daysSinceSev1, "day") + " ago";
  }

  // ---- Open incidents ---------------------------------------------------------
  function renderIncidents() {
    const list = $("incidents");
    const meta = $("open-meta");
    if (!hasData()) {
      meta.innerHTML = "";
      list.innerHTML = `<li class="empty"><strong class="placeholder">—</strong>${S.feed === "loading" ? "Waiting for data" : "No data"}</li>`;
      return;
    }
    const n = S.feed === "stale" ? S.lastUpdate : now();
    const open = [...S.incidents].sort((a, b) => a.sev - b.sev || a.opened - b.opened);
    const diff = open.length - S.kpis.openYesterday;
    const counts = [1, 2, 3].map((k) => [k, open.filter((i) => i.sev === k).length]).filter(([, c]) => c);
    meta.innerHTML = open.length
      ? `<b class="num">${open.length}</b> open · ${counts.map(([k, c]) => `${c} SEV${k}`).join(", ")} · <span class="delta" data-good="${diff <= 0}">${diff > 0 ? "▲" : diff < 0 ? "▼" : "="} ${Math.abs(diff)} ${diff >= 0 ? "more" : "fewer"} than yesterday</span>`
      : "";
    if (!open.length) {
      // Calm, but not blank: show what was fixed most recently, visibly quieter.
      const recent = [...S.resolved].sort((a, b) => b.resolved - a.resolved).slice(0, 4);
      list.innerHTML = `<li class="empty"><strong>Nothing open.</strong>New incidents appear here, most severe first.</li>` +
        (recent.length ? `<li class="incidents-subhead">Recently resolved</li>` : "") +
        recent.map((i) => `<li class="incident is-resolved">${sevChip(i.sev)}
          <div style="min-width:0"><p class="incident-title">${esc(i.title)}</p>
          <p class="incident-meta"><span class="mono">${i.id}</span> · ${esc(i.service)} · took ${dur(i.resolved - i.opened)}</p></div>
          <p class="incident-age">${dur(n - i.resolved)}<small>ago</small></p></li>`).join("");
      return;
    }
    const row = (i) => {
      const owner = i.owner === "Unassigned" ? `<span class="warn">No owner</span>` : esc(i.owner);
      return `<li class="incident" data-sev="${i.sev}">
        ${sevChip(i.sev)}
        <div style="min-width:0"><p class="incident-title" title="${esc(i.title)}">${esc(i.title)}</p>
        <p class="incident-meta"><span class="mono">${i.id}</span> · ${esc(i.service)} · ${i.status} · ${owner}</p></div>
        <p class="incident-age"><span class="visually-hidden">Open for </span>${dur(n - i.opened)}<small>${openedLabel(i.opened, n)}</small></p>
      </li>`;
    };
    list.innerHTML = open.map(row).join("");
    // TV has no scrolling: drop the least severe rows until the list fits, and say so.
    if (root.dataset.display === "tv") {
      const panel = list.closest(".panel");
      let shown = open.length;
      while (shown > 1 && panel.scrollHeight > panel.clientHeight + 1) {
        shown--;
        const hidden = open.slice(shown);
        const n3 = hidden.filter((i) => i.sev === 3).length;
        list.innerHTML = open.slice(0, shown).map(row).join("") +
          `<li class="incidents-more">+ ${hidden.length} more${n3 === hidden.length ? " SEV3" : ""} · ${hidden.map((i) => i.id).join(", ")}</li>`;
      }
    }
  }

  // ---- KPIs -------------------------------------------------------------------
  function deltaHTML(diff, goodWhenDown, text) {
    if (diff === 0) return `<span class="delta">= ${text}</span>`;
    const good = goodWhenDown ? diff < 0 : diff > 0;
    return `<span class="delta" data-good="${good}">${diff > 0 ? "▲" : "▼"} ${text}<span class="visually-hidden">${good ? " (better)" : " (worse)"}</span></span>`;
  }
  function sparkline(values) {
    const W = 200, H = 56, pad = 6;
    const lo = Math.min(...values) * 0.9, hi = Math.max(...values) * 1.05;
    const x = (i) => pad + (i * (W - pad * 2)) / (values.length - 1);
    const y = (v) => H - pad - ((v - lo) / (hi - lo)) * (H - pad * 2);
    const pts = values.map((v, i) => `${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(" ");
    const last = values.length - 1;
    const dots = values.map((v, i) => i === last ? "" :
      `<rect class="spark-hit" x="${x(i) - 12}" y="0" width="24" height="${H}" tabindex="0" data-tip="${last - i} weeks ago: ${v} min"></rect><circle class="spark-dot" cx="${x(i)}" cy="${y(v)}" r="2.5"></circle>`).join("");
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Mean time to resolve, last 8 weeks: ${values.join(", ")} minutes">
      <polyline class="spark-line" points="${pts}"></polyline>${dots}
      <rect class="spark-hit" x="${x(last) - 12}" y="0" width="24" height="${H}" tabindex="0" data-tip="This week: ${values[last]} min"></rect>
      <circle class="spark-last" cx="${x(last)}" cy="${y(values[last])}" r="5"></circle></svg>`;
  }
  function meter(pct) {
    const W = 200, H = 14, r = 4;
    const level = pct < 10 ? 1 : pct < 25 ? 2 : 0;
    const w = Math.max(r * 2, (pct / 100) * W);
    return `<svg viewBox="0 0 ${W} ${H + 8}" role="img" aria-label="${pct}% of error budget left">
      <rect class="meter-track" x="0" y="0" width="${W}" height="${H}" rx="${r}"></rect>
      <rect class="meter-fill" data-level="${level}" x="0" y="0" width="${w}" height="${H}" rx="${r}"></rect>
      <line class="meter-tick" x1="${W * 0.25}" x2="${W * 0.25}" y1="${H + 1}" y2="${H + 7}"></line></svg>`;
  }
  function renderKPIs() {
    const k = S.kpis;
    const box = $("kpis");
    if (!hasData()) {
      box.innerHTML = ["Time to resolve · 7 days", "Pages today", "Error budget left"].map((l) =>
        `<div class="kpi"><div><p class="kpi-label">${l}</p><p class="kpi-value placeholder">—</p></div><div></div></div>`).join("");
      return;
    }
    const m = k.mttr, p = k.pages, b = k.budget;
    const mPct = Math.round(((m.value - m.prior) / m.prior) * 100);
    box.innerHTML = `
      <div class="kpi"><div><p class="kpi-label">Mean time to resolve · 7 days</p>
        <p class="kpi-value">${m.value}<span class="unit">min</span></p>
        ${deltaHTML(m.value - m.prior, true, `${Math.abs(m.value - m.prior)} min (${Math.abs(mPct)}%) vs last week`)}</div>
        <div class="kpi-viz">${sparkline(m.weeks)}<p class="viz-caption">Last 8 weeks</p></div></div>
      <div class="kpi"><div><p class="kpi-label">Pages today</p>
        <p class="kpi-value">${p.today}</p>
        ${deltaHTML(p.today - p.yesterday, true, `${Math.abs(p.today - p.yesterday)} vs yesterday`)}</div>
        <div class="kpi-viz"><p class="viz-caption">7-day average <b class="num">${p.avg7}</b> a day</p></div></div>
      <div class="kpi"><div><p class="kpi-label">Error budget left · ${b.window}</p>
        <p class="kpi-value">${b.left}<span class="unit">%</span></p>
        ${deltaHTML(b.left - b.weekAgo, false, `${Math.abs(b.left - b.weekAgo)} pts this week`)}</div>
        <div class="kpi-viz">${meter(b.left)}<p class="viz-caption">Below the 25% mark, freeze risky changes</p></div></div>`;
  }

  // ---- On call ------------------------------------------------------------------
  function renderOncall() {
    const ul = $("oncall");
    $("oncall-meta").textContent = hasData() ? `Next handover ${S.oncall[0].until}` : "";
    if (!hasData()) { ul.innerHTML = `<li class="empty"><strong class="placeholder">—</strong></li>`; return; }
    const n = S.feed === "stale" ? S.lastUpdate : now();
    const people = S.oncall.map((p) => `<li class="person"><span class="person-role">${p.role}</span>
      <span class="person-name">${esc(p.name)} <span>· ${esc(p.team)}</span></span><span class="person-until">until ${p.until}</span></li>`);
    const major = S.incidents.filter((i) => i.sev <= 2);
    const sev1 = S.incidents.find((i) => i.sev === 1);
    let ic;
    if (S.ic) ic = `<li class="person"><span class="person-role">Incident commander</span><span class="person-name">${esc(S.ic.name)} <span>· ${esc(S.ic.team)}</span></span><span class="person-until">since ${hhmm(S.ic.since)}</span></li>`;
    else if (sev1) ic = `<li class="person" data-alert><span class="person-role">Incident commander</span><span class="person-name">Not assigned</span><span class="person-until">SEV1 open ${dur(n - sev1.opened)}</span></li>`;
    else ic = `<li class="person" data-quiet><span class="person-role">Incident commander</span><span class="person-name">Not needed</span><span class="person-until">${major.length ? "SEV2s run by on-call" : "nothing major open"}</span></li>`;
    ul.innerHTML = people.join("") + ic;
  }

  // ---- Services bars ----------------------------------------------------------
  function renderServices() {
    const box = $("services");
    if (!hasData()) { box.innerHTML = `<p class="empty placeholder">—</p>`; return; }
    const rows = S.byService;
    const total = rows.reduce((a, r) => a + r.n, 0);
    const fs = parseFloat(getComputedStyle(root).fontSize);
    const tv = root.dataset.display === "tv";
    const W = box.clientWidth || 600;
    const labelW = Math.min(W * 0.36, fs * (tv ? 12 : 11));
    const valueW = fs * 2.6;
    const rowH = Math.round(fs * (tv ? 1.55 : 2));
    const barH = Math.min(24, Math.round(rowH * 0.5));
    const max = Math.max(...rows.map((r) => r.n));
    const H = rows.length * rowH;
    const bw = (n) => Math.max(4, (n / max) * (W - labelW - valueW));
    box.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" role="img" aria-label="Incidents by service in the last 30 days: ${rows.map((r) => `${r.service} ${r.n}`).join(", ")}">
      <line x1="${labelW}" x2="${labelW}" y1="0" y2="${H}" stroke="var(--line)" stroke-width="1"></line>
      ${rows.map((r, i) => {
        const y = i * rowH, w = bw(r.n), cy = y + rowH / 2;
        return `<g class="svc-row" tabindex="0" data-tip="${esc(r.service)}: ${r.n} incidents in 30 days (${Math.round((r.n / total) * 100)}% of ${total})">
          <rect class="svc-hit" x="0" y="${y}" width="${W}" height="${rowH}"></rect>
          <text class="svc-label" x="${labelW - fs * 0.6}" y="${cy}" dominant-baseline="central" text-anchor="end">${esc(r.service)}</text>
          <path class="svc-bar" d="M${labelW + 1},${cy - barH / 2} h${w - 4} a4,4 0 0 1 4,4 v${barH - 8} a4,4 0 0 1 -4,4 h-${w - 4} z"></path>
          <text class="svc-value" x="${labelW + 1 + w + fs * 0.5}" y="${cy}" dominant-baseline="central">${r.n}</text></g>`;
      }).join("")}</svg>`;
  }

  // ---- Resolved table --------------------------------------------------------------
  function renderResolved() {
    const t = $("resolved");
    if (!hasData()) { t.innerHTML = `<tbody><tr><td class="placeholder">—</td></tr></tbody>`; return; }
    t.innerHTML = `<thead><tr><th>Severity</th><th>ID</th><th>Title</th><th>Service</th><th class="r">Duration</th><th class="r">Resolved</th></tr></thead><tbody>` +
      S.resolved.map((i) => `<tr><td>${sevChip(i.sev)}</td><td class="mono">${i.id}</td><td class="title">${esc(i.title)}</td><td>${esc(i.service)}</td>
        <td class="r">${dur(i.resolved - i.opened)}</td><td class="r">${dayLabel(i.resolved) === dayLabel(SNAPSHOT) ? "Today" : i.resolved.toLocaleDateString("en-GB", { weekday: "short", timeZone: tz })} ${hhmm(i.resolved)}</td></tr>`).join("") + `</tbody>`;
  }

  // ---- Tooltip (hover + keyboard focus show the same thing) ---------------------
  const tip = $("tooltip");
  function showTip(el, x, y) {
    if (root.dataset.display === "tv") return;
    tip.textContent = el.dataset.tip;
    tip.hidden = false;
    const r = tip.getBoundingClientRect();
    tip.style.left = Math.min(window.innerWidth - r.width - 8, x + 12) + "px";
    tip.style.top = Math.max(8, y - r.height - 10) + "px";
  }
  document.addEventListener("pointermove", (e) => {
    const el = e.target.closest && e.target.closest("[data-tip]");
    if (el) showTip(el, e.clientX, e.clientY); else tip.hidden = true;
  });
  document.addEventListener("focusin", (e) => {
    const el = e.target.closest && e.target.closest("[data-tip]");
    if (el) { const r = el.getBoundingClientRect(); showTip(el, r.left + r.width / 2, r.top); } else tip.hidden = true;
  });
  document.addEventListener("focusout", () => (tip.hidden = true));

  // ---- Demo switcher -----------------------------------------------------------------
  function buildDemo() {
    const groups = { state: STATES, display: DISPLAYS, theme: THEMES };
    for (const [g, opts] of Object.entries(groups)) {
      const row = document.querySelector(`.demo-row[data-group="${g}"]`);
      row.innerHTML = opts.map(([v, l]) => `<button type="button" data-v="${v}">${l}</button>`).join("");
      row.addEventListener("click", (e) => {
        const btn = e.target.closest("button"); if (!btn) return;
        if (g === "display") settings.theme = null; // theme follows display unless chosen
        settings[g] = btn.dataset.v;
        apply();
      });
    }
    const toggle = $("demo-toggle"), body = $("demo-body");
    const set = (open) => { body.hidden = !open; toggle.setAttribute("aria-expanded", String(open)); };
    toggle.addEventListener("click", () => set(body.hidden));
    document.addEventListener("keydown", (e) => { if (e.key.toLowerCase() === "d" && !e.metaKey && !e.ctrlKey) set(body.hidden); });
    if (params.has("demo")) set(true);
  }
  function syncDemo() {
    const cur = { state: settings.state, display: root.dataset.display, theme: root.dataset.theme };
    document.querySelectorAll(".demo-row").forEach((row) => {
      row.querySelectorAll("button").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.v === cur[row.dataset.group])));
    });
    const u = new URL(location.href);
    u.searchParams.set("state", settings.state);
    u.searchParams.set("display", settings.display);
    if (settings.theme) u.searchParams.set("theme", settings.theme); else u.searchParams.delete("theme");
    history.replaceState(null, "", u);
  }

  function renderAll() {
    // Incidents last: on TV the list trims itself to the space the other panels leave.
    renderHeader(); renderFeedbar(); renderBanner();
    renderKPIs(); renderOncall(); renderServices(); renderResolved(); renderIncidents();
  }
  function apply() {
    root.dataset.display = settings.display;
    root.dataset.theme = themeFor(settings.display);
    S = buildState(settings.state);
    renderAll();
    syncDemo();
  }

  buildDemo();
  apply();
  // Ages and the clock move on their own; a real feed would replace S every 60 s.
  setInterval(() => { renderHeader(); if (S.feed === "ok") { renderBanner(); renderIncidents(); renderOncall(); } }, 1000);
  let rz; window.addEventListener("resize", () => { clearTimeout(rz); rz = setTimeout(renderServices, 100); });
})();
