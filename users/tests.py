from django.core.management import call_command
from django.test import TestCase

from users.models import User


class CreateAdminCommandTest(TestCase):
    def test_create_admin_user(self):
        # Запускаем команду
        call_command("csu")

        # Проверяем, что пользователь с нужным email создан
        user = User.objects.filter(email="admin@example.ru").first()
        self.assertIsNotNone(user, "Пользователь admin@example.ru не создан")

        # Проверяем права пользователя
        self.assertTrue(user.is_staff, "Пользователь не является staff")
        self.assertTrue(user.is_active, "Пользователь не активен")
        self.assertTrue(user.is_superuser, "Пользователь не является superuser")

        # Проверяем пароль
        self.assertTrue(user.check_password("123qwe"), "Пароль пользователя неверный")
