from django.contrib import admin
from .models import Endereco

@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = ('nome_do_local', 'rua', 'numero', 'cidade', 'estado', 'cep')
    search_fields = ('nome_do_local', 'rua', 'cidade', 'estado', 'cep')
    fieldsets = (
        ('Local', {
            'fields': ('nome_do_local',)
        }),
        ('Endereço', {
            'fields': ('rua', 'numero', 'complemento', 'bairro', 'cidade', 'estado', 'cep')
        }),
    )