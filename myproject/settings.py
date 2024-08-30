import os
from pathlib import Path
from celery import Celery
from celery.schedules import crontab
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
DEBUG = True

site_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN', default='')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    site_domain,
    # Add any other domains or IPs as needed
]

CSRF_TRUSTED_ORIGINS = [
    f'https://{site_domain}',
    'http://localhost:8000',  # Add other domains as needed
]

# Application definition
INSTALLED_APPS = [
    'customadmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyAppConfig',
    'django_celery_beat',
    'django_celery_results',
    'django_celery_flower',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'myapp', 'templates')],
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



WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'railway',
        'USER': 'postgres',
        'PASSWORD': 'CJWXRVupUzQgccKlpPkzLsbiYbyJMDLf',
        'HOST': 'monorail.proxy.rlwy.net',
        'PORT': '52974',
    }
}



# Password validation
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'myapp/static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_URL = 'custom_login'
LOGOUT_URL = 'custom_logout'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'custom_login'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'juliavictorio16@gmail.com'
EMAIL_HOST_PASSWORD = 'lovi mltt gpzl tgcf'
DEFAULT_FROM_EMAIL = 'Test account'


# In your Django settings (settings.py), add or update the LOGGING configuration:

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        # You can add your custom logger here
        'myapp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [
   os.path.join(BASE_DIR, 'myapp', 'static'),
]



# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Access your variables
PAYPAL_MODE = 'sandbox' 
PAYPAL_CLIENT_ID = env('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = env('PAYPAL_CLIENT_SECRET')


SQUARE_ACCESS_TOKEN = env('SQUARE_ACCESS_TOKEN')

# settings.py


import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Celery Configuration
# myproject/settings.py
#CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
if os.getenv('RAILWAY_ENVIRONMENT'):
   CELERY_BROKER_URL = os.getenv('REDIS_URL') 
else:
   CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'

CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_EXTENDED = True
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Manila'
TIME_ZONE = 'Asia/Manila'
USE_TZ = True
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True






#app = Celery('myproject')
#app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'


#redis://default:lGwEqNTvstKGbtAZqQlkSXYNeXWsvCXe@junction.proxy.rlwy.net:23867 redis url