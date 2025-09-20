import os
from pathlib import Path

import environ

from .base import *  # noqa: F403,F401

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Initialise environment variables
env = environ.Env()
env.read_env(os.path.join(BASE_DIR, ".env.test"))
DEBUG = True

ALLOWED_HOSTS = ["*"]

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
