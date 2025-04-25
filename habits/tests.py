from django.test import TestCase
from django.core.exceptions import ValidationError
from habits.models import Habit
from users.models import User

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", email="test@test.com")
        self.related_habit = Habit.objects.create(
            user=self.user,
            place="Home",
            action="Meditate",
            time_required=10,
            is_pleasant=True
        )

    def test_habit_creation(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Park",
            action="Running",
            time_required=30,
            periodicity=7,
            reward="Coffee"
        )
        self.assertEqual(habit.__str__(), "Running at Park")

    def test_invalid_time_required(self):
        with self.assertRaises(ValidationError):
            habit = Habit(
                user=self.user,
                action="Invalid Habit",
                time_required=500  # >120 секунд
            )
            habit.full_clean()  # Вызовет ValidationError

    def test_related_habit_and_reward_conflict(self):
        habit = Habit(
            user=self.user,
            action="Test",
            related_habit=self.related_habit,
            reward="Chocolate",
            time_required=15
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

from rest_framework.test import APITestCase
from rest_framework import status
from habits.models import Habit
from users.models import User

class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            action="Reading",
            time_required=20
        )

    def test_create_habit(self):
        response = self.client.post(
            "/api/habits/",
            {
                "place": "Office",
                "action": "Drink water",
                "time_required": 5,
                "periodicity": 1
            },)

# habits/tests/test_models.py
from django.test import TestCase
from habits.models import Habit
from users.models import User

class HabitModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            action="Read",
            time_required=15,
            is_pleasant=False
        )

    def test_habit_creation(self):
        self.assertEqual(self.habit.action, "Read")
        self.assertEqual(self.habit.time_required, 15)

    def test_invalid_time_required(self):
        habit = Habit(
            user=self.user,
            action="Invalid",
            time_required=500  # >120 секунд
        )
        with self.assertRaises(ValidationError):
            habit.full_clean()

# habits/tests/test_views.py
from rest_framework.test import APITestCase
from habits.models import Habit

class HabitAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="123")
        self.client.force_authenticate(user=self.user)

    def test_create_habit(self):
        response = self.client.post(
            "/api/habits/",
            {"action": "Run", "time_required": 30},
            format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Habit.objects.count(), 1)

    def test_public_habits_list(self):
        Habit.objects.create(action="Public", is_public=True, user=self.user)
        response = self.client.get("/api/habits/public/")
        self.assertEqual(len(response.data), 1)


# habits/tests/test_validators.py
from django.core.exceptions import ValidationError
from habits.validators import validate_duration

class ValidatorsTest(TestCase):
    def test_valid_time(self):
        validate_duration(120)  # Не должно вызывать ошибку

    def test_invalid_time(self):
        with self.assertRaises(ValidationError):
            validate_duration(121)

from unittest import TestCase
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from config.settings import TELEGRAM_BOT_TOKEN, TELEGRAM_URL

from .models import Habit
from .services import message_generator, send_tg_message
from .tasks import reminder_of_habits

User = get_user_model()


class ReminderOfHabitsTests(TestCase):
    @patch("habits.tasks.send_tg_message")
    @patch("habits.tasks.message_generator")
    def test_reminder_of_habits_with_users(
        self, mock_message_generator, mock_send_tg_message
    ):
        # Настраиваем тестовых пользователей
        user_with_chat_id = User.objects.create(
            email="test@user1.ru", tg_chat_id="123456"
        )

        # Настраиваем возвращаемое значение для message_generator
        mock_message_generator.return_value = {
            "Test message 1": user_with_chat_id.tg_chat_id,
        }

        # Вызываем нашу задачу
        reminder_of_habits()

        # Проверяем, что message_generator был вызван один раз
        mock_message_generator.assert_called_once_with(user=user_with_chat_id)

    @patch("habits.tasks.send_tg_message")
    @patch("habits.tasks.message_generator")
    def test_reminder_of_habits_no_users(
        self, mock_message_generator, mock_send_tg_message
    ):
        # Убедимся, что нет пользователей в базе данных
        self.assertEqual(User.objects.count(), 0)
        reminder_of_habits()

        # Проверяем, что send_tg_message не был вызван
        mock_send_tg_message.assert_not_called()

    @patch("habits.tasks.send_tg_message")
    @patch("habits.tasks.message_generator")
    def test_reminder_of_habits_multiple_users(
        self, mock_message_generator, mock_send_tg_message
    ):
        # Создаем нескольких пользователей
        user1 = User.objects.create(email="test@user3.ru", tg_chat_id="123")
        user2 = User.objects.create(email="test@user4.ru", tg_chat_id="456")

        # Настраиваем возвращаемое значение для message_generator
        mock_message_generator.side_effect = [
            {"Message for user 1": user1.tg_chat_id},
            {"Message for user 2": user2.tg_chat_id},
        ]

        # Вызываем нашу задачу
        reminder_of_habits()

        # Проверяем, что message_generator был вызван для каждого пользователя
        self.assertEqual(mock_message_generator.call_count, 2)

        # Проверяем, что send_tg_message был вызван дважды с правильными параметрами
        mock_send_tg_message.assert_any_call(
            message="Message for user 1", chat_id="123"
        )
        mock_send_tg_message.assert_any_call(
            message="Message for user 2", chat_id="456"
        )

    def tearDown(self):
        # Очищаем базу данных после теста
        User.objects.all().delete()


class NotificationTests(APITestCase):

    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(
            email="test@example.com", password="password123", tg_chat_id="123456789"
        )

        # Создание тестовой привычки
        Habit.objects.create(
            user=self.user,
            action="Пить воду",
            time="12:00",
            place="Кухня",
            reward="1 балл",
            duration=60,
            is_public=True,
        )

    @patch("habits.services.requests.get")
    def test_send_tg_message(self, mock_get):
        message = "Тестовое сообщение"
        chat_id = "123456789"

        send_tg_message(message, chat_id)

        # Проверяем, что запрос был отправлен
        self.assertTrue(mock_get.called)

        # Проверяем, что запрос отправлен с правильными параметрами
        params = {
            "text": message,
            "chat_id": chat_id,
        }
        mock_get.assert_called_once_with(
            f"{TELEGRAM_URL}{TELEGRAM_BOT_TOKEN}/sendMessage", params=params
        )

    def test_message_generator(self):
        # Генерация сообщений для пользователя
        messages = message_generator(self.user)

        # Проверка, что сообщения сгенерированы правильно
        self.assertEqual(messages["chat_id"], self.user.tg_chat_id)
        self.assertIn("Напоминание: 'Пить воду'", messages["message"])
        self.assertIn("в 12:00", messages["message"])
        self.assertIn("в месте: 'Кухня'.", messages["message"])
        self.assertIn("Награда: '1 балл'.", messages["message"])

    def tearDown(self):
        # Очистка после тестов
        self.user.delete()


class HabitTests(APITestCase):

    def setUp(self):
        """Создание пользователя и привычки для тестов."""
        self.user = User.objects.create(email="test@user.ru")
        self.client.force_authenticate(user=self.user)

    def test_create_habit_success(self):
        """Тест успешного создания привычки."""
        data = {
            "action": "Чтение книги",
            "time": "10:00:00",
            "place": "Библиотека",
            "reward": "Уроки",
            "pleasant_habit": False,
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        url = reverse("habits:habits-list")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
        self.assertEqual(Habit.objects.get().action, "Чтение книги")

    def test_create_habit_with_reward_and_related_habit(self):
        """Тест создания привычки с наградой и связанной привычкой."""
        related_habit = Habit.objects.create(
            user=self.user,
            action="Заботиться о здоровье",
            time="09:00:00",
            place="Тренажерный зал",
            reward=None,
            pleasant_habit=True,
            periodicity=1,
            duration=60,
            is_public=False,
        )
        data = {
            "action": "Пить воду",
            "time": "08:00:00",
            "place": "Кухня",
            "reward": "Уроки",
            "related_habit": related_habit.id,
            "pleasant_habit": False,
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        url = reverse("habits:habits-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_habit_periodicity_validation(self):
        """Тест валидации периодичности привычки."""
        data = {
            "action": "Заниматься спортом",
            "time": "07:00:00",
            "place": "Стадион",
            "reward": None,
            "pleasant_habit": False,
            "periodicity": 8,  # Неверная периодичность
            "duration": 60,
            "is_public": False,
        }
        url = reverse("habits:habits-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Периодичность должна быть от 1 до 7 дней", str(response.data))

    def test_get_user_habits(self):
        """Тест получения привычек пользователя."""
        Habit.objects.create(
            user=self.user,
            action="Пить воду",
            time="08:00:00",
            place="Кухня",
            reward=None,
            pleasant_habit=False,
            periodicity=1,
            duration=60,
            is_public=False,
        )
        url = reverse("habits:habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_public_habits(self):
        """Тест получения публичных привычек."""
        Habit.objects.create(
            user=self.user,
            action="Чтение книги",
            time="10:00:00",
            place="Библиотека",
            reward=None,
            pleasant_habit=False,
            periodicity=1,
            duration=60,
            is_public=True,
        )
        url = reverse("habits:habits-list") + "?public=True"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().count(), 1)

    def test_habit_duration_validation(self):
        """Тест валидации продолжительности привычки."""
        data = {
            "action": "Заниматься спортом",
            "time": "07:00:00",
            "place": "Стадион",
            "reward": None,
            "pleasant_habit": False,
            "periodicity": 1,
            "duration": 130,  # Неверная продолжительность
            "is_public": False,
        }
        url = reverse("habits:habits-list")
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Продолжительность выполнения привычки не может превышать 120 секунд",
            str(response.data),
        )

    def test_update_habit(self):
        """Тест обновления привычки."""
        habit = Habit.objects.create(
            user=self.user,
            action="Смотреть фильмы",
            time="20:00:00",
            place="Дом",
            reward="Уроки",
            pleasant_habit=False,
            periodicity=1,
            duration=60,
            is_public=False,
        )
        data = {
            "action": "Смотреть сериалы",
            "time": "20:30:00",
            "place": "Дом",
            "reward": "Уроки",
            "pleasant_habit": False,
            "periodicity": 1,
            "duration": 60,
            "is_public": False,
        }
        url = reverse("habits:habits-list")
        response = self.client.put(f"{url}{habit.id}/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        habit.refresh_from_db()
        self.assertEqual(habit.action, "Смотреть сериалы")

    def test_delete_habit(self):
        """Тест удаления привычки."""
        habit = Habit.objects.create(
            user=self.user,
            action="Смотреть фильмы",
            time="20:00:00",
            place="Дом",
            reward="Уроки",
            pleasant_habit=False,
            periodicity=1,
            duration=60,
            is_public=False,
        )
        url = reverse("habits:habits-list")
        response = self.client.delete(f"{url}{habit.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Habit.objects.count(), 0)