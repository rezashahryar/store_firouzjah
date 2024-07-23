from rest_framework import permissions

# create your permissions here


class ProductCommetPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user)
