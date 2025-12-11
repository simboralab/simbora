from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from django.http import HttpResponseForbidden

from .forms import EventoForm,EnderecoForm
from .models import Eventos, Endereco


def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, "eventos/visualizar_evento.html", {"evento": evento})

def editar_evento(request, evento_id):
    # Lógica para editar um evento existente
    pass

@login_required(login_url='signin')
def deletar_evento(request, evento_id):

  
    evento = get_object_or_404(Eventos, id=evento_id)
    
 
    if evento.organizador != request.user:
        return HttpResponseForbidden("Você não tem permissão para deletar este evento.")

    if request.method == 'POST':
        
        with transaction.atomic():
            evento.delete()

        return redirect('visualizar_eventos')
        
    
    return render(request, 'confirmar_delecao.html', {'evento': evento})


@login_required(login_url='signin')
def criar_evento(request):
    if request.method == 'POST':
        evento_form = EventoForm(request.POST, request.FILES)
        endereco_form = EnderecoForm(request.POST)

        if request.user.is_authenticated:
            evento_form.instance.organizador = request.user.perfil

        if evento_form.is_valid() and endereco_form.is_valid():
            with transaction.atomic():
                endereco_instance = endereco_form.save() 
                
                evento_instance = evento_form.save(commit=False)
                evento_instance.endereco = endereco_instance
                evento_instance.save()

                return redirect('visualizar_evento')

    else:
        evento_form = EventoForm()
        endereco_form = EnderecoForm()

    return render(request, 'eventos/page/teste.html', {
        'evento_form': evento_form,
        'endereco_form': endereco_form,
    })
