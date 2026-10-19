// Harbour onboarding prototype. No network; all bank responses are simulated.
// Prototype rules: a card number ending 0000 is "not found"; code 000000 is wrong;
// any other valid input succeeds. Every state can be opened directly, for review:
//   #welcome #details #details-errors #details-notfound #details-nocard
//   #code #code-wrong #code-expired #code-help #code-locked
//   #passcode #passcode-errors #biometrics #working #working-slow #working-failed #done
//   add ?help=1 to open the help sheet, ?theme=dark|light, ?scale=150|200 for larger text.
(() => {
  "use strict";
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];
  const params = new URLSearchParams(location.search);
  if (params.get("theme")) document.documentElement.dataset.theme = params.get("theme");
  if (params.get("scale")) document.documentElement.dataset.scale = params.get("scale");

  const STEPS = { details: [1, "Your details"], code: [2, "Check it's you"], passcode: [3, "Your passcode"], biometrics: [4, "How you log in"] };
  const ORDER = ["welcome", "details", "code", "passcode", "biometrics", "working", "done"];
  const NO_BACK = new Set(["welcome", "working", "done"]);
  const SAVED_KEY = "harbour-onboarding";

  const state = { screen: "welcome", detailTries: 3, codeTries: 3, useAccount: false, timers: [] };

  const announce = (msg) => { const el = $("#announce"); el.textContent = ""; setTimeout(() => { el.textContent = msg; }, 50); };
  const clearTimers = () => { state.timers.forEach(clearTimeout); state.timers = []; };
  const later = (fn, ms) => state.timers.push(setTimeout(fn, ms));
  const clock = (offsetMin = 0) => {
    const d = new Date(Date.now() + offsetMin * 60000);
    let h = d.getHours(); const m = String(d.getMinutes()).padStart(2, "0");
    const ap = h >= 12 ? "pm" : "am"; h = h % 12 || 12;
    return `${h}:${m}${ap}`;
  };

  // Keep entered (non-secret) details on this phone, so stopping costs nothing.
  const save = () => {
    try {
      const data = { screen: state.screen, card: $("#card").value, d: $("#dob-d").value, m: $("#dob-m").value, y: $("#dob-y").value };
      localStorage.setItem(SAVED_KEY, JSON.stringify(data));
    } catch (_) { /* storage unavailable: the flow still works */ }
  };
  const restore = () => {
    try {
      const data = JSON.parse(localStorage.getItem(SAVED_KEY) || "null");
      if (!data) return null;
      $("#card").value = data.card || ""; $("#dob-d").value = data.d || ""; $("#dob-m").value = data.m || ""; $("#dob-y").value = data.y || "";
      return data.screen;
    } catch (_) { return null; }
  };

  // ---------- Screen changes: one thing per screen, focus to its question ----------
  function show(name, { focus = true } = {}) {
    clearTimers();
    state.screen = name;
    $$(".screen").forEach((s) => { s.hidden = s.dataset.screen !== name; });
    const step = STEPS[name];
    $("#progress").hidden = !step;
    if (step) {
      $("#progress-text").textContent = `Step ${step[0]} of 4: ${step[1]}`;
      $("#progress-fill").style.width = `${(step[0] / 4) * 100}%`;
    }
    // Back keeps its place even when unavailable, so Help never moves.
    $("#back").hidden = NO_BACK.has(name);
    $("#wordmark").hidden = !NO_BACK.has(name);
    document.title = `${$(`[data-screen="${name}"] h1`).textContent} - Harbour`;
    if (name === "code") startCode();
    if (name === "working") startWorking();
    if (focus) $(`[data-screen="${name}"] h1`).focus();
    window.scrollTo(0, 0);
    save();
  }

  $("#back").addEventListener("click", () => {
    const i = ORDER.indexOf(state.screen);
    if (i > 0) show(ORDER[i - 1]);
  });
  $$("[data-go]").forEach((b) => b.addEventListener("click", () => show(b.dataset.go)));

  // ---------- Field errors ----------
  function setError(fieldId, errorId, msg) {
    const f = $(`#${fieldId}`), e = $(`#${errorId}`);
    f.classList.toggle("has-error", !!msg);
    e.hidden = !msg;
    e.innerHTML = msg ? `<span class="vh">Error: </span>${msg}` : "";
    $$("input", f).forEach((i) => (msg ? i.setAttribute("aria-invalid", "true") : i.removeAttribute("aria-invalid")));
  }

  // ---------- Step 1: details ----------
  const digits = (v) => v.replace(/\D/g, "");
  $("#card").addEventListener("input", (e) => {
    // Group in fours as the card does; accept spaces and dashes when pasted.
    const el = e.target, raw = digits(el.value).slice(0, 16);
    const grouped = raw.replace(/(\d{4})(?=\d)/g, "$1 ");
    if (grouped !== el.value) el.value = grouped;
  });

  $("#swap-id").addEventListener("click", () => {
    state.useAccount = !state.useAccount;
    $("#card-fields").hidden = state.useAccount;
    $("#account-fields").hidden = !state.useAccount;
    $("#swap-id").textContent = state.useAccount ? "Use my card instead" : "I don't have my card with me";
    (state.useAccount ? $("#sort") : $("#card")).focus();
  });

  function validateDetails() {
    const errs = [];
    if (state.useAccount) {
      const s = digits($("#sort").value), a = digits($("#acc").value);
      const se = !s ? "Enter your sort code" : s.length !== 6 ? `A sort code is 6 numbers. You've entered ${s.length}.` : "";
      const ae = !a ? "Enter your account number" : a.length !== 8 ? `An account number is 8 numbers. You've entered ${a.length}.` : "";
      setError("f-sort", "sort-error", se); setError("f-acc", "acc-error", ae);
      if (se) errs.push(["sort", se]); if (ae) errs.push(["acc", ae]);
    } else {
      const c = digits($("#card").value);
      const ce = !c ? "Enter the long number on your card" : c.length !== 16 ? `The card number is 16 numbers. You've entered ${c.length}.` : "";
      setError("f-card", "card-error", ce);
      if (ce) errs.push(["card", ce]);
    }
    const d = +$("#dob-d").value, m = +$("#dob-m").value, y = +$("#dob-y").value;
    let de = "";
    if (!$("#dob-d").value && !$("#dob-m").value && !$("#dob-y").value) de = "Enter your date of birth";
    else if (!d || !m || !y) de = "Your date of birth needs a day, a month and a year";
    else if (m > 12) de = "The month should be a number from 1 to 12";
    else if (String(y).length !== 4) de = "Write the year with 4 numbers, like 1951";
    else {
      const dt = new Date(y, m - 1, d);
      if (dt.getDate() !== d) de = "That date doesn't exist. Check the day and month";
      else if (y < 1900 || dt > new Date()) de = "Check the year you were born";
    }
    setError("f-dob", "dob-error", de);
    if (de) errs.push(["dob-d", de]);
    return errs;
  }

  function showSummary(errs) {
    const box = $("#details-summary");
    $("#details-summary-list").innerHTML = errs.map(([id, msg]) => `<li><a href="#${id}" data-focus="${id}">${msg}</a></li>`).join("");
    box.hidden = !errs.length;
    $$("[data-focus]", box).forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); $(`#${a.dataset.focus}`).focus(); }));
    if (errs.length) { box.focus(); box.scrollIntoView({ block: "start" }); }
  }

  $("#details-form").addEventListener("submit", (e) => {
    e.preventDefault();
    $("#details-notfound").hidden = true;
    const errs = validateDetails();
    showSummary(errs);
    if (errs.length) return;
    if (!state.useAccount && digits($("#card").value).endsWith("0000")) {
      state.detailTries -= 1;
      const p = $("#details-notfound");
      $("strong", p).textContent = `${Math.max(state.detailTries, 0)} more time${state.detailTries === 1 ? "" : "s"}`;
      p.hidden = false; p.focus(); window.scrollTo(0, 0);
      return;
    }
    show("code");
  });

  // ---------- Step 2: code (the message preview is the novelty moment) ----------
  function startCode({ sent = false } = {}) {
    const msg = $("#message"), status = $("#message-status");
    msg.classList.remove("arrived");
    status.textContent = "Sending your text…";
    later(() => {
      msg.classList.add("arrived");
      status.textContent = `Sent at ${clock()}. Check your messages.`;
    }, sent ? 0 : 1200);
  }

  $("#otp").addEventListener("input", (e) => { e.target.value = e.target.value.replace(/[^\d ]/g, ""); });

  $("#code-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const c = digits($("#otp").value);
    $("#code-resent").hidden = true;
    if (c.length !== 6) { setError("f-code", "code-error", c ? `The code is 6 numbers. You've entered ${c.length}.` : "Enter the 6 numbers from the text"); $("#otp").focus(); return; }
    if (c === "000000") { codeWrong(); return; }
    setError("f-code", "code-error", "");
    show("passcode");
  });

  function codeWrong() {
    state.codeTries -= 1;
    if (state.codeTries <= 0) return codeLocked();
    setError("f-code", "code-error", `That code doesn't match. Check you're using the newest text from Harbour. You can try ${state.codeTries} more time${state.codeTries === 1 ? "" : "s"}.`);
    $("#otp").select(); $("#otp").focus();
  }
  function codeLocked() {
    $("#locked-until").textContent = clock(30);
    $("#code-locked").hidden = false;
    $("#code-form").hidden = true; $("#preview").hidden = true;
    $(".disclosure").hidden = true;
    $("[data-screen=code] h1").textContent = "Setup is paused";
    $("[data-screen=code] h1 + p").hidden = true;
    $("#code-locked").focus();
  }
  function codeExpired() {
    setError("f-code", "code-error", "This code has run out. Codes last 10 minutes. Choose “I haven't had a text” below to get a new one.");
  }

  $("#nocode-toggle").addEventListener("click", () => {
    const b = $("#nocode-toggle"), open = b.getAttribute("aria-expanded") !== "true";
    b.setAttribute("aria-expanded", String(open)); $("#nocode").hidden = !open;
  });
  $("#resend").addEventListener("click", () => {
    const r = $("#code-resent");
    r.textContent = `We sent a new code at ${clock()}. Use the newest text; older codes won't work now.`;
    r.hidden = false; setError("f-code", "code-error", "");
    $("#otp").value = ""; startCode({ sent: true }); $("#otp").focus();
  });
  $("#callme").addEventListener("click", () => {
    const r = $("#code-resent");
    r.textContent = "We'll phone your mobile ending 482 within a minute. A recorded voice will read the code twice. It won't ask you anything.";
    r.hidden = false; $("#otp").focus();
  });

  // ---------- Step 3: passcode ----------
  $("#pass-show").addEventListener("click", (e) => {
    const on = e.target.getAttribute("aria-pressed") !== "true";
    e.target.setAttribute("aria-pressed", String(on));
    e.target.textContent = on ? "Hide numbers" : "Show numbers";
    ["#pass", "#pass2"].forEach((s) => { $(s).type = on ? "text" : "password"; });
  });
  ["#pass", "#pass2"].forEach((s) => $(s).addEventListener("input", (e) => { e.target.value = digits(e.target.value).slice(0, 6); }));

  const easy = (p) => /^(\d)\1+$/.test(p) || "0123456789".includes(p) || "9876543210".includes(p);
  function birthdayLike(p) {
    const d = $("#dob-d").value.padStart(2, "0"), m = $("#dob-m").value.padStart(2, "0"), y = $("#dob-y").value;
    return !!(d && m && y) && (p === d + m + y.slice(2) || p === m + d + y.slice(2));
  }
  $("#pass-form").addEventListener("submit", (e) => {
    e.preventDefault();
    const p = $("#pass").value, q = $("#pass2").value;
    let pe = "", qe = "";
    if (p.length !== 6) pe = p ? `Your passcode needs 6 numbers. You've typed ${p.length}.` : "Choose 6 numbers for your passcode";
    else if (easy(p)) pe = "Those numbers are easy to guess because they repeat or run in order. Choose a different 6.";
    else if (birthdayLike(p)) pe = "That's your date of birth, which other people may know. Choose a different 6.";
    else if (q !== p) qe = "The two passcodes don't match. Type the same 6 numbers in both boxes.";
    setError("f-pass", "pass-error", pe); setError("f-pass2", "pass2-error", qe);
    if (pe) { $("#pass").focus(); return; }
    if (qe) { $("#pass2").value = ""; $("#pass2").focus(); return; }
    show("biometrics");
  });

  // ---------- Step 4: biometrics ----------
  $$("[data-bio]").forEach((b) => b.addEventListener("click", () => show("working")));

  // ---------- Working: named steps that fill in place; honest when slow or failed ----------
  function setTask(i, cls) {
    const li = $(`[data-task="${i}"]`);
    li.className = cls || "";
    $(".task-state", li).textContent = cls === "is-done" ? ", done" : cls === "is-active" ? ", in progress" : ", waiting";
  }
  function startWorking(mode = "normal") {
    $("#work-slow").hidden = true; $("#work-failed").hidden = true;
    $("#tasks").hidden = false;
    $("#work-lead").hidden = false;
    [0, 1, 2].forEach((i) => setTask(i, ""));
    setTask(0, "is-active");
    if (mode === "failed") {
      setTask(0, "is-done"); setTask(1, "is-active");
      return failWorking();
    }
    later(() => { setTask(0, "is-done"); setTask(1, "is-active"); }, mode === "slow" ? 600 : 1400);
    if (mode === "slow") {
      later(() => { $("#work-slow").hidden = false; announce("This is taking longer than usual. You don't need to do anything."); }, 800);
      return;
    }
    later(() => { setTask(1, "is-done"); setTask(2, "is-active"); }, 2800);
    later(() => { setTask(2, "is-done"); announce("Setup finished."); }, 4000);
    later(() => show("done"), 4800);
  }
  function failWorking() {
    $(".is-active .task-state")?.replaceChildren(", stopped");
    $$(".tasks li.is-active").forEach((li) => { li.className = ""; });
    $("#work-lead").hidden = true;
    $("#work-failed").hidden = false; $("#work-failed").focus();
  }
  $("#retry").addEventListener("click", () => { $("[data-screen=working] h1").focus(); startWorking(); });

  $("#to-account").addEventListener("click", () => { try { localStorage.removeItem(SAVED_KEY); } catch (_) {} announce("This prototype ends here."); });

  // ---------- Help: same place on every screen, about this step first, then a person ----------
  const HELP = {
    welcome: "<p>This sets up the app on this phone so you can bank from home. Your account, card and branch stay exactly the same.</p><p>You can stop at any point and come back. Nothing changes on your account until the last step.</p>",
    details: "<p><strong>The long number</strong> is the 16 numbers across the front of your card. Leave out the spaces if it's easier; we'll add them.</p><p>No card with you? Choose “I don't have my card with me” and use your sort code and account number. They're on your statements and chequebook.</p>",
    code: "<p>We text a code to make sure it's really you holding this phone. It's 6 numbers and lasts 10 minutes.</p><p><strong>Harbour will never phone you and ask for this code.</strong> If anyone does, hang up. Then call us on the number on the back of your card, from a different phone if you can.</p>",
    passcode: "<p>Your passcode opens the app, like a PIN opens the cash machine. Choose 6 numbers that you'll remember and other people won't guess.</p><p>It's fine to write a reminder, as long as it doesn't look like a passcode and isn't kept with your phone.</p>",
    biometrics: "<p>Your phone checks your fingerprint or face itself. Harbour never receives a copy.</p><p>If family members have their fingerprints saved on this phone, they could open the app too. Choose the passcode if you'd rather they couldn't.</p>",
    working: "<p>We're connecting this phone to your account. You don't need to do anything. If it stops, nothing changes on your account and you can try again.</p>",
    done: "<p>You can do the same things in your branch as before. The app is an extra way to bank, not a replacement.</p>",
  };
  let helpReturn = null;
  function openHelp() {
    helpReturn = document.activeElement;
    $("#help-context").innerHTML = HELP[state.screen] || HELP.welcome;
    $("#help").hidden = false; $("#scrim").hidden = false;
    $(".app").setAttribute("inert", "");
    $("#help-title").focus();
  }
  function closeHelp() {
    $("#help").hidden = true; $("#scrim").hidden = true;
    $(".app").removeAttribute("inert");
    (helpReturn && document.contains(helpReturn) ? helpReturn : $("#help-open")).focus();
  }
  $("#help-open").addEventListener("click", openHelp);
  $("#help-close").addEventListener("click", closeHelp);
  $("#scrim").addEventListener("click", closeHelp);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !$("#help").hidden) closeHelp();
    if (e.key === "Tab" && !$("#help").hidden) {
      const f = $$("#help a, #help button");
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
  });

  // ---------- Entry: a review state from the hash, else resume where the user stopped ----------
  function fillDetails() { $("#card").value = "4921 3388 0154 7712"; $("#dob-d").value = "27"; $("#dob-m").value = "3"; $("#dob-y").value = "1951"; }
  const routes = {
    "details-errors": () => { show("details", { focus: false }); $("#card").value = "4921 3388 0154"; $("#dob-d").value = "31"; $("#dob-m").value = "2"; $("#dob-y").value = "1951"; showSummary(validateDetails()); },
    "details-notfound": () => { show("details", { focus: false }); fillDetails(); $("#card").value = "4921 3388 0154 0000"; $("#details-form").requestSubmit(); },
    "details-nocard": () => { show("details", { focus: false }); $("#swap-id").click(); },
    "code-wrong": () => { show("code", { focus: false }); $("#otp").value = "000000"; $("#code-form").requestSubmit(); },
    "code-expired": () => { show("code", { focus: false }); $("#otp").value = "482913"; codeExpired(); },
    "code-help": () => { show("code", { focus: false }); $("#nocode-toggle").click(); $("#resend").click(); },
    "code-locked": () => { show("code", { focus: false }); state.codeTries = 1; codeWrong(); },
    "passcode-errors": () => { show("passcode", { focus: false }); $("#pass").value = "123456"; $("#pass2").value = "123456"; $("#pass-form").requestSubmit(); },
    "working-slow": () => { show("working", { focus: false }); clearTimers(); startWorking("slow"); },
    "working-failed": () => { show("working", { focus: false }); clearTimers(); startWorking("failed"); },
  };
  const hash = location.hash.slice(1);
  if (routes[hash]) routes[hash]();
  else if (ORDER.includes(hash)) { if (hash !== "welcome" && hash !== "details") fillDetails(); show(hash, { focus: false }); }
  else {
    const resumed = restore();
    show(resumed && ["details", "code"].includes(resumed) ? resumed : "welcome", { focus: false });
  }
  if (params.get("help") === "1") openHelp();
})();
