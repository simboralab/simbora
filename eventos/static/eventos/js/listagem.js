document.addEventListener('DOMContentLoaded', () => {
  const GRID_ID = 'listagem-grid';
  const PAGE_TITLE = document.getElementById('page-title');
  const searchForm = document.getElementById('global-search');
  const searchInput = document.getElementById('search-input');
  const filtersToolbar = document.getElementById('filters-toolbar');

  // páginasize / estado
  const PAGE_SIZE = 12;
  let currentPage = 1;
  let filtered = [];
  let loading = false;
  let allEventos = []; // Dados do backend
  let categoriasDisponiveis = ['Esporte','Lazer','Cultura','Tecnologia','Educação'];
  let cidadesDisponiveis = [];

  // URL base da API
  const API_URL = window.location.pathname;

  // le parâmetros da URL para determinar contexto
  const params = new URLSearchParams(window.location.search);
  const q = params.get('q') || '';
  const categoryParam = params.get('category') || '';
  const mode = params.get('mode') || (q ? 'search' : (categoryParam ? 'category' : 'explore'));

  // inicializa input de busca conforme URL
  if (searchInput) searchInput.value = q;

  // define título acorde ao contexto
  if (PAGE_TITLE) {
    if (mode === 'search') {
      PAGE_TITLE.textContent = `Resultados para "${q}"`;
    } else if (mode === 'category') {
      PAGE_TITLE.textContent = categoryParam || 'Categoria';
    } else {
      PAGE_TITLE.textContent = 'Explorar';
    }
  }

  // filtros dinâmicos
  const filters = {
    q: q,
    category: categoryParam,
    city: params.get('city') || '',
    price: params.get('price') || 'all',
    status: params.get('status') || '',
    dateRange: ''
  };

  // Carregar dados do backend
  loadEventos();

  // utilitário de toast pequeno para feedback (usado por fav/share)
  function showToast(message, timeout = 2200) {
    const t = document.createElement('div');
    t.className = 'lf-toast';
    t.textContent = message;
    t.style.cssText = 'position:fixed;bottom:20px;left:50%;transform:translateX(-50%);background:#0b2540;color:#fff;padding:10px 16px;border-radius:999px;box-shadow:0 6px 20px rgba(2,6,23,0.4);z-index:99999;font-weight:600;';
    document.body.appendChild(t);
    setTimeout(()=>{ t.style.opacity = '0'; t.style.transition = 'opacity 240ms ease'; setTimeout(()=> t.remove(), 260); }, timeout);
  }

  // Função para carregar eventos do backend
  async function loadEventos() {
    loading = true;
    try {
      const urlParams = new URLSearchParams();
      if (filters.q) urlParams.set('q', filters.q);
      if (filters.category) urlParams.set('category', filters.category);
      if (filters.city) urlParams.set('city', filters.city);
      if (filters.status) urlParams.set('status', filters.status);
      if (filters.price !== 'all') urlParams.set('price', filters.price);
      urlParams.set('format', 'json');

      const response = await fetch(`${API_URL}?${urlParams.toString()}`, {
        headers: {
          'X-Requested-With': 'XMLHttpRequest'
        }
      });

      if (!response.ok) {
        throw new Error('Erro ao carregar eventos');
      }

      const data = await response.json();
      allEventos = data.eventos || [];
      
      // Extrair cidades únicas dos eventos
      cidadesDisponiveis = uniqueValues(allEventos, 'city');
      
      // Aplicar filtros e renderizar
      applyAndRender();
      renderFilters();
    } catch (error) {
      console.error('Erro ao carregar eventos:', error);
      showToast('Erro ao carregar eventos. Tente novamente.');
      allEventos = [];
      applyAndRender();
    } finally {
      loading = false;
    }
  }

  // busca: atualiza URL e aplica filtro
  if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const val = searchInput.value.trim();
      filters.q = val;
      updateURL({ q: val, mode: val ? 'search' : 'explore' });
      loadEventos();
    });
  }

  // rolagem infinita (carrega mais)
  window.addEventListener('scroll', () => {
    if (loading) return;
    const nearBottom = window.innerHeight + window.scrollY >= document.body.offsetHeight - 600;
    if (nearBottom) loadMore();
  });

  // funções
  function renderFilters() {
    // construir filtros como pills com dropdown — Category, Cidade, Preço, Ordenar
    const categories = categoriasDisponiveis;
    const cities = cidadesDisponiveis;
    const priceOptions = [ {value:'all',label:'Todos'}, {value:'free',label:'Grátis'}, {value:'paid',label:'Pago'} ];
    const statusOptions = [ {value:'',label:'Todos'}, {value:'novo',label:'Novo'}, {value:'esgotado',label:'Esgotado'}, {value:'disponivel',label:'Disponível'} ];

    if (!filtersToolbar) return;
    filtersToolbar.innerHTML = '';

    // helper para criar pill com dropdown
    function makePill(key, label, options, selectedValue) {
      const pill = document.createElement('div');
      pill.className = 'pill filter-pill';
      pill.tabIndex = 0;
      pill.setAttribute('data-filter-key', key);
      pill.innerHTML = `<span class="pill-label">${label}</span> <span class="pill-value">${selectedValue || ''}</span>`;

      const dropdown = document.createElement('div');
      dropdown.className = 'filter-dropdown';

      const ul = document.createElement('ul');

      // se opções vierem com contagem (ex.: categorias), calcule as contagens
      const counts = {};
      if (key === 'category' || key === 'city') {
        options.forEach(opt => {
          const v = opt.value ?? opt;
          counts[v] = allEventos.filter(i => (key === 'category' ? i.category : i.city) === v).length;
        });
      } else if (key === 'status') {
        options.forEach(opt => {
          const v = opt.value ?? opt;
          if (!v) {
            counts[v] = allEventos.length;
          } else if (v === 'novo') {
            counts[v] = allEventos.filter(i => i.badges && i.badges.includes('Novo')).length;
          } else if (v === 'esgotado') {
            counts[v] = allEventos.filter(i => i.badges && i.badges.includes('Esgotado')).length;
          } else if (v === 'disponivel') {
            counts[v] = allEventos.filter(i => i.badges && i.badges.includes('Disponível')).length;
          } else {
            counts[v] = 0;
          }
        });
      }

      options.forEach(opt => {
        const li = document.createElement('li');
        li.className = 'filter-option';
        const val = opt.value ?? opt;
        const labelText = opt.label ?? opt;

        // checkbox visual
        li.innerHTML = `<label class="option-label"><input type="checkbox" class="option-checkbox" data-value="${val}"> <span class="opt-text">${labelText}</span> <span class="opt-count">${counts[val] ? '('+counts[val]+')' : ''}</span></label>`;

        li.addEventListener('click', (e)=>{
          e.stopPropagation();
          // toggle selection (single-select behaviour)
          const checkbox = li.querySelector('.option-checkbox');
          const wasChecked = checkbox.checked;
          // clear other checkboxes
          ul.querySelectorAll('.option-checkbox').forEach(cb=> cb.checked = false);
          checkbox.checked = !wasChecked;

          filters[key] = checkbox.checked ? val : '';
          if (key === 'category') updateURL({category: checkbox.checked ? val : ''});
          updatePillValue(pill, filters[key], checkbox.checked ? labelText : '');

          // Aplicar filtro imediatamente e fechar dropdown
          loadEventos();
          closeAllDropdowns();
        });

        ul.appendChild(li);
      });

      dropdown.appendChild(ul);

      // clear button aparecerá dentro da pill quando houver valor selecionado
      const clearBtn = document.createElement('button');
      clearBtn.className = 'pill-clear';
      clearBtn.setAttribute('aria-label', `Limpar filtro ${label}`);
      clearBtn.innerHTML = '&times;';
      clearBtn.style.display = selectedValue ? 'inline-flex' : 'none';
      pill.appendChild(clearBtn);

      // rodapé com ações para categoria (Visualizar / Limpar tudo)
      if (key === 'category'){
        const footer = document.createElement('div');
        footer.className = 'filter-dropdown-footer';
        footer.innerHTML = `<div class="footer-actions"><button class="btn-visualizar">Visualizar</button><button class="btn-limpar">Limpar tudo</button></div>`;
        footer.querySelector('.btn-visualizar').addEventListener('click',(e)=>{ e.stopPropagation(); closeAllDropdowns(); loadEventos(); });
        footer.querySelector('.btn-limpar').addEventListener('click',(e)=>{ e.stopPropagation(); filters.category = ''; updatePillValue(pill,'',''); ul.querySelectorAll('.option-checkbox').forEach(cb=> cb.checked = false); updateURL({category:''}); loadEventos(); closeAllDropdowns(); });
        dropdown.appendChild(footer);
      }

      pill.appendChild(dropdown);

      // abrir/fechar dropdown ao clicar no corpo da pill (exceto no botão limpar)
      pill.addEventListener('click', (e)=>{ 
        if (e.target.closest && e.target.closest('.pill-clear')) return; 
        e.stopPropagation(); 
        toggleDropdown(pill); 
      });
      pill.addEventListener('keydown', (e)=>{ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleDropdown(pill); } });

      // comportamento do botão limpar
      clearBtn.addEventListener('click', (e)=>{
        e.stopPropagation();
        filters[key] = '';
        updatePillValue(pill,'','');
        // limpar checkboxes no dropdown se existirem
        const ulEl = pill.querySelector('.filter-dropdown ul');
        if (ulEl) ulEl.querySelectorAll('.option-checkbox').forEach(cb=> cb.checked = false);
        if (key === 'category') updateURL({category: ''});
        updateURL({ [key]: '' });
        loadEventos();
      });

      return pill;
    }

    function updatePillValue(pill, value, label){
        const span = pill.querySelector('.pill-value');
        span.textContent = label || value || '';
        const clearBtn = pill.querySelector('.pill-clear');
        if (clearBtn) {
          clearBtn.style.display = (label || value) ? 'inline-flex' : 'none';
        }
        // atualizar visibilidade do limpar-tudo quando um pill muda (se a função existir)
        if (typeof updateClearAllVisibility === 'function') updateClearAllVisibility();
    }

    // Category pill: se a página já está filtrada por categoria (filters.category vindo da URL),
    // não renderizamos a pill de categoria — o usuário já selecionou a categoria na navegação inicial.
    const catOpts = [{value:'',label:'Todas as categorias'}].concat(categories.map(c=>({value:c,label:c})));
    if (!filters.category) {
      filtersToolbar.appendChild(makePill('category','Categoria',catOpts, filters.category));
    }

    // City pill
    const cityOpts = [{value:'',label:'Todas as cidades'}].concat(cities.map(c=>({value:c,label:c})));
    filtersToolbar.appendChild(makePill('city','Cidade',cityOpts, filters.city));

    // Price pill
    filtersToolbar.appendChild(makePill('price','Preço', priceOptions, filters.price));

    // Status pill (filtra por Novo / Esgotado)
    filtersToolbar.appendChild(makePill('status','Status', statusOptions, filters.status));

    // botão Limpar tudo (visível apenas quando há filtros ativos)
    const clearAllBtn = document.createElement('button');
    clearAllBtn.className = 'filters-clear-all';
    clearAllBtn.type = 'button';
    clearAllBtn.textContent = 'Limpar tudo';
    clearAllBtn.style.display = 'none';
    filtersToolbar.appendChild(clearAllBtn);

    function updateClearAllVisibility(){
      // não considere a category fixa (página de categoria) como motivo para mostrar "Limpar tudo"
      const categoryActive = Boolean(filters.category && filters.category !== '' && !window.__fixedCategory);
      const anySelected = Boolean(filters.q || categoryActive || (filters.city && filters.city !== '') || (filters.price && filters.price !== 'all') || (filters.status && filters.status !== '') || filters.dateRange);
      clearAllBtn.style.display = anySelected ? 'inline-flex' : 'none';
    }

    // inicializa visibilidade
    updateClearAllVisibility();

    clearAllBtn.addEventListener('click', (e)=>{
      e.stopPropagation();
      // resetar todos os filtros para valores padrão
      filters.q = '';
      // se a página define uma categoria fixa, não a removemos
      if (!window.__fixedCategory) {
        filters.category = '';
      }
      filters.city = '';
      filters.price = 'all';
      filters.status = '';
      filters.dateRange = '';

      // atualizar URL removendo params — preserve category quando fixa
      if (window.__fixedCategory) {
        updateURL({ q: '', city: '', price: '', status: '', dateRange: '' });
      } else {
        updateURL({ q: '', category: '', city: '', price: '', status: '', dateRange: '' });
      }

      // fechar quaisquer dropdowns abertos
      closeAllDropdowns();
      // limpar também o input de busca visível, se houver
      try { if (typeof fallbackSearchInput !== 'undefined' && fallbackSearchInput) fallbackSearchInput.value = ''; } catch(e){}
      try { if (typeof searchInput !== 'undefined' && searchInput) searchInput.value = ''; } catch(e){}
      // rerenderizar listagem e os próprios filtros
      loadEventos();
      renderFilters();
      // garantir atualização do estado do botão limpar-tudo
      if (typeof updateClearAllVisibility === 'function') updateClearAllVisibility();
    });

    // fechar dropdowns ao clicar fora
    document.addEventListener('click', closeAllDropdowns);

    function toggleDropdown(pill){
      const open = pill.classList.contains('open');
      closeAllDropdowns();
      if (!open) openDropdownPortal(pill);
    }

    function closeAllDropdowns(){
      const opened = document.querySelectorAll('.filter-pill.open');
      opened.forEach(el=> closeDropdownPortal(el));
    }

    // Comportamento de portal: mover o dropdown para o body para evitar recorte por elementos ancestrais
    function openDropdownPortal(pill){
      pill.classList.add('open');
      const dropdown = pill.querySelector('.filter-dropdown');
      if (!dropdown) return;

      // compute position relative to viewport
      const rect = pill.getBoundingClientRect();
      // remember original parent for later
      dropdown._originalParent = dropdown.parentElement;
      dropdown._originalNext = dropdown.nextSibling;

      // anexar ao body
      document.body.appendChild(dropdown);
      dropdown.style.minWidth = Math.max(220, rect.width) + 'px';
      // usar posicionamento fixed para que o dropdown seja relativo à viewport (evitar recorte por ancestrais)
      dropdown.style.position = 'fixed';
      // preferir a posição à esquerda, mas manter dentro da viewport
      const left = Math.min(window.innerWidth - 12 - Math.max(220, rect.width), Math.max(8, rect.left));
      dropdown.style.left = left + 'px';
      dropdown.style.top = (rect.bottom + 10) + 'px';
      dropdown.style.display = 'block';
      dropdown.classList.add('portal-open');

      // reposicionar ao rolar/redimensionar
      function reposition(){
        const r = pill.getBoundingClientRect();
        const left = Math.min(window.innerWidth - 12 - Math.max(220, r.width), Math.max(8, r.left));
        dropdown.style.left = left + 'px';
        dropdown.style.top = (r.bottom + 10) + 'px';
      }
      dropdown._reposition = reposition;
      window.addEventListener('scroll', reposition);
      window.addEventListener('resize', reposition);
    }

    function closeDropdownPortal(pill){
      pill.classList.remove('open');
      const dropdown = pill.querySelector('.filter-dropdown') || document.querySelector('.filter-dropdown.portal-open');
      if (!dropdown) return;

      // remover ouvintes de evento
      if (dropdown._reposition) {
        window.removeEventListener('scroll', dropdown._reposition);
        window.removeEventListener('resize', dropdown._reposition);
        delete dropdown._reposition;
      }

      // mover de volta para o pai original, se existir
      if (dropdown._originalParent) {
        if (dropdown._originalNext) dropdown._originalParent.insertBefore(dropdown, dropdown._originalNext);
        else dropdown._originalParent.appendChild(dropdown);
        delete dropdown._originalParent;
        delete dropdown._originalNext;
      }

      dropdown.style.position = '';
      dropdown.style.left = '';
      dropdown.style.top = '';
      dropdown.style.display = '';
      dropdown.classList.remove('portal-open');
    }
  }

  // --- Busca: fallback para inputs/buttons que existem fora da página ---
  // Se não houver um form com id "global-search", tentamos ligar ao input com classe .search-input
  const fallbackSearchInput = searchInput || document.querySelector('.search-input');
  const fallbackSearchButton = document.querySelector('.search-button');

  if (fallbackSearchInput) {
    // garantir que o input reflita o termo da URL
    fallbackSearchInput.value = filters.q || fallbackSearchInput.value || '';
    // Enter no input
    fallbackSearchInput.addEventListener('keypress', function(e){
      if (e.key === 'Enter'){
        e.preventDefault();
        const val = this.value.trim();
        filters.q = val;
        updateURL({ q: val, mode: val ? 'search' : 'explore' });
        loadEventos();
      }
    });
  }

  if (fallbackSearchButton && fallbackSearchInput) {
    fallbackSearchButton.addEventListener('click', function(e){
      e.preventDefault();
      const val = fallbackSearchInput.value.trim();
      filters.q = val;
      updateURL({ q: val, mode: val ? 'search' : 'explore' });
      loadEventos();
    });
  }

  function wrapFilter(labelText, control) {
    const wrap = document.createElement('div');
    wrap.className = 'filter-wrap';
    const label = document.createElement('label');
    label.textContent = labelText;
    label.style.display = 'block';
    label.style.fontSize = '0.9rem';
    label.style.marginBottom = '6px';
    wrap.appendChild(label);
    wrap.appendChild(control);
    return wrap;
  }

  function applyAndRender() {
    // Os filtros já são aplicados no backend, então apenas renderizamos
    filtered = allEventos;
    currentPage = 1;
    renderCardsPage();
  }

  function resetAndRender() { 
    currentPage = 1; 
    applyAndRender(); 
    window.scrollTo({top:0,behavior:'smooth'}); 
  }

  function renderCardsPage() {
    const grid = document.getElementById(GRID_ID);
    if (!grid) return;
    grid.innerHTML = '';
    const pageItems = filtered.slice(0, PAGE_SIZE * currentPage);
    pageItems.forEach(item => grid.appendChild(createCard(item)));

    // se houver mais, adiciona um botão de carregar mais
    const pagination = document.getElementById('pagination');
    if (pagination) pagination.innerHTML = '';
    if (filtered.length > PAGE_SIZE * currentPage) {
      const btn = document.createElement('button');
      btn.textContent = 'Carregar mais';
      btn.addEventListener('click', loadMore);
      if (pagination) pagination.appendChild(btn);
    }
  }

  function loadMore() {
    if (loading) return;
    if (filtered.length <= PAGE_SIZE * currentPage) return;
    loading = true;
    // simula loading
    setTimeout(()=>{
      currentPage++;
      renderCardsPage();
      loading = false;
    }, 350);
  }

  function createCard(item) {
    const card = document.createElement('article');
    card.className = 'card';
    card.tabIndex = 0;
    card.setAttribute('role','button');

    // wrapper para a mídia (garante posicionamento relativo para badges sobrepostos)
    const wrapper = document.createElement('div');
    wrapper.className = 'card-wrapper';

    const media = document.createElement('img');
    media.className = 'card-media';
    media.src = item.image || 'https://via.placeholder.com/800x450';
    media.alt = item.title;

    // badge overlay (ex: Grátis / Novo / Esgotado) - no canto superior direito
    if (item.badges && item.badges.length) {
      const btext = item.badges[0];
      const badge = document.createElement('div');
      const key = (btext || '').toString().toLowerCase();
      let extra = 'badge-default';
      if (key === 'novo') extra = 'badge-novo';
      if (key === 'esgotado') extra = 'badge-esgotado';
      badge.className = 'card-badge ' + extra;
      badge.textContent = btext;
      wrapper.appendChild(badge);
    }

    // badge de categoria sobre a imagem (canto superior esquerdo)
    if (item.category) {
      const cat = document.createElement('div');
      // criar slug seguro para classe (remover acentos e espaços)
      const slug = item.category ? item.category.normalize('NFD').replace(/\p{Diacritic}/gu, '').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'') : 'cat';
      cat.className = 'card-category cat-' + slug;
      cat.textContent = item.category;
      cat.setAttribute('title', `Filtrar por ${item.category}`);
      cat.setAttribute('role','button');
      cat.tabIndex = 0;

      // clique na badge filtra pela categoria (não navega para detalhes)
      cat.addEventListener('click', (e)=>{
        e.stopPropagation();
        filters.category = item.category;
        updateURL({ category: item.category, mode: 'category' });
        // rerenderiza resultados e filtros (oculta a pill de categoria automaticamente)
        loadEventos();
        renderFilters();
      });
      cat.addEventListener('keydown', (e)=>{ if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); cat.click(); } });

      wrapper.appendChild(cat);
    }

    wrapper.appendChild(media);
    card.appendChild(wrapper);

    const body = document.createElement('div');
    body.className = 'card-body';

    // Organização conforme referência: título, local (venue - city), data
    const title = document.createElement('div');
    title.className = 'card-title';
    // remover prefixo de categoria do título quando presente (ex: "Esporte Evento 1" -> "Evento 1")
    let displayTitle = item.title || '';
    if (item.category && displayTitle) {
      const esc = s => s.replace(/[.*+?^${}()|[\\]\\]/g, '\\$&');
      const re = new RegExp('^\\s*' + esc(item.category) + '[\\s:-]+', 'i');
      displayTitle = displayTitle.replace(re, '');
    }
    title.textContent = displayTitle;

    const location = document.createElement('div');
    location.className = 'card-location';
    // ex: "Arena Ratones - Florianópolis, SC"
    const venueText = item.venue || item.provider || '';
    location.textContent = venueText ? `${venueText} - ${item.city}` : item.city;

    const dateLine = document.createElement('div');
    dateLine.className = 'card-date';
    dateLine.textContent = item.date;

    // price/tags - manter como badge interno (se necessário)
    const tags = document.createElement('div');
    tags.className = 'card-tags';
    tags.innerHTML = `${item.price === 0 ? '<span class="badge">Grátis</span>' : '<span class="badge">R$ '+item.price+'</span>'}`;

    body.appendChild(title);
    body.appendChild(location);
    body.appendChild(dateLine);
    body.appendChild(tags);

    const actions = document.createElement('div'); actions.className='card-actions';
    const fav = document.createElement('button');
    fav.type = 'button';
    fav.className = 'btn-fav';
    fav.setAttribute('aria-label','Favoritar');
    fav.setAttribute('aria-pressed', 'false');
    fav.title = 'Favoritar';
    fav.innerHTML = `<span class="material-symbols-rounded">favorite_border</span>`;

    const share = document.createElement('button');
    share.type = 'button';
    share.className = 'btn-share';
    share.setAttribute('aria-label','Compartilhar');
    share.title = 'Compartilhar';
    share.innerHTML = `<span class="material-symbols-rounded">share</span>`;

    // toggle de favorito (apenas visual)
    fav.addEventListener('click', (e)=>{
      e.stopPropagation();
      const pressed = fav.getAttribute('aria-pressed') === 'true';
      fav.setAttribute('aria-pressed', String(!pressed));
      if (!pressed) {
        fav.classList.add('favorited');
        fav.innerHTML = `<span class="material-symbols-rounded">favorite</span>`;
        showToast('Adicionado aos favoritos');
      } else {
        fav.classList.remove('favorited');
        fav.innerHTML = `<span class="material-symbols-rounded">favorite_border</span>`;
        showToast('Removido dos favoritos');
      }
    });

    // comportamento de compartilhamento: preferir Web Share API, fallback para copiar link
    share.addEventListener('click', (e)=>{
      e.stopPropagation();
      const shareUrl = `${window.location.origin}/eventos/visualizar/${item.id}/`;
      if (navigator.share) {
        navigator.share({ title: item.title, text: item.title, url: shareUrl }).catch(()=>{});
      } else if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(shareUrl).then(()=>{ showToast('Link copiado para a área de transferência'); }).catch(()=>{ showToast('Não foi possível copiar o link'); });
      } else {
        // fallback: prompt para copiar o link
        window.prompt('Copie o link abaixo', shareUrl);
      }
    });

    actions.appendChild(fav); actions.appendChild(share);
    body.appendChild(actions);

    card.appendChild(body);

    // clique abre detalhes
    card.addEventListener('click', ()=> { window.location.href = `/eventos/visualizar/${item.id}/`; });
    card.addEventListener('keydown', (e)=> { if (e.key === 'Enter') window.location.href = `/eventos/visualizar/${item.id}/`; });

    return card;
  }

  // helpers
  function uniqueValues(arr, key) { return Array.from(new Set(arr.map(i=>i[key]).filter(Boolean))); }

  function updateURL(changes) {
    const u = new URL(window.location.href);
    Object.keys(changes).forEach(k => { if (changes[k] === '' || changes[k] === null) u.searchParams.delete(k); else u.searchParams.set(k, changes[k]); });
    window.history.replaceState({},'',u.toString());
  }
});
