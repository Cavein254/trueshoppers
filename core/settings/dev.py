import os
from pathlib import Path

import environ

from .base import *  # noqa: F403,F401

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialise environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env.dev"))

DEBUG = True

ALLOWED_HOSTS = ["*"]

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


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # service name = redis
    }
}

CELERY_BROKER_URL = "amqp://user:pass@rabbitmq:5672//"
CELERY_RESULT_BACKEND = "rpc://"
