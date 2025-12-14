
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Eventos
from perfil.models import Perfil

def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, "eventos/visualizar_evento.html", {"evento": evento})    


@login_required
def meus_eventos(request):
    filtro = request.GET.get('filtro', 'all')
    user = request.user

    # Correção principal: usa get_or_create para garantir que o Perfil exista
    perfil, criado = Perfil.objects.get_or_create(
        usuario=user,
        defaults={
            'nome_social': user.username,  # ou user.get_full_name() se tiver nome
            # Adicione outros campos default se necessário (ex: bio='', foto=None)
        }
    )

    # Se foi criado agora, você pode mostrar uma mensagem de boas-vindas
    if criado:
        messages.info(request, "Seu perfil foi criado automaticamente. Complete suas informações!")

    # Agora todas as queries usam o 'perfil' (instância de Perfil)
    if filtro == 'created':
        eventos = Eventos.objects.filter(organizador=perfil)
    elif filtro == 'enrolled':
        # Correção: participantes é ManyToMany com Perfil, não User
        eventos = Eventos.objects.filter(participantes=perfil)
    elif filtro == 'completed':
        eventos = Eventos.objects.filter(status='FINALIZADO')  # ou 'concluido' se for o caso
    else:  # 'all' ou qualquer outro
        eventos = Eventos.objects.filter(
            Q(organizador=perfil) | Q(participantes=perfil)
        ).distinct()

    eventos = eventos.order_by('-data_inicio')

    context = {
        'eventos': eventos,
        'filtro_ativo': filtro,
    }

    return render(request, 'eventos/meus_eventos.html', context)

@login_required
def criar_evento(request):
    messages.info(request, "Página de criação de evento em desenvolvimento.")
    return redirect('eventos:meus_eventos')

@login_required
def editar_evento(request, pk):
    evento = get_object_or_404(Eventos, pk=pk, organizador__usuario=request.user)
    messages.info(request, f"Edição do evento '{evento.nome_evento}' em desenvolvimento.")
    return redirect('eventos:meus_eventos')

@login_required
def participantes_evento(request, pk):
    evento = get_object_or_404(Eventos, pk=pk, organizador__usuario=request.user)
    messages.info(request, f"Lista de participantes do evento '{evento.nome_evento}' em desenvolvimento.")
    return redirect('eventos:meus_eventos')

@login_required
def cancelar_evento(request, pk):
    evento = get_object_or_404(Eventos, pk=pk, organizador__usuario=request.user)
    messages.info(request, f"Cancelamento do evento '{evento.nome_evento}' em desenvolvimento.")
    return redirect('eventos:meus_eventos')