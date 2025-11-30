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
            # Cria a instância do formulário de login com request e dados
            login_form = LoginForm(request, data=request.POST) 
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                # Redirecionamento após LOGIN BEM-SUCEDIDO
                return redirect('sucesso') 
            else:
                # Se falhar, a instância 'login_form' já contém os erros.
                # A mensagem de erro já está sendo adicionada, mas o form
                # com os erros precisa ser passado para o contexto.
                messages.error(request, 'Email ou senha inválidos. Por favor, tente novamente.')
        
        elif action == 'cadastro':
            # 2. Processar Cadastro
            cadastro_form = CadastroCompletoForm(request.POST) # Cria a instância do formulário de cadastro com dados
            if cadastro_form.is_valid():
                with transaction.atomic():
                    usuario = cadastro_form.save()
                    Perfil.objects.create(
                        usuario=usuario,
                        data_nascimento=cadastro_form.cleaned_data['data_nascimento'],
                        genero=cadastro_form.cleaned_data['genero']
                    )

                login(request, usuario)
                # Redirecionamento após CADASTRO BEM-SUCEDIDO
                return redirect('sucesso')
            # Se o cadastro falhar, a instância 'cadastro_form' já contém os erros
            
        else:
            messages.error(request, 'Ação desconhecida.')

    # O contexto final usa as instâncias atualizadas (com erros, se houver) ou as instâncias vazias.
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


def teste_view(request):
    cadastro_form = CadastroCompletoForm()
    context = {
        'cadastro_form': cadastro_form,
    }
    return render(request, 'perfil/rotateste.html', context)