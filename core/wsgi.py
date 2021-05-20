"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application


# WEBSITE_HOSTNAME が環境変数として定義されている場合は、実行中です。
# AzureAppService では、 production.py の生産設定を使用する必要があります。
settings_module = "core.production" if 'WEBSITE_HOSTNAME' in os.environ else 'core.settings'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

sys.path.append('/home/NaoyaOgura/CurryGraphy')

application = get_wsgi_application()
