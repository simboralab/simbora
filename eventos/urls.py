from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.lista_eventos, name="lista_eventos"),
    path("visualizar/<int:evento_id>/", views.visualizar_evento, name="visualizar_evento"),
    path("criar/", views.criar_evento, name="criar_evento"),
    path("editar/<int:evento_id>/", views.editar_evento, name="editar_evento"),
    path("deletar/<int:evento_id>/", views.deletar_evento, name="deletar_evento"),
]
