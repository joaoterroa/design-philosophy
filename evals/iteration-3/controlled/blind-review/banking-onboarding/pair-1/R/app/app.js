'use strict';
const bank=window.EVAL_FIXTURES.bank;
document.title=bank.name+' · Mobile banking setup';
const app=document.querySelector('#app');
const params=new URLSearchParams(location.search);
const known=['welcome','details','details-error','code','code-error','help','done'];
let state=known.includes(params.get('screen'))?params.get('screen'):'welcome';
let person={name:'',mobile:''};
let codeValue='';
let fieldErrors={};
let returnState='code';
let helpTrigger=null;
const escapeHTML=v=>String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const arrow='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14m-6-6 6 6-6 6"/></svg>';
const backArrow='<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 6-6 6 6 6"/></svg>';
function syncURL(next,replace=false){const u=new URL(location.href);u.searchParams.set('screen',next);history[replace?'replaceState':'pushState']({screen:next},'',u);}
function go(next){state=next;syncURL(next);render(true);window.scrollTo(0,0);}
function warning(){return `<aside class="safety" aria-label="Keep your code safe"><strong>Keep your code safe</strong><p>${escapeHTML(bank.warning)}</p></aside>`;}
function saveFields(){const n=document.querySelector('#full-name'),m=document.querySelector('#mobile'),c=document.querySelector('#security-code');if(n)person.name=n.value;if(m)person.mobile=m.value;if(c)codeValue=c.value;}
function render(focus=false){
 const isHelp=state==='help';const current=isHelp?'code':state;
 const isDetails=current.startsWith('details');const isCode=current.startsWith('code');
 const step=isDetails?'Step 1 of 3':isCode?'Step 2 of 3':current==='done'?'Step 3 of 3':'';
 app.innerHTML=`<header><div class="brand"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="M5 23V15a11 11 0 0 1 22 0v8M10 23v-8a6 6 0 0 1 12 0v8M3 27h26"/></svg><span>${escapeHTML(bank.name)}</span></div><button class="help-button" id="help-button" type="button">Help</button></header>${step?`<nav aria-label="Setup progress">${current==='done'?'<span></span>':`<button type="button" class="back" id="back">${backArrow}Back</button>`}<span class="progress">${step}</span></nav>`:''}<main class="${current==='welcome'?'welcome':''}" id="main">${content(current)}</main><footer><p>Practice setup · no account changes</p></footer><dialog id="help-dialog" aria-labelledby="help-title" aria-describedby="help-description"><div class="dialog-heading"><h2 id="help-title" tabindex="-1">Talk to a person</h2></div><div class="help-content" tabindex="0" role="region" aria-label="Help information"><p id="help-description">Our team can help you set up mobile banking, one step at a time.</p><a class="primary phone" href="tel:${bank.helpPhone.replace(/\s/g,'')}">Call ${escapeHTML(bank.helpPhone)}</a><p class="note">Opens your phone’s calling app. You can also visit your usual branch.</p>${warning()}</div><div class="dialog-actions"><button class="secondary" id="close-help" type="button">Back to setup</button></div></dialog>`;
 document.querySelector('#help-button').addEventListener('click',openHelp);
 document.querySelector('#back')?.addEventListener('click',()=>{saveFields();go(isCode?'details':'welcome');});
 document.querySelector('#start')?.addEventListener('click',()=>go('details'));
 document.querySelector('#details-form')?.addEventListener('submit',submitDetails);
 document.querySelector('#code-form')?.addEventListener('submit',submitCode);
 document.querySelector('#code-help')?.addEventListener('click',openHelp);
 document.querySelector('#finish')?.addEventListener('click',()=>{person={name:'',mobile:''};codeValue='';fieldErrors={};go('welcome');});
 const dialog=document.querySelector('#help-dialog');
 document.querySelector('#close-help').addEventListener('click',()=>dialog.close());
 dialog.addEventListener('close',closeHelp);
 dialog.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const items=[...dialog.querySelectorAll('[tabindex="0"],a[href],button')];const first=items[0],last=items[items.length-1];if(e.shiftKey&&(document.activeElement===first||document.activeElement===document.querySelector('#help-title'))){e.preventDefault();last.focus();}else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}});
 if(isHelp){returnState='code';helpTrigger=document.querySelector('#help-button');dialog.showModal();document.querySelector('#help-title').focus();}
 else if(focus)document.querySelector('h1').focus();
}
function content(current){
 if(current==='welcome')return `<p class="eyebrow">WELCOME TO MOBILE BANKING</p><h1 tabindex="-1">Banking, at<br>your own pace.</h1><p class="lead">Let’s get you set up.<br>Your branch is still here for you.</p><ol class="steps" aria-label="Your setup steps"><li><span class="step-number" aria-hidden="true">1</span>Your name and mobile</li><li><span class="step-number" aria-hidden="true">2</span>A security code</li><li><span class="step-number" aria-hidden="true">3</span>You’re ready</li></ol><button class="primary" type="button" id="start">Get started ${arrow}</button><p class="note">Have your mobile phone with you.<br>There’s no need to rush.</p>`;
 if(current.startsWith('details')){
 const errors=current==='details-error'?fieldErrors:{};
 const nameError=errors.name||'';const mobileError=errors.mobile||'';
 return `<h1 tabindex="-1">First, your details</h1><p>Use the name and mobile number you gave the bank.</p>${Object.keys(errors).length?'<div class="error-summary" role="alert"><p>Please check your details below.</p></div>':''}<form id="details-form" novalidate><div class="field"><label for="full-name">Full name</label><input id="full-name" name="name" autocomplete="name" autocapitalize="words" value="${escapeHTML(person.name)}" aria-invalid="${!!nameError}" ${nameError?'aria-describedby="name-error"':''} required>${nameError?`<p class="error" id="name-error">${nameError}</p>`:''}</div><div class="field"><label for="mobile">Mobile number</label><input id="mobile" name="tel" type="tel" inputmode="tel" autocomplete="tel" value="${escapeHTML(person.mobile)}" aria-invalid="${!!mobileError}" aria-describedby="mobile-hint${mobileError?' mobile-error':''}" required><p class="hint" id="mobile-hint">UK number, starting with 07 or +44.</p>${mobileError?`<p class="error" id="mobile-error">${mobileError}</p>`:''}</div><button class="primary form-action" type="submit">Continue ${arrow}</button><p class="note">Next: confirm your mobile number with a security code.</p></form>`;
 }
 if(current.startsWith('code')){
 const ending=person.mobile?person.mobile.replace(/\D/g,'').slice(-3):bank.mobileEnding;
 return `<h1 tabindex="-1">Check your mobile</h1><p class="destination">Enter your ${bank.codeLength}-digit security code.<br>Mobile number ending <strong>${escapeHTML(ending)}</strong>.</p><form id="code-form" novalidate><label for="security-code">Security code</label><input class="code-input" id="security-code" name="code" inputmode="numeric" autocomplete="one-time-code" pattern="[0-9]{${bank.codeLength}}" maxlength="${bank.codeLength}" value="${escapeHTML(codeValue)}" aria-invalid="${current==='code-error'}" aria-describedby="code-hint${current==='code-error'?' code-error':''}" required><p class="hint" id="code-hint">${bank.codeLength} numbers, with no spaces.</p>${current==='code-error'?`<p class="error" id="code-error" role="alert">That code doesn’t match. Check all ${bank.codeLength} numbers and try again.</p>`:''}<button class="primary form-action" type="submit">Confirm code ${arrow}</button></form><button class="text-action" type="button" id="code-help">Haven’t received a code?</button>${warning()}<p class="note">In this practice setup, no text is sent.</p>`;
 }
 return `<div class="success-mark"><svg viewBox="0 0 32 32" aria-hidden="true"><path d="m7 16 6 6L25 9"/></svg></div><h1 tabindex="-1">You’re all set.</h1><p class="lead">A new way to bank.<br>The same support behind you.</p><div class="done-list"><p>You’ve completed this practice setup. Your account has not changed.</p><p>Whenever you need a hand, use Help or visit your branch.</p></div><button class="primary" type="button" id="finish">Finish ${arrow}</button>`;
}
function submitDetails(e){e.preventDefault();saveFields();fieldErrors={};if((person.name.match(/\p{L}/gu)||[]).length<2||/\d/.test(person.name))fieldErrors.name='Enter the name on your account.';let m=person.mobile.replace(/[\s()-]/g,'').replace(/^0044/,'+44');if(!/^(07\d{9}|\+447\d{9})$/.test(m))fieldErrors.mobile='Enter a UK mobile number with 11 digits, or use +44.';if(Object.keys(fieldErrors).length){go('details-error');document.querySelector(fieldErrors.name?'#full-name':'#mobile').focus();}else{codeValue='';go('code');}}
function submitCode(e){e.preventDefault();saveFields();if(codeValue===bank.testCode){codeValue='';go('done');}else{go('code-error');document.querySelector('#security-code').focus();}}
function openHelp(e){saveFields();returnState=state;helpTrigger=e.currentTarget;state='help';syncURL('help');document.querySelector('#help-dialog').showModal();document.querySelector('#help-title').focus();}
function closeHelp(){state=returnState;syncURL(state,true);helpTrigger?.focus();}
window.addEventListener('popstate',()=>{state=new URLSearchParams(location.search).get('screen')||'welcome';render(true);});
if(state==='details-error')fieldErrors={name:'Enter the name on your account.',mobile:'Enter a UK mobile number with 11 digits, or use +44.'};
render();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change',e=>{if(!['light','dark'].includes(new URLSearchParams(location.search).get('theme')))document.documentElement.dataset.theme=e.matches?'dark':'light';});
