import os
from datetime import timedelta
from django.utils.translation import gettext_lazy as _
from config.env import BASE_DIR, env
from config.settings.cache_redis import *  # noqa
from config.settings.celery import *  # noqa
from config.settings.cors import *  # noqa

# from config.settings.sentry import *  # noqa
from config.settings.sessions import *  # noqa
from config.settings.silk import *  # noqa

env.read_env(os.path.join(BASE_DIR, ".env"))

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_filters",
    "rest_framework.authtoken",
    "silk",
    "django_elasticsearch_dsl",
    "django.contrib.sites",
    "dj_rest_auth",
    "config.apps.authantification",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth.registration",
    "django_extensions",
    "django",
    "config.apps.Loan",
    "corsheaders",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "config.apps.search",
]
SITE_ID = 1

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    'django.middleware.locale.LocaleMiddleware',
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
 
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "loans" / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"

AUTH_USER_MODEL = "authantification.User"

# Database (to be overridden in specific environments)
DATABASES = {}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization settings
LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('nl', _('Dutch')),
    ('pl', _('Polish')),
    ('pt', _('Portuguese')),
    ('ru', _('Russian')),
]
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'Loans/','media'


STATIC_URL = '/static/'

# Directory where collected static files will be stored
STATIC_ROOT = '/vol/static/'


# If you want to collect static files from additional locations

# Email settings

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "ORDERING_PARAM": "ordering",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    # "DEFAULT_THROTTLE_RATES": {
    #     "anon": "100/day",
    #     "user": "1000/day",
    # },
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_THROTTLE_CLASSES": (
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Loan Management API",
    "DESCRIPTION": "API documentation for the Loan Management project",
    "VEfrom elasticsearch_dsl.connections import connectionsRSION": "1.0.0",
    "CONTACT": {"name": "Ndikumana Idris", "email": "ndiku6241@gmail.com"},
    "LICENSE": {"name": "MIT License"},
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
}

REST_AUTH = {
    "USER_DETAILS_SERIALIZER": "dj_rest_auth.serializers.UserDetailsSerializer",
    "REGISTER_SERIALIZER": "config.apps.authantification.serializers.RegisterSerializer",
    "REGISTER_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "SESSION_LOGIN": True,
    "USE_JWT": False,
    "JWT_AUTH_COOKIE": "auth",
    "JWT_AUTH_HTTPONLY": False,
    "PASSWORD_RESET_USE_SITES_DOMAIN": False,
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=12),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

ACCOUNT_EMAIL_REQUIRED = False
# ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCOUNT_LOGIN_METHODS = {'username', 'email'}

SILKY_AUTHENTICATION = True  # Enables authentication for Silk views
SILKY_AUTHORISATION = True  # Enables authorization for Silk views
SILKY_META = True  # Logs meta details about requests
SILKY_PYTHON_PROFILER = True  # Enables Python profiling
SILKY_MAX_RECORDED_REQUESTS = 1000  # Limit on the number of requests to store


# Elasticsearch settings
# settings.py

ELASTICSEARCH_DSL = {
    'default': {
        "hosts": "http://elasticsearch:9200", # Use HTTPS if security is enabled
        'http_auth': ('elastic', 'idris23'),  # Username and password
        'verify_certs': False,  # Disable SSL verification (only for local dev)
    },
}



# If you want to use a different cache backend, you can modify this settings accordingly.
