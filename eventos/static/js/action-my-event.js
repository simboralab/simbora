
// Adicionar interatividade às abas de filtro
document.querySelectorAll('.filter-tab').forEach(aba => {
    aba.addEventListener('click', function() {
        // Remover classe active de todas as abas
        document.querySelectorAll('.filter-tab').forEach(t => {
            t.classList.remove('active');
        });
        
        // Adicionar classe active à aba clicada
        this.classList.add('active');
        
        // Obter o filtro selecionado
        const filtro = this.getAttribute('data-filter');
        
        // Filtrar eventos
        const eventos = document.querySelectorAll('.event-card');
        eventos.forEach(evento => {
            const status = evento.getAttribute('data-status');
            const categories = evento.getAttribute('data-categories') || '';
            
            if (filtro === 'all') {
                // Mostrar todos os eventos
                evento.style.display = 'flex';
            } else if (filtro === 'created' && categories.includes('created')) {
                // Mostrar apenas eventos criados pelo usuário (Host)
                evento.style.display = 'flex';
            } else if (filtro === 'enrolled' && categories.includes('enrolled')) {
                // Mostrar apenas eventos que o usuário está inscrito
                evento.style.display = 'flex';
            } else if (filtro === 'completed' && status === 'completed') {
                // Mostrar apenas eventos concluídos
                evento.style.display = 'flex';
            } else {
                // Ocultar eventos que não correspondem ao filtro
                evento.style.display = 'none';
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // JavaScript para funcionalidades futuras
    console.log('Meus Eventos - Página carregada');
});
