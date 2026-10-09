import { containDialogFocus } from './dialog';

const menu = document.querySelector<HTMLDialogElement>('#mobile-menu');
const toggle = document.querySelector<HTMLButtonElement>('.menu-toggle');
if (menu && toggle) {
  containDialogFocus(menu);
  const close = () => menu.close();
  toggle.addEventListener('click', () => {
    menu.showModal();
    toggle.setAttribute('aria-expanded', 'true');
    document.body.classList.add('modal-open');
  });
  menu.querySelector('[data-menu-close]')?.addEventListener('click', close);
  menu.addEventListener('click', (event) => {
    if (event.target === menu) close();
  });
  menu.addEventListener('close', () => {
    toggle.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('modal-open');
    toggle.focus();
  });
  window.matchMedia('(min-width: 1101px)').addEventListener('change', (event) => {
    if (event.matches && menu.open) close();
  });
}
