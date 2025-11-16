# Seu views.py (não precisa mudar, a lógica é a mesma)
from django.shortcuts import render, redirect
from django.db import transaction
from .forms import CadastroCompletoForm
from django.contrib import messages
from .models import Perfil

def cadastro_login(request):
    form = CadastroCompletoForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            
            #Garantindo que o campo de perfil seja criado
            with transaction.atomic(): 
                usuario = form.save()
                
                data_nascimento = form.cleaned_data['data_nascimento']
                
                Perfil.objects.create(
                    usuario=usuario,
                    data_nascimento=data_nascimento
                    # O resto dos campos do Perfil será NULL ou DEFAULT.
                )

            messages.success(request, 'Cadastro realizado com sucesso! Faça login para continuar.')
            
            return redirect('account') 

    context = {
        'form': form,
    }

    return render(request, 'perfil/cadastro.html', context)