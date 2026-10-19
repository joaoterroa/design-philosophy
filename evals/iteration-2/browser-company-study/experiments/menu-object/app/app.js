/* Rota: menu-bar on-call schedule + shift handover. Prototype logic over sample data. */
(() => {
  const D = window.ROTA_DATA;
  const P = D.people;
  const $ = (sel, root = document) => root.querySelector(sel);
  const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));

  // ---------- time ----------
  const DAYS = ["Sat", "Sun", "Mon", "Tue", "Wed", "Thu", "Fri"];
  const DATES = [18, 19, 20, 21, 22, 23, 24];
  const dayIdx = (h) => Math.floor(h / 24);
  const pad = (n) => String(n).padStart(2, "0");
  const hhmm = (h) => { const m = Math.round((((h % 24) + 24) % 24) * 60); return `${pad(Math.floor(m / 60) % 24)}:${pad(m % 60)}`; };
  const dayName = (h) => { const i = dayIdx(h); return i >= 0 && i < 7 ? DAYS[i] : DAYS[((i % 7) + 7) % 7]; };
  const dayDate = (h) => { const i = dayIdx(h); return i >= 0 && i < 7 ? `${DAYS[i]} ${DATES[i]} Oct` : (i >= 7 ? `${DAYS[i % 7]} ${18 + i} Oct` : `${DAYS[((i % 7) + 7) % 7]} ${18 + i} Oct`); };
  const when = (h) => (dayIdx(h) === dayIdx(D.now) ? hhmm(h) : `${dayName(h)} ${hhmm(h)}`);
  // Ranges never break mid-range: non-breaking spaces, and word joiners around the dash.
  const range = (a, b) => (dayIdx(a) === dayIdx(b) ? `${dayName(a)}\u00a0${hhmm(a)}\u2060–\u2060${hhmm(b)}` : `${dayName(a)}\u00a0${hhmm(a)}\u00a0→ ${dayName(b)}\u00a0${hhmm(b)}`);
  const hours = (n) => { const r = Math.round(n); return `${r} hour${r === 1 ? "" : "s"}`; };
  const longLeft = (n) => { const d = Math.floor(n / 24), h = Math.round(n - d * 24); return d ? `${d} day${d > 1 ? "s" : ""} ${h} hour${h === 1 ? "" : "s"}` : `${Math.floor(n)} hours ${Math.round((n % 1) * 60)} min`; };
  const shortLeft = (n) => { const d = Math.floor(n / 24), h = Math.floor(n - d * 24), m = Math.round((n % 1) * 60); return d ? `${d}d ${h}h` : `${h}h ${pad(m)}m`; };
  const first = (id) => P[id].name.split(" ")[0];
  const theirTime = (id, a, b) => { const tz = P[id].tz; return tz ? `${hhmm(a + tz)}–${hhmm(b + tz)} in ${P[id].city}` : ""; };

  // ---------- state ----------
  const SCENARIOS = [
    ["oncall", "On call"],
    ["offcall", "Not on call"],
    ["compose", "Hand over: choosing"],
    ["sendfail", "Hand over: send failed"],
    ["pending", "Waiting for reply"],
    ["accepted", "Handover accepted"],
    ["declined", "Handover declined"],
    ["incoming", "Someone asks you"],
    ["gap", "Gap in coverage"],
    ["offline", "Offline (cached)"],
    ["loading", "First sync"],
    ["connect", "Not connected"],
  ];
  const defaultCompose = () => ({ mode: "part", start: 34, end: 42, to: null, query: "", note: "", linkInc: true });
  let S;
  function scenario(name) {
    S = { name, view: "main", open: true, onCall: true, connected: true, loading: false, offline: false, incoming: false, gap: false,
      handover: null, sendError: false, compose: defaultCompose(), menu: false, gapCovered: false, incomingDone: null };
    const pr = { to: "pr", start: 34, end: 42 };
    if (name === "offcall") S.onCall = false;
    if (name === "compose") { S.view = "compose"; S.compose.to = "pr"; S.compose.note = "INC-4821 is mitigated but the checkout p99 alert is still flappy; safe to ack."; }
    if (name === "sendfail") { S.view = "compose"; S.compose.to = "pr"; S.sendError = true; S.compose.note = "INC-4821 is mitigated but the checkout p99 alert is still flappy; safe to ack."; }
    if (name === "pending") S.handover = { ...pr, status: "pending", ago: "2 min ago" };
    if (name === "accepted") S.handover = { ...pr, status: "accepted" };
    if (name === "declined") S.handover = { ...pr, status: "declined", reason: "At my sister’s wedding all Sunday, sorry." };
    if (name === "incoming") S.incoming = true;
    if (name === "gap") S.gap = true;
    if (name === "offline") S.offline = true;
    if (name === "loading") S.loading = true;
    if (name === "connect") S.connected = false;
    render();
  }

  const left = () => D.myShift.to - D.now;
  const shiftFrac = () => left() / (D.myShift.to - D.myShift.from);

  // ---------- mark: a dial whose filled wedge is the share of your shift still to run ----------
  function mark(frac, dot) {
    const r = 5, cx = 8, cy = 8;
    let wedge = "";
    if (frac > 0) {
      const a = Math.min(frac, 0.999) * 2 * Math.PI;
      const x = cx + r * Math.sin(a), y = cy - r * Math.cos(a);
      wedge = `<path d="M${cx} ${cy} L${cx} ${cy - r} A${r} ${r} 0 ${a > Math.PI ? 1 : 0} 1 ${x.toFixed(2)} ${y.toFixed(2)} Z" fill="currentColor"/>`;
    } else {
      wedge = `<path d="M8 2.6 V5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>`;
    }
    const badge = dot ? `<circle cx="13.6" cy="2.6" r="2.4" fill="currentColor"/>` : "";
    const mask = dot ? `<mask id="m"><rect width="16" height="16" fill="white"/><circle cx="13.6" cy="2.6" r="3.6" fill="black"/></mask>` : "";
    return `<svg class="mark" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true">${mask}<g ${dot ? 'mask="url(#m)"' : ""}><circle cx="8" cy="8" r="6.75" fill="none" stroke="currentColor" stroke-width="1.5"/>${wedge}</g>${badge}</svg>`;
  }

  function renderStatusItem() {
    const el = $("#status-item");
    const on = S.connected && !S.loading && S.onCall;
    const title = on ? shortLeft(left()) : "";
    el.innerHTML = mark(on ? shiftFrac() : 0, S.incoming && !S.incomingDone) + (title ? `<span class="status-title">${title}</span>` : "");
    el.classList.toggle("is-open", S.open);
    el.classList.toggle("is-stale", S.offline);
    el.setAttribute("aria-expanded", String(S.open));
    const label = !S.connected ? "Rota, not connected" : on ? `Rota, you’re on call, ${longLeft(left())} left` : "Rota, you’re not on call";
    el.setAttribute("aria-label", label + (S.incoming && !S.incomingDone ? ", 1 request waiting" : "") + (S.offline ? ", offline" : ""));
  }

  // ---------- shift strip ----------
  // Window shown: now -> Tue 00:00 (the past is not yours to hand over). Segments: [from, to, kind, who]
  const WIN = [D.now, 72];
  function stripSegments(override) {
    const base = [[WIN[0], 57, "you", "je"], [57, WIN[1], "other", "ob"]];
    if (!override) return base;
    const out = [];
    for (const [a, b, k, w] of base) {
      if (override.end <= a || override.start >= b) { out.push([a, b, k, w]); continue; }
      if (override.start > a) out.push([a, override.start, k, w]);
      out.push([Math.max(a, override.start), Math.min(b, override.end), override.kind, override.who]);
      if (override.end < b) out.push([override.end, b, k, w]);
    }
    return out;
  }
  let lastPreviewKey = "";
  function strip(override, large) {
    const span = WIN[1] - WIN[0];
    const pct = (h) => ((h - WIN[0]) / span) * 100;
    const segs = stripSegments(override);
    const key = override ? `${override.kind}${override.who}${override.start}${override.end}` : "";
    const animate = override && override.kind === "preview" && key !== lastPreviewKey;
    if (override && override.kind === "preview") lastPreviewKey = key;
    const words = [];
    const html = segs.map(([a, b, k, w]) => {
      const name = w ? (w === D.me ? "You" : P[w].name) : "Nobody yet";
      const status = k === "pending" ? ` (asked ${first(w)}; still yours until accepted)` : k === "preview" ? " (if accepted)" : "";
      words.push(`${name} ${range(a, b)}${status}`);
      const wpx = ((b - a) / span) * 316;
      const label = !w ? "" : w === D.me ? (wpx > 30 ? "You" : "") : wpx > 64 ? first(w) : wpx > 26 ? P[w].initials : "";
      return `<span class="seg seg-${k}${animate && k === "preview" ? " is-entering" : ""}" style="left:${pct(a)}%;width:${pct(b) - pct(a)}%" title="${esc(name + " · " + range(a, b) + status)}"><span class="seg-label">${esc(label)}${k === "pending" ? "?" : ""}</span></span>`;
    }).join("");
    const ticks = [24, 48].map((h) => `<span class="tick" style="left:${pct(h)}%"></span>`).join("");
    const days = [[D.now, "Now"], [24, "Sun"], [48, "Mon"]].map(([h, d]) => `<span class="day" style="left:${pct(h)}%">${d}</span>`).join("");
    return `<div class="strip${large ? " strip-lg" : ""}" role="img" aria-label="Platform Primary from now to Tuesday: ${esc(words.join("; "))}">
      <div class="strip-track">${html}</div><div class="strip-days" aria-hidden="true">${ticks}${days}</div></div>`;
  }

  // ---------- main view ----------
  function avatar(id) { return `<span class="avatar" aria-hidden="true">${P[id].initials}</span>`; }

  function needsYou() {
    let out = "";
    if (S.incoming) {
      const r = D.incoming;
      if (S.incomingDone) {
        out += `<section class="needs" aria-live="polite"><p class="needs-text">${S.incomingDone === "accept" ? `You’re covering ${r.rotation} ${r.layer} ${range(r.start, r.end)} for ${first(r.from)}. It’s in PagerDuty.` : `Declined. ${first(r.from)} has been told.`}</p></section>`;
      } else {
        out += `<section class="needs" aria-labelledby="inc-h">
          <h2 class="needs-title" id="inc-h">${esc(P[r.from].name)} asks you to cover</h2>
          <p class="needs-text"><strong>${r.rotation} ${r.layer}</strong>, ${range(r.start, r.end)} (${hours(r.end - r.start)})</p>
          <blockquote class="quote">${esc(r.note)}</blockquote>
          <p class="caption">${esc(r.fit)}</p>
          <div class="actions"><button class="btn" data-act="inc-decline">Decline…</button><button class="btn btn-primary" data-act="inc-accept">Cover it</button></div>
        </section>`;
      }
    }
    if (S.gap) {
      const g = D.gap;
      out += S.gapCovered
        ? `<section class="needs" aria-live="polite"><p class="needs-text">Posted in #sre-oncall. The gap stays here until someone takes it.</p></section>`
        : `<section class="needs needs-danger" aria-labelledby="gap-h">
          <h2 class="needs-title" id="gap-h">${g.rotation} ${g.layer} has nobody on call ${range(g.start, g.end)}</h2>
          <p class="caption">${esc(g.reason)} Pages then go straight to ${g.rotation} Secondary.</p>
          <div class="actions"><button class="btn" data-act="gap-cover">Ask in #sre-oncall</button></div>
        </section>`;
    }
    return out;
  }

  function handoverNote() {
    const h = S.handover; if (!h) return "";
    const n = P[h.to].name;
    if (h.status === "pending") return `<div class="note note-pending" role="status">
      <p><strong>Waiting for ${esc(n)}</strong> to cover ${range(h.start, h.end)}. Asked ${h.ago}.</p>
      <p class="caption-on">You’re still on call until ${first(h.to)} accepts.</p>
      <button class="link" data-act="cancel-req">Cancel request</button></div>`;
    if (h.status === "accepted") return `<p class="line" role="status">${esc(n)} covers ${range(h.start, h.end)}. It’s in PagerDuty as an override.</p>`;
    if (h.status === "declined") return `<div class="line-block" role="status"><p class="line">${esc(first(h.to))} can’t cover ${range(h.start, h.end)}: “${esc(h.reason)}”</p>
      <p class="caption">You’re still on call then.</p><button class="btn" data-act="ask-other">Ask someone else…</button></div>`;
    return "";
  }

  function youSection() {
    const disabled = S.offline ? " disabled aria-describedby=\"offline-why\"" : "";
    const why = S.offline ? `<p class="caption" id="offline-why">Handing over needs a connection to PagerDuty.</p>` : "";
    if (!S.onCall) {
      const n = D.myNextShift;
      return `<section class="you" aria-labelledby="you-h">
        <h2 class="answer" id="you-h">You’re not on call</h2>
        <p class="caption">Next: ${n.rotation} ${n.layer}, ${dayDate(n.from)} ${hhmm(n.from)} → ${dayDate(n.to)} ${hhmm(n.to)} · in 4 days</p>
        <div class="actions actions-start"><button class="btn" data-act="handover"${disabled}>Hand over…</button></div>${why}
      </section>`;
    }
    const h = S.handover;
    const ov = h && h.status !== "declined" ? { start: h.start, end: h.end, kind: h.status === "pending" ? "pending" : "other", who: h.to } : null;
    const showBtn = !(h && h.status === "declined");
    return `<section class="you" aria-labelledby="you-h">
      <p class="eyebrow">You’re on call · ${D.myShift.rotation} ${D.myShift.layer}</p>
      <h2 class="answer" id="you-h">${longLeft(left())} left</h2>
      <p class="caption">Until ${dayDate(D.myShift.to)}, ${hhmm(D.myShift.to)}, then ${esc(P[D.myShift.next].name)}</p>
      ${strip(ov, false)}
      ${handoverNote()}
      ${showBtn ? `<div class="actions actions-start"><button class="btn" data-act="handover"${disabled}>Hand over…</button></div>${why}` : ""}
    </section>`;
  }

  function nowSection() {
    const rows = D.onCallNow.map((r) => {
      const me = r.who === D.me;
      const name = me ? "You" : P[r.who].name;
      return `<li><a class="row" href="slack://user?team=sre&id=${P[r.who].handle}" ${me ? 'aria-current="true"' : `aria-label="${esc(`${name}, ${r.rotation} ${r.layer} until ${dayDate(r.until)} ${hhmm(r.until)}. Message on Slack`)}"`}>
        ${avatar(r.who)}
        <span class="row-main"><span class="row-name">${esc(name)}</span><span class="row-sub">${r.rotation} ${r.layer}${me ? "" : ` · @${P[r.who].handle}`}</span></span>
        <span class="row-until">until ${when(r.until)}</span></a></li>`;
    }).join("");
    return `<section class="now-list" aria-labelledby="now-h"><h2 class="section-title" id="now-h">On call now</h2><ul class="rows">${rows}</ul></section>`;
  }

  function footer() {
    const sync = S.offline
      ? `<p class="sync sync-stale">Offline. Showing the schedule as of 13:02; it may have changed since.</p>`
      : `<p class="sync">Synced from PagerDuty 1 min ago</p>`;
    const menu = S.menu ? `<div class="menu" role="menu" aria-label="Rota">
      <button role="menuitem" class="menu-item">Open schedule in PagerDuty</button>
      <button role="menuitem" class="menu-item">Settings…<span class="kbd">⌘,</span></button>
      <span class="menu-sep" role="separator"></span>
      <button role="menuitem" class="menu-item">Quit Rota<span class="kbd">⌘Q</span></button></div>` : "";
    return `<footer class="foot">${sync}<button class="icon-btn" data-act="menu" aria-label="More" aria-haspopup="menu" aria-expanded="${S.menu}" data-focus="menu"><svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><circle cx="3.5" cy="8" r="1.3" fill="currentColor"/><circle cx="8" cy="8" r="1.3" fill="currentColor"/><circle cx="12.5" cy="8" r="1.3" fill="currentColor"/></svg></button>${menu}</footer>`;
  }

  function mainView() {
    if (!S.connected) return `<div class="empty">
      ${mark(0.35, false).replace('class="mark"', 'class="mark mark-lg"')}
      <h2 class="answer">See who’s on call, and hand over shifts</h2>
      <p class="caption">Rota reads your team’s schedules from PagerDuty. It only changes them when you hand over or cover a shift.</p>
      <div class="actions actions-center"><button class="btn btn-primary" data-act="connect">Sign in to PagerDuty…</button></div>
      <p class="caption">Uses your company SSO.</p></div>`;
    if (S.loading) return `<div class="loading" role="status"><span class="spinner" aria-hidden="true"></span><p class="caption">Getting schedules from PagerDuty…</p></div>`;
    return needsYou() + youSection() + nowSection() + footer();
  }

  // ---------- compose view ----------
  const STARTS = () => { const out = [Math.ceil(D.now)]; for (let h = Math.ceil(D.now) + 1; h < D.myShift.to; h++) out.push(h); return out; };
  function opt(h, sel) { return `<option value="${h}"${h === sel ? " selected" : ""}>${dayName(h)} ${hhmm(h)}</option>`; }
  function eligible() {
    const q = S.compose.query.trim().toLowerCase();
    const order = { free: 0, caution: 1, blocked: 2 };
    return D.platformMembers.filter((id) => !q || P[id].name.toLowerCase().includes(q) || P[id].handle.includes(q))
      .sort((a, b) => order[D.availability[a].kind] - order[D.availability[b].kind]);
  }
  function peopleList() {
    const c = S.compose, [a, b] = composeRange();
    const ids = eligible();
    if (!ids.length) return `<p class="caption list-empty">Nobody in the Platform rotation matches “${esc(c.query)}”.</p>`;
    return ids.map((id) => {
      const av = D.availability[id], tt = theirTime(id, a, b);
      const blocked = av.kind === "blocked";
      return `<label class="person${c.to === id ? " is-selected" : ""}${blocked ? " is-blocked" : ""}">
        <input type="radio" name="to" value="${id}"${c.to === id ? " checked" : ""}${blocked ? " disabled" : ""} data-focus="to-${id}">
        ${avatar(id)}<span class="row-main"><span class="row-name">${esc(P[id].name)}</span>
        <span class="row-sub${av.kind === "caution" ? " sub-caution" : ""}">${esc(av.text)}${tt ? ` · ${tt}` : ""}</span></span></label>`;
    }).join("");
  }
  function composeRange() { const c = S.compose; return c.mode === "rest" ? [D.now, D.myShift.to] : [c.start, c.end]; }
  function summary() {
    const c = S.compose, [a, b] = composeRange();
    if (b <= a) return `<p class="summary summary-error" role="alert">“Until” has to be after “From”.</p>`;
    if (S.sendError) return `<div class="summary-error-block" role="alert"><p><strong>Couldn’t send the request.</strong> PagerDuty didn’t answer within 10 seconds.</p><p>Nothing changed: you’re still on call. Your note is kept.</p></div>`;
    if (!c.to) return `<p class="summary">Choose who covers ${range(a, b)} (${hours(b - a)}).</p>`;
    const f = first(c.to);
    const caution = D.availability[c.to].kind === "caution" ? ` ${esc(D.availability[c.to].text)}.` : "";
    const what = c.mode === "rest" ? `The rest of your shift (to ${dayName(b)} ${hhmm(b)})` : `${range(a, b)} (${hours(b - a)})`;
    return `<p class="summary">${what} moves to ${f} once accepted. Until then it’s still yours.${caution}</p>`;
  }
  function composeView() {
    const c = S.compose, [a, b] = composeRange();
    const ov = { start: a, end: b, kind: "preview", who: c.to };
    const inc = D.openIncidents[0];
    const sendLabel = S.sendError ? "Try again" : c.to ? `Ask ${first(c.to)}` : "Ask";
    const valid = b > a && c.to;
    return `<header class="compose-head">
        <button class="icon-btn" data-act="back" aria-label="Back" data-focus="back"><svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M10 3 5 8l5 5" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></button>
        <div><h2 class="section-title-lg" id="compose-h">Hand over</h2><p class="caption">${D.myShift.rotation} ${D.myShift.layer} · yours until ${dayName(D.myShift.to)} ${hhmm(D.myShift.to)}</p></div>
      </header>
      <div class="compose-body">
        <div id="compose-strip">${strip(ov, true)}</div>
        <fieldset class="field"><legend class="legend">Which part</legend>
          <label class="choice"><input type="radio" name="mode" value="rest"${c.mode === "rest" ? " checked" : ""} data-focus="mode-rest"><span>The rest of my shift <span class="caption-inline">now → ${dayName(D.myShift.to)} ${hhmm(D.myShift.to)}, ${hours(D.myShift.to - D.now)}</span></span></label>
          <label class="choice"><input type="radio" name="mode" value="part"${c.mode === "part" ? " checked" : ""} data-focus="mode-part"><span>Part of it</span></label>
          <div class="times"${c.mode === "part" ? "" : " hidden"}>
            <label class="time"><span class="caption">From</span><select name="start" data-focus="start">${STARTS().map((h) => opt(h, c.start)).join("")}</select></label>
            <label class="time"><span class="caption">Until</span><select name="end" data-focus="end">${STARTS().slice(1).concat([D.myShift.to]).map((h) => opt(h, c.end)).join("")}</select></label>
          </div>
        </fieldset>
        <fieldset class="field"><legend class="legend">Who covers</legend>
          <input class="search" type="search" name="q" placeholder="Search Platform rotation (11)" value="${esc(c.query)}" aria-label="Search people in the Platform rotation" data-focus="q">
          <div class="people" id="people" role="radiogroup" aria-label="Who covers">${peopleList()}</div>
        </fieldset>
        <fieldset class="field"><legend class="legend">Note${c.to ? ` for ${first(c.to)}` : ""} <span class="caption-inline">optional</span></legend>
          <textarea name="note" rows="2" placeholder="Anything they should know: open work, noisy alerts" data-focus="note">${esc(c.note)}</textarea>
          <label class="check"><input type="checkbox" name="linkInc"${c.linkInc ? " checked" : ""} data-focus="linkInc"><span>Link open incident <span class="caption-inline">${inc.id} ${esc(inc.title)}, ${inc.sev}, ${inc.status}</span></span></label>
        </fieldset>
      </div>
      <footer class="compose-foot"><div id="summary">${summary()}</div>
        <div class="actions"><button class="btn" data-act="back">Cancel</button><button class="btn btn-primary" data-act="send" data-focus="send"${valid ? "" : " disabled"}>${sendLabel}</button></div>
      </footer>`;
  }

  // ---------- render ----------
  function render() {
    const pop = $("#popover");
    const focusKey = document.activeElement && document.activeElement.dataset ? document.activeElement.dataset.focus : null;
    renderStatusItem();
    pop.hidden = !S.open;
    pop.classList.toggle("is-compose", S.view === "compose");
    pop.setAttribute("aria-labelledby", S.view === "compose" ? "compose-h" : "");
    pop.innerHTML = S.view === "compose" ? composeView() : mainView();
    if (focusKey) { const el = pop.querySelector(`[data-focus="${focusKey}"]`); if (el) el.focus(); }
    renderControls();
  }

  function renderControls() {
    $("#state-list").innerHTML = SCENARIOS.map(([k, l]) => `<label class="ctl"><input type="radio" name="scenario" value="${k}"${S.name === k ? " checked" : ""}> ${l}</label>`).join("");
    const t = document.documentElement.dataset.theme || "system";
    $("#theme-list").innerHTML = [["system", "System"], ["light", "Light"], ["dark", "Dark"]].map(([k, l]) => `<label class="ctl"><input type="radio" name="theme" value="${k}"${t === k ? " checked" : ""}> ${l}</label>`).join("");
  }

  // ---------- events ----------
  document.addEventListener("click", (e) => {
    const si = e.target.closest("#status-item");
    if (si) { S.open = !S.open; S.menu = false; render(); return; }
    const btn = e.target.closest("[data-act]");
    if (!btn) { if (S.menu && !e.target.closest(".menu")) { S.menu = false; render(); } return; }
    const act = btn.dataset.act;
    if (act === "handover" || act === "ask-other") {
      S.view = "compose"; S.sendError = false;
      if (act === "ask-other") { S.compose = { ...defaultCompose(), start: S.handover.start, end: S.handover.end }; S.handover = null; }
      if (!S.onCall) { S.compose.mode = "rest"; }
      render(); $("#popover [name=mode]:checked")?.focus(); return;
    }
    if (act === "back") { S.view = "main"; render(); $('#popover [data-act="handover"]')?.focus(); return; }
    if (act === "send") {
      const [a, b] = composeRange();
      S.handover = { to: S.compose.to, start: a, end: b, status: "pending", ago: "just now" };
      S.view = "main"; S.sendError = false; render(); $("#popover .note")?.focus(); return;
    }
    if (act === "cancel-req") { S.handover = null; render(); $('#popover [data-act="handover"]')?.focus(); return; }
    if (act === "inc-accept") { S.incomingDone = "accept"; render(); return; }
    if (act === "inc-decline") { S.incomingDone = "decline"; render(); return; }
    if (act === "gap-cover") { S.gapCovered = true; render(); return; }
    if (act === "connect") { S.connected = true; S.loading = true; render(); setTimeout(() => { S.loading = false; render(); }, 1200); return; }
    if (act === "menu") { S.menu = !S.menu; render(); if (S.menu) $("#popover .menu-item")?.focus(); }
  });

  document.addEventListener("change", (e) => {
    const t = e.target;
    if (t.name === "scenario") { scenario(t.value); return; }
    if (t.name === "theme") { if (t.value === "system") delete document.documentElement.dataset.theme; else document.documentElement.dataset.theme = t.value; renderControls(); $(`[name=theme][value=${t.value}]`).focus(); return; }
    const c = S.compose;
    if (t.name === "mode") { c.mode = t.value; render(); return; }
    if (t.name === "start") { c.start = +t.value; if (c.end <= c.start) c.end = Math.min(c.start + 1, D.myShift.to); render(); return; }
    if (t.name === "end") { c.end = +t.value; render(); return; }
    if (t.name === "to") { c.to = t.value; S.sendError = false; render(); return; }
    if (t.name === "linkInc") { c.linkInc = t.checked; }
  });
  document.addEventListener("input", (e) => {
    const t = e.target;
    if (t.name === "note") S.compose.note = t.value;
    if (t.name === "q") { S.compose.query = t.value; $("#people").innerHTML = peopleList(); }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (S.menu) { S.menu = false; render(); $('[data-act="menu"]')?.focus(); }
      else if (S.view === "compose") { S.view = "main"; render(); $('#popover [data-act="handover"]')?.focus(); }
      else if (S.open) { S.open = false; render(); $("#status-item").focus(); }
    }
    if (e.key === "Enter" && e.metaKey && S.view === "compose") { $('[data-act="send"]:not([disabled])')?.click(); }
  });

  window.rota = { scenario, get state() { return S; } };
  const q = new URLSearchParams(location.search);
  if (q.get("theme")) document.documentElement.dataset.theme = q.get("theme");
  scenario(q.get("state") || "oncall");
})();
