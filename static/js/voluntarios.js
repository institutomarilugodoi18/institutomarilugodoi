document.addEventListener("DOMContentLoaded", function () {
  // --- Seleção segura do form (use um id no HTML se tiver, ex.: id="form-voluntarios")
  const form = document.querySelector("#form-voluntarios") || document.querySelector("form");
  if (!form) return;

  // --- Campos (tente adequar aos seus names/ids de Django Forms)
  const fields = {
    nome:
      document.querySelector("#id_nome") ||
      document.querySelector("[name='nome']") ||
      document.querySelector("#nome"),
    email:
      document.querySelector("#id_email") ||
      document.querySelector("[name='email']") ||
      document.querySelector("#email"),
    telefone:
      document.querySelector("#id_whatsapp") ||
      document.querySelector("[name='whatsapp']") ||
      document.querySelector("[name='telefone']") ||
      document.querySelector("#whatsapp") ||
      document.querySelector("#telefone"),
  };

  // --- Mensagem global (topo do card)
  const alertBox = document.createElement("div");
  alertBox.className = "alert alert-warning form-global-alert mb-4 d-none";
  alertBox.setAttribute("role", "alert");
  alertBox.textContent = "Corrija os campos destacados para enviar o formulário.";
  form.prepend(alertBox);

  // --- Regras
  const nomeRegex = /^(?=.{3,80}$)[A-Za-zÀ-ÿ'’´`^~.\- ]+$/;
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/i;
  const telRegex = /^\(\d{2}\)\s?\d{5}-\d{4}$/; // (99) 99999-9999

  // Helpers de feedback (.invalid-feedback do Bootstrap)
  function ensureFeedbackEl(input) {
    let fb = input.nextElementSibling;
    if (!fb || !fb.classList.contains("invalid-feedback")) {
      fb = document.createElement("div");
      fb.className = "invalid-feedback";
      input.insertAdjacentElement("afterend", fb);
    }
    return fb;
  }
  function setError(input, message) {
    const fb = ensureFeedbackEl(input);
    input.classList.add("is-invalid");
    fb.textContent = message;
  }
  function clearError(input) {
    input.classList.remove("is-invalid");
    const fb = input.nextElementSibling;
    if (fb && fb.classList.contains("invalid-feedback")) fb.textContent = "";
  }

  // Validações de cada campo
  function validateNome() {
    const el = fields.nome;
    if (!el) return true;
    const v = (el.value || "").trim();
    if (!v) { setError(el, "Informe seu nome completo."); return false; }
    if (!nomeRegex.test(v)) { setError(el, "Use apenas letras e espaços (mín. 3 caracteres)."); return false; }
    clearError(el); return true;
  }

  function validateEmail() {
    const el = fields.email;
    if (!el) return true;
    const v = (el.value || "").trim();
    if (!v) { setError(el, "Informe seu e-mail."); return false; }
    if (!emailRegex.test(v)) { setError(el, "E-mail inválido. Ex.: nome@exemplo.com"); return false; }
    clearError(el); return true;
  }

  function validateTelefone() {
    const el = fields.telefone;
    if (!el) return true;

    // Mantém apenas números e limita a 11 (DD + 9)
    let digits = (el.value || "").replace(/\D/g, "").slice(0, 11);

    // Aplica máscara (99) 99999-9999 conforme digita
    let masked = "";
    if (digits.length > 0) {
      masked = "(" + digits.slice(0, 2);
      if (digits.length >= 2) masked += ") ";
      if (digits.length > 2) masked += digits.slice(2, Math.min(7, digits.length));
      if (digits.length >= 7) masked += "-" + digits.slice(7);
    }
    el.value = masked;

    // Mensagens
    if (!digits) { setError(el, "Informe seu WhatsApp com DDD."); return false; }
    if (digits.length !== 11 || !telRegex.test(el.value)) {
      setError(el, "Telefone inválido. Use o formato (99) 99999-9999.");
      return false;
    }

    clearError(el);
    return true;
  }

  // Listeners (tempo real)
  fields.nome && ["input", "blur"].forEach(evt => fields.nome.addEventListener(evt, validateNome));
  fields.email && ["input", "blur"].forEach(evt => fields.email.addEventListener(evt, validateEmail));
  fields.telefone && ["input", "blur", "change"].forEach(evt => fields.telefone.addEventListener(evt, validateTelefone));

  // Impede envio se houver erros
  form.setAttribute("novalidate", "novalidate");
  form.addEventListener("submit", function (e) {
    const okNome = validateNome();
    const okEmail = validateEmail();
    const okTel = validateTelefone();
    const isValid = okNome && okEmail && okTel;

    if (!isValid) {
      e.preventDefault();
      alertBox.classList.remove("d-none");
      const firstInvalid = form.querySelector(".is-invalid");
      if (firstInvalid) firstInvalid.focus();
    } else {
      alertBox.classList.add("d-none");
    }
  });
});
