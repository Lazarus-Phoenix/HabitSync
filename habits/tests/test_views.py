import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User
from habits.models import Habit


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpass123",
        username="testuser"  # Явно передаем username
    )


@pytest.fixture
def authenticated_client(test_user):
    client = APIClient()
    client.force_authenticate(user=test_user)
    return client


@pytest.mark.django_db
def test_create_habit_authenticated(authenticated_client):
    data = {
        "place": "Test Place",
        "time": "10:00:00",
        "action": "Test Action",
        "is_pleasant": False,
        "periodicity": 1,
        "reward": "Test Reward",
        "time_to_complete": 120,
        "is_public": False,
    }
    url = reverse("habit-list")
    response = authenticated_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_habit_list_unauthenticated(api_client):
    url = reverse("habit-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_habit_list_authenticated(authenticated_client):
    Habit.objects.create(
        user=authenticated_client.user,
        place="Test Place",
        time="10:00:00",
        action="Test Action",
        is_pleasant=False,
        periodicity=1,
        reward="Test Reward",
        time_to_complete=120,
        is_public=False,
    )
    url = reverse("habit-list")
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
