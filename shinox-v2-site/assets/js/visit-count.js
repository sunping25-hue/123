/* GoatCounter's public total is optional: keep the footer quiet if unavailable. */
(() => {
  'use strict';
  if (window.__shinoxVisitCountLoaded) return;
  window.__shinoxVisitCountLoaded = true;

  let count = null;
  const english = document.documentElement.lang.toLowerCase().startsWith('en');
  const label = english ? 'Total visits: ' : '累計瀏覽人次：';

  function mount() {
    const footer = document.querySelector('footer');
    if (!footer) return;
    let wrapper = footer.querySelector('#visit-count-wrap');
    if (!wrapper) {
      wrapper = document.createElement('small');
      wrapper.id = 'visit-count-wrap';
      wrapper.hidden = true;
      wrapper.style.cssText = 'display:none;font-size:0.75rem;line-height:1.6;font-weight:400;color:inherit;opacity:0.7';
      const value = document.createElement('span');
      value.id = 'visit-count';
      wrapper.append(document.createTextNode(label), value);
      const copyright = [...footer.querySelectorAll('p,span')].find(node =>
        node.textContent.includes('©') && !node.querySelector('p,span'));
      (copyright || footer).append(wrapper);
    }
    const value = wrapper.querySelector('#visit-count');
    if (value && count !== null) {
      if (value.textContent !== count) value.textContent = count;
      wrapper.hidden = false;
      wrapper.style.display = 'block';
    } else {
      wrapper.hidden = true;
      wrapper.style.display = 'none';
    }
  }

  function validCount(value) {
    if (typeof value === 'number') {
      return Number.isSafeInteger(value) && value >= 0 ? String(value) : null;
    }
    if (typeof value !== 'string') return null;
    const text = value.trim();
    // Preserve the grouping supplied by GoatCounter without accepting markup.
    return /^\d+(?:[,\. \u00a0\u202f]\d+)*$/.test(text) ? text : null;
  }

  function start() {
    mount();
    // Some shared page scripts create or replace the footer after page load.
    new MutationObserver(mount).observe(document.body, { childList: true, subtree: true });
    fetch('https://shinox.goatcounter.com/counter/TOTAL.json')
      .then(response => {
        if (!response.ok) throw new Error('Counter unavailable');
        return response.json();
      })
      .then(data => {
        count = validCount(data && data.count);
        mount();
      })
      .catch(() => {
        count = null;
        mount();
      });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start, { once: true });
  } else {
    start();
  }
})();
