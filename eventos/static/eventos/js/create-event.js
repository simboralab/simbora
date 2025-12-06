// Preview de imagem ao selecionar arquivo
const coverImageInput = document.getElementById("cover-image");
const imagePreview = document.getElementById("image-preview");
const previewImg = document.getElementById("preview-img");
const removeImageBtn = document.getElementById("remove-image");
const fileLabel = document.querySelector(".file-label");

if (
  coverImageInput &&
  imagePreview &&
  previewImg &&
  removeImageBtn &&
  fileLabel
) {
  coverImageInput.addEventListener("change", function (e) {
    const file = e.target.files[0];
    if (file) {
      // Validação de tamanho (2MB)
      if (file.size > 2 * 1024 * 1024) {
        alert(
          "A imagem é muito grande. Por favor, selecione uma imagem menor que 2MB."
        );
        coverImageInput.value = "";
        return;
      }

      // Validação de tipo
      const allowedTypes = ["image/jpeg", "image/jpg", "image/png"];
      if (!allowedTypes.includes(file.type)) {
        alert("Por favor, selecione apenas arquivos JPEG ou PNG.");
        coverImageInput.value = "";
        return;
      }

      const reader = new FileReader();
      reader.onload = function (e) {
        previewImg.src = e.target.result;
        imagePreview.style.display = "block";
        fileLabel.style.display = "none";
      };
      reader.readAsDataURL(file);
    }
  });

  // Remover imagem
  removeImageBtn.addEventListener("click", function () {
    coverImageInput.value = "";
    imagePreview.style.display = "none";
    fileLabel.style.display = "flex";
    previewImg.src = "";
  });

  // Drag and drop
  const uploadContainer = document.querySelector(".image-upload-container");

  if (uploadContainer) {
    ["dragenter", "dragover", "dragleave", "drop"].forEach((eventName) => {
      uploadContainer.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
      e.preventDefault();
      e.stopPropagation();
    }

    ["dragenter", "dragover"].forEach((eventName) => {
      uploadContainer.addEventListener(eventName, highlight, false);
    });

    ["dragleave", "drop"].forEach((eventName) => {
      uploadContainer.addEventListener(eventName, unhighlight, false);
    });

    function highlight(e) {
      fileLabel.style.borderColor = "var(--azul-principal)";
      fileLabel.style.background = "rgba(0, 74, 173, 0.1)";
    }

    function unhighlight(e) {
      fileLabel.style.borderColor = "var(--cinza-medio)";
      fileLabel.style.background = "var(--cinza-claro)";
    }

    uploadContainer.addEventListener("drop", handleDrop, false);

    function handleDrop(e) {
      const dt = e.dataTransfer;
      const files = dt.files;

      if (files.length > 0) {
        coverImageInput.files = files;
        const event = new Event("change", { bubbles: true });
        coverImageInput.dispatchEvent(event);
      }
    }
  }
}

// Sistema de Tags
const tagsInput = document.getElementById("tags-input");
const tagsList = document.getElementById("tags-list");
const tagsArray = [];

if (tagsInput && tagsList) {
  tagsInput.addEventListener("keydown", function (e) {
    if (e.key === "Enter" || e.key === ",") {
      e.preventDefault();
      addTag();
    }
  });

  tagsInput.addEventListener("blur", function () {
    if (this.value.trim()) {
      addTag();
    }
  });

  function addTag() {
    const tagText = tagsInput.value.trim();

    if (
      tagText &&
      !tagsArray.includes(tagText.toLowerCase()) &&
      tagsArray.length < 5
    ) {
      tagsArray.push(tagText.toLowerCase());
      renderTags();
      tagsInput.value = "";
    } else if (tagsArray.length >= 5) {
      alert("Máximo de 5 tags permitidas.");
    }
  }

  function removeTag(tagToRemove) {
    const index = tagsArray.indexOf(tagToRemove.toLowerCase());
    if (index > -1) {
      tagsArray.splice(index, 1);
      renderTags();
    }
  }

  function renderTags() {
    tagsList.innerHTML = "";
    tagsArray.forEach((tag) => {
      const tagElement = document.createElement("div");
      tagElement.className = "tag-item";
      tagElement.innerHTML = `
                <span>${tag}</span>
                <button type="button" class="tag-remove" onclick="removeTagFromList('${tag}')">
                    <span class="material-symbols-rounded">close</span>
                </button>
            `;
      tagsList.appendChild(tagElement);
    });

    // Criar input hidden para enviar tags no formulário
    updateTagsInput();
  }

  function updateTagsInput() {
    // Remove inputs hidden antigos
    const oldInputs = document.querySelectorAll('input[name="tags[]"]');
    oldInputs.forEach((input) => input.remove());

    // Cria novos inputs hidden com as tags
    tagsArray.forEach((tag) => {
      const hiddenInput = document.createElement("input");
      hiddenInput.type = "hidden";
      hiddenInput.name = "tags[]";
      hiddenInput.value = tag;
      tagsList.appendChild(hiddenInput);
    });
  }

  // Função global para remover tag (chamada pelo onclick)
  window.removeTagFromList = function (tag) {
    removeTag(tag);
  };
}
