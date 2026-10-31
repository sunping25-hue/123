/* One accessible process component, shared content and independent instance state. */
(()=>{
 const original=document.querySelector('#biz-process-demo');if(!original)return;
 document.querySelectorAll('[data-biz-process-mount]').forEach(target=>{
  const clone=original.cloneNode(true),prefix=target.dataset.bizProcessMount+'-';
  clone.id='biz-process-'+target.dataset.bizProcessMount;clone.classList.add('biz-process-compact');
  clone.querySelectorAll('.biz-process-intro,.biz-process-videos').forEach(el=>el.remove());
  clone.querySelectorAll('[id]').forEach(el=>el.id=prefix+el.id);
  [clone,...clone.querySelectorAll('*')].forEach(el=>{
   ['aria-controls','aria-labelledby','aria-describedby'].forEach(attr=>{
    if(el.hasAttribute(attr))el.setAttribute(attr,el.getAttribute(attr).split(/\s+/).map(id=>prefix+id).join(' '));
   });
  });
  const oldTitle=clone.querySelector('h2'),title=document.createElement('h3');
  for(const attr of oldTitle.attributes)title.setAttribute(attr.name,attr.value);
  title.classList.add('biz-process-title');title.textContent=oldTitle.textContent;oldTitle.replaceWith(title);
  const hint='點選階段查看介紹，依 01–06 順序了解建場流程。';
  clone.querySelector('.biz-process-status').textContent=window.ShinoXLocale?.t(hint)||hint;
  target.replaceChildren(clone);
 });
 function mount(section){
 const tabs=[...section.querySelectorAll('[role=tab]')],panels=[...section.querySelectorAll('[role=tabpanel]')],track=section.querySelector('.biz-process-scroller');
 const previous=section.querySelector('[data-biz-previous]'),next=section.querySelector('[data-biz-next]'),auto=section.querySelector('[data-biz-auto]'),live=section.querySelector('.biz-process-panels');
 const motion=matchMedia('(prefers-reduced-motion: reduce)');let current=0,playing=false,visible=false,timer=null;
 function schedule(){clearTimeout(timer);timer=null;const focused=section.querySelector('[role=tablist]').contains(document.activeElement)&&document.activeElement.matches(':focus-visible');if(playing&&visible&&!document.hidden&&!focused)timer=setTimeout(()=>select((current+1)%tabs.length,false),6000)}
 function select(index,focus=false){
  current=index;tabs.forEach((tab,i)=>{const selected=i===current;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;panels[i].hidden=!selected});previous.disabled=current===0;next.disabled=current===tabs.length-1;
  if(track.scrollWidth>track.clientWidth){const tab=tabs[current];track.scrollTo({left:tab.offsetLeft-(track.clientWidth-tab.offsetWidth)/2,behavior:motion.matches?'instant':'smooth'})}
  if(focus)tabs[current].focus();schedule();
 }
 tabs.forEach((tab,i)=>{
  tab.addEventListener('click',()=>select(i));
  tab.addEventListener('keydown',event=>{let index;if(event.key==='ArrowRight')index=(i+1)%tabs.length;if(event.key==='ArrowLeft')index=(i+tabs.length-1)%tabs.length;if(event.key==='Home')index=0;if(event.key==='End')index=tabs.length-1;if(index!==undefined){event.preventDefault();select(index,true)}});
 });
 previous.addEventListener('click',()=>select(Math.max(0,current-1)));next.addEventListener('click',()=>select(Math.min(tabs.length-1,current+1)));
 auto.addEventListener('click',()=>{playing=!playing;auto.setAttribute('aria-pressed',String(playing));auto.querySelector('span').textContent=window.ShinoXLocale?.t(playing?'停止自動展示':'自動展示')||(playing?'停止自動展示':'自動展示');live.setAttribute('aria-live',playing?'off':'polite');schedule()});
 section.addEventListener('focusin',()=>queueMicrotask(schedule));section.addEventListener('focusout',()=>queueMicrotask(schedule));
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;schedule()},{threshold:0}).observe(section);
 document.addEventListener('visibilitychange',schedule);
 motion.addEventListener('change',()=>{if(motion.matches&&playing)auto.click();schedule()});
 select(0);
 }
 [original,...document.querySelectorAll('.biz-process-compact')].forEach(mount);
})();
