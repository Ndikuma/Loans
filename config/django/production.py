import dj_database_url

from config.env import env

from .base import *  # noqa: F401

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
DATABASES = {
    "default": dj_database_url.parse(
        "postgresql://comlabuser:LuvPJAgmzVQQAGwl4mKCoNKegGje3RRa@dpg-ctum13q3esus739e4rh0-a.oregon-postgres.render.com/comlabdb"
    )
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "testcomlab24@gmail.com"
EMAIL_HOST_PASSWORD = "nyhbfgzcvhsadrpp"
