#!/usr/bin/env python
"""管理タスクのためのDjangoのコマンドラインユーティリティ"""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Djangoをインポートできませんでした。インストールされていますか？"
            "PYTHONPATH環境変数が利用できますか？"
            "仮想環境をアクティブ化するのを忘れましたか？"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
