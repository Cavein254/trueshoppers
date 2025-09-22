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

INSTALLED_APPS = INSTALLED_APPS + ["authentication", "products"]  # noqa: F405


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "USER_ID_FIELD": "public_id",
    "USER_ID_CLAIM": "user_id",
}
