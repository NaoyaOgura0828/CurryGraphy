from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.urls import reverse

from post.models import Stream, Post, Tag, Likes, PostFileContent
from post.forms import NewPostForm
from stories.models import StoryStream
from comment.models import Comment
from comment.forms import CommentForm
from authy.models import Profile


class IndexView(generic.TemplateView):
	template_name = "index.html"


@login_required
def timeline(request):
	"""タイムラインの表示"""
	user = request.user
	posts = Stream.objects.filter(user=user)

	stories = StoryStream.objects.filter(user=user)

	group_ids = []

	for post in posts:
		group_ids.append(post.post_id)

	post_items = Post.objects.filter(id__in=group_ids).all().order_by('-posted')

	template = loader.get_template('timeline.html')

	context = {
		'post_items': post_items,
		'stories': stories,

	}

	return HttpResponse(template.render(context, request))


def post_details(request, post_id):
	"""投稿の表示"""
	post = get_object_or_404(Post, id=post_id)
	user = request.user
	profile = Profile.objects.get(user=user)
	favorited = False

	# コメント
	comments = Comment.objects.filter(post=post).order_by('date')
	
	if request.user.is_authenticated:
		profile = Profile.objects.get(user=user)
		# For the color of the favorite button

		if profile.favorites.filter(id=post_id).exists():
			favorited = True

	# コメントフォーム
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.user = user
			comment.save()
			return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
	else:
		form = CommentForm()

	template = loader.get_template('post_detail.html')

	context = {
		'post': post,
		'favorited': favorited,
		'profile': profile,
		'form': form,
		'comments': comments,
	}

	return HttpResponse(template.render(context, request))


@login_required
def new_post(request):
	"""新規投稿の表示"""
	user = request.user
	tags_objs = []
	files_objs = []

	if request.method == 'POST':
		form = NewPostForm(request.POST, request.FILES)
		if form.is_valid():
			files = request.FILES.getlist('content')
			caption = form.cleaned_data.get('caption')
			tags_form = form.cleaned_data.get('tags')

			tags_list = list(tags_form.split(','))

			for tag in tags_list:
				t, created = Tag.objects.get_or_create(title=tag)
				tags_objs.append(t)

			for file in files:
				file_instance = PostFileContent(file=file, user=user)
				file_instance.save()
				files_objs.append(file_instance)

			p, created = Post.objects.get_or_create(caption=caption, user=user)
			p.tags.set(tags_objs)
			p.content.set(files_objs)
			p.save()
			return redirect('timeline')
	else:
		form = NewPostForm()

	context = {
		'form': form,
	}

	return render(request, 'newpost.html', context)


def tags_define(request, tag_slug):
	"""タグの表示"""
	tag = get_object_or_404(Tag, slug=tag_slug)
	posts = Post.objects.filter(tags=tag).order_by('-posted')

	template = loader.get_template('tag.html')

	context = {
		'posts': posts,
		'tag': tag,
	}

	return HttpResponse(template.render(context, request))


@login_required
def like_define(request, post_id):
	"""いいね！の表示"""
	user = request.user
	post = Post.objects.get(id=post_id)
	current_likes = post.likes
	liked = Likes.objects.filter(user=user, post=post).count()

	if not liked:
		Likes.objects.create(user=user, post=post)
		current_likes = current_likes + 1

	else:
		Likes.objects.filter(user=user, post=post).delete()
		current_likes = current_likes - 1

	post.likes = current_likes
	post.save()

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))


@login_required
def favorite_define(request, post_id):
	"""お気に入りの表示"""
	user = request.user
	post = Post.objects.get(id=post_id)
	profile = Profile.objects.get(user=user)

	if profile.favorites.filter(id=post_id).exists():
		profile.favorites.remove(post)

	else:
		profile.favorites.add(post)

	return HttpResponseRedirect(reverse('postdetails', args=[post_id]))
