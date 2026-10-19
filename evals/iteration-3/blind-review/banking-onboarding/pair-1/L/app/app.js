(() => {
'use strict';
const bank = window.EVAL_FIXTURES.bank;
const app = document.getElementById('app');
const params = new URLSearchParams(location.search);
const preference = matchMedia('(prefers-color-scheme: dark)');
function setTheme(){document.documentElement.dataset.theme = ['light','dark'].includes(params.get('theme')) ? params.get('theme') : preference.matches ? 'dark' : 'light';}
setTheme(); preference.addEventListener('change',setTheme);
const stateNames = ['welcome','details','details-error','code','code-error','help','done'];
let current = stateNames.includes(params.get('screen')) ? params.get('screen') : 'welcome';
let customerName='', mobile='', code='';
let invalidName=false, invalidMobile=false, invalidCode=false;
const arrow = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 12h15m-6-6 6 6-6 6"/></svg>';
const shield = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M12 3 4 6v6c0 5 8 9 8 9s8-4 8-9V6z"/><path d="m8 12 3 3 5-6"/></svg>';
const check = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m5 12 4 4L19 6"/></svg>';
const phone = '<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="m7 3 3 5-3 3c2 3 3 4 6 6l3-3 5 3c-1 4-4 5-7 3C8 17 5 14 3 8 2 5 4 3 7 3Z"/></svg>';
const mark='<svg aria-hidden="true" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M3 25h26M7 24V14a9 9 0 0 1 18 0v10M12 24V14a4 4 0 0 1 8 0v10M3 29h26"/></svg>';
const illustration=`<div class="art" aria-hidden="true"><svg viewBox="0 0 340 108" fill="none"><path d="M24 101h292" stroke="var(--gold)"/><circle cx="244" cy="31" r="22" fill="var(--soft)"/><path d="M100 101V36l70-28 70 28v65" fill="var(--soft)" stroke="var(--fg)" stroke-width="1.4"/><path d="M93 38h154M103 44h134M109 48h122" stroke="var(--fg)" stroke-width="1.4"/><path d="M151 101V70a19 19 0 0 1 38 0v31" fill="var(--bg)" stroke="var(--fg)" stroke-width="1.4"/><path d="M170 51v50M183 79v6M116 57h22v27h-22zM202 57h22v27h-22zM127 57v27M213 57v27M116 70h22M202 70h22M94 101h152M89 106h162" stroke="var(--fg)" stroke-width="1.4"/><path d="M66 87c-13-4-14-15-10-20 8 1 13 7 10 20Zm0 0c13-4 16-15 11-20-8 1-12 8-11 20ZM66 90V74" fill="var(--soft)" stroke="var(--fg)" stroke-width="1.4"/><path d="m56 88 3 13h14l3-13zM268 88l3 13h14l3-13z" fill="var(--soft)" stroke="var(--fg)" stroke-width="1.4"/><path d="M278 88V64m0 13c-12-1-15-10-11-15 8 0 12 8 11 15Zm0 4c12-1 16-10 12-15-8 0-13 8-12 15Z" stroke="var(--fg)" stroke-width="1.4"/></svg></div>`;
function safe(value){return String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function progress(step,label){return `<div class="eyebrow"><span class="progress" aria-hidden="true">${[1,2,3].map(i=>`<i class="${i<=step?'active':''}"></i>`).join('')}</span><span>Step ${step} of 3 · ${label}</span></div>`;}
function safety(){return `<aside class="safety">${shield}<div><strong>Keep your code safe</strong>${bank.warning}</div></aside>`;}
function go(state){current=state;const u=new URL(location.href);u.searchParams.set('screen',state);history.pushState({screen:state},'',u);render(true);}
function render(moveFocus=false){
 const isHelp=current==='help';
 const screen=isHelp?'code':current;
 if(screen==='details-error'){invalidName=true;invalidMobile=true;if(!customerName)customerName='A';if(!mobile)mobile='077';}
 if(screen==='code-error')invalidCode=true;
 let content='';
 if(screen==='welcome')content=`${illustration}<h1 id="page-title" tabindex="-1">Your bank,<br>wherever you are.</h1><p class="intro">Let’s set up mobile banking.<br>We’ll take it one step at a time.</p><ol class="steps"><li><span class="step-number">1</span>Your details</li><li><span class="step-number">2</span>A code by text</li><li><span class="step-number">3</span>You’re ready</li></ol><button class="primary" id="start">Let’s get started ${arrow}</button><p class="next-note">You’ll need the mobile you use with us.</p>`;
 if(screen.startsWith('details'))content=`${progress(1,'Your details')}<h1 id="page-title" tabindex="-1">Let’s start with you.</h1><p class="intro">Use the details for your existing ${bank.name} account.</p>${invalidName||invalidMobile?'<div class="error-summary" role="alert">Please check the details below.</div>':''}<form id="details-form" novalidate><div class="field"><label for="full-name">Full name</label><input id="full-name" name="name" type="text" autocomplete="name" maxlength="100" value="${safe(customerName)}" aria-invalid="${invalidName}" aria-describedby="name-hint${invalidName?' name-error':''}"><p class="hint" id="name-hint">As it appears on your account.</p>${invalidName?'<p class="error" id="name-error">Enter your name as it appears on your account.</p>':''}</div><div class="field"><label for="mobile">Mobile number</label><input id="mobile" name="tel" type="tel" inputmode="tel" autocomplete="tel" maxlength="25" value="${safe(mobile)}" aria-invalid="${invalidMobile}" aria-describedby="mobile-hint${invalidMobile?' mobile-error':''}"><p class="hint" id="mobile-hint">The UK mobile number you use with us.</p>${invalidMobile?'<p class="error" id="mobile-error">Enter an 11-digit mobile number starting with 07, or use +44.</p>':''}</div><p class="before-action">Next, we’ll check your mobile with a code by text.</p><button class="primary" type="submit">Continue ${arrow}</button></form>`;
 if(screen.startsWith('code'))content=`${progress(2,'Check your mobile')}<h1 id="page-title" tabindex="-1">Check your<br>text messages.</h1><p class="intro">Enter the ${bank.codeLength}-digit code for your mobile ending <strong>${safe(mobile?mobile.replace(/\D/g,'').slice(-3):bank.mobileEnding)}</strong>.</p><form id="code-form" novalidate><div class="field"><label for="code">Text message code</label><input id="code" class="code-input" name="code" type="text" inputmode="numeric" pattern="[0-9]{${bank.codeLength}}" autocomplete="one-time-code" maxlength="${bank.codeLength}" value="${safe(code)}" aria-invalid="${invalidCode}" aria-describedby="code-hint${invalidCode?' code-error':''}"><p class="hint" id="code-hint">Enter all ${bank.codeLength} numbers.</p>${invalidCode?'<p class="error" id="code-error" role="alert">That code doesn’t match. Check your text and try again.</p>':''}</div>${safety()}<button class="primary" type="submit">Confirm code ${arrow}</button></form><button class="quiet change-number" id="change-number">Change mobile number</button><p class="prototype-note">This is a practice setup. No text message is sent.</p>`;
 if(screen==='done')content=`${progress(3,'Complete')}<div class="success-mark">${check}</div><h1 id="page-title" tabindex="-1">You’re all set.</h1><p class="intro">${safe(customerName||bank.customer)}, you’ve completed your mobile banking setup.</p><section class="account" aria-label="Your account"><h2>${bank.accountName}</h2><p class="account-label">Available balance</p><p class="balance">${bank.balance}</p><dl><div><dt>Sort code</dt><dd>${bank.sortCode}</dd></div><div><dt>Account number</dt><dd>${bank.accountNumber}</dd></div></dl></section><p>You can close this setup. Your branch is still here when you need us.</p><details><summary>Keep your banking safe</summary><p>${bank.warning}</p><p class="next-note">If you’re unsure, call us on <a href="tel:${bank.helpPhone.replace(/ /g,'')}">${bank.helpPhone}</a>.</p></details>`;
 app.innerHTML=`<header class="header"><div class="brand">${mark}<span>${bank.name}</span></div><button class="quiet" id="help-open"><span class="help-icon" aria-hidden="true">?</span>Help</button></header>${screen!=='welcome'?`<nav class="back-row" aria-label="Setup navigation"><button class="quiet" id="back"><svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="m14 6-6 6 6 6"/></svg>Back</button></nav>`:''}<main class="${screen==='welcome'?'welcome':''}" aria-labelledby="page-title">${content}</main><footer class="footer">Practice setup · Your account won’t change.</footer><dialog id="help-dialog" aria-labelledby="help-title" aria-describedby="help-description"><h2 id="help-title" tabindex="-1">A person, when<br>you need one.</h2><p id="help-description">Our team can help you with mobile banking, one step at a time.</p><a class="phone-link" href="tel:${bank.helpPhone.replace(/ /g,'')}">${phone}${bank.helpPhone}</a><p class="help-small">You can also ask for help at your branch.</p><p class="help-small">We’ll never ask you to tell us your text message code.</p><button class="primary" id="help-close">Back to setup</button></dialog>`;
 document.title=`${screen==='welcome'?'Welcome':screen.startsWith('details')?'Your details':screen==='done'?'Setup complete':'Check your mobile'} · ${bank.name}`;
 document.getElementById('start')?.addEventListener('click',()=>go('details'));
 document.getElementById('back')?.addEventListener('click',()=>{invalidName=false;invalidMobile=false;invalidCode=false;code='';go(screen.startsWith('details')?'welcome':screen==='done'?'code':'details');});
 document.getElementById('change-number')?.addEventListener('click',()=>{invalidCode=false;code='';go('details');});
 document.getElementById('details-form')?.addEventListener('submit',event=>{
 event.preventDefault();customerName=document.getElementById('full-name').value.trim();mobile=document.getElementById('mobile').value.trim();
 invalidName=!/^[\p{L}\p{M}][\p{L}\p{M}'’.\- ]+$/u.test(customerName)||(customerName.match(/[\p{L}]/gu)||[]).length<2;
 invalidMobile=!/^(07\d{9}|(?:\+44|0044)7\d{9})$/.test(mobile.replace(/[\s()\-]/g,''));
 if(invalidName||invalidMobile){current='details';render();document.getElementById(invalidName?'full-name':'mobile').focus();}else{invalidCode=false;code='';go('code');}
 });
 document.getElementById('code-form')?.addEventListener('submit',event=>{
 event.preventDefault();code=document.getElementById('code').value.trim();
 if(code!==bank.testCode){invalidCode=true;current='code';render();document.getElementById('code').focus();document.getElementById('code').select();}else{invalidCode=false;code='';go('done');}
 });
 // Inputs are remembered in memory only, including when Help opens.
 document.getElementById('full-name')?.addEventListener('input',e=>customerName=e.target.value);
 document.getElementById('mobile')?.addEventListener('input',e=>mobile=e.target.value);
 document.getElementById('code')?.addEventListener('input',e=>code=e.target.value);
 const dialog=document.getElementById('help-dialog');
 let returnFocus=null;
 function openHelp(){returnFocus=document.activeElement;dialog.showModal();document.getElementById('help-title').focus();}
 document.getElementById('help-open').addEventListener('click',openHelp);
 document.getElementById('help-close').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',()=>{if(isHelp){current='code';const u=new URL(location.href);u.searchParams.set('screen','code');history.replaceState({screen:'code'},'',u);} (returnFocus?.isConnected?returnFocus:document.getElementById('help-open')).focus();});
 if(moveFocus){window.scrollTo(0,0);document.getElementById('page-title').focus({preventScroll:true});}
 if(isHelp)openHelp();
}
window.addEventListener('popstate',()=>{const s=new URLSearchParams(location.search).get('screen');current=stateNames.includes(s)?s:'welcome';invalidName=false;invalidMobile=false;invalidCode=false;render(true);});
render();
})();
