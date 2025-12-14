from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from eventos.models import Eventos
from perfil.models import Perfil

# Create your views here.
def custom_404_view(request, exception):
    return render(request, 'core/page/404.html', status=404)

def finalizar_eventos_vencidos():
    """
    Atualiza automaticamente o status dos eventos para FINALIZADO
    quando a data atual for maior que a data_termino do evento.
    """
    agora = timezone.now()
    
    # Busca eventos ATIVOS cuja data_termino já passou
    eventos_vencidos = Eventos.objects.filter(
        status='ATIVO',
        data_termino__lt=agora
    )
    
    # Atualiza o status para FINALIZADO
    eventos_atualizados = eventos_vencidos.update(status='FINALIZADO')
    
    return eventos_atualizados

def home(request):
    # Atualiza automaticamente eventos vencidos para FINALIZADO
    finalizar_eventos_vencidos()
    
    # Busca os 6 eventos mais próximos (status ATIVO)
    # Ordena por data_inicio: eventos futuros primeiro (crescente), depois eventos passados (decrescente)
    agora = timezone.now()
    
    # Busca eventos futuros ordenados por data crescente (mais próximo primeiro)
    eventos_futuros = Eventos.objects.filter(
        status='ATIVO',
        data_inicio__gte=agora
    ).order_by('data_inicio').prefetch_related(
        'participacoes__participante',
        'organizador',
        'endereco'
    )
    
    # Busca eventos passados ordenados por data decrescente (mais recente primeiro)
    eventos_passados = Eventos.objects.filter(
        status='ATIVO',
        data_inicio__lt=agora
    ).order_by('-data_inicio').prefetch_related(
        'participacoes__participante',
        'organizador',
        'endereco'
    )
    
    # Combina: futuros primeiro, depois passados, limitando a 6
    eventos_proximos = list(eventos_futuros) + list(eventos_passados)
    eventos_proximos = eventos_proximos[:6]
    
    # Prepara os dados no mesmo formato usado em lista_eventos
    eventos_com_info = []
    for evento in eventos_proximos:
        # Busca participantes ativos (excluindo cancelados e ausentes)
        participantes_ativos_qs = evento.participacoes.exclude(
            status__in=['CANCELADO', 'AUSENTE']
        ).exclude(participante__isnull=True).select_related('participante')
        
        # Lista de participantes para exibição (incluindo organizador se necessário)
        participantes_para_exibicao = list(participantes_ativos_qs)
        
        # Verifica se organizador está na lista
        organizador_na_lista = False
        if evento.organizador:
            organizador_na_lista = any(
                p.participante and p.participante.id == evento.organizador.id 
                for p in participantes_para_exibicao
            )
            if not organizador_na_lista:
                # Cria participação virtual para organizador
                class ParticipacaoVirtual:
                    def __init__(self, participante):
                        self.participante = participante
                        self.status = 'CONFIRMADO'
                
                organizador_participacao = ParticipacaoVirtual(evento.organizador)
                participantes_para_exibicao.insert(0, organizador_participacao)
        
        total_participantes = len(participantes_para_exibicao)
        
        # Verifica se o usuário logado é o organizador do evento
        usuario_eh_organizador = False
        if request.user.is_authenticated:
            try:
                perfil_usuario = Perfil.objects.get(usuario=request.user)
                usuario_eh_organizador = evento.organizador and evento.organizador.id == perfil_usuario.id
            except Perfil.DoesNotExist:
                usuario_eh_organizador = False
        
        eventos_com_info.append({
            'evento': evento,
            'total_participantes': total_participantes,
            'participantes_para_exibicao': participantes_para_exibicao,
            'usuario_eh_organizador': usuario_eh_organizador,
        })
    
    # Busca os 5 últimos perfis criados
    uma_semana_atras = agora - timedelta(days=7)
    
    # Busca perfis ordenados por data de criação do usuário (mais recentes primeiro)
    # Filtra apenas perfis que têm usuário associado
    ultimos_perfis = Perfil.objects.filter(
        usuario__isnull=False
    ).select_related('usuario').order_by('-usuario__date_joined')[:5]
    
    # Conta quantos perfis foram criados na última semana
    perfis_semana = Perfil.objects.filter(
        usuario__isnull=False,
        usuario__date_joined__gte=uma_semana_atras
    ).count()
    
    context = {
        'eventos_com_info': eventos_com_info,
        'ultimos_perfis': ultimos_perfis,
        'perfis_semana': perfis_semana,
    }
    
    return render(request, 'core/page/main.html', context)

def teste(request):
    return render(request, 'core/page/404.html')

def quem_somos_view(request):
    return render(request, 'core/page/quem-somos.html')