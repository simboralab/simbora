from django.urls import path
from . import views

app_name = "eventos"

urlpatterns = [
    path("", views.lista_eventos, name="lista_eventos"),
    path("visualizar/<int:evento_id>/", views.visualizar_evento, name="visualizar_evento"),
    path("confirmar-presenca/<int:evento_id>/", views.confirmar_presenca, name="confirmar_presenca"),
]
