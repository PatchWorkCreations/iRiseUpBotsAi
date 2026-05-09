import os
from pathlib import Path

import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def get_bool_env(name, default=False):
    return os.getenv(name, str(default)).strip().lower() in {"1", "true", "yes", "on"}


def get_list_env(name, default=None):
    raw_value = os.getenv(name)
    if not raw_value:
        return default or []
    return [item.strip() for item in raw_value.split(",") if item.strip()]


ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")

# Secret key
SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "pqu__%t3x2e$+%lk9d#vg-7d=s7$m+b1&u91tfk8#gt*di$xkn",
)

# Debug mode
DEBUG = get_bool_env("DEBUG", True)

# Allowed hosts and trusted origins
DEFAULT_ALLOWED_HOSTS = ["www.iriseup.ai", "iriseup.ai"]
ALLOWED_HOSTS = list(
    dict.fromkeys(
        get_list_env("ALLOWED_HOSTS", default=DEFAULT_ALLOWED_HOSTS)
        + ["localhost", "127.0.0.1", "0.0.0.0"]
    )
)
CSRF_TRUSTED_ORIGINS = ["https://www.iriseup.ai"]

# Installed apps
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "myapp.apps.MyAppConfig",
    "cloudinary",
    "cloudinary_storage",
    "apscheduler",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "myapp.middleware.MissingStaticFileMiddleware",
    "myapp.middleware.ClearSessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
]

ROOT_URLCONF = "myproject.urls"
WSGI_APPLICATION = "myproject.wsgi.application"

# Template settings
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "myapp" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# Database (DATABASE_URL only)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Add it to your .env file.")
DATABASES = {"default": dj_database_url.parse(DATABASE_URL)}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Session configuration
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600  # Sessions last 2 weeks
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_SECURE = False
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_NAME = "sessionid"

# Static and media files
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "myapp" / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
WHITENOISE_MANIFEST_STRICT = False

# Authentication redirects
LOGIN_URL = "sign_in"
LOGOUT_URL = "sign_in"
LOGIN_REDIRECT_URL = "sign_in"
LOGOUT_REDIRECT_URL = "sign_in"

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django.template": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    },
}

# Email configuration (Resend SMTP)
RESEND_API_KEY = os.getenv("RESEND_API_KEY") or os.getenv("Resend_API_KEY", "")
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.resend.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = get_bool_env("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "resend")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD") or RESEND_API_KEY
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "onboarding@resend.dev")
SUPPORT_EMAIL = os.getenv("SUPPORT_EMAIL", DEFAULT_FROM_EMAIL)

# Third-party API keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SQUARE_ACCESS_TOKEN = os.getenv("SQUARE_ACCESS_TOKEN")
SQUARE_APPLICATION_ID = os.getenv("SQUARE_APPLICATION_ID", "")
SQUARE_LOCATION_ID = os.getenv("SQUARE_LOCATION_ID", "")
SQUARE_ENVIRONMENT = os.getenv("SQUARE_ENVIRONMENT", "production").strip().lower()
PAYPAL_API_BASE = os.getenv("PAYPAL_API_BASE", "https://api-m.paypal.com")
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", "")
PAYPAL_CLIENT_SECRET = os.getenv("PAYPAL_CLIENT_SECRET", "")

AI_PRODUCTS = {
    "414255": "inspire_chat.html",  # Elevate AI
    "414273": "pulse_chat.html",  # Thrive AI
    "414195": "soulspark_chat.html",  # Lumos AI
    "414223": "echo_chat.html",  # Imagine AI
    "414281": "gideon_chat.html",  # Gideon AI
    "414301": "mentor_iq_chat.html",  # Mentor IQ AI
    "414302": "nexus_chat.html",  # Nexara AI
    "414303": "keystone_chat.html",  # Keystone AI
}

CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.getenv("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.getenv("CLOUDINARY_API_KEY"),
    "API_SECRET": os.getenv("CLOUDINARY_API_SECRET"),
}
DEFAULT_FILE_STORAGE = "cloudinary_storage.storage.MediaCloudinaryStorage"

# Global tone prompt for all AI bots
AI_TONE_PROMPT = """
Always speak with a voice that is wise yet witty, kind, compassionate, understanding, intelligent yet humorous.
Your tone should be warm and engaging-like a trusted mentor or a thoughtful friend.
Keep your responses insightful and relatable-long enough to deliver value, short enough to keep attention.
Speak with clarity and purpose. Use real-world examples when helpful.
If unsure of the user's intent, ask thoughtful, clarifying questions.
Even while leaning on your specialty, always reflect the heart and mission of your founder-Maria Gregory: someone who leads with love, wisdom, and humor.
Responses should leave people better, smarter, and more hopeful.
"""

OPENAI_TO_DJANGO_LANG = {
    "en-US": "en",
    "ja-JP": "ja",
    "es-ES": "es",
    "fr-FR": "fr",
    "de-DE": "de",
    "it-IT": "it",
    "pt-PT": "pt",
    "pt-BR": "pt-br",
    "ru-RU": "ru",
    "zh-CN": "zh-hans",
    "zh-TW": "zh-hant",
    "ko-KR": "ko",
    "ar-SA": "ar",
    "tr-TR": "tr",
    "nl-NL": "nl",
    "sv-SE": "sv",
    "pl-PL": "pl",
    "da-DK": "da",
    "no-NO": "no",
    "fi-FI": "fi",
    "he-IL": "he",
    "th-TH": "th",
    "hi-IN": "hi",
    "cs-CZ": "cs",
    "ro-RO": "ro",
    "hu-HU": "hu",
    "sk-SK": "sk",
    "bg-BG": "bg",
    "uk-UA": "uk",
    "vi-VN": "vi",
    "id-ID": "id",
    "ms-MY": "ms",
    "sr-RS": "sr",
    "hr-HR": "hr",
    "el-GR": "el",
    "lt-LT": "lt",
    "lv-LV": "lv",
    "et-EE": "et",
    "sl-SI": "sl",
    "is-IS": "is",
    "sq-AL": "sq",
    "mk-MK": "mk",
    "bs-BA": "bs",
    "ca-ES": "ca",
    "gl-ES": "gl",
    "eu-ES": "eu",
    "hy-AM": "hy",
    "fa-IR": "fa",
    "sw-KE": "sw",
    "ta-IN": "ta",
    "te-IN": "te",
    "kn-IN": "kn",
    "ml-IN": "ml",
    "mr-IN": "mr",
    "pa-IN": "pa",
    "gu-IN": "gu",
    "or-IN": "or",
    "as-IN": "as",
    "ne-NP": "ne",
    "si-LK": "si",
    "af-ZA": "af",
    "bn-IN": "bn",
    "my-MM": "my",
    "zh-HK": "zh-hk",
    "zh-MO": "zh-mo",
    "tl-PH": "tl",
    "ka-GE": "ka",
    "de-AT": "de-at",
    "de-CH": "de-ch",
    "lo-LA": "lo",
}

AVAILABLE_LANGUAGE_CODES = list(OPENAI_TO_DJANGO_LANG.keys())
CSRF_FAILURE_VIEW = "django.views.csrf.csrf_failure"
