from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import UsuarioCreationForm

# Create your views here.

def cadastro_login(request):
    if request.method == 'POST':
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            # Salva o usuário (UserCreationForm garante o hashing da senha)
            form.save()
            messages.success(request, 'Usuário cadastrado com sucesso!')
            # Redireciona o usuário para a página de login após o cadastro
            return redirect('cadastro_login') # Use o nome da sua URL de login
    else:
        # Se for um GET, cria um formulário vazio
        form = UsuarioCreationForm()
        
    return render(request, 'cadastro_login/cadastro.html', {'form': form})
