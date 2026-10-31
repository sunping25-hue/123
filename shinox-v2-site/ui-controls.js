/* One control language across static pages and dynamically created dialogs. */
(()=>{
 const groups=[
  ['ui-primary','.btn.primary,.button.primary,.head-contact,.header-contact,.campaign-popup-cta,.calculator-submit,button[type="submit"]'],
  ['ui-tab','.element-tabs [role="tab"],.form-tabs button,.board-filters button'],
  ['ui-nav','.nav a,.site-header nav a,.header nav a'],
  ['ui-secondary','.btn:not(.primary),.button:not(.primary),.board-pill,.text-link,.footer-calculators-buttons a'],
  ['ui-functional','.toggle,.menu-toggle,.calculator-close,.campaign-popup-close,.campaign-popup-later,.video-control,.back,.calculator-contact,.language,.product-language,.language-switch a'],
  ['ui-investment','.investment-tool'],
  ['ui-inline','.contact-phone,.contact-email,.email']
 ];
 const cards='.shinox-category-visual,.product-item,.mini-product,.products-section .product,.related-grid>a';
 const cardActions='.shinox-pill-link,.product-item>span,.mini-product .mini-arrow,.products-section .product>span,.related-grid>a>span';
 function arrow(el){
  if(el.matches('.ui-arrow')||el.closest('svg'))return;
  for(const node of [...el.childNodes]){
   if(node.nodeType===Node.TEXT_NODE){const found=node.textContent.match(/([↗→↑])\s*$/);if(!found)continue;const at=node.textContent.lastIndexOf(found[1]);const tail=document.createElement('span');tail.className='ui-arrow';tail.setAttribute('aria-hidden','true');tail.textContent=found[1];node.textContent=node.textContent.slice(0,at);node.after(tail)}
   else if(node.nodeType===Node.ELEMENT_NODE&&!node.matches('svg,.ui-arrow,.whatsapp-symbol,.line-mark'))arrow(node);
  }
 }
 function vectorArrow(el){
  const direction=el.textContent.trim();if(el.querySelector('svg')||!['↗','→','↑','←'].includes(direction))return;
  const paths={'↗':'M4 14 14 4M4 4h10v10','→':'M3 9h12M10 4l5 5-5 5','↑':'M9 15V3M4 8l5-5 5 5','←':'M15 9H3M8 4 3 9l5 5'};
  el.innerHTML='<svg aria-hidden="true" focusable="false" viewBox="0 0 18 18" width="18" height="18" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="'+paths[direction]+'"/></svg>';
 }
 function match(root,selector){return [...(root.matches?.(selector)?[root]:[]),...root.querySelectorAll(selector)]}
 function enhance(root){
  groups.forEach(([kind,selector])=>match(root,selector).forEach(el=>{
   if(el.classList.contains('ui-control'))return;
   el.classList.add('ui-control',kind);
   if(el.matches('.text-link'))el.classList.add('ui-text');
   if(el.matches('.calculator-close,.campaign-popup-close'))el.classList.add('ui-close');
   if(el.matches('.footer-calculators-buttons a'))el.classList.add('ui-tool-small');
   arrow(el);
  }));
  match(root,'button:not(.line-float):not(.whatsapp-float)').forEach(el=>{if(!el.classList.contains('ui-control'))el.classList.add('ui-control','ui-functional')});
  match(root,cards).forEach(el=>el.classList.add('ui-card-hover'));
  match(root,cardActions).forEach(el=>{el.classList.add('ui-card-action');arrow(el)});
  match(root,'.ui-control,.line-label').forEach(arrow);
  match(root,'.ui-arrow').forEach(vectorArrow);
 }
 enhance(document);
 new MutationObserver(entries=>entries.forEach(entry=>entry.addedNodes.forEach(node=>{if(node.nodeType===Node.ELEMENT_NODE)enhance(node)}))).observe(document.body,{childList:true,subtree:true});
 const back=document.createElement('button');back.type='button';back.className='ui-backtop ui-control ui-functional';back.setAttribute('aria-label',document.documentElement.lang.startsWith('en')?'Back to top':'返回頂部');back.innerHTML='<span class="ui-arrow" aria-hidden="true">↑</span>';back.hidden=true;document.body.append(back);
 let scheduled=false;
 const update=()=>{back.hidden=scrollY<600;scheduled=false};
 window.addEventListener('scroll',()=>{if(!scheduled){scheduled=true;requestAnimationFrame(update)}},{passive:true});update();
 back.addEventListener('click',()=>{
  const title=document.querySelector('h1');if(title){const had=title.hasAttribute('tabindex');if(!had)title.tabIndex=-1;title.focus({preventScroll:true});if(!had)title.addEventListener('blur',()=>title.removeAttribute('tabindex'),{once:true})}
  window.scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
 });
})();
