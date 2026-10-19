(() => {
'use strict';
const F=window.EVAL_FIXTURES, M=F.menu, app=document.querySelector('#app');
const states=['main','compose','pending','offline','empty','accepted'];
const params=new URLSearchParams(location.search);
const system=matchMedia('(prefers-color-scheme: dark)');
function theme(){document.documentElement.dataset.theme=['light','dark'].includes(params.get('theme'))?params.get('theme'):(system.matches?'dark':'light')}
theme();system.addEventListener('change',theme);
document.documentElement.dataset.display=params.get('display')==='tv'?'tv':'laptop';
let state=states.includes(params.get('screen'))?params.get('screen'):'main';
let phase=state==='pending'?'pending':state==='accepted'?'accepted':params.get('handover')||'';
let step=params.get('step')==='review'?'review':'choose';
let recipient=step==='review'?M.handoverTo:'', note='';
let offlineChecked=false, emptyChecked=false;
const date=new Date(F.now), dateLabel=new Intl.DateTimeFormat('en-GB',{weekday:'short',day:'numeric',month:'short',timeZone:'UTC'}).format(date);
const nowLabel=date.toISOString().slice(11,16);
const endHour=Number(M.shiftEnd.split(':')[0]), startHour=Number(M.shiftStart.split(':')[0]);
const hoursLeft=endHour-date.getUTCHours(), elapsed=(date.getUTCHours()-startHour)/(endHour-startHour)*100;
app.style.setProperty('--elapsed',`${elapsed}%`);
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const icon=(name)=>{const paths={back:'<path d="m11 5-6 7 6 7M5 12h14"/>',clock:'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',check:'<path d="m5 12 4 4L19 6"/>',offline:'<path d="m3 3 18 18M8.5 8.5a10 10 0 0 1 11 2M4 10a12 12 0 0 1 2-1.3M7 14a8 8 0 0 1 8-1M10 18a3 3 0 0 1 4 0"/>',calendar:'<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M8 3v4m8-4v4M4 11h16"/>'};return `<svg viewBox="0 0 24 24" aria-hidden="true">${paths[name]||paths.clock}</svg>`};
const mark='<svg class="mark" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 13a7 7 0 0 1 12-6l2 2M19 4v5h-5M19 11A7 7 0 0 1 7 17l-2-2M5 20v-5h5"/></svg>';
const header=()=>`<header><div class="brand">${mark}<span>${esc(M.product)}</span></div><span class="date">${dateLabel}</span></header>`;
const nav=title=>`<header class="nav-header"><button class="text-button" data-action="back">${icon('back')}<span>Back</span></button><span class="nav-title">${title}</span></header>`;
const footer=(status='Local preview')=>`<footer><span>All times in UTC</span><span>${status}</span></footer>`;
function roster(){return `<section class="section-top" aria-labelledby="roster-title"><div class="section-head"><h2 id="roster-title">Also on call</h2><small>Until · UTC</small></div><ul class="roster">${M.roster.filter(p=>p.name!==M.user).map(p=>`<li><span class="avatar" aria-hidden="true">${p.name.split(' ').map(n=>n[0]).join('')}</span><div class="person"><strong>${esc(p.name)}</strong><small>${esc(p.role)}</small></div><span class="until">${esc(p.until)}</span></li>`).join('')}</ul></section>`}
function hero(offline=false){const accepted=phase==='accepted'&&!offline;if(accepted)return `<section class="hero" aria-label="Current coverage"><p class="eyebrow">${esc(M.rotation)}</p><h1>Priya is on call</h1><p class="muted">${esc(M.handoverTo)}</p><div class="shift-time"><span>${nowLabel}–${M.shiftEnd} <small>UTC</small></span><small>Cover accepted</small></div><p class="caption space-top">${esc(M.user)} is off call.</p></section>`;return `<section class="hero" aria-label="${offline?'Last-known shift':'Your current shift'}"><p class="eyebrow">${esc(M.rotation)}</p><h1>${offline?'You were on call':accepted?'Priya is on call':'You’re on call'}</h1><p class="muted">${esc(accepted?M.handoverTo:M.user)}</p><div class="shift-time"><span>${M.shiftStart}–${M.shiftEnd} <small>UTC</small></span><small>${offline?'As of '+nowLabel:accepted?'Handed over':hoursLeft+'h remaining'}</small></div><div class="rail" aria-hidden="true"><div class="elapsed"></div></div><div class="rail-labels"><span>${M.shiftStart}</span><span>${nowLabel}${offline?' last saved':' now'}</span><span>${M.shiftEnd}</span></div></section>`}
function main(){return `${header()}<div class="content">${hero()}${phase==='pending'?'<p class="status-inline">Handover pending · You’re still responsible.</p>':''}${phase==='accepted'?'<p class="caption space-top">Your handover to Priya was accepted.</p>':`<button class="primary wide space-top" data-action="${phase==='pending'?'pending':'compose'}">${phase==='pending'?'View handover request':'Hand over shift'}<span aria-hidden="true">→</span></button>`}${roster()}</div>${footer()}`}
const summary=()=>`<div class="summary"><strong>${esc(M.rotation)}</strong><small>Today · ${M.shiftStart}–${M.shiftEnd} UTC</small></div>`;
function compose(){if(step==='review')return `${nav('Review handover')}<div class="content review"><h1>Ready to hand over?</h1><dl class="detail-list"><div><dt>From</dt><dd>${esc(M.user)} (you)</dd></div><div><dt>To</dt><dd>${esc(recipient||M.handoverTo)}</dd></div><div><dt>Rotation</dt><dd>${esc(M.rotation)}</dd></div><div><dt>Cover</dt><dd>Now–${M.shiftEnd} UTC</dd></div></dl>${note?`<p class="caption">Handover note</p><p class="note-display" tabindex="0" aria-label="Handover note">${esc(note)}</p>`:''}<div class="notice"><strong>You stay on call until Priya accepts.</strong>Sending a request does not transfer responsibility.</div><div class="actions"><button class="secondary" data-action="edit">Edit</button><button class="primary" data-action="send">Send request</button></div></div>${footer()}`;
return `${nav('Hand over shift')}<div class="content"><h1>Who’s taking over?</h1><p class="intro">Hand over the rest of your current shift.</p>${summary()}<form id="handover-form"><label for="recipient">Hand over to</label><select id="recipient" name="recipient" required><option value="">Choose a teammate…</option><option value="${esc(M.handoverTo)}" ${recipient?'selected':''}>${esc(M.handoverTo)}</option></select><div class="space-top"><label for="note">Handover note <span class="optional">(optional)</span></label><textarea id="note" name="note" maxlength="240" placeholder="Anything Priya should know?">${esc(note)}</textarea></div><p class="caption space-top">Cover from now until ${M.shiftEnd} UTC.</p><button class="primary wide section-top" id="review-button" type="submit" ${recipient?'':'disabled'}>Review handover <span aria-hidden="true">→</span></button></form></div>${footer()}`}
function pending(){return `${header()}<div class="content"><h1>Waiting for Priya</h1><p class="intro">Your handover request is pending.</p><div class="transfer"><div class="person"><strong>${esc(M.user)}</strong><small>You · on call</small></div><span class="arrow" aria-hidden="true">→</span><div class="person"><strong>${esc(M.handoverTo)}</strong><small>Awaiting acceptance</small></div></div><dl class="detail-list"><div><dt>Rotation</dt><dd>${esc(M.rotation)}</dd></div><div><dt>Requested cover</dt><dd>${nowLabel}–${M.shiftEnd} UTC</dd></div></dl><div class="notice"><strong>You’re still responsible.</strong>Stay on call until Priya accepts the handover.</div><button class="primary wide section-top" data-action="main">Back to schedule</button><button class="text-button wide space-top" data-action="cancel-request">Cancel request</button></div>${footer()}`}
function accepted(){return `${header()}<div class="content"><div class="state-icon success-icon">${icon('check')}</div><h1>Shift handed over</h1><p class="intro">Priya accepted your request.</p><div class="summary"><strong>${esc(M.handoverTo)} is now on call.</strong><small>${esc(M.rotation)} · Until ${M.shiftEnd} UTC</small></div><p>You’re no longer responsible for this shift.</p><button class="primary wide section-top" data-action="main">Back to schedule</button></div>${footer()}`}
function offline(){return `${header()}<div class="content offline"><h1>You’re offline</h1><p class="intro">Last saved ${dateLabel}, ${nowLabel} UTC. Current coverage may have changed.</p><div class="summary"><strong>${esc(M.user)} · You</strong><small>${esc(M.rotation)} · ${M.shiftStart}–${M.shiftEnd} UTC</small></div><p class="caption offline-status">${offlineChecked?'Still offline. Showing the saved schedule. Handovers are unavailable.':'Last-known coverage. Handovers are unavailable offline.'}</p>${roster()}<button class="secondary wide space-top" data-action="retry">Try again</button></div>${footer('Saved schedule')}`}
function empty(){return `${nav('Schedule')}<div class="content"><div class="empty"><div class="state-icon">${icon('calendar')}</div><h1>No schedule yet</h1><p>There’s no on-call schedule to show. Ask your rota administrator to add your team’s rotations.</p><button class="secondary wide" data-action="refresh">Refresh schedule</button>${emptyChecked?'<p class="caption" role="status">No schedule is available yet.</p>':''}</div></div>${footer()}`}
function url(){const u=new URL(location);u.searchParams.set('screen',state);if(phase)u.searchParams.set('handover',phase);else u.searchParams.delete('handover');if(state==='compose'&&step==='review')u.searchParams.set('step','review');else u.searchParams.delete('step');return u}
function render(focus=false){app.innerHTML=({main,compose,pending,accepted,offline,empty}[state])();if(focus){const target=app.querySelector('h1');target.tabIndex=-1;target.focus({preventScroll:true})}document.title=`Rota · ${state==='main'?'On-call schedule':state}`}
function go(next){state=next;history.pushState({},'',url());render(true)}
function announce(text){document.querySelector('#announcer').textContent=text}
app.addEventListener('change',e=>{if(e.target.id==='recipient'){recipient=e.target.value;document.querySelector('#review-button').disabled=!recipient}});
app.addEventListener('input',e=>{if(e.target.id==='note')note=e.target.value});
app.addEventListener('submit',e=>{e.preventDefault();if(!recipient)return;step='review';go('compose')});
app.addEventListener('click',e=>{const action=e.target.closest('[data-action]')?.dataset.action;if(!action)return;
if(action==='compose'){step='choose';go('compose')}
else if(action==='edit'){step='choose';go('compose');document.querySelector('#recipient').focus()}
else if(action==='send'){phase='pending';go('pending');announce('Request pending. You are still responsible until Priya accepts.')}
else if(action==='cancel-request'){phase='';step='choose';go('main');announce('Request cancelled. You remain on call.')}
else if(action==='back'){if(state==='compose'&&step==='review'){step='choose';go('compose')}else go('main')}
else if(action==='cancel')go('main');
else if(action==='retry'){offlineChecked=true;render();app.querySelector('[data-action="retry"]').focus();announce('Still offline. Showing the saved schedule.')}
else if(action==='refresh'){emptyChecked=true;render();app.querySelector('[data-action="refresh"]').focus()}
else if(states.includes(action))go(action);
});
window.addEventListener('popstate',()=>{const p=new URLSearchParams(location.search);state=states.includes(p.get('screen'))?p.get('screen'):'main';phase=state==='pending'?'pending':state==='accepted'?'accepted':p.get('handover')||'';step=p.get('step')==='review'?'review':'choose';render(true)});
window.addEventListener('keydown',e=>{if(e.key==='Escape'&&state!=='main'&&state!=='offline'){e.preventDefault();if(state==='compose'&&step==='review'){step='choose';go('compose')}else go('main')}});
// Only the separate offline review harness can explicitly simulate acceptance.
window.addEventListener('message',e=>{if(window.parent!==window&&e.source===window.parent&&e.data?.type==='rota:accept'&&phase==='pending'){phase='accepted';go('accepted');announce('Priya accepted. You are no longer responsible for this shift.')}});
render();
})();
