/* Restrained 05/06 motion; no scroll loop, no motion outside the viewport. */
(()=>{
 const sections=[...document.querySelectorAll('#news.home-editorial-story,#cases.home-editorial-story')];if(!sections.length)return;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)'),visible=new Set();
 function activity(){sections.forEach(section=>{section.dataset.editorialActive=String(visible.has(section)&&!document.hidden&&!reduced.matches)})}
 function preference(){sections.forEach(section=>{section.dataset.editorialMotion=reduced.matches?'off':'on';if(reduced.matches)section.classList.add('is-revealed')});activity()}
 if('IntersectionObserver' in window){
  const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(entry.isIntersecting){entry.target.classList.add('is-revealed');visible.add(entry.target)}else visible.delete(entry.target)});activity()},{threshold:.08});
  sections.forEach(section=>observer.observe(section));
 }else{sections.forEach(section=>{section.classList.add('is-revealed');visible.add(section)})}
 reduced.addEventListener('change',preference);document.addEventListener('visibilitychange',activity);preference();
})();
