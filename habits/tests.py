from unittest import TestCase
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from habits.tasks import send_telegram_message
from users.models import User


class HabitTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="22:37:00",
            action="Идти спать",
            is_pleasant=False,
            reward="Шоколадка",
            frequency_days=1,
            estimated_time_seconds=60,
            is_public=True,
        )
        self.client.force_authenticate(user=self.user)

    def test_habit_retrieve(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("action"), self.habit.action)

    def test_habit_create(self):
        url = reverse("habits:habit-list")
        data = {
            "place": "Дом",
            "time": "22:37:00",
            "action": "Идти спать",
            "is_pleasant": False,
            "reward": "Шоколадка",
            "frequency_days": 1,
            "estimated_time_seconds": 60,
            "is_public": True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.all().count(), 2)

    def test_course_update(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        data = {"reward": "Шоколад"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("reward"), "Шоколад")

    def test_course_delete(self):
        url = reverse("habits:habit-detail", args=(self.habit.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.all().count(), 0)

    def test_course_list(self):
        url = reverse("habits:habit-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "action": self.habit.action,
                    "estimated_time_seconds": self.habit.estimated_time_seconds,
                    "frequency_days": self.habit.frequency_days,
                    "id": self.habit.id,
                    "is_pleasant": self.habit.is_pleasant,
                    "is_public": self.habit.is_public,
                    "place": self.habit.place,
                    "related_habit": self.habit.related_habit,
                    "reward": self.habit.reward,
                    "time": "22:37:00",
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)


class SendTelegramMessageTaskTest(TestCase):
    @patch("habits.tasks.requests.post")
    def test_send_telegram_message(self, mock_post):
        # Настраиваем mock-объект, чтобы вернуть нужный json
        mock_post.return_value.json.return_value = {"ok": True, "result": {}}

        chat_id = 12345
        text = "Test message"

        result = send_telegram_message(chat_id, text)

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args

        # Проверяем, что запрос отправлен на правильный URL
        self.assertIn("sendMessage", args[0])

        # Проверяем, что payload содержит chat_id и text
        self.assertEqual(kwargs["data"]["chat_id"], chat_id)
        self.assertEqual(kwargs["data"]["text"], text)

        # Проверяем, что результат функции — это то, что вернул mock
        self.assertEqual(result, {"ok": True, "result": {}})
