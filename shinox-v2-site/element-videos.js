/* User-provided element clips. Only the selected, visible clip can autoplay. */
(() => {
 const section=document.querySelector('#technology');if(!section)return;
 const clips=[...section.querySelectorAll('.element-video')];
 const motion=matchMedia('(prefers-reduced-motion: reduce)');
 const connection=navigator.connection;
 const limited=()=>connection&&(connection.saveData||['slow-2g','2g'].includes(connection.effectiveType));
 let visible=false;const stopped=new WeakSet();
 function sync(video){const button=video.parentElement.querySelector('.element-playback');button.textContent=video.paused?'播放動畫 ▷':'暫停動畫 Ⅱ';button.setAttribute('aria-label',(video.paused?'播放':'暫停')+video.getAttribute('aria-label'))}
 function play(video){if(video.error)video.load();if(!video.getAttribute('src'))video.src=video.dataset.elementSrc;video.muted=true;video.play().catch(()=>sync(video))}
 function update(){clips.forEach(video=>{const selected=!video.closest('[role="tabpanel"]').hidden;if(selected&&visible&&!document.hidden&&!motion.matches&&!limited()&&!stopped.has(video)){play(video)}else video.pause()})}
 clips.forEach(video=>{
  video.muted=true;video.defaultMuted=true;video.loop=true;video.playsInline=true;
  video.addEventListener('play',()=>sync(video));video.addEventListener('pause',()=>sync(video));
  video.addEventListener('error',()=>{stopped.add(video);sync(video)});
  video.parentElement.querySelector('.element-playback').addEventListener('click',()=>{if(video.paused){stopped.delete(video);play(video)}else{stopped.add(video);video.pause()}});
 });
 new IntersectionObserver(entries=>{visible=entries[0].isIntersecting&&entries[0].intersectionRatio>0;update()},{threshold:0.05}).observe(section);
 new MutationObserver(update).observe(section,{subtree:true,attributes:true,attributeFilter:['hidden']});
 document.addEventListener('visibilitychange',update);motion.addEventListener('change',update);
})();
