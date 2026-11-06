/* One official-channel component. Never infer a product video from the channel URL. */
(()=>{
 const official='https://www.youtube.com/@ShinoXwash';
 const t=value=>window.ShinoXLocale?.t(value)||value;
 const icon='<svg class="youtube-icon" aria-hidden="true" focusable="false" viewBox="0 0 28 20"><rect width="28" height="20" rx="5.5" fill="#FF0033"/><path d="m11 5.5 8 4.5-8 4.5Z" fill="#fff"/></svg>';
 function decorate(a,label){
  a.classList.add('ui-youtube','ui-control','ui-secondary');a.target='_blank';a.rel='noopener noreferrer';a.removeAttribute('style');
  a.setAttribute('aria-label',t(label)+' '+t('（另開新分頁）'));
  a.innerHTML=icon+'<span class="youtube-label"></span><span class="ui-arrow" aria-hidden="true">↗</span>';a.querySelector('.youtube-label').textContent=t(label);return a;
 }
 function make(label,url=official){const a=document.createElement('a');a.href=url;return decorate(a,label)}
 const footer=document.querySelector('footer');
 if(footer){
  const matches=[...footer.querySelectorAll('a[href]')].filter(a=>{try{const u=new URL(a.href);return ['youtube.com','www.youtube.com'].includes(u.hostname)&&u.pathname.replace(/\/$/,'').toLowerCase()==='/@shinoxwash'}catch(_){return false}});
  let link=matches[0];matches.slice(1).forEach(a=>a.remove());
  if(link)decorate(link,'ShinoX 官方 YouTube 頻道');
  else{const wrap=document.createElement('div');wrap.className='shinox-youtube-footer';link=make('ShinoX 官方 YouTube 頻道');wrap.append(link);footer.append(wrap)}
  link.dataset.shinoxYoutube='official-channel';
 }
 function verified(record){
  if(!record?.verified||!record.source)return null;
  try{const u=new URL(record.url);if(u.protocol!=='https:')return null;if(u.hostname==='youtu.be'&&/^\/[A-Za-z0-9_-]{11}$/.test(u.pathname))return u.href;if(['youtube.com','www.youtube.com'].includes(u.hostname)&&((u.pathname==='/watch'&&/^[A-Za-z0-9_-]{11}$/.test(u.searchParams.get('v')||''))||/^\/(shorts|embed)\/[A-Za-z0-9_-]{11}$/.test(u.pathname)))return u.href}catch(_){}return null;
 }
 const registry=window.SHINOX_CONFIRMED_PRODUCT_VIDEOS||{},product=location.pathname.match(/\/products\/([^/]+)\.html$/)?.[1];
 if(product){const url=verified(registry[product]),actions=document.querySelector('.product-hero .actions');if(url&&actions&&!actions.querySelector('[data-product-video]')){const a=make('觀看實機影片',url);a.dataset.productVideo=product;actions.append(a)}}
 document.querySelectorAll('.board-product').forEach(card=>{const product=card.querySelector('a[href*="products/"]')?.getAttribute('href').match(/products\/([^/]+)\.html/)?.[1],url=verified(registry[product]);if(url&&!card.querySelector('[data-product-video]')){const a=make('觀看實機影片',url);a.dataset.productVideo=product;a.classList.add('product-video-action');card.lastElementChild.append(a)}});
})();
