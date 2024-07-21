from rest_framework.permissions import BasePermission

class IsWebMailPermission(BasePermission):
    def has_permission(self, request, view):
        return True