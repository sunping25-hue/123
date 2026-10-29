/* Only the compact About film; independent of the homepage Hero player. */
(() => {
  'use strict';
  const frame = document.querySelector('[data-brand-film]');
  const video = frame?.querySelector('video');
  if (!video) return;
  const fallback = frame.querySelector('[data-brand-film-fallback]');
  const motion = matchMedia('(prefers-reduced-motion: reduce)');
  const connection = navigator.connection;
  const limited = () => Boolean(connection && (connection.saveData || ['slow-2g', '2g'].includes(connection.effectiveType)));
  let visible = false;
  let userPaused = false;
  let automaticPause = false;
  let failed = false;
  video.muted = true;
  video.defaultMuted = true;

  function pauseForEnvironment() {
    if (!video.paused) {
      automaticPause = true;
      video.pause();
    }
  }
  function sync() {
    if (!visible || document.hidden || motion.matches || limited()) {
      pauseForEnvironment();
    } else if (!userPaused && !failed) {
      video.play().catch(() => { /* Native controls remain available when autoplay is blocked. */ });
    }
  }
  video.addEventListener('pause', () => {
    if (automaticPause) automaticPause = false;
    else userPaused = true;
  });
  video.addEventListener('play', () => {
    userPaused = false;
    if (!visible || document.hidden) pauseForEnvironment();
  });
  video.addEventListener('error', () => {
    failed = true;
    if (fallback) fallback.hidden = false;
  });
  motion.addEventListener('change', sync);
  connection?.addEventListener?.('change', sync);
  document.addEventListener('visibilitychange', sync);
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      visible = entries[0].isIntersecting && entries[0].intersectionRatio >= 0.35;
      sync();
    }, { threshold: [0, 0.35] });
    observer.observe(video);
    window.addEventListener('pagehide', pauseForEnvironment);
  }
})();
