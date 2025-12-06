// Inicia a validação quando o DOM estiver pronto
document.addEventListener("DOMContentLoaded", initValidationEventForm);

// ---------- APOIO DE DOM e ERROS ----------
function getId(id) {
  return document.getElementById(id);
}

function createErrorElementIfNeeded(errorId) {
  let el = document.getElementById(errorId);
  if (!el) {
    el = document.createElement("div");
    el.id = errorId;
    el.className = "validation-error";
    el.setAttribute("role", "alert");
    el.setAttribute("aria-live", "assertive");
  }
  return el;
}

function showValidationError(elId, errId, message) {
  const el = document.getElementById(elId);
  if (!el) return;

  el.setAttribute("aria-invalid", "true");
  const errEl = createErrorElementIfNeeded(errId);
  errEl.textContent = message || "";

  // Associado para leitores de tela
  const described = el.getAttribute("aria-describedby") || "";
  if (!described.includes(errId)) {
    const newVal = described ? `${described} ${errId}` : errId;
    el.setAttribute("aria-describedby", newVal);
  }

  // Insere uma mensagem de erro depois após o campo
  if (!document.getElementById(errId)) {
    if (el.nextSibling) el.parentNode.insertBefore(errEl, el.nextSibling);
    else el.parentNode.appendChild(errEl);
  }

  el.classList && el.classList.add("is-invalid");
}

function clearValidationError(elId, errId) {
  const el = document.getElementById(elId);
  if (!el) return;

  el.removeAttribute("aria-invalid");

  // Remove o id do aria-describedby
  const described = (el.getAttribute("aria-describedby") || "")
    .split(" ")
    .filter(Boolean)
    .filter((id) => id !== errId);
  if (described.length)
    el.setAttribute("aria-describedby", described.join(" "));
  else el.removeAttribute("aria-describedby");

  // Remove o elemento de erro do DOM
  const errEl = document.getElementById(errId);
  if (errEl && errEl.parentNode) errEl.parentNode.removeChild(errEl);

  el.classList && el.classList.remove("is-invalid");
}

// Trim seguro
function _safeTrim(v) {
  return typeof v === "string" ? v.trim() : "";
}

// ---------- FUNÇÕES DE VALIDAÇÃO ----------
function validateEventName(nome) {
  // 5 a 100 caracteres — letras, números, espaço e .,'- caracteres comuns
  const nomeRegex = /^[A-Za-zÀ-ÖØ-öø-ÿ0-9\s.,'\-]{5,100}$/;
  return nomeRegex.test(nome);
}

function validateEventDateTime(data, hora) {
  if (!data || !hora) return false;
  const iso = `${data}T${hora}`;
  const dt = new Date(iso);
  if (!dt || isNaN(dt.getTime())) return false;
  return dt.getTime() > new Date().getTime();
}

// ---------- VALIDAÇÕES UTEIS ----------
/**
 * Configura validação simples (blur + input)
 * inputElement: elemento DOM
 */
function setupInputValidation(
  inputElement,
  errorMessage,
  customValidationFn = null,
  customErrorMessage = ""
) {
  if (!inputElement || !inputElement.id) return;
  const inputId = inputElement.id;
  const errId = `${inputId}-error`;

  inputElement.addEventListener("blur", function () {
    const value = _safeTrim(this.value);

    if (!value) {
      showValidationError(inputId, errId, errorMessage);
      return;
    }

    if (customValidationFn && !customValidationFn(value)) {
      showValidationError(inputId, errId, customErrorMessage || errorMessage);
      return;
    }

    clearValidationError(inputId, errId);
  });

  inputElement.addEventListener("input", function () {
    clearValidationError(inputId, errId);
  });
}

// Inicializador do formulário de evento
function initValidationEventForm() {
  const formulario = document.querySelector("#form-event");
  if (!formulario) return;

  // Recuperar elementos (alguns são opcionais no form)
  const e = (id) => document.getElementById(id);
  const eventNameInput = e("event-name");
  const eventCategorySelect = e("event-category");
  const eventDescriptionInput = e("event-description");
  const whatsappGroupInput = e("whatsapp-group");
  const eventTagsInput = e("event-tags");
  const eventDateInput = e("event-date");
  const eventTimeInput = e("event-time");
  const eventAddressInput = e("event-address");
  const eventAddressNumberInput = e("event-address-number");
  const eventZipCodeInput = e("event-zip-code");
  const eventNeighborhoodInput = e("event-neighborhood");
  const eventCityInput = e("event-city");
  const eventStateInput = e("event-state");
  const eventMeetingInput = e("event-meeting");
  const eventMeetingDateInput = e("event-meeting-date");
  const eventMeetingTimeInput = e("event-meeting-time");
  const eventMeetingDescriptionInput = e("event-meeting-description");
  const eventMembersInput = e("event-members");
  const eventPhotoInput = e("event-photo");
  const eventPhotoPreview = e("event-photo-preview");
  const eventRulesInput = e("event-rules");
  const acceptPoliciesCheckbox = e("accept-policies");

  // Mensagens padrão reutilizáveis
  const messages = {
    required: "Campo obrigatório.",
    nameInvalid: "Nome inválido — 5 a 100 caracteres.",
    dateFuture: "A data e hora do evento devem ser futuras.",
    meetingDateFuture: "A data/hora do ponto de encontro devem ser futuras.",
    membersPositive: "A capacidade de membros deve ser um número positivo.",
    photoType: "Formato inválido. Use JPG, PNG ou WEBP.",
    photoMaxSize: "A imagem deve ter no máximo 5 MB.",
  };

  // Conectar validação nos inputs usando setupInputValidation
  if (eventNameInput)
    setupInputValidation(
      eventNameInput,
      "O nome do evento é obrigatório.",
      validateEventName,
      messages.nameInvalid
    );
  if (eventCategorySelect)
    setupInputValidation(
      eventCategorySelect,
      "A categoria do evento é obrigatória."
    );
  if (eventDescriptionInput)
    setupInputValidation(
      eventDescriptionInput,
      "A descrição do evento é obrigatória."
    );
  if (whatsappGroupInput)
    setupInputValidation(
      whatsappGroupInput,
      "O link do grupo do WhatsApp é obrigatório."
    );
  if (eventTagsInput)
    setupInputValidation(eventTagsInput, "As tags do evento são obrigatórias.");
  if (eventAddressInput)
    setupInputValidation(eventAddressInput, "O endereço é obrigatório.");
  if (eventAddressNumberInput)
    setupInputValidation(
      eventAddressNumberInput,
      "O número do endereço é obrigatório."
    );
  if (eventZipCodeInput)
    setupInputValidation(eventZipCodeInput, "O CEP é obrigatório.");
  if (eventNeighborhoodInput)
    setupInputValidation(eventNeighborhoodInput, "O bairro é obrigatório.");
  if (eventCityInput)
    setupInputValidation(eventCityInput, "A cidade é obrigatória.");
  if (eventMeetingInput)
    setupInputValidation(
      eventMeetingInput,
      "O ponto de encontro é obrigatório."
    );
  if (eventMeetingDescriptionInput)
    setupInputValidation(
      eventMeetingDescriptionInput,
      "A descrição do ponto de encontro é obrigatória."
    );

  if (eventMembersInput) {
    eventMembersInput.addEventListener("blur", function () {
      const v = _safeTrim(this.value);
      if (!v || isNaN(v) || parseInt(v, 10) <= 0)
        showValidationError(
          "event-members",
          "event-members-error",
          messages.membersPositive
        );
      else clearValidationError("event-members", "event-members-error");
    });
    eventMembersInput.addEventListener("input", () =>
      clearValidationError("event-members", "event-members-error")
    );
  }

  // Data e hora
  if (eventDateInput && eventTimeInput) {
    const checkDateTime = () => {
      const d = _safeTrim(eventDateInput.value);
      const t = _safeTrim(eventTimeInput.value);
      if (d && t && !validateEventDateTime(d, t))
        showValidationError(
          "event-date",
          "event-date-error",
          messages.dateFuture
        );
      else clearValidationError("event-date", "event-date-error");
    };
    eventDateInput.addEventListener("blur", checkDateTime);
    eventTimeInput.addEventListener("blur", checkDateTime);
  }

  if (eventMeetingDateInput && eventMeetingTimeInput) {
    const checkMeetingDateTime = () => {
      const d = _safeTrim(eventMeetingDateInput.value);
      const t = _safeTrim(eventMeetingTimeInput.value);
      if (d && t && !validateEventDateTime(d, t))
        showValidationError(
          "event-meeting-date",
          "event-meeting-date-error",
          messages.meetingDateFuture
        );
      else
        clearValidationError("event-meeting-date", "event-meeting-date-error");
    };
    eventMeetingDateInput.addEventListener("blur", checkMeetingDateTime);
    eventMeetingTimeInput.addEventListener("blur", checkMeetingDateTime);
  }

  // Foto (preview + validação no momento da seleção)
  if (eventPhotoInput) {
    const allowedTypes = ["image/jpeg", "image/png", "image/webp"];
    const maxSize = 5 * 1024 * 1024;

    eventPhotoInput.addEventListener("change", function () {
      clearValidationError("event-photo", "event-photo-error");
      const file = this.files && this.files[0];
      if (!file) {
        if (eventPhotoPreview) eventPhotoPreview.removeAttribute("src");
        return;
      }

      if (!allowedTypes.includes(file.type)) {
        this.value = "";
        showValidationError(
          "event-photo",
          "event-photo-error",
          messages.photoType
        );
        if (eventPhotoPreview) eventPhotoPreview.removeAttribute("src");
        return;
      }

      if (file.size > maxSize) {
        this.value = "";
        showValidationError(
          "event-photo",
          "event-photo-error",
          messages.photoMaxSize
        );
        if (eventPhotoPreview) eventPhotoPreview.removeAttribute("src");
        return;
      }

      if (eventPhotoPreview) {
        const reader = new FileReader();
        reader.onload = function (ev) {
          eventPhotoPreview.src = ev.target.result;
        };
        reader.readAsDataURL(file);
      }
    });
  }

  // Evitar mensagens nativas do navegador — manter HTML5
  (function preventNativeTooltips() {
    const all = formulario.querySelectorAll("input, select, textarea");
    all.forEach((el) => {
      el.addEventListener(
        "invalid",
        function (e) {
          e.preventDefault();
          this.setCustomValidity(" ");
        },
        true
      );
      const clear = function () {
        this.setCustomValidity("");
        clearValidationError(this.id, `${this.id}-error`);
      };
      if (el.type === "checkbox") el.addEventListener("change", clear);
      else el.addEventListener("input", clear);
    });
  })();

  // ====== SUBMIT ======
  formulario.addEventListener("submit", function (ev) {
    let hasError = false;
    let firstEl = null;

    const markError = (id, errId, msg) => {
      showValidationError(id, errId, msg);
      if (!firstEl) firstEl = getId(id);
      hasError = true;
    };

    const get = (id) => document.getElementById(id);

    // Nome
    if (eventNameInput) {
      const v = _safeTrim(eventNameInput.value);
      if (!v)
        markError(
          "event-name",
          "event-name-error",
          "O nome do evento é obrigatório."
        );
      else if (!validateEventName(v))
        markError("event-name", "event-name-error", messages.nameInvalid);
    }

    // Categoria
    if (eventCategorySelect && !eventCategorySelect.value)
      markError(
        "event-category",
        "event-category-error",
        "A categoria do evento é obrigatória."
      );

    // Descrição
    if (eventDescriptionInput && !eventDescriptionInput.value.trim())
      markError(
        "event-description",
        "event-description-error",
        "A descrição do evento é obrigatória."
      );

    // Aceitar políticas
    if (acceptPoliciesCheckbox && !acceptPoliciesCheckbox.checked)
      markError(
        "accept-policies",
        "accept-policies-error",
        "Você deve aceitar as políticas para continuar."
      );

    // CEP
    if (eventZipCodeInput) {
      const z = _safeTrim(eventZipCodeInput.value);
      const zipRegex = /^\d{5}-?\d{3}$/;
      if (!z)
        markError(
          "event-zip-code",
          "event-zip-code-error",
          "O CEP é obrigatório."
        );
      else if (!zipRegex.test(z))
        markError("event-zip-code", "event-zip-code-error", "CEP inválido.");
    }

    // Endereço
    if (eventAddressInput && !eventAddressInput.value.trim())
      markError(
        "event-address",
        "event-address-error",
        "O endereço é obrigatório."
      );
    if (eventAddressNumberInput) {
      const num = _safeTrim(eventAddressNumberInput.value);
      if (!num)
        markError(
          "event-address-number",
          "event-address-number-error",
          "O número do endereço é obrigatório."
        );
      else if (isNaN(num) || parseInt(num, 10) <= 0)
        markError(
          "event-address-number",
          "event-address-number-error",
          "Número do endereço inválido."
        );
    }

    // Cidade
    if (eventCityInput && !eventCityInput.value.trim())
      markError("event-city", "event-city-error", "A cidade é obrigatória.");

    // Estado
    if (eventStateInput && !eventStateInput.value.trim())
      markError("event-state", "event-state-error", "O estado é obrigatório.");

    // Data e hora do evento
    if (eventDateInput || eventTimeInput) {
      const d = eventDateInput ? _safeTrim(eventDateInput.value) : "";
      const t = eventTimeInput ? _safeTrim(eventTimeInput.value) : "";
      if (!d || !t)
        markError(
          "event-date",
          "event-date-error",
          "Data e hora do evento são obrigatórias."
        );
      else if (!validateEventDateTime(d, t))
        markError("event-date", "event-date-error", messages.dateFuture);
    }

    // Capacidade
    if (eventMembersInput) {
      const m = _safeTrim(eventMembersInput.value);
      if (!m)
        markError(
          "event-members",
          "event-members-error",
          "A capacidade de membros é obrigatória."
        );
      else if (isNaN(m) || parseInt(m, 10) <= 0)
        markError(
          "event-members",
          "event-members-error",
          messages.membersPositive
        );
    }

    // WhatsApp
    if (whatsappGroupInput && !whatsappGroupInput.value.trim())
      markError(
        "whatsapp-group",
        "whatsapp-group-error",
        "O link do grupo do WhatsApp é obrigatório."
      );

    // Tags
    if (eventTagsInput && !eventTagsInput.value.trim())
      markError(
        "event-tags",
        "event-tags-error",
        "As tags do evento são obrigatórias."
      );

    // Foto selecionada (se existir)
    if (eventPhotoInput) {
      const file = eventPhotoInput.files && eventPhotoInput.files[0];
      if (file) {
        const allowed = ["image/jpeg", "image/png", "image/webp"];
        if (!allowed.includes(file.type))
          markError("event-photo", "event-photo-error", messages.photoType);
        else if (file.size > 5 * 1024 * 1024)
          markError("event-photo", "event-photo-error", messages.photoMaxSize);
      }
    }

    // Regras
    if (
      eventRulesInput &&
      eventRulesInput.value &&
      eventRulesInput.value.length > 1000
    )
      markError(
        "event-rules",
        "event-rules-error",
        "As regras devem ter no máximo 1000 caracteres."
      );

    // Meeting (opcional) — se preenchido deve ser válido
    if (eventMeetingDateInput || eventMeetingTimeInput) {
      const md = eventMeetingDateInput
        ? _safeTrim(eventMeetingDateInput.value)
        : "";
      const mt = eventMeetingTimeInput
        ? _safeTrim(eventMeetingTimeInput.value)
        : "";
      if ((md && !mt) || (!md && mt))
        markError(
          "event-meeting-date",
          "event-meeting-date-error",
          "Preencha data e hora do ponto de encontro juntos."
        );
      else if (md && mt && !validateEventDateTime(md, mt))
        markError(
          "event-meeting-date",
          "event-meeting-date-error",
          messages.meetingDateFuture
        );
    }

    // Se tem erro, evitar enviar e focar no primeiro campo
    if (hasError) {
      ev.preventDefault();
      if (firstEl && typeof firstEl.focus === "function") {
        try {
          firstEl.focus();
          firstEl.scrollIntoView({ behavior: "smooth", block: "center" });
        } catch (er) {}
      }
    }
  });
}
