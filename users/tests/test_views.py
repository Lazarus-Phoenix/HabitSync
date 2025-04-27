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
def test_login_user(api_client, test_user):
    url = reverse("users:login")  # Используем namespace:name
    data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.data

@pytest.mark.django_db
def test_register_user(api_client):
    data = {
        "email": "newuser@example.com",
        "password": "newpass123",
        "tg_chat_id": "456456"
    }
    url = reverse("users:register")  # Используем namespace:name
    response = api_client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(email="newuser@example.com").exists()