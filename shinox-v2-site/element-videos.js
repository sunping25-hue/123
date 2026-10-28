/* Only the selected, visible user-provided element clip plays. */
(() => {
 const section=document.querySelector('#technology');if(!section)return;
 const clips=[...section.querySelectorAll('.element-video')];
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 const connection=navigator.connection;
 const limited=()=>connection&&(connection.saveData||['slow-2g','2g'].includes(connection.effectiveType));
 let visible=false;
 function update(){clips.forEach(video=>{
  const selected=!video.closest('[role="tabpanel"]').hidden;
  if(selected&&visible&&!document.hidden&&!motion.matches&&!limited()){
   if(!video.getAttribute('src'))video.src=video.dataset.elementSrc;
   video.play().catch(()=>{});
  }else video.pause();
 })}
 clips.forEach(video=>{video.muted=true;video.defaultMuted=true;video.loop=true;video.playsInline=true});
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting&&entries[0].intersectionRatio>0;update()},{threshold:0.05}).observe(section);
 new MutationObserver(update).observe(section,{subtree:true,attributes:true,attributeFilter:['hidden']});
 document.addEventListener('visibilitychange',update);motion.addEventListener('change',update);
})();
