from rest_framework import permissions
from reviews.models import User


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка: является ли пользователь администратором."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user.username)
            if current_user.role == 'admin':
                return True
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user.username)
            if current_user.role == 'admin':
                return True
        return request.method in permissions.SAFE_METHODS
