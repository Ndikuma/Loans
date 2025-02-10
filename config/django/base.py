import os
from datetime import timedelta

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
        "DIRS": [],
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

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = "static/"
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
    "DEFFAUT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 1,
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
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "optional"

SILKY_AUTHENTICATION = True  # Enables authentication for Silk views
SILKY_AUTHORISATION = True  # Enables authorization for Silk views
SILKY_META = True  # Logs meta details about requests
SILKY_PYTHON_PROFILER = True  # Enables Python profiling
SILKY_MAX_RECORDED_REQUESTS = 1000  # Limit on the number of requests to store


# Elasticsearch settings
# settings.py

ELASTICSEARCH_DSL = {
    "default": {
        "hosts": "https://my-elasticsearch-project-e2edb7.es.us-east-1.aws.elastic.cloud:443",
        # 'http_auth': ('username', 'password'),  # If authentication is required
        "api_key": "SC14ZnNwUUI4c2ItUlFCdVJwQlg6VmxfSWtkNzBSYXF0MVdmMS0xUEZOUQ==",  # Use your actual API key
    }
}


# If you want to use a different cache backend, you can modify this settings accordingly.
