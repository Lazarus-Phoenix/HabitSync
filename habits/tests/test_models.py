import pytest
from datetime import date, time
from habits.models import Habit
from users.models import User


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="habituser@example.com",
        password="testpass123"
    )


@pytest.mark.django_db
def test_create_habit(test_user):
    habit = Habit.objects.create(
        user=test_user,
        title="Morning Exercise",
        description="15-minute morning routine",
        time=time(7, 30),
        date=date.today(),
        frequency="daily"
    )

    assert habit.title == "Morning Exercise"
    assert habit.frequency == "daily"
    assert str(habit.time) == "07:30:00"
    assert habit.is_completed is False