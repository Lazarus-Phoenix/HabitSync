import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from habits.models import Habit
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpass123"
    )


@pytest.fixture
def test_habit(test_user):
    return Habit.objects.create(
        user=test_user,
        title="Test Habit",
        frequency="daily"
    )


@pytest.mark.django_db
def test_create_habit_authenticated(api_client, test_user):
    api_client.force_authenticate(user=test_user)
    url = reverse("habit-list")
    data = {
        "title": "New Habit",
        "frequency": "weekly",
        "time": "08:00:00"
    }

    response = api_client.post(url, data)
    assert response.status_code == 201
    assert Habit.objects.filter(title="New Habit").exists()


@pytest.mark.django_db
def test_habit_list_unauthenticated(api_client):
    url = reverse("habit-list")
    response = api_client.get(url)
    assert response.status_code == 401