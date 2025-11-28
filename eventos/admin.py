from django.contrib import admin
from .models import Eventos, Participacao



@admin.register(Participacao)
class ParticipacaoAdmin(admin.ModelAdmin):
    list_display = ['participante', 'evento', 'status', 'data_inscricao', 'avaliacao_host']
    list_filter = ['status', 'data_inscricao']
    search_fields = ['participante__nome_social', 'evento__nome_evento']
    date_hierarchy = 'data_inscricao'


@admin.register(Eventos)
class EventosAdmin(admin.ModelAdmin):
    list_display = ['nome_evento', 'organizador', 'status', 'data_inicio', 'created_at']
    list_filter = ['status', 'aceita_participantes', 'data_inicio']
    search_fields = ['nome_evento', 'descricao', 'local_encontro']
    date_hierarchy = 'data_inicio'
    
    class ParticipacaoInline(admin.TabularInline):
        model = Participacao
        extra = 0
        fields = ['participante', 'status', 'avaliacao_host']
    
    inlines = [ParticipacaoInline]
