/* Keep decorative looping videos (no controls) playing, incl. iOS. */
(() => {
  'use strict';
  const vids = [...document.querySelectorAll('video.footer-install-video, video.sx-abc-video, video.sci-mascot-video')];
  if (!vids.length) return;
  const kick = v => { v.muted = true; v.defaultMuted = true; v.playsInline = true; v.setAttribute('playsinline', ''); if (v.paused) { const p = v.play(); if (p && p.catch) p.catch(() => {}); } };
  vids.forEach(v => { kick(v); v.addEventListener('pause', () => { if (!document.hidden) setTimeout(() => kick(v), 300); }); });
  const all = () => vids.forEach(kick);
  ['touchstart', 'pointerdown', 'scroll'].forEach(e => window.addEventListener(e, all, { passive: true, once: true }));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) all(); });
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) kick(e.target); }), { threshold: 0.1 });
    vids.forEach(v => io.observe(v));
  }
})();
