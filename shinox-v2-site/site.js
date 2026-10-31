'use strict';
const APPS_SCRIPT_URL='https://script.google.com/macros/s/AKfycbyIHCL_KxWtDzHB02x0GkkPNAT-rOIi9NbXa6eNyrFvhrFdwITomHPNDqVSYoVbj2G5ow/exec';
const menuButton=document.querySelector('.toggle'),nav=document.querySelector('#nav');
function closeMenu(){nav.classList.remove('open');menuButton.setAttribute('aria-expanded','false');menuButton.setAttribute('aria-label','開啟導覽選單')}
menuButton.addEventListener('click',()=>{const open=nav.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));menuButton.setAttribute('aria-label',open?'關閉導覽選單':'開啟導覽選單')});
nav.querySelectorAll('a').forEach(a=>a.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&nav.classList.contains('open')){closeMenu();menuButton.focus()}});
const tabs=[...document.querySelectorAll('[role="tab"]')];function selectTab(tab){tabs.forEach(t=>{const active=t===tab;t.setAttribute('aria-selected',String(active));t.tabIndex=active?0:-1;document.getElementById(t.getAttribute('aria-controls')).hidden=!active})}
tabs.forEach((tab,i)=>{tab.addEventListener('click',()=>selectTab(tab));tab.addEventListener('keydown',e=>{let next;if(e.key==='ArrowRight')next=(i+1)%tabs.length;if(e.key==='ArrowLeft')next=(i+tabs.length-1)%tabs.length;if(e.key==='Home')next=0;if(e.key==='End')next=tabs.length-1;if(next!==undefined){e.preventDefault();selectTab(tabs[next]);tabs[next].focus()}})});
const form=document.querySelector('#inquiry-form');
if(form){
  const fields=form.querySelector('#inquiry-fields'),notice=document.querySelector('#form-runtime'),result=form.querySelector('#form-result'),submit=form.querySelector('.submit');
  const english=document.documentElement.lang.startsWith('en');
  const consent=form.elements.consent,confirmedAt=form.elements.consentConfirmedAt,policyVersion=form.elements.privacyPolicyVersion;
  const modeButtons=[...document.querySelectorAll('[data-form-mode]')];
  let formMode='lead',available=true,submitting=false;
  const failure=english?'Submission failed. Please contact us via LINE @shinox or call +886 979-666-302.':'送出失敗，請改用 LINE @shinox 或來電 0979-666-302';

  // Only this Google Sheets route is available independently of the local API.
  fields.disabled=false;
  submit.textContent=english?'Send enquiry ↗':'送出洽詢 ↗';
  if(notice)notice.textContent=english?'Enquiries are sent to Google Sheets. Visit times require separate confirmation.':'洽詢資料將送至 Google 試算表，參觀時段仍需專人確認。';
  consent.checked=false;
  confirmedAt.value='';
  consent.addEventListener('change',()=>{confirmedAt.value=consent.checked?new Date().toISOString():''});
  form.addEventListener('reset',()=>{confirmedAt.value=''});
  function selectMode(mode){
    formMode=mode==='booking'?'booking':'lead';
    modeButtons.forEach(button=>{const active=button.dataset.formMode===formMode;button.classList.toggle('active',active);button.setAttribute('aria-pressed',String(active))});
    form.querySelector('#booking-fields').hidden=formMode!=='booking';
    result.textContent='';
  }
  modeButtons.forEach(button=>button.addEventListener('click',()=>selectMode(button.dataset.formMode)));

  form.addEventListener('submit',async event=>{
    event.preventDefault();
    if(!available||submitting||!form.reportValidity()||!consent.checked)return;
    const values=new FormData(form),read=name=>String(values.get(name)||'').trim();
    if(read('website')){result.textContent=failure;return;}
    if(!confirmedAt.value)confirmedAt.value=new Date().toISOString();
    const data={
      name:read('name'),phone:read('phone'),email:read('email'),region:read('region'),
      hasSite:read('hasSite'),model:read('subject'),message:read('message'),
      description:read('description')||read('message'),
      location:formMode==='booking'?read('location'):'',
      preferredDate:formMode==='booking'?read('preferredDate'):'',
      preferredTime:formMode==='booking'?read('preferredTime'):'',
      consent:consent.checked,consentConfirmedAt:confirmedAt.value,
      privacyPolicyVersion:policyVersion.value,website:read('website'),
      formType:formMode,lang:document.documentElement.lang,page:location.pathname
    };
    submitting=true;
    submit.disabled=true;
    submit.setAttribute('aria-busy','true');
    result.textContent=english?'Submitting…':'正在送出…';
    try{
      // A no-cors response is opaque: delivery cannot confirm a saved spreadsheet row.
      await fetch(APPS_SCRIPT_URL,{method:'POST',mode:'no-cors',headers:{'Content-Type':'text/plain;charset=utf-8'},body:JSON.stringify(data)});
      form.reset();
      selectMode('lead');
      result.textContent=english?'Thank you, we have received your enquiry and will contact you soon.':'已收到，我們會盡快與您聯繫';
    }catch(error){
      result.textContent=failure;
    }finally{
      submitting=false;
      submit.disabled=false;
      submit.removeAttribute('aria-busy');
    }
  });
}
