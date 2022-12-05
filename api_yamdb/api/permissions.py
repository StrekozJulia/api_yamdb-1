from rest_framework import permissions


class AdminOrReadOnly(permissions.BasePermission):
    """Проверка: является ли пользователь администратором."""
    message = 'Данное действие доступно только администратору.'

    def has_permission(self, request, view):

        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin)


class IsAuthorIsAdminIsModeratorOrReadOnly(permissions.BasePermission):
    """
    Проверяем является ли пользователь автором,
    модератором или администратором. Для отзывов, комментариев.
    """

    message = 'У вас недостаточно прав для выполнения данного действия.'

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator)


class IsAdmin(permissions.BasePermission):

    message = 'Доступно только администратору.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)
