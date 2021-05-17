from django.urls import path

from direct.views import inbox, user_search, directs_message, new_conversation, send_direct


urlpatterns = [
	path('inbox', inbox, name='inbox'),
	path('directs/<username>', directs_message, name='directs'),
	path('new/', user_search, name='usersearch'),
	path('new/<username>', new_conversation, name='newconversation'),
	path('send/', send_direct, name='send_direct'),
]
