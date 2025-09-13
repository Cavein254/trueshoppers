from .base import *
DEBUG = False
ALLOWED_HOSTS = ["yourdomain.com"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "prod_db",
        "USER": "produser",
        "PASSWORD": "prodpass",
        "HOST": "localhost",
        "PORT": "5435",
    }
}



CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/1",  # service name = redis
    }
}

CELERY_BROKER_URL = 'amqp://user:pass@rabbitmq:5672//'
CELERY_RESULT_BACKEND = "rpc://"