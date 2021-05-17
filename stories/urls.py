from django.urls import path

from stories.views import new_story, show_media

urlpatterns = [
	path('newstory/', new_story, name='newstory'),
	path('showmedia/<stream_id>', show_media, name='showmedia'),
]
