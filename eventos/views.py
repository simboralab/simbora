from django.shortcuts import render, get_object_or_404
from .models import Eventos
from django.http import JsonResponse
from django.db.models import Q

def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)
    return render(request, "eventos/visualizar_evento.html", {"evento": evento})

def buscar_eventos(request):
    term = request.GET.get("term", "")

    eventos = Eventos.objects.filter(
        Q(nome_evento__icontains=term) |
        Q(organizador__usuario__first_name__icontains=term) |
        Q(organizador__usuario__last_name__icontains=term) |
        Q(endereco__cidade__icontains=term) |
        Q(endereco__rua__icontains=term)
    )[:20]

    results = [
        {
            "id": e.id,
            "text": f"{e.data_inicio.strftime('%d/%m/%Y')} • {e.nome_evento} • {e.endereco.cidade if e.endereco else ''} • {e.organizador}"
        }
        for e in eventos
    ]

    return JsonResponse({"results": results})