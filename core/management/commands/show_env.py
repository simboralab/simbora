"""
Comando Django para mostrar o ambiente atual e configurações.
Uso: python manage.py show_env
"""
from django.core.management.base import BaseCommand
from django.conf import settings
from config import settings as dynaconf_settings


class Command(BaseCommand):
    help = 'Mostra o ambiente atual e as configurações carregadas'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('\n' + '=' * 70))
        self.stdout.write(self.style.SUCCESS('  VALIDAÇÃO DE AMBIENTE - SIMBORA'))
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))
        
        # Ambiente Dynaconf
        env = dynaconf_settings.current_env
        import os
        env_var = os.getenv('SIMBORA_ENV', 'não definida (padrão: development)')
        
        # Cores baseadas no ambiente
        if env == 'production':
            env_style = self.style.ERROR
            env_icon = '🔴'
        elif env == 'development':
            env_style = self.style.WARNING
            env_icon = '🟡'
        elif env == 'testing':
            env_style = self.style.SUCCESS
            env_icon = '🟢'
        else:
            env_style = self.style.SUCCESS
            env_icon = '⚪'
        
        self.stdout.write(f'{env_icon} Ambiente Atual: {env_style(env.upper())}')
        self.stdout.write(f'   Variável de ambiente: {env_var}')
        self.stdout.write('')
        
        # Configurações Django
        self.stdout.write(self.style.SUCCESS('Configurações Django:'))
        self.stdout.write(f'  • DEBUG: {self.style.ERROR("True") if settings.DEBUG else self.style.SUCCESS("False")}')
        self.stdout.write(f'  • ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}')
        self.stdout.write(f'  • ENVIRONMENT: {getattr(settings, "ENVIRONMENT", "não definido")}')
        self.stdout.write('')
        
        # Validações
        self.stdout.write(self.style.SUCCESS('Validações:'))
        if env == 'production':
            if settings.DEBUG:
                self.stdout.write(self.style.ERROR('  ⚠️  ATENÇÃO: DEBUG está True em produção!'))
            else:
                self.stdout.write(self.style.SUCCESS('  ✅ DEBUG está False (correto para produção)'))
            
            if not settings.ALLOWED_HOSTS:
                self.stdout.write(self.style.ERROR('  ⚠️  ATENÇÃO: ALLOWED_HOSTS está vazio!'))
            else:
                self.stdout.write(self.style.SUCCESS(f'  ✅ ALLOWED_HOSTS configurado: {settings.ALLOWED_HOSTS}'))
        else:
            self.stdout.write(self.style.WARNING(f'  ℹ️  Ambiente {env} - validações de produção não aplicadas'))
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 70 + '\n'))

