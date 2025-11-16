from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.cadastro_login,name='account'),
]