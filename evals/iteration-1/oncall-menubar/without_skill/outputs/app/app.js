/* Handover prototype: renders the menu-bar item and its panel for each state. */
(function () {
  const D = window.DATA;
  const $ = (s, el = document) => el.querySelector(s);
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  /* ---------- Glyphs (drawn on a 16-unit grid; template images in the native app) ---------- */
  const G = {
    pagerOff: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="1.9" y="3.4" width="12.2" height="9.2" rx="2.4"/><rect x="4.4" y="5.9" width="7.2" height="2.6" rx="0.8"/><path d="M4.6 10.6h2.2"/></svg>',
    pagerOn: '<svg viewBox="0 0 16 16"><path fill="currentColor" fill-rule="evenodd" d="M4.3 2.8h7.4a2.9 2.9 0 0 1 2.9 2.9v4.6a2.9 2.9 0 0 1-2.9 2.9H4.3a2.9 2.9 0 0 1-2.9-2.9V5.7a2.9 2.9 0 0 1 2.9-2.9Zm.9 2.8a.8.8 0 0 0-.8.8v1.6c0 .44.36.8.8.8h5.6a.8.8 0 0 0 .8-.8V6.4a.8.8 0 0 0-.8-.8H5.2Zm-.6 4.4a.6.6 0 0 0 0 1.2h2.2a.6.6 0 0 0 0-1.2H4.6Z"/></svg>',
    pagerStale: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" opacity="0.55"><rect x="1.9" y="3.4" width="12.2" height="9.2" rx="2.4"/><path d="M2.5 13.8 13.5 2.2"/></svg>',
    wifi: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M2 6.2a8.6 8.6 0 0 1 12 0M4.2 8.6a5.4 5.4 0 0 1 7.6 0M6.4 11a2.3 2.3 0 0 1 3.2 0"/></svg>',
    battery: '<svg viewBox="0 0 22 16" style="width:22px"><rect x="1" y="4" width="17.5" height="8.5" rx="2.4" fill="none" stroke="currentColor" opacity="0.5"/><rect x="2.6" y="5.6" width="11" height="5.3" rx="1.2" fill="currentColor"/><path d="M20 6.8v3" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" opacity="0.5"/></svg>',
    toggles: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><rect x="1.8" y="2.8" width="12.4" height="4.4" rx="2.2"/><rect x="1.8" y="8.8" width="12.4" height="4.4" rx="2.2"/><circle cx="11.9" cy="5" r="1.2" fill="currentColor"/><circle cx="4.1" cy="11" r="1.2" fill="currentColor"/></svg>',
    gear: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3"><circle cx="8" cy="8" r="2.2"/><path d="M8 1.6v1.8M8 12.6v1.8M1.6 8h1.8M12.6 8h1.8M3.5 3.5l1.3 1.3M11.2 11.2l1.3 1.3M3.5 12.5l1.3-1.3M11.2 4.8l1.3-1.3"/></svg>',
    back: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M10 3 5 8l5 5"/></svg>',
    search: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"><circle cx="7" cy="7" r="4.5"/><path d="m10.4 10.4 3.4 3.4"/></svg>',
    chevrons: '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"><path d="m3.5 4.5 2.5-2.5 2.5 2.5M3.5 7.5 6 10l2.5-2.5"/></svg>',
    tick: '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="m3.5 8.5 3 3 6-7"/></svg>',
  };

  /* ---------- State ---------- */
  const PRESETS = [
    { id: "off", label: "Off call", s: { me: "off" } },
    { id: "on", label: "On call now", s: { me: "on" } },
    { id: "choose", label: "Hand over: choose who", s: { me: "on", view: "handover" } },
    { id: "pending", label: "Hand over: waiting", s: { me: "on", handover: "pending" } },
    { id: "accepted", label: "Hand over: accepted", s: { me: "on", handover: "accepted" } },
    { id: "declined", label: "Hand over: declined", s: { me: "on", handover: "declined" } },
    { id: "incoming", label: "Someone asks you", s: { me: "off", incoming: "ask" } },
    { id: "offline", label: "Can't reach PagerDuty", s: { me: "on", offline: true } },
    { id: "schedule", label: "Schedule tab", s: { me: "on", tab: "schedule" } },
  ];
  const BASE = { me: "on", view: "main", tab: "now", handover: null, incoming: null, offline: false, open: true,
                 range: "part", pick: 0, query: "", incident: true, more: false };
  let S = { ...BASE };
  let lastView = "main";

  function go(patch) { S = { ...S, ...patch }; render(); }
  function preset(id) {
    const p = PRESETS.find((x) => x.id === id);
    S = { ...BASE, ...p.s };
    try { history.replaceState(null, "", "#" + id); } catch (e) {}
    render();
  }

  /* ---------- Pieces ---------- */
  const pct = (h) => (h / D.myShift.hours) * 100;

  // The handover as currently set up: who (S.pick) and which part (S.range).
  function H() {
    const c = D.candidates[S.pick == null ? 0 : S.pick];
    const rest = S.range === "rest";
    return {
      to: c.name, toFirst: c.name.split(" ")[0], rest,
      from: rest ? "now" : D.handover.from, fromAt: rest ? D.myShift.nowAt : D.handover.fromAt,
      until: D.handover.until, askedAgo: D.handover.askedAgo,
      declineNote: S.pick === 0 || S.pick == null ? D.handover.declineNote : "Can't this time, sorry.",
    };
  }

  function bar(kind) {
    const sh = D.myShift, ho = H();
    let range = "";
    if (kind) {
      const from = kind === "select" && S.range === "rest" ? sh.nowAt : ho.fromAt;
      const label = kind === "given" ? ho.toFirst : kind === "pending" ? ho.toFirst + "?" : "";
      range = `<div class="bar-range ${kind}" style="left:${pct(from)}%;width:${pct(sh.hours - from)}%">${esc(label)}</div>`;
    }
    return `<div class="bar" aria-hidden="true">
      <div class="bar-now-label"><span style="left:${pct(sh.nowAt)}%">now · 18:47</span></div>
      <div class="bar-track">
        <div class="bar-done" style="width:${pct(sh.nowAt)}%"></div>
        ${range}
        <div class="bar-now" style="left:${pct(sh.nowAt)}%"></div>
      </div>
      <div class="bar-labels"><span>${sh.startShort}</span><span class="end">${sh.endShort}</span></div>
    </div>`;
  }

  function youPanel() {
    const sh = D.myShift, ho = H(), nx = D.myNext[0], inc = D.incoming;
    if (S.incoming === "ask") {
      return `<section class="you" aria-labelledby="you-h">
        <h2 id="you-h">${esc(inc.from)} asks you to take a shift</h2>
        <p>${esc(inc.rotation)} · ${esc(inc.when)} · ${inc.length}</p>
        <blockquote>“${esc(inc.note)}”</blockquote>
        <p>${esc(inc.fit)}</p>
        <div class="actions"><span class="note"></span>
          <button class="btn" data-act="decline-incoming">Decline…</button>
          <button class="btn default" data-act="accept-incoming">Accept</button></div>
      </section>`;
    }
    if (S.incoming === "accepted") {
      return `<section class="you" aria-labelledby="you-h">
        <h2 id="you-h">You're taking ${esc(inc.rotation)} on Tuesday</h2>
        <p>${esc(inc.when)} · ${inc.length}. ${esc(inc.first)} has been told and the override is in PagerDuty.</p>
      </section>`;
    }
    if (S.me === "off") {
      return `<section class="you" aria-labelledby="you-h">
        <h2 id="you-h">You're off call</h2>
        <p>Next: ${esc(nx.rotation)}, ${esc(nx.when)} · ${nx.inDays}</p>
        <div class="actions"><button class="btn" data-act="handover">Hand over…</button></div>
      </section>`;
    }
    const head = `You're on call for ${sh.rotation}`;
    if (S.handover === "pending") {
      return `<section class="you" aria-labelledby="you-h">
        <h2 id="you-h">${head}</h2>
        <p>Until ${sh.end} · ${sh.left} left</p>
        ${bar("pending")}
        <p class="status-line"><span class="pending-dot" aria-hidden="true"></span>Waiting for ${esc(ho.to)} · asked ${ho.askedAgo}</p>
        <p>${ho.rest ? "The rest of your shift" : ho.from + " → " + ho.until}. You're on call until ${esc(ho.toFirst)} accepts.</p>
        <div class="actions"><button class="btn" data-act="withdraw">Withdraw request</button><span class="note"></span></div>
      </section>`;
    }
    if (S.handover === "accepted") {
      return `<section class="you" aria-labelledby="you-h">
        <h2 id="you-h">${ho.rest ? "You're off call" : "You're on call until " + ho.from}</h2>
        <p>${ho.rest ? esc(ho.to) + " has " + sh.rotation + " until " + ho.until + "." : "1 h 13 m left. Then " + esc(ho.to) + " has it until " + ho.until + "."}</p>
        ${bar("given")}
        <p class="status-line">${esc(ho.toFirst)} accepted just now. The override is in PagerDuty.</p>
      </section>`;
    }
    if (S.handover === "declined") {
      return `<section class="you" aria-labelledby="you-h">
        <h2 id="you-h">${head}</h2>
        <p>Until ${sh.end} · ${sh.left} left</p>
        ${bar(null)}
        <p class="warn-text status-line">${esc(ho.to)} declined. You're still on call.</p>
        <blockquote>“${esc(ho.declineNote)}”</blockquote>
        <div class="actions"><button class="btn default" data-act="ask-again">Ask someone else…</button></div>
      </section>`;
    }
    const disabled = S.offline ? " disabled" : "";
    return `<section class="you" aria-labelledby="you-h">
      <h2 id="you-h">${head}</h2>
      <p>Until ${sh.end} · ${sh.left} left</p>
      ${bar(null)}
      <div class="actions"><button class="btn" data-act="handover"${disabled}>Hand over…</button>
      ${S.offline ? '<span class="note">Paused while PagerDuty can’t be reached.</span>' : ""}</div>
    </section>`;
  }

  function nowList() {
    const rows = D.nowOn.map((r, i) => (S.me === "off" && i === 0 ? { ...D.nowOnWhenOff, name: "Inês Carvalho", initials: "IC" } : r));
    return `<section class="section" aria-labelledby="now-h">
      <h3 class="label" id="now-h"><span>ON CALL NOW</span></h3>
      <ul class="rows">${rows.map((r) => `
        <li class="row">
          <span class="avatar${r.you ? " me" : ""}" aria-hidden="true">${r.initials}</span>
          <div class="main"><div class="name">${esc(r.name)}</div><div class="sub">${esc(r.rotation)}${r.tz ? " · " + esc(r.tz) : ""}${r.you && S.handover === "accepted" ? " · then " + esc(H().to) : ""}</div></div>
          <span class="right${r.you ? "" : " hide-on-hover"}">until ${r.you && S.handover === "accepted" ? (H().rest ? "now" : H().from) : r.until}</span>
          ${r.you ? "" : `<button class="row-action" aria-label="Message ${esc(r.name)} on Slack">Message</button>`}
        </li>`).join("")}
      </ul>
    </section>`;
  }

  function nextList() {
    const list = S.me === "off" ? D.myNext.slice(1, 3) : D.myNext.slice(0, 2);
    return `<section class="section" aria-labelledby="next-h">
      <h3 class="label" id="next-h"><span>YOUR NEXT SHIFTS</span></h3>
      <ul class="rows">${list.map((r) => `
        <li class="row">
          <div class="main"><div class="name">${esc(r.rotation)}</div><div class="sub">${esc(r.when)} · ${r.length}</div></div>
          <span class="right hide-on-hover">${r.inDays}</span>
          <button class="row-action" data-act="handover"${S.offline ? " disabled" : ""}>Hand over…</button>
        </li>`).join("")}
      </ul>
    </section>`;
  }

  function scheduleTab() {
    return `<div class="section" style="padding-top:2px">
        <button class="picker" aria-haspopup="menu">Core platform · primary ${G.chevrons}</button>
      </div>
      ${D.schedule.map((d) => `
        <section class="day">
          <h3>${esc(d.day.toUpperCase())}</h3>
          <ul class="rows">${d.rows.map((r) => `
            <li class="row">
              <span class="avatar${r.you ? " me" : ""}" aria-hidden="true">${r.initials}</span>
              <div class="main"><div class="name">${esc(r.name)}</div><div class="sub">${esc(r.sub)}</div></div>
              ${r.you ? `<span class="right hide-on-hover">${r.right}</span><button class="row-action" data-act="handover">Hand over…</button>` : ""}
            </li>`).join("")}
          </ul>
          ${d.gap ? `<p class="gap"><strong>Gap.</strong> ${esc(d.gap)}</p>` : ""}
        </section>`).join("")}
      <div class="section"><button class="link" style="font:var(--fs-meta)">Open the full schedule in PagerDuty ↗</button></div>`;
  }

  function footer() {
    if (S.offline) {
      return `<footer class="pop-foot"><span>Last synced 18:31</span><span class="spacer"></span><span>⌃⌥O</span></footer>`;
    }
    return `<footer class="pop-foot"><span class="dot" aria-hidden="true"></span><span>Synced with PagerDuty 1 min ago</span><span class="spacer"></span><span aria-label="Shortcut: Control Option O">⌃⌥O</span></footer>`;
  }

  function mainView() {
    const notice = S.offline
      ? `<div class="notice" role="alert"><p>Can't reach PagerDuty since 18:31. This is the schedule as of then, and handovers are paused until it's back.</p><button class="btn" data-act="retry">Try again</button></div>`
      : "";
    const body = S.tab === "schedule" ? scheduleTab() : youPanel() + nowList() + nextList();
    return `<div class="view${lastView === "handover" ? "" : ""}">
      <header class="pop-head">
        <div class="seg" role="tablist" aria-label="View">
          <button role="tab" aria-selected="${S.tab === "now"}" data-tab="now">Now</button>
          <button role="tab" aria-selected="${S.tab === "schedule"}" data-tab="schedule">Schedule</button>
        </div>
        <button class="icon-btn" aria-label="Settings" aria-haspopup="menu">${G.gear}</button>
      </header>
      <div class="pop-body" role="tabpanel">${body}</div>
      ${notice}
      ${footer()}
    </div>`;
  }

  function handoverView() {
    const sh = D.myShift;
    const q = S.query.trim().toLowerCase();
    const all = D.candidates.map((c, i) => ({ ...c, i }));
    const free = all.filter((c) => !c.warn && !c.away);
    const rest = all.filter((c) => c.warn || c.away);
    const list = q ? all.filter((c) => c.name.toLowerCase().includes(q)) : S.more ? all : free;
    const moreLink = !q && !S.more
      ? `<li class="people-more"><button class="link" data-act="more">${rest.length} more: would double up, be up overnight, or away</button></li>` : "";
    const picked = S.pick != null ? D.candidates[S.pick] : null;
    const first = picked ? picked.name.split(" ")[0] : null;
    const len = S.range === "rest" ? sh.left : D.handover.length;
    return `<div class="view from-right">
      <header class="sheet-head">
        <button class="icon-btn" data-act="back" aria-label="Back">${G.back}</button>
        <h1>Hand over a shift</h1>
      </header>
      <div class="pop-body">
        <div class="sheet">
          <p class="shift-name">${sh.rotation}</p>
          <p class="shift-time">${sh.start} → ${sh.end}</p>
          ${bar("select")}

          <fieldset class="fieldset">
            <legend>WHICH PART</legend>
            <label class="radio"><input type="radio" name="range" value="rest" ${S.range === "rest" ? "checked" : ""}><span class="ctl"></span>
              <span>The rest of it<span class="muted">Now → Mon 09:00 · ${sh.left}</span></span></label>
            <label class="radio"><input type="radio" name="range" value="part" ${S.range === "part" ? "checked" : ""}><span class="ctl"></span>
              <span>Part of it<span class="muted">${S.range === "part" ? "13 h" : "Choose when it starts and ends"}</span></span></label>
            <div class="times" ${S.range === "part" ? "" : 'style="opacity:.45"'}>
              <span class="stepper">Sun 18 Oct, 20:00</span> → <span class="stepper">Mon 20 Oct, 09:00</span>
            </div>
          </fieldset>

          <fieldset class="fieldset">
            <legend style="display:flex;justify-content:space-between;width:100%"><span>TO</span><span style="font:var(--fs-small);letter-spacing:0">${D.rotationSize} people on this rotation</span></legend>
            <label class="field">${G.search}<span class="vh">Search people</span><input id="q" type="search" placeholder="Search all ${D.teamSize} on the team" value="${esc(S.query)}" autocomplete="off"></label>
            <ul class="people" role="radiogroup" aria-label="Who takes it">${list.map((c) => `
              <li><button class="person" role="radio" data-pick="${c.i}" aria-checked="${S.pick === c.i}" ${c.away ? 'aria-disabled="true"' : ""}>
                <span class="avatar" aria-hidden="true">${c.initials}</span>
                <span class="main"><span class="name">${esc(c.name)} <span class="tz">${esc(c.tz)}</span></span>
                  <span class="why${c.warn ? " warn" : ""}" style="display:block">${esc(c.why)}</span></span>
                <span class="tick">${S.pick === c.i ? G.tick : ""}</span>
              </button></li>`).join("") || `<li class="people-more">Nobody on the team matches “${esc(S.query)}”.</li>`}${list.length ? moreLink : ""}
            </ul>
          </fieldset>

          <fieldset class="fieldset">
            <legend>HANDOVER NOTE</legend>
            <label class="check"><input type="checkbox" data-act="incident" ${S.incident ? "checked" : ""}><span class="ctl"></span>
              <span>Include ${D.openIncident.id} · ${esc(D.openIncident.title)}<span class="muted">${esc(D.openIncident.detail)}. Assigned to you, still open.</span></span></label>
            <textarea aria-label="Anything else they should know" placeholder="Anything else they should know?">Watching the error budget on checkout-api after tonight's rollback. Deploys are frozen until Monday.</textarea>
          </fieldset>
        </div>
      </div>
        <div class="sheet-foot">
          <p>${picked ? `${esc(first)} gets a Slack message and a notification. You stay on call until ${esc(first)} accepts; if not, nothing changes.` : "Choose who takes it."}</p>
          <div class="buttons">
            <button class="btn" data-act="back">Cancel</button>
            <button class="btn default" data-act="send" ${picked && !picked.away ? "" : "disabled"}>${picked ? `Ask ${esc(first)} · ${len}` : "Ask"}</button>
          </div>
        </div>
    </div>`;
  }

  /* ---------- Render ---------- */
  function menubar() {
    const onNow = S.me === "on" && !(S.handover === "accepted" && S.range === "rest");
    const glyph = S.offline ? G.pagerStale : onNow ? G.pagerOn : G.pagerOff;
    const text = onNow && !S.offline ? (S.handover === "accepted" ? "1h" : "14h") : "";
    const needsYou = S.incoming === "ask" || S.handover === "declined";
    const label = onNow ? `On call, ${text === "1h" ? "1 hour 13 minutes" : "14 hours 13 minutes"} left` : "Off call";
    $("#mb-app").innerHTML = `${glyph}${text ? `<span>${text}</span>` : ""}${needsYou ? '<span class="mb-dot"></span>' : ""}`;
    $("#mb-app").setAttribute("aria-label", "Handover: " + label + (needsYou ? ", needs you" : ""));
    $("#mb-app").setAttribute("aria-expanded", String(S.open));
    $("#mb-wifi").innerHTML = G.wifi;
    $("#mb-batt").innerHTML = G.battery;
    $("#mb-cc").innerHTML = G.toggles;
    $("#mb-clock").textContent = D.now.clock;
  }

  function render() {
    menubar();
    const pop = $("#pop");
    pop.hidden = !S.open;
    pop.innerHTML = S.view === "handover" ? handoverView() : mainView();
    lastView = S.view;
    // prototype controls
    const cur = currentPresetId();
    document.querySelectorAll("[data-preset]").forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.preset === cur)));
    $("#sim").hidden = S.handover !== "pending";
  }

  function currentPresetId() {
    for (const p of PRESETS) {
      const t = { ...BASE, ...p.s };
      if (["me", "view", "tab", "handover", "incoming", "offline"].every((k) => t[k] === S[k])) return p.id;
    }
    return null;
  }

  /* ---------- Events ---------- */
  document.addEventListener("click", (e) => {
    const t = e.target.closest("button, [data-act]");
    if (!t) return;
    if (t.id === "mb-app") return go({ open: !S.open });
    if (t.dataset.preset) return preset(t.dataset.preset);
    if (t.dataset.theme) {
      document.documentElement.dataset.theme = t.dataset.theme;
      document.querySelectorAll("[data-theme]").forEach((b) => b.setAttribute("aria-selected", String(b === t)));
      return;
    }
    if (t.dataset.tab) return go({ tab: t.dataset.tab });
    if (t.dataset.pick != null) {
      const c = D.candidates[+t.dataset.pick];
      if (c.away) return;
      return go({ pick: +t.dataset.pick });
    }
    switch (t.dataset.act) {
      case "handover": return go({ view: "handover", handover: null });
      case "back": return go({ view: "main" });
      case "send": return go({ view: "main", tab: "now", handover: "pending", me: "on" });
      case "withdraw": return go({ handover: null });
      case "ask-again": return go({ view: "handover", handover: null, pick: null });
      case "retry": return go({ offline: false });
      case "more": return go({ more: true });
      case "accept-incoming": return go({ incoming: "accepted" });
      case "decline-incoming": return go({ incoming: null });
      case "sim-accept": return go({ handover: "accepted" });
      case "sim-decline": return go({ handover: "declined" });
    }
  });
  document.addEventListener("change", (e) => {
    if (e.target.name === "range") go({ range: e.target.value });
    if (e.target.dataset.act === "incident") S.incident = e.target.checked;
  });
  document.addEventListener("input", (e) => {
    if (e.target.id === "q") {
      const pos = e.target.selectionStart;
      go({ query: e.target.value });
      const q = $("#q"); q.focus(); q.setSelectionRange(pos, pos);
    }
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      if (S.view === "handover") go({ view: "main" });
      else go({ open: false });
    }
  });

  /* ---------- Prototype controls ---------- */
  $("#presets").innerHTML = PRESETS.map((p, i) => `<li><button data-preset="${p.id}">${i + 1}. ${p.label}</button></li>`).join("");
  const params = new URLSearchParams(location.search);
  if (params.get("theme")) {
    document.documentElement.dataset.theme = params.get("theme");
    document.querySelectorAll("[data-theme]").forEach((b) => b.setAttribute("aria-selected", String(b.dataset.theme === params.get("theme"))));
  }
  window.addEventListener("hashchange", () => {
    const id = location.hash.slice(1);
    if (PRESETS.some((p) => p.id === id) && id !== currentPresetId()) preset(id);
  });
  const start = location.hash.slice(1);
  preset(PRESETS.some((p) => p.id === start) ? start : "on");
})();
