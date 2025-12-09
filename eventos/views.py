from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import EventoForm
from .models import Eventos


def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, "eventos/visualizar_evento.html", {"evento": evento})

def editar_evento(request, evento_id):
    # Lógica para editar um evento existente
    pass

def deletar_evento(request, evento_id):
    # Lógica para deletar um evento existente
    pass    


@login_required(login_url='signin')
def criar_evento(request):
    form = EventoForm()

    return render(request, "eventos/page/teste.html", {"form": form})
