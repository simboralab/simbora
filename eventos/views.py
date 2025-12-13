from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Eventos, Participacao

def lista_eventos(request):
    eventos = Eventos.objects.all().order_by("-data_inicio")
    return render(request, "eventos/lista_eventos.html", {"eventos": eventos})


def visualizar_evento(request, evento_id):
    evento = get_object_or_404(Eventos, id=evento_id)

    # Verifica se o usuário autenticado é o organizador
    eh_organizador = False
    usuario_confirmado = False
    
    if request.user.is_authenticated:
        try:
            if hasattr(request.user, 'perfil') and request.user.perfil:
                perfil_usuario = request.user.perfil
                # Verifica se é o organizador
                if evento.organizador and evento.organizador.id == perfil_usuario.id:
                    eh_organizador = True
                    usuario_confirmado = True  # Organizador está automaticamente confirmado
                    print(f"DEBUG: Usuário {request.user.email} é organizador do evento {evento.id}")
                else:
                    # Verifica se já está inscrito/confirmado
                    # Considera qualquer participação que não seja CANCELADO ou AUSENTE
                    # Status válidos: INSCRITO, CONFIRMADO, LISTA_ESPERA, PRESENTE
                    tem_participacao_valida = evento.participacoes.filter(
                        participante=perfil_usuario
                    ).exclude(status__in=['CANCELADO', 'AUSENTE']).exists()
                    
                    if tem_participacao_valida:
                        usuario_confirmado = True
                        # Pega o status para debug
                        participacao = evento.participacoes.filter(
                            participante=perfil_usuario
                        ).exclude(status__in=['CANCELADO', 'AUSENTE']).first()
                        print(f"DEBUG: Usuário {request.user.email} está inscrito no evento {evento.id} com status: {participacao.status if participacao else 'N/A'}")
                    else:
                        # Verifica se existe alguma participação (mesmo cancelada) para debug
                        todas_participacoes = evento.participacoes.filter(participante=perfil_usuario).all()
                        if todas_participacoes.exists():
                            print(f"DEBUG: Usuário {request.user.email} tem participação no evento {evento.id} mas com status inválido:")
                            for p in todas_participacoes:
                                print(f"  - Status: {p.status}")
                        else:
                            print(f"DEBUG: Usuário {request.user.email} NÃO tem participação no evento {evento.id}")
            else:
                print(f"DEBUG: Usuário {request.user.email} não tem perfil associado")
        except Exception as e:
            print(f"DEBUG: Erro ao verificar participação do usuário {request.user.email if request.user.is_authenticated else 'anônimo'}: {e}")
            import traceback
            traceback.print_exc()

    # Conta participantes ativos: INSCRITOS e CONFIRMADOS
    # (exclui CANCELADOS, AUSENTES, etc e participantes sem perfil)
    participantes_ativos = evento.participacoes.exclude(
        status__in=['CANCELADO', 'AUSENTE']
    ).exclude(
        participante__isnull=True
    )
    
    # DEBUG: Log detalhado para diagnóstico
    print(f"\n=== DEBUG CONTAGEM EVENTO {evento.id} ===")
    print(f"Nome do evento: {evento.nome_evento}")
    print(f"Organizador: {evento.organizador}")
    
    # Lista todas as participações para debug
    todas_participacoes = evento.participacoes.all()
    print(f"\nTotal de participações no banco: {todas_participacoes.count()}")
    for p in todas_participacoes:
        print(f"  - Participante: {p.participante}, Status: {p.status}, Participante é None: {p.participante is None}")
    
    print(f"\nParticipantes ativos (após filtros): {participantes_ativos.count()}")
    for p in participantes_ativos:
        print(f"  - Participante: {p.participante}, Status: {p.status}")
    
    # Se o organizador não estiver na lista de participantes, adiciona ele
    if evento.organizador and not participantes_ativos.filter(participante=evento.organizador).exists():
        # O organizador conta como participante confirmado automaticamente
        pass  # Não vamos criar participação, apenas contar ele
    
    # Para exibição, mostra apenas CONFIRMADOS na galera
    confirmados = evento.participacoes.filter(
        status='CONFIRMADO',
        participante__isnull=False
    )
    
    # Total de participantes ativos (INSCRITO + CONFIRMADO + LISTA_ESPERA + PRESENTE)
    # Conta o organizador também, pois ele é um participante
    total_confirmados = participantes_ativos.count()
    
    # Se organizador não está na lista de participações, conta ele também
    organizador_na_lista = False
    if evento.organizador:
        organizador_na_lista = participantes_ativos.filter(participante=evento.organizador).exists()
        print(f"Organizador ID: {evento.organizador.id}")
        print(f"Organizador na lista de participantes ativos: {organizador_na_lista}")
        if not organizador_na_lista:
            total_confirmados += 1  # Conta o organizador
            print(f"Organizador adicionado ao total. Total agora: {total_confirmados}")
        else:
            print(f"Organizador já está na lista, não precisa adicionar. Total: {total_confirmados}")
    
    print(f"Total final de confirmados: {total_confirmados}")
    print(f"Máximo de participantes: {evento.maximo_participantes}")
    print(f"=== FIM DEBUG ===\n")
    
    # Adiciona organizador à lista de participantes ativos para exibição (se não estiver)
    participantes_para_exibicao = list(participantes_ativos)
    if evento.organizador and not organizador_na_lista:
        # Cria um objeto simples para representar o organizador como participante
        class ParticipacaoVirtual:
            def __init__(self, participante):
                self.participante = participante
                self.status = 'CONFIRMADO'
                self.id = None
        
        organizador_participacao = ParticipacaoVirtual(evento.organizador)
        participantes_para_exibicao.insert(0, organizador_participacao)

    if evento.maximo_participantes:
        try:
            progresso = int((total_confirmados / evento.maximo_participantes) * 100)
        except (TypeError, ZeroDivisionError):
            progresso = 0
        progresso = min(max(progresso, 0), 100)
    else:
        progresso = 0

    if evento.maximo_participantes:
        faltam = max(evento.maximo_participantes - total_confirmados, 0)
    else:
        faltam = None

    # Verifica se está lotado (incluindo organizador)
    esta_lotado = False
    if evento.maximo_participantes is not None:
        esta_lotado = total_confirmados >= evento.maximo_participantes

    contexto = {
        "evento": evento,
        "confirmados": confirmados,  # Apenas CONFIRMADOS para exibição na galera
        "participantes_ativos": participantes_ativos,  # QuerySet original
        "participantes_para_exibicao": participantes_para_exibicao,  # Lista com organizador incluído
        "total_confirmados": total_confirmados,  # Total de participantes ativos
        "progresso": progresso,
        "faltam": faltam,
        "esta_lotado": esta_lotado,
        "eh_organizador": eh_organizador,
        "usuario_confirmado": usuario_confirmado,
    }

    return render(request, "eventos/visualizar_evento.html", contexto)


@login_required
@require_http_methods(["POST"])
def confirmar_presenca(request, evento_id):
    """
    View para confirmar presença em um evento via AJAX
    """
    try:
        evento = get_object_or_404(Eventos, id=evento_id)
        
        # Verifica se o usuário tem perfil
        if not hasattr(request.user, 'perfil') or request.user.perfil is None:
            return JsonResponse({
                'success': False,
                'error': 'Perfil não encontrado. Complete seu cadastro primeiro.'
            }, status=400)
        
        perfil = request.user.perfil
        
        # Verifica se é o organizador
        if evento.organizador and evento.organizador.id == perfil.id:
            return JsonResponse({
                'success': False,
                'error': 'Você é o organizador deste evento e já está automaticamente confirmado!'
            }, status=400)
        
        # Verifica se já existe uma participação
        participacao_existente = None
        try:
            participacao_existente = Participacao.objects.get(evento=evento, participante=perfil)
        except Participacao.DoesNotExist:
            pass
        
        # Se não existe participação, verifica se pode criar uma nova
        if not participacao_existente:
            # Debug: log do status do evento
            print(f"DEBUG - Status do evento: {evento.status}")
            print(f"DEBUG - Aceita participantes: {evento.aceita_participantes}")
            
            # Verifica se o evento está cancelado ou finalizado
            if evento.status in ['CANCELADO', 'FINALIZADO']:
                return JsonResponse({
                    'success': False,
                    'error': f'Este evento não está mais disponível para inscrições. (Status: {evento.get_status_display()})'
                }, status=400)
            
            # Para eventos ATIVOS, sempre permite inscrição (ignora aceita_participantes)
            # O campo aceita_participantes pode ser usado para controle administrativo,
            # mas não bloqueia inscrições para eventos ativos
            # Se necessário bloquear, o organizador deve cancelar ou finalizar o evento
            
            # Verifica se o evento está lotado (só para novos participantes)
            # Conta o organizador também, pois ele ocupa uma vaga
            participantes_ativos = evento.participacoes.exclude(
                status__in=['CANCELADO', 'AUSENTE']
            ).exclude(participante__isnull=True)
            
            total_confirmados = participantes_ativos.count()
            # Se organizador não está na lista, conta ele também
            if evento.organizador and not participantes_ativos.filter(participante=evento.organizador).exists():
                total_confirmados += 1  # Conta o organizador
            
            # Debug: log dos valores
            print(f"DEBUG - Evento ID: {evento.id}")
            print(f"DEBUG - Total confirmados: {total_confirmados}")
            print(f"DEBUG - Máximo participantes: {evento.maximo_participantes}")
            print(f"DEBUG - Organizador na lista: {participantes_ativos.filter(participante=evento.organizador).exists() if evento.organizador else 'N/A'}")
            print(f"DEBUG - Comparação lotação: {total_confirmados} >= {evento.maximo_participantes} = {total_confirmados >= evento.maximo_participantes if evento.maximo_participantes else 'N/A'}")
            
            # Só verifica lotação se tiver máximo definido
            if evento.maximo_participantes is not None:
                if total_confirmados >= evento.maximo_participantes:
                    return JsonResponse({
                        'success': False,
                        'error': f'Este evento está lotado. ({total_confirmados}/{evento.maximo_participantes} participantes)'
                    }, status=400)
            
            # Cria nova participação com status CONFIRMADO usando get_or_create para evitar duplicatas
            try:
                participacao, created = Participacao.objects.get_or_create(
                    evento=evento,
                    participante=perfil,
                    defaults={'status': 'CONFIRMADO'}
                )
                # Se já existia mas estava cancelada/ausente, atualiza para CONFIRMADO
                if not created and participacao.status in ['CANCELADO', 'AUSENTE']:
                    participacao.status = 'CONFIRMADO'
                    participacao.save()
            except Exception as e:
                # Se ainda assim der erro de duplicata, tenta buscar a existente
                import traceback
                print(f"Erro ao criar participação: {str(e)}")
                print(traceback.format_exc())
                try:
                    participacao = Participacao.objects.get(evento=evento, participante=perfil)
                    # Atualiza status se necessário
                    if participacao.status in ['CANCELADO', 'AUSENTE']:
                        participacao.status = 'CONFIRMADO'
                        participacao.save()
                except Participacao.DoesNotExist:
                    # Se não encontrou, retorna erro
                    return JsonResponse({
                        'success': False,
                        'error': 'Erro ao processar inscrição. Tente novamente.'
                    }, status=400)
        else:
            # Se já existe participação, processa normalmente (mesmo se aceita_participantes=False)
            participacao = participacao_existente
            
            # Se já existe e está confirmado ou inscrito
            if participacao.status in ['CONFIRMADO', 'INSCRITO']:
                # Se está apenas INSCRITO, atualiza para CONFIRMADO
                if participacao.status == 'INSCRITO':
                    participacao.status = 'CONFIRMADO'
                    participacao.save()
                
                # Recalcula total após possível atualização
                # Conta o organizador também, pois ele ocupa uma vaga
                participantes_ativos = evento.participacoes.exclude(
                    status__in=['CANCELADO', 'AUSENTE']
                ).exclude(participante__isnull=True)
                
                total_confirmados = participantes_ativos.count()
                # Se organizador não está na lista, conta ele também
                if evento.organizador and not participantes_ativos.filter(participante=evento.organizador).exists():
                    total_confirmados += 1
                
                # Calcula informações atualizadas
                if evento.maximo_participantes:
                    try:
                        progresso = int((total_confirmados / evento.maximo_participantes) * 100)
                    except (TypeError, ZeroDivisionError):
                        progresso = 0
                    progresso = min(max(progresso, 0), 100)
                    faltam = max(evento.maximo_participantes - total_confirmados, 0)
                    esta_lotado = total_confirmados >= evento.maximo_participantes
                else:
                    progresso = 0
                    faltam = None
                    esta_lotado = False
                
                return JsonResponse({
                    'success': True,
                    'total_confirmados': total_confirmados,
                    'maximo_participantes': evento.maximo_participantes,
                    'progresso': progresso,
                    'faltam': faltam,
                    'esta_lotado': esta_lotado,
                    'grupo_whatsapp': evento.grupo_whatsapp,
                    'message': 'Presença confirmada com sucesso!',
                    'ja_confirmado': True
                })
            
            # Se existe mas está cancelado ou ausente, atualiza o status
            if participacao.status in ['CANCELADO', 'AUSENTE']:
                participacao.status = 'CONFIRMADO'
                participacao.save()
        
        # Recalcula total de confirmados (para ambos os casos: nova ou existente)
        # Conta o organizador também, pois ele ocupa uma vaga
        participantes_ativos = evento.participacoes.exclude(
            status__in=['CANCELADO', 'AUSENTE']
        ).exclude(participante__isnull=True)
        
        total_confirmados = participantes_ativos.count()
        # Se organizador não está na lista, conta ele também
        if evento.organizador and not participantes_ativos.filter(participante=evento.organizador).exists():
            total_confirmados += 1
        
        # Calcula progresso e outras informações
        if evento.maximo_participantes:
            try:
                progresso = int((total_confirmados / evento.maximo_participantes) * 100)
            except (TypeError, ZeroDivisionError):
                progresso = 0
            progresso = min(max(progresso, 0), 100)
            faltam = max(evento.maximo_participantes - total_confirmados, 0)
            esta_lotado = total_confirmados >= evento.maximo_participantes
        else:
            progresso = 0
            faltam = None
            esta_lotado = False
        
        # Retorna resposta JSON com todas as informações atualizadas
        return JsonResponse({
            'success': True,
            'total_confirmados': total_confirmados,
            'maximo_participantes': evento.maximo_participantes,
            'progresso': progresso,
            'faltam': faltam,
            'esta_lotado': esta_lotado,
            'grupo_whatsapp': evento.grupo_whatsapp,
            'message': 'Presença confirmada com sucesso!',
            'ja_confirmado': False  # Sempre False para nova confirmação
        })
        
    except Exception as e:
        # Log do erro para debug
        import traceback
        error_msg = str(e)
        print(f"Erro ao confirmar presença: {error_msg}")
        print(traceback.format_exc())
        
        # Se for erro de duplicata, tenta buscar a participação existente e retornar sucesso
        if 'UNIQUE constraint' in error_msg or 'duplicate key' in error_msg.lower():
            try:
                evento = get_object_or_404(Eventos, id=evento_id)
                perfil = request.user.perfil
                participacao = Participacao.objects.get(evento=evento, participante=perfil)
                
                # Recalcula totais
                participantes_ativos = evento.participacoes.exclude(
                    status__in=['CANCELADO', 'AUSENTE']
                ).exclude(participante__isnull=True)
                total_confirmados = participantes_ativos.count()
                if evento.organizador and not participantes_ativos.filter(participante=evento.organizador).exists():
                    total_confirmados += 1
                
                # Retorna sucesso mesmo sendo duplicata (usuário já estava inscrito)
                return JsonResponse({
                    'success': True,
                    'total_confirmados': total_confirmados,
                    'maximo_participantes': evento.maximo_participantes,
                    'message': 'Você já está confirmado neste evento!',
                    'ja_confirmado': True
                })
            except Exception:
                # Se não conseguir buscar, retorna erro amigável
                return JsonResponse({
                    'success': False,
                    'error': 'Você já está inscrito neste evento.'
                }, status=400)
        
        # Para outros erros, retorna mensagem genérica
        return JsonResponse({
            'success': False,
            'error': 'Erro ao processar solicitação. Tente novamente.'
        }, status=500)