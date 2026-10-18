/* Larch onboarding prototype.
   One question per screen. Every screen is reachable by URL hash so states
   can be reviewed directly (index.html#checking-slow, #code-wrong ...). */

(function () {
  "use strict";

  var BANK = "Larch";
  var PHONE = "0808 157 0192";          // Ofcom drama range: not a real number
  var PHONE_TEL = "tel:+448081570192";
  var HOURS = "Monday to Saturday, 8am to 8pm";
  var MOBILE_END = "0471";
  var STEPS = ["Find your account", "Check it's you", "Make a passcode", "Stay safe"];

  var state = {
    day: "", month: "", year: "", sort: "", acct: "",
    code: "", passcode: "",
    errors: null,       // { field: message } for the current screen
    tries: 3,
    checkTimer: null,
    tick: 0
  };

  var $screen = document.getElementById("screen");
  var $back = document.getElementById("back");
  var $backSpacer = document.getElementById("back-spacer");
  var $help = document.getElementById("help");
  var $helpSheet = document.getElementById("help-sheet");
  var $helpBody = document.getElementById("help-body");
  var $timeout = document.getElementById("timeout-sheet");
  var $announce = document.getElementById("announce");

  /* ---------- small helpers ---------- */

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }
  function digits(s) { return String(s || "").replace(/\D/g, ""); }
  function announce(msg) { $announce.textContent = ""; setTimeout(function () { $announce.textContent = msg; }, 50); }
  function go(route) { if (location.hash.slice(1) === route) render(); else location.hash = route; }

  var ICON = {
    tick: '<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8.5 6.5 12 13 4.5" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    bigTick: '<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M7 16.5 13.5 23 25.5 9.5" fill="none" stroke="currentColor" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    card: '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="3" y="7" width="26" height="18" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 12.5h26" stroke="currentColor" stroke-width="3"/><path d="M7 20h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    phone: '<svg viewBox="0 0 32 32" aria-hidden="true"><rect x="9" y="3" width="14" height="26" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M14 24.5h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    clock: '<svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="12" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 9v7.5l5 3" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    mark: '<svg viewBox="0 0 44 44" aria-hidden="true"><rect class="mark-tile" width="44" height="44" rx="10"/><path class="mark-line" d="M22 9c-5 6-8 11-8 16a8 8 0 0 0 16 0c0-5-3-10-8-16Z" fill="none" stroke-width="2.6" stroke-linejoin="round"/><path class="mark-line" d="M22 18v18" stroke-width="2.6" stroke-linecap="round"/></svg>'
  };

  function progress(n) {
    var bars = STEPS.map(function (_, i) { return '<span class="' + (i < n ? "is-done" : "") + '"></span>'; }).join("");
    return '<p class="step-label">Step ' + n + " of " + STEPS.length + ": " + STEPS[n - 1] + "</p>" +
      '<div class="progress" aria-hidden="true">' + bars + "</div>";
  }

  function errorSummary(errors, order) {
    if (!errors) return "";
    var keys = order.filter(function (k) { return errors[k]; });
    if (!keys.length) return "";
    var items = keys.map(function (k) {
      return '<li><a href="#' + k + '" data-focus="' + k + '">' + esc(errors[k]) + "</a></li>";
    }).join("");
    return '<div class="error-summary" role="alert" tabindex="-1" id="error-summary">' +
      "<h2>Please check " + (keys.length > 1 ? "these" : "this") + "</h2><ul>" + items + "</ul></div>";
  }

  function fieldErr(k) {
    return state.errors && state.errors[k] ? '<span class="field-error" id="' + k + '-error">' + esc(state.errors[k]) + "</span>" : "";
  }
  function invalid(k) { return state.errors && state.errors[k] ? ' is-invalid" aria-invalid="true' : ""; }
  function describedBy(k, hint) {
    var ids = [];
    if (hint) ids.push(k + "-hint");
    if (state.errors && state.errors[k]) ids.push(k + "-error");
    return ids.length ? ' aria-describedby="' + ids.join(" ") + '"' : "";
  }
  function hasErr(keys) {
    return state.errors && keys.some(function (k) { return state.errors[k]; }) ? " has-error" : "";
  }

  function callBox(lead) {
    return '<div class="call"><span>' + (lead || "Or talk to a person") + "</span>" +
      '<a class="num" href="' + PHONE_TEL + '">' + PHONE + "</a>" +
      '<span class="small">' + HOURS + ". Free from mobiles and landlines.</span></div>";
  }

  /* ---------- screens ---------- */

  var screens = {};

  screens.welcome = {
    back: false,
    html: function () {
      return '<div class="brand">' + ICON.mark + "<span>" + BANK + "</span></div>" +
        "<h1 tabindex=\"-1\">Your bank account, on your phone</h1>" +
        '<p class="lede">Check your balance, see what you have spent and pay people, at any time of day.</p>' +
        "<p>Your branch, your card and telephone banking stay exactly as they are. This adds to them; it does not replace them.</p>" +
        '<div class="actions">' +
        '<button class="btn" data-go="prepare">I already bank with ' + BANK + "</button>" +
        '<button class="btn secondary" data-go="new">I am new to ' + BANK + "</button>" +
        "</div>";
    }
  };

  screens["new"] = {
    html: function () {
      return "<h1 tabindex=\"-1\">Opening a new account</h1>" +
        "<p>This prototype covers people who already have a " + BANK + " account and want to use the app.</p>" +
        "<p>To open a new account, visit any branch or call us.</p>" + callBox("Call us") +
        '<div class="actions"><button class="btn secondary" data-go="welcome">Go back to the start</button></div>';
    }
  };

  screens.prepare = {
    html: function () {
      return "<h1 tabindex=\"-1\">Before you start</h1>" +
        '<p class="lede">Setting up takes about 10 minutes. You will need:</p>' +
        '<ul class="plain needs">' +
        "<li>" + ICON.card + "<span><b>Your sort code and account number</b>They are on your bank card, your statement, your chequebook or your passbook.</span></li>" +
        "<li>" + ICON.phone + "<span><b>Your mobile phone</b>We will send a text to the number we have for you, ending " + MOBILE_END + ".</span></li>" +
        "<li>" + ICON.clock + "<span><b>No rush</b>You can stop at any point. If you do, you will start again from this screen.</span></li>" +
        "</ul>" +
        '<p class="small">Would you rather do this with someone? Staff in any branch can set it up with you. Bring your phone and your card.</p>' +
        '<div class="actions"><button class="btn" data-go="details">Start</button></div>';
    }
  };

  screens.details = {
    step: 1,
    html: function () {
      var e = state.errors;
      return progress(1) +
        errorSummary(e, ["day", "sort", "acct"]) +
        "<h1 tabindex=\"-1\">Your account details</h1>" +
        '<p class="lede">We use these to find your account.</p>' +
        '<form id="details-form" novalidate>' +
        '<div class="field' + hasErr(["day"]) + '"><fieldset role="group" aria-describedby="dob-hint' + (e && e.day ? " day-error" : "") + '">' +
        "<legend>Date of birth</legend>" +
        '<span class="hint" id="dob-hint">For example, 27 3 1951</span>' + fieldErr("day") +
        '<div class="date-row">' +
        '<div><label for="day">Day</label><input class="input w-2' + invalid("day") + '" id="day" name="day" inputmode="numeric" autocomplete="bday-day" maxlength="2" value="' + esc(state.day) + '"></div>' +
        '<div><label for="month">Month</label><input class="input w-2' + invalid("day") + '" id="month" name="month" inputmode="numeric" autocomplete="bday-month" maxlength="2" value="' + esc(state.month) + '"></div>' +
        '<div><label for="year">Year</label><input class="input w-4' + invalid("day") + '" id="year" name="year" inputmode="numeric" autocomplete="bday-year" maxlength="4" value="' + esc(state.year) + '"></div>' +
        "</div></fieldset></div>" +
        '<div class="field' + hasErr(["sort"]) + '"><label for="sort">Sort code</label>' +
        '<span class="hint" id="sort-hint">6 numbers, for example 30 94 12</span>' + fieldErr("sort") +
        '<input class="input w-sort' + invalid("sort") + '" id="sort" name="sort" inputmode="numeric" autocomplete="off" maxlength="8"' + describedBy("sort", true) + ' value="' + esc(state.sort) + '"></div>' +
        '<div class="field' + hasErr(["acct"]) + '"><label for="acct">Account number</label>' +
        '<span class="hint" id="acct-hint">8 numbers</span>' + fieldErr("acct") +
        '<input class="input w-acct' + invalid("acct") + '" id="acct" name="acct" inputmode="numeric" autocomplete="off" maxlength="10"' + describedBy("acct", true) + ' value="' + esc(state.acct) + '"></div>' +
        '<p><button type="button" class="link-btn" data-help="details">Where do I find these numbers?</button></p>' +
        '<div class="actions inline"><button class="btn" type="submit">Continue</button></div>' +
        "</form>";
    },
    after: function () {
      document.getElementById("details-form").addEventListener("submit", function (ev) {
        ev.preventDefault();
        var f = ev.target;
        state.day = f.day.value.trim(); state.month = f.month.value.trim(); state.year = f.year.value.trim();
        state.sort = f.sort.value.trim(); state.acct = f.acct.value.trim();
        var errs = validateDetails();
        if (errs) { state.errors = errs; render(); focusSummary(); return; }
        state.errors = null;
        go("checking");
      });
    }
  };

  function validateDetails() {
    var e = {};
    var d = +digits(state.day), m = +digits(state.month), y = +digits(state.year);
    if (!state.day && !state.month && !state.year) e.day = "Enter your date of birth";
    else if (!state.day || !state.month || !state.year) e.day = "Your date of birth needs a day, a month and a year";
    else if (m < 1 || m > 12) e.day = "The month should be a number from 1 to 12";
    else if (d < 1 || d > 31) e.day = "The day should be a number from 1 to 31";
    else if (digits(state.year).length !== 4) e.day = "Enter the year as 4 numbers, for example 1951";
    else if (y < 1900 || y > 2008) e.day = "Check the year you were born";
    var s = digits(state.sort), a = digits(state.acct);
    if (!s) e.sort = "Enter your sort code";
    else if (s.length !== 6) e.sort = "Your sort code should be 6 numbers. You have entered " + s.length + ".";
    if (!a) e.acct = "Enter your account number";
    else if (a.length !== 8) e.acct = "Your account number should be 8 numbers. You have entered " + a.length + ".";
    return Object.keys(e).length ? e : null;
  }

  function focusSummary() {
    var s = document.getElementById("error-summary");
    if (s) s.focus();
  }

  /* Checking: the moment people are most likely to worry. Words for each
     stage, a calm pulse, and an honest message if it is slow or fails. */
  function checkingScreen(mode) {
    return {
      step: 1,
      back: false,
      html: function () {
        var rows = [
          ["Finding your account", mode === "failed" ? "now" : "done"],
          ["Matching your date of birth", mode === "normal" || mode === "slow" || mode === "veryslow" ? "now" : (mode === "failed" ? "todo" : "failed")],
          ["Getting a text ready", "todo"]
        ];
        if (mode === "failed") rows[0][1] = "failed";
        if (mode === "normal" && state.tick < 1) { rows[0][1] = "now"; rows[1][1] = "todo"; }
        var li = rows.map(function (r) {
          var cls = { done: "is-done", now: "is-now", failed: "is-failed", todo: "" }[r[1]];
          var dot = r[1] === "done" ? ICON.tick : r[1] === "failed" ? "!" : "";
          var label = { done: "Done", now: "Checking", failed: "Stopped", todo: "Waiting" }[r[1]];
          return '<li class="' + cls + '"><span class="dot" aria-hidden="true">' + dot + "</span><span>" + r[0] + '</span><span class="state">' + label + "</span></li>";
        }).join("");

        var title, lede, slot = "", actions = "";
        if (mode === "failed") {
          title = "We could not finish checking";
          lede = "Our system did not reply in time. Nothing has been changed on your account and no money has moved.";
          slot = '<div class="panel"><p>This is a problem on our side, not with the details you entered. They are still filled in if you try again.</p></div>';
          actions = '<div class="actions"><button class="btn" data-go="checking">Try again</button>' +
            '<button class="btn secondary" data-help="checking">Get help</button></div>';
        } else if (mode === "nomatch") {
          title = "We could not find your account";
          lede = "The date of birth, sort code and account number do not match an account we hold.";
          slot = '<div class="panel"><p>Check the numbers against your card or statement. If they are right, your date of birth may be recorded differently. Please call us and we will sort it out.</p></div>';
          actions = '<div class="actions"><button class="btn" data-go="details">Check my details</button>' + "</div>" + callBox();
        } else {
          title = "Checking your details";
          lede = "This usually takes less than a minute. You do not need to do anything.";
          if (mode === "slow") {
            slot = '<div class="panel" role="status"><p><strong>This is taking longer than usual.</strong> We are still checking. Please keep this screen open.</p></div>';
          } else if (mode === "veryslow") {
            slot = '<div class="panel" role="status"><p><strong>Still checking, sorry for the wait.</strong> You can keep waiting, or stop and try again later. Your details will be kept.</p>' +
              '<p><button class="link-btn" data-go="details">Stop and go back</button></p></div>';
          }
        }
        return progress(1) + "<h1 tabindex=\"-1\">" + title + "</h1>" + '<p class="lede">' + lede + "</p>" +
          '<ol class="plain checks" aria-label="Progress">' + li + "</ol>" +
          '<div class="slow-slot">' + slot + "</div>" + actions;
      },
      after: function () {
        if (mode !== "normal") return;
        // Live simulation: 2s per stage. Sort code 11-11-11 simulates slowness,
        // 00-00-00 finds no account.
        var slow = digits(state.sort) === "111111";
        state.checkTimer = setTimeout(function () {
          state.tick = 1; rerenderChecking();
          state.checkTimer = setTimeout(function () {
            if (digits(state.sort) === "000000") { go("checking-nomatch"); return; }
            if (!slow) { go("code"); return; }
            history.replaceState(null, "", "#checking-slow"); render(); announce("This is taking longer than usual. We are still checking.");
            state.checkTimer = setTimeout(function () {
              history.replaceState(null, "", "#checking-veryslow"); render();
              announce("Still checking. You can keep waiting, or stop and try again later.");
              state.checkTimer = setTimeout(function () { go("code"); }, 6000);
            }, 8000);
          }, 2200);
        }, 1800);
      }
    };
  }
  function rerenderChecking() {
    $screen.innerHTML = screens.checking.html();
  }
  screens.checking = checkingScreen("normal");
  screens["checking-slow"] = checkingScreen("slow");
  screens["checking-veryslow"] = checkingScreen("veryslow");
  screens["checking-failed"] = checkingScreen("failed");
  screens["checking-nomatch"] = checkingScreen("nomatch");

  screens.code = {
    step: 2,
    html: function () {
      var e = state.errors;
      return progress(2) + errorSummary(e, ["code"]) +
        "<h1 tabindex=\"-1\">Enter the code we sent you</h1>" +
        '<p class="lede">We have sent a text to your mobile ending <strong>' + MOBILE_END + "</strong>. It can take up to 2 minutes to arrive.</p>" +
        '<p class="small" id="sms-label">The text will look like this:</p>' +
        '<div class="sms" aria-labelledby="sms-label"><span class="sms-from">' + BANK + "</span>Your " + BANK + " code is 482 913. Never share it. We will never call you to ask for it.</div>" +
        '<form id="code-form" novalidate><div class="field' + hasErr(["code"]) + '">' +
        '<label for="code">6-number code</label>' + fieldErr("code") +
        '<input class="input w-code' + invalid("code") + '" id="code" name="code" inputmode="numeric" autocomplete="one-time-code" maxlength="7"' + describedBy("code", false) + ' value="' + esc(state.code) + '"></div>' +
        '<div class="actions inline"><button class="btn" type="submit">Continue</button></div></form>' +
        '<p class="after-form"><button class="link-btn" data-go="code-help">I have not received a text</button></p>';
    },
    after: function () {
      document.getElementById("code-form").addEventListener("submit", function (ev) {
        ev.preventDefault();
        state.code = ev.target.code.value.trim();
        var c = digits(state.code);
        if (!c) state.errors = { code: "Enter the 6-number code from the text" };
        else if (c.length !== 6) state.errors = { code: "The code is 6 numbers. You have entered " + c.length + "." };
        else if (c === "000000") { state.tries -= 1; state.errors = { code: wrongCodeMsg() }; }
        else state.errors = null;
        if (state.errors) { render(); focusSummary(); return; }
        go("passcode");
      });
    }
  };
  function wrongCodeMsg() {
    if (state.tries <= 0) return "That code does not match. For your safety, please ask for a new code.";
    return "That code does not match the one we sent. Check the text and try again. You can try " +
      (state.tries === 1 ? "1 more time" : state.tries + " more times") + ".";
  }

  screens["code-help"] = {
    step: 2,
    html: function () {
      return progress(2) + "<h1 tabindex=\"-1\">If the text has not arrived</h1>" +
        '<p class="lede">Texts can take a few minutes, especially with a weak signal.</p>' +
        '<div class="actions inline">' +
        '<button class="btn" data-action="resend">Send the text again</button>' +
        '<button class="btn secondary" data-action="callme">Call my phone and read the code out</button>' +
        "</div>" +
        "<h2>My mobile number has changed</h2>" +
        "<p>For your safety we can only send the code to the number we already have. To change it, call us or visit a branch with photo ID.</p>" +
        callBox("Call us") ;
    }
  };

  screens.passcode = {
    step: 3,
    html: function () {
      var e = state.errors;
      return progress(3) + errorSummary(e, ["passcode"]) +
        "<h1 tabindex=\"-1\">Make a 6-number passcode</h1>" +
        '<p class="lede">You will use this to open the app. Choose numbers you will remember but other people would not guess.</p>' +
        '<form id="pc-form" novalidate><div class="field' + hasErr(["passcode"]) + '">' +
        '<label for="passcode">New passcode</label><span class="hint" id="passcode-hint">Do not use your date of birth or numbers in order, like 123456</span>' + fieldErr("passcode") +
        '<input class="input w-code' + invalid("passcode") + '" id="passcode" name="passcode" type="password" inputmode="numeric" autocomplete="new-password" maxlength="6"' + describedBy("passcode", true) + "></div>" +
        '<label class="check"><input type="checkbox" id="show"> Show the numbers as I type</label>' +
        '<div class="actions inline"><button class="btn" type="submit">Continue</button></div></form>';
    },
    after: function () {
      bindShow("passcode");
      document.getElementById("pc-form").addEventListener("submit", function (ev) {
        ev.preventDefault();
        var p = digits(ev.target.passcode.value);
        var err = passcodeProblem(p);
        if (err) { state.errors = { passcode: err }; render(); focusSummary(); return; }
        state.errors = null; state.passcode = p;
        go("passcode-confirm");
      });
    }
  };
  function passcodeProblem(p) {
    if (!p) return "Enter a passcode of 6 numbers";
    if (p.length !== 6) return "Your passcode needs 6 numbers. You have entered " + p.length + ".";
    if (/^(\d)\1+$/.test(p) || "0123456789".indexOf(p) >= 0 || "9876543210".indexOf(p) >= 0)
      return "That passcode would be easy for someone to guess. Choose numbers that are not in order or all the same.";
    var dob = ("0" + digits(state.day)).slice(-2) + ("0" + digits(state.month)).slice(-2) + digits(state.year).slice(-2);
    if (state.day && p === dob) return "That is your date of birth, which other people may know. Choose different numbers.";
    return null;
  }
  function bindShow(id) {
    var box = document.getElementById("show"), input = document.getElementById(id);
    box.addEventListener("change", function () { input.type = box.checked ? "text" : "password"; });
  }

  screens["passcode-confirm"] = {
    step: 3,
    html: function () {
      var e = state.errors;
      return progress(3) + errorSummary(e, ["confirm"]) +
        "<h1 tabindex=\"-1\">Enter your passcode again</h1>" +
        '<p class="lede">This makes sure it was typed the way you meant.</p>' +
        '<form id="pc2-form" novalidate><div class="field' + hasErr(["confirm"]) + '">' +
        '<label for="confirm">Passcode again</label>' + fieldErr("confirm") +
        '<input class="input w-code' + invalid("confirm") + '" id="confirm" name="confirm" type="password" inputmode="numeric" autocomplete="new-password" maxlength="6"' + describedBy("confirm", false) + "></div>" +
        '<label class="check"><input type="checkbox" id="show"> Show the numbers as I type</label>' +
        '<div class="actions inline"><button class="btn" type="submit">Continue</button></div></form>' +
        (e ? '<p class="after-form"><button class="link-btn" data-go="passcode">Choose a different passcode</button></p>' : "");
    },
    after: function () {
      bindShow("confirm");
      document.getElementById("pc2-form").addEventListener("submit", function (ev) {
        ev.preventDefault();
        var p = digits(ev.target.confirm.value);
        if (!p) state.errors = { confirm: "Enter your passcode again" };
        else if (p !== state.passcode) state.errors = { confirm: "The passcodes do not match. Enter the same 6 numbers as on the last screen." };
        else state.errors = null;
        if (state.errors) { render(); focusSummary(); return; }
        go("fingerprint");
      });
    }
  };

  screens.fingerprint = {
    step: 3,
    html: function () {
      return progress(3) + "<h1 tabindex=\"-1\">Open the app with your fingerprint?</h1>" +
        '<p class="lede">Instead of typing your passcode each time, you can touch the sensor on your phone.</p>' +
        "<p>Your passcode will still work. We never see or store your fingerprint; it stays on your phone.</p>" +
        '<p class="small">You can change this later in Settings.</p>' +
        '<div class="actions"><button class="btn" data-go="safety">Use my fingerprint</button>' +
        '<button class="btn secondary" data-go="safety">Not now, use my passcode</button></div>';
    }
  };

  screens.safety = {
    step: 4,
    html: function () {
      return progress(4) + "<h1 tabindex=\"-1\">Three things we will never do</h1>" +
        '<p class="lede">Criminals pretend to be banks. Knowing these keeps your money safe.</p>' +
        '<ol class="plain promises">' +
        "<li>We will never ask for your passcode or a text code, by phone, text or email.</li>" +
        "<li>We will never ask you to move money to a “safe account”.</li>" +
        "<li>We will never send someone to your home to collect your card or cash.</li>" +
        "</ol>" +
        "<p>If anyone does, hang up. Then call the number on the back of your card, using a different phone if you can.</p>" +
        '<div class="actions"><button class="btn" data-go="done">I understand</button></div>';
    }
  };

  screens.done = {
    back: false,
    html: function () {
      return '<div class="done-mark">' + ICON.bigTick + "</div>" +
        "<h1 tabindex=\"-1\">You are set up</h1>" +
        '<p class="lede">Next time, open the app and use your passcode' + " to get in.</p>" +
        '<div class="panel"><div class="account"><span>Current account<br><span class="small">Ending 4417</span></span><span class="amount">£1,284.50</span></div></div>' +
        "<p>Your branch, card and telephone banking work just as before.</p>" +
        '<div class="actions"><button class="btn" data-go="welcome">Go to my accounts</button></div>';
    }
  };

  /* ---------- help content, specific to where you are ---------- */

  var help = {
    details: '<h3>Where to find your sort code and account number</h3>' +
      "<p>They are printed on the front of your bank card, at the top of your paper statement, at the bottom of your cheques and inside your passbook.</p>" +
      '<svg class="card-art" viewBox="0 0 288 180" role="img" aria-label="A bank card with the sort code and account number printed together near the bottom left">' +
      '<rect class="art-ground" x="2" y="2" width="284" height="176" rx="14" stroke="currentColor" stroke-width="2"/>' +
      '<rect x="22" y="44" width="40" height="30" rx="5" fill="none" stroke="currentColor" stroke-width="2"/>' +
      '<text x="26" y="120" font-size="13" fill="currentColor">SORT CODE</text>' +
      '<text x="128" y="120" font-size="13" fill="currentColor">ACCOUNT NUMBER</text>' +
      '<text x="26" y="146" font-size="20" font-weight="700" class="art-strong">30-94-12</text>' +
      '<text x="128" y="146" font-size="20" font-weight="700" class="art-strong">12345678</text>' +
      '<rect x="16" y="102" width="246" height="56" rx="8" class="art-ring" fill="none" stroke-width="3"/></svg>' +
      "<h3>The numbers are different on my card</h3>" +
      "<p>Some older cards show a different number. Use your statement or passbook instead.</p>",
    code: "<h3>The text has not arrived</h3><p>Wait 2 minutes, then use “I have not received a text” on the screen. We can send it again or call your phone and read it out.</p>",
    "code-help": "<h3>Why can you not use a new number?</h3><p>If someone else had your details, they could add their own phone. Changing your number on the phone or in a branch, with ID, protects you.</p>",
    checking: "<h3>What happens while we check?</h3><p>We look up your account and make sure the date of birth matches. Nothing is changed and no money moves.</p><h3>It keeps failing</h3><p>Please call us. We can see what has gone wrong and finish setting up with you.</p>",
    passcode: "<h3>Choosing a passcode</h3><p>Pick 6 numbers that mean something to you but are not written down anywhere, like part of an old phone number. Avoid your birthday and numbers in order.</p><h3>If I forget it</h3><p>You can reset it in the app with your card details and a text code.</p>",
    fingerprint: "<h3>Is it safe?</h3><p>Your fingerprint never leaves your phone. The app only learns whether it matched.</p><h3>Other people’s fingerprints</h3><p>If someone else has added their fingerprint to this phone, they could open the app too. Choose “Not now” if that applies.</p>",
    generic: "<h3>Can I still use my branch?</h3><p>Yes. Nothing about your branch, card or telephone banking changes.</p><h3>Can someone help me do this?</h3><p>Yes. Staff in any branch can set up the app with you. Bring your phone and your card.</p>"
  };
  help["passcode-confirm"] = help.passcode;
  ["checking-slow", "checking-veryslow", "checking-failed", "checking-nomatch"].forEach(function (k) { help[k] = help.checking; });

  function openHelp(key) {
    var k = key || current();
    var body = help[k] || help.generic;
    $helpBody.innerHTML = body + callBox(k === "generic" || !help[k] ? "Talk to a person" : "Still stuck? Talk to a person");
    $helpSheet.showModal();
  }

  /* ---------- timeout (WCAG 2.2.1: people can ask for more time) ---------- */

  function openTimeout() { $timeout.showModal(); }
  document.getElementById("more-time").addEventListener("click", function () { $timeout.close(); announce("You have 20 more minutes."); });
  document.getElementById("stop-now").addEventListener("click", function () { $timeout.close(); go("welcome"); });

  /* ---------- router ---------- */

  function current() { return location.hash.slice(1) || "welcome"; }

  // Prototype states that need data or errors pre-filled. After applying,
  // the URL is rewritten to the real screen so submitting works normally.
  var demo = {
    "details-errors": function () {
      state.day = "27"; state.month = "13"; state.year = "1951"; state.sort = "30941"; state.acct = "";
      state.errors = validateDetails(); return "details";
    },
    "code-wrong": function () { state.tries = 2; state.code = "000000"; state.errors = { code: wrongCodeMsg() }; return "code"; },
    "passcode-easy": function () { state.errors = { passcode: passcodeProblem("123456") }; return "passcode"; },
    "passcode-mismatch": function () { state.passcode = "583920"; state.errors = { confirm: "The passcodes do not match. Enter the same 6 numbers as on the last screen." }; return "passcode-confirm"; },
    "help": function () { setTimeout(function () { openHelp("details"); }, 0); return "details"; },
    "timeout": function () { setTimeout(openTimeout, 0); return "code"; }
  };

  var lastRoute = null;
  function render() {
    clearTimeout(state.checkTimer);
    var r = current();
    if (demo[r]) {
      state.errors = null;
      r = demo[r]();
      history.replaceState(null, "", "#" + r);
    } else if (r !== lastRoute) {
      state.errors = null;          // arriving on a screen fresh: no old errors
    }
    if (r !== lastRoute) state.tick = 0;
    var s = screens[r] || screens.welcome;
    lastRoute = r;
    var showBack = s.back !== false;
    $back.hidden = !showBack;
    $backSpacer.hidden = showBack;
    $screen.innerHTML = s.html();
    $screen.dataset.screen = r;
    document.title = ($screen.querySelector("h1") || {}).textContent + " \u2013 " + BANK;
    if (s.after) s.after();
    var h = $screen.querySelector("h1");
    if (!document.querySelector("#error-summary") && h) h.focus({ preventScroll: true });
    window.scrollTo(0, 0);
  }

  var prev = { prepare: "welcome", "new": "welcome", details: "prepare", code: "details", "code-help": "code",
    passcode: "code", "passcode-confirm": "passcode", fingerprint: "passcode-confirm", safety: "fingerprint" };

  $back.addEventListener("click", function () {
    state.errors = null;
    go(prev[$screen.dataset.screen] || "welcome");
  });
  $help.addEventListener("click", function () { openHelp($screen.dataset.screen); });
  $helpSheet.addEventListener("click", function (ev) {
    if (ev.target.hasAttribute("data-close") || ev.target === $helpSheet) $helpSheet.close();
  });

  document.addEventListener("click", function (ev) {
    var t = ev.target.closest("[data-go],[data-help],[data-focus],[data-action]");
    if (!t) return;
    if (t.dataset.focus) {
      ev.preventDefault();
      var el = document.getElementById(t.dataset.focus);
      if (el) { el.focus(); el.scrollIntoView({ block: "center" }); }
      return;
    }
    if (t.dataset.help) { openHelp(t.dataset.help); return; }
    if (t.dataset.action === "resend") { state.tries = 3; state.errors = null; go("code"); setTimeout(function () { announce("We have sent a new text to your mobile ending " + MOBILE_END + "."); }, 300); return; }
    if (t.dataset.action === "callme") { state.errors = null; go("code"); setTimeout(function () { announce("We are calling your mobile ending " + MOBILE_END + " now."); }, 300); return; }
    if (t.dataset.go) { state.errors = null; go(t.dataset.go); }
  });

  window.addEventListener("hashchange", render);

  // Prototype jump list
  var routes = ["welcome", "prepare", "details", "details-errors", "help", "checking", "checking-slow", "checking-veryslow",
    "checking-failed", "checking-nomatch", "code", "code-wrong", "code-help", "timeout", "passcode", "passcode-easy",
    "passcode-confirm", "passcode-mismatch", "fingerprint", "safety", "done", "new"];
  document.getElementById("proto-links").innerHTML = routes.map(function (r) {
    return '<li><a href="#' + r + '">' + r + "</a></li>";
  }).join("");

  render();
})();
