(() => {
  'use strict';
  const dialog = document.querySelector('#share-dialog');
  // The original links still download their PNG if dialogs or JavaScript are unavailable.
  if (!dialog || typeof dialog.showModal !== 'function') return;

  const script = document.querySelector('script[data-social-manifest]');
  const preview = document.querySelector('#share-preview');
  const title = document.querySelector('#share-title');
  const loading = document.querySelector('#share-loading');
  const nativeButton = document.querySelector('#share-native');
  const download = document.querySelector('#share-download');
  const copyButton = document.querySelector('#share-copy');
  const retryButton = document.querySelector('#share-retry');
  const urlInput = document.querySelector('#share-url');
  const hint = document.querySelector('#share-hint');
  const feedback = document.querySelector('#share-feedback');
  const canonical = new URL(document.querySelector('link[rel="canonical"]').href);
  let manifestPromise;
  let selection = 0;
  let opener;
  let activeService;
  let activeFile;
  let previewURL;
  let fileSharing = false;
  const fileCache = new Map();

  const readManifest = () => {
    if (!manifestPromise) {
      manifestPromise = fetch(script.dataset.socialManifest).then((response) => {
        if (!response.ok) throw new Error('Manifest unavailable');
        return response.json();
      }).then((services) => {
        if (!Array.isArray(services)) throw new Error('Invalid service manifest');
        return services;
      }).catch((error) => {
        manifestPromise = undefined;
        throw error;
      });
    }
    return manifestPromise;
  };

  const readFile = (service) => {
    if (!fileCache.has(service.image)) {
      const request = fetch(service.image).then((response) => {
        if (!response.ok) throw new Error('Image unavailable');
        return response.blob();
      }).then((blob) => {
        if (blob.type !== 'image/png' || !blob.size) throw new Error('Invalid image');
        return new File([blob], service.filename, { type: 'image/png' });
      }).catch((error) => {
        fileCache.delete(service.image);
        throw error;
      });
      fileCache.set(service.image, request);
    }
    return fileCache.get(service.image);
  };

  const releasePreview = () => {
    if (previewURL) URL.revokeObjectURL(previewURL);
    previewURL = undefined;
    preview.removeAttribute('src');
    preview.hidden = true;
  };

  const prepare = async (trigger) => {
    const request = ++selection;
    activeFile = undefined;
    activeService = undefined;
    fileSharing = false;
    releasePreview();
    const name = trigger.closest('.service-card').querySelector('h3').textContent;
    title.textContent = `Compartir ${name}`;
    urlInput.value = new URL(`#servicio-${trigger.dataset.share}`, canonical).href;
    download.href = trigger.href;
    download.download = trigger.download;
    feedback.textContent = '';
    retryButton.hidden = true;
    nativeButton.hidden = true;
    nativeButton.disabled = false;
    loading.hidden = false;
    loading.textContent = 'Preparando imagen…';
    hint.textContent = 'Descarga la imagen para publicarla y acompáñala con el enlace.';
    try {
      const services = await readManifest();
      const service = services.find((entry) => entry.key === trigger.dataset.share);
      if (!service) throw new Error('Unknown service');
      const file = await readFile(service);
      if (selection !== request || !dialog.open) return;
      activeService = service;
      activeFile = file;
      previewURL = URL.createObjectURL(file);
      preview.alt = service.alt;
      preview.src = previewURL;
      await preview.decode();
      if (selection !== request || !dialog.open) return;
      loading.hidden = true;
      preview.hidden = false;
      download.href = previewURL;
      download.download = service.filename;
      urlInput.value = service.url;
      if (typeof navigator.share === 'function') {
        try {
          fileSharing = typeof navigator.canShare === 'function' && navigator.canShare({ files: [file] });
        } catch { fileSharing = false; }
        nativeButton.textContent = fileSharing ? 'Compartir imagen' : 'Compartir enlace';
        nativeButton.hidden = false;
        hint.textContent = fileSharing
          ? 'Elige la app y confirma el envío. También puedes descargar el PNG para tus estados.'
          : 'Para publicar la imagen en historias o estados, descarga el PNG. El menú comparte el enlace.';
      }
    } catch {
      if (selection !== request || !dialog.open) return;
      if (activeService?.image) fileCache.delete(activeService.image);
      releasePreview();
      activeFile = undefined;
      activeService = undefined;
      loading.textContent = 'No se pudo preparar la vista previa.';
      feedback.textContent = 'Puedes volver a intentarlo. El enlace del servicio sigue disponible para copiar.';
      retryButton.hidden = false;
    }
  };

  document.querySelectorAll('[data-share]').forEach((trigger) => {
    trigger.setAttribute('aria-haspopup', 'dialog');
    trigger.setAttribute('aria-controls', 'share-dialog');
    trigger.addEventListener('click', (event) => {
      // Modified clicks retain the browser's normal download/open-link behavior.
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      opener = trigger;
      dialog.showModal();
      document.body.classList.add('share-dialog-open');
      prepare(trigger);
    });
  });

  dialog.querySelector('.share-close').addEventListener('click', () => dialog.close());
  dialog.addEventListener('keydown', (event) => {
    if (event.key !== 'Tab') return;
    const controls = [...dialog.querySelectorAll('button:not(:disabled), a[href], input')]
      .filter((element) => element.getClientRects().length > 0);
    const first = controls[0];
    const last = controls[controls.length - 1];
    if (event.shiftKey && (document.activeElement === first || document.activeElement === dialog)) {
      event.preventDefault();
      last?.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first?.focus();
    }
  });
  dialog.addEventListener('click', (event) => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => {
    selection++;
    document.body.classList.remove('share-dialog-open');
    releasePreview();
    activeFile = undefined;
    activeService = undefined;
    opener?.focus({ preventScroll: true });
  });
  retryButton.addEventListener('click', () => { if (opener) prepare(opener); });

  nativeButton.addEventListener('click', async () => {
    if (!activeService || !activeFile || nativeButton.disabled) return;
    feedback.textContent = '';
    nativeButton.disabled = true;
    const request = selection;
    try {
      // Assets are prepared before this click to preserve the fresh user gesture.
      if (fileSharing) {
        await navigator.share({ files: [activeFile], title: activeService.title, text: activeService.text });
      } else {
        await navigator.share({ title: activeService.title, text: activeService.title, url: activeService.url });
      }
      if (dialog.open && selection === request) feedback.textContent = 'Listo. Puedes cerrar esta vista.';
    } catch (error) {
      if (error.name !== 'AbortError' && dialog.open && selection === request) {
        feedback.textContent = 'No se pudo abrir el menú para compartir. Puedes descargar la imagen o copiar el enlace.';
      }
    } finally {
      if (selection === request) nativeButton.disabled = false;
    }
  });

  copyButton.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(urlInput.value);
      feedback.textContent = 'Enlace copiado.';
    } catch {
      urlInput.focus();
      urlInput.select();
      feedback.textContent = 'Selecciona y copia el enlace de este servicio.';
    }
  });
})();
