// Estado da confirmação
// Usa window. para acessar variáveis globais definidas no template
let confirmado = window.USUARIO_CONFIRMADO || false;
let confirmadosAtual = window.TOTAL_CONFIRMADOS || 0;
const confirmadosTotal = window.MAXIMO_PARTICIPANTES || null;

// Verifica se as variáveis foram definidas
if (typeof window.EVENTO_ID === 'undefined') {
  console.error('ERRO: Variáveis globais não foram definidas! Verifique o template.');
}

// Torna a função globalmente acessível
window.confirmarPresenca = function confirmarPresenca() {
  console.log('=== confirmarPresenca chamada ===');
  console.log('confirmado:', confirmado);
  console.log('CONFIRMAR_PRESENCA_URL:', window.CONFIRMAR_PRESENCA_URL);
  
  if (confirmado) {
    // Se já confirmado, vai direto para o WhatsApp
    console.log('Usuário já confirmado, indo para WhatsApp');
    acessarGrupoWhatsApp();
    return;
  }

  // Chamada ao backend Django
  console.log('Fazendo requisição para:', window.CONFIRMAR_PRESENCA_URL);
  if (!window.CONFIRMAR_PRESENCA_URL) {
    alert('Erro: URL de confirmação não definida. Recarregue a página.');
    return;
  }
  
  // Obtém o CSRF token usando método alternativo
  const csrftoken = getCSRFToken();
  console.log('CSRF Token:', csrftoken ? `Encontrado (${csrftoken.substring(0, 10)}...)` : 'NÃO ENCONTRADO');
  console.log('Todos os cookies:', document.cookie);
  
  if (!csrftoken) {
    console.error('CSRF token não encontrado! Tentando métodos alternativos...');
    // Tenta obter do Django via AJAX se disponível
    alert('Erro: Token de segurança não encontrado. Recarregue a página.');
    return;
  }
  
  // Tenta primeiro com JSON
  fetch(window.CONFIRMAR_PRESENCA_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
      'X-Requested-With': 'XMLHttpRequest'
    },
    credentials: 'same-origin', // Importante para incluir cookies
    body: JSON.stringify({ evento_id: window.EVENTO_ID })
  })
  .then(async response => {
    console.log('Resposta recebida:', response.status, response.statusText);
    
    // Lê a resposta como texto primeiro (só pode ser lido uma vez!)
    const responseText = await response.text();
    console.log('Resposta em texto:', responseText);
    
    // Tenta parsear como JSON
    let data;
    try {
      data = JSON.parse(responseText);
      console.log('Dados parseados:', data);
    } catch (e) {
      console.error('Erro ao parsear JSON:', e);
      data = { error: 'Resposta inválida do servidor', raw: responseText };
    }
    
    if (!response.ok) {
      // Se houver erro, lança com os dados da resposta
      const errorObj = { 
        status: response.status, 
        data: data,
        responseText: responseText
      };
      console.error('Erro na resposta:', errorObj);
      throw errorObj;
    }
    return data;
  })
  .then(data => {
    console.log('Dados recebidos:', data);
    if (data.success) {
      confirmado = true;
      // Atualiza o total de confirmados com o valor retornado pelo servidor
      confirmadosAtual = data.total_confirmados || confirmadosAtual + 1;
      console.log('Confirmação bem-sucedida! Total atualizado:', confirmadosAtual);
      
      // Atualiza a UI (incluindo barra de progresso)
      atualizarUIConfirmacao();
      
      // Mostra o modal de confirmação
      console.log('Chamando mostrarModal()');
      mostrarModal();
    } else {
      console.error('Erro na resposta:', data);
      const errorMsg = data.error || data.message || 'Erro ao confirmar presença. Tente novamente.';
      alert(errorMsg);
    }
  })
  .catch(error => {
    console.error('Erro completo:', error);
    console.error('Tipo do erro:', typeof error);
    console.error('Status:', error.status);
    console.error('Data:', error.data);
    console.error('Response Text:', error.responseText);
    
    if (error.data) {
      // Erro com dados do servidor
      const errorMsg = error.data.error || error.data.message || `Erro ${error.status}: ${JSON.stringify(error.data)}`;
      console.error('Mensagem de erro do servidor:', errorMsg);
      alert(errorMsg);
    } else if (error.responseText) {
      alert(`Erro ${error.status || 'desconhecido'}: ${error.responseText.substring(0, 200)}`);
    } else {
      alert('Erro ao confirmar presença. Verifique o console para mais detalhes.');
    }
  });
}

function atualizarUIConfirmacao() {
  const btnConfirmar = document.getElementById('btn-confirmar');
  const confirmadosText = document.getElementById('confirmados-text');
  const progressFill = document.getElementById('progress-bar-fill');
  const btnWhatsApp = document.getElementById('btn-whatsapp-group');
  const buttonsContainer = document.getElementById('buttons-container');
  
  console.log('atualizarUIConfirmacao chamada');
  console.log('Elementos encontrados:', {
    btnConfirmar: !!btnConfirmar,
    confirmadosText: !!confirmadosText,
    progressFill: !!progressFill,
    btnWhatsApp: !!btnWhatsApp,
    buttonsContainer: !!buttonsContainer
  });
  
  if (!btnConfirmar || !confirmadosText) {
    console.error('Elementos essenciais não encontrados!');
    return;
  }
  
  // Muda o botão principal
  btnConfirmar.textContent = 'NO ROLÊ!';
  btnConfirmar.classList.remove('btn-main');
  btnConfirmar.classList.add('btn-confirmado');
  btnConfirmar.onclick = acessarGrupoWhatsApp;

  // Revela o botão do WhatsApp (se existir)
  if (btnWhatsApp) {
    btnWhatsApp.style.display = 'flex';
  }
  if (buttonsContainer) {
    buttonsContainer.style.flexWrap = 'wrap';
  }

  // Atualiza o texto de confirmados
  if (confirmadosTotal) {
    const faltam = confirmadosTotal - confirmadosAtual;
    confirmadosText.textContent = `${confirmadosAtual}/${confirmadosTotal} confirmados${faltam > 0 ? ` — Faltam ${faltam}!` : ' — Rolê completo!'}`;
    
    // Atualiza a barra de progresso (igual ao front-end original)
    if (progressFill && confirmadosTotal > 0) {
      const porcentagem = (confirmadosAtual / confirmadosTotal) * 100;
      console.log(`=== Atualizando Barra de Progresso ===`);
      console.log(`Valores: ${confirmadosAtual} / ${confirmadosTotal} = ${porcentagem}%`);
      
      // Atualiza a largura
      progressFill.style.width = `${porcentagem}%`;
      
      // Verifica se foi aplicado
      setTimeout(() => {
        const computedWidth = window.getComputedStyle(progressFill).width;
        const parentWidth = progressFill.parentElement.offsetWidth;
        const computedPercent = parentWidth > 0 ? (parseFloat(computedWidth) / parentWidth) * 100 : 0;
        console.log('Verificação após atualização:', {
          'width aplicado': progressFill.style.width,
          'width computado': computedWidth,
          'largura do pai': parentWidth,
          'porcentagem computada': computedPercent.toFixed(2) + '%',
          'porcentagem desejada': porcentagem.toFixed(2) + '%'
        });
        
        if (Math.abs(computedPercent - porcentagem) > 1 && porcentagem > 0) {
          console.warn('⚠️ Largura não foi aplicada corretamente! Tentando forçar...');
          progressFill.setAttribute('style', `width: ${porcentagem}% !important;`);
        } else {
          console.log('✓ Barra de progresso atualizada com sucesso!');
        }
      }, 100);
    } else if (!progressFill) {
      console.warn('Barra de progresso não encontrada para atualização');
    }
  } else {
    confirmadosText.textContent = `${confirmadosAtual} confirmados`;
    if (progressFill) {
      console.warn('Evento sem máximo de participantes, mas barra de progresso existe');
    }
  }
}

function mostrarModal() {
  console.log('mostrarModal chamada');
  const modal = document.getElementById('modal-confirmacao');
  console.log('Modal encontrado:', modal);
  
  if (!modal) {
    console.error('Modal não encontrado! ID: modal-confirmacao');
    // Tenta encontrar qualquer elemento modal
    const modals = document.querySelectorAll('.modal');
    console.log('Modais encontrados na página:', modals.length);
    alert('Erro: Modal não encontrado na página. Verifique o console para mais detalhes.');
    return;
  }
  
  console.log('Exibindo modal...');
  console.log('Estado antes:', {
    display: modal.style.display,
    classes: modal.className,
    computedDisplay: window.getComputedStyle(modal).display
  });
  
  // Força a exibição do modal
  modal.style.display = 'flex';
  modal.style.visibility = 'visible';
  modal.style.opacity = '1';
  modal.classList.add('show');
  document.body.style.overflow = 'hidden'; // Previne scroll
  
  console.log('Estado depois:', {
    display: modal.style.display,
    classes: modal.className,
    computedDisplay: window.getComputedStyle(modal).display,
    zIndex: window.getComputedStyle(modal).zIndex
  });
  
  // Verifica se realmente apareceu após um pequeno delay
  setTimeout(() => {
    const computedDisplay = window.getComputedStyle(modal).display;
    if (computedDisplay !== 'flex' && computedDisplay !== 'block') {
      console.error('Modal ainda não visível! Display:', computedDisplay);
      // Tenta forçar novamente
      modal.style.display = 'flex !important';
    } else {
      console.log('Modal exibido com sucesso!');
    }
  }, 100);
}

function fecharModal() {
  console.log('fecharModal chamada');
  const modal = document.getElementById('modal-confirmacao');
  if (modal) {
    modal.style.display = 'none';
    modal.style.visibility = 'hidden';
    modal.classList.remove('show');
    document.body.style.overflow = 'auto'; // Restaura scroll
    console.log('Modal fechado');
  }
}

function acessarGrupoWhatsApp() {
  // Verifica se o usuário confirmou presença
  if (!confirmado && !window.EH_ORGANIZADOR) {
    alert('Você precisa confirmar presença primeiro!');
    return;
  }
  
  // Verifica se temos o link do WhatsApp
  if (window.GRUPO_WHATSAPP) {
    // Fecha o modal se estiver aberto
    fecharModal();
    
    // Abre o grupo do WhatsApp em nova aba
    window.open(window.GRUPO_WHATSAPP, '_blank', 'noopener,noreferrer');
  } else {
    alert('Link do grupo WhatsApp não disponível para este evento.');
  }
}

function irParaChat() {
  // Redireciona para o grupo WhatsApp
  acessarGrupoWhatsApp();
}

function convidarAmigos() {
  // Fecha o modal se estiver aberto
  fecharModal();
  
  // Scroll suave até a seção de compartilhamento
  const compartilharSection = document.querySelector('.compartilhar');
  if (compartilharSection) {
    compartilharSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

function mostrarGaleraCompleta() {
  // Implementar lógica para mostrar lista completa de participantes
  // Pode abrir um modal ou scrollar para seção completa
  console.log('Mostrar galera completa');
  // Exemplo: scroll suave para seção completa (se existir)
  // document.querySelector('.galera-completa')?.scrollIntoView({ behavior: 'smooth' });
}

// Fecha modal ao clicar fora dele
window.onclick = function(event) {
  const modal = document.getElementById('modal-confirmacao');
  if (event.target === modal) {
    fecharModal();
  }
}

function copiarLink() {
  const url = window.location.href;
  navigator.clipboard.writeText(url).then(() => {
    // Feedback visual melhorado
    const btn = event.target.closest('.share-btn');
    if (btn) {
      const originalText = btn.innerHTML;
      btn.innerHTML = '<span class="material-symbols-rounded">check</span> Copiado!';
      btn.style.backgroundColor = 'var(--verde-limao)';
      btn.style.color = 'var(--azul-principal)';
      setTimeout(() => {
        btn.innerHTML = originalText;
        btn.style.backgroundColor = '';
        btn.style.color = '';
      }, 2000);
    }
  }).catch(() => {
    // Fallback para navegadores mais antigos
    const textArea = document.createElement('textarea');
    textArea.value = url;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
    alert('Link copiado para a área de transferência!');
  });
}

function compartilharFacebook() {
  const url = encodeURIComponent(window.location.href);
  const text = encodeURIComponent(document.querySelector('h1').textContent || 'Evento Simbora');
  window.open(`https://www.facebook.com/sharer/sharer.php?u=${url}&quote=${text}`, '_blank', 'width=600,height=400');
}

// Função auxiliar para obter o token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Função alternativa para obter CSRF token
function getCSRFToken() {
  // Tenta do cookie primeiro
  let token = getCookie('csrftoken');
  
  // Se não encontrou no cookie, tenta de um input hidden
  if (!token) {
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput) {
      token = csrfInput.value;
    }
  }
  
  // Se ainda não encontrou, tenta de um meta tag
  if (!token) {
    const metaTag = document.querySelector('meta[name=csrf-token]');
    if (metaTag) {
      token = metaTag.getAttribute('content');
    }
  }
  
  return token;
}

// Inicialização quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
  console.log('DOM carregado');
  console.log('Variáveis globais:', {
    EVENTO_ID: window.EVENTO_ID,
    CONFIRMAR_PRESENCA_URL: window.CONFIRMAR_PRESENCA_URL,
    USUARIO_CONFIRMADO: window.USUARIO_CONFIRMADO,
    EH_ORGANIZADOR: window.EH_ORGANIZADOR,
    TOTAL_CONFIRMADOS: window.TOTAL_CONFIRMADOS,
    MAXIMO_PARTICIPANTES: window.MAXIMO_PARTICIPANTES,
    GRUPO_WHATSAPP: window.GRUPO_WHATSAPP
  });
  
  // Verifica se todas as variáveis necessárias estão definidas
  if (typeof window.EVENTO_ID === 'undefined' || typeof window.CONFIRMAR_PRESENCA_URL === 'undefined') {
    console.error('ERRO CRÍTICO: Variáveis globais não foram definidas corretamente!');
    alert('Erro ao carregar a página. Recarregue a página.');
    return;
  }
  
  // Verifica se o modal existe e garante que está oculto inicialmente
  const modal = document.getElementById('modal-confirmacao');
  if (modal) {
    console.log('Modal encontrado no DOM');
    modal.style.display = 'none';
    modal.classList.remove('show');
  } else {
    console.error('Modal NÃO encontrado no DOM! ID: modal-confirmacao');
  }
  
  // Inicializa a barra de progresso com o valor inicial (igual ao front-end original)
  const progressFillInit = document.getElementById('progress-bar-fill');
  if (progressFillInit) {
    console.log('=== Inicialização da Barra de Progresso ===');
    console.log('Elemento encontrado:', progressFillInit);
    console.log('MAXIMO_PARTICIPANTES:', window.MAXIMO_PARTICIPANTES);
    console.log('TOTAL_CONFIRMADOS:', window.TOTAL_CONFIRMADOS);
    
    if (window.MAXIMO_PARTICIPANTES && window.TOTAL_CONFIRMADOS !== undefined && window.MAXIMO_PARTICIPANTES > 0) {
      // Calcula a porcentagem inicial
      const porcentagem = (window.TOTAL_CONFIRMADOS / window.MAXIMO_PARTICIPANTES) * 100;
      console.log(`Calculando porcentagem: ${window.TOTAL_CONFIRMADOS} / ${window.MAXIMO_PARTICIPANTES} = ${porcentagem}%`);
      
      // Atualiza a barra (igual ao front-end original)
      progressFillInit.style.width = `${porcentagem}%`;
      
      // Verifica se foi aplicado
      setTimeout(() => {
        const computedWidth = window.getComputedStyle(progressFillInit).width;
        const parentWidth = progressFillInit.parentElement.offsetWidth;
        const computedPercent = (parseFloat(computedWidth) / parentWidth) * 100;
        console.log('Verificação após inicialização:', {
          'width aplicado': progressFillInit.style.width,
          'width computado': computedWidth,
          'largura do pai': parentWidth,
          'porcentagem computada': computedPercent.toFixed(2) + '%',
          'porcentagem desejada': porcentagem.toFixed(2) + '%'
        });
        
        if (Math.abs(computedPercent - porcentagem) > 1) {
          console.warn('⚠️ Largura não foi aplicada corretamente! Tentando forçar...');
          progressFillInit.setAttribute('style', `width: ${porcentagem}% !important;`);
        }
      }, 100);
      
      console.log(`✓ Barra de progresso inicializada: ${window.TOTAL_CONFIRMADOS}/${window.MAXIMO_PARTICIPANTES} = ${porcentagem}%`);
    } else {
      console.warn('Barra de progresso encontrada mas não inicializada:', {
        temMaximo: !!window.MAXIMO_PARTICIPANTES,
        temTotal: window.TOTAL_CONFIRMADOS !== undefined,
        maximo: window.MAXIMO_PARTICIPANTES,
        total: window.TOTAL_CONFIRMADOS
      });
    }
  } else {
    console.error('❌ Barra de progresso NÃO encontrada! ID: progress-bar-fill');
  }
  
  // Se o usuário já está confirmado, atualiza a UI
  if (confirmado || window.EH_ORGANIZADOR) {
    atualizarUIConfirmacao();
  }
  
  // Adiciona listener ao botão
  const btnConfirmar = document.getElementById('btn-confirmar');
  if (btnConfirmar) {
    console.log('Botão "Eu vou!" encontrado');
    
    // Remove qualquer listener anterior (se houver)
    const newBtn = btnConfirmar.cloneNode(true);
    btnConfirmar.parentNode.replaceChild(newBtn, btnConfirmar);
    
    // Adiciona listener ao novo botão
    const btn = document.getElementById('btn-confirmar');
    
    // Função de handler
    const handleClick = function(e) {
      e.preventDefault();
      e.stopPropagation();
      console.log('=== BOTÃO CLICADO ===');
      console.log('Chamando confirmarPresenca()...');
      try {
        if (typeof window.confirmarPresenca === 'function') {
          window.confirmarPresenca();
        } else {
          console.error('confirmarPresenca não é uma função!', typeof window.confirmarPresenca);
          alert('Erro: Função não disponível. Recarregue a página.');
        }
      } catch (error) {
        console.error('Erro ao executar confirmarPresenca:', error);
        alert('Erro ao confirmar presença: ' + error.message);
      }
      return false;
    };
    
    btn.addEventListener('click', handleClick);
    
    // Também adiciona onclick como fallback
    btn.onclick = handleClick;
    
    console.log('✓ Listeners adicionados ao botão');
    
    // Adiciona um teste visual: muda a cor do botão quando o mouse passa por cima
    btn.addEventListener('mouseenter', function() {
      console.log('Mouse sobre o botão - tudo funcionando!');
    });
    
    console.log('Listener adicionado ao botão com sucesso');
  } else {
    console.error('ERRO: Botão "Eu vou!" não encontrado! ID: btn-confirmar');
    // Tenta encontrar qualquer botão com texto "Eu vou!"
    const botoes = document.querySelectorAll('button');
    console.log('Botões encontrados na página:', botoes.length);
    botoes.forEach((btnItem, index) => {
      if (btnItem.textContent.includes('Eu vou')) {
        console.log(`Botão ${index} tem texto "Eu vou":`, btnItem);
      }
    });
  }
  
  // Verifica se a função está acessível globalmente
  console.log('Função confirmarPresenca disponível globalmente:', typeof window.confirmarPresenca);
  
  // Teste rápido: verifica se consegue chamar a função
  if (typeof window.confirmarPresenca === 'function') {
    console.log('✓ Função confirmarPresenca está disponível e pronta para uso');
  } else {
    console.error('✗ ERRO: Função confirmarPresenca não está disponível!');
  }
});
