import os
from pathlib import Path
import environ
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
env = environ.Env()
load_dotenv(os.path.join(BASE_DIR, '.env'))  # Load .env if available
environ.Env.read_env()  # Optional if you're using django-environ only

# Secret key
SECRET_KEY = env('DJANGO_SECRET_KEY', default="pqu__%t3x2e$+%lk9d#vg-7d=s7$m+b1&u91tfk8#gt*di$xkn")

# Debug mode
DEBUG = env.bool('DEBUG', default=False)

# Allowed hosts and trusted origins
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['iriseupbotsai-production.up.railway.app', 'localhost', '127.0.0.1', '0.0.0.0'])
CSRF_TRUSTED_ORIGINS = [f"https://{host}" for host in ALLOWED_HOSTS if host != 'localhost']

# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyAppConfig',
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'myapp.middleware.MissingStaticFileMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
WSGI_APPLICATION = 'myproject.wsgi.application'

# settings.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'


# Template settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'myapp' / 'templates'],
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

import dj_database_url

DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Session settings
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # Sessions last 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False



# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'myapp' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'



# Authentication redirects
LOGIN_URL = 'custom_login'
LOGOUT_URL = 'custom_logout'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'custom_login'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.template': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

# Third-party API keys
OPENAI_API_KEY = env('OPENAI_API_KEY')
SQUARE_ACCESS_TOKEN = env('SQUARE_ACCESS_TOKEN')
