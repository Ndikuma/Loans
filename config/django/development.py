from config.env import env

from .base import *  # noqa: F401

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env(
    "SECRET_KEY",
    default="django-insecure-2*ijp440(trkyh-d=ndn7+jfrmj@-zd^hl$(y&jw#o7l$%o68=",
)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=True)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["*"])

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "loans.sqlite3",
    }
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "testcomlab24@gmail.com"
EMAIL_HOST_PASSWORD = "nyhbfgzcvhsadrpp"
