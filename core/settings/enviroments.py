from pathlib import Path
from typing import List


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-a!0i7yw43(c0#od!x9(p^3n+$qornbv5s(hinr6cqvg0haz%zl" # noqa

DEBUG = True

ALLOWED_HOSTS: List[str] = []

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# Phone number app configurations
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = None
PHONENUMBER_DEFAULT_FORMAT = "E164"
