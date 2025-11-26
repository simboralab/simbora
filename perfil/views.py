from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse

from perfil.models import Perfil

from .forms import CadastroCompletoForm, LoginForm


def account_view(request):
    if request.user.is_authenticated:
        return redirect('sucesso') 

    login_form = LoginForm()
    cadastro_form = CadastroCompletoForm()

    if request.method == 'POST':
        action = request.POST.get('action') 

        if action == 'login':
            # 1. Processar Login
            login_form = LoginForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('sucesso')
            else:
                messages.error(request, 'Email ou senha inválidos. Por favor, tente novamente.')
        
        elif action == 'cadastro':
            # 2. Processar Cadastro
            cadastro_form = CadastroCompletoForm(request.POST)
            if cadastro_form.is_valid():
                with transaction.atomic():
                    usuario = cadastro_form.save()
                    Perfil.objects.create(
                        usuario=usuario,
                        data_nascimento=cadastro_form.cleaned_data['data_nascimento'],
                        genero=cadastro_form.cleaned_data['genero']
                    )

                login(request, usuario)
                messages.success(request, 'Cadastro realizado com sucesso!')
                return redirect('sucesso')
            
        else:
            messages.error(request, 'Ação desconhecida.')

    context = {
        'login_form': login_form,
        'cadastro_form': cadastro_form,
    }
    return render(request, 'perfil/account.html', context)


def sucess_view(request):
    if not request.user.is_authenticated:
        return redirect('account') 

    nome_completo = f"{request.user.first_name} {request.user.last_name}"
    
    context = {
        'nome_completo': nome_completo
    }
    return render(request, 'perfil/sucess.html', context)



def logout_view(request):
    logout(request)
    return redirect('account')