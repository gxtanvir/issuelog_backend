from django.urls import path
from .views import NotificationListView, UnreadCountView, MarkReadView

urlpatterns = [
    path('notifications/', NotificationListView.as_view(), name='notifications-list'),
    path('notifications/unread-count/', UnreadCountView.as_view(), name='notifications-unread-count'),
    path('notifications/<int:pk>/mark-read/', MarkReadView.as_view(), name='notifications-mark-read'),
]
