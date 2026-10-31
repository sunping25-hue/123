(() => {
  'use strict';
  const inp = document.getElementById('revcalc-customers');
  if (!inp) return;
  const m = document.getElementById('revcalc-month'), y = document.getElementById('revcalc-year');
  const sel = document.getElementById('revcalc-ticket');
  const DAYS = 30, MONTHS = 12;
  const root = document.getElementById('revenue-calculator');
  const CUR = (root && root.dataset.currency) || 'NT$';
  const fmt = n => CUR + Math.round(n).toLocaleString('en-US');
  const run = () => {
    const c = Math.max(0, Math.floor(Number(inp.value) || 0));
    const ticket = Number(sel && sel.value) || 0;
    const month = c * ticket * DAYS;
    m.textContent = fmt(month); y.textContent = fmt(month * MONTHS);
  };
  inp.addEventListener('input', run); if (sel) sel.addEventListener('change', run); run();
})();
