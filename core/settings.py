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


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - 本番環境には不適切
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# セキュリティ警告 : 本番環境で使用される秘密鍵は秘密にしてください。
SECRET_KEY = os.environ['SECRET_KEY']


# セキュリティ警告 : 本番環境でデバッグをオンにして実行しないでください。
DEBUG = True

ALLOWED_HOSTS = [os.environ['ALLOWED_HOSTS']]


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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
        'DIRS': [BASE_DIR / 'templates'],
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


# データベース
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DB_HOST は、完全なURLではなくサーバー名のみです。
hostname = os.environ['DB_HOST']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'] + "@" + hostname,
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': hostname + '.postgres.database.azure.com',
    }
}


# パスワードの検証
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


# 国際化
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

LOGIN_REDIRECT_URL = 'timeline'
LOGOUT_REDIRECT_URL = 'index'
LOGIN_URL = '/user/login/'


# Celery Broker
CELERY_BROKER_URL = 'amqp://localhost:5672'
