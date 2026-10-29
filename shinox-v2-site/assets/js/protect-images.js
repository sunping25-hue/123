/* Image interaction deterrent only: this does not prevent access to image files.
   Text selection/copy, ordinary links and explicit PDF/download controls remain native. */
(() => {
  'use strict';
  const marker = 'data-sx-image-protected';
  const styleId = 'sx-image-protection-style';
  if (document.getElementById(styleId)) return;

  const style = document.createElement('style');
  style.id = styleId;
  style.textContent = `img[${marker}] {-webkit-user-drag:none;user-select:none;-webkit-touch-callout:none;}`;
  document.head.append(style);
  const originals = new WeakMap();

  function downloadImage(image) {
    const link = image.closest('a');
    if (!link) return false;
    if (link.hasAttribute('download')) return true;
    try {
      return /\.pdf$/i.test(new URL(link.getAttribute('href') || '', document.baseURI).pathname);
    } catch (_) {
      return false;
    }
  }

  function protect(image) {
    if (downloadImage(image)) {
      if (originals.has(image)) {
        const original = originals.get(image);
        if (original === null) image.removeAttribute('draggable');
        else if (image.getAttribute('draggable') !== original) image.setAttribute('draggable', original);
        originals.delete(image);
      }
      image.removeAttribute(marker);
      return;
    }
    if (!originals.has(image)) originals.set(image, image.getAttribute('draggable'));
    if (image.getAttribute('draggable') !== 'false') image.setAttribute('draggable', 'false');
    if (!image.hasAttribute(marker)) image.setAttribute(marker, '');
  }

  function protectWithin(node) {
    if (!(node instanceof Element)) return;
    if (node.matches('img')) protect(node);
    node.querySelectorAll('img').forEach(protect);
  }

  document.querySelectorAll('img').forEach(protect);
  new MutationObserver((records) => {
    records.forEach((record) => {
      if (record.type === 'childList') record.addedNodes.forEach(protectWithin);
      else protectWithin(record.target);
    });
  }).observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['href', 'download', 'draggable']
  });

  function preventImageInteraction(event) {
    const image = event.target;
    if (image instanceof HTMLImageElement && !downloadImage(image)) event.preventDefault();
  }
  document.addEventListener('contextmenu', preventImageInteraction, true);
  document.addEventListener('dragstart', preventImageInteraction, true);
})();
