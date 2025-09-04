from django.core.exceptions import ValidationError
from django.db import models

from users.models import User


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255, blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)  # Признак приятной привычки
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        limit_choices_to={"is_pleasant": True},
        related_name="related_to",
        help_text="Связанная приятная привычка (только для полезных привычек)",
    )
    reward = models.CharField(max_length=255, blank=True, null=True)
    frequency_days = models.PositiveIntegerField(
        default=1, help_text="Периодичность в днях (1-7)"
    )
    estimated_time_seconds = models.PositiveIntegerField(
        default=120, help_text="Время на выполнение (секунды, макс 120)"
    )
    is_public = models.BooleanField(default=False)

    def clean(self):
        # Исключить одновременный выбор связанной привычки и вознаграждения
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        # У приятной привычки не может быть вознаграждения или связанной привычки
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # Время выполнения не больше 120 секунд
        if self.estimated_time_seconds > 120:
            raise ValidationError("Время выполнения не может быть больше 120 секунд.")

        # Периодичность: не реже 1 раза в 7 дней
        if not (1 <= self.frequency_days <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} by {self.user.email}"
