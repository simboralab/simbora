from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Endereco

from perfil.models import Perfil

from .forms import CadastroCompletoForm, LoginForm, PerfilForm


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


@login_required
def edit_profile_view(request):

    perfil = request.user.perfil  # pega o perfil do usuário logado
    endereco = perfil.endereco if perfil.endereco else None
    ufs = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

    if request.method == "POST":
        form = PerfilForm(request.POST, request.FILES, instance=perfil)

        # Endereço também será atualizado manualmente:
        cidade = request.POST.get("cidade")
        estado = request.POST.get("estado")

        if form.is_valid():
            perfil = form.save()

            # Atualizar endereço
            if endereco:
                endereco.cidade = cidade
                endereco.estado = estado
                endereco.save()
            else:
                # cria caso não exista
                novo_endereco = Endereco.objects.create(cidade=cidade, estado=estado)
                perfil.endereco = novo_endereco
                perfil.save()

            return redirect("edit_profile")

    else:
        form = PerfilForm(instance=perfil)

    context = {
        "form": form,
        "perfil": perfil,
        "endereco": endereco,
        "ufs": ufs,
    }

    return render(request, "perfil/page/edit_profile.html", context)
