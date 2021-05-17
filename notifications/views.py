from django.shortcuts import redirect
from django.template import loader
from django.http import HttpResponse

from notifications.models import Notification


def show_notifications(request):
	user = request.user
	notifications = Notification.objects.filter(user=user).order_by('-date')
	Notification.objects.filter(user=user, is_seen=False).update(is_seen=True)

	template = loader.get_template('notifications.html')

	context = {
		'notifications': notifications,
	}

	return HttpResponse(template.render(context, request))


def delete_notification(request, noti_id):
	user = request.user
	Notification.objects.filter(id=noti_id, user=user).delete()
	return redirect('show-notifications')


def count_notifications(request):
	countnotifications = 0
	if request.user.is_authenticated:
		countnotifications = Notification.objects.filter(user=request.user, is_seen=False).count()

	return {'count_notifications': countnotifications}
