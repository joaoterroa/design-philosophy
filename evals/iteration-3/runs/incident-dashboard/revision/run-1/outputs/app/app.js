'use strict';
const fixture = window.EVAL_FIXTURES.dashboard;
const params = new URLSearchParams(location.search);
const screen = ['live','stale','surge'].includes(params.get('screen')) ? params.get('screen') : 'live';
const isTV = document.documentElement.dataset.display === 'tv';
const stale = screen === 'stale';
const incidents = fixture.incidents.slice(0, screen === 'surge' ? fixture.surgeCount : fixture.openCount);
const pageSize = isTV ? 7 : incidents.length;
let currentPage = 0;
let returnFocus = null;
const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const severityCount = n => incidents.filter(i => i.severity === n).length;
const app = document.querySelector('#app');
app.classList.toggle('stale',stale);
app.innerHTML = `
<a class="skip" href="#open-incidents">Skip to open incidents</a>
<header class="topbar"><div class="brand"><svg class="compass" viewBox="0 0 28 28" fill="none" aria-hidden="true"><path d="M14 1 24 26 14 20 4 26 14 1Z" stroke="currentColor" stroke-width="1.8"/><path d="M14 3v17M8 21l6-11 6 11" stroke="currentColor" stroke-width="1.5"/></svg><span>Northwind</span><span class="product-name">Operations / Incidents</span></div><div class="header-right"><span class="date">${esc(fixture.displayDate)}</span><time>${esc(fixture.displayTime)} UTC</time></div></header>
<main>
<div class="page-heading"><div><p class="eyebrow">Operations room</p><h1>Incident overview</h1></div><div class="snapshot"><span class="snapshot-mark" aria-hidden="true"></span><span><span class="snapshot-label">${stale?'Data is stale':'Current snapshot'}</span><br><span class="muted">As of ${stale?esc(fixture.staleAsOf):esc(fixture.displayTime)} UTC</span></span></div></div>
${stale?`<div class="stale-banner" role="status"><strong>Updates unavailable.</strong><span>Showing the last-known snapshot from ${esc(fixture.staleAsOf)} UTC. Counts, durations and on-call details may have changed.</span></div>`:''}
<section class="metrics" aria-label="Incident metrics${stale?', last known at '+fixture.staleAsOf+' UTC':''}">
<div class="metric open-metric"><div class="metric-value">${incidents.length}</div><div><div class="metric-label">Open incidents</div><div class="severity-summary"><span>${severityCount(1)} SEV1</span><span>${severityCount(2)} SEV2</span><span>${severityCount(3)} SEV3</span></div><div class="metric-note">${screen==='surge'?(fixture.surgeCount-fixture.openCount)+' more than the standard snapshot':'+2 vs yesterday'}</div></div></div>
<div class="metric"><div class="metric-label">MTTR <span class="muted">/ 7 days</span></div><div class="metric-value">${esc(fixture.mttr)}</div><div class="metric-note good">↘ ${esc(fixture.mttrChange)} vs last week</div></div>
<div class="metric"><div class="metric-label">Pages today</div><div class="metric-value">${fixture.pages}</div><div class="metric-note">+${fixture.pagesDelta} vs yesterday</div></div>
<div class="metric"><div class="metric-label">SLO budget left</div><div class="metric-value">${esc(fixture.slo)}</div><div class="metric-note">↘ ${esc(fixture.sloChange)}</div></div>
</section>
<div class="content-grid"><div class="incident-column"><section aria-labelledby="open-incidents"><div class="section-head"><div><h2 id="open-incidents" tabindex="-1">Open incidents <span class="count">${incidents.length}</span></h2><p>Investigating, mitigated and monitoring · ordered by severity</p></div></div><div class="incidents-panel"><div class="table-wrap"><table class="incident-table" aria-labelledby="open-incidents"><caption hidden>Open incidents with severity, service, status, incident commander and duration. Select a title for full details, including opened time.</caption><colgroup><col class="severity-col"><col><col class="state-col"><col class="owner-col"><col class="duration-col"></colgroup><thead><tr><th scope="col">Severity</th><th scope="col">Incident / service</th><th scope="col">Status</th><th scope="col">Commander</th><th scope="col">Duration</th></tr></thead><tbody id="incident-rows"></tbody></table></div><div class="table-footer"><span id="range" aria-live="polite"></span><div class="pagination" ${incidents.length<=pageSize?'hidden':''}><button id="previous" aria-label="Previous incident page">← Previous</button><span id="page-label" class="mono"></span><button id="next" aria-label="Next incident page">Next →</button></div><span id="all-shown" ${incidents.length>pageSize?'hidden':''}>All open incidents shown</span></div></div></section>
<section class="resolved-section" aria-labelledby="resolved-title"><div class="resolved-heading"><h2 id="resolved-title">Recently resolved <span class="count">${fixture.resolved.length}</span></h2><span>Separate from open count</span></div><div class="resolved-list">${fixture.resolved.map(i=>`<article class="resolved-item"><h3>${esc(i.title)}</h3><p class="resolved-meta"><span class="mono">${esc(i.id)}</span> · SEV${i.severity} · ${esc(i.status)}<br>${esc(i.service)} · Opened ${esc(i.opened)} · Duration <span class="duration">${esc(i.duration)}</span></p></article>`).join('')}</div></section></div>
<aside class="sidebar" aria-label="On-call coverage and service history"><section class="side-panel"><div class="panel-top"><h2>${stale?'On call at '+esc(fixture.staleAsOf):'On call now'}</h2><span>Until ${esc(fixture.until)}</span></div><dl class="roster"><div><dt>Primary</dt><dd>${esc(fixture.primary)}</dd></div><div><dt>Secondary</dt><dd>${esc(fixture.secondary)}</dd></div></dl><div class="commander-warning"><span>Incident commander</span><strong>Unassigned</strong></div></section>
<section class="side-panel"><div class="panel-top"><h2>Incidents by service</h2><span>30 days</span></div><ul class="service-list">${fixture.services.map(s=>`<li><div class="service-label"><span>${esc(s.name)}</span><strong>${s.value}</strong></div><div class="bar-track" aria-hidden="true"><div class="bar-fill" style="--value:${s.value/Math.max(...fixture.services.map(s=>s.value))*100}%"></div></div></li>`).join('')}</ul><p class="service-footnote">${fixture.services.reduce((sum,s)=>sum+s.value,0)} incidents across 5 services</p></section></aside></div>
<footer class="footer"><span>${stale?'Last-known':'Local'} snapshot · No live monitoring connection</span><span>All times UTC · Durations as recorded</span></footer>
</main>
<dialog id="incident-dialog" aria-labelledby="detail-title" aria-describedby="detail-note"><div class="dialog-top"><span id="detail-id" class="mono muted"></span><button class="dialog-close" id="close-detail">Close <span aria-hidden="true">×</span></button></div><h2 id="detail-title"></h2><dl class="detail-grid" id="detail-fields"></dl><p class="dialog-note" id="detail-note">${stale?'Last-known data from '+esc(fixture.staleAsOf)+' UTC. Details may have changed.':'Snapshot details. Durations are shown as recorded.'}</p></dialog>`;
function renderRows(){
 const start=currentPage*pageSize;
 document.querySelector('#incident-rows').innerHTML=incidents.slice(start,start+pageSize).map(i=>`<tr class="${i.severity===1?'critical-row':''}"><td><span class="severity sev${i.severity}">SEV${i.severity}</span></td><td><button class="incident-link" data-incident="${esc(i.id)}" aria-label="View ${esc(i.id)}: ${esc(i.title)}"><span class="incident-title">${esc(i.title)}</span><span class="incident-meta"><span class="mono">${esc(i.id)}</span> ${esc(i.service)} · Opened ${esc(i.opened)}</span></button></td><td>${esc(i.status)}</td><td class="${i.commander?'':'owner-missing'}">${esc(i.commander || 'Unassigned')}</td><td class="duration">${esc(i.duration)}</td></tr>`).join('');
 document.querySelector('#range').textContent=`Showing ${start+1}–${Math.min(start+pageSize,incidents.length)} of ${incidents.length}${incidents.length>Math.min(start+pageSize,incidents.length)?' · '+(incidents.length-Math.min(start+pageSize,incidents.length))+' more after this page':''}`;
 const previous=document.querySelector('#previous'),next=document.querySelector('#next');
 // aria-disabled keeps keyboard focus on the button after a page change.
 previous.setAttribute('aria-disabled',String(currentPage===0));next.setAttribute('aria-disabled',String((currentPage+1)*pageSize>=incidents.length));
 document.querySelector('#page-label').textContent=`${currentPage+1} / ${Math.ceil(incidents.length/pageSize)}`;
}
renderRows();
document.querySelector('#previous').addEventListener('click',()=>{if(currentPage>0){currentPage--;renderRows();}});
document.querySelector('#next').addEventListener('click',()=>{if((currentPage+1)*pageSize<incidents.length){currentPage++;renderRows();}});
const dialog=document.querySelector('#incident-dialog');
document.querySelector('#incident-rows').addEventListener('click',event=>{
 const button=event.target.closest('[data-incident]');if(!button)return;
 const i=incidents.find(i=>i.id===button.dataset.incident);returnFocus=button;
 document.querySelector('#detail-id').textContent=i.id;
 document.querySelector('#detail-title').textContent=i.title;
 const fields=[['Service',i.service],['Severity','SEV'+i.severity],['Status',i.status],['Commander',i.commander||'Unassigned'],['Opened',i.opened+' UTC'],['Duration',i.duration]];
 document.querySelector('#detail-fields').innerHTML=fields.map(([label,value])=>`<div><dt>${label}</dt><dd class="${label==='Commander'&&!i.commander?'owner-missing':''}">${esc(value)}</dd></div>`).join('');dialog.showModal();
});
document.querySelector('#close-detail').addEventListener('click',()=>dialog.close());
dialog.addEventListener('keydown',event=>{
 if(event.key==='Tab'){event.preventDefault();document.querySelector('#close-detail').focus();}
});
dialog.addEventListener('close',()=>{if(returnFocus?.isConnected)returnFocus.focus();});
const systemTheme=matchMedia('(prefers-color-scheme: dark)');
systemTheme.addEventListener('change',event=>{if(!['light','dark'].includes(params.get('theme')))document.documentElement.dataset.theme=event.matches?'dark':'light';});
