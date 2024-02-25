from rest_framework import permissions
from rest_framework.permissions import BasePermission


class OwnerAuthenticated(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.user


class PostOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if view.action in ['update_post', 'destroy', 'update_post_hashtag']:
            if request.user == obj.user:
                return True
            else:
                print("You do not have permission to delete this post.")
                return False



