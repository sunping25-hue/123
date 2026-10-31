/* The owner's contact animation replaces only the homepage contact artwork. */
(()=>{
 const video=document.querySelector('.contact-background video');if(!video)return;
 const section=video.closest('#contact'),motion=matchMedia('(prefers-reduced-motion: reduce)'),connection=navigator.connection;
 let visible=false;
 function update(){
  const limited=connection&&(connection.saveData||['slow-2g','2g'].includes(connection.effectiveType));
  if(visible&&!document.hidden&&!motion.matches&&!limited){
   if(!video.getAttribute('src'))video.src=video.dataset.contactSrc;
   video.play().catch(()=>{});
  }else video.pause();
 }
 video.muted=true;video.defaultMuted=true;video.loop=true;video.playsInline=true;
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;update()},{threshold:0}).observe(section);
 document.addEventListener('visibilitychange',update);motion.addEventListener('change',update);connection?.addEventListener?.('change',update);
})();
