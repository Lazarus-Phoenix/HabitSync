from celery import shared_task

from habits.services import message_generator, send_tg_message


from django.contrib.auth import get_user_model

@shared_task
def reminder_of_habits():
    User = get_user_model()

    for user in User.objects.filter(tg_chat_id__isnull=False):
        messages = message_generator(user)
        for msg in messages:
            try:
                send_tg_message(msg['message'], msg['chat_id'])
                print(f"Sent to {msg['chat_id']}: {msg['message']}")  # Логирование
            except Exception as e:
                print(f"Error sending to {msg['chat_id']}: {str(e)}")


# from users.models import User


# @shared_task
# def reminder_of_habits():
#     """Задача: напоминание о привычках"""
#     users = User.objects.all()
#     user_dict = {}
#     for user in users:
#         if user.tg_chat_id:
#             user_dict = message_generator(user=user)
#         if user_dict:
#             for message, chat_id in user_dict.items():
#                 send_tg_message(message=message, chat_id=chat_id)