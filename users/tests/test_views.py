import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpass123",
        username="testuser"  # Явно передаем username
    )

@pytest.fixture
def api_client():
    return APIClient()

@pytest.mark.django_db
def test_login_user(api_client, test_user):
    data = {
        "email": "testuser@example.com",
        "password": "testpass123",
    }
    url = reverse("login")
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_register_user(api_client):
    data = {
        "email": "newuser@example.com",
        "password": "newpass123",
        "username": "newuser" # Явно передаем username
    }
    url = reverse("register")
    response = api_client.post(url, data=data)
    assert response.status_code == status.HTTP_201_CREATED
