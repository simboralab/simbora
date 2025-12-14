from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.lista_eventos, name="lista_eventos"),
    path("meus-eventos/", views.meus_eventos, name="meus_eventos"),
    
    path("criar/", views.criar_evento, name="criar_evento"),
    path("visualizar/<int:evento_id>/", views.visualizar_evento, name="visualizar_evento"),
    
    path("<int:pk>/editar/", views.editar_evento, name="editar_evento"),
    path("<int:pk>/participantes/", views.participantes_evento, name="participantes_evento"),
    path("<int:pk>/cancelar/", views.cancelar_evento, name="cancelar_evento"),
    
    # Opcionais futuras
    # path("<int:pk>/inscrever/", views.inscrever_evento, name="inscrever_evento"),
    # path("<int:pk>/sair/", views.sair_evento, name="sair_evento"),
]