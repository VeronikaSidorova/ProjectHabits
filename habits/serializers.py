from rest_framework import serializers

from habits.models import Habit


class HabitSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Habit
        fields = "__all__"

    def validate(self, data):
        reward = data.get("reward")
        related_habit = data.get("related_habit")
        is_pleasant = data.get("is_pleasant", False)
        estimated_time_seconds = data.get("estimated_time_seconds", 120)
        frequency_days = data.get("frequency_days", 1)

        # Исключить одновременный выбор
        if reward and related_habit:
            raise serializers.ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        # Приятная привычка без reward/related
        if is_pleasant and (reward or related_habit):
            raise serializers.ValidationError(
                "У приятной привычки не может быть вознаграждения или связанной привычки."
            )

        # Время > 120 сек
        if estimated_time_seconds > 120:
            raise serializers.ValidationError(
                "Время выполнения не может быть больше 120 секунд."
            )

        # Периодичность 1-7 дней
        if not (1 <= frequency_days <= 7):
            raise serializers.ValidationError(
                "Периодичность должна быть от 1 до 7 дней."
            )

        # Связанная привычка должна быть приятной
        if related_habit and not related_habit.is_pleasant:
            raise serializers.ValidationError(
                "Связанная привычка должна быть приятной."
            )

        return data
