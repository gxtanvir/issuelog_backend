from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Issue
from .serializers import IssueSerializer
from .permissions import IsOwnerOrReadOnly

class IssueViewSet(viewsets.ModelViewSet):
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        # Only show issues inserted by the current logged-in user
        return Issue.objects.filter(inserted_by=self.request.user).order_by("-created_at")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        # Ensure inserted_by and inserted_by_name are saved from request.user
        serializer.save(inserted_by=self.request.user, inserted_by_name=self.request.user.name)

    @action(detail=False, methods=["get"])
    def next_id(self, request):
        last = Issue.objects.order_by("-issue_id").first()
        next_id = (last.issue_id + 1) if last else 1
        return Response({"next_issue_id": next_id})
