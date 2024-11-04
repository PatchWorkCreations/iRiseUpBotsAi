import os
from pathlib import Path
import environ
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
import os

# Fetch the secret key from environment variables with a fallback to a default
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "pqu__%t3x2e$+%lk9d#vg-7d=s7$m+b1&u91tfk8#gt*di$xkn")

DEBUG = True

site_domain = os.getenv('RAILWAY_PUBLIC_DOMAIN', default='')

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000', 
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyAppConfig',
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

# Ensure session backend is properly configured
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Ensure this is enabled for database-backed sessions
SESSION_COOKIE_AGE = 1209600  # Sessions last 2 weeks, can be adjusted
SESSION_SAVE_EVERY_REQUEST = True  # Ensures the session is saved on every request
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keeps the session alive when the browser is closed


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'myapp' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

LOGIN_URL = 'custom_login'
LOGOUT_URL = 'custom_logout'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'custom_login'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# In your Django settings (settings.py), add or update the LOGGING configuration:

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


# Initialize environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Access your variables
'''
PAYPAL_MODE = 'live' 
PAYPAL_CLIENT_ID = env('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = env('PAYPAL_CLIENT_SECRET')
'''
SQUARE_ACCESS_TOKEN = env('SQUARE_ACCESS_TOKEN')


import environ

env = environ.Env()
environ.Env.read_env()  # This loads the .env file and makes env vars available

# Assign the OpenAI API key to settings
OPENAI_API_KEY = env('OPENAI_API_KEY')


import os
from dotenv import load_dotenv

# Load environment variables from Railway or .env
load_dotenv()

# Fetch OpenAI API Key from environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

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

#redis-server (to run redis server locally)
#celery -A myproject flower (to run flower locally)
#python manage.py shell (to run python shell)
#celery -A myproject beat -l info (to run celery beat)
#celery -A myproject worker -l info ( to run cleery worker)

#app = Celery('myproject')
#app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'


#redis://default:lGwEqNTvstKGbtAZqQlkSXYNeXWsvCXe@junction.proxy.rlwy.net:23867 redis url

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')