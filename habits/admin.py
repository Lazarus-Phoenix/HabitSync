from django.contrib import admin

from habits.models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    # Базовые настройки отображения
    list_display = [
        "id",
        "user",
        "action",
        "time",
        "place",
        "reward",
        "pleasant_habit",
        "related_habit",
        "periodicity",
        "duration",
        "is_public",
    ]

    # Расширенные фильтры для удобства поиска
    list_filter = [
        "action",
        "user",
        "is_public",
        "periodicity",
    ]

    # Поля для поиска
    search_fields = [
        "action",
        "place",
        "reward",
    ]

    # Добавляем обработку ошибок при отображении связанных полей
    def pleasant_habit(self, obj):
        return getattr(obj.pleasant_habit, "action", "-") if obj.pleasant_habit else "-"

    def related_habit(self, obj):
        return getattr(obj.related_habit, "action", "-") if obj.related_habit else "-"

    # Добавляем короткие описания для админки
    pleasant_habit.short_description = "Положительная привычка"
    related_habit.short_description = "Связанная привычка"
