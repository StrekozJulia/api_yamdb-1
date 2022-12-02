from rest_framework import permissions
from reviews.models import User


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка: является ли пользователь администратором."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            current_user = User.objects.get(username=request.user.username)
            if current_user.role == 'admin' or request.user.is_superuser:
                return True
        return request.method in permissions.SAFE_METHODS


class IsAuthorIsAdminIsModeratorOrReadOnly(permissions.BasePermission):
    """
    Проверяем является ли пользователь автором,
    модератором или администратором. Для отзывов, комментариев.
    """

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or request.user.is_superuser)
