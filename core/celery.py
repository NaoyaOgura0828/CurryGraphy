import os

from celery import Celery

# 'celery' プログラムのデフォルトのDjango設定モジュールを設定します。
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# ここで文字列を使用することは、ワーカーがシリアル化する必要がないことを意味します
# 子プロセスに対する構成オブジェクト
# namespace='CELERY' は、すべてのCelery関連の構成キーを意味します
#   should have a `CELERY_` prefix.
# 接頭語として `CELERY_` が必要です。
app.config_from_object('django.conf:settings', namespace='CELERY')

# 登録されているすべてのDjangoアプリ構成からタスクモジュールをロードします。
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
