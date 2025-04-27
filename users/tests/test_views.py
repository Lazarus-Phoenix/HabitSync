import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from users.models import User


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpass123",
        name="Test User"
    )


@pytest.mark.django_db
def test_register_user(api_client):
    url = reverse("register")
    data = {
        "email": "newuser@example.com",
        "password": "newpass123",
        "name": "New User"
    }

    response = api_client.post(url, data)
    assert response.status_code == 201
    assert User.objects.filter(email=data["email"]).exists()


@pytest.mark.django_db
def test_login_user(api_client, test_user):
    url = reverse("login")
    data = {
        "email": "testuser@example.com",
        "password": "testpass123"
    }

    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.data
    assert "refresh" in response.data