// Leitor de Texto (Web Speech API)
// - Lê seleção ou conteúdo do #conteudo-principal
// - Ignora áreas dinâmicas (carrossel etc.) usando [data-tts-ignore] e seletores
// - Retoma de onde parou mesmo se o DOM variar levemente (âncora de contexto)

(function () {
  const btnLer = document.getElementById('tts-ler');
  const btnParar = document.getElementById('tts-parar');

  const hasTTS = 'speechSynthesis' in window && 'SpeechSynthesisUtterance' in window;
  if (!hasTTS) {
    if (btnLer) { btnLer.disabled = true; btnLer.title = 'Leitor não suportado neste navegador.'; }
    if (btnParar) { btnParar.disabled = true; btnParar.title = 'Leitor não suportado neste navegador.'; }
    return;
  }

  // ==== Estado ====
  let voices = [];
  let currentUtter = null;
  let isSpeaking = false;

  const resumeState = {
    baseText: '',     // texto base da última leitura
    source: '',       // 'selection' | 'main' | 'body'
    lastIndex: 0,     // índice absoluto no baseText
    anchor: ''        // trecho usado para realinhar após mudanças no DOM
  };

  // ==== Voz ====
  function loadVoices() { voices = window.speechSynthesis.getVoices() || []; }
  loadVoices();
  window.speechSynthesis.onvoiceschanged = loadVoices;

  function pickFemalePtBrVoice() {
    if (!voices || !voices.length) return null;
    const preferredNames = [
      'Google português do Brasil',
      'Microsoft Maria - Portuguese (Brazil)',
      'Microsoft Leticia - Portuguese (Brazil)',
      'Luciana', 'Camila'
    ];
    for (const name of preferredNames) {
      const v = voices.find(voice => voice.name.toLowerCase().includes(name.toLowerCase()));
      if (v) return v;
    }
    const femalePtBr = voices.find(v => /pt-BR/i.test(v.lang) && /feminina|female|woman/i.test(v.name));
    if (femalePtBr) return femalePtBr;
    const anyPtBr = voices.find(v => /pt-BR/i.test(v.lang));
    if (anyPtBr) return anyPtBr;
    const anyPt = voices.find(v => /^pt/i.test(v.lang));
    if (anyPt) return anyPt;
    return voices[0] || null;
  }

  // ==== Captura de texto ====
  function normalizeText(txt) {
    return (txt || '').replace(/\s+/g, ' ').trim();
  }

  function getSelectionText() {
    const sel = window.getSelection && window.getSelection().toString();
    return normalizeText(sel);
  }

  // Extrai texto do main excluindo áreas dinâmicas
  function getMainText() {
    const main = document.getElementById('conteudo-principal');
    if (!main) return '';

    // Clona e remove partes dinâmicas
    const clone = main.cloneNode(true);
    const removeSel = [
      '[data-tts-ignore]',
      '.carousel', '.carousel-inner', '.carousel-item', '.carousel-caption',
      'script', 'style', 'noscript'
    ].join(',');

    clone.querySelectorAll(removeSel).forEach(el => el.remove());

    const txt = clone.innerText || clone.textContent || '';
    return normalizeText(txt);
  }

  function getBodyText() {
    const body = document.body;
    if (!body) return '';
    const clone = body.cloneNode(true);
    const removeSel = [
      '[data-tts-ignore]',
      '.carousel', '.carousel-inner', '.carousel-item', '.carousel-caption',
      'script', 'style', 'noscript',
      '#navbarSupportedContent', 'nav', 'footer' // opcional: evita ler nave e rodapé no fallback
    ].join(',');

    clone.querySelectorAll(removeSel).forEach(el => el.remove());
    const txt = clone.innerText || clone.textContent || '';
    return normalizeText(txt);
  }

  function computeBaseText() {
    const sel = getSelectionText();
    if (sel) return { text: sel, source: 'selection' };

    const main = getMainText();
    if (main) return { text: main, source: 'main' };

    return { text: getBodyText(), source: 'body' };
  }

  // ==== UI ====
  function updateUI() {
    if (!btnLer) return;
    if (isSpeaking) {
      btnLer.setAttribute('aria-label', 'Lendo...');
      btnLer.title = 'Lendo...';
      btnLer.disabled = true;
    } else {
      const hasResume = resumeState.baseText && resumeState.lastIndex > 0 && resumeState.lastIndex < resumeState.baseText.length;
      const thereIsSelection = !!getSelectionText();
      if (hasResume && !thereIsSelection) {
        btnLer.setAttribute('aria-label', 'Continuar leitura');
        btnLer.title = 'Continuar leitura';
        const label = btnLer.querySelector('.tts-label'); if (label) label.textContent = 'Continuar';
      } else {
        btnLer.setAttribute('aria-label', 'Ler');
        btnLer.title = 'Ler';
        const label = btnLer.querySelector('.tts-label'); if (label) label.textContent = 'Ler';
      }
      btnLer.disabled = false;
    }
  }

  // ==== Fala ====
  function makeAnchor(text, index) {
    // trecho curto após o ponto atual para realinhar em DOM mutável
    const start = Math.max(0, index);
    return text.slice(start, start + 80); // 80 chars de contexto é suficiente
  }

  function realignIndexWithAnchor(newText, fallbackIndex, anchor) {
    if (!anchor) return fallbackIndex;
    const pos = newText.indexOf(anchor);
    if (pos !== -1) return pos; // achou o trecho exato
    // Fallback simples: mantém índice se estiver em faixa válida
    if (fallbackIndex >= 0 && fallbackIndex < newText.length) return fallbackIndex;
    return 0;
  }

  function speakFrom(text, startIndex, source) {
    if (!text) return;

    const idx = Math.max(0, Math.min(startIndex || 0, text.length));
    const remaining = text.slice(idx);
    if (!remaining) return;

    window.speechSynthesis.cancel();

    const utter = new SpeechSynthesisUtterance(remaining);
    currentUtter = utter;

    const voice = pickFemalePtBrVoice();
    if (voice) utter.voice = voice;
    utter.lang = (voice && voice.lang) || 'pt-BR';
    utter.rate = 1;
    utter.pitch = 1;

    // Atualiza estado de retomada
    resumeState.baseText = text;
    resumeState.source = source;
    resumeState.lastIndex = idx;
    resumeState.anchor = makeAnchor(text, idx);

    utter.onboundary = function (e) {
      if (typeof e.charIndex === 'number') {
        resumeState.lastIndex = idx + e.charIndex;
        resumeState.anchor = makeAnchor(text, resumeState.lastIndex);
      }
    };

    utter.onstart = function () { isSpeaking = true; updateUI(); };
    utter.onend = function () {
      isSpeaking = false;
      if (resumeState.lastIndex >= resumeState.baseText.length - 1) {
        resumeState.lastIndex = 0;
        resumeState.anchor = '';
      }
      updateUI();
    };
    utter.onerror = function () { isSpeaking = false; updateUI(); };

    window.speechSynthesis.speak(utter);
  }

  // ==== Eventos ====
  if (btnLer) {
    btnLer.addEventListener('click', function () {
      const sel = getSelectionText();
      if (sel) {
        speakFrom(sel, 0, 'selection');
        return;
      }

      const { text: computedText, source } = computeBaseText();

      // Tenta realinhar pelo âncora, mesmo que o texto-base tenha mudado um pouco (carrossel etc.)
      const startAt = realignIndexWithAnchor(
        computedText,
        resumeState.lastIndex,
        resumeState.anchor
      );

      speakFrom(computedText, startAt, source);
    });
  }

  if (btnParar) {
    btnParar.addEventListener('click', function () {
      window.speechSynthesis.cancel();
      isSpeaking = false;
      updateUI();
    });
  }

  updateUI();
})();
