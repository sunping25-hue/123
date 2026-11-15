/* Shared Hero playback: original approved video + a derived compact rendition. */
(() => {
  'use strict';
  const base = new URL('.', document.currentScript.src);
  const video = document.querySelector('video');
  const control = document.querySelector('.video-control');
  if (!video || !control) return;
  const english = document.documentElement.lang.startsWith('en');
  const labels = english
    ? { play: 'Play background video ▷', pause: 'Pause background video Ⅱ', retry: 'Retry background video ▷' }
    : { play: '播放影片 ▷', pause: '暫停影片 Ⅱ', retry: '重新載入影片 ▷' };
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const limited = () => connection && (connection.saveData || ['slow-2g', '2g'].includes(connection.effectiveType));
  let userPaused = false;
  let resumeOnVisible = false;
  let failed = false;
  const source = new URL(matchMedia('(max-width: 767px)').matches
    ? 'media/shinox-hero-mobile.mp4' : 'media/shinox-hero.mp4', base).href;
  video.muted = true;
  video.defaultMuted = true;
  video.loop = true;
  video.playsInline = true;
  function sync() {
    const text = failed ? labels.retry : video.paused ? labels.play : labels.pause;
    control.textContent = text;
    control.setAttribute('aria-label', text.replace(/[▷Ⅱ]/g, '').trim());
  }
  function play() {
    if (failed) { video.removeAttribute('src'); video.load(); failed = false; }
    if (!video.getAttribute('src')) video.src = source;
    video.play().catch(sync);
  }
  video.addEventListener('play', sync);
  video.addEventListener('pause', sync);
  video.addEventListener('error', () => { failed = true; sync(); });
  control.addEventListener('click', () => {
    if (video.paused || failed) { userPaused = false; play(); }
    else { userPaused = true; video.pause(); }
  });
  motion.addEventListener('change', () => {
    if (motion.matches) video.pause();
    else if (!userPaused && !limited() && !document.hidden) play();
  });
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) { resumeOnVisible = !video.paused; video.pause(); }
    else if (resumeOnVisible && !userPaused && !motion.matches && !limited()) play();
  });
  if (!motion.matches && !limited() && !document.hidden) { video.autoplay = true; play(); }
  sync();
})();
