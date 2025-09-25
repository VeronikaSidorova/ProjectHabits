import requests
from celery import shared_task
from django.utils import timezone

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL
from habits.models import Habit


@shared_task
def send_telegram_message(chat_id, text):
    url = f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
    }
    resp = requests.post(url, data=payload)
    return resp.json()


@shared_task
def send_due_reminders():
    now = timezone.localtime().replace(second=0, microsecond=0).time()

    habits_due = Habit.objects.filter(time=now)
    for habit in habits_due:
        user = habit.user
        if user.telegram_chat_id:
            text = f"Напоминание: пора выполнить привычку '{habit.action}'! Вознаграждение: '{habit.reward}'"
            send_telegram_message.delay(user.telegram_chat_id, text)
