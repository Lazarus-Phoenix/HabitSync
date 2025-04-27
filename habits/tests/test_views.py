import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpass123",
        tg_chat_id="123123"
    )

@pytest.mark.django_db
def test_create_habit_authenticated(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    url = reverse("habits:habits-list")  # Используем namespace:basename
    data = {
        "place": "Home",
        "time": "12:00:00",
        "action": "Read a book",
        "is_pleasant": False,
        "frequency": 1,
        "reward": "Watch TV",
        "duration": 120,
        "is_public": True
    }
    response = api_client.post(url, data)
    assert response.status_code == 201

@pytest.mark.django_db
def test_habit_list_unauthenticated(api_client):
    url = reverse("habits:habits-list")  # Используем namespace:basename
    response = api_client.get(url)
    assert response.status_code == 401  # Unauthorized

@pytest.mark.django_db
def test_habit_list_authenticated(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    url = reverse("habits:habits-list")  # Используем namespace:basename
    response = api_client.get(url)
    assert response.status_code == 200