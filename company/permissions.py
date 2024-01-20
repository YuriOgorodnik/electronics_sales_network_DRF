from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    """
    Пользовательское разрешение для проверки того, является ли пользователь активным сотрудником
    """

    def has_permission(self, request, view):
        """
        Возвращает True, если пользователь аутентифицирован и является активным сотрудником,
        в противном случае возвращает False
        """
        return request.user and request.user.is_authenticated and request.user.is_active
