import os
from datetime import timedelta
from pathlib import Path

import environ

from .base import *  # noqa: F403,F401

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialise environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env.dev"))

DEBUG = True

SECRET_KEY = "django-insecure-)_@g-pqhg&^95arw(^a7&9=t+3x=!#x(d2o8duyfpj*(qu!yj1"


ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = INSTALLED_APPS + [  # noqa: F405
    "authentication",
    "products",
    "shop",
    "django_extensions",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="dev_db"),
        "USER": env("DB_USER", default="devuser"),
        "PASSWORD": env("DB_PASSWORD", default="devpass"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT", default="5433"),
    }
}

REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # noqa: F405
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.122.200",
    "http://192.168.122.200:30080",
    "https://yourdomain.com",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Vite default
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "public_id",
    "USER_ID_CLAIM": "user_id",
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # service name = redis
    }
}

CELERY_BROKER_URL = "amqp://user:pass@rabbitmq:5672//"
CELERY_RESULT_BACKEND = "rpc://"
