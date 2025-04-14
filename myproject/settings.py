import os
from pathlib import Path
import environ
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize django-environ
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")  # This resolves to E:/Downloads/iRiseUpBotsAi/.env

if os.path.exists(env_file):
    env.read_env(env_file)
    print(f"✅ Loaded environment from: {env_file}")
else:
    print("⚠️ .env file not found, falling back to system environment variables.")


# Secret key
SECRET_KEY = env('DJANGO_SECRET_KEY', default="pqu__%t3x2e$+%lk9d#vg-7d=s7$m+b1&u91tfk8#gt*di$xkn")

# Debug mode
DEBUG = env.bool('DEBUG', default=True)

# Allowed hosts and trusted origins
ALLOWED_HOSTS = ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=[' www.iriseup.ai', 'localhost', '127.0.0.1', '0.0.0.0'])
CSRF_TRUSTED_ORIGINS = ["https://www.iriseup.ai"]


# Installed apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp.apps.MyAppConfig',
    'cloudinary',
    'cloudinary_storage',
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
    'django.middleware.locale.LocaleMiddleware',
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


import cloudinary
import cloudinary.uploader
import cloudinary.api
import os

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}

DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"


# Global tone prompt for all AI bots
AI_TONE_PROMPT = """
Always speak with a voice that is wise yet witty, kind, compassionate, understanding, intelligent yet humorous.
Your tone should be warm and engaging—like a trusted mentor or a thoughtful friend.
Keep your responses insightful and relatable—long enough to deliver value, short enough to keep attention.
Speak with clarity and purpose. Use real-world examples when helpful.
If unsure of the user's intent, ask thoughtful, clarifying questions.
Even while leaning on your specialty, always reflect the heart and mission of your founder—Maria Gregory: someone who leads with love, wisdom, and humor.
Responses should leave people better, smarter, and more hopeful.
"""

# settings.py

OPENAI_TO_DJANGO_LANG = {
    'en-US': 'en', 'ja-JP': 'ja', 'es-ES': 'es', 'fr-FR': 'fr', 'de-DE': 'de',
    'it-IT': 'it', 'pt-PT': 'pt', 'pt-BR': 'pt-br', 'ru-RU': 'ru', 'zh-CN': 'zh-hans',
    'zh-TW': 'zh-hant', 'ko-KR': 'ko', 'ar-SA': 'ar', 'tr-TR': 'tr', 'nl-NL': 'nl',
    'sv-SE': 'sv', 'pl-PL': 'pl', 'da-DK': 'da', 'no-NO': 'no', 'fi-FI': 'fi',
    'he-IL': 'he', 'th-TH': 'th', 'hi-IN': 'hi', 'cs-CZ': 'cs', 'ro-RO': 'ro',
    'hu-HU': 'hu', 'sk-SK': 'sk', 'bg-BG': 'bg', 'uk-UA': 'uk', 'vi-VN': 'vi',
    'id-ID': 'id', 'ms-MY': 'ms', 'sr-RS': 'sr', 'hr-HR': 'hr', 'el-GR': 'el',
    'lt-LT': 'lt', 'lv-LV': 'lv', 'et-EE': 'et', 'sl-SI': 'sl', 'is-IS': 'is',
    'sq-AL': 'sq', 'mk-MK': 'mk', 'bs-BA': 'bs', 'ca-ES': 'ca', 'gl-ES': 'gl',
    'eu-ES': 'eu', 'hy-AM': 'hy', 'fa-IR': 'fa', 'sw-KE': 'sw', 'ta-IN': 'ta',
    'te-IN': 'te', 'kn-IN': 'kn', 'ml-IN': 'ml', 'mr-IN': 'mr', 'pa-IN': 'pa',
    'gu-IN': 'gu', 'or-IN': 'or', 'as-IN': 'as', 'ne-NP': 'ne', 'si-LK': 'si',
    'af-ZA': 'af', 'bn-IN': 'bn', 'my-MM': 'my', 'zh-HK': 'zh-hk', 'zh-MO': 'zh-mo',
    'tl-PH': 'tl', 'ka-GE': 'ka', 'de-AT': 'de-at', 'de-CH': 'de-ch', 'lo-LA': 'lo'
}

# Optional: for convenience in views
AVAILABLE_LANGUAGE_CODES = list(OPENAI_TO_DJANGO_LANG.keys())
