from celery import shared_task
from django.contrib.auth import get_user_model

from habits.services import message_generator, send_tg_message


@shared_task
def reminder_of_habits():
    User = get_user_model()

    for user in User.objects.filter(tg_chat_id__isnull=False):
        messages = message_generator(user)
        for msg in messages:
            try:
                send_tg_message(msg["message"], msg["chat_id"])
                print(
                    f"Сообщение отправлено {msg['chat_id']}: {msg['message']}"
                )  # Логирование
            except Exception as e:
                print(f"Ошибка отправки от пользователя {msg['chat_id']}: {str(e)}")
