"""
core プロジェクトのASGI構成。

ASGI呼び出し可能オブジェクトを 'application' という名前のモジュールレベルの変数として公開します。
このファイルの詳細については、URLを参照してください。
https://docs.djangoproject.com/en/3.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_asgi_application()
