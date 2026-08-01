const menuButton = document.querySelector('[data-menu-toggle]');
const nav = document.querySelector('[data-main-nav]');
menuButton?.addEventListener('click', () => nav?.classList.toggle('open'));

const locationDialog = document.querySelector('[data-location-dialog]');
document.querySelector('[data-location-button]')?.addEventListener('click', () => locationDialog?.showModal());
document.querySelectorAll('[data-location-close]').forEach((button) => {
  button.addEventListener('click', () => locationDialog?.close());
});

document.querySelector('[data-flash-close]')?.addEventListener('click', (event) => {
  event.currentTarget.closest('.flash')?.remove();
});
