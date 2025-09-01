"""
Django settings for gestao_patrimonial project.
Gerado por 'django-admin startproject'
"""

from pathlib import Path
from decouple import config, Csv
import dj_database_url
import os

# -------------------------------------------------------------------
# Caminho base do projeto
# -------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# Segurança
# -------------------------------------------------------------------
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
CSRF_TRUSTED_ORIGINS = ['https://*.ngrok-free.app']

# -------------------------------------------------------------------
# Configuração de arquivos estáticos (CSS, JS, imagens)
# -------------------------------------------------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
os.makedirs(BASE_DIR / "static", exist_ok=True)

# -------------------------------------------------------------------
# Arquivos de mídia (uploads)
# -------------------------------------------------------------------
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
os.makedirs(MEDIA_ROOT, exist_ok=True)

# -------------------------------------------------------------------
# Internacionalização
# -------------------------------------------------------------------
LANGUAGE_CODE = 'pt-br'
# TIME_ZONE = 'America/Sao_Paulo'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

# -------------------------------------------------------------------
# Configuração dos templates
# -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
            BASE_DIR / "interface" / "templates",
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'builtins': [
                "core.templatetags.saldo",
            ],
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------------------------------------------------
# Aplicações instaladas
# -------------------------------------------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'core',
    'interface',
]

# -------------------------------------------------------------------
# Middleware
# -------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -------------------------------------------------------------------
# Configuração de URLs
# -------------------------------------------------------------------
ROOT_URLCONF = 'gestao_patrimonial.urls'

# -------------------------------------------------------------------
# WSGI
# -------------------------------------------------------------------
WSGI_APPLICATION = 'gestao_patrimonial.wsgi.application'

# -------------------------------------------------------------------
# Banco de Dados
# -------------------------------------------------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('POSTGRES_DB'),
        'USER': config('POSTGRES_USER'),
        'PASSWORD': config('POSTGRES_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'client_encoding': 'UTF8',
        },
    }
}

# Alternativa com DATABASE_URL (descomente se quiser usar em produção):
# DATABASES = {
#     'default': dj_database_url.parse(
#         config('DATABASE_URL', default='postgres://postgres:123@localhost:5432/gestao_utf8'),
#         conn_max_age=600
#     )
# }

# -------------------------------------------------------------------
# Django REST Framework
# -------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}

# -------------------------------------------------------------------
# Campos padrões de chaves primárias
# -------------------------------------------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------------------------------------------
# Login e redirecionamento
# -------------------------------------------------------------------
LOGIN_REDIRECT_URL = 'lista_produtos'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

# -------------------------------------------------------------------
# Usuário personalizado
# -------------------------------------------------------------------
AUTH_USER_MODEL = 'core.Usuario'

# -------------------------------------------------------------------
# Cosmos API
# -------------------------------------------------------------------
COSMOS_API_KEY = config('COSMOS_API_KEY')
COSMOS_API_URL = config('COSMOS_API_URL')
