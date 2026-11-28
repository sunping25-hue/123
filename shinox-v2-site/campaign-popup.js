/* Monthly advertisements are independent of calculator login. */
(()=>{
 const c=window.SHINOX_CAMPAIGN;if(!c?.enabled||!c.title||!c.image)return;
 const isEnglish=(document.documentElement.lang||'').toLowerCase().startsWith('en');
 const copy={...c,...(isEnglish?c.locales?.en:{})};
 const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Asia/Taipei',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
 if(c.startDate&&today<c.startDate||c.endDate&&today>c.endDate)return;
 const key='shinox-campaign-seen-'+(c.id||'default');
 try{if(c.frequency!=='always'&&sessionStorage.getItem(key)==='1')return}catch(_){}
 function safeUrl(value){try{const u=new URL(value,location.href);return ['https:','http:'].includes(u.protocol)?u.href:null}catch(_){return null}}
 const image=safeUrl(c.image);if(!image)return;
 const dialog=document.createElement('dialog');dialog.className='campaign-popup';dialog.setAttribute('aria-labelledby','campaign-title');
 if(c.variant==='product-launch')dialog.classList.add('campaign-popup--product-launch');
 const descriptionId=typeof c.descriptionId==='string'&&c.descriptionId&&!/\s/.test(c.descriptionId)?c.descriptionId:'campaign-description';
 dialog.setAttribute('aria-describedby',descriptionId);
 const inner=document.createElement('div');inner.className='campaign-popup-inner';
 const close=document.createElement('button');close.type='button';close.className='campaign-popup-close';close.setAttribute('aria-label',isEnglish?'Close advertisement':'關閉活動視窗');close.textContent='×';
 const heading=document.createElement('h2');heading.id='campaign-title';heading.textContent=copy.title;
 const desc=document.createElement('p');desc.id=descriptionId;desc.textContent=copy.description||'';
 const img=document.createElement('img');img.src=image;img.alt=copy.imageAlt||copy.title;img.width=Number.isInteger(c.imageWidth)&&c.imageWidth>0?c.imageWidth:1920;img.height=Number.isInteger(c.imageHeight)&&c.imageHeight>0?c.imageHeight:1094;
 inner.append(close,img,heading,desc);
 const cta=safeUrl(c.ctaUrl);if(cta){const a=document.createElement('a');a.className='campaign-popup-cta';a.href=cta;a.textContent=copy.ctaText||(isEnglish?'Learn more':'了解活動');inner.append(a)}
 const later=document.createElement('button');later.type='button';later.className='campaign-popup-later';later.textContent=isEnglish?'Later':'稍後再看';inner.append(later);
 dialog.append(inner);document.body.append(dialog);let previous=null;
 function dismiss(){dialog.close();if(previous?.isConnected)previous.focus()}
 close.addEventListener('click',dismiss);later.addEventListener('click',dismiss);dialog.addEventListener('click',e=>{if(e.target===dialog)dismiss()});
 dialog.addEventListener('keydown',e=>{
  if(e.key!=='Tab')return;
  const buttons=[...dialog.querySelectorAll('button:not([disabled]),a[href]')].filter(node=>node.getClientRects().length);
  const first=buttons[0],last=buttons[buttons.length-1];if(!first)return;
  if(e.shiftKey&&(document.activeElement===first||!dialog.contains(document.activeElement))){e.preventDefault();last.focus()}
  else if(!e.shiftKey&&(document.activeElement===last||!dialog.contains(document.activeElement))){e.preventDefault();first.focus()}
 });
 dialog.addEventListener('cancel',()=>{if(previous?.isConnected)setTimeout(()=>previous.focus(),0)});
 function show(){if(document.hidden){document.addEventListener('visibilitychange',()=>{if(!document.hidden)show()},{once:true});return}if(dialog.open)return;previous=document.activeElement;dialog.showModal();close.focus();try{sessionStorage.setItem(key,'1')}catch(_){}}
 // Do not wait for video downloads or window.load before showing the entrance ad.
 requestAnimationFrame(show);
})();
