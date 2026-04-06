"""
Django settings for taskmanager project.
Proyecto: Django Web App - Evaluación Módulo #6 (Alkemy)
"""

from pathlib import Path

# ─── Rutas base ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ─── Seguridad ────────────────────────────────────────────────────────────────
# ADVERTENCIA: en producción, esta clave debe guardarse en variable de entorno
SECRET_KEY = 'django-insecure-cambia-esta-clave-en-produccion-12345abcde'

# En producción cambiar a False
DEBUG = True

ALLOWED_HOSTS = ['*']

# ─── Aplicaciones instaladas ──────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps propias
    'apps.accounts',
    'apps.projects',
]

# ─── Middlewares ──────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',      # Protección CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'taskmanager.urls'

# ─── Templates ────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # carpeta global de templates
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

WSGI_APPLICATION = 'taskmanager.wsgi.application'

# ─── Base de datos (SQLite para desarrollo) ───────────────────────────────────
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ─── Validadores de contraseña ────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─── Internacionalización ─────────────────────────────────────────────────────
LANGUAGE_CODE = 'es-ar'
TIME_ZONE = 'America'
USE_I18N = True
USE_TZ = True

# ─── Archivos estáticos ───────────────────────────────────────────────────────
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# ─── Archivos de medios (imágenes, adjuntos) ──────────────────────────────────
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ─── Autenticación: redirecciones post-login y logout ─────────────────────────
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/projects/'       # Después de loguearse → lista de proyectos
LOGOUT_REDIRECT_URL = '/accounts/login/' # Después de salir → login

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
