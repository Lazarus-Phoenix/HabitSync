import requests
from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL
from habits.models import Habit
from django.utils import timezone
from datetime import timedelta

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
        print(f"Telegram API не сработал: {e}")
        return None


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
                f"⏰ Напоминание: Задача '{habit.action}' "
                f"в {habit.time.strftime('%H:%M')} "
                f"место выполнения: '{habit.place}'"
            )
            if habit.reward:
                message += f"\n🏆 Награда: за выполнение вы получите'{habit.reward}'"

            messages.append({
                "chat_id": habit.user.tg_chat_id,
                "message": message
            })

    return messages
