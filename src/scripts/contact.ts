const root = document.querySelector<HTMLElement>('[data-contact]');
if (root) {
  const form = root.querySelector<HTMLFormElement>('form')!;
  const tabs = Array.from(root.querySelectorAll<HTMLButtonElement>('[data-mode]'));
  const result = root.querySelector<HTMLElement>('.form-result')!;
  const summary = root.querySelector<HTMLTextAreaElement>('#contact-summary')!;
  const alert = root.querySelector<HTMLElement>('.form-error-summary')!;
  const copyStatus = root.querySelector<HTMLElement>('.copy-status')!;
  let mode = 'anunciar';
  type Control = HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement;
  const activeFields = () =>
    Array.from(form.querySelectorAll<Control>('input, select, textarea')).filter(
      (field) => !field.closest('fieldset')!.disabled,
    );
  const clearError = (field: Control) => {
    field.removeAttribute('aria-invalid');
    const error = document.getElementById(`${field.id}-error`)!;
    error.hidden = true;
    error.textContent = '';
  };
  const switchMode = (tab: HTMLButtonElement) => {
    mode = tab.dataset.mode!;
    tabs.forEach((item) => {
      const selected = item === tab;
      item.setAttribute('aria-selected', String(selected));
      item.tabIndex = selected ? 0 : -1;
      const panel = document.getElementById(item.getAttribute('aria-controls')!)!;
      panel.hidden = !selected;
      panel.querySelector<HTMLFieldSetElement>('fieldset')!.disabled = !selected;
    });
    result.hidden = true;
    alert.hidden = true;
    form.querySelectorAll<Control>('input, select, textarea').forEach(clearError);
  };
  tabs.forEach((tab, index) => {
    tab.addEventListener('click', () => switchMode(tab));
    tab.addEventListener('keydown', (event) => {
      if (['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(event.key)) {
        event.preventDefault();
        const next =
          event.key === 'Home'
            ? 0
            : event.key === 'End'
              ? tabs.length - 1
              : (index + 1) % tabs.length;
        switchMode(tabs[next]);
        tabs[next].focus();
      }
    });
  });
  const params = new URLSearchParams(window.location.search);
  for (const name of ['cidade', 'solucao']) {
    const control = document.getElementById(`anunciar-${name}`) as HTMLSelectElement;
    const value = params.get(name);
    if (value && Array.from(control.options).some((option) => option.value === value))
      control.value = value;
  }
  if (params.get('intencao') === 'ceder') switchMode(tabs[1]);
  form.querySelector<HTMLButtonElement>('[type="submit"]')!.disabled = false;
  form.addEventListener('input', (event) => {
    if (
      event.target instanceof HTMLInputElement ||
      event.target instanceof HTMLTextAreaElement ||
      event.target instanceof HTMLSelectElement
    )
      clearError(event.target);
    result.hidden = true;
    alert.hidden = true;
  });
  form.addEventListener('change', () => {
    result.hidden = true;
  });
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    result.hidden = true;
    let firstInvalid: Control | undefined;
    let errors = 0;
    for (const field of activeFields()) {
      clearError(field);
      const value = field.value.trim();
      let message = '';
      if (field.required && !value)
        message =
          field instanceof HTMLSelectElement
            ? 'Selecione uma opção para continuar.'
            : 'Preencha este campo para continuar.';
      else if (field instanceof HTMLInputElement && field.type === 'email' && !field.validity.valid)
        message = 'Informe um e-mail válido, como nome@empresa.com.br.';
      else if (field.name === 'telefone' && value && !/^[+\d\s().-]+$/.test(value))
        message = 'Informe um telefone com DDD, usando apenas números e sinais de telefone.';
      else if (
        field.name === 'telefone' &&
        value &&
        (value.replace(/\D/g, '').length < 10 || value.replace(/\D/g, '').length > 15)
      )
        message = 'Informe um telefone com DDD (10 a 15 dígitos).';
      else if (field.name === 'contato' && value) {
        const emailValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
        const phoneValid =
          /^[+\d\s().-]+$/.test(value) &&
          value.replace(/\D/g, '').length >= 10 &&
          value.replace(/\D/g, '').length <= 15;
        if (!emailValid && !phoneValid)
          message = 'Informe um e-mail válido ou um telefone com DDD.';
      }
      if (message) {
        const error = document.getElementById(`${field.id}-error`)!;
        error.textContent = message;
        error.hidden = false;
        field.setAttribute('aria-invalid', 'true');
        firstInvalid ||= field;
        errors++;
      }
    }
    if (firstInvalid) {
      alert.textContent = `Confira ${errors === 1 ? 'o campo indicado' : `os ${errors} campos indicados`} antes de preparar o resumo.`;
      alert.hidden = false;
      firstInvalid.focus();
      return;
    }
    alert.hidden = true;
    summary.value = [
      `Midialand — ${mode === 'anunciar' ? 'Quero anunciar' : 'Quero ceder espaço'}`,
      '',
      ...activeFields()
        .filter((field) => field.value.trim())
        .map((field) => `${field.dataset.label}: ${field.value.trim()}`),
      '',
      'Resumo preparado em demonstração. Nenhum dado foi enviado.',
    ].join('\n');
    copyStatus.textContent = '';
    result.hidden = false;
    root.querySelector<HTMLElement>('#result-title')!.focus();
  });
  root.querySelector<HTMLButtonElement>('[data-copy]')!.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(summary.value);
      copyStatus.textContent = 'Resumo copiado. Nenhum dado foi enviado.';
    } catch {
      summary.focus();
      summary.select();
      copyStatus.textContent =
        'A cópia automática não está disponível. O resumo está selecionado: use a opção Copiar do seu dispositivo.';
    }
  });
}
