from django.urls import path

from . import views

urlpatterns = [
    path('account/', views.account_view,name='account'),
    path('sucesso/', views.sucess_view, name='sucesso'),
    path('logout/', views.logout_view, name='logout'),
]