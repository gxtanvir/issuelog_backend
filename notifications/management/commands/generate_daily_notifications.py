# notifications/management/commands/generate_daily_notifications.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from accounts.models import User
from issues.models import Issue
from notifications.models import Notification
from datetime import timedelta

class Command(BaseCommand):
    help = "Generate daily pending issue notifications for users"

    def handle(self, *args, **options):
        today = timezone.now().date()
        # You can tweak filter (e.g., for month)
        users = User.objects.filter(is_active=True)
        created = 0
        for user in users:
            pending_count = Issue.objects.filter(inserted_by=user, gms_status="Pending").count()
            if pending_count > 0:
                msg = f"You have {pending_count} pending issue(s) as of {today}."
                Notification.objects.create(user=user, message=msg)
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Notifications created: {created}"))
