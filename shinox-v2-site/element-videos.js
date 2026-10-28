/* Play the selected visible clip and rotate Metal → Energy → Air → Water → Fluid every 6s. */
(() => {
 const section=document.querySelector('#technology');if(!section)return;
 const clips=[...section.querySelectorAll('.element-video')];
 const tabs=[...section.querySelectorAll('[role="tab"]')];
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 const connection=navigator.connection;
 const limited=()=>connection&&(connection.saveData||['slow-2g','2g'].includes(connection.effectiveType));
 let visible=false,timer=null;
 const keyboardFocus=()=>section.contains(document.activeElement)&&document.activeElement.matches(':focus-visible');
 function update(){
  const active=visible&&!document.hidden&&!motion.matches&&!limited();
  clips.forEach(video=>{
   const selected=!video.closest('[role="tabpanel"]').hidden;
   if(selected&&active){
    if(!video.getAttribute('src'))video.src=video.dataset.elementSrc;
    video.play().catch(()=>{});
   }else video.pause();
  });
  clearTimeout(timer);timer=null;
  if(active&&tabs.length>1&&!keyboardFocus())timer=setTimeout(()=>{
   const current=tabs.findIndex(tab=>tab.getAttribute('aria-selected')==='true');
   tabs[(current+1)%tabs.length].click();
  },6000);
 }
 clips.forEach(video=>{video.muted=true;video.defaultMuted=true;video.loop=true;video.playsInline=true});
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting&&entries[0].intersectionRatio>0;update()},{threshold:0.05}).observe(section);
 // Manual selection also starts a fresh six-second interval, including reselecting a tab.
 tabs.forEach(tab=>tab.addEventListener('click',update));
 new MutationObserver(update).observe(section,{subtree:true,attributes:true,attributeFilter:['hidden']});
 section.addEventListener('focusin',()=>queueMicrotask(update));
 section.addEventListener('focusout',()=>queueMicrotask(update));
 document.addEventListener('visibilitychange',update);motion.addEventListener('change',update);
 connection?.addEventListener?.('change',update);
})();
