const menuButton = document.querySelector('.menu-toggle');
const menu = document.querySelector('#main-nav');
const header = document.querySelector('.site-header');
function closeMenu() {
  menu.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
}
menuButton.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});
menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.classList.contains('open')) {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
header.addEventListener('focusout', event => {
  if (!header.contains(event.relatedTarget)) closeMenu();
});
matchMedia('(min-width: 1121px)').addEventListener('change', closeMenu);

// Product details also include the same footer calculator shortcuts.
(()=>{const style=document.createElement('link');style.rel='stylesheet';style.href='../calculator-gate.css';document.head.append(style);const script=document.createElement('script');script.src='../calculator-gate.js';script.defer=true;document.body.append(script)})();
