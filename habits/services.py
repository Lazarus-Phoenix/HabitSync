import requests
from django.utils import timezone

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL
from habits.models import Habit


def send_tg_message(message, chat_id):
    """Отправка сообщения в Telegram с обработкой ошибок"""
    try:
        response = requests.get(
            f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage",
            params={"chat_id": chat_id, "text": message},
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Telegram API error: {e}")
        return None


# def message_generator(user):
#     """Функция генерирует сообщения пользователю с напоминаниями о привычках."""
#     current_time = timezone.now().time()
#
#     habits = Habit.objects.filter(user=user, time__gte=current_time)
#
#     messages = []
#     for habit in habits:
#         if habit.user.tg_chat_id:
#             message = (
#                 f"Напоминание: '{habit.action}' "
#                 f"в {habit.time.strftime('%H:%M')} "
#                 f"в месте: '{habit.place}'."
#             )
#
#             if habit.reward:
#                 message += f" Награда: '{habit.reward}'."
#
#             messages.append({
#                 "chat_id": habit.user.tg_chat_id,
#                 "message": message,
#             })
#
#     return messages

from django.utils import timezone
from datetime import timedelta


def message_generator(user):
    """Генерирует сообщения о привычках, которые должны выполниться в ближайший час."""
    current_time = timezone.now().time()
    next_hour = (timezone.now() + timedelta(hours=1)).time()

    habits = Habit.objects.filter(
        user=user,
        time__gte=current_time,
        time__lte=next_hour
    )

    messages = []
    for habit in habits:
        if habit.user.tg_chat_id:
            message = (
                f"⏰ Напоминание: '{habit.action}' "
                f"в {habit.time.strftime('%H:%M')} "
                f"в месте: '{habit.place}'"
            )
            if habit.reward:
                message += f"\n🏆 Награда: '{habit.reward}'"

            messages.append({
                "chat_id": habit.user.tg_chat_id,
                "message": message
            })

    return messages