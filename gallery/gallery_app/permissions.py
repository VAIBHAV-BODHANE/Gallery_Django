from rest_framework.permissions import BasePermission, SAFE_METHODS


class OwnObjectPermission(BasePermission):
    """Object level permission to allow updateing and delteing own data"""

    allowed_methods = ('POST')

    message = "Not Authorized!"

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS or request.method in self.allowed_methods:
            return True
        return obj.user == request.user
