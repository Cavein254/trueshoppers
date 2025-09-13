from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "test_db",
        "USER": "testuser",
        "PASSWORD": "testpass",
        "HOST": "localhost",
        "PORT": "5434",
    }
}
