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
            "Djangoをインポートできませんでした。インストールされているか確認してください。"
            "環境変数「PYTHONPATH」に登録されていますか？"
            "仮想環境のアクティベーションを忘れていませんか？"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
