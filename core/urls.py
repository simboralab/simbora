from django.urls import path

# core/urls.py
# MUDAR ISSO:
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('quem-somos/', views.quem_somos_view, name='quem_somos'),
]