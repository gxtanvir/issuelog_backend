from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    related_issue_id = serializers.IntegerField(source='related_issue.id', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'message', 'created_at', 'is_read', 'related_issue_id']
