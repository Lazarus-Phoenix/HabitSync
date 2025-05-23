import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="test@example.com",
        password="testpass123",
        tg_chat_id="123456",  # Используем существующее поле вместо username
    )
    assert user.email == "test@example.com"
    assert user.check_password("testpass123")
    assert not user.is_staff
    assert not user.is_superuser


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        email="admin@example.com",
        password="adminpass123",
        tg_chat_id="654321",  # Используем существующее поле вместо username
    )
    assert user.email == "admin@example.com"
    assert user.check_password("adminpass123")
    assert user.is_staff
    assert user.is_superuser
