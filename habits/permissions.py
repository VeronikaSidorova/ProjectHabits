from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Пользователь может редактировать/удалять только свои привычки.
    Публичные привычки доступны всем на чтение.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено для всех
        if request.method in permissions.SAFE_METHODS:
            return True
        # Запись только для владельца
        return obj.user == request.user
