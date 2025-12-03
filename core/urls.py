from django.urls import path

# core/urls.py
# MUDAR ISSO:
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('erroteste404/', views.teste, name='404')
]