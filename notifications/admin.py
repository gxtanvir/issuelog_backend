from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_read', 'created_at', 'related_issue')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__user_id', 'user__name', 'message')
