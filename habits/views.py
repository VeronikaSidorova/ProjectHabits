from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.pagination import HabitPagination
from habits.permissions import IsOwnerOrReadOnly
from habits.serializers import HabitSerializer


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()
    serializer_class = HabitSerializer
    pagination_class = HabitPagination

    def get_permissions(self):
        if self.action == "list_public":
            return [AllowAny()]  # Публичные привычки доступны всем
        return [IsAuthenticated(), IsOwnerOrReadOnly()]

    def get_queryset(self):
        if self.action == "list_public":
            return Habit.objects.filter(is_public=True)
        return Habit.objects.filter(user=self.request.user)

    @action(detail=False, methods=["get"], url_path="public")
    def list_public(self, request):
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
