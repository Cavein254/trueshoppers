import os
from pathlib import Path

import dj_database_url
import environ

from .base import *  # noqa: F403,F401

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env"))

DEBUG = False
ALLOWED_HOSTS = [""]

DATABASES = {
    "default": dj_database_url.config(
        default=env(
            "DATABASE_URL",
        ),
        conn_max_age=600,
        ssl_require=env.bool("DB_SSL_REQUIRED", default=False),
    )
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # service name = redis
    }
}

CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL", default="amqp://guest:guest@rabbitmq:5672//"
)
CELERY_RESULT_BACKEND = "rpc://"
