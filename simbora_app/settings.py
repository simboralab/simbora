from pathlib import Path
import os
import dj_database_url
from config import settings

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = settings.get('SECRET_KEY')
FIELD_ENCRYPTION_KEY = settings.get('FIELD_ENCRYPTION_KEY')


DEBUG = settings.get('DEBUG', False)

# ALLOWED_HOSTS: Dynaconf gerencia via settings.toml
# O Dynaconf já retorna uma lista quando configurado como lista no TOML
# No Render, pode definir SIMBORA_ALLOWED_HOSTS via variável de ambiente
# ou será adicionado automaticamente o RENDER_EXTERNAL_HOSTNAME abaixo
ALLOWED_HOSTS = list(settings.get('ALLOWED_HOSTS', []))
# Adicionar RENDER_EXTERNAL_HOSTNAME se disponível (Render define automaticamente)
# Isso permite que o Render adicione o hostname sem precisar configurar manualmente
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME and RENDER_EXTERNAL_HOSTNAME not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

ENVIRONMENT = settings.current_env

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'perfil',
    'core',
    'eventos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Adicionado para servir static files no Render
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'simbora_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'simbora_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Configuração para usar PostgreSQL no Render ou SQLite localmente
# O dj_database_url lê DATABASE_URL diretamente do ambiente (padrão do Render)
# O Dynaconf também pode fornecer via SIMBORA_DATABASE_URL se necessário
# Prioridade: DATABASE_URL (ambiente) > SIMBORA_DATABASE_URL (Dynaconf) > SQLite (padrão)
database_url = os.environ.get('DATABASE_URL') or settings.get('DATABASE_URL', None)
DATABASES = {
    'default': dj_database_url.config(
        # Valor padrão para desenvolvimento local (SQLite)
        # Em produção no Render, DATABASE_URL será fornecido automaticamente
        default=database_url or ('sqlite:///' + str(BASE_DIR / 'db.sqlite3')),
        conn_max_age=600
    )
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'perfil.Usuario'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# Usar settings.get() com valores padrão para evitar erros de acesso
LANGUAGE_CODE = settings.get('LANGUAGE_CODE', 'pt-BR')

TIME_ZONE = settings.get('TIME_ZONE', 'America/Sao_Paulo')

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração do WhiteNoise para produção (Render)
if not DEBUG:
    # Enable the WhiteNoise storage backend, which compresses static files
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = settings.get('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = settings.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = settings.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = settings.get('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = settings.get('EMAIL_HOST_USER', 'suporte.simbora.app@gmail.com')
EMAIL_HOST_PASSWORD = settings.get('simbora_password', '')
DEFAULT_FROM_EMAIL = settings.get('DEFAULT_FROM_EMAIL', 'suporte.simbora.app@gmail.com')
