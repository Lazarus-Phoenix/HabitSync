import pytest
from django.contrib.auth import get_user_model

from habits.models import Habit

User = get_user_model()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="habituser@example.com",
        password="testpass123",
        username="habituser"  # Явно передаем username
    )


@pytest.mark.django_db
def test_create_habit(test_user):
    habit = Habit.objects.create(
        user=test_user,
        place="Test Place",
        time="10:00:00",
        action="Test Action",
        is_pleasant=False,
        periodicity=1,
        reward="Test Reward",
        time_to_complete=120,
        is_public=False,
    )
    assert habit.user == test_user
    assert habit.place == "Test Place"
    assert habit.time == "10:00:00"
    assert habit.action == "Test Action"
    assert habit.is_pleasant == False
    assert habit.periodicity == 1
    assert habit.reward == "Test Reward"
    assert habit.time_to_complete == 120
    assert habit.is_public == False
