
// Adicionar interatividade às abas de filtro
document.querySelectorAll('.filter-tab').forEach(aba => {
    aba.addEventListener('click', function(e) {
        // Se for um link, não prevenir o comportamento padrão para permitir navegação
        // O filtro será feito pelo servidor via query string
        // Apenas atualiza a classe active visualmente
        document.querySelectorAll('.filter-tab').forEach(t => {
            t.classList.remove('active');
        });
        this.classList.add('active');
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // JavaScript para funcionalidades futuras
    console.log('Meus Eventos - Página carregada');
});
