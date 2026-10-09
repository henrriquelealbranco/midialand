/** Keep keyboard navigation inside a modal, including the last/first Tab boundary. */
export function containDialogFocus(dialog: HTMLDialogElement) {
  dialog.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const controls = Array.from(
      dialog.querySelectorAll<HTMLElement>(
        'a[href], button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex="0"]',
      ),
    ).filter((control) => control.getClientRects().length > 0);
    const first = controls[0];
    const last = controls.at(-1);
    if (!first || !last) return;
    if (
      event.shiftKey &&
      (document.activeElement === first || !dialog.contains(document.activeElement))
    ) {
      event.preventDefault();
      last.focus();
    } else if (
      !event.shiftKey &&
      (document.activeElement === last || !dialog.contains(document.activeElement))
    ) {
      event.preventDefault();
      first.focus();
    }
  });
}
