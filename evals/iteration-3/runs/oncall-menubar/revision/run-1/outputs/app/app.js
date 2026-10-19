(() => {
  'use strict';
  const F = window.EVAL_FIXTURES;
  const M = F.menu;
  const app = document.querySelector('#app');
  const params = new URLSearchParams(location.search);
  const states = ['main', 'compose', 'review', 'pending', 'offline', 'empty', 'accepted'];
  let screen = states.includes(params.get('screen')) ? params.get('screen') : 'main';
  let selected = false;
  let note = '';
  let flash = '';
  let owner = params.get('owner') === 'priya' || screen === 'accepted' ? 'priya' : 'jamie';
  let pending = screen === 'pending' || params.get('request') === 'pending';
  let requestOutcome = owner === 'priya' ? 'accepted' : null;
  const darkPreference = matchMedia('(prefers-color-scheme: dark)');
  const applyTheme = () => document.documentElement.dataset.theme = ['light','dark'].includes(params.get('theme')) ? params.get('theme') : darkPreference.matches ? 'dark' : 'light';
  applyTheme();
  darkPreference.addEventListener('change', applyTheme);
  const escapeHTML = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const initials = name => name.split(' ').map(x=>x[0]).join('');
  const paths = {
    rota: '<path d="M5 5h9l-3-3M15 15H6l3 3M16 6v4M4 14v-4"/>',
    arrow: '<path d="M3 8h10M9 4l4 4-4 4"/>',
    clock: '<circle cx="8" cy="8" r="6"/><path d="M8 4v4l3 2"/>',
    check: '<path d="m3 8 3 3 7-7"/>',
    wait: '<circle cx="8" cy="8" r="6" stroke-dasharray="2.5 3"/><path d="M8 4v4l2 1"/>',
    offline: '<path d="m2 2 12 12M2 6a10 10 0 0 1 2-1M7 4a10 10 0 0 1 7 2M4 9a6 6 0 0 1 2-1M10 8l2 1M7 12l1-1 1 1"/>',
    calendar: '<rect x="2" y="3" width="12" height="11" rx="2"/><path d="M5 1v4M11 1v4M2 7h12M6 10h4"/>',
    back: '<path d="m10 3-5 5 5 5"/>'
  };
  const icon = name => `<svg class="icon" viewBox="0 0 16 16" aria-hidden="true">${paths[name] || ''}</svg>`;
  const button = (text, action, type='primary', disabled=false) => `<button type="button" class="${type}" data-action="${action}" ${disabled ? 'disabled' : ''}>${text}</button>`;
  const header = (action='') => `<header class="app-header"><div class="brand">${icon('rota')}<span>${escapeHTML(M.product)}</span></div>${action || '<span class="team-label">Team · '+M.teamSize+' people</span>'}</header>`;
  const now = new Date(F.now);
  const asOf = now.toISOString().slice(11,16);
  const shortDate = now.toLocaleDateString('en-GB',{day:'numeric',month:'short',timeZone:'UTC'});
  const toMinutes = time => time.split(':').reduce((hours, minutes) => Number(hours) * 60 + Number(minutes));
  const totalHours = (toMinutes(M.shiftEnd) - toMinutes(M.shiftStart)) / 60;
  const elapsedHours = Math.min(totalHours, Math.max(0, (now.getUTCHours() * 60 + now.getUTCMinutes() - toMinutes(M.shiftStart)) / 60));
  const remainingHours = totalHours - elapsedHours;
  app.style.setProperty('--progress', `${elapsedHours / totalHours * 100}%`);
  const date = new Date(F.now).toLocaleDateString('en-GB',{weekday:'long',day:'numeric',month:'long',timeZone:'UTC'});
  const footer = (offline=false) => `<footer class="app-footer"><span class="footer-note">${icon(offline?'offline':'clock')}${offline?'Last known':'Schedule as of'} ${asOf} UTC</span><span>${shortDate}</span></footer>`;
  const person = p => `<li class="person"><span class="avatar" aria-hidden="true">${initials(p.name)}</span><div class="person-info"><div class="person-name">${escapeHTML(p.name)}</div><div class="person-role">${escapeHTML(p.role)}</div></div><time>${p.until}</time></li>`;
  const roster = (offline=false) => `<section class="roster" aria-labelledby="roster-title"><div class="section-heading"><h2 id="roster-title">${offline?`Also on call at ${asOf}`:'Also on call'}</h2><span>Until · UTC</span></div><ul class="people">${M.roster.filter(p=>p.name !== M.user).map(person).join('')}</ul></section>`;
  const responsibility = text => `<p class="responsibility">${icon('clock')}<span>${text}</span></p>`;
  function transfer() {
    return `<section class="transfer" aria-label="Handover details"><div class="transfer-person"><span class="avatar" aria-hidden="true">JE</span><div><small>From</small><b>${M.user} <span class="optional">(you)</span></b></div></div><div class="transfer-path" aria-hidden="true"></div><div class="transfer-person"><span class="avatar" aria-hidden="true">PR</span><div><small>To</small><b>${M.handoverTo}</b></div></div><div class="transfer-time">${M.rotation}<br>Remainder of today’s shift · until ${M.shiftEnd} UTC</div>${note?`<div class="note-preview"><b>Your note</b>${escapeHTML(note)}</div>`:''}</section>`;
  }
  function mainView(offline=false) {
    const transferred = owner === 'priya';
    let status = offline ? 'Last known: you were on call' : transferred ? 'Priya is on call' : 'You’re on call';
    return `${header()}<div class="content">${offline?'':`<div class="date-line"><span>${date}</span><span class="mono">UTC</span></div>`}${offline?'<aside class="notice"><b>You’re offline · saved at '+asOf+' UTC</b><p>Coverage may have changed. Reconnect to hand over a shift.</p></aside>':''}${flash?`<p class="inline-status" role="status">${flash}</p>`:''}<section class="shift" aria-labelledby="shift-title"><div class="status"><span class="dot" aria-hidden="true"></span>${status}</div><h1 id="shift-title" tabindex="-1">${M.rotation}</h1><p class="owner">${transferred ? M.handoverTo : M.user+' (you)'}</p><div class="shift-time"><span>${M.shiftStart}</span><span>${M.shiftEnd} UTC</span></div>${offline?'':`<div class="progress" role="progressbar" aria-label="Shift progress at ${asOf} UTC" aria-valuemin="0" aria-valuemax="${totalHours}" aria-valuenow="${elapsedHours}"><span></span></div>`}${offline?'':`<p class="remaining">${transferred?'Your handover is complete.':`${remainingHours} hours remaining`}</p>`}${offline?button('Hand over shift','compose','primary',true):transferred?'':pending?button('View pending handover '+icon('arrow'),'pending'):button('Hand over shift '+icon('arrow'),'compose')}</section>${roster(offline)}${offline?`<div class="actions">${button('Try again','retry','text-button')}</div><p class="screen-status" role="status" id="retry-status"></p>`:''}</div>${footer(offline)}`;
  }
  function composeView() {
    return `${header(button('Cancel','cancel','text-button'))}<div class="content"><div class="page-intro"><div class="eyebrow">Handover · 1 of 2</div><h1 tabindex="-1">Hand over shift</h1><p>Ask a teammate to take the rest of your shift.</p></div><div class="shift-summary"><b>${M.rotation}</b><span>Today · ${M.shiftStart}–${M.shiftEnd} UTC</span></div><form id="handover-form"><fieldset><legend>Hand over to</legend><label class="recipient"><span class="avatar" aria-hidden="true">PR</span><span><span class="person-name">${M.handoverTo}</span><br><span class="optional">Suggested teammate</span></span><input type="radio" name="recipient" value="priya" aria-label="${M.handoverTo}" ${selected?'checked':''} required></label></fieldset><div class="field"><label class="field-label" for="note">Handover note <span class="optional">(optional)</span></label><textarea id="note" name="note" maxlength="500" placeholder="Anything Priya should know?">${escapeHTML(note)}</textarea></div>${responsibility('You stay on call until Priya accepts.')}<div class="actions"><button class="primary" id="review-button" type="submit" ${selected?'':'disabled'}>Review handover ${icon('arrow')}</button></div></form></div>${footer()}`;
  }
  function reviewView() {
    return `${header(button(icon('back')+' Back','compose','text-button'))}<div class="content"><div class="page-intro"><div class="eyebrow">Handover · 2 of 2</div><h1 tabindex="-1">Review handover</h1><p>Check the details before sending your request.</p></div>${transfer()}${responsibility('Sending a request does not end your responsibility. You stay on call until Priya accepts.')}<div class="actions">${button('Send handover request','send')}${button('Cancel','cancel','text-button')}</div></div>${footer()}`;
  }
  function pendingView() {
    return `${header()}<div class="content"><div class="state-symbol">${icon('wait')}</div><div class="page-intro"><h1 tabindex="-1">Waiting for Priya</h1><p>Your handover request is pending acceptance.</p></div>${transfer()}<aside class="notice pending-responsibility"><b>You’re still on call</b><p>You remain responsible for ${M.rotation} until Priya accepts.</p></aside><div class="actions">${button('Back to schedule','schedule')}${button('Cancel request','cancel-request','text-button')}</div></div>${footer()}`;
  }
  function acceptedView() {
    return `${header()}<div class="content"><div class="state-symbol success">${icon('check')}</div><div class="page-intro"><div class="eyebrow">Handover complete</div><h1 tabindex="-1">Priya is now on call</h1><p>You’re off call for the rest of this shift.</p></div>${transfer()}<p class="responsibility">${icon('check')}<span>Priya accepted responsibility for ${M.rotation} until ${M.shiftEnd} UTC.</span></p><div class="actions">${button('Back to schedule','schedule')}</div></div>${footer()}`;
  }
  function emptyView() {
    return `${header()}<div class="content empty-content"><div class="state-symbol">${icon('calendar')}</div><h1 tabindex="-1">No schedule available</h1><p>There are no on-call shifts to show. Check with your rotation owner to confirm coverage.</p><div class="actions">${button('Check again','check-empty','secondary')}</div><p class="screen-status" role="status" id="empty-status"></p></div>${footer()}`;
  }
  function writeURL(replace=false) {
    const url = new URL(location.href);
    url.searchParams.set('screen',screen);
    if(owner==='priya') url.searchParams.set('owner','priya'); else url.searchParams.delete('owner');
    if(pending) url.searchParams.set('request','pending'); else url.searchParams.delete('request');
    history[replace?'replaceState':'pushState']({},'',url);
  }
  function render(focus=false) {
    app.className = screen === 'offline' ? 'offline' : '';
    app.dataset.screen = screen;
    app.innerHTML = screen==='main'? mainView() : screen==='offline'? mainView(true) : screen==='compose'? composeView() : screen==='review'? reviewView() : screen==='pending'? pendingView() : screen==='accepted'? acceptedView() : emptyView();
    document.title = `Rota — ${ {main:'On call',compose:'Hand over shift',review:'Review handover',pending:'Waiting for Priya',offline:'Offline schedule',empty:'No schedule',accepted:'Handover complete'}[screen]}`;
    app.scrollTop = 0;
    if(focus) app.querySelector('h1')?.focus({preventScroll:true});
  }
  function go(next) { screen=next; flash=''; writeURL(); render(true); }
  function cancelRequest() { pending=false; requestOutcome='cancelled'; selected=false; note=''; screen='main'; flash='Request cancelled. You’re still on call.'; writeURL(); render(true); }
  app.addEventListener('input',e=>{if(e.target.id==='note') note=e.target.value;});
  app.addEventListener('change',e=>{if(e.target.name==='recipient'){selected=true;app.querySelector('#review-button').disabled=false;}});
  app.addEventListener('submit',e=>{e.preventDefault();if(selected){note=app.querySelector('#note').value;go('review');}});
  app.addEventListener('click',e=>{
    const action=e.target.closest('[data-action]')?.dataset.action;
    if(!action) return;
    if(action==='compose'){if(screen==='review') selected=true;go('compose');}
    if(action==='pending') go('pending');
    if(action==='cancel'){selected=false;note='';go('main');}
    if(action==='send'){pending=true;requestOutcome=null;go('pending');}
    if(action==='schedule') go('main');
    if(action==='cancel-request') cancelRequest();
    if(action==='retry') app.querySelector('#retry-status').textContent='Still offline. The last-known schedule is shown.';
    if(action==='check-empty') app.querySelector('#empty-status').textContent='No schedule is available. Confirm coverage with your rotation owner.';
  });
  document.addEventListener('keydown',e=>{
    if(e.key==='Escape' && ['compose','review'].includes(screen)){e.preventDefault();if(screen==='review')go('compose');else go('main');}
  });
  window.addEventListener('popstate',()=>{
    const q=new URLSearchParams(location.search);
    screen=states.includes(q.get('screen'))?q.get('screen'):'main';
    owner=q.get('owner')==='priya'||screen==='accepted'||requestOutcome==='accepted'?'priya':'jamie';
    pending=requestOutcome===null && (screen==='pending'||q.get('request')==='pending');
    if(screen==='pending' && requestOutcome) screen=requestOutcome==='accepted'?'accepted':'main';
    if(owner==='priya' && ['compose','review'].includes(screen)) screen='main';
    writeURL(true);render(true);
  });
  // Only the separate local review harness can explicitly simulate acceptance.
  window.addEventListener('message',e=>{
    if(window.parent===window || e.source!==window.parent || e.data?.type!=='rota:simulate-acceptance' || !pending) return;
    pending=false;owner='priya';requestOutcome='accepted';go('accepted');
  });
  render();
})();
