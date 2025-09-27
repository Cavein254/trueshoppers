import os
from datetime import timedelta
from pathlib import Path

import environ

from .base import *  # noqa: F403,F401

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialise environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env.test"))
DEBUG = True

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = INSTALLED_APPS + ["authentication", "products", "shop"]  # noqa: F405

# Store uploaded files in a temporary directory during tests
MEDIA_ROOT = os.path.join(BASE_DIR, "tmp_test_media")

# Ensure directory exists
os.makedirs(MEDIA_ROOT, exist_ok=True)


# Use in-memory database for tests for data isolation
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Use in-memory cache instead of Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "test-cache",
    }
}

# Disable password validators for faster tests
AUTH_PASSWORD_VALIDATORS = []


# Faster password hashing (so tests run quickly)
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


# Don’t use Celery + Redis in tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Email backend — doesn’t actually send emails
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "public_id",
    "USER_ID_CLAIM": "user_id",
}
