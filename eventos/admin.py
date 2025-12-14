from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import Eventos, Participacao



@admin.register(Participacao)
class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ['participante', 'evento', 'status', 'data_inscricao', 'avaliacao_host']
    list_filter = ['status', 'data_inscricao']
    search_fields = ['participante__nome_social', 'evento__nome_evento']
    date_hierarchy = 'data_inscricao'


@admin.register(Eventos)
class EventosAdmin(admin.ModelAdmin):
    list_display = ['nome_evento', 'organizador', 'status', 'categoria', 'data_inicio', 'created_at']
    list_filter = ['status', 'categoria', 'aceita_participantes', 'data_inicio']
    search_fields = ['nome_evento', 'descricao', 'local_encontro']
    date_hierarchy = 'data_inicio'
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome_evento', 'categoria', 'organizador', 'status')
        }),
        ('Descrição e Conteúdo', {
            'fields': ('descricao', 'regras', 'foto', 'foto_url')
        }),
        ('Localização', {
            'fields': ('endereco', 'local_encontro')
        }),
        ('Datas e Horários', {
            'fields': ('data_inicio', 'data_termino', 'data_encontro')
        }),
        ('Participantes', {
            'fields': ('minimo_participantes', 'maximo_participantes', 'aceita_participantes')
        }),
        ('Outros', {
            'fields': ('grupo_whatsapp',)
        }),
    )
    
    class ParticipacaoInline(admin.TabularInline):
        model = Participacao
        extra = 0
        fields = ['participante', 'status', 'avaliacao_host']
    
    inlines = [ParticipacaoInline]
    
    def get_queryset(self, request):
        """
        Filtra eventos para mostrar apenas aqueles onde o usuário é organizador
        Superusuários e usuários que não são do grupo Beta Teste veem todos os eventos
        Membros do grupo Beta Teste só veem seus próprios eventos
        """
        qs = super().get_queryset(request)
        
        # Superusuários veem tudo
        if request.user.is_superuser:
            return qs
        
        # Verifica se é membro do grupo "Beta Teste"
        eh_beta_teste = request.user.is_staff and request.user.groups.filter(name='Beta Teste').exists()
        
        if eh_beta_teste:
            # Membros do Beta Teste só veem eventos onde são organizadores
            if hasattr(request.user, 'perfil') and request.user.perfil:
                return qs.filter(organizador=request.user.perfil)
            else:
                # Se não tem perfil, não vê nenhum evento
                return qs.none()
        
        # Outros usuários staff (não Beta Teste) veem tudo
        return qs
    
    def has_change_permission(self, request, obj=None):
        """
        Verifica se o usuário pode editar o evento
        """
        if obj is None:
            return True
        
        # Superusuários podem editar tudo
        if request.user.is_superuser:
            return True
        
        # Verifica se é membro do grupo "Beta Teste"
        eh_beta_teste = request.user.is_staff and request.user.groups.filter(name='Beta Teste').exists()
        
        if eh_beta_teste:
            # Membros do Beta Teste só podem editar se forem organizadores
            if hasattr(request.user, 'perfil') and request.user.perfil:
                return obj.organizador == request.user.perfil
            return False
        
        # Outros usuários staff podem editar tudo
        return True
    
    def has_delete_permission(self, request, obj=None):
        """
        Verifica se o usuário pode deletar o evento
        """
        if obj is None:
            return True
        
        # Superusuários podem deletar tudo
        if request.user.is_superuser:
            return True
        
        # Verifica se é membro do grupo "Beta Teste"
        eh_beta_teste = request.user.is_staff and request.user.groups.filter(name='Beta Teste').exists()
        
        if eh_beta_teste:
            # Membros do Beta Teste só podem deletar se forem organizadores
            if hasattr(request.user, 'perfil') and request.user.perfil:
                return obj.organizador == request.user.perfil
            return False
        
        # Outros usuários staff podem deletar tudo
        return True
    
    def save_model(self, request, obj, form, change):
        """
        Define automaticamente o organizador como o perfil do usuário ao criar
        Para membros do Beta Teste, sempre define como organizador
        """
        if not change:  # Se está criando um novo evento
            if hasattr(request.user, 'perfil') and request.user.perfil:
                obj.organizador = request.user.perfil
        
        # Verifica permissão antes de salvar (apenas para Beta Teste)
        eh_beta_teste = request.user.is_staff and request.user.groups.filter(name='Beta Teste').exists()
        if change and eh_beta_teste and not self.has_change_permission(request, obj):
            raise PermissionDenied("Você não tem permissão para editar este evento.")
        
        super().save_model(request, obj, form, change)
    
