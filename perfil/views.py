import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from django.urls import reverse
from core.models import Endereco

from perfil.models import Perfil

from .forms import CadastroCompletoForm, LoginForm, PerfilForm

logger = logging.getLogger(__name__)


def signup_view(request):
    logger.info(f"signup_view: Acesso à página de cadastro - IP: {request.META.get('REMOTE_ADDR')}")
    
    if request.user.is_authenticated:
        logger.debug(f"signup_view: Usuário já autenticado ({request.user.email}), redirecionando para home")
        return redirect('home') 

    if request.method == 'POST':
        logger.info(f"signup_view: Tentativa de cadastro - IP: {request.META.get('REMOTE_ADDR')}")
        cadastro_form = CadastroCompletoForm(request.POST) 
        if cadastro_form.is_valid():
            try:
                with transaction.atomic():
                    usuario = cadastro_form.save()
                    logger.info(f"signup_view: Usuário criado com sucesso - Email: {usuario.email}, ID: {usuario.id}")
                   
                    perfil = Perfil.objects.create(
                        usuario=usuario,
                        data_nascimento=cadastro_form.cleaned_data['data_nascimento'],
                        genero=cadastro_form.cleaned_data['genero']
                    )
                    logger.info(f"signup_view: Perfil criado com sucesso - Perfil ID: {perfil.id}")

                login(request, usuario)
                logger.info(f"signup_view: Usuário autenticado com sucesso - Email: {usuario.email}")
                return redirect('home')
            except Exception as e:
                logger.error(f"signup_view: Erro ao criar usuário/perfil - Erro: {str(e)}", exc_info=True)
                raise
        else:
            logger.warning(f"signup_view: Formulário inválido - Erros: {cadastro_form.errors}")
    else:
        cadastro_form = CadastroCompletoForm() 

    context = {
        'cadastro_form': cadastro_form,
    }
    
    return render(request, 'perfil/page/signup.html', context)

def signin_view(request):
    logger.info(f"signin_view: Acesso à página de login - IP: {request.META.get('REMOTE_ADDR')}")
    
    if request.user.is_authenticated:
        logger.debug(f"signin_view: Usuário já autenticado ({request.user.email}), redirecionando para home")
        return redirect('home') 

    if request.method == 'POST':
        email = request.POST.get('username', '')
        logger.info(f"signin_view: Tentativa de login - Email: {email}, IP: {request.META.get('REMOTE_ADDR')}")
        login_form = LoginForm(request, data = request.POST) 
        if login_form.is_valid():
            usuario = login_form.get_user()
            login(request, usuario)
            logger.info(f"signin_view: Login bem-sucedido - Email: {usuario.email}, ID: {usuario.id}")
            return redirect('home')
        else:
            logger.warning(f"signin_view: Falha no login - Email: {email}, Erros: {login_form.errors}")
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
    user_email = request.user.email if request.user.is_authenticated else 'Anônimo'
    logger.info(f"logout_view: Logout realizado - Usuário: {user_email}, IP: {request.META.get('REMOTE_ADDR')}")
    logout(request)
    return redirect('home')


@login_required
def edit_profile_view(request):
    user_email = request.user.email
    logger.info(f"edit_profile_view: Acesso à edição de perfil - Usuário: {user_email}, IP: {request.META.get('REMOTE_ADDR')}")

    try:
        perfil = request.user.perfil  # pega o perfil do usuário logado
        logger.debug(f"edit_profile_view: Perfil encontrado - Perfil ID: {perfil.id}, Usuário: {user_email}")
    except AttributeError:
        logger.error(f"edit_profile_view: Perfil não encontrado para usuário {user_email}", exc_info=True)
        # Redirecionar ou criar perfil se necessário
        return redirect('home')
    
    endereco = perfil.endereco if perfil.endereco else None
    logger.debug(f"edit_profile_view: Endereço {'encontrado' if endereco else 'não encontrado'} - Perfil ID: {perfil.id}")
    
    ufs = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"
    ]

    if request.method == "POST":
        logger.info(f"edit_profile_view: Tentativa de atualização de perfil - Usuário: {user_email}, Perfil ID: {perfil.id}")
        form = PerfilForm(request.POST, request.FILES, instance=perfil)

        # Endereço também será atualizado manualmente:
        cidade = request.POST.get("cidade", "").strip()
        estado = request.POST.get("estado", "").strip()
        logger.debug(f"edit_profile_view: Dados de endereço recebidos - Cidade: {cidade}, Estado: {estado}")

        if form.is_valid():
            try:
                perfil = form.save()
                logger.info(f"edit_profile_view: Perfil atualizado com sucesso - Perfil ID: {perfil.id}")

                # Atualizar endereço apenas se cidade e estado estiverem preenchidos
                if cidade and estado:
                    if endereco:
                        # Atualiza apenas cidade e estado
                        logger.debug(f"edit_profile_view: Atualizando endereço existente - Endereço ID: {endereco.id}")
                        endereco.cidade = cidade
                        endereco.estado = estado
                        endereco.save()
                        logger.info(f"edit_profile_view: Endereço atualizado - Endereço ID: {endereco.id}, Cidade: {cidade}, Estado: {estado}")
                    else:
                        # Cria novo endereço com valores padrão para campos obrigatórios
                        logger.debug(f"edit_profile_view: Criando novo endereço - Cidade: {cidade}, Estado: {estado}")
                        try:
                            novo_endereco = Endereco.objects.create(
                                rua="Não informado",
                                numero="0",
                                bairro="Não informado",
                                cidade=cidade,
                                estado=estado,
                                cep="00000-000"
                            )
                            perfil.endereco = novo_endereco
                            perfil.save()
                            logger.info(f"edit_profile_view: Novo endereço criado com sucesso - Endereço ID: {novo_endereco.id}, Cidade: {cidade}, Estado: {estado}")
                        except Exception as e:
                            logger.error(f"edit_profile_view: Erro ao criar endereço - Cidade: {cidade}, Estado: {estado}, Erro: {str(e)}", exc_info=True)
                            raise

                logger.info(f"edit_profile_view: Redirecionando após atualização bem-sucedida - Usuário: {user_email}")
                return redirect(reverse("edit_profile") + "?saved=1")
            except Exception as e:
                logger.error(f"edit_profile_view: Erro ao salvar perfil - Usuário: {user_email}, Perfil ID: {perfil.id}, Erro: {str(e)}", exc_info=True)
                raise
        else:
            logger.warning(f"edit_profile_view: Formulário inválido - Usuário: {user_email}, Erros: {form.errors}")

    else:
        form = PerfilForm(instance=perfil)
        logger.debug(f"edit_profile_view: Carregando formulário de edição - Perfil ID: {perfil.id}")

    context = {
        "form": form,
        "perfil": perfil,
        "endereco": endereco,
        "ufs": ufs,
    }

    return render(request, "perfil/page/edit_profile.html", context)
