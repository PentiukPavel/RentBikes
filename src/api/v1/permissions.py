from rest_framework import permissions


class IsRenter(permissions.BasePermission):
    """
    Разрешение на просмотр и отмену аренды только к арендатора.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.renter == request.user
