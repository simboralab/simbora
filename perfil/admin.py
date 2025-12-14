from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Perfil


@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    model = Usuario

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {
            'fields': (
                'first_name',
                'last_name',
                'username',
            )
        }),
        ('Permissões', {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
        ('Datas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
            ),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'nome_social',
        'cpf',
        'genero',
        'data_nascimento',
        'idade',
    )

    search_fields = (
        'cpf',
        'nome_social',
        'usuario__email',
        'usuario__first_name',
        'usuario__last_name',
    )

    raw_id_fields = ('usuario', 'endereco')

    def idade(self, obj):
        return obj.idade

    idade.short_description = 'Idade'
