from django.core.exceptions import ValidationError


def validate_reward_and_related_habit(habit):
    """Исключить одновременный выбор связанной привычки и указания вознаграждения."""
    if habit.reward and habit.related_habit:
        raise ValidationError(
            "Заполните только одно из двух полей: 'Награда' или 'Связанная привычка'."
        )


def validate_duration(habit):
    """Время выполнения должно быть не больше 120 секунд."""
    if habit.duration is None:
        raise ValidationError(
            "Продолжительность выполнения привычки не может быть пустой."
        )
    if habit.duration > 120:
        raise ValidationError(
            "Продолжительность выполнения привычки не может превышать 120 секунд."
        )


def validate_related_habit_pleasant(habit):
    """В связанные привычки могут попадать только привычки с признаком приятной привычки."""
    if habit.related_habit and not habit.related_habit.pleasant_habit:
        raise ValidationError(
            "Связанные привычки должны быть с признаком 'Приятная привычка'."
        )


def validate_pleasant_habit(habit):
    """У приятной привычки не может быть вознаграждения или связанной привычки."""
    if habit.pleasant_habit and (habit.reward or habit.related_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки."
        )


def validate_periodicity(habit):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    if habit.periodicity < 1 or habit.periodicity > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней.")


def validate_habit_execution(habit):
    """Нельзя не выполнять привычку более 7 дней."""
    if habit.periodicity < 1 or habit.periodicity > 7:
        raise ValidationError("Периодичность должна составлять от 1 до 7 дней.")
