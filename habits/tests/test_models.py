import pytest
from django.contrib.auth import get_user_model

from habits.models import Habit

User = get_user_model()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="habituser@example.com", password="testpass123", tg_chat_id="789789"
    )


@pytest.mark.django_db
def test_create_habit(test_user):
    habit = Habit.objects.create(
        user=test_user,
        place="Home",
        time="12:00:00",
        action="Read a book",
        is_pleasant=False,
        frequency=1,
        reward="Watch TV",
        duration=120,
        is_public=True,
    )
    assert habit.user == test_user
    assert habit.action == "Read a book"
