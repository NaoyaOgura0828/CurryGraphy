import os
from PIL import Image

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.conf import settings

from post.models import Post


def user_directory_path(instance, filename):
	"""ユーザーディレクトリのパス"""
	"""ファイルは MEDIA_ROOT/user_<id>/<filename> へアップロードされる。"""
	profile_pic_name = 'user_{0}/profile.jpg'.format(instance.user.id)
	full_path = os.path.join(settings.MEDIA_ROOT, profile_pic_name)

	if os.path.exists(full_path):
		os.remove(full_path)

	return profile_pic_name


class Profile(models.Model):
	"""プロフィールモデル"""
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	first_name = models.CharField(max_length=50, null=True, blank=True)
	last_name = models.CharField(max_length=50, null=True, blank=True)
	location = models.CharField(max_length=50, null=True, blank=True)
	url = models.CharField(max_length=80, null=True, blank=True)
	profile_info = models.TextField(max_length=150, null=True, blank=True)
	created = models.DateField(auto_now_add=True)
	favorites = models.ManyToManyField(Post)
	picture = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Picture')

	def save(self, *args, **kwargs):
		"""プロフィールモデルの picture をリサイズする"""
		super().save(*args, **kwargs)
		size = 250, 250

		if self.picture:
			pic = Image.open(self.picture.path).convert('RGB')  # RGB形式に変換するコードを追記したが将来的に見直し予定
			pic.thumbnail(size, Image.LANCZOS)
			pic.save(self.picture.path)

	def __str__(self):
		return self.user.username
		

def create_user_profile(sender, instance, created, **kwargs):
	"""ユーザープロフィールモデルの作成"""
	if created:
		Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
	"""ユーザープロフィールモデルの保存"""
	instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
