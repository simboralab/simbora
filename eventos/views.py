from django.shortcuts import render, get_object_or_404
from .models import Eventos, Participacao

def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)

    confirmados = evento.participacoes.filter(status='CONFIRMADO')

    total_confirmados = confirmados.count()

    if evento.maximo_participantes:
        try:
            progresso = int((total_confirmados / evento.maximo_participantes) * 100)
        except (TypeError, ZeroDivisionError):
            progresso = 0
        progresso = min(max(progresso, 0), 100)
    else:
        progresso = 0

    if evento.maximo_participantes:
        faltam = max(evento.maximo_participantes - total_confirmados, 0)
    else:
        faltam = None

    esta_lotado = (
        evento.maximo_participantes is not None and
        total_confirmados >= evento.maximo_participantes
    )

    contexto = {
        "evento": evento,
        "confirmados": confirmados,        
        "total_confirmados": total_confirmados,
        "progresso": progresso,
        "faltam": faltam,
        "esta_lotado": esta_lotado,
    }

    return render(request, "eventos/visualizar_evento.html", contexto)