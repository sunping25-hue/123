/* The same six-stage interaction serves both language versions. Auto presentation is opt-in. */
(()=>{
 const section=document.querySelector('#biz-process-demo');if(!section)return;
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
})();
