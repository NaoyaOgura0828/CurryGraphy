from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db import transaction
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from django.core.paginator import Paginator

from authy.models import Profile
from authy.forms import SignupForm, ChangePasswordForm, EditProfileForm
from post.models import Post, Follow, Stream


def user_profile(request, username):
	"""自分のプロフィールページの表示"""
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	url_name = resolve(request.path).url_name
	
	if url_name == 'profile':
		posts = Post.objects.filter(user=user).order_by('-posted')

	else:
		posts = profile.favorites.all()

	# プロフィール情報
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	# follow ステータス
	follow_status = Follow.objects.filter(following=user, follower=request.user).exists()

	# ページネーション
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile.html')

	context = {
		'posts': posts_paginator,
		'profile': profile,
		'following_count': following_count,
		'followers_count': followers_count,
		'posts_count': posts_count,
		'follow_status': follow_status,
		'url_name': url_name,
	}

	return HttpResponse(template.render(context, request))


def user_profile_favorites(request, username):
	"""他ユーザーのプロフィールページの表示"""
	user = get_object_or_404(User, username=username)
	profile = Profile.objects.get(user=user)
	
	posts = profile.favorites.all()

	# プロフィール情報
	posts_count = Post.objects.filter(user=user).count()
	following_count = Follow.objects.filter(follower=user).count()
	followers_count = Follow.objects.filter(following=user).count()

	# ページネーション
	paginator = Paginator(posts, 8)
	page_number = request.GET.get('page')
	posts_paginator = paginator.get_page(page_number)

	template = loader.get_template('profile_favorite.html')

	context = {
		'posts': posts_paginator,
		'profile': profile,
		'following_count': following_count,
		'followers_count': followers_count,
		'posts_count': posts_count,
	}

	return HttpResponse(template.render(context, request))


def signup(request):
	"""サインアップの表示"""
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			User.objects.create_user(username=username, email=email, password=password)
			return redirect('index')
	else:
		form = SignupForm()
	
	context = {
		'form': form,
	}

	return render(request, 'signup.html', context)


@login_required
def password_change(request):
	"""パスワード変更の表示"""
	user = request.user
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			new_password = form.cleaned_data.get('new_password')
			user.set_password(new_password)
			user.save()
			update_session_auth_hash(request, user)
			return redirect('change_password_done')
	else:
		form = ChangePasswordForm(instance=user)

	context = {
		'form': form,
	}

	return render(request, 'change_password.html', context)


def password_change_done(request):
	"""パスワード変更完了の表示"""
	return render(request, 'change_password_done.html')


@login_required
def edit_profile(request):
	"""プロフィール編集の表示"""
	user = request.user.id
	profile = Profile.objects.get(user__id=user)
	base_width = 400

	if request.method == 'POST':
		form = EditProfileForm(request.POST, request.FILES)
		if form.is_valid():
			profile.picture = form.cleaned_data.get('picture')
			profile.first_name = form.cleaned_data.get('first_name')
			profile.last_name = form.cleaned_data.get('last_name')
			profile.location = form.cleaned_data.get('location')
			profile.url = form.cleaned_data.get('url')
			profile.profile_info = form.cleaned_data.get('profile_info')
			profile.save()
			return redirect('timeline')
	else:
		form = EditProfileForm()

	context = {
		'form': form,
	}

	return render(request, 'edit_profile.html', context)


@login_required
def follow(request, username, option):
	"""フォローの表示"""
	following = get_object_or_404(User, username=username)

	try:
		f, created = Follow.objects.get_or_create(follower=request.user, following=following)

		if int(option) == 0:
			f.delete()
			Stream.objects.filter(following=following, user=request.user).all().delete()
		else:
			posts = Post.objects.all().filter(user=following)[:25]

			with transaction.atomic():
				for post in posts:
					stream = Stream(post=post, user=request.user, date=post.posted, following=following)
					stream.save()

		return HttpResponseRedirect(reverse('profile', args=[username]))

	except User.DoesNotExist:
		return HttpResponseRedirect(reverse('profile', args=[username]))
