from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse

from perfil.models import Perfil

from .forms import CadastroCompletoForm, LoginForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('sucesso') 

    if request.method == 'POST':
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
            return redirect('sucesso')
    else:
        cadastro_form = CadastroCompletoForm() 

    context = {
        'cadastro_form': cadastro_form,
    }
    
    return render(request, 'perfil/page/signup.html', context)

def signin_view(request):
    if request.user.is_authenticated:
        return redirect('sucesso') 

    if request.method == 'POST':
        login_form = LoginForm(request, data = request.POST) 
        if login_form.is_valid():
            usuario = login_form.get_user()
            login(request, usuario)
            return redirect('sucesso')
    else:
        login_form = LoginForm()        
    context = {
        'login_form': login_form,
    }
    return render(request, 'perfil/page/signin.html', context)

def sucess_view(request):
    if not request.user.is_authenticated:
        return redirect('signin') 

    nome_completo = f"{request.user.first_name} {request.user.last_name}"
    
    context = {
        'nome_completo': nome_completo
    }
    return render(request, 'perfil/sucess.html', context)



def logout_view(request):
    logout(request)
    return redirect('home')

