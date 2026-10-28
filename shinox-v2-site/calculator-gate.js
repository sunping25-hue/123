'use strict';
/* Footer calculator links are visible sitewide. Client-side password prompt is a
   marketing gate only; destination sites need their own server-side access control. */
(()=>{
 if(document.documentElement.dataset.shinoxCalcLoaded)return;
 document.documentElement.dataset.shinoxCalcLoaded='1';
 const base=location.pathname.includes('/products/')?'../':'';
 const allowed=[
  {name:'自助洗車場投資獲利試算',url:'https://shinox.ai.studio'},
  {name:'水刀洗車店投資獲利試算',url:'https://service-carwasher-360.ai.studio'}
 ];
 const footer=document.querySelector('footer');
 if(!footer)return;
 const block=document.createElement('div');
 block.className='footer-calculators';
 block.innerHTML='<div class="footer-calculators-label">投資獲利試算工具</div><div class="footer-calculators-buttons"></div>';
 const group=block.querySelector('.footer-calculators-buttons');
 allowed.forEach(item=>{
   const a=document.createElement('a');a.href=item.url;a.textContent=item.name+' ↗';
   a.dataset.calculatorUrl=item.url;a.dataset.calculatorTitle=item.name;group.append(a);
 });
 footer.append(block);
 const dialog=document.createElement('dialog');
 dialog.className='calculator-dialog';
 dialog.innerHTML='<form class="calculator-dialog-panel"><button type="button" class="calculator-close" aria-label="關閉">×</button><p class="calculator-eyebrow">SHINOX / INVESTMENT TOOLS</p><h2>請聯絡業務索取密碼登入</h2><p class="calculator-destination-label"></p><label for="calculator-password">登入密碼</label><input id="calculator-password" type="password" required autocomplete="off" placeholder="請輸入密碼"/><p role="alert" aria-live="polite" class="calculator-error"></p><button type="submit" class="calculator-submit">確認登入 ↗</button><a class="calculator-contact" href="'+base+'contact.html">聯絡業務索取密碼 ↗</a><small>此為網站入口驗證，無法取代試算網站本身的存取權限。</small></form>';
 document.body.append(dialog);
 const form=dialog.querySelector('form'),input=form.querySelector('input'),error=dialog.querySelector('.calculator-error');
 let target='';
 function close(){dialog.close();input.value='';error.textContent=''}
 dialog.querySelector('.calculator-close').addEventListener('click',close);
 dialog.addEventListener('click',e=>{if(e.target===dialog)close()});
 document.addEventListener('click',e=>{
  const a=e.target.closest('[data-calculator-url]');
  if(!a||!allowed.some(v=>v.url===a.dataset.calculatorUrl))return;
  e.preventDefault();target=a.dataset.calculatorUrl;dialog.querySelector('.calculator-destination-label').textContent=a.dataset.calculatorTitle;
  error.textContent='';input.value='';if(!dialog.open)dialog.showModal();input.focus();
 });
 form.addEventListener('submit',async e=>{
  e.preventDefault();
  if(!crypto?.subtle){error.textContent='請使用支援安全驗證的最新版瀏覽器';return}
  const bytes=new TextEncoder().encode(input.value);
  const d=await crypto.subtle.digest('SHA-256',bytes);
  const hash=Array.from(new Uint8Array(d),b=>b.toString(16).padStart(2,'0')).join('');
  if(hash!=='6f47ec7e8dc1ee807d732e52523f39809208d0997eb943fa9ac733e9cfa5693b'){
    error.textContent='密碼不正確，請聯絡業務';input.select();return
  }
  const url=target;close();location.assign(url);
 });
})();
