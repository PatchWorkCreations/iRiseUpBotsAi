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
DEBUG = env.bool('DEBUG', default=True)

# Allowed hosts and trusted origins
ALLOWED_HOSTS = ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[' www.iriseup.ai', 'localhost', '127.0.0.1', '0.0.0.0'])
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
    'myapp.middleware.ClearSessionMiddleware',
]

ROOT_URLCONF = 'myproject.urls'
WSGI_APPLICATION = 'myproject.wsgi.application'

# settings.py
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
manifest_strict = False

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

import environ
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environ
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

USE_SQLITE = env.bool('USE_SQLITE', default=False)  # Default is False to prioritize PostgreSQL
if USE_SQLITE:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(default=env('DATABASE_URL'))
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Session settings
# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 1209600  # Sessions last 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Session Cookie Configuration
SESSION_COOKIE_SECURE = False          # Set to True if using HTTPS
SESSION_COOKIE_HTTPONLY = True         # Helps to prevent JavaScript access to the session cookie
SESSION_COOKIE_SAMESITE = 'Lax'        # Limits cross-site request forgery; use 'None' only if cross-site requests are needed
SESSION_COOKIE_NAME = 'sessionid'      # Default name for the Django session cookie; you can customize if necessary




# Static and media files
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'myapp' / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
WHITENOISE_MANIFEST_STRICT = False



# Authentication redirects
LOGIN_URL = 'sign_in'
LOGOUT_URL = 'sign_in'
LOGIN_REDIRECT_URL = 'sign_in'
LOGOUT_REDIRECT_URL = 'sign_in'

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
   
import os

import os
import environ

# Initialize django-environ
env = environ.Env()

# Load environment variables from .env file (if exists)
environ.Env.read_env()

# Function to fetch environment variables with fallback to os.getenv
def get_env(var_name, default=None):
    """
    Fetch environment variable using django-environ first,
    then fallback to os.getenv if not found.
    """
    return env(var_name, default=os.getenv(var_name, default))

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('EMAIL_HOST', default='smtp.gmail.com')
EMAIL_PORT = int(get_env('EMAIL_PORT', default=587))
EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', default=True) in [True, 'True', 'true', 1, '1']
EMAIL_HOST_USER = get_env('EMAIL_HOST_USER', default='iriseupgroupofcompanies@gmail.com')
EMAIL_HOST_PASSWORD = get_env('EMAIL_HOST_PASSWORD')  # App password
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', default=EMAIL_HOST_USER)

# Third-party API keys
OPENAI_API_KEY = env('OPENAI_API_KEY')
SQUARE_ACCESS_TOKEN = env('SQUARE_ACCESS_TOKEN')


AI_PRODUCTS = {
    "414255": "inspire_chat.html",      # Elevate AI   1
    "414273": "pulse_chat.html",        # Thrive AI   1
    "414195": "soulspark_chat.html",    # Lumos AI   1
    "414223": "echo_chat.html",         # Imagine AI  1
    "414281": "gideon_chat.html",       # Gideon AI  1
    "414301": "mentor_iq_chat.html",    # Mentor IQ AI (New Product ID)
    "414302": "nexus_chat.html",        # Nexara AI (New Product ID)
    "414303": "keystone_chat.html",     # Keystone AI (New Product ID)  1
}
