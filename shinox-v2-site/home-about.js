/* Homepage 02: progressive reveals and bounded, event-driven image parallax. */
(()=>{
 const section=document.querySelector('#about.home-about-visual');if(!section)return;
 const motion=matchMedia('(prefers-reduced-motion: reduce)'),fine=matchMedia('(hover:hover) and (pointer:fine)'),wide=matchMedia('(min-width:901px)');
 const blocks=[...section.querySelectorAll('.home-about-reveal')],image=section.querySelector('.home-about-parallax'),cards=[...section.querySelectorAll('.home-about-card')];let active=false,frame=0;
 cards.forEach((card,i)=>card.style.setProperty('--about-delay',i*90+'ms'));
 section.dataset.aboutMotion=motion.matches?'off':'on';
 if('IntersectionObserver' in window){
  const reveal=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-revealed');reveal.unobserve(entry.target)}}),{threshold:.12});
  blocks.forEach(block=>reveal.observe(block));
  new IntersectionObserver(entries=>{active=entries[0].isIntersecting;if(active)schedule()},{threshold:0}).observe(section);
 }else{blocks.forEach(block=>block.classList.add('is-revealed'));active=true}
 function update(){frame=0;if(motion.matches||!fine.matches||!wide.matches||document.hidden){image.style.setProperty('--about-parallax','0px');return}const r=section.getBoundingClientRect(),offset=Math.max(-6,Math.min(6,((innerHeight/2-r.top-r.height/2)/innerHeight)*10));image.style.setProperty('--about-parallax',offset.toFixed(2)+'px')}
 function schedule(){if(active&&!frame)frame=requestAnimationFrame(update)}
 addEventListener('scroll',schedule,{passive:true});addEventListener('resize',schedule,{passive:true});
 function preference(){section.dataset.aboutMotion=motion.matches?'off':'on';if(motion.matches)blocks.forEach(block=>block.classList.add('is-revealed'));update()}
 motion.addEventListener('change',preference);fine.addEventListener('change',update);wide.addEventListener('change',update);document.addEventListener('visibilitychange',()=>{if(!document.hidden)schedule()});preference();
})();
