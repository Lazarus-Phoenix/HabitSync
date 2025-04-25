from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "phone": "1234567890",
            "avatar": None,
            "tg_nick": "testnick",
            "tg_chat_id": "1295919455",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Проверка создания нового пользователя."""
        User.objects.all().delete()
        url = reverse("users:users-list")  # Замените на правильный URL
        response = self.client.post(url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)  # Один уже создан в setUp
        self.assertEqual(
            User.objects.get(email="testuser@example.com").email, "testuser@example.com"
        )

    def test_create_user_without_email(self):
        url = reverse("users:users-list")
        data = self.user_data.copy()
        data["email"] = ""
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_superuser(self):
        url = reverse("users:users-list")
        superuser_data = {
            "email": "superuser@example.com",
            "password": "superpassword",
            "is_staff": True,
            "is_superuser": True,
        }
        response = self.client.post(url, superuser_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.count(), 2
        )  # Один из setUp и один суперпользователь
        self.assertTrue(User.objects.get(email="superuser@example.com").is_superuser)

    def test_user_list(self):
        url = reverse("users:users-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_detail(self):
        url = reverse("users:users-list") + f"{self.user.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

# users/tests/test_models.py
from django.test import TestCase
from users.models import User

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create(username="test", email="test@test.com")
        self.assertEqual(user.email, "test@test.com")

# users/tests/test_auth.py
from rest_framework.test import APITestCase

class AuthTest(APITestCase):
    def test_register(self):
        response = self.client.post(
            "/api/auth/register/",
            {"username": "newuser", "password": "123", "email": "new@test.com"}
        )
        self.assertEqual(response.status_code, 201)

    def test_login(self):
        User.objects.create_user(username="test", password="123")
        response = self.client.post(
            "/api/auth/token/",
            {"username": "test", "password": "123"}
        )
        self.assertIn("access", response.data)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import User


class UserTests(APITestCase):

    def setUp(self):
        self.user_data = {
            "email": "testuser@example.com",
            "password": "testpassword",
            "phone": "1234567890",
            "avatar": None,
            "tg_nick": "testnick",
            "tg_chat_id": "1295919455",
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_create_user(self):
        """Проверка создания нового пользователя."""
        User.objects.all().delete()
        url = reverse("users:users-list")  # Замените на правильный URL
        response = self.client.post(url, self.user_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)  # Один уже создан в setUp
        self.assertEqual(
            User.objects.get(email="testuser@example.com").email, "testuser@example.com"
        )

    def test_create_user_without_email(self):
        url = reverse("users:users-list")
        data = self.user_data.copy()
        data["email"] = ""
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)

    def test_create_superuser(self):
        url = reverse("users:users-list")
        superuser_data = {
            "email": "superuser@example.com",
            "password": "superpassword",
            "is_staff": True,
            "is_superuser": True,
        }
        response = self.client.post(url, superuser_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            User.objects.count(), 2
        )  # Один из setUp и один суперпользователь
        self.assertTrue(User.objects.get(email="superuser@example.com").is_superuser)

    def test_user_list(self):
        url = reverse("users:users-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_detail(self):
        url = reverse("users:users-list") + f"{self.user.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)