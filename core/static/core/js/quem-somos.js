// Função para detectar a equipe baseada no papel/função do membro
function detectarEquipe(papel) {
  if (!papel) return 'todos';
  
  const papelLower = papel.toLowerCase().trim();
  
  if (papelLower.includes('produto')) {
    return 'produto';
  } else if (papelLower.includes('design')) {
    return 'design';
  } else if (papelLower.includes('front-end') || papelLower.includes('frontend') || papelLower.includes('front end')) {
    return 'front-end';
  } else if (papelLower.includes('back-end') || papelLower.includes('backend') || papelLower.includes('back end')) {
    return 'back-end';
  } else if (papelLower.includes('liderança técnica') || papelLower.includes('lideranca tecnica') || papelLower.includes('liderança tecnica') || papelLower.includes('mentor') || papelLower.includes('orientador') || papelLower.includes('professor')) {
    return 'lideranca-tecnica';
  }
  
  return 'todos';
}

document.addEventListener('DOMContentLoaded', function () {
  const membros = document.querySelectorAll('.membro-equipe');
  const navLinks = document.querySelectorAll('.nav-quem-somos .nav-links a');
  const equipesBloco = document.querySelector('.equipes-bloco');

  // garante que o bloco de equipes esteja visível 
  function mostrarBlocoEquipes() {
    if (!equipesBloco) return;
    equipesBloco.classList.remove('oculto');
    equipesBloco.setAttribute('aria-hidden', 'false');
  }

  // helper: animação de scroll suave levando em conta header fixo
  function scrollPara(element) {
    const rect = element.getBoundingClientRect();
    const docEl = document.documentElement;
    const scrollTop = (window.pageYOffset || docEl.scrollTop) - (docEl.clientTop || 0);
    const header = document.querySelector('.nav-quem-somos');
    const headerHeight = header ? header.getBoundingClientRect().height : 0;
    const targetY = rect.top + scrollTop - headerHeight - 20; 

    window.scrollTo({ top: targetY, behavior: 'smooth' });
  }

  // Atualiza classe ativo na nav (removendo dos outros links)
  function marcarAtivo(link) {
    navLinks.forEach(a => a.classList.remove('ativo'));
    if (link) link.classList.add('ativo');
  }

  // lidar com cliques nas âncoras da nav -> rolar para o bloco de equipes quando clicar em #equipe
  navLinks.forEach(link => {
    const href = link.getAttribute('href');
    link.addEventListener('click', function (e) {
      e.preventDefault();
      if (href === '#equipe') {
        // preferir rolar para o bloco que contém os links das equipes
        const alvo = equipesBloco || document.querySelector(href);
        if (alvo) {
          mostrarBlocoEquipes();
          scrollPara(alvo);
        } else {
          window.scrollTo({ top: 0, behavior: 'smooth' });
        }
      } else {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }
      marcarAtivo(link);
    });
  });

  /* ---------- Filtragem por equipe (links dentro do bloco 'Equipes') ---------- */
  const linksEquipes = document.querySelectorAll('.links-equipes a');


  // atribui data-equipe a cada membro se ainda não tiver
  membros.forEach(member => {
    if (!member.dataset.equipe) {
      const info = member.querySelector('.informacoes p');
      const papel = info ? info.textContent.trim() : '';
      const equipe = detectarEquipe(papel);
      member.dataset.equipe = equipe;
    }
  });

  // função que mostra/oculta membros conforme filtro
  function filtrarEquipe(equipe) {
    membros.forEach(member => {
      if (!equipe || equipe === 'todos') {
        member.classList.remove('escondido');
      } else {
        if (member.dataset.equipe === equipe) {
          member.classList.remove('escondido');
        } else {
          member.classList.add('escondido');
        }
      }
    });
  }

  // scroll para as âncoras reais (existentes na página) e filtro
  linksEquipes.forEach(link => {
    const href = link.getAttribute('href');
    // extrai nome da equipe do href (removendo #)
    const equipeNome = href ? href.replace('#', '') : null;
    link.addEventListener('click', function (e) {
      e.preventDefault();
      // garantir que o painel de equipes esteja visível
      mostrarBlocoEquipes();
      // marcar visualmente
      document.querySelectorAll('.links-equipes a').forEach(a => a.classList.remove('ativo-equipe'));
      link.classList.add('ativo-equipe');

      // filtrar membros
      filtrarEquipe(equipeNome);

      // rolar para a âncora correspondente 
      const alvo = document.querySelector(href);
      if (alvo) scrollPara(alvo);
      else if (equipesBloco) scrollPara(equipesBloco);
      else scrollPara(document.querySelector('#equipe'));
    });
  });

  // se o usuário clicar no link "Equipe" da nav principal, remove qualquer filtro
  const navEquipe = document.querySelector('.nav-quem-somos .nav-links a[href="#equipe"]');
  if (navEquipe) {
    navEquipe.addEventListener('click', function (e) {
      e.preventDefault();
      // mostrar bloco de equipes
      mostrarBlocoEquipes();
      // remover filtros e classes de destaque das equipes
      filtrarEquipe('todos');
      document.querySelectorAll('.links-equipes a').forEach(a => a.classList.remove('ativo-equipe'));
      // rolar para o bloco de equipes preferencialmente
      if (equipesBloco) scrollPara(equipesBloco);
      else {
        const alvo = document.querySelector('#equipe');
        if (alvo) scrollPara(alvo);
        else window.scrollTo({ top: 0, behavior: 'smooth' });
      }
    });
  }

  membros.forEach(member => {
    const envoltura = member.querySelector('.envoltura-foto');
    const sobreposicao = member.querySelector('.sobreposicao-gif');
    let carregado = false;

    function mostrar() {
      if (!carregado && sobreposicao && sobreposicao.dataset && sobreposicao.dataset.gif) {
        sobreposicao.src = sobreposicao.dataset.gif;
        carregado = true;
      }
      member.classList.add('mostrando');
    }

    function esconder() {
      member.classList.remove('mostrando');
    }

    if (envoltura) {
      envoltura.addEventListener('mouseenter', mostrar);
      envoltura.addEventListener('mouseleave', esconder);
      envoltura.addEventListener('focus', mostrar);
      envoltura.addEventListener('blur', esconder);

      // suporte teclado (Enter / Space)
      envoltura.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault();
          if (member.classList.contains('mostrando')) esconder(); else mostrar();
        }
      });
    }
  });
});

