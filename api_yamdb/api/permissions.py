from rest_framework import permissions


class IsAdmin(permissions.BasePermission):

    message = 'Доступно только администратору.'

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin')
