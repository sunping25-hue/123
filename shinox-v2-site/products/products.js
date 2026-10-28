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


/* Official ShinoX YouTube: shared footer link; no unverified video IDs. */
(function addOfficialYoutubeLink(){
  const footer=document.querySelector('footer');
  if(!footer||footer.querySelector('[data-shinox-youtube]'))return;
  const english=document.documentElement.lang?.toLowerCase().startsWith('en');
  const link=document.createElement('a');
  link.href='https://www.youtube.com/@ShinoXwash';
  link.target='_blank';
  link.rel='noopener noreferrer';
  link.setAttribute('data-shinox-youtube','official-channel');
  link.setAttribute('aria-label',english?'Visit ShinoX official YouTube channel (opens new tab)':'前往 ShinoX 官方 YouTube 頻道（另開新分頁）');
  link.innerHTML='<svg aria-hidden="true" viewBox="0 0 24 24" width="22" height="22" fill="none" xmlns="http://www.w3.org/2000/svg"><rect x="1.5" y="4.5" width="21" height="15" rx="4.5" fill="#FF0033"/><path d="m10 8.5 6 3.5-6 3.5v-7Z" fill="#fff"/></svg><span>'+(english?'Official YouTube Channel':'ShinoX 官方 YouTube 頻道')+' ↗</span>';
  link.style.cssText='display:inline-flex;gap:10px;align-items:center;justify-content:center;min-height:44px;padding:10px 17px;border:1px solid #4b9eae;border-radius:100px;color:#edfaff;background:linear-gradient(120deg,#102e43,#061a2b);text-decoration:none;font-size:13px;font-weight:600;letter-spacing:.01em;transition:border-color .2s,box-shadow .2s,transform .2s;max-width:100%';
  link.addEventListener('mouseenter',()=>{link.style.borderColor='#17ddc7';link.style.boxShadow='0 0 18px #17ddc740';link.style.transform='translateY(-2px)'});
  link.addEventListener('mouseleave',()=>{link.style.borderColor='#4b9eae';link.style.boxShadow='none';link.style.transform='none'});
  const wrap=document.createElement('div');
  wrap.className='shinox-youtube-footer';
  wrap.style.cssText='display:flex;align-items:center;flex-wrap:wrap;gap:10px;padding:12px 0';
  wrap.appendChild(link);
  footer.appendChild(wrap);
})();
