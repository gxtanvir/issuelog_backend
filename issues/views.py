from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Issue
from .serializers import IssueSerializer
from .permissions import IsOwnerOrReadOnly
from django.db.models import Count, Q
from django.utils.timezone import now
from accounts.models import User  # ✅ use custom user from accounts app


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
        serializer.save(
            inserted_by=self.request.user,
            inserted_by_name=self.request.user.name
        )

    @action(detail=False, methods=["get"])
    def next_id(self, request):
        last = Issue.objects.order_by("-issue_id").first()
        next_id = (last.issue_id + 1) if last else 1
        return Response({"next_issue_id": next_id})

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAdminUser]
    )
    def summary(self, request):
        """
        Admin: Get monthly summary of issues per user
        Example: GET /api/issues/summary/
        """
        today = now().date()
        first_day = today.replace(day=1)

        summary = (
            Issue.objects.filter(created_at__gte=first_day)
            .values("inserted_by__user_id", "inserted_by__name")
            .annotate(
                pending=Count("issue_id", filter=Q(gms_status="Pending")),
                solved=Count("issue_id", filter=Q(gms_status="Completed")),
                total=Count("issue_id"),
            )
        )

        formatted = [
            {
                "user_id": item["inserted_by__user_id"],
                "user_name": item["inserted_by__name"] or "Unknown",
                "pending": item["pending"],
                "solved": item["solved"],
                "total": item["total"],
            }
            for item in summary
        ]

        return Response(formatted)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[permissions.IsAdminUser],
        url_path='user/(?P<user_id>[^/.]+)'
    )
    def issues_for_user(self, request, user_id=None):
        """
        Admin can fetch issues for a specific user by user_id (string key)
        Example: GET /api/issues/user/MIS-18/
        """
        try:
            user = User.objects.get(user_id=user_id)  # 👈 use user_id, not id
        except User.DoesNotExist:
            return Response({"detail": f"User '{user_id}' not found"}, status=404)

        issues = Issue.objects.filter(inserted_by=user).order_by("-created_at")
        serializer = self.get_serializer(issues, many=True)
        return Response(serializer.data)
