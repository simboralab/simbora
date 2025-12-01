from django.shortcuts import render, get_object_or_404
from .models import Eventos

def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, "eventos/visualizar_evento.html", {"evento": evento})
