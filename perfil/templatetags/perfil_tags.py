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
    
    Prioridade: imagem_url > avatar padrão
    Se não houver imagem_url cadastrada, sempre usa o avatar padrão.
    
    Args:
        perfil: Objeto Perfil ou None
        nome_fallback: Nome para usar no avatar padrão se não houver perfil (opcional)
    
    Returns:
        URL da imagem do avatar
    """
    # PRIORIDADE 1: Se tem perfil e imagem_url válida, retorna imagem_url
    if perfil and perfil.imagem_url:
        imagem_url = str(perfil.imagem_url).strip()
        if imagem_url:  # Verifica se não está vazio
            return imagem_url
    
    # Se não tem imagem_url, sempre retorna avatar padrão
    
    # Avatar padrão usando ui-avatars.com (mesmo padrão das outras páginas)
    # Tenta obter nome do perfil, senão usa nome_fallback, senão 'Usuário'
    nome_avatar = 'Usuário'
    
    if perfil:
        # Tenta obter nome do perfil
        if hasattr(perfil, 'nome_completo') and perfil.nome_completo:
            nome_avatar = perfil.nome_completo
        elif hasattr(perfil, 'nome_social') and perfil.nome_social:
            nome_avatar = perfil.nome_social
        elif hasattr(perfil, 'usuario') and perfil.usuario:
            usuario = perfil.usuario
            if hasattr(usuario, 'first_name') and usuario.first_name:
                nome_avatar = usuario.first_name
            elif hasattr(usuario, 'email') and usuario.email:
                nome_avatar = usuario.email
        elif nome_fallback:
            nome_avatar = nome_fallback
    elif nome_fallback:
        nome_avatar = nome_fallback
    
    nome_encoded = quote(str(nome_avatar))
    return f"https://ui-avatars.com/api/?name={nome_encoded}&background=CCEE52&color=004AAD&size=128"
