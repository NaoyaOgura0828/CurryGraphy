from celery import shared_task
from datetime import datetime, timedelta

from stories.models import Story, StoryStream


@shared_task
def check_stories_date():
	"""ストーリーの日付を確認するタスク"""
	exp_date = datetime.now() - timedelta(hours=1)
	old_stories = Story.objects.filter(posted__lt=exp_date)
	old_stories.update(expired=True)
	print("Stories updated")


@shared_task
def delete_expired():
	"""check_stories_dateタスクによって期限切れとしてマークされたストーリーを削除するタスク"""
	Story.objects.filter(expired=True).delete()
	StoryStream.objects.filter(story=None).delete()
