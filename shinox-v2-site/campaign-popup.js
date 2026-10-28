'use strict';
(()=>{
 const c=window.SHINOX_CAMPAIGN;
 if(!c?.enabled||!c.title||!c.image)return;
 const now=new Date();if(c.startDate&&now<new Date(c.startDate))return;
 if(c.endDate&&now>new Date(c.endDate))return;
 const key='shinox-campaign-seen-'+(c.id||'default');
 try{if(sessionStorage.getItem(key)==='1')return}catch(_){}
 const dialog=document.createElement('dialog');dialog.className='campaign-popup';dialog.setAttribute('aria-label',c.title);
 const inner=document.createElement('div');inner.className='campaign-popup-inner';
 const close=document.createElement('button');close.type='button';close.className='campaign-popup-close';close.setAttribute('aria-label','關閉本月活動');close.textContent='×';
 const heading=document.createElement('h2');heading.textContent=c.title;
 const desc=document.createElement('p');desc.textContent=c.description||'';
 const img=document.createElement('img');img.src=c.image;img.alt=c.imageAlt||c.title;img.loading='eager';
 inner.append(close,img,heading,desc);
 if(c.ctaUrl&&/^https?:\/\//i.test(c.ctaUrl)){const a=document.createElement('a');a.className='campaign-popup-cta';a.href=c.ctaUrl;a.textContent=c.ctaText||'了解活動';a.rel='noopener noreferrer';inner.append(a)}
 dialog.append(inner);document.body.append(dialog);
 function dismiss(){if(dialog.open)dialog.close();try{sessionStorage.setItem(key,'1')}catch(_){}}
 close.addEventListener('click',dismiss);
 dialog.addEventListener('cancel',()=>{try{sessionStorage.setItem(key,'1')}catch(_){}});
 dialog.addEventListener('click',e=>{if(e.target===dialog)dismiss()});
 window.addEventListener('load',()=>dialog.showModal(),{once:true});
})();
