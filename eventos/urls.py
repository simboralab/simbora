from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.lista_eventos, name="lista_eventos"),
    path("meus-eventos/", views.meus_eventos, name="meus_eventos"),
    path("visualizar/<int:evento_id>/", views.visualizar_evento, name="visualizar_evento"),
    path("confirmar-presenca/<int:evento_id>/", views.confirmar_presenca, name="confirmar_presenca"),
    path("criar/", views.criar_evento, name="criar_evento"),
    path("editar/<int:evento_id>/", views.editar_evento, name="editar_evento"),
    path("participantes/<int:evento_id>/", views.participantes_evento, name="participantes_evento"),
    path("cancelar/<int:evento_id>/", views.cancelar_evento, name="cancelar_evento"),
    path("sair/<int:evento_id>/", views.sair_evento, name="sair_evento"),
]
