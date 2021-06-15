"""core URL構成

'urlpatterns' リストはURLを views にルーティングします。詳細については、以下を参照してください。
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
例 :
Function views
    1. インポートを追加します :  from my_app import views
    2. urlpatterns にURLを追加します :  path('', views.home, name='home')
Class-based views
    1. インポートを追加します :  from other_app.views import Home
    2. urlpatterns にURLを追加します :  path('', Home.as_view(), name='home')
Including another URLconf
    1. include() 関数をインポートします : from django.urls import include, path
    2. urlpatterns にURLを追加します :  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from authy.views import user_profile, user_profile_favorites, follow

urlpatterns = [
    path('', include('post.urls')),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('user/', include('authy.urls')),
    path('direct/', include('direct.urls')),
    path('stories/', include('stories.urls')),
    path('notifications/', include('notifications.urls')),
    path('<username>/', user_profile, name='profile'),
    path('<username>/saved', user_profile, name='profilefavorites'),
    path('<username>/follow/<option>', follow, name='follow'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
