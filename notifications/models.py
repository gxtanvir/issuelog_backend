from django.db import models
from django.conf import settings

class Notification(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    # optional link to an Issue (nullable)
    related_issue = models.ForeignKey(
        'issues.Issue',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='notifications'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification({self.user}, read={self.is_read})"
