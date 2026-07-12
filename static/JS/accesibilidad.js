(function () {
  const STORAGE_KEYS = {
    contraste: 'a11y-alto-contraste',
    fuente: 'a11y-fuente',
    tts: 'a11y-tts',
    subrayar: 'a11y-subrayar-links'
  };

  const FUENTE_NIVELES = ['fuente-normal', 'fuente-grande', 'fuente-extra-grande'];
  const FUENTE_KEYS = ['normal', 'grande', 'extra-grande'];

  let ttsActivo = false;
  let ultimoTextoLeido = '';

  function getTextoElemento(el) {
    if (!el || el.closest('.a11y-panel') || el.closest('.a11y-toggle')) return '';
    const aria = el.getAttribute('aria-label');
    if (aria) return aria.trim();
    const tag = el.tagName.toLowerCase();
    if (tag === 'input' || tag === 'textarea') {
      const label = el.labels && el.labels[0] ? el.labels[0].textContent : '';
      const val = el.value || el.placeholder || '';
      return [label, val].filter(Boolean).join('. ').trim();
    }
    if (tag === 'select') {
      const label = el.labels && el.labels[0] ? el.labels[0].textContent : '';
      const opt = el.options[el.selectedIndex];
      return [label, opt ? opt.textContent : ''].filter(Boolean).join('. ').trim();
    }
    const txt = (el.textContent || '').replace(/\s+/g, ' ').trim();
    return txt.slice(0, 300);
  }

  function hablar(texto) {
    if (!ttsActivo || !texto || !window.speechSynthesis) return;
    if (texto === ultimoTextoLeido) return;
    ultimoTextoLeido = texto;
    window.speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(texto);
    u.lang = 'es-PE';
    u.rate = 0.95;
    u.onend = function () {
      setTimeout(function () { ultimoTextoLeido = ''; }, 500);
    };
    window.speechSynthesis.speak(u);
  }

  function onInteract(e) {
    const el = e.target.closest('button, a, h1, h2, h3, h4, h5, h6, label, [aria-label], input, select, textarea');
    if (!el) return;
    const texto = getTextoElemento(el);
    if (texto) hablar(texto);
  }

  function activarTTS(activo) {
    ttsActivo = activo;
    if (activo) {
      document.addEventListener('focusin', onInteract);
      document.addEventListener('click', onInteract);
    } else {
      document.removeEventListener('focusin', onInteract);
      document.removeEventListener('click', onInteract);
      if (window.speechSynthesis) window.speechSynthesis.cancel();
    }
    localStorage.setItem(STORAGE_KEYS.tts, activo ? '1' : '0');
    const btn = document.getElementById('a11y-tts-btn');
    if (btn) btn.classList.toggle('activo', activo);
  }

  function aplicarContraste(activo) {
    document.body.classList.toggle('alto-contraste', activo);
    localStorage.setItem(STORAGE_KEYS.contraste, activo ? '1' : '0');
    const btn = document.getElementById('a11y-contraste-btn');
    if (btn) btn.classList.toggle('activo', activo);
  }

  function aplicarSubrayar(activo) {
    document.body.classList.toggle('subrayar-links', activo);
    localStorage.setItem(STORAGE_KEYS.subrayar, activo ? '1' : '0');
    const btn = document.getElementById('a11y-subrayar-btn');
    if (btn) btn.classList.toggle('activo', activo);
  }

  function aplicarFuente(nivel) {
    FUENTE_NIVELES.forEach(function (c) { document.body.classList.remove(c); });
    const idx = Math.max(0, Math.min(nivel, FUENTE_NIVELES.length - 1));
    document.body.classList.add(FUENTE_NIVELES[idx]);
    localStorage.setItem(STORAGE_KEYS.fuente, FUENTE_KEYS[idx]);
    document.querySelectorAll('.a11y-fuente-btns button').forEach(function (b, i) {
      b.classList.toggle('activo', i === idx);
    });
  }

  function restaurarEstado() {
    aplicarContraste(localStorage.getItem(STORAGE_KEYS.contraste) === '1');
    aplicarSubrayar(localStorage.getItem(STORAGE_KEYS.subrayar) === '1');
    const fuenteKey = localStorage.getItem(STORAGE_KEYS.fuente) || 'normal';
    const idx = FUENTE_KEYS.indexOf(fuenteKey);
    aplicarFuente(idx >= 0 ? idx : 0);
    activarTTS(localStorage.getItem(STORAGE_KEYS.tts) === '1');
  }

  function togglePanel() {
    const panel = document.getElementById('a11y-panel');
    if (panel) panel.classList.toggle('abierto');
  }

  document.addEventListener('DOMContentLoaded', function () {
    restaurarEstado();

    const toggleBtn = document.getElementById('a11y-toggle-btn');
    if (toggleBtn) toggleBtn.addEventListener('click', togglePanel);

    const contrasteBtn = document.getElementById('a11y-contraste-btn');
    if (contrasteBtn) {
      contrasteBtn.addEventListener('click', function () {
        aplicarContraste(!document.body.classList.contains('alto-contraste'));
      });
    }

    const subrayarBtn = document.getElementById('a11y-subrayar-btn');
    if (subrayarBtn) {
      subrayarBtn.addEventListener('click', function () {
        aplicarSubrayar(!document.body.classList.contains('subrayar-links'));
      });
    }

    const ttsBtn = document.getElementById('a11y-tts-btn');
    if (ttsBtn) {
      ttsBtn.addEventListener('click', function () {
        activarTTS(!ttsActivo);
      });
    }

    document.querySelectorAll('.a11y-fuente-btns button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        aplicarFuente(parseInt(btn.dataset.nivel, 10));
      });
    });

    document.addEventListener('click', function (e) {
      const panel = document.getElementById('a11y-panel');
      const toggle = document.getElementById('a11y-toggle-btn');
      if (panel && panel.classList.contains('abierto') &&
          !panel.contains(e.target) && e.target !== toggle && !toggle.contains(e.target)) {
        panel.classList.remove('abierto');
      }
    });
  });
})();
