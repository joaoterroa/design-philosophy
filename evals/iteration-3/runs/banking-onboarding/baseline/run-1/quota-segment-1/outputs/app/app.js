(() => {
  'use strict';
  const bank = window.EVAL_FIXTURES.bank;
  const app = document.getElementById('app');
  const params = new URLSearchParams(location.search);
  const allowed = ['welcome', 'details', 'details-error', 'code', 'code-error', 'help', 'done'];
  const initial = allowed.includes(params.get('screen')) ? params.get('screen') : 'welcome';
  let screen = initial === 'help' ? 'code' : initial;
  let name = initial === 'details-error' ? '' : bank.customer;
  let mobile = initial === 'details-error' ? '07700' : '';
  let code = '';
  let savedFocus = null;
  const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const arrow = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m14 6-6 6 6 6M8 12h13"/></svg>';
  const mark = '<svg class="brand-mark" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 22V13a10 10 0 0 1 20 0v9M3 22c4-4 9 4 13 0s9 4 13 0M3 28c4-4 9 4 13 0s9 4 13 0"/></svg>';
  const steps = n => `<div class="topline"><button type="button" class="utility back" id="back">${arrow}Back</button><p class="step">Step ${n} of 2</p></div>`;
  const disclosure = '<p class="fine disclosure">Preview only. No account changes.</p>';

  function updateURL(next, replace = false) {
    const url = new URL(location.href);
    url.searchParams.set('screen', next);
    history[replace ? 'replaceState' : 'pushState']({}, '', url);
  }
  function go(next) {
    screen = next;
    updateURL(next);
    render(true);
    window.scrollTo(0, 0);
  }
  function welcome() {
    return `<main class="welcome"><p class="eyebrow">MOBILE BANKING</p><h1>Your bank.<br>Now at home.</h1><p class="intro">Let’s set up your phone, one step at a time.</p><ol class="journey" aria-label="What happens next"><li><span class="number" aria-hidden="true">1</span><div><strong>Tell us your details</strong><p>Your name and mobile number.</p></div></li><li><span class="number" aria-hidden="true">2</span><div><strong>Enter a text message code</strong><p>To check it’s your phone.</p></div></li><li><span class="number" aria-hidden="true">✓</span><div><strong>You’re ready</strong><p>See your account in one place.</p></div></li></ol><div class="actions"><button class="primary" id="start">Get started</button><p class="reassurance fine">Have your mobile phone to hand.<br>There’s no need to rush.</p>${disclosure}</div></main>`;
  }
  function details() {
    const invalid = screen === 'details-error';
    return `<main>${steps(1)}<h1>Your details</h1><p class="intro">Use the details you gave us when you opened your account.</p><form id="details-form" novalidate><div class="field"><label for="full-name">Full name</label><input id="full-name" name="name" autocomplete="name" type="text" value="${escape(name)}" aria-describedby="name-error" ${invalid ? 'aria-invalid="true"' : ''}><p id="name-error" class="error">${invalid ? 'Enter your name as it appears on your account.' : ''}</p></div><div class="field"><label for="mobile">Mobile number</label><p class="hint" id="mobile-hint">A UK mobile number, starting 07 or +44.</p><input id="mobile" name="mobile" autocomplete="tel" inputmode="tel" type="tel" value="${escape(mobile)}" aria-describedby="mobile-hint mobile-error" ${invalid ? 'aria-invalid="true"' : ''}><p id="mobile-error" class="error">${invalid ? 'Enter the full mobile number. A number starting 07 has 11 digits.' : ''}</p></div><p class="fine">We’ll use this number for your security code.</p><div class="actions"><button class="primary" type="submit">Continue</button>${disclosure}</div></form></main>`;
  }
  function codeStep() {
    const invalid = screen === 'code-error';
    const ending = mobile ? mobile.replace(/\D/g, '').slice(-3) : bank.mobileEnding;
    return `<main>${steps(2)}<h1>Check your phone</h1><p class="intro">Enter the ${bank.codeLength}-digit code from the text message to your mobile ending <strong>${escape(ending)}</strong>.</p><form id="code-form" novalidate><div class="field"><label for="code">Security code</label><input class="code-input" id="code" name="code" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="12" spellcheck="false" value="${escape(code)}" aria-describedby="code-hint code-error" ${invalid ? 'aria-invalid="true"' : ''}><p id="code-hint" class="sr-only">Enter all ${bank.codeLength} digits in this field. You can also paste the code.</p><p class="error" id="code-error">${invalid ? `That code doesn’t match. Check the ${bank.codeLength} digits and try again.` : ''}</p><button type="button" class="utility inline-action" id="code-help">I haven’t received a code</button></div><aside class="notice" aria-label="Keep your code safe"><strong>Keep your code safe</strong>${escape(bank.warning)}</aside><p class="fine prototype">In this preview, no text message is sent.</p><div class="actions"><button class="primary" type="submit">Confirm code</button></div></form></main>`;
  }
  function done() {
    return `<main><div class="success-mark" aria-hidden="true"><svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2"><path d="m8 16 5 5L24 10"/></svg></div><h1>You’re all set,<br>${escape((name || bank.customer).split(' ')[0])}.</h1><p class="intro">Your account, now a little closer.</p><section class="account" aria-label="Your account details"><div class="account-heading"><p class="fine">${escape(bank.name)}</p><strong>${escape(bank.accountName)}</strong></div><dl><div><dt>Account holder</dt><dd>${escape(name || bank.customer)}</dd></div><div><dt>Sort code</dt><dd>${escape(bank.sortCode)}</dd></div><div><dt>Account number</dt><dd>${escape(bank.accountNumber)}</dd></div><div><dt>Available balance</dt><dd class="balance">${escape(bank.balance)}</dd></div></dl></section><p class="fine">Need a hand finding your way?<br>Help is always at the top of the screen.</p><div class="actions"><button class="primary" id="finish">Finish</button>${disclosure}</div></main>`;
  }
  function helpDialog() {
    return `<dialog id="help-dialog" aria-labelledby="help-title" aria-describedby="help-description"><h2 id="help-title" tabindex="-1">Talk to us</h2><p id="help-description">Our team can help you set up mobile banking.</p><a class="primary" href="tel:${bank.helpPhone.replace(/\s/g, '')}"><span>Call our team</span><span class="phone">${escape(bank.helpPhone)}</span></a><p class="fine">Keep your security code private, even when speaking to us.</p><button type="button" class="secondary" id="return-help">Back to setup</button></dialog>`;
  }
  function render(focus = false) {
    const content = screen === 'welcome' ? welcome() : screen.startsWith('details') ? details() : screen === 'done' ? done() : codeStep();
    app.innerHTML = `<header class="masthead"><div class="brand">${mark}<span>${escape(bank.name)}</span></div><button class="utility" id="help" aria-label="Help with setup">Help</button></header>${content}<div class="sr-only" role="status" id="announcement"></div>${helpDialog()}`;
    document.title = `${document.querySelector('h1').textContent} · ${bank.name}`;
    document.querySelector('h1').tabIndex = -1;
    if (focus) document.querySelector('h1').focus({preventScroll:true});
    document.getElementById('help').addEventListener('click', openHelp);
    document.getElementById('start')?.addEventListener('click', () => { name = ''; mobile = ''; go('details'); });
    document.getElementById('back')?.addEventListener('click', () => { capture(); go(screen.startsWith('details') ? 'welcome' : 'details'); });
    document.getElementById('code-help')?.addEventListener('click', openHelp);
    document.getElementById('finish')?.addEventListener('click', () => go('welcome'));
    document.getElementById('details-form')?.addEventListener('submit', validateDetails);
    document.getElementById('code-form')?.addEventListener('submit', validateCode);
    document.getElementById('return-help').addEventListener('click', closeHelp);
    const dialog = document.getElementById('help-dialog');
    dialog.addEventListener('cancel', event => { event.preventDefault(); closeHelp(); });
  }
  function capture() {
    name = document.getElementById('full-name')?.value ?? name;
    mobile = document.getElementById('mobile')?.value ?? mobile;
    code = document.getElementById('code')?.value ?? code;
  }
  function setError(id, message) {
    const input = document.getElementById(id);
    input.setAttribute('aria-invalid', message ? 'true' : 'false');
    document.getElementById(id === 'full-name' ? 'name-error' : `${id}-error`).textContent = message;
  }
  function validateDetails(event) {
    event.preventDefault(); capture();
    name = name.trim();
    const digits = mobile.replace(/[\s()-]/g, '');
    const validName = name.length >= 2 && /\p{L}/u.test(name);
    const validPhone = /^(07\d{9}|\+447\d{9})$/.test(digits);
    setError('full-name', validName ? '' : 'Enter your name as it appears on your account.');
    setError('mobile', validPhone ? '' : 'Enter the full mobile number. A number starting 07 has 11 digits.');
    if (!validName || !validPhone) {
      screen = 'details-error'; updateURL(screen, true);
      document.getElementById('announcement').textContent = 'Please check your details. There is a problem with ' + (!validName && !validPhone ? 'your name and mobile number.' : !validName ? 'your name.' : 'your mobile number.');
      document.getElementById(validName ? 'mobile' : 'full-name').focus();
      return;
    }
    code = ''; go('code');
  }
  function validateCode(event) {
    event.preventDefault(); capture();
    const clean = code.replace(/\s/g, '');
    if (clean === bank.testCode) { go('done'); return; }
    const message = new RegExp(`^\\d{${bank.codeLength}}$`).test(clean)
      ? `That code doesn’t match. Check the ${bank.codeLength} digits and try again.`
      : `Enter the ${bank.codeLength}-digit code from your text message.`;
    setError('code', message);
    screen = 'code-error'; updateURL(screen, true);
    document.getElementById('announcement').textContent = message;
    document.getElementById('code').focus();
  }
  function openHelp() {
    savedFocus = document.activeElement?.matches('button, a, input') ? document.activeElement : document.getElementById('help');
    const dialog = document.getElementById('help-dialog');
    dialog.showModal();
    document.getElementById('help-title').focus({preventScroll:true});
    updateURL('help', true);
  }
  function closeHelp() {
    document.getElementById('help-dialog').close();
    updateURL(screen, true);
    (savedFocus?.isConnected ? savedFocus : document.getElementById('help')).focus({preventScroll:true});
  }
  window.addEventListener('popstate', () => {
    capture();
    const next = new URLSearchParams(location.search).get('screen');
    screen = allowed.includes(next) && next !== 'help' ? next : 'code';
    render(true);
    if (next === 'help') openHelp();
  });
  render();
  if (initial === 'help') {
    savedFocus = document.getElementById('help');
    openHelp();
  }
})();
