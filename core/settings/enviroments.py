from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY","Insecure")

DEBUG = 1 if int(os.environ.get("DEBUG","1")) == 1 else 0

ALLOWED_HOSTS = []

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# Phone number app configurations
PHONENUMBER_DB_FORMAT = "E164"
PHONENUMBER_DEFAULT_REGION = None
PHONENUMBER_DEFAULT_FORMAT = "E164"
