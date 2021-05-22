"""
core projectのDjango設定。

Django3.0.7を使用して 'django-admin startproject' によって生成されます。

このファイルの詳細については、以下を参照してください。
https://docs.djangoproject.com/en/3.0/topics/settings/

設定とその値の完全なリストについては、以下を参照してください。
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
from pathlib import Path
import os

# 次のようにプロジェクト内にパスを作成します : BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - 本番環境には不適切
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# セキュリティ警告 : 本番環境で使用される秘密鍵は秘密にしてください。
SECRET_KEY = 'wkpwid&=r9wp2nl9jyr_%66zjgq4fku9*%g%^%-4iijga+t2lg'


# セキュリティ警告 : 本番環境でデバッグをオンにして実行しないでください。
DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    # Local apps
    'authy',
    'post',
    'comment',
    'direct',
    'notifications',
    'stories',

    # Third party apps


    # django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django_celery_beat',

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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notifications.views.count_notifications',
                'direct.views.check_directs',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DB_HOST は、完全なURLではなくサーバー名のみです。
hostname = os.environ.get('DB_HOST')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'] + '@' + hostname,
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = 'timeline'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = '/user/login/'


# Celery Broker
CELERY_BROKER_URL = 'amqp://localhost:5672'


# 本番環境用のセキュリティ設定
"""try:
    from .local_settings import *
except ImportError:
    pass

if not DEBUG:
    SECRET_KEY = os.environ['SECRET_KEY']"""
