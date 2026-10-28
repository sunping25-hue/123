const menu = document.querySelector('.toggle');
const nav = document.querySelector('#navigation');
function closeMenu() { nav.classList.remove('open'); menu.setAttribute('aria-expanded', 'false'); }
menu.addEventListener('click', () => { const open = nav.classList.toggle('open'); menu.setAttribute('aria-expanded', String(open)); });
nav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => { if (event.key === 'Escape' && nav.classList.contains('open')) { closeMenu(); menu.focus(); } });
const video = document.querySelector('video');
const control = document.querySelector('.video-control');
const motion = matchMedia('(prefers-reduced-motion: reduce)');
video.muted = true;
video.defaultMuted = true;
function sync() { const paused = video.paused; control.textContent = paused ? 'Play background video ▷' : 'Pause background video Ⅱ'; control.setAttribute('aria-label', paused ? 'Play background video' : 'Pause background video'); }
video.addEventListener('play', sync);
video.addEventListener('pause', sync);
video.addEventListener('error', () => { control.hidden = true; });
control.addEventListener('click', () => { if (video.paused) video.play().catch(sync); else video.pause(); });
function preference() { if (motion.matches) video.pause(); else video.play().catch(sync); sync(); }
motion.addEventListener('change', preference);
preference();
