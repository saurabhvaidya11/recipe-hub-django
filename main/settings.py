from pathlib import Path
import os
import cloudinary
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# SECURITY
# ==============================

SECRET_KEY = os.environ.get("SECRET_KEY")

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set!")

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".onrender.com"]


# ==============================
# INSTALLED APPS
# ==============================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'vege',

    # Cloudinary
    'cloudinary',
    'cloudinary_storage',
]


# ==============================
# MIDDLEWARE
# ==============================

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ==============================
# URLS & TEMPLATES
# ==============================

ROOT_URLCONF = 'main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main.wsgi.application'


# ==============================
# DATABASE (Render PostgreSQL)
# ==============================

DATABASES = {
    'default': dj_database_url.parse(os.environ.get("DATABASE_URL"))
}


# ==============================
# PASSWORD VALIDATION
# ==============================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================
# INTERNATIONALIZATION
# ==============================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================
# STATIC FILES (WhiteNoise)
# ==============================

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# ==============================
# STORAGE (Django 4.2+ CORRECT WAY)
# ==============================

STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ==============================
# DEFAULT FIELD
# ==============================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================
# LOGIN
# ==============================

LOGIN_URL = 'login_page'


# ==============================
# CLOUDINARY CONFIG
# ==============================

cloudinary.config(
    cloud_name=os.environ.get("CLOUDINARY_CLOUD_NAME"),
    api_key=os.environ.get("CLOUDINARY_API_KEY"),
    api_secret=os.environ.get("CLOUDINARY_API_SECRET"),
)


# ==============================
# RENDER HTTPS FIX (important)
# ==============================

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True