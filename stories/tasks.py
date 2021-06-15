from celery import shared_task
from datetime import datetime, timedelta

from stories.models import Story, StoryStream


# ストーリーの日付を確認するタスク
@shared_task
def check_stories_date():
	exp_date = datetime.now() - timedelta(hours=1)
	old_stories = Story.objects.filter(posted__lt=exp_date)
	old_stories.update(expired=True)
	print("Stories updated")


# check_stories_dateタスクによって期限切れとしてマークされたストーリーを削除するタスク
@shared_task
def delete_expired():
	Story.objects.filter(expired=True).delete()
	StoryStream.objects.filter(story=None).delete()
