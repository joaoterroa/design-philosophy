(() => {
'use strict';
const bank=window.EVAL_FIXTURES.bank;
const app=document.getElementById('app'),dialog=document.getElementById('help-dialog');
const arrow='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m9 5 7 7-7 7M4 12h12"/></svg>';
const backIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="m14 5-7 7 7 7M7 12h13"/></svg>';
const mark='<svg viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M6 7v12m20-12v12M3 23c4-5 9 5 13 0s9 5 13 0M3 28c4-5 9 5 13 0s9 5 13 0M6 11h20"/></svg>';
const branch='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="m3 8 9-5 9 5v2H3V8Zm2 5v6m7-6v6m7-6v6M3 22h18"/></svg>';
let state='welcome',returnState='code',helpReturn=null;
let data={name:'',mobile:'',code:''};
const escape=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const warning=()=>`<div class="safety"><strong>Keep your code private</strong>${escape(bank.warning)}</div>`;
const button=(text)=>`<button class="primary" type="submit">${text}${arrow}</button>`;
function url(screen,replace=false){const u=new URL(location.href);u.searchParams.set('screen',screen);history[replace?'replaceState':'pushState']({},'',u);}
function save(){for(const key of ['name','mobile','code']){const el=document.getElementById(key);if(el)data[key]=el.value;}}
function navigate(next,push=true){save();if(dialog.open)dialog.close();state=next;if(push)url(next);render();window.scrollTo(0,0);document.querySelector('h1').focus();}
function render(){
 const isDetails=state.startsWith('details'),isCode=state.startsWith('code');
 app.innerHTML=`<header><div class="brand">${mark}<span>${escape(bank.name)}</span></div><button class="help-button" id="open-help" type="button">Help <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M9.5 9a2.5 2.5 0 0 1 5 0c0 2-2.5 2-2.5 4m0 3v.5"/></svg></button></header><main id="main">${state==='welcome'?welcome():isDetails?details():isCode?code():done()}</main><footer><p>Practice setup · No account changes</p></footer>`;
 document.getElementById('open-help').onclick=openHelp;
 document.getElementById('back')?.addEventListener('click',()=>navigate(isCode?'details':'welcome'));
 document.getElementById('start')?.addEventListener('click',()=>navigate('details'));
 document.getElementById('details-form')?.addEventListener('submit',submitDetails);
 document.getElementById('code-form')?.addEventListener('submit',submitCode);
 document.getElementById('no-code')?.addEventListener('click',openHelp);
 document.getElementById('finish')?.addEventListener('click',()=>{data={name:'',mobile:'',code:''};navigate('welcome');});
}
function welcome(){return `<h1 class="hero-title" tabindex="-1">Your bank.<br>At your pace.</h1><p class="intro">Set up mobile banking in two simple steps. We’re here if you need a hand.</p><ol class="journey"><li><span class="number" aria-hidden="true">1</span><div><strong>Your details</strong><p>Name and mobile number</p></div></li><li><span class="number" aria-hidden="true">2</span><div><strong>A text message</strong><p>A code to check it’s you</p></div></li></ol><button class="primary" id="start">Set up the app ${arrow}</button><div class="branch-note">${branch}<p>You can still visit us in branch.</p></div>`;}
function back(){return `<button class="back" id="back" type="button">${backIcon}Back</button>`;}
function details(){const err=state==='details-error';return `${back()}<p class="eyebrow">Step 1 of 2 · Your details</p><h1 tabindex="-1">Let’s start with you.</h1><p class="intro">Use the details you gave us in branch.</p><form class="form" id="details-form" novalidate><div class="field"><label for="name">Full name</label><input id="name" name="name" maxlength="100" autocomplete="name" autocapitalize="words" value="${escape(data.name)}" aria-describedby="name-error" ${err?'aria-invalid="true"':''}><p class="field-error" aria-live="polite" id="name-error">${err?'Enter your full name, as it appears on your account.':''}</p></div><div class="field"><label for="mobile">Mobile phone number</label><input id="mobile" name="mobile" type="tel" inputmode="tel" autocomplete="tel" value="${escape(data.mobile)}" aria-describedby="mobile-hint mobile-error" ${err?'aria-invalid="true"':''}><p class="hint" id="mobile-hint">The UK mobile number registered with us.</p><p class="field-error" aria-live="polite" id="mobile-error">${err?'Enter an 11-digit mobile number starting with 07, or use +44.':''}</p></div>${button('Continue')}</form>`;}
function code(){const err=state==='code-error';const digits=data.mobile.replace(/\D/g,'');const ending=digits?digits.slice(-3):bank.mobileEnding;return `${back()}<p class="eyebrow">Step 2 of 2 · Check your mobile</p><h1 tabindex="-1">Check your text messages.</h1><p class="intro">Enter the ${bank.codeLength}-digit code for your mobile number ending <strong>${escape(ending)}</strong>.</p><p class="practice">This practice setup does not send a text.</p><form class="form" id="code-form" novalidate><div class="field"><label for="code">${bank.codeLength}-digit code</label><input class="code-input" id="code" name="code" type="text" inputmode="numeric" autocomplete="one-time-code" maxlength="${bank.codeLength}" value="${escape(data.code)}" aria-describedby="code-error safety-text" ${err?'aria-invalid="true"':''}><p class="field-error" aria-live="polite" id="code-error">${err?'That code doesn’t match. Check the code and try again.':''}</p></div><div id="safety-text">${warning()}</div>${button('Confirm code')}<button class="text-button" type="button" id="no-code">I haven’t received a code</button></form>`;}
function done(){return `<div class="complete-mark"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="m5 12 4 4L19 6"/></svg></div><p class="eyebrow">Setup complete</p><h1 tabindex="-1">You’re ready, ${escape((data.name||bank.customer).split(' ')[0])}.</h1><p class="intro">That’s the end of your practice setup. You haven’t opened or changed a bank account.</p><div class="next"><strong>Your branch is still here for you.</strong><p>When you use the real app, you can bank on your mobile and keep visiting us in person.</p></div><button class="secondary" id="finish">Finish practice</button>`;}
function fieldError(id,message){const input=document.getElementById(id);input.setAttribute('aria-invalid',String(!!message));document.getElementById(id+'-error').textContent=message;}
function submitDetails(e){e.preventDefault();save();const nameOK=/\p{L}/u.test(data.name.trim());const mobileOK=/^(07\d{9}|447\d{9})$/.test(data.mobile.replace(/[\s()+-]/g,''));fieldError('name',nameOK?'':'Enter your full name, as it appears on your account.');fieldError('mobile',mobileOK?'':'Enter an 11-digit mobile number starting with 07, or use +44.');if(!nameOK||!mobileOK){state='details-error';url(state,true);document.getElementById(!nameOK?'name':'mobile').focus();return;}data.name=data.name.trim();navigate('code');}
function submitCode(e){e.preventDefault();save();if(data.code.trim()!==bank.testCode){state='code-error';url(state,true);fieldError('code',new RegExp('^\\d{'+bank.codeLength+'}$').test(data.code)?'That code doesn’t match. Check the code and try again.':`Enter the ${bank.codeLength}-digit code, using numbers only.`);document.getElementById('code').focus();document.getElementById('code').select();return;}navigate('done');}
function openHelp(){save();returnState=state;helpReturn=document.activeElement;url('help',true);dialog.showModal();document.getElementById('help-title').focus();}
function closeHelp(){dialog.close();url(returnState,true);(helpReturn?.isConnected?helpReturn:document.getElementById('open-help')).focus();}
 document.getElementById('help-phone').textContent=bank.helpPhone;
 document.getElementById('call-help').href='tel:'+bank.helpPhone.replace(/\s/g,'');

 document.getElementById('close-help').onclick=closeHelp;
 dialog.addEventListener('cancel',e=>{e.preventDefault();closeHelp();});
 dialog.addEventListener('keydown',e=>{
  if(e.key!=='Tab')return;
  const first=document.getElementById('call-help'),last=document.getElementById('close-help');
  if(e.shiftKey&&(document.activeElement===first||document.activeElement===document.getElementById('help-title'))){e.preventDefault();last.focus();}
  else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first.focus();}
 });
function load(){let requested=new URLSearchParams(location.search).get('screen')||'welcome';const allowed=['welcome','details','details-error','code','code-error','help','done'];if(!allowed.includes(requested))requested='welcome';state=requested==='help'?'code':requested;render();if(requested==='help'){returnState='code';helpReturn=document.getElementById('open-help');dialog.showModal();document.getElementById('help-title').focus();}}
window.addEventListener('popstate',()=>{save();if(dialog.open)dialog.close();load();document.querySelector('h1').focus();});
const preference=matchMedia('(prefers-color-scheme: dark)');preference.addEventListener('change',e=>{if(!['light','dark'].includes(new URLSearchParams(location.search).get('theme')))document.documentElement.dataset.theme=e.matches?'dark':'light';});
load();
})();
