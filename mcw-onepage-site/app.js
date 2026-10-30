(() => {
  'use strict';
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const fmt = n => Math.round(n).toLocaleString('zh-TW');
  /* calculator */
  const f = $('#calc-form');
  if (f) {
    const mc = $('#c-machines');
    $$('[data-step]', f).forEach(b => b.addEventListener('click', () => {
      const cur = Number(mc.value) || 0, d = Number(b.dataset.step);
      mc.value = Math.min(12, Math.max(1, cur + d)); run();
    }));
    const out = $('#calc-out'), msg = $('#calc-msg');
    const run = () => {
      const v = id => $('#c-' + id).value.trim();
      const r = MCWCalc.compute({ machines: v('machines'), rent: v('rent'), turns: v('turns'), price: v('price'), utilities: v('utilities'), investment: v('investment') });
      if (!r.ok) { out.hidden = true; msg.hidden = false; return; }
      msg.hidden = true; out.hidden = false;
      ['dayRev', 'monthRev', 'yearRev', 'dayNet', 'monthNet', 'yearNet'].forEach(k => { $('#o-' + k).textContent = fmt(r[k]) + ' 元'; });
      $('#o-payback').textContent = r.payback === null ? '以目前條件無法推估回本時間' : '約 ' + (Math.ceil(r.payback * 10) / 10).toLocaleString('zh-TW') + ' 個月';
    };
    f.addEventListener('submit', e => { e.preventDefault(); run(); });
    f.addEventListener('input', () => { if (!out.hidden || !msg.hidden) run(); });
  }
  /* store carousel buttons (mobile swipe is native scroll-snap) */
  $$('[data-scroll]').forEach(b => b.addEventListener('click', () => {
    const t = $(b.dataset.target); t.scrollBy({ left: Number(b.dataset.scroll) * t.clientWidth * 0.85, behavior: 'smooth' });
  }));
  /* lead form */
  const lf = $('#lead-form');
  if (lf) lf.addEventListener('submit', async e => {
    e.preventDefault();
    const st = $('#lead-status'); st.className = 'lead-status';
    if (!lf.checkValidity()) { lf.reportValidity(); return; }
    const d = new FormData(lf), body = {};
    for (const [k, v] of d) body[k] = body[k] ? body[k] + '、' + v : v;
    body.submittedAt = new Date().toISOString();
    const url = (window.MCW_CONFIG || {}).formEndpoint;
    if (!url) { st.textContent = '表單送出位置尚未設定（開發預覽）。請直接加 LINE @mcw27 或撥打加盟專線 07-788-1902。'; st.classList.add('is-warn'); return; }
    const btn = $('button[type=submit]', lf); btn.disabled = true;
    try {
      await fetch(url, { method: 'POST', mode: 'no-cors', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(body) });
      lf.reset(); st.textContent = '已收到您的預約，我們會盡快與您聯繫。也可以直接加 LINE @mcw27。'; st.classList.add('is-ok');
    } catch (_) {
      st.textContent = '送出失敗，請稍後再試，或直接加 LINE @mcw27。'; st.classList.add('is-warn');
    } finally { btn.disabled = false; }
  });
})();
