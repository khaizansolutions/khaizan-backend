"""
Django settings for config project.
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-b)%c!k0d4w902hwi_k0rdy-2ns-kad88&3dse9y3hmxkp8mfh&')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third party
    'rest_framework',
    'corsheaders',
    'django_filters',
    'cloudinary_storage',  # Must be before 'cloudinary'
    'cloudinary',

    # Local apps
    'products',
    'quotes',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'neondb',
        'USER': 'neondb_owner',
        'PASSWORD': 'npg_9Mbgd0vixpta',
        'HOST': 'ep-falling-river-a1s9mv5j-pooler.ap-southeast-1.aws.neon.tech',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dubai'
USE_I18N = True
USE_TZ = True

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    "https://khaizen-frontend.vercel.app",
    "https://www.khaizansolution.com",
    "https://khaizansolution.com",
    "http://localhost:3001",
    "http://localhost:3000",
]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 15,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Cloudinary Configuration for Media Files
import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dfou5jsq4',
    'API_KEY': '676198389127474',
    'API_SECRET': '2Qr8hrT7z6zPPeWtqqOIPWIF0UU',
}

cloudinary.config(
    cloud_name='dfou5jsq4',
    api_key='676198389127474',
    api_secret='2Qr8hrT7z6zPPeWtqqOIPWIF0UU',
    secure=True
)

# Use Cloudinary for media file storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Media URL (Cloudinary will provide actual URLs like https://res.cloudinary.com/...)
MEDIA_URL = '/media/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'