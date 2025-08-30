from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Allow read to authenticated users; write (PUT/PATCH/DELETE) only if the object's inserted_by == request.user.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for safe methods for authenticated users (your viewset uses IsAuthenticated).
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions only to owner
        return obj.inserted_by == request.user
