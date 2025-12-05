from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_user_perfil(context):
    """Retorna o perfil do usuário de forma segura, ou None se não existir"""
    # Tenta pegar o usuário do request primeiro (mais confiável)
    request = context.get('request')
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        user = request.user
    else:
        # Fallback para o contexto padrão do Django
        user = context.get('user')
    
    if not user or not user.is_authenticated:
        return None
    
    try:
        # Tenta acessar o perfil via relacionamento OneToOne
        if hasattr(user, 'perfil'):
            return user.perfil
        return None
    except Exception:
        return None
