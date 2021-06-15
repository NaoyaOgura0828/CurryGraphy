"""
core プロジェクトのWSGI構成.

WSGI呼び出し可能オブジェクトを 'application' という名前のモジュールレベルの変数として公開します。
このファイルの詳細については、URLを参照してください。
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
