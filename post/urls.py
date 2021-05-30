from django.urls import path

from post.views import IndexView, timeline, new_post, post_details, tags_define, like_define, favorite_define


urlpatterns = [
	path('/', IndexView.as_view(), name="index"),
	path('timeline/', timeline, name='timeline'),
	path('newpost/', new_post, name='newpost'),
	path('<uuid:post_id>', post_details, name='postdetails'),
	path('<uuid:post_id>/like', like_define, name='postlike'),
	path('<uuid:post_id>/favorite', favorite_define, name='postfavorite'),
	path('tag/<slug:tag_slug>', tags_define, name='tags'),
]
