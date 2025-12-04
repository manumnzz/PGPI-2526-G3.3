"""
Django settings for Natursur project.
"""

from pathlib import Path
import os
import dj_database_url # Necesario para PostgreSQL de Render
from dotenv import load_dotenv

# Cargar variables del archivo .env (útil en desarrollo)
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------------------------------------------
# 🔒 1. SEGURIDAD Y ENTORNO (AJUSTADO PARA PRODUCCIÓN EN RENDER)
# -------------------------------------------------------------------

# La clave secreta se lee de la variable de entorno de Render, con un fallback
SECRET_KEY = os.environ.get(
    "SECRET_KEY", 
    "django-insecure-h6pv@92%126#oa7l9grf9dpv7t(as$&b3+0a60felt99wt=*eo"
)

# DEBUG es False en Render (Producción) y True solo si se define la variable o en local.
DEBUG = os.environ.get("DEBUG") == "True"

# Hosts permitidos: lee la variable ALLOWED_HOSTS de Render y añade localhosts si DEBUG es True.
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
if DEBUG:
    ALLOWED_HOSTS += ["localhost", "127.0.0.1"]


# -------------------------------------------------------------------
# ⚙️ 2. DEFINICIÓN DE APLICACIONES Y MIDDLEWARE
# -------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware", # <--- AÑADIDO para archivos estáticos en Render
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "Natursur.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Natursur.wsgi.application"


# -------------------------------------------------------------------
# 💾 3. BASE DE DATOS (AJUSTADO PARA POSTGRESQL DE RENDER)
# -------------------------------------------------------------------

# Si existe la variable DATABASE_URL (proporcionada por Render), usa PostgreSQL.
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600  
        )
    }
# Si no existe (Desarrollo local), usa SQLite.
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# ------------------------------
# 📁 4. ARCHIVOS ESTÁTICOS Y MEDIA (AJUSTADO PARA WHITE NOISE)
# ------------------------------

# Ruta base para los estáticos
STATIC_URL = "static/"
# Directorio donde collectstatic pondrá los archivos estáticos en Render
STATIC_ROOT = BASE_DIR / "staticfiles" 


# Archivos Media (Imágenes subidas)
MEDIA_URL = "/images/"
MEDIA_ROOT = BASE_DIR / "images" # Advertencia: Los archivos guardados aquí en Render no son permanentes.


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ----------------------------------
# GROQ API (IA del asistente)
# ----------------------------------
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")