"""scouts_wwdb_api.settings.

Django settings for scouts_wwdb_api project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import logging
import logging.config
import os

from environs import Env

# Get a pre-config logger
logger = logging.getLogger(__name__)

env = Env()
env.read_env()

LOGGING_CONFIG = None
LOGGING_LEVEL = env.str("LOGGING_LEVEL", "INFO")
LOGGING_LEVEL_ROOT = env.str("LOGGING_LEVEL_ROOT", "ERROR")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(asctime)s - %(levelname)-7s - %(name)-12s - %(message)s",
        },
        "simple": {
            "format": "%(levelname)-8s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOGGING_LEVEL,
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOGGING_LEVEL_ROOT,
    },
    "loggers": {
        "apps": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
        "xhtml2pdf": {
            "handlers": ["console"],
            "level": LOGGING_LEVEL,
            "propagate": False,
        },
    },
}
logging.config.dictConfig(LOGGING)

logging.info("LOGGING_LEVEL: %s", LOGGING_LEVEL)
logging.info("LOGGING_LEVEL_ROOT: %s", LOGGING_LEVEL_ROOT)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
BASE_URL = env.str("BASE_URL")

APPEND_SLASH = True


# Application definition
INSTALLED_APPS = [  # order alphabetically
    "apps.files",
    "apps.scouts_auth",
    "apps.workshops",
    "apps.wwdb_exports",
    "apps.wwdb_mails",
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_filters",
    "drf_yasg",
    "mozilla_django_oidc",
    "rest_framework",
    "storages",
    # "django_extensions",
]

if DEBUG:
    INSTALLED_APPS.append("django_extensions")

MIDDLEWARE = [  # actual ordering matters for middleware
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "scouts_wwdb_api.urls"

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

WSGI_APPLICATION = "scouts_wwdb_api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("DBNAME"),
        "USER": env.str("DBUSER"),
        "PASSWORD": env.str("DBPASSWORD"),
        "HOST": env.str("DBHOST"),
        "PORT": env.str("DBPORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Brussels"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_DIRS = [
    env.str("STATICFILES_EXPORT_WWDB"),
]

STATIC_URL = "static/"
STATIC_ROOT = env.str("STATIC_ROOT")

# Rest framework

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "apps.oidc.auth.InuitsOIDCAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "scouts_wwdb_api.pagination.ScoutsPageNumberPagination",
}

# Email
email = env.dj_email_url("EMAIL_URL")
EMAIL_HOST = email["EMAIL_HOST"]
EMAIL_PORT = email["EMAIL_PORT"]
EMAIL_HOST_PASSWORD = email["EMAIL_HOST_PASSWORD"]
EMAIL_HOST_USER = email["EMAIL_HOST_USER"]
EMAIL_USE_TLS = email["EMAIL_USE_TLS"]

DEFAULT_FROM_EMAIL = env.str("EMAIL_SENDER")
DEFAULT_EMAIL_RECIPIENTS = env.list("EMAIL_RECIPIENTS")


# CORS
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")

# OIDC
AUTH_USER_MODEL = "scouts_auth.User"

AUTHENTICATION_BACKENDS = {
    "apps.oidc.auth.InuitsOIDCAuthenticationBackend",
}
OIDC_DRF_AUTH_BACKEND = "apps.oidc.auth.InuitsOIDCAuthenticationBackend"
OIDC_RP_SIGN_ALGO = "RS256"

OIDC_OP_JWKS_ENDPOINT = env.str("OIDC_OP_JWKS_ENDPOINT")
OIDC_OP_AUTHORIZATION_ENDPOINT = env.str("OIDC_OP_AUTHORIZATION_ENDPOINT")
OIDC_OP_TOKEN_ENDPOINT = env.str("OIDC_OP_TOKEN_ENDPOINT")
OIDC_OP_USER_ENDPOINT = env.str("OIDC_OP_USER_ENDPOINT")

OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")

# Storages/S3

DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_ACCESS_KEY_ID = env.str("S3_ACCESS_KEY")
AWS_SECRET_ACCESS_KEY = env.str("S3_ACCESS_SECRET")
AWS_STORAGE_BUCKET_NAME = env.str("S3_STORAGE_BUCKET_NAME")
AWS_S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL")
# AWS_DEFAULT_ACL = "public-read"
AWS_DEFAULT_ACL = None
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SIGNATURE_VERSION = "s3v4"
