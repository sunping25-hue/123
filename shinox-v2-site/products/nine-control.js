/* Nine-in-one V2: page-local choices only; no device, payment or cloud requests. */
(() => {
  'use strict';
  const root = document.querySelector('main[data-nine-v2]');
  if (!root || root.dataset.ready === 'true') return;
  root.dataset.ready = 'true';
  const english = /^en(?:-|$)/i.test(document.documentElement.lang || '');
  const text = (zh, en) => english ? en : zh;
  const write = (selector, value) => {
    const node = root.querySelector(selector);
    if (node) node.textContent = value;
  };

  function choices(selector, attribute, labels, update) {
    const buttons = [...root.querySelectorAll(selector)];
    function choose(value) {
      if (!Object.prototype.hasOwnProperty.call(labels, value)) return;
      buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset[attribute] === value)));
      update(value, labels[value]);
    }
    buttons.forEach((button, index) => {
      button.addEventListener('click', () => choose(button.dataset[attribute]));
      button.addEventListener('keydown', event => {
        if (event.altKey || event.ctrlKey || event.metaKey) return;
        let next;
        if (['ArrowRight', 'ArrowDown'].includes(event.key)) next = (index + 1) % buttons.length;
        if (['ArrowLeft', 'ArrowUp'].includes(event.key)) next = (index + buttons.length - 1) % buttons.length;
        if (event.key === 'Home') next = 0;
        if (event.key === 'End') next = buttons.length - 1;
        if (next === undefined) return;
        event.preventDefault();
        buttons[next].focus({ preventScroll: true });
        choose(buttons[next].dataset[attribute]);
      });
    });
  }

  choices('[data-model]', 'model', {
    upright: text('直立式', 'Upright'),
    dual: text('雙掛式', 'Dual-mount')
  }, (key, label) => {
    root.querySelectorAll('[data-model-card]').forEach(card => card.classList.toggle('is-selected', card.dataset.modelCard === key));
    write('#n9v-model-status', text('目前選擇：', 'Selected format: ') + label);
  });

  choices('[data-color]', 'color', {
    silver: text('不鏽鋼銀', 'Stainless silver'),
    blue: text('藍色', 'Blue'),
    black: text('黑色', 'Black'),
    red: text('紅色', 'Red')
  }, (_key, label) => write('#n9v-color-status', text('目前選擇：', 'Selected finish: ') + label));

  const cloud = root.querySelector('#n9v-cloud');
  const cloudViews = [...root.querySelectorAll('[data-cloud-view]')];
  cloudViews.forEach(button => button.addEventListener('click', () => {
    const members = button.dataset.cloudView === 'members';
    cloudViews.forEach(node => node.setAttribute('aria-pressed', String(node === button)));
    const title = cloud && cloud.querySelector('[data-cloud-title]');
    if (title) title.textContent = members ? text('會員管理', 'Membership management') : text('營運總覽', 'Operations overview');
    // The illustrative chart remains non-numeric and never claims live data.
    if (cloud) cloud.dataset.view = members ? 'members' : 'operations';
  }));

  const form = root.querySelector('#n9v-settings-form');
  if (form) {
    const output = form.querySelector('#n9v-settings-output');
    const amountField = form.querySelector('[data-amount-field]');
    function syncMode() {
      const showAmount = form.elements.mode.value === 'amount';
      if (amountField) amountField.hidden = !showAmount;
      if (form.elements.amount) {
        form.elements.amount.disabled = !showAmount;
        form.elements.amount.required = showAmount;
      }
    }
    form.elements.mode.addEventListener('change', syncMode);
    syncMode();
    const say = message => { if (output) output.textContent = message; };
    form.addEventListener('input', () => say(''));
    form.addEventListener('invalid', () => say(text('請修正標示的設定欄位。', 'Correct the highlighted settings fields.')), true);
    form.addEventListener('submit', event => {
      event.preventDefault();
      if (!form.reportValidity()) return;
      const seconds = Number(form.elements.seconds.value);
      if (!Number.isSafeInteger(seconds) || seconds < 1) {
        say(text('請填寫有效的整數秒數。', 'Enter a valid whole number of seconds.'));
        return;
      }
      const mode = form.elements.mode.selectedOptions[0].textContent;
      const amount = form.elements.mode.value === 'amount' ? form.elements.amount.value : '';
      if (amount !== '' && (!Number.isFinite(Number(amount)) || Number(amount) < 0)) {
        say(text('請填寫有效的示意數值。', 'Enter a valid illustrative value.'));
        return;
      }
      const amountText = amount !== '' ? text(`／自行填寫數值 ${amount}`, ` / user-entered value ${amount}`) : '';
      const pause = form.elements.pausable.checked ? text('允許暫停', 'pause enabled') : text('不允許暫停', 'pause disabled');
      say(text(
        `本頁預覽：${mode}／${seconds} 秒${amountText}／${pause}。未連接設備、未扣款；吃到飽模式仍依確認的時長與規則運作。`,
        `Page preview: ${mode} / ${seconds} seconds${amountText} / ${pause}. No equipment is connected or payment charged. All-you-can-use operation follows the confirmed duration and rules.`
      ));
    });
    form.addEventListener('reset', event => {
      event.preventDefault();
      form.elements.mode.value = 'time';
      form.elements.seconds.value = '';
      form.elements.pausable.checked = false;
      form.elements.amount.value = '';
      syncMode();
      say(text('已清除本頁預覽設定。', 'Page preview settings cleared.'));
    });
  }

  const options = [...root.querySelectorAll('[data-option]')];
  options.forEach(button => button.addEventListener('click', () => {
    button.setAttribute('aria-pressed', String(button.getAttribute('aria-pressed') !== 'true'));
    const selected = options.filter(node => node.getAttribute('aria-pressed') === 'true').map(node => node.querySelector('span').textContent);
    write('#n9v-options-output', selected.length
      ? text('已選需求：', 'Selected requirements: ') + selected.join(text('、', ', '))
      : text('尚未選擇選配需求。', 'No optional requirements selected.'));
    const plus = button.querySelector('b');
    if (plus) plus.textContent = button.getAttribute('aria-pressed') === 'true' ? '✓' : '＋';
  }));
})();
