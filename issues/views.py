from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Issue
from accounts.models import User
from .serializers import IssueSerializer


class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_context(self):
        # Pass request to serializer so we can access request.user
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    # optional: quick endpoint to get next issue id (preview only)
    @action(detail=False, methods=["get"])
    def next_id(self, request):
        last = Issue.objects.order_by("-issue_id").first()
        next_id = (last.issue_id + 1) if last else 1
        return Response({"next_issue_id": next_id})
