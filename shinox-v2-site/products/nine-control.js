/* Issue 10: a page-memory-only interface demonstration, never device control. */
(() => {
  'use strict';

  function init() {
    const root = document.querySelector('main[data-sx9]');
    if (!root || root.dataset.sx9Ready === 'true') return;
    root.dataset.sx9Ready = 'true';
    const english = /^en(?:-|$)/i.test(document.documentElement.lang || '');
    const text = (zh, en) => english ? en : zh;
    const find = (selector) => root.querySelector(selector);
    const write = (selector, value) => {
      const element = find(selector);
      if (element) element.textContent = value;
    };

    const finishes = {
      silver: { color: '#C8D7E6', name: text('不鏽鋼銀・規劃色票', 'Stainless silver · planning swatch') },
      blue: { color: '#087CFF', name: text('科技藍・規劃色票', 'Technology blue · planning swatch') },
      black: { color: '#303944', name: text('石墨黑・規劃色票', 'Graphite black · planning swatch') },
      red: { color: '#B54C50', name: text('深紅・規劃色票', 'Deep red · planning swatch') }
    };
    const functions = {
      rinse: [text('高壓沖水', 'High-pressure rinse'), text('規劃中的沖洗功能示意。實際壓力、時間與設備配置須由專人確認；點選不會啟動設備。', 'A planned rinse function for this interface demo. Pressure, timing and equipment configuration require confirmation; selecting it does not start equipment.')],
      foam: [text('雪花泡沫', 'Foam wash'), text('規劃中的泡沫清潔操作示意。清潔劑、供給方式與功能配置待確認，不代表實際出液。', 'A planned foam-wash interface demonstration. Chemicals, supply method and configuration require confirmation; no fluid is dispensed.')],
      water: [text('低壓淨水', 'Low-pressure water'), text('規劃中的低壓淨水功能示意。水質、水處理及配管需求須另行確認；此處不連接設備。', 'A planned low-pressure water function. Water quality, treatment and plumbing require confirmation; this page is not connected to equipment.')],
      air: [text('乾式風槍', 'Air gun'), text('規劃中的氣流操作示意。空壓、管路與配套設備須依場域確認，這是介面展示。', 'A planned air-gun interface demonstration. Air supply, plumbing and supporting equipment depend on the site and require confirmation.')],
      coating: [text('奈米鍍膜（配置待確認）', 'Nano coating · configuration pending'), text('規劃中的鍍膜功能名稱。藥劑、來源與實際設備配置待查驗確認；此處僅切換示意介面。', 'A planned coating-function label. Chemical details, source and equipment configuration require verification; this only switches the demonstration interface.')],
      glass: [text('玻璃清潔劑', 'Glass cleaner'), text('規劃中的玻璃清潔功能示意。清潔劑與供液配置待確認，不代表已包含於正式機型。', 'A planned glass-cleaning function. Cleaning agent and fluid supply require confirmation; inclusion in a production model is not established.')],
      vacuum: [text('乾濕兩用吸塵・選配規劃', 'Wet/dry vacuum · optional planning'), text('乾區選配規劃示意。吸塵設備、接線與安裝需求須另外確認；不視為標準配備。', 'An optional dry-zone concept. Vacuum equipment, wiring and installation require separate confirmation; this is not a standard-equipment claim.')],
      polish: [text('氣動打蠟・選配規劃', 'Pneumatic waxing · optional planning'), text('乾區選配規劃示意。氣源、工具與功能配置待確認；不視為標準配備。', 'An optional dry-zone concept. Air supply, tools and configuration require confirmation; this is not a standard-equipment claim.')],
      aux: [text('預留功能・待確認', 'Reserved function · to be confirmed'), text('預留位置，不補造第九項正式功能。完整九種配置須依業主確認；這個按鈕只展示選取狀態。', 'A reserved position, not an invented ninth production function. The complete nine-function configuration requires owner confirmation; this button only demonstrates selection.')]
    };

    // These remain independent local UI choices; never modify a product image.
    let finish = 'silver';
    let selectedFunction = 'rinse';
    const defaults = Object.freeze({ seconds: 180, credits: 30, unlimited: false, pausable: true });
    let settings = { ...defaults };

    function updateFinish(key) {
      if (!Object.prototype.hasOwnProperty.call(finishes, key)) return;
      finish = key;
      root.querySelectorAll('button[data-finish]').forEach((button) => {
        button.setAttribute('aria-pressed', String(button.dataset.finish === finish));
      });
      write('#sx9-finish-name', finishes[finish].name);
      write('#sx9-finish-note', text(
        '僅為規劃色票；實際外觀、色樣與供應狀態待確認。保留原始設備參考圖，不套色、不改造實機外觀。',
        'Planning swatch only. Actual finish, appearance and availability require confirmation. The original equipment reference remains unchanged, without recoloring.'
      ));
      const image = find('#sx9-finish-visual');
      const frame = find('[data-finish-frame]') || (image && image.parentElement);
      if (frame) frame.style.setProperty('--finish', finishes[finish].color);
    }

    function updateFunction(key) {
      if (!Object.prototype.hasOwnProperty.call(functions, key)) return;
      selectedFunction = key;
      root.querySelectorAll('button[data-function]').forEach((button) => {
        button.setAttribute('aria-pressed', String(button.dataset.function === selectedFunction));
      });
      write('#sx9-function-name', functions[key][0]);
      write('#sx9-function-description', functions[key][1]);
    }

    function renderSettings() {
      const minutes = String(Math.floor(settings.seconds / 60)).padStart(2, '0');
      const seconds = String(settings.seconds % 60).padStart(2, '0');
      // All-you-can-use mode still operates within the configured demo duration.
      write('#sx9-demo-time', `${minutes}:${seconds}`);
      write('#sx9-demo-mode', settings.unlimited
        ? text('吃到飽示意・限設定時長內', 'All-you-can-use demo · within configured duration')
        : text('一般計時示意', 'Standard timed demo'));
      write('#sx9-demo-credit', String(settings.credits));
    }

    // Native buttons remain reachable by Tab; arrows offer an additional shortcut.
    function wireChoices(selector, attribute, choices, update) {
      const buttons = [...root.querySelectorAll(selector)].filter((button) =>
        Object.prototype.hasOwnProperty.call(choices, button.dataset[attribute]));
      buttons.forEach((button) => {
        button.type = 'button';
        button.addEventListener('click', () => update(button.dataset[attribute]));
        button.addEventListener('keydown', (event) => {
          if (event.altKey || event.ctrlKey || event.metaKey) return;
          const enabled = buttons.filter((item) => !item.disabled);
          const current = enabled.indexOf(button);
          if (current < 0) return;
          let next;
          if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (current + 1) % enabled.length;
          if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (current + enabled.length - 1) % enabled.length;
          if (event.key === 'Home') next = 0;
          if (event.key === 'End') next = enabled.length - 1;
          if (next === undefined) return;
          event.preventDefault();
          enabled[next].focus({ preventScroll: true });
          update(enabled[next].dataset[attribute]);
        });
      });
    }

    wireChoices('button[data-finish]', 'finish', finishes, updateFinish);
    wireChoices('button[data-function]', 'function', functions, updateFunction);
    updateFinish(finish);
    updateFunction(selectedFunction);
    renderSettings();

    const form = find('#sx9-settings-form');
    if (form) {
      const secondsField = form.querySelector('[name="seconds"]');
      const creditsField = form.querySelector('[name="credits"]');
      const unlimitedField = form.querySelector('[name="unlimited"]');
      const pausableField = form.querySelector('[name="pausable"]');
      const output = form.querySelector('[data-settings-output]') || find('[data-settings-output]');
      if (output) {
        output.setAttribute('role', 'status');
        output.setAttribute('aria-live', 'polite');
        output.setAttribute('aria-atomic', 'true');
      }
      function say(message) {
        if (output) output.textContent = message;
      }
      function resetFields() {
        if (secondsField) secondsField.value = String(defaults.seconds);
        if (creditsField) creditsField.value = String(defaults.credits);
        if (unlimitedField) unlimitedField.checked = defaults.unlimited;
        if (pausableField) pausableField.checked = defaults.pausable;
      }
      if (secondsField) {
        secondsField.type = 'number';
        secondsField.min = '30';
        secondsField.max = '1800';
        secondsField.step = '30';
        secondsField.required = true;
      }
      if (creditsField) {
        creditsField.type = 'number';
        creditsField.min = '1';
        creditsField.max = '999';
        creditsField.step = '1';
        creditsField.required = true;
      }
      resetFields();
      // Invalid native submissions fire `invalid`, not `submit`; clear stale success.
      form.addEventListener('invalid', () => say(text(
        '請先修正標示欄位；示範設定尚未套用。',
        'Correct the highlighted fields first. Demo settings have not been applied.'
      )), true);
      form.addEventListener('input', () => say(''));
      form.addEventListener('submit', (event) => {
        event.preventDefault();
        if (!secondsField || !creditsField) {
          say(text('示範欄位尚未備齊，無法套用。', 'Demo fields are incomplete; no settings were applied.'));
          return;
        }
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
        const seconds = Number(secondsField.value);
        const credits = Number(creditsField.value);
        if (!Number.isInteger(seconds) || seconds < 30 || seconds > 1800 || seconds % 30 !== 0 ||
            !Number.isInteger(credits) || credits < 1 || credits > 999) {
          say(text('請填寫有效的時間與示意點數；設定尚未套用。', 'Enter a valid duration and illustrative credit value. Settings were not applied.'));
          return;
        }
        settings = { seconds, credits, unlimited: !!(unlimitedField && unlimitedField.checked), pausable: !!(pausableField && pausableField.checked) };
        renderSettings();
        const pauseText = settings.pausable ? text('允許暫停', 'pause enabled') : text('不允許暫停', 'pause disabled');
        const modeText = settings.unlimited
          ? text('吃到飽示意，仍限設定時長內', 'all-you-can-use demo within the configured duration')
          : text('一般計時示意', 'standard timed demo');
        say(text(
          `已套用本頁示範設定（${modeText}；${pauseText}）；未儲存至設備、未扣款，重新載入即還原。`,
          `Page-only demo settings applied (${modeText}; ${pauseText}). Nothing was saved to equipment or charged; reloading resets the demo.`
        ));
      });
      form.addEventListener('reset', (event) => {
        event.preventDefault();
        settings = { ...defaults };
        resetFields();
        updateFinish('silver');
        updateFunction('rinse');
        renderSettings();
        say(text('已還原本頁示範預設值與選取狀態；沒有變更任何實際設備。', 'Demo defaults and selections restored. No actual equipment was changed.'));
      });
    }

    const periods = {
      day: { cycles: 128, online: 6, members: 42, values: [8, 18, 25, 14, 28, 23, 12], labels: ['08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00'] },
      week: { cycles: 836, online: 6, members: 236, values: [92, 114, 103, 128, 121, 160, 118], labels: english ? ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] : ['週一', '週二', '週三', '週四', '週五', '週六', '週日'] }
    };
    function renderPeriod(period) {
      const dataset = periods[period] || periods.day;
      ['cycles', 'online', 'members'].forEach((key) => write(`[data-kpi="${key}"]`, String(dataset[key])));
      const max = Math.max(...dataset.values);
      root.querySelectorAll('[data-chart-bar]').forEach((bar, index) => {
        if (index >= dataset.values.length) return;
        const value = dataset.values[index];
        bar.style.height = `${Math.max(8, Math.round(value / max * 100))}%`;
        bar.setAttribute('role', 'img');
        bar.removeAttribute('aria-hidden');
        const label = text(`${dataset.labels[index]}：${value} 次，模擬資料`, `${dataset.labels[index]}: ${value} cycles, simulated data`);
        bar.setAttribute('aria-label', label);
        bar.title = label;
        const visibleLabel = bar.parentElement && bar.parentElement.querySelector('[data-chart-label]');
        const adjacentLabel = bar.nextElementSibling;
        if (visibleLabel) visibleLabel.textContent = dataset.labels[index];
        else if (adjacentLabel && adjacentLabel.tagName === 'SPAN') adjacentLabel.textContent = dataset.labels[index];
      });
      write('#sx9-cloud-description', text(
        `${period === 'week' ? '每週' : '單日'}介面示範：所有指標與圖表均為模擬資料，未連接雲端或任何實際站點，不代表設備效能或營運實績。`,
        `${period === 'week' ? 'Weekly' : 'Daily'} interface demo: all metrics and charts use simulated data. No cloud or real site is connected; these are not equipment-performance or operating results.`
      ));
    }
    const periodField = find('#sx9-period');
    if (periodField) {
      if (!Object.prototype.hasOwnProperty.call(periods, periodField.value)) periodField.value = 'day';
      periodField.addEventListener('change', () => renderPeriod(periodField.value));
      renderPeriod(periodField.value);
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, { once: true });
  else init();
})();
