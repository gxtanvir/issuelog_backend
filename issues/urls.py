from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueViewSet

router = DefaultRouter()
router.register(r'issues', IssueViewSet, basename='issues')

urlpatterns = [
    path('', include(router.urls)),
]
