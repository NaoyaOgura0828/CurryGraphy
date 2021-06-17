from django.shortcuts import render, redirect
from django.template import loader, RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from django.views.generic import TemplateView

from direct.models import Message


@login_required
def inbox(request):
	"""メッセージBOXの表示"""
	messages = Message.get_messages(user=request.user)
	active_direct = None
	directs = None

	if messages:
		message = messages[0]
		active_direct = message['user'].username
		directs = Message.objects.filter(user=request.user, recipient=message['user'])
		directs.update(is_read=True)
		for message in messages:
			if message['user'].username == active_direct:
				message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
		}

	template = loader.get_template('direct/direct.html')

	return HttpResponse(template.render(context, request))


@login_required
def user_search(request):
	"""ユーザー検索の表示"""
	query = request.GET.get("q")
	context = {}
	
	if query:
		users = User.objects.filter(Q(username__icontains=query))

		# Pagination
		paginator = Paginator(users, 6)
		page_number = request.GET.get('page')
		users_paginator = paginator.get_page(page_number)

		context = {
				'users': users_paginator,
			}
	
	template = loader.get_template('direct/search_user.html')
	
	return HttpResponse(template.render(context, request))


@login_required
def directs_message(request, username):
	"""メッセージウィンドウの表示"""
	user = request.user
	messages = Message.get_messages(user=user)
	active_direct = username
	directs = Message.objects.filter(user=user, recipient__username=username)
	directs.update(is_read=True)
	for message in messages:
		if message['user'].username == username:
			message['unread'] = 0

	context = {
		'directs': directs,
		'messages': messages,
		'active_direct': active_direct,
	}

	template = loader.get_template('direct/direct.html')

	return HttpResponse(template.render(context, request))


@login_required
def new_conversation(request, username):
	"""新規メッセージの表示"""
	from_user = request.user
	body = ''
	try:
		to_user = User.objects.get(username=username)
	except Exception as e:
		return redirect('usersearch')
	if from_user != to_user:
		Message.send_message(from_user, to_user, body)
	return redirect('inbox')


@login_required
def send_direct(request):
	"""送信メッセージの表示"""
	from_user = request.user
	to_user_username = request.POST.get('to_user')
	body = request.POST.get('body')
	
	if request.method == 'POST':
		to_user = User.objects.get(username=to_user_username)
		Message.send_message(from_user, to_user, body)
		return redirect('inbox')
	else:
		HttpResponseBadRequest()


def check_directs(request):
	"""受信メッセージの表示"""
	directs_count = 0
	if request.user.is_authenticated:
		directs_count = Message.objects.filter(user=request.user, is_read=False).count()

	return {'directs_count': directs_count}
