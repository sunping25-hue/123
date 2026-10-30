(() => {
  'use strict';
  const inp = document.getElementById('revcalc-customers');
  if (!inp) return;
  const m = document.getElementById('revcalc-month'), y = document.getElementById('revcalc-year');
  const TICKET = 250, DAYS = 30, MONTHS = 12;
  const fmt = n => 'NT$' + Math.round(n).toLocaleString('en-US');
  const run = () => {
    const c = Math.max(0, Math.floor(Number(inp.value) || 0));
    const month = c * TICKET * DAYS;
    m.textContent = fmt(month); y.textContent = fmt(month * MONTHS);
  };
  inp.addEventListener('input', run); run();
})();
