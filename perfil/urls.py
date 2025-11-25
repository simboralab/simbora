from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

# app_name = 'perfil'

urlpatterns = [
    path('account/', views.cadastro_login,name='account'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='/perfil/password_change_done'), name='password_change'),
    path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='/perfil/password_reset_done'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete')
]