from .settings import *
import os


# 環境変数を使用してドメイン名を設定します
# そのAzureは自動的に私たちのために作成されます。
ALLOWED_HOSTS = [os.environ['WEBSITE_HOSTNAME']] if 'WEBSITE_HOSTNAME' in os.environ else []


# WhiteNoise の設定
MIDDLEWARE = [                                                                   
    'django.middleware.security.SecurityMiddleware',
    # セキュリティミドルウェアの後にホワイトエイジーミドルウェアを追加します
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',                      
    'django.middleware.common.CommonMiddleware',                                 
    'django.middleware.csrf.CsrfViewMiddleware',                                 
    'django.contrib.auth.middleware.AuthenticationMiddleware',                   
    'django.contrib.messages.middleware.MessageMiddleware',                      
    'django.middleware.clickjacking.XFrameOptionsMiddleware',                    
]





# DB_HOST は、完全なURLではなくサーバー名のみです。
hostname = os.environ['DB_HOST']


# Postgres database を設定します。 フルユーザー名は username@servername です。
# DB_HOST 値を使用して構築します。
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DB_NAME'],
        'HOST': hostname + ".postgres.database.azure.com",
        'USER': os.environ['DB_USER'] + "@" + hostname,
        'PASSWORD': os.environ['DB_PASSWORD']
    }
}
