/* Fine-pointer interactions; no replacement of approved videos or layouts. */
(()=>{
 const hero=document.querySelector('.hero');if(!hero)return;
 const motion=matchMedia('(prefers-reduced-motion: reduce)'),pointer=matchMedia('(hover: hover) and (pointer: fine)');
 const cards=[...document.querySelectorAll('.shinox-category-visual,.product-item,.products-section .product')];
 const targets=[hero,...cards];const pending=new Map();let frame=0;
 const enabled=()=>pointer.matches&&!motion.matches;
 function flush(){pending.forEach((position,el)=>{el.style.setProperty('--pointer-x',position.x+'%');el.style.setProperty('--pointer-y',position.y+'%');el.style.setProperty('--tilt-x',position.tx+'deg');el.style.setProperty('--tilt-y',position.ty+'deg');if(el===hero){el.style.setProperty('--hero-x',position.hx+'px');el.style.setProperty('--hero-y',position.hy+'px')}});pending.clear();frame=0}
 function schedule(el,position){pending.set(el,position);if(!frame)frame=requestAnimationFrame(flush)}
 function reset(el){schedule(el,{x:50,y:50,tx:0,ty:0,hx:0,hy:0})}
 targets.forEach(el=>{let rect;el.classList.add(el===hero?'pointer-hero':'pointer-tilt');el.addEventListener('pointerenter',()=>{rect=el.getBoundingClientRect()});el.addEventListener('pointermove',event=>{if(!enabled()||event.pointerType==='touch')return;rect=rect||el.getBoundingClientRect();const x=Math.max(0,Math.min(1,(event.clientX-rect.left)/rect.width)),y=Math.max(0,Math.min(1,(event.clientY-rect.top)/rect.height));schedule(el,{x:x*100,y:y*100,tx:(.5-y)*6,ty:(x-.5)*8,hx:(x-.5)*14,hy:(y-.5)*10})},{passive:true});el.addEventListener('pointerleave',()=>{rect=null;reset(el)})});
 document.querySelectorAll('.element-tabs [role="tab"]').forEach(tab=>tab.addEventListener('pointerenter',()=>{if(enabled())tab.click()}));
 motion.addEventListener('change',()=>targets.forEach(reset));pointer.addEventListener('change',()=>targets.forEach(reset));window.addEventListener('blur',()=>targets.forEach(reset));
})();
