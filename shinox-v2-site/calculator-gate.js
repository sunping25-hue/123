'use strict';
/**
 * ShinoX calculator link gate.
 * IMPORTANT: This is only a client-side convenience check, NOT access control.
 * The destination tools themselves must enforce server-side authentication if protected data exists.
 */
(()=> {
 const links=[...document.querySelectorAll('[data-calculator-url]')];
 if(!links.length)return;
 const allowed=new Set(['https://shinox.ai.studio','https://service-carwasher-360.ai.studio']);
 const sha256='6f47ec7e8dc1ee807d732e52523f39809208d0997eb943fa9ac733e9cfa5693b';
 const modal=document.createElement('dialog');
 modal.className='calculator-dialog';
 modal.setAttribute('aria-labelledby','calculator-dialog-title');
 modal.innerHTML='<form method="dialog" class="calculator-dialog-panel"><button type="button" class="calculator-close" aria-label="關閉登入視窗">×</button><p class="eyebrow">SHINOX / INVESTMENT CALCULATOR</p><h2 id="calculator-dialog-title">試算工具登入</h2><p class="calculator-dialog-prompt">請聯絡業務索取密碼登入</p><p id="calculator-destination-label" class="calculator-destination-label"></p><label for="calculator-password">登入密碼</label><input id="calculator-password" type="password" required autocomplete="off" placeholder="請輸入密碼" /><p class="calculator-error" role="alert" aria-live="polite"></p><div class="calculator-actions"><button type="submit" class="btn primary">登入並開啟試算 ↗</button><a href="contact.html" class="btn">聯絡業務索取密碼</a></div><p class="calculator-security-note">此為網站入口驗證，試算資料的存取權限由試算網站本身管理。</p></form>';
 document.body.append(modal);
 const close=modal.querySelector('.calculator-close'),form=modal.querySelector('form'),password=modal.querySelector('input'),error=modal.querySelector('.calculator-error'),destination=modal.querySelector('.calculator-destination-label');
 let current='';
 function hide(){modal.close();password.value='';error.textContent=''}
 close.addEventListener('click',hide);
 modal.addEventListener('click',e=>{if(e.target===modal)hide()});
 links.forEach(link=>link.addEventListener('click',e=>{
  e.preventDefault();const target=link.dataset.calculatorUrl;
  if(!allowed.has(target))return;
  current=target;destination.textContent=link.dataset.calculatorTitle||'投資獲利試算';
  error.textContent='';password.value='';
  modal.showModal();password.focus();
 }));
 form.addEventListener('submit',async e=>{
  e.preventDefault();
  if(!window.crypto?.subtle){error.textContent='此瀏覽器不支援密碼驗證，請使用最新版瀏覽器。';return}
  try{
   const digest=await crypto.subtle.digest('SHA-256',new TextEncoder().encode(password.value));
   const hex=[...new Uint8Array(digest)].map(x=>x.toString(16).padStart(2,'0')).join('');
   if(hex!==sha256){error.textContent='密碼不正確，請聯絡業務確認。';password.select();return}
   const url=current;hide();window.location.assign(url);
  }catch(err){error.textContent='驗證失敗，請重新嘗試。'}
 });
})();
