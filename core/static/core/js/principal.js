
// Função para inicializar o menu mobile toggle
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!menuToggle || !navMenu) {
        console.warn('Menu toggle não encontrado:', { menuToggle, navMenu });
        return false;
    }
    
    console.log('Inicializando menu mobile toggle...');
    
    // Remove qualquer listener anterior
    const newToggle = menuToggle.cloneNode(true);
    menuToggle.parentNode.replaceChild(newToggle, menuToggle);
    
    const newNavMenu = document.querySelector('.nav-menu');
    const newMenuToggle = document.querySelector('.menu-toggle');
    
    // Função para toggle do menu
    function toggleMenu(e) {
        if (e) {
            e.preventDefault();
            e.stopPropagation();
            e.stopImmediatePropagation();
        }
        
        const isActive = newNavMenu.classList.contains('active');
        console.log('Toggle menu - estado atual:', isActive ? 'aberto' : 'fechado');
        
        if (isActive) {
            newNavMenu.classList.remove('active');
            newMenuToggle.classList.remove('active');
            console.log('Menu fechado');
        } else {
            newNavMenu.classList.add('active');
            newMenuToggle.classList.add('active');
            console.log('Menu aberto');
        }
        
        return false;
    }
    
    // Adiciona listener direto
    newMenuToggle.onclick = toggleMenu;
    
    // Também adiciona via addEventListener
    newMenuToggle.addEventListener('click', toggleMenu, false);
    
    // Touch event para mobile
    newMenuToggle.addEventListener('touchend', function(e) {
        e.preventDefault();
        toggleMenu(e);
    }, false);
    
    // Fechar menu ao clicar fora (após um pequeno delay)
    setTimeout(function() {
        document.addEventListener('click', function closeMenuOnOutsideClick(e) {
            if (newNavMenu && newNavMenu.classList.contains('active')) {
                if (!newNavMenu.contains(e.target) && !newMenuToggle.contains(e.target)) {
                    newNavMenu.classList.remove('active');
                    newMenuToggle.classList.remove('active');
                    console.log('Menu fechado por clique fora');
                }
            }
        }, false);
    }, 200);
    
    console.log('Menu mobile toggle inicializado com sucesso');
    return true;
}

// Inicializa quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
        initMobileMenu();
    });
} else {
    // DOM já está pronto
    initMobileMenu();
}

// Tenta novamente após um delay caso não tenha funcionado
setTimeout(function() {
    const menuToggle = document.querySelector('.menu-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (menuToggle && navMenu && !navMenu.classList.contains('active')) {
        console.log('Tentando re-inicializar menu mobile...');
        initMobileMenu();
    }
}, 500);
    
    // MENU DROPDOWN DO PERFIL
    function initProfileMenu() {
        const profileTrigger = document.getElementById('profile-trigger');
        const profileMenu = document.getElementById('profile-menu');
        
        if (profileTrigger && profileMenu) {
            // Toggle dropdown ao clicar no perfil
            profileTrigger.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                profileMenu.classList.toggle('active');
                profileTrigger.classList.toggle('active');
            });
            
            // Fechar dropdown ao clicar fora (com verificação para não interferir com modal)
            document.addEventListener('click', function closeProfileMenu(e) {
                const modal = document.getElementById('modal-bora');
                const isModalOpen = modal && modal.style.display === 'flex';
                
                // Não fechar se o modal estiver aberto
                if (isModalOpen) {
                    return;
                }
                
                // Não fechar se o clique foi no trigger ou no menu
                if (!profileMenu.contains(e.target) && !profileTrigger.contains(e.target)) {
                    profileMenu.classList.remove('active');
                    profileTrigger.classList.remove('active');
                }
            });
            
            // Prevenir que cliques dentro do dropdown o fechem
            profileMenu.addEventListener('click', function(e) {
                e.stopPropagation();
            });
            
            return true;
        }
        return false;
    }
    
    // Tenta inicializar imediatamente
    if (!initProfileMenu()) {
        // Se não encontrou, tenta novamente após um pequeno delay
        setTimeout(function() {
            initProfileMenu();
        }, 100);
    }
    
    // SMOOTH SCROLL PARA CARROSSEL

    const eventsCarousel = document.querySelector('.events-carousel');
    if (eventsCarousel) {
        eventsCarousel.style.scrollBehavior = 'smooth';
    }
    
    console.log('Página principal carregada com sucesso!');
});

// Função para buscar eventos (placeholder)
function searchEvents() {
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        const query = searchInput.value;
        console.log('Buscando eventos:', query);
        // Implementar lógica de busca aqui
    }
}

// Event listener para o botão de busca
document.addEventListener('DOMContentLoaded', function() {
    const searchButton = document.querySelector('.search-button');
    if (searchButton) {
        searchButton.addEventListener('click', searchEvents);
    }
    
    // Buscar ao pressionar Enter no input
    const searchInput = document.querySelector('.search-input');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchEvents();
            }
        });
    }
    

    // EVENTOS - INTERATIVIDADE
    // Nota: O comportamento dos botões "Bora!" agora é gerenciado pelo modal em main.html
    // Este código foi removido para evitar conflitos
    

    // PONTOS DE ÔNIBUS - INTERATIVIDADE

    // Botões "Quero ir junto"
    const busJoinButtons = document.querySelectorAll('.btn-bus-join');
    busJoinButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation(); // Evitar propagação do evento
            const card = this.closest('.bus-stop-card');
            const title = card.querySelector('.bus-stop-title').textContent;
            const time = card.querySelector('.time-badge').textContent.trim();
            
            // Animação de sucesso
            const originalText = this.innerHTML;
            this.innerHTML = '<span class="material-symbols-rounded">check_circle</span> Confirmado!';
            this.style.background = 'var(--verde-limao)';
            this.style.color = 'var(--azul-principal)';
            
            // Feedback visual
            card.style.border = '2px solid var(--verde-limao)';
            
            // Mostrar mensagem de confirmação
            showNotification(`Você confirmou presença para "${title}" às ${time}`, 'success');
            
            // Resetar após 2 segundos (para demonstração)
            setTimeout(() => {
                this.innerHTML = originalText;
                this.style.background = '';
                this.style.color = '';
                card.style.border = '';
            }, 2000);
        });
    });
    
    // Clique no card inteiro para ver detalhes
    const busStopCards = document.querySelectorAll('.bus-stop-card');
    busStopCards.forEach(card => {
        // Evitar que o clique no botão acione o clique do card
        card.addEventListener('click', function(e) {
            if (!e.target.closest('.btn-bus-join')) {
                // Redirecionar para página de detalhes (quando criada)
                console.log('Abrindo detalhes do ponto de ônibus...');
                // window.location.href = 'bus-stop-details.html';
            }
        });
        
        // Adicionar cursor pointer para indicar que é clicável
        card.style.cursor = 'pointer';
    });
    
    // Hover nos avatares para mostrar nome (simulado)
    const peopleAvatars = document.querySelectorAll('.people-avatars img');
    peopleAvatars.forEach(avatar => {
        avatar.title = 'Ver perfil';
    });
});


// SISTEMA DE NOTIFICAÇÕES

function showNotification(message, type = 'info') {
    // Criar elemento de notificação
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span class="material-symbols-rounded">
            ${type === 'success' ? 'check_circle' : 'info'}
        </span>
        <span>${message}</span>
    `;
    
    // Adicionar estilos inline (poderia estar no CSS)
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? 'var(--verde-limao)' : 'var(--azul-principal)'};
        color: ${type === 'success' ? 'var(--azul-principal)' : 'var(--branco)'};
        padding: 16px 24px;
        border-radius: 50px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        display: flex;
        align-items: center;
        gap: 12px;
        font-family: var(--font-body);
        font-size: 0.9375rem;
        font-weight: 600;
        z-index: 9999;
        animation: slideInRight 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    // Remover após 3 segundos
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-in';
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Adicionar animações CSS dinamicamente
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);