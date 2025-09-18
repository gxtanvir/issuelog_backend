# issues/tasks.py
from django.utils import timezone
from celery import shared_task
from .models import Issue, Notification
from django.contrib.auth.models import User

@shared_task
def send_daily_notifications():
    now = timezone.now()
    if now.hour == 10:  # Run daily at 10 AM
        for user in User.objects.all():
            pending_count = Issue.objects.filter(responsible=user, status="Pending").count()
            if pending_count > 0:
                Notification.objects.create(
                    user=user,
                    message=f"You have {pending_count} pending issues.",
                )
