from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "password",
            "username",
            "id",
            "email",
            "phone",
            "tg_nik",
            "telegram_chat_id",
        )

class UserProfileSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "tg_nik",
            "telegram_chat_id",
        )