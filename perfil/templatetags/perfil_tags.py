from django import template
from urllib.parse import quote

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

@register.simple_tag
def get_avatar_url(perfil, nome_fallback=None):
    """
    Retorna a URL do avatar do perfil ou uma imagem padrão.
    Segue o mesmo padrão usado nas outras páginas do projeto.
    
    Args:
        perfil: Objeto Perfil ou None
        nome_fallback: Nome para usar no avatar padrão se não houver perfil (opcional)
    
    Returns:
        URL da imagem do avatar
    """
    # Se tem perfil e foto_perfil, retorna foto_perfil
    if perfil and perfil.foto_perfil:
        return perfil.foto_perfil.url
    
    # Se tem perfil e imagem_url, retorna imagem_url
    if perfil and perfil.imagem_url:
        return perfil.imagem_url
    
    # Avatar padrão usando ui-avatars.com (mesmo padrão das outras páginas)
    # Tenta obter nome do perfil, senão usa nome_fallback, senão 'Usuário'
    if perfil and hasattr(perfil, 'usuario'):
        usuario = perfil.usuario
        nome_avatar = usuario.first_name or usuario.email or nome_fallback or 'Usuário'
    elif nome_fallback:
        nome_avatar = nome_fallback
    else:
        nome_avatar = 'Usuário'
    
    nome_encoded = quote(nome_avatar)
    return f"https://ui-avatars.com/api/?name={nome_encoded}&background=CCEE52&color=004AAD&size=128"
