import { containDialogFocus } from './dialog';

document.querySelectorAll<HTMLElement>('[data-gallery]').forEach((gallery) => {
  const dialog = gallery.querySelector<HTMLDialogElement>('dialog')!;
  containDialogFocus(dialog);
  const image = dialog.querySelector<HTMLImageElement>('[data-lightbox-image]')!;
  const caption = dialog.querySelector<HTMLElement>('#lightbox-caption')!;
  const count = dialog.querySelector<HTMLElement>('[data-lightbox-count]')!;
  const entries = Array.from(gallery.querySelectorAll<HTMLButtonElement>('[data-gallery-open]'));
  let current = 0;
  let opener: HTMLButtonElement | null = null;
  const visible = () => entries.filter((button) => !button.closest<HTMLElement>('figure')!.hidden);
  const show = (index: number) => {
    const items = visible();
    current = (index + items.length) % items.length;
    const entry = items[current];
    image.src = entry.dataset.src!;
    image.alt = entry.dataset.alt!;
    caption.textContent = entry.dataset.title!;
    count.textContent = `${current + 1} / ${items.length}`;
  };
  entries.forEach((button) =>
    button.addEventListener('click', () => {
      opener = button;
      show(visible().indexOf(button));
      dialog.showModal();
      document.body.classList.add('modal-open');
    }),
  );
  dialog.querySelector('[data-lightbox-close]')!.addEventListener('click', () => dialog.close());
  dialog.querySelector('[data-lightbox-prev]')!.addEventListener('click', () => show(current - 1));
  dialog.querySelector('[data-lightbox-next]')!.addEventListener('click', () => show(current + 1));
  dialog.addEventListener('keydown', (event) => {
    if (event.key === 'ArrowLeft') {
      event.preventDefault();
      show(current - 1);
    }
    if (event.key === 'ArrowRight') {
      event.preventDefault();
      show(current + 1);
    }
  });
  dialog.addEventListener('click', (event) => {
    if (event.target === dialog) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    opener?.focus();
  });
  gallery.querySelectorAll<HTMLButtonElement>('[data-filter]').forEach((button) =>
    button.addEventListener('click', () => {
      gallery
        .querySelectorAll('[data-filter]')
        .forEach((filter) => filter.setAttribute('aria-pressed', String(filter === button)));
      gallery.querySelectorAll<HTMLElement>('figure').forEach((figure) => {
        figure.hidden =
          button.dataset.filter !== 'Todos' && figure.dataset.category !== button.dataset.filter;
      });
      gallery.querySelector('[data-gallery-status]')!.textContent =
        `${visible().length} imagens exibidas`;
    }),
  );
});
