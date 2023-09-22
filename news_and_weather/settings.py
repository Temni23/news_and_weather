import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'key_for_default')

DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split()

AUTH_USER_MODEL = 'users.User'

INSTALLED_APPS = [
    'users.apps.UsersConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'djoser',
    'drf_yasg',
    'django_summernote',
    'rest_framework.authtoken',
    'news.apps.NewsConfig',
    'places.apps.PlacesConfig',
    'django_celery_results',
    'django_celery_beat',
    'constance',
    'constance.backends.database',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'news_and_weather.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['venv/lib/python3.9/'
                 'site-packages/django_admin_geomap/templates']
        ,
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

WSGI_APPLICATION = 'news_and_weather.wsgi.application'

POSTGRES_SETTINGS = {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': os.getenv('POSTGRES_DB', 'django'),
    'USER': os.getenv('POSTGRES_USER', 'django'),
    'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
    'HOST': os.getenv('DB_HOST', ''),
    'PORT': os.getenv('DB_PORT', 5432)
}

SQLITE_SETTINGS = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': BASE_DIR / 'data_base/db.sqlite3',
}

DATABASES = {
    'default':
        (POSTGRES_SETTINGS, SQLITE_SETTINGS)[os.getenv('DATABASE') == 'sqlite']
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Krasnoyarsk'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#############################################################################
#                            DRF settings
#############################################################################

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 'SEARCH_PARAM': 'name'
    # Используем по умолчанию в запросе name вместо search
}

#############################################################################
#                            Djoser settings
#############################################################################

DJOSER = {
    'LOGIN_FIELD': 'email',
    'LOGOUT_ON_PASSWORD_CHANGE': True,
    'SERIALIZERS': {
        'user_create': 'api.serializers.UserCreateSerializer',
        'current_user': 'api.serializers.UserSerializer',
        'user': 'api.serializers.UserSerializer'}
}
#############################################################################
#                            Summernote settings
#############################################################################

SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'width': '100%',
        'height': '400px',
    },
}

#############################################################################
#                            Celery settings
#############################################################################

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_ACCEPT_CONTENT = ['json']
# CELERY_TASK_SERIALIZER = 'json'
# CELERY_RESULT_SERIALIZER = 'json'
#############################################################################
#                            Models constants
#############################################################################

STR_SYMBOLS_AMOUNT = 30
MAX_LENGTH_EMAIL = 254
MAX_LENGTH_USERNAME = 150
MAX_LENGTH_FIRST_NAME = 150
MAX_LENGTH_LAST_NAME = 150
MIN_RATING = 0
MAX_RATING = 25
