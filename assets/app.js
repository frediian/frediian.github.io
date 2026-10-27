(() => {
  'use strict';
  document.documentElement.classList.remove('no-js');

  const menuToggle = document.querySelector('.menu-toggle');
  const menu = document.querySelector('#main-menu');
  const closeMenu = () => {
    menuToggle.setAttribute('aria-expanded', 'false');
    menu.classList.remove('is-open');
  };
  menuToggle.addEventListener('click', () => {
    const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
    menuToggle.setAttribute('aria-expanded', String(!expanded));
    menu.classList.toggle('is-open', !expanded);
  });
  menu.addEventListener('click', (event) => {
    if (event.target.closest('a')) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && menu.classList.contains('is-open')) {
      closeMenu();
      menuToggle.focus();
    }
  });
  document.addEventListener('click', (event) => {
    if (!event.target.closest('.site-header')) closeMenu();
  });

  // Avoid a plaintext phone number and a crawlable contact href in the page.
  // This deters basic scrapers; any public WhatsApp destination can be decoded.
  const contactBytes = [98, 110, 100, 110, 111, 97, 111, 99, 96, 111, 97, 110];
  const contactMessages = {
    general: 'Hola, frediian. Me gustaría consultar sobre tus servicios de desarrollo y TI.',
    free: 'Hola, frediian. Me interesan las recomendaciones gratuitas. Mi consulta es: ',
    technical: 'Hola, frediian. Quisiera coordinar una consulta técnica con cita previa de USD 40 por 2 horas. Mi caso es: '
  };
  const contactStatus = document.querySelector('#contact-status');
  let statusTimer;
  document.querySelectorAll('[data-contact]').forEach((button) => {
    button.addEventListener('click', () => {
      const destination = contactBytes.map((byte) => String.fromCharCode(byte ^ 87)).join('');
      const url = new URL(destination, 'https://wa.me/');
      url.searchParams.set('text', contactMessages[button.dataset.contact] || contactMessages.general);
      const opened = window.open(url.href, '_blank', 'noopener,noreferrer');
      if (opened) opened.opener = null;
      contactStatus.textContent = 'Se solicitó abrir WhatsApp. Allí puedes enviar tu consulta y coordinar disponibilidad.';
      clearTimeout(statusTimer);
      statusTimer = setTimeout(() => { contactStatus.textContent = ''; }, 7000);
    });
  });

  const backToTop = document.querySelector('.back-to-top');
  const updateTopButton = () => { backToTop.hidden = window.scrollY < 480; };
  window.addEventListener('scroll', updateTopButton, { passive: true });
  updateTopButton();
  document.querySelector('#current-year').textContent = new Date().getFullYear();

  const video = document.querySelector('#profile-video');
  const videoToggle = document.querySelector('#video-toggle');
  const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
  const reducedData = navigator.connection?.saveData === true;
  let manuallyPaused = motionPreference.matches || reducedData;
  const updatePlaybackButton = () => {
    const playing = !video.paused;
    videoToggle.querySelector('.playback-symbol').textContent = playing ? 'Ⅱ' : '▷';
    videoToggle.querySelector('.playback-label').textContent = playing ? 'Pausar animación' : 'Reproducir animación';
  };
  const playVideo = () => video.play().catch(updatePlaybackButton);
  videoToggle.hidden = false;
  video.addEventListener('play', updatePlaybackButton);
  video.addEventListener('pause', updatePlaybackButton);
  video.addEventListener('error', () => {
    videoToggle.hidden = true;
    video.poster = 'assets/frediian-poster.webp';
  });
  videoToggle.addEventListener('click', () => {
    if (video.paused) {
      manuallyPaused = false;
      playVideo();
    } else {
      manuallyPaused = true;
      video.pause();
    }
  });
  motionPreference.addEventListener('change', (event) => {
    if (event.matches) {
      manuallyPaused = true;
      video.pause();
    }
  });
  // Keep the animation from consuming resources off screen or in another tab.
  const observer = new IntersectionObserver(([entry]) => {
    if (!entry.isIntersecting || document.hidden) video.pause();
    else if (!manuallyPaused) playVideo();
  }, { threshold: 0.1 });
  observer.observe(video);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) video.pause();
    else if (!manuallyPaused && video.getBoundingClientRect().bottom > 0 && video.getBoundingClientRect().top < window.innerHeight) playVideo();
  });
  updatePlaybackButton();
})();
