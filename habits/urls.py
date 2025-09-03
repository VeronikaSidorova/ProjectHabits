from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .apps import HabitsConfig
from .views import HabitViewSet

app_name = HabitsConfig.name

router = SimpleRouter()
router.register("", HabitViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
